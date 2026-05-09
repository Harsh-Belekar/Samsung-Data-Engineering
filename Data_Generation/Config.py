"""
Config.py
=========
Central configuration for the Samsung India Data Generator.

Edit this file to control:
    - Date ranges for all generated data
    - Row counts for every table
    - Output folder and file formats
    - Data quality settings (null %, duplicate %, messy value %)

All other modules import from here — no need to touch generator files
for routine parameter changes.
"""

from datetime import datetime

# =====================================================================
# RANDOM SEEDS  (change for different data, keep fixed for repeatable runs)
# =====================================================================
NUMPY_SEED  = 42
RANDOM_SEED = 42

# =====================================================================
#  DATE RANGE  — applies to transactions, complaints, reviews, etc.
# =====================================================================
DATE_START = datetime(2022, 1, 1)    # Start date
DATE_END   = datetime(2025, 12, 31)  # End date 

# Date formats injected to simulate real-world messy ingestion
DATE_FORMATS = [
    "%Y-%m-%d",    # 2024-03-15  (standard ISO — most common)
    "%d/%m/%Y",    # 15/03/2024  (Indian style)
    "%d-%m-%Y",    # 15-03-2024
    "%m/%d/%Y",    # 03/15/2024  (US style — intentional mess)
    "%Y/%m/%d",    # 2024/03/15
    "%d %b %Y",    # 15 Mar 2024
]


# =====================================================================
# ROW COUNTS PER TABLE 
# =====================================================================
# Adjust any value below to generate more or fewer rows.
'''Tables that reference others (e.g. sales → customers) will
automatically sample from whatever pool was generated.'''

ROW_COUNTS = {
    "products"               :  2_000,    # JSON  — product catalogue
    "warehouses"             :     25,    # JSON  — Fixed; add entries in master_data.py
    "service_centers"        :  1_200,    # JSON
    "customers"              : 200_000,   # CSV
    "dealers"                :  10_000,   # CSV
    "suppliers"              :    500,    # CSV
    "sales_transactions"     : 750_000,   # CSV
    "complaints"             : 200_000,   # CSV
    "financial_transactions" : 650_000,   # CSV   (+ ~2 % duplicates injected)
    "product_reviews"        :  50_000,   # CSV
    "campaigns"              :  1_000,    # XLSX
    "employees"              :  15_000,   # XLSX
    "inventory"              : 100_000,   # XLSX
    "returns"                :  75_000,   # XLSX  (+ ~3 % duplicates injected)
}

# =====================================================================
# DATA QUALITY KNOBS
# =====================================================================
'''These percentages control intentional messiness injected to make
the dataset realistic for ETL / data-cleaning exercises.'''

QUALITY = {
    # Fraction of values replaced with None / NaN
    "null_pct_default"   : 0.03,   # 3 % nulls in most columns
    "null_pct_high"      : 0.07,   # 7 % for less-critical fields

    # Fraction of rows where a "bad" string value is injected
    "bad_value_pct"      : 0.02,

    # Fraction of email rows that are duplicate (same email, two customers)
    "email_dup_pct"      : 0.02,

    # Fraction of phone numbers that get a "+91" or "0" prefix
    "phone_prefix_pct"   : 0.06,

    # Fraction of PIN codes replaced with a random invalid PIN
    "invalid_pin_pct"    : 0.04,

    # Fraction of financial & return rows that are fully duplicated
    "fin_dup_pct"        : 0.02,
    "returns_dup_pct"    : 0.03,

    # Fraction of category names that get casing/spelling variants
    "category_mess_pct"  : 0.07,
}

# =====================================================================
# OUTPUT PATHS
# =====================================================================
OUTPUT_DIR = "./Data"   # All generated files land here
