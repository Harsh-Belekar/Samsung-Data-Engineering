# 🏢 SAMSUNG INDIA — RAW DATA GENERATION

## 🎯 Synthetic Data Generation Documentation — Raw Data

**Prepared by:** Harsh Belekar
**Project Phase:** Raw Data Generation
**Data Scope:** 2,000,000 Rows | 14 Tables | 6 Business Domains | CSV + JSON + XLSX
**Date Range:** January 2022 – December 2025
**Tools:** Python (Pandas, NumPy) | PostgreSQL
**Pipeline Stage:** Raw → Bronze → Silver → Gold

---

## TABLE OF CONTENTS

1. [Project Overview](#1--project-overview)
2. [Project at a Glance](#2--project-at-a-glance)
3. [Project Structure](#3-️-project-structure)
4. [Setup & Installation](#4-️-setup--installation)
5. [Configuration Guide](#5--configuration-guide)
6. [Generated Tables — All 14 Tables](#6-️-generated-tables--all-14-tables)
7. [Data Quality & Messiness Injected](#7--data-quality--messiness-injected)
8. [Running the Generator](#8-️-running-the-generator)
9. [Logs](#9--logs)
10. [Dependency Chain](#10--dependency-chain)
11. [Troubleshooting](#11-️-troubleshooting)
12. [Extending the Project](#12--extending-the-project)
13. [FAQs](#13--frequently-asked-questions)
14. [Author](#-author)

---

## 1. 🚀 PROJECT OVERVIEW

Samsung India's Data Engineering pipeline begins at the Bronze Layer — raw, unprocessed, realistic data ingested exactly as it arrives from operational systems. This project generates that Bronze Layer dataset entirely in Python, without any external data dependencies or paid data sources.

Across **14 tables**, **6 business domains**, and **2,000,000 rows**, this generator produces a dataset that mirrors what a real Samsung India data engineering team would receive from their CRM, ERP, WMS, and after-sales systems every day — including all the data quality issues that come with it.

**Why synthetic but messy?** Real enterprise data is never clean. PINs are invalid. Phone numbers arrive with `+91` prefixes. Salaries are stored as `"18 LPA"` in one column and `"150000"` in the next. Categories are sometimes `"Smartphones"`, sometimes `"smartphones"`, sometimes `"SMARTPHONES"`. This generator injects all of that intentionally — making it a genuine Bronze Layer that requires a full Silver Layer cleaning pipeline before it is analytics-ready.

**The Three Design Principles**

The first principle is **reproducibility**. Every run with the same seed (`NUMPY_SEED = 42`) produces identical data. This means pipeline bugs can be isolated, re-run, and compared deterministically.

The second principle is **configurability**. Every parameter — row counts, date ranges, null percentages, duplicate injection rates — lives in a single file: `Config.py`. No generator file needs to be touched for routine changes.

The third principle is **referential integrity**. Foreign keys are real. `sales_transactions.customer_id` references actual IDs from `customers.csv`. `inventory.warehouse_id` references actual IDs from `warehouses.json`. Downstream JOIN operations in the Silver Layer will work correctly.

---

## 2. 📊 PROJECT AT A GLANCE

| Property | Detail |
|---|---|
| **Total Rows Generated** | ~2,000,000 |
| **Total Tables** | 14 |
| **Output Formats** | CSV, JSON, XLSX |
| **Date Range** | 1 Jan 2022 → 31 Dec 2025 |
| **Business Domains** | Sales, Finance, After-Sales, HR, Inventory, Marketing |
| **Geography** | India — 50+ cities across all major states |
| **Products Covered** | Samsung Smartphones, Tablets, TVs, ACs, Washing Machines, Refrigerators |
| **Largest Table** | `sales_transactions.csv` — 750,000 rows |
| **Smallest Table** | `warehouses.json` — 25 rows (fixed) |
| **Random Seed** | 42 (fully reproducible) |
| **Estimated Total File Size** | ~300–350 MB |
| **Estimated Generation Time** | 3–8 minutes (machine dependent) |
| **Python Version Required** | 3.10+ |

### Domain Breakdown

| Domain | Tables | Total Rows |
|---|---|---|
| 🛒 Sales & Distribution (SND) | `sales_transactions`, `dealers` | 760,000 |
| 💳 Finance & Payments (FIP) | `financial_transactions` | ~663,000 |
| 👥 Customers (CRM) | `customers`, `product_reviews` | 250,000 |
| 🔧 After-Sales Service (AS2) | `complaints`, `returns`, `service_centers` | 277,450 |
| 🏭 Supply Chain & Inventory (SCI) | `inventory`, `warehouses`, `suppliers` | 100,525 |
| 📢 HR & Marketing (HRM) | `employees`, `campaigns`, `products` | 18,000 |

---

## 3. 🗂️ PROJECT STRUCTURE

```
Samsung Data Engineering/
│
├── Data Generation/
│   ├── Main.py                              ← Entry point — run this file
│   ├── Config.py                            ← ALL tunable parameters live here
│   ├── Master_Data.py                       ← Static lookup data (products, cities, names)
│   ├── Utils.py                             ← Shared helpers (dates, phones, messiness)
│   ├── requirements.txt                     ← pip dependencies
│   │
│   └── Generators/
│       ├── __init__.py
│       ├── Products_Warehouses.py           ← Tables 1 & 2
│       ├── Customers_Dealers.py             ← Tables 3 & 4
│       ├── Service_Campaigns_Suppliers.py   ← Tables 5, 6 & 7
│       ├── Employees_Inventory.py           ← Tables 8 & 9
│       └── Transactions.py                  ← Tables 10 – 14
│
├── Data/
│   └── Raw_data/                            ← All 14 generated files land here
│         ├── AS2/                           ← After-Sales Service (AS2)
│         │    ├── complaints.csv
│         │    ├── returns.xlsx
│         │    └── service_centers.json
│         ├── CRM/                           ← Customers (CRM)
│         │    ├── customers.csv
│         │    └── product_reviews.csv
│         ├── FIN/                           ← Finance & Payments (FIP)
│         │    └── financial_transactions.csv
│         ├── HRM/                           ← HR & Marketing (HRM)
│         │    ├── campaigns.xlsx
│         │    ├── employees.xlsx
│         │    └── products.json
│         ├── SCI/                           ← Supply Chain & Inventory (SCI)
│         │    ├── inventory.xlsx
│         │    ├── suppliers.csv
│         │    └── warehouses.json        
│         └── SND/                           ← Sales & Distribution (SND)
│             ├── dealers.csv
│             └── sales_transactions.csv     
└── Logs/
    └── Data_generation.log                  ← Auto-created on first run
```

### What Each File Does

**`Config.py`** — The only file you ever need to edit. Controls date ranges, row counts, null percentages, duplicate rates, output paths, and random seeds. Every other file reads from here.

**`Master_Data.py`** — All static lookup data: 100 Indian first/last names, 50 city-state-pincode tuples, 40 Samsung product SKUs with full specs, and all enum lists (payment modes, issue types, campaign names, etc.). To add a new product or city, edit only this file.

**`Utils.py`** — Shared helper functions: `rnd_phone()`, `rnd_upi()`, `rnd_gstin()`, `rnd_date()`, `add_messy()`, `mess_case()`. Every generator imports these instead of duplicating logic.

**`Generators/`** — Five generator modules, each containing one or more generator classes. Every class follows the same interface: `generate()` returns the data, `save()` writes the file.

**`Main.py`** — The orchestrator. Instantiates generators in dependency order, passes ID pools between them, logs every step, and prints the final summary.

---

## 4. ⚙️ SETUP & INSTALLATION

### Prerequisites

- Python **3.10 or higher**
- pip (comes with Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
```

> ⚠️ **Most common error:** `ModuleNotFoundError: No module named 'openpyxl'`
> Fix: `pip install openpyxl`
> This is required for all `.xlsx` file generation (campaigns, employees, inventory, returns).

### Recommended: Virtual Environment

```bash
# Step 1 — Create virtual environment
python -m venv venv

# Step 2 — Activate (Windows)
venv\Scripts\activate

# Step 2 — Activate (Mac / Linux)
source venv/bin/activate

# Step 3 — Install dependencies
pip install -r requirements.txt

# Step 4 — Run
python Main.py
```

---

## 5. 🔧 CONFIGURATION GUIDE

**All parameters live exclusively in `Config.py`.** No other file needs to be edited for routine changes — not `Main.py`, not any Generator file.

### Date Range

The date range applies to all transactional tables: sales, complaints, returns, financial transactions, reviews, and inventory snapshots.

```python
# Config.py
DATE_START = datetime(2022, 1, 1)    # ← Change start date here
DATE_END   = datetime(2025, 12, 31)  # ← Change end date here
```

### Row Counts Per Table

Adjust any value below to generate more or fewer rows. Tables that reference other tables (e.g. `sales_transactions` needs `customer_id`) automatically sample from whatever pool was generated upstream.

```python
ROW_COUNTS = {
    "products"               :   2_000,   # JSON  — product catalogue
    "warehouses"             :      25,   # JSON  — fixed; add entries in Products_Warehouses.py
    "service_centers"        :   1_200,   # JSON
    "customers"              : 200_000,   # CSV
    "dealers"                :  10_000,   # CSV
    "suppliers"              :     500,   # CSV
    "sales_transactions"     : 750_000,   # CSV
    "complaints"             : 200_000,   # CSV
    "financial_transactions" : 650_000,   # CSV   (+2% duplicate rows injected)
    "product_reviews"        :  50_000,   # CSV
    "campaigns"              :   1_000,   # XLSX
    "employees"              :  15_000,   # XLSX
    "inventory"              : 100_000,   # XLSX
    "returns"                :  75_000,   # XLSX  (+3% duplicate rows injected)
}
```

### Data Quality Knobs

These percentages control the intentional messiness injected into the dataset. Increase them for harder cleaning exercises; decrease them for cleaner data.

```python
QUALITY = {
    "null_pct_default"   : 0.03,  # 3% nulls in most columns
    "null_pct_high"      : 0.07,  # 7% for less-critical fields
    "bad_value_pct"      : 0.02,  # Injected garbage strings (e.g. "N/A", "?")
    "email_dup_pct"      : 0.02,  # 2% duplicate emails across customers
    "phone_prefix_pct"   : 0.06,  # "+91" or leading "0" added to phones
    "invalid_pin_pct"    : 0.04,  # Random invalid PIN codes
    "fin_dup_pct"        : 0.02,  # Duplicate rows in financial_transactions
    "returns_dup_pct"    : 0.03,  # Duplicate rows in returns
    "category_mess_pct"  : 0.07,  # Casing/spelling errors on category names
}
```

### Reproducibility Seed

```python
NUMPY_SEED  = 42   # Change for a completely different dataset
RANDOM_SEED = 42   # Keep both the same for consistency
```

---

## 6. 🗃️ GENERATED TABLES — ALL 14 TABLES

### Reference & Dimension Tables

| # | File | Format | Rows | Domain | Key Fields |
|---|---|---|---|---|---|
| 1 | `products.json` | JSON | 2,000 | HR & Marketing (HRM) | SKU, MRP, RAM, Storage, Category |
| 2 | `warehouses.json` | JSON | 25 | Supply Chain & Inventory (SCI) | Capacity, Coordinates, Type |
| 3 | `service_centers.json` | JSON | 1,200 | After-Sales Service (AS2) | Tier, City, Capacity/Day |
| 4 | `customers.csv` | CSV | 200,000 | Customers (CRM) | Segment, DOB, City, is_active |
| 5 | `dealers.csv` | CSV | 10,000 | Sales & Distribution (SND) | Chain, Tier, Store Type |
| 6 | `suppliers.csv` | CSV | 500 | Supply Chain & Inventory (SCI) | Country, GSTIN, Category, Rating |
| 7 | `campaigns.xlsx` | XLSX | 1,000 | HR & Marketing (HRM) | Budget, Discount, Region, Status |
| 8 | `employees.xlsx` | XLSX | 15,000 | HR & Marketing (HRM) | Department, Salary, PF Number |

### Fact & Transaction Tables

| # | File | Format | Rows | Domain | Key Fields |
|---|---|---|---|---|---|
| 9 | `inventory.xlsx` | XLSX | 100,000 | Supply Chain & Inventory (SCI) | Qty Available, Reorder Level |
| 10 | `sales_transactions.csv` | CSV | 750,000 | Sales & Distribution (SND) | Amount, Channel, Payment Mode |
| 11 | `complaints.csv` | CSV | 200,000 | After-Sales Service (AS2) | Issue Type, Priority, CSAT Score |
| 12 | `returns.xlsx` | XLSX | ~77,250 | After-Sales Service (AS2) | Return Reason, Refund Mode |
| 13 | `financial_transactions.csv` | CSV | ~663,000 | Finance & Payments (FIP) | Payment Mode, GST, UPI Ref, EMI |
| 14 | `product_reviews.csv` | CSV | 50,000 | Customers (CRM) | Rating, Review Text, Verified |

> **Note:** Rows marked `~` include intentionally injected duplicate rows to simulate ETL double-loading — a real-world problem this pipeline is designed to clean.

### Table Detail — Key Design Decisions

**`customers.csv` (200,000 rows)**
The largest reference table. Customers are segmented into Premium (15%), Mid-Range (35%), Budget (40%), and Enterprise (10%) tiers. Gender is encoded in seven different ways — `Male`, `male`, `M`, `Female`, `female`, `F`, `Other` — to simulate real CRM export inconsistency.

**`sales_transactions.csv` (750,000 rows)**
The primary fact table. Channel distribution is weighted to reflect India's actual e-commerce landscape: **Flipkart (28%)**, **Amazon IN (22%)**, **Croma (12%)**, **Samsung SmartCafé (9%)**. Amount fields contain three types of corruption: negative values (~2%), wrong currency prefix `"USD 82999"` (~2%), and nulls (~2%).

**`employees.xlsx` (15,000 rows)**
Salary is stored in **three different formats** in the same column: `"18 LPA"` (annual CTC), `"150000"` (monthly gross as integer string), and `"18L"` (shorthand). This is the most common salary-data cleaning challenge in Indian HR systems.

**`financial_transactions.csv` (650,000 rows)**
UPI reference VPAs are only populated for UPI payments. EMI tenure (months) is only populated for EMI payment rows. GST is stored in four different formats: `"18%"`, `"18"`, `"28%"`, and `"GST@18"` — all in the same column.

**`inventory.xlsx` (100,000 rows)**
Approximately 5% of `snapshot_date` values are stored as **Unix epoch timestamps** (e.g. `"1711065600"`) instead of ISO date strings. Approximately 1% of `qty_available` values are **negative**, simulating over-allocation bugs in the WMS.

---

## 7. 🧹 DATA QUALITY & MESSINESS INJECTED

The dataset is intentionally imperfect. Every issue below is a real problem found in enterprise data systems and must be resolved before the data is promoted to the Silver Layer.

### Complete Issue Inventory

| Issue Type | Table(s) Affected | Example |
|---|---|---|
| **Null / missing values** | All 14 tables | `pincode = None`, `tier = None` |
| **Duplicate rows** | `returns`, `financial_transactions` | Identical row appears twice |
| **Duplicate emails** | `customers` | Two different customers share one email |
| **Mixed date formats** | All date columns | `2024-03-15` vs `15/03/2024` vs `15 Mar 2024` |
| **Phone number prefix variants** | `customers`, `dealers` | `9876543210`, `+919876543210`, `09876543210` |
| **Mixed boolean encodings** | `is_active`, `is_exclusive`, `bis_certified` | `True`, `1`, `Yes`, `TRUE`, `true` |
| **Category casing errors** | `products` | `"Smartphones"` vs `"smartphones"` vs `"TELEVISIONS"` |
| **Invalid PIN codes** | `customers` | `"836294"` — valid format, invalid geography |
| **Negative stock quantities** | `inventory` | `qty_available = -23` (over-allocation) |
| **Mixed salary formats** | `employees` | `"18 LPA"`, `"150000"` (monthly), `"18L"` |
| **Wrong currency prefix** | `sales_transactions` | `"USD 82999"` instead of `82999` |
| **Out-of-range rating values** | `product_reviews` | `rating = 6`, `rating = -1`, `rating = 0` |
| **Epoch timestamps** | `inventory` | `snapshot_date = "1711065600"` |
| **Mixed GST formats** | `financial_transactions` | `"18%"`, `"18"`, `"GST@18"` |
| **Corrupted coordinates** | `warehouses` | `latitude = "28,5355"` (comma instead of period) |
| **RAM / storage with suffix** | `products` | `"8gb"` instead of `"8"`, `"256GB"` instead of `"256"` |

### Messiness by Severity

**🔴 High Impact — blocks aggregation without cleaning:**
Mixed date formats, mixed salary formats, wrong currency prefix, epoch timestamps, negative quantities, mixed boolean encodings.

**🟡 Medium Impact — causes incorrect JOINs or GROUP BYs:**
Category casing errors, mixed payment mode spellings (`"upi"` vs `"UPI"`), mixed GST formats, RAM/storage suffix variants.

**🟢 Low Impact — data completeness issues only:**
Null pincodes, null tier values, null CSAT scores, null resolution dates for unresolved complaints.

---

## 8. ▶️ RUNNING THE GENERATOR

```bash
python Main.py
```

### Expected Console Output

```
======================================================================
  Samsung India Raw Data Generator
  Date range : 2022-01-01  to  2025-12-31
  Output dir : ./Data/Raw_data
======================================================================
[1/14]  Completed Creating 'products.json'
[2/14]  Completed Creating 'warehouses.json'
[3/14]  Completed Creating 'customers.csv'
[4/14]  Completed Creating 'dealers.csv'
[5/14]  Completed Creating 'service_centers.json'
[6/14]  Completed Creating 'campaigns.xlsx'
[7/14]  Completed Creating 'suppliers.csv'
[8/14]  Completed Creating 'employees.xlsx'
[9/14]  Completed Creating 'inventory.xlsx'
[10/14] Completed Creating 'sales_transactions.csv'
[11/14] Completed Creating 'complaints.csv'
[12/14] Completed Creating 'returns.xlsx'
[13/14] Completed Creating 'financial_transactions.csv'
[14/14] Completed Creating 'product_reviews.csv'
```

### Expected Run Time

| Machine | Approximate Time |
|---|---|
| Modern laptop — i5 / Ryzen 5, 16 GB RAM | 3 – 5 minutes |
| Older machine or low RAM | 8 – 12 minutes |
| High-end workstation | 1 – 2 minutes |

> **Bottleneck:** The slowest steps are `customers.csv` (200K rows with per-row phone/email generation) and any `.xlsx` file — `openpyxl` is significantly slower than CSV writing. If generation time is critical, reduce `inventory` rows first — it is the largest XLSX table at 100,000 rows.

### Output File Sizes (Approximate)

| File | Approximate Size |
|---|---|
| `sales_transactions.csv` | ~85 MB |
| `financial_transactions.csv` | ~75 MB |
| `complaints.csv` | ~25 MB |
| `customers.csv` | ~22 MB |
| `inventory.xlsx` | ~18 MB |
| `returns.xlsx` | ~12 MB |
| `employees.xlsx` | ~4 MB |
| All other files | < 2 MB each |
| **Total** | **~300 – 350 MB** |

---

## 9. 📋 LOGS

Every run appends to `Logs/Data_generation.log`. The `Logs/` folder is created automatically on first run — no manual setup needed.

### What Gets Logged

- **Run start** — timestamp, date range, output directory
- **Each step** — file name, target row count, actual rows written, time taken in seconds
- **Final summary** — all 14 file sizes in MB, total dataset size, total elapsed time
- **Errors** — full Python traceback if any step fails, diagnosable without re-running

### Sample Log Output

```
2025-01-15 10:23:01 | INFO | ======================================================================
2025-01-15 10:23:01 | INFO | SAMSUNG RAW DATA GENERATION [INDIA]
2025-01-15 10:23:01 | INFO | Date range : 2022-01-01  to  2025-12-31
2025-01-15 10:23:01 | INFO | Output dir : ./Data/Raw_data
2025-01-15 10:23:02 | INFO | [1/14] Completed Creating 'products.json' with 2,000 rows in (0.41s)
2025-01-15 10:23:02 | INFO | [2/14] Completed Creating 'warehouses.json' with 25 rows in (0.01s)
2025-01-15 10:23:13 | INFO | [3/14] Completed Creating 'customers.csv' with 200,000 rows in (10.62s)
...
2025-01-15 10:26:44 | INFO | GENERATION COMPLETE — File Summary
2025-01-15 10:26:44 | INFO |   CSV     sales_transactions.csv                    87.40 MB
2025-01-15 10:26:44 | INFO |   TOTAL                                            318.74 MB
2025-01-15 10:26:44 | INFO |   Total generation time : 222.14s
2025-01-15 10:26:44 | INFO | ======================================================================
```

> **Note:** Each run **appends** to the same log file — it does not overwrite. Delete or archive `Data_generation.log` manually before a fresh run if you want a clean log history.

---

## 10. 🔗 DEPENDENCY CHAIN

Generator classes pass ID pools to downstream generators as constructor arguments. **The order in `Main.py` must be preserved** — changing it will cause `KeyError` or empty foreign-key columns.

```
[Step 1]  ProductGenerator      → pid_pool  ───────────────────────────────────┐
[Step 2]  WarehouseGenerator    → wh_ids    ──────────────────────┐            │
[Step 3]  CustomerGenerator     → cust_ids  ──────────┐           │            │
[Step 4]  DealerGenerator       → dealer_ids   ──┐    │           │            │
                                                  │    │           │            │
[Step 5]  ServiceCenterGenerator  (no FK output)  │    │           │            │
[Step 6]  CampaignGenerator       (no FK output)  │    │           │            │
[Step 7]  SupplierGenerator       (no FK output)  │    │           │            │
[Step 8]  EmployeeGenerator       (no FK output)  │    │           │            │
                                                  │    │           │            │
[Step 9]  InventoryGenerator   ←──────────────────┼────┼── wh_ids + pid_pool   │
[Step 10] SalesTransactionGenerator ←─────────────┘    └── cust_ids + pid_pool │
             → txn_ids ──────────────────┐                                     │
[Step 11] ComplaintGenerator   ←── cust_ids + pid_pool                         │
[Step 12] ReturnGenerator      ←── txn_ids + cust_ids + pid_pool               │
[Step 13] FinancialTransactionGenerator ←── txn_ids                            │
[Step 14] ProductReviewGenerator ←── cust_ids + pid_pool ──────────────────────┘
```

**The critical path is Steps 1 → 3 → 4 → 10.** Products, Customers, and Dealers must all complete before Sales Transactions. Everything downstream of Step 10 depends on `txn_ids`.

---

## 11. 🛠️ TROUBLESHOOTING

### Installation & Setup Errors

#### 1. ModuleNotFoundError: No module named `openpyxl`

The most common error. `openpyxl` is not installed in your Python environment.

```bash 
pip install openpyxl
```

If you are using a virtual environment, make sure it is activated before running the install.

---

#### 2. ModuleNotFoundError: No module named `Config`

Python cannot find `Config.py`. This happens when you run `Main.py` from a different directory than the project root.

```bash
# ❌ Wrong — running from outside the project folder
python "C:\Projects\Samsung Data Engineering\Data Generation\Main.py"

# ✅ Correct — navigate into the project folder first
cd "C:\Projects\Samsung Data Engineering\Data Generation"
python Main.py
```

---

#### 3. ModuleNotFoundError: No module named `Generators.Products_Warehouses`

The `Generators/` folder is missing its` __init__.py` file, or the folder itself is not in the same directory as `Main.py`.

**Check your folder structure:**
```
Samsung Data Engineering/
├── Main.py
├── Generators/
│   ├── __init__.py       ← This file must exist
│   ├── Products_Warehouses.py
│   └── ...
```

**If `__init__.py` is missing, create an empty one:**

```bash
# Windows
type nul > Generators\__init__.py

# Mac / Linux
touch Generators/__init__.py
```

---

### Runtime Errors

#### 1. Generation stops at Step 6 — `campaigns.xlsx` with no error message

This is almost always the `openpyxl` missing error caught silently. Run:

```bash
pip install openpyxl
python Main.py
```

---

#### 2. PermissionError: [Errno 13] Permission denied: `./Data/Raw_data/customers.csv`

The output file is currently open in Excel or another program. Close the file and re-run.

---

#### 3. `MemoryError` during large table generation

Your machine does not have enough RAM to hold the full DataFrame in memory. Try reducing the row count in `Config.py`:

```python
# Config.py — reduce the largest tables first
ROW_COUNTS = {
    "sales_transactions"     : 300_000,   # Reduced from 750,000
    "financial_transactions" : 250_000,   # Reduced from 650,000
    "complaints"             : 100_000,   # Reduced from 200,000
    "customers"              : 100_000,   # Reduced from 200,000
    "inventory"              :  50_000,   # Reduced from 100,000
}
```

---

#### 4. `ValueError: could not convert string to float` during downstream analysis

This is expected — the Bronze Layer intentionally contains messy values like `"USD 82999"`, `"18 LPA"`, and `"18%"`. These columns need to be cleaned in the Silver Layer before any numeric operations. Do not modify the generator — fix the column in your cleaning pipeline.

---

#### 5. `FileNotFoundError`: [Errno 2] No such file or directory: `'./Data/Raw_data/...'`

The output directory does not exist and could not be created, usually due to a path permission issue. Either create the folder manually or change `OUTPUT_DIR` in `Config.py` to a path you have write access to:

```python
# Config.py
OUTPUT_DIR = "C:/Users/YourName/Desktop/Samsung_Output"
```

---

### Log File Issues

#### 1. The log file is too large after many runs
The log file appends on every run and never auto-clears. Archive or delete it manually before a fresh run:

```bash
# Windows
del Logs\Data_generation.log

# Mac / Linux
rm Logs/Data_generation.log
```

---

## 12. ➕ EXTENDING THE PROJECT

### Add a New Table

1. Create a new generator class in the appropriate `Generators/` file (or a new file).
2. Follow the standard two-method interface — every generator in the project uses this pattern:

```python
class MyNewGenerator:
    def __init__(self, out_dir: str, ...foreign_key_pools...):
        self.n        = ROW_COUNTS["my_new_table"]
        self.out_path = f"{out_dir}/my_new_table.csv"

    def generate(self) -> pd.DataFrame:
        # build and return DataFrame here
        ...

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)
```

3. Add the row count key to `ROW_COUNTS` in `Config.py`.
4. Add the generation step to `Main.py` in the correct dependency order.

### Add New Samsung Products

Edit the `SAMSUNG_PRODUCTS` list in `Master_Data.py`:

```python
# (SKU, name, category, subcategory, MRP_INR, RAM_GB, storage_GB, display_inches)
("SM-XXXXXXXX", "Galaxy S26", "Smartphones", "Galaxy S Series", 89999, 8, 256, "6.3"),
```

### Add New Cities

Edit the `CITIES_STATES` list in `Master_Data.py`:

```python
# (city, state, pincode)
("Dehradun", "Uttarakhand", "248001"),
("Shimla",   "Himachal Pradesh", "171001"),
```

### Change Output Format (e.g. CSV → Parquet)

Only the `save()` method of the relevant generator needs to change:

```python
# Before — CSV
def save(self, df: pd.DataFrame) -> None:
    df.to_csv(self.out_path, index=False)

# After — Parquet (faster for large tables, smaller file size)
def save(self, df: pd.DataFrame) -> None:
    df.to_parquet(self.out_path.replace(".csv", ".parquet"), index=False)
```

No other file needs to be modified.

### Scale Up to 10 Million Rows

Increase the row counts in `Config.py`. For very large scales, also consider:

- Switching all `.xlsx` tables to `.csv` or `.parquet` — `openpyxl` is slow beyond 500K rows
- Reducing `DATE_FORMATS` variants in `Config.py` to speed up vectorised date generation
- Using chunked CSV writing with pandas `chunksize` for the largest tables

---

## 13. ❓ FREQUENTLY ASKED QUESTIONS

#### Q1: Can I run only specific tables instead of all 14?

**Ans:** Not directly — `Main.py` runs all steps in a fixed dependency order. However, you can comment out any step in `Main.py` as long as its downstream tables are also commented out. For example, if you skip Step 3 (customers), you must also skip Steps 10, 11, 12, and 14 since they all require cust_ids.

#### Q2: Will I get the same data every time I run?

**Ans:** Yes, as long as NUMPY_SEED and RANDOM_SEED in `Config.py` are unchanged (both default to 42). Every run with the same seed produces byte-for-byte identical output files. Change either seed value to produce a completely different dataset.

#### Q3: Can I generate data for a different company — not Samsung?

**Ans:** Yes. The only Samsung-specific content is in `Master_Data.py` — the product catalogue (SAMSUNG_PRODUCTS), retail chains (RETAIL_CHAINS), and campaign names (CAMPAIGN_NAMES). Replace those lists with your own company's data and everything else — customers, transactions, complaints, finance — will generate correctly around your new master data.

#### Q4: Why are some row counts in the output slightly higher than the target in `Config.py`?

**Ans:** Two tables — returns.xlsx and financial_transactions.csv — have duplicate rows intentionally injected after generation (3% and 2% respectively). So if ROW_COUNTS["returns"] is 75,000, the actual file will contain approximately 77,250 rows. This is by design. The log records the actual row count written.

#### Q5: The customers.csv step takes 10+ seconds. Is that normal?

**Ans:** Yes. Generating 200,000 customers involves per-row operations — random phone number generation, email construction, and PIN validation — that cannot be fully vectorised. On most laptops this step takes 8–15 seconds. It is the slowest reference-table step. If speed is critical, reduce ROW_COUNTS["customers"] or pre-generate the phone/email columns using a vectorised approach in `Utils.py`.

#### Q6: Can I add a new column to an existing table without breaking anything?

**Ans:** Yes. Add the column inside the generate() method of the relevant generator class — it will appear in the output file automatically. No other file needs to change unless another generator depends on that column as a foreign key.

#### Q7: Why is warehouses.json always exactly 25 rows even if I change ROW_COUNTS["warehouses"]?

**Ans:** The warehouse table is generated from a fixed WAREHOUSE_DATA list inside Products_Warehouses.py, not from the row count config. This is intentional — Samsung India has a fixed number of real warehouses. To add warehouses, add new tuples to the WAREHOUSE_DATA list directly in that file.

#### Q8: Can I use this data for a portfolio project or interview case study?

**Ans:** Absolutely. The data is entirely synthetic. All names, phone numbers, GSTINs, email addresses, and transaction IDs are computer-generated and have no connection to real individuals or businesses. Clearly note in your project that the dataset is synthetic and generated for data engineering practice.

#### Q9: Why does inventory.xlsx have negative qty_available values?

**Ans:** This is intentional messiness simulating an over-allocation bug in a Warehouse Management System — a real problem in enterprise inventory data. Your Silver Layer cleaning pipeline should detect and handle these negative values (either zero-floor them, flag them for review, or exclude them from stock calculations depending on your business rule).

#### Q10: I changed DATE_START and DATE_END in `Config.py` but some dates in the output are outside my range.

**Ans:** Check two things. First, some generators have hardcoded date ranges for non-transactional fields that are independent of the global range — for example, employees.join_date always spans 2010–2024 regardless of DATE_START/DATE_END because employee join dates predate the analysis period. 
Second, the contract_start column in suppliers.csv also uses a fixed historical range. Only transactional tables (sales, complaints, returns, finance, reviews, inventory) use the global date range from `Config.py`.

---

## 📄 LICENSE

This data generation scripts is provided for educational and portfolio purposes.

---

# ⚠️ Dataset Disclaimer  
All datasets used are **dummy, synthetic, or public**, intended only for learning and portfolio demonstration.  
No real customer or company data is used.

**Last Updated:** May 2026  
**Version:** 1.0

---

## 🧑‍💻 Author

**👤 Harsh Belekar**  
📍 Data Analyst | Python Developer | SQL | Power BI | Excel | Data Visualization  
📬[LinkedIn](https://www.linkedin.com/in/harshbelekar) | 🔗[GitHub](https://github.com/Harsh-Belekar)

📧 [harshbelekar74@gmail.com](mailto:harshbelekar74@gmail.com)

---

⭐ *If you found this project helpful, feel free to star the repo and connect with me for collaboration!*

**Happy Data Generating! 🚀**
