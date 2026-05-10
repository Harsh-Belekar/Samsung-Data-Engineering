"""
Generators/Service_Campaigns_Suppliers.py
==========================================
Generates three tables:
    1. service_centers.json  — 1,200 rows (configurable)  -> JSON
    2. campaigns.xlsx        — 1,000 rows (configurable)  -> XLSX
    3. suppliers.csv         —   500 rows (configurable)  -> CSV
"""

import json
import random
import string
from datetime import timedelta
import numpy as np
import pandas as pd
from Config      import ROW_COUNTS, DATE_START, DATE_END, DATE_FORMATS, QUALITY
from Master_data import (
    CITIES_STATES, CAMPAIGN_NAMES, CHANNELS, STATES,
    SUPPLIER_CATEGORIES, CITIES
)
from Utils import rnd_date, rnd_gstin, add_messy


class ServiceCenterGenerator:
    """
    Generates Samsung authorised service-centre records.

    Messiness: null capacity/phone/email, state casing errors,
    mixed is_active encodings, varied working-hours formats.
    """

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["service_centers"]
        self.out_path = f"{out_dir}/service_centers.json"

    def generate(self) -> list:
        records = []
        working_hour_formats = [
            "9AM-7PM", "10:00-18:00", "9:00 AM - 6:00 PM",
            None, "Monday-Saturday 10-7",
        ]
        centre_types = ["Service Center", "Care Center", "Service Plaza", "SmartCare"]
        tier_values  = ["Premium", "Standard", "Brand Shop", "premium", "STANDARD"]

        for i in range(self.n):
            ci               = np.random.randint(0, len(CITIES_STATES))
            city, state, pin = CITIES_STATES[ci]

            records.append({
                "center_id"       : f"SC{i + 1:04d}",
                "center_name"     : f"Samsung {random.choice(centre_types)} {city}",
                "tier"            : random.choice(tier_values) if random.random() > QUALITY["null_pct_default"] else None,
                "city"            : city,
                "state"           : state if random.random() > 0.08 else state.upper(),
                "pincode"         : pin  if random.random() > 0.06 else None,
                "phone"           : f"0{random.randint(1000000000, 9999999999)}" if random.random() > 0.03 else None,
                "email"           : f"sc{i + 1:04d}@samsung-care.in" if random.random() > 0.05 else None,
                "working_hours"   : random.choice(working_hour_formats),
                "capacity_per_day": random.randint(20, 150) if random.random() > QUALITY["null_pct_high"] else None,
                "is_active"       : random.choice(["Yes", "No", "1", "0", "Active", "Inactive"]),
            })
        return records

    def save(self, records: list) -> None:
        with open(self.out_path, "w") as f:
            json.dump(records, f, indent=2)


class CampaignGenerator:
    """
    Generates the marketing-campaign dimension table.

    Messiness: mixed date formats, budget nulls, discount stored as
    both "30%" strings and plain integers, mixed status casing.
    """

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["campaigns"]
        self.out_path = f"{out_dir}/campaigns.xlsx"

    def generate(self) -> pd.DataFrame:
        n = self.n

        start_dates = [
            DATE_START + timedelta(days=int(np.random.randint(0, (DATE_END - DATE_START).days)))
            for _ in range(n)
        ]
        end_dates = [s + timedelta(days=int(np.random.randint(7, 90))) for s in start_dates]

        budgets = [
            int(np.random.randint(500_000, 50_000_000))
            if random.random() > QUALITY["null_pct_high"] else None
            for _ in range(n)
        ]

        discounts = [
            f"{np.random.randint(5, 40)}%"
            if random.random() > QUALITY["bad_value_pct"] else str(np.random.randint(5, 40))
            for _ in range(n)
        ]

        region_pool = (
            ["Pan India", "North India", "South India", "West India", "East India",
                "Maharashtra", "Karnataka", "UP & Bihar", "Tamil Nadu", "Gujarat"]
            + list(STATES[:15])
        )
        regions = np.random.choice(region_pool, n)

        return pd.DataFrame({
            "campaign_id"    : [f"CAMP{i + 1:04d}" for i in range(n)],
            "campaign_name"  : [
                f"{random.choice(CAMPAIGN_NAMES)} {random.randint(2022, 2025)}"
                for _ in range(n)
            ],
            "type"           : np.random.choice(
                ["Digital","TV","Outdoor","In-Store","Social Media","Email","Influencer"], n
            ),
            "start_date"     : [d.strftime(random.choice(DATE_FORMATS)) for d in start_dates],
            "end_date"       : add_messy([d.strftime("%Y-%m-%d") for d in end_dates], null_pct=0.04),
            "budget_inr"     : budgets,
            "discount_pct"   : discounts,
            "target_region"  : add_messy(list(regions), null_pct=QUALITY["null_pct_default"]),
            "target_segment" : np.random.choice(
                ["All","Premium","Youth","Family","Students","Corporate"], n
            ),
            "channel"        : np.random.choice(CHANNELS, n),
            "status"         : np.random.choice(
                ["Active","Completed","Paused","Draft","cancelled","ACTIVE"], n
            ),
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_excel(self.out_path, index=False)


class SupplierGenerator:
    """
    Generates the supplier master table.

    Messiness: country-name casing errors, missing GSTIN for some
    Indian suppliers, mixed payment-term formats, null ratings.
    """

    SUPPLIER_NAMES = [
        "Dixon Technologies","Bharat FIH","Jabil India","Flextronics",
        "Foxconn India","Salcomp India","Samsung SDI","SK Hynix",
        "Qualcomm","MediaTek","BOE Technology","LG Innotek",
        "Tata Electronics","Motherson Group","Wistron India","Pegatron",
        "Inventec","Compal","Avnet India","Arrow Electronics",
        "Ingram Micro","TD Synnex","Celestica","Sanmina",
    ]
    FOREIGN_CITIES = ["Seoul","Shenzhen","Taipei","Tokyo","Berlin","Kuala Lumpur"]

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["suppliers"]
        self.out_path = f"{out_dir}/suppliers.csv"

    def generate(self) -> pd.DataFrame:
        # from Master_data import CITIES
        n = self.n

        countries = np.random.choice(
            ["India","South Korea","China","Taiwan","Vietnam",
                "Japan","USA","Germany","Malaysia","Thailand"],
            n, p=[0.40,0.20,0.15,0.08,0.05,0.04,0.03,0.02,0.02,0.01],
        )

        suffixes  = ["Ltd","Pvt Ltd","Inc","Co","GmbH","Corp"]
        sup_names = [
            f"{random.choice(self.SUPPLIER_NAMES)} {random.choice(suffixes)}"
            for _ in range(n)
        ]
        gstins = [
            rnd_gstin() if (c == "India" and random.random() > 0.10) else None
            for c in countries
        ]
        cities = [
            random.choice(CITIES) if c == "India"
            else random.choice(self.FOREIGN_CITIES)
            for c in countries
        ]
        pay_terms = np.random.choice(
            ["30","45","60","Net 30","Net 45","60 days","45 Days","30 days"], n
        )
        ratings = [
            round(random.uniform(2.5, 5.0), 1) if random.random() > 0.05 else None
            for _ in range(n)
        ]
        emails = []
        for name in sup_names:
            slug   = name.lower().replace(" ","").replace(".","")
            suffix = "".join(random.choices(string.ascii_lowercase, k=2))
            domain = "com" if random.random() > 0.3 else "in"
            emails.append(f"procurement@{slug}{suffix}.{domain}")

        return pd.DataFrame({
            "supplier_id"        : [f"SUP{i + 1:04d}" for i in range(n)],
            "supplier_name"      : sup_names,
            "country"            : [c if random.random() > 0.03 else c.lower() for c in countries],
            "city"               : cities,
            "gstin"              : gstins,
            "contact_email"      : emails,
            "payment_terms_days" : add_messy(list(pay_terms), null_pct=0.04),
            "category"           : np.random.choice(SUPPLIER_CATEGORIES, n),
            "rating"             : add_messy(ratings, null_pct=0.06),
            "is_msme"            : np.random.choice(
                ["Yes","No","1","0","TRUE"], n, p=[0.30,0.45,0.10,0.10,0.05]
            ),
            "contract_start"     : rnd_date(
                pd.Timestamp("2015-01-01").to_pydatetime(),
                pd.Timestamp("2023-01-01").to_pydatetime(), n,
            ),
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)
