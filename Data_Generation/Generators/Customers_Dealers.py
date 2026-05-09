"""
Generators/Customers_Dealers.py
================================
Generates two CSV tables:
    1. customers.csv   — 200,000 rows (configurable)
    2. dealers.csv     — 10,000  rows (configurable)

Messiness injected
------------------
Customers : mixed email duplicates, phone-number prefix variations,
            invalid PINs, mixed gender/is_active encodings,
            mixed date formats, mixed name casing.
Dealers   : tier-value casing, null store_type, mixed is_exclusive
            boolean encodings.
"""

import random
import numpy as np
import pandas as pd
from Config      import ROW_COUNTS, DATE_START, DATE_END, DATE_FORMATS, QUALITY
from Master_data import (
    FIRST_NAMES, LAST_NAMES, CITIES_STATES, RETAIL_CHAINS, STORE_TYPES,
)
from Utils import rnd_date, rnd_phone, add_messy, mess_case


class CustomerGenerator:
    """
    Generates the customers table.

    Attributes
    ----------
    cust_ids : List of all generated customer_id strings — consumed
                by downstream generators as foreign-key values.
    """

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["customers"]
        self.out_path = f"{out_dir}/customers.csv"
        self.cust_ids: list[str] = []

    def generate(self) -> pd.DataFrame:
        """Build and return the customers DataFrame."""
        n = self.n

        # IDs 
        self.cust_ids = [f"CUST{i + 1:07d}" for i in range(n)]

        # Names (with random casing mess)
        fn = np.random.choice(FIRST_NAMES, n)
        ln = np.random.choice(LAST_NAMES,  n)
        fn_messy   = mess_case(list(fn), mess_pct=0.10)
        ln_messy   = mess_case(list(ln), mess_pct=0.10)
        full_names = [f"{f} {l}" for f, l in zip(fn_messy, ln_messy)]

        # Emails (~2 % duplicates injected)
        domains = np.random.choice(
            ["gmail.com", "yahoo.com", "hotmail.com", "rediffmail.com", "outlook.com"], n
        )
        emails = [
            f"{f.lower()}.{l.lower()}{np.random.randint(1, 999)}@{d}"
            for f, l, d in zip(fn, ln, domains)
        ]
        dup_idx = np.random.choice(n, max(1, int(n * QUALITY["email_dup_pct"])), replace=False)
        for i in dup_idx:
            emails[i] = emails[np.random.randint(0, n // 2)]

        # Phones (some with +91 or leading 0)
        phones = [rnd_phone() for _ in range(n)]
        for i in np.random.choice(n, int(n * QUALITY["phone_prefix_pct"]), replace=False):
            phones[i] = "+91" + phones[i]
        for i in np.random.choice(n, int(n * 0.03), replace=False):
            phones[i] = "0" + phones[i]

        # Geography
        city_idx = np.random.randint(0, len(CITIES_STATES), n)
        cities   = [CITIES_STATES[i][0] for i in city_idx]
        states   = [CITIES_STATES[i][1] for i in city_idx]
        pincodes = [CITIES_STATES[i][2] for i in city_idx]

        # Inject invalid PINs
        pin_list = list(pincodes)
        for i in np.random.choice(n, int(n * QUALITY["invalid_pin_pct"]), replace=False):
            pin_list[i] = str(np.random.randint(100000, 999999))

        # Categorical columns
        genders = np.random.choice(
            ["Male", "Female", "male", "female", "M", "F", "Other"],
            n, p=[0.38, 0.37, 0.04, 0.04, 0.04, 0.04, 0.09],
        )
        segments = np.random.choice(
            ["Premium", "Mid-Range", "Budget", "Enterprise"],
            n, p=[0.15, 0.35, 0.40, 0.10],
        )
        is_active = np.random.choice(
            ["True", "False", "1", "0", "Yes", "No"],
            n, p=[0.70, 0.10, 0.10, 0.04, 0.03, 0.03],
        )

        # Dates
        dobs = rnd_date(pd.Timestamp("1960-01-01").to_pydatetime(),
                            pd.Timestamp("2005-12-31").to_pydatetime(), n, DATE_FORMATS)
        reg_dates = rnd_date(DATE_START, DATE_END, n)

        return pd.DataFrame({
            "customer_id"  : self.cust_ids,
            "full_name"    : full_names,
            "email"        : emails,
            "phone"        : phones,
            "city"         : cities,
            "state"        : states,
            "pincode"      : add_messy(pin_list, null_pct=QUALITY["null_pct_default"]),
            "gender"       : genders,
            "dob"          : dobs,
            "segment"      : segments,
            "registered_on": reg_dates,
            "is_active"    : is_active,
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)


class DealerGenerator:
    """
    Generates the dealers / retail-partner table.

    Attributes
    ----------
    dealer_ids : List of all generated dealer_id strings.
    """

    def __init__(self, out_dir: str):
        self.n          = ROW_COUNTS["dealers"]
        self.out_path   = f"{out_dir}/dealers.csv"
        self.dealer_ids: list[str] = []

    def generate(self) -> pd.DataFrame:
        n = self.n
        self.dealer_ids = [f"DLR{i + 1:05d}" for i in range(n)]

        ci     = np.random.randint(0, len(CITIES_STATES), n)
        chains = np.random.choice(
            RETAIL_CHAINS,
            n,
            p=[0.10, 0.10, 0.08, 0.07, 0.07, 0.06, 0.06, 0.15, 0.15, 0.16],
        )

        # Derive store type from chain
        store_types = [self._chain_to_store_type(c) for c in chains]

        # Tier values with intentional casing/encoding variants
        tiers = np.random.choice(
            ["Tier 1", "Tier 2", "Tier 3", "tier 1", "TIER1", "T1"],
            n, p=[0.25, 0.30, 0.28, 0.06, 0.06, 0.05],
        )
        is_exclusive = np.random.choice(
            ["Yes", "No", "1", "0", "TRUE", "FALSE"],
            n, p=[0.15, 0.55, 0.10, 0.10, 0.05, 0.05],
        )

        return pd.DataFrame({
            "dealer_id"    : self.dealer_ids,
            "dealer_name"  : [
                f"{random.choice(RETAIL_CHAINS)} - {CITIES_STATES[ci[i]][0]}"
                for i in range(n)
            ],
            "store_type"   : add_messy(store_types, null_pct=0.04),
            "chain"        : chains,
            "city"         : [CITIES_STATES[ci[i]][0] for i in range(n)],
            "state"        : [CITIES_STATES[ci[i]][1] for i in range(n)],
            "tier"         : add_messy(list(tiers), null_pct=0.05),
            "contact_phone": [rnd_phone() for _ in range(n)],
            "active_since" : rnd_date(pd.Timestamp("2010-01-01").to_pydatetime(),
                                        pd.Timestamp("2023-01-01").to_pydatetime(), n),
            "is_exclusive" : is_exclusive,
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)

    # private helper
    @staticmethod
    def _chain_to_store_type(chain: str) -> str:
        """Map a retail chain name to the appropriate store type."""
        if chain in ("Amazon IN", "Flipkart", "Paytm Mall"):
            return "Online Exclusive Partner"
        if chain == "Samsung SmartCafé":
            return "Samsung SmartCafé"
        if chain in ("Croma", "Reliance Digital", "Vijay Sales"):
            return random.choice(["Large Format Retail", "Multi-Brand Outlet"])
        return random.choice(STORE_TYPES)
