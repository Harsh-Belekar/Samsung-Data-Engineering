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
