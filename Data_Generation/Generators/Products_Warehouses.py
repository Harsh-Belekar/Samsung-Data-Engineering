"""
Generators/Products_Warehouses.py
===================================
Generates two reference tables:
    1. products.json      — 2,000 rows (configurable via ROW_COUNTS["products"])
    2. warehouses.json    — fixed 25 rows  (add rows in WAREHOUSE_DATA below)

Both are written as JSON because they are relatively small lookup
tables that are easier to inspect and ingest from JSON.
"""

import json
import random
import numpy as np
from Config  import ROW_COUNTS, QUALITY
from Master_data import SAMSUNG_PRODUCTS, COLOUR_VARIANTS, CATEGORY_MESS_MAP
from Utils   import rnd_date
from datetime import datetime


# =====================================================================
# Fixed warehouse master  (25 rows)
# Add new warehouses here; nothing else needs to change.
# =====================================================================

WAREHOUSE_DATA = [
    # (id, name, city, state, pincode, capacity_units, lat, lon, type)
    ("WH001","Noida Main Warehouse",        "Noida",             "Uttar Pradesh",  "201301",150000,"28.5355","77.3910","Primary Distribution"),
    ("WH002","Sriperumbudur Factory",        "Sriperumbudur",     "Tamil Nadu",     "602105",300000,"12.9698","79.8897","Manufacturing Hub"),
    ("WH003","Bhiwandi DC",                  "Bhiwandi",          "Maharashtra",    "421302",120000,"19.2952","73.0631","Distribution Center"),
    ("WH004","Kolkata Hub",                  "Kolkata",           "West Bengal",    "700088", 80000,"22.5726","88.3639","Regional Hub"),
    ("WH005","Hyderabad DC",                 "Hyderabad",         "Telangana",      "500055", 90000,"17.3850","78.4867","Regional Hub"),
    ("WH006","Bengaluru South",              "Bengaluru",         "Karnataka",      "560099",100000,"12.9141","77.6101","Distribution Center"),
    ("WH007","Ahmedabad Hub",                "Ahmedabad",         "Gujarat",        "382350", 70000,"23.0225","72.5714","Regional Hub"),
    ("WH008","Pune DC",                      "Pune",              "Maharashtra",    "411057", 60000,"18.5204","73.8567","Distribution Center"),
    ("WH009","Delhi NCR Hub",                "Delhi",             "Delhi",          "110020",110000,"28.7041","77.1025","Primary Distribution"),
    ("WH010","Chennai DC",                   "Chennai",           "Tamil Nadu",     "600073", 75000,"13.0827","80.2707","Distribution Center"),
    ("WH011","Jaipur Hub",                   "Jaipur",            "Rajasthan",      "302017", 45000,"26.9124","75.7873","Regional Hub"),
    ("WH012","Lucknow DC",                   "Lucknow",           "Uttar Pradesh",  "226010", 40000,"26.8467","80.9462","Distribution Center"),
    ("WH013","Patna Hub",                    "Patna",             "Bihar",          "800020", 35000,"25.5941","85.1376","Regional Hub"),
    ("WH014","Bhubaneswar DC",               "Bhubaneswar",       "Odisha",         "751010", 30000,"20.2961","85.8245","Distribution Center"),
    ("WH015","Guwahati NE Hub",              "Guwahati",          "Assam",          "781001", 25000,"26.1445","91.7362","Regional Hub"),
    ("WH016","Nagpur Central",               "Nagpur",            "Maharashtra",    "440001", 50000,"21.1458","79.0882","Distribution Center"),
    ("WH017","Surat Hub",                    "Surat",             "Gujarat",        "395010", 55000,"21.1702","72.8311","Regional Hub"),
    ("WH018","Coimbatore DC",                "Coimbatore",        "Tamil Nadu",     "641001", 40000,"11.0168","76.9558","Distribution Center"),
    ("WH019","Visakhapatnam Hub",            "Visakhapatnam",     "Andhra Pradesh", "530001", 35000,"17.6868","83.2185","Regional Hub"),
    ("WH020","Indore DC",                    "Indore",            "Madhya Pradesh", "452010", 38000,"22.7196","75.8577","Distribution Center"),
    ("WH021","Chandigarh Hub",               "Chandigarh",        "Chandigarh",     "160001", 30000,"30.7333","76.7794","Regional Hub"),
    ("WH022","Kochi DC",                     "Kochi",             "Kerala",         "682030", 35000, "9.9312","76.2673","Distribution Center"),
    ("WH023","Ludhiana Hub",                 "Ludhiana",          "Punjab",         "141001", 28000,"30.9010","75.8573","Regional Hub"),
    ("WH024","Ranchi DC",                    "Ranchi",            "Jharkhand",      "834001", 22000,"23.3441","85.3096","Distribution Center"),
    ("WH025","Thiruvananthapuram DC",        "Thiruvananthapuram","Kerala",         "695001", 20000, "8.5241","76.9366","Distribution Center"),
]


class ProductGenerator:
    """
    Generates the product catalogue as a JSON file.

    The base catalogue comes from SAMSUNG_PRODUCTS in master_data.py.
    Additional rows are created by generating colour variants of
    existing products until the target row count is reached.

    Attributes
    ----------
    n         : Total rows to generate (from ROW_COUNTS["products"]).
    out_path  : Absolute path to output JSON file.
    pid_pool  : List of all generated product_id strings — consumed
                by downstream generators that need foreign-key values.
    """

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["products"]
        self.out_path = f"{out_dir}/products.json"
        self.pid_pool: list[str] = []   # populated during generate()

    def generate(self) -> list[dict]:
        """Build and return the full product record list."""
        records = self._build_base_records()
        records += self._build_variant_records(len(records))
        self.pid_pool = [r["product_id"] for r in records]
        return records

    def save(self, records: list[dict]) -> None:
        """Serialise *records* to JSON at self.out_path."""
        with open(self.out_path, "w") as f:
            json.dump(records, f, indent=2, default=str)

    # private helpers 
    def _build_base_records(self) -> list[dict]:
        """Create one record per entry in SAMSUNG_PRODUCTS."""
        records = []
        for i, (sku, name, cat, subcat, mrp, ram, storage, disp) in enumerate(SAMSUNG_PRODUCTS):
            pid = f"PROD{i + 1:04d}"
            records.append(self._make_record(pid, sku, name, cat, subcat, mrp, ram, storage, disp))
        return records

    def _build_variant_records(self, offset: int) -> list[dict]:
        """
        Create colour-variant records until we reach self.n total rows.
        Each variant gets a modified SKU suffix and colour appended to the name.
        """
        records = []
        needed = self.n - offset
        for i in range(needed):
            sku, name, cat, subcat, mrp, ram, storage, disp = random.choice(SAMSUNG_PRODUCTS)
            colour  = random.choice(COLOUR_VARIANTS)
            var_sku = sku[:-2] + random.choice(["WH", "BL", "GR", "GD", "SL"])
            pid     = f"PROD{offset + i + 1:04d}"

            # Slightly vary MRP (±10 %)
            var_mrp = int(mrp * random.uniform(0.9, 1.1)) if random.random() > QUALITY["null_pct_default"] else None
            records.append(self._make_record(
                pid, var_sku, f"{name} {colour}",
                cat if random.random() > QUALITY["category_mess_pct"] else cat.lower(),
                subcat, var_mrp, ram, storage, disp,
            ))
        return records

    def _make_record(self, pid, sku, name, cat, subcat, mrp, ram, storage, disp) -> dict:
        """Assemble a single product dict with optional messy fields."""
        # Intentionally inject category casing errors at configured rate
        messy_cat = (
            CATEGORY_MESS_MAP.get(cat, cat)
            if random.random() < QUALITY["category_mess_pct"]
            else cat
        )
        return {
            "product_id"      : pid,
            "sku"             : sku,
            "product_name"    : name,
            "category"        : messy_cat,
            "subcategory"     : subcat,
            "mrp_inr"         : mrp if random.random() > QUALITY["null_pct_default"] else None,
            "launch_date_india": rnd_date(datetime(2020, 1, 1), datetime(2024, 6, 1), 1)[0],
            # RAM stored as string; sometimes suffixed with "gb" (messy)
            "ram_gb"          : (
                (str(ram) if random.random() > QUALITY["bad_value_pct"] else str(ram) + "gb")
                if ram else None
            ),
            # Storage stored as string; sometimes suffixed with "GB" (messy)
            "storage_gb"      : (
                (str(storage) if random.random() > QUALITY["bad_value_pct"] else str(storage) + "GB")
                if storage else None
            ),
            "display_inches"  : disp,
            "bis_certified"   : random.choice(["Yes", "yes", "YES", "No", "1", "0", "true"]),
            "warranty_years"  : str(random.choice([1, 2])) if random.random() > QUALITY["null_pct_default"] else None,
            "color_variants"  : random.randint(1, 6),
        }


class WarehouseGenerator:
    """
    Generates the warehouse reference table as a JSON file.

    The 25 warehouse records are fixed in WAREHOUSE_DATA above.
    Light messiness (null capacity, casing errors on state) is
    injected at the configured quality rates.

    Attributes
    ----------
    wh_ids    : List of all warehouse_id strings for FK use downstream.
    """

    def __init__(self, out_dir: str):
        self.out_path = f"{out_dir}/warehouses.json"
        self.wh_ids: list[str] = []

    def generate(self) -> list[dict]:
        """Build and return warehouse records."""
        records = []
        for row in WAREHOUSE_DATA:
            wid, wname, city, state, pin, cap, lat, lon, wtype = row
            self.wh_ids.append(wid)

            # Randomly uppercase state name to simulate messy ETL
            messy_state = state if random.random() > 0.10 else state.upper()

            # Occasionally corrupt latitude (replace "." with ",")
            messy_lat = lat if random.random() > 0.06 else lat.replace(".", ",")

            records.append({
                "warehouse_id"   : wid,
                "warehouse_name" : wname,
                "city"           : city,
                "state"          : messy_state,
                "pincode"        : pin if random.random() > 0.05 else None,
                "capacity_units" : cap if random.random() > QUALITY["null_pct_high"] else None,
                "latitude"       : messy_lat,
                "longitude"      : lon,
                "type"           : wtype,
            })
        return records

    def save(self, records: list[dict]) -> None:
        with open(self.out_path, "w") as f:
            json.dump(records, f, indent=2)
