# 🏢 Samsung — Data Engineering Project

![Project Banner](banner.png)

### End-to-End Data Engineering Project using Medallion Architecture 

**A fully End-to-End Data Engineering project — from Synthetic data generation to a production-grade three-layer Data Warehouse — built to demonstrate real-world data engineering skills using Python, SQL, and PostgreSQL.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Manipulation-orange?logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-blue?logo=numpy) ![Tool](https://img.shields.io/badge/Tool-PostgreSQL-blue) ![Process](https://img.shields.io/badge/Process-Data_Warehousing_|_ETL-orange) ![Process](https://img.shields.io/badge/Process-Star_Schema_|_Data_Modeling-yellow) ![Feature](https://img.shields.io/badge/Feature-Fact_|_Dimension_Tables-green) ![Domain](https://img.shields.io/badge/Domain-Retail_Analytics-red) ![Type](https://img.shields.io/badge/Type-End_to_End_Project-critical) ![Project](https://img.shields.io/badge/Project-Data%20Engineering-blue) ![Status](https://img.shields.io/badge/Status-Completed-success) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)

---

## 📌 Table of Contents

1. [Project Overview](#1--project-overview)
2. [Data Warehouse Architecture](#2--data-warehouse-architecture)
3. [Project Folder Structure](#3--project-folder-structure)
4. [Data Domains](#4--data-domains)
5. [Dataset Overview](#5--dataset-overview)
6. [Tech Stack](#6--tech-stack)
7. [Project Workflow — Step by Step](#7--project-workflow--step-by-step)
   - [Phase 1 — Synthetic Data Generation](#phase-1--synthetic-data-generation)
   - [Phase 2 — Database Setup](#phase-2--database-setup)
   - [Phase 3 — Bronze Layer](#phase-3--bronze-layer)
   - [Phase 4 — Silver Layer](#phase-4--silver-layer)
   - [Phase 5 — Gold Layer](#phase-5--gold-layer)
8. [Naming Conventions](#8--naming-conventions)
9. [Pipeline Execution Guide](#9--pipeline-execution-guide)
10. [Project Documentation](#10--project-documentation)
11. [Logs](#11--logs)
12. [Author](#-author)

---

## 1. 🚀 Project Overview

This project builds a **production-grade Data Warehouse** for Samsung India — from scratch — using the **Medallion Architecture (Bronze → Silver → Gold)**. The pipeline begins with synthetic data generation simulating Samsung India's real business operations across Sales, Finance, Customer Relations, After-Sales Service, Supply Chain, and Marketing, then processes that data through three structured warehouse layers into analytics-ready Gold views.

The project is implemented **twice** — once using **Python Scripts** and once using **SQL Scripts** — deliberately, to showcase proficiency in both approaches on the same problem.

### What This Project Covers

- ✅ Synthetic data generation — **2,000,000+ rows** across **14 tables** using Python
- ✅ Multi-format raw data — **CSV, JSON, and XLSX** files organised by business domain
- ✅ **Bronze Layer** — raw data ingestion with no transformations (14 tables)
- ✅ **Silver Layer** — cleaned, typed, standardised, and normalised data (14 tables)
- ✅ **Gold Layer** — business-ready Star Schema views for analytics (14 views)
- ✅ **Dual implementation** — complete Python Scripts + complete SQL Scripts
- ✅ **Structured logging** — every pipeline stage produces its own log file
- ✅ **Full documentation** — Data Catalog, Data Generation Guide, Naming Conventions

---

## 2. 🏗️ Data Warehouse Architecture

![Data Warehouse Architecture](Images/Data_Warehouse_Architecture.png)

The architecture follows the **Medallion (Multi-Hop) pattern** with three progressive layers inside a single PostgreSQL database (`Samsung_Data_Warehouse`):

| Layer | Schema | Object Type | Load Strategy | Transformations | Data Model |
|---|---|---|---|---|---|
| **Bronze** | `bronze` | Tables | Batch · Full Load · Truncate & Insert | None — raw as-is | No model |
| **Silver** | `silver` | Tables | Batch · Full Load · Truncate & Insert | Cleaning · Standardisation · Normalisation · Enrichment | No model |
| **Gold** | `gold` | Views | No load — live reads from Silver | Data Integration · Aggregations · Business Logic | Star Schema |

### Data Flow

```
Source Files (CSV / JSON / XLSX)
        │
        ▼  File_converter.py (JSON & XLSX → CSV)
        │
        ▼  Load_Bronze  (Python) / Proc_Load_Bronze  (SQL)
┌─────────────────────────────────┐
│         BRONZE LAYER            │  ← Raw ingestion, all columns TEXT
│   14 Tables · bronze schema     │
└────────────────┬────────────────┘
                 │
                 ▼  Load_Silver  (Python) / Proc_Load_Silver  (SQL)
┌─────────────────────────────────┐
│         SILVER LAYER            │  ← Typed, cleaned, deduplicated
│   14 Tables · silver schema     │
└────────────────┬────────────────┘
                 │
                 ▼  DDL_Gold  (Python / SQL) — Views only
┌─────────────────────────────────┐
│          GOLD LAYER             │  ← Business-ready Star Schema
│   14 Views  · gold schema       │
└────────────────┬────────────────┘
                 │
        ┌────────┴─────────┐
        ▼                  ▼
   Power BI           SQL Analysis
   QuickBI             Tableau · ML
```

---

## 3. 📁 Project Folder Structure

```
Samsung Data Engineering/
│
├── Data/                              ← Raw source data organised by business domain
│   ├── AS2/                           ← After-Sales Service
│   │   ├── complaints.csv
│   │   ├── returns.csv
│   │   ├── returns.xlsx
│   │   ├── service_centers.csv
│   │   └── service_centers.json
│   ├── CRM/                           ← Customer Relationship Management
│   │   ├── customers.csv
│   │   └── product_reviews.csv
│   ├── FIP/                           ← Finance & Payments
│   │   └── financial_transactions.csv
│   ├── HRM/                           ← Human Resources & Marketing
│   │   ├── campaigns.csv
│   │   ├── campaigns.xlsx
│   │   ├── employees.csv
│   │   ├── employees.xlsx
│   │   ├── products.csv
│   │   └── products.json
│   ├── SCI/                           ← Supply Chain & Inventory
│   │   ├── inventory.csv
│   │   ├── inventory.xlsx
│   │   ├── suppliers.csv
│   │   ├── warehouses.csv
│   │   └── warehouses.json
│   └── SND/                           ← Sales & Distribution
│       ├── dealers.csv
│       └── sales_transactions.csv
│
├── Data_Generation/                   ← Synthetic data generation pipeline
│   ├── Config.py                      ← All tunable parameters (rows, dates, quality)
│   ├── Main.py                        ← Entry point — run this to generate all data
│   ├── Master_data.py                 ← Static lookup data (products, cities, names)
│   ├── Utils.py                       ← Shared helper functions
│   └── Generators/                    ← One generator class per domain pair
│       ├── __init__.py
│       ├── Customers_Dealers.py
│       ├── Employees_Inventory.py
│       ├── Products_Warehouses.py
│       ├── Service_Campaigns_Suppliers.py
│       └── Transactions.py
│
├── Docs/                                ← Project documentation
│   ├── Data_Catalog.md                  ← Gold layer table & column reference
│   ├── Data_Generation_Documentation.md ← Data generation guide & configuration
│   └── Naming_Conventions.md            ← Schema, table, column naming standards
│
├── Images/                            ← Architecture and schema diagrams
│   ├── Data_Warehouse_Architecture.png
│   └── Schema.png
│
├── Logs/                              ← Auto-generated logs for every pipeline stage
│   ├── Data_generation.log
│   ├── Init_database.log
│   ├── DDL_Bronze.log
│   ├── Load_Bronze.log
│   ├── DDL_Silver.log
│   ├── Helper_func.log
│   ├── Load_Silver.log
│   └── DDL_Gold.log
│
├── Python Scripts/                    ← Full Python implementation of the pipeline
│   ├── Init_database.py               ← Creates bronze, silver, gold schemas
│   ├── File_converter.py              ← Converts JSON & XLSX files to CSV
│   ├── Bronze/
│   │   ├── DDL_Bronze.py              ← Creates 14 Bronze tables
│   │   └── Load_Bronze.py             ← Loads CSV data into Bronze tables
│   ├── Silver/
│   │   ├── DDL_Silver.py              ← Creates 14 Silver tables (typed columns)
│   │   ├── Helper_func.py             ← Shared data cleaning functions
│   │   └── Load_Silver.py             ← Cleans & loads Bronze → Silver
│   └── Gold/
│       └── DDL_Gold.py                ← Creates 14 Gold views (Star Schema)
│
├── SQL Scripts/                       ← Full SQL implementation of the pipeline
│   ├── Init_database.sql              ← Creates bronze, silver, gold schemas
│   ├── Bronze/
│   │   ├── DDL_Bronze.sql             ← Creates 14 Bronze tables
│   │   └── Proc_Load_Bronze.sql       ← Stored procedure: load_bronze
│   ├── Silver/
│   │   ├── DDL_Silver.sql             ← Creates 14 Silver tables (typed columns)
│   │   ├── Helper_function.sql        ← Shared SQL cleaning functions
│   │   └── Proc_Load_Silver.sql       ← Stored procedure: load_silver
│   └── Gold/
│       └── DDL_Gold.sql               ← Creates 14 Gold views (Star Schema)
│
├── README.md                          ← This file
├── LICENSE                            ← MIT License
└── requirements.txt                   ← Python dependencies
```

---

## 4. 🗂️ Data Domains

The 14 source tables are organised into **6 business domains**, each stored in its own subfolder inside `Data/`. The domain prefix is carried through all three warehouse layers as part of the naming convention.

| Domain | Prefix | Business Area | Tables |
|---|---|---|---|
| After-Sales Service | `AS2` | Complaints, Returns, Service Centres | `complaints`, `returns`, `service_centers` |
| Customer Relationship | `CRM` | Customers, Reviews | `customers`, `product_reviews` |
| Finance & Payments | `FIP` | Payments, GST, EMI | `financial_transactions` |
| Human Resources & Marketing | `HRM` | Products, Employees, Campaigns | `products`, `employees`, `campaigns` |
| Supply Chain & Inventory | `SCI` | Warehouses, Suppliers, Inventory | `warehouses`, `suppliers`, `inventory` |
| Sales & Distribution | `SND` | Dealers, Sales Transactions | `dealers`, `sales_transactions` |

---

## 5. 📊 Dataset Overview

All data is **synthetically generated** using the custom Python pipeline in the `Data Generation/` folder. It simulates Samsung India's real-world business operations across 2022–2025.

| # | Table | Domain | Format | Approx. Rows | Description |
|---|---|---|---|---|---|
| 1 | `products` | HRM | JSON / CSV | 2,000 | Samsung India product catalogue |
| 2 | `warehouses` | SCI | JSON / CSV | 25 | National warehouse master |
| 3 | `service_centers` | AS2 | JSON / CSV | 1,200 | Authorised service centres |
| 4 | `customers` | CRM | CSV | 200,000 | Registered customer master |
| 5 | `dealers` | SND | CSV | 10,000 | Retail dealer and partner master |
| 6 | `suppliers` | SCI | CSV | 500 | Component and logistics suppliers |
| 7 | `campaigns` | HRM | XLSX / CSV | 1,000 | Marketing campaign master |
| 8 | `employees` | HRM | XLSX / CSV | 15,000 | Employee HR master |
| 9 | `inventory` | SCI | XLSX / CSV | 100,000 | Daily inventory snapshots |
| 10 | `sales_transactions` | SND | CSV | 750,000 | Primary sales fact table |
| 11 | `complaints` | AS2 | CSV | 200,000 | After-sales complaint cases |
| 12 | `returns` | AS2 | XLSX / CSV | ~77,250 | Product returns (+3% duplicates) |
| 13 | `financial_transactions` | FIP | CSV | ~663,000 | Payment ledger (+2% duplicates) |
| 14 | `product_reviews` | CRM | CSV | 50,000 | Customer product ratings |

> **Total: ~2,070,000 rows across 14 tables spanning 6 business domains and 4 years (2022–2025)**

The raw data intentionally contains **real-world data quality issues** — mixed date formats, null values, duplicate rows, casing errors, and invalid values — to make the Silver layer cleaning pipeline meaningful and realistic.

---

## 6. 🛠️ Tech Stack

| Tool / Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.10+ | Data generation, pipeline orchestration, data cleaning |
| **PostgreSQL** | 14+ | Data warehouse database engine |
| **Pandas** | 2.0+ | DataFrame manipulation and CSV I/O |
| **NumPy** | 1.24+ | Vectorised data generation |
| **openpyxl** | 3.1+ | Reading and writing XLSX files |
| **psycopg2** | 2.9+ | PostgreSQL connection from Python |
| **SQLAlchemy** | 2.0+ | ORM and database connection pooling |
| **SQL** | PostgreSQL dialect | DDL, stored procedures, helper functions |
| **Power BI** | Latest | Dashboard and reporting (Gold layer consumer) |

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

---



---

## 🧑‍💻 Author

**👤 Harsh Belekar**  
📍 Data Analyst | Python Developer | SQL | Power BI | Excel | Data Visualization  
📬 [LinkedIn](https://www.linkedin.com/in/harshbelekar) | 🔗[GitHub](https://github.com/Harsh-Belekar)

📧 [harshbelekar74@gmail.com](mailto:harshbelekar74@gmail.com)

---

⭐ *If you found this project helpful, feel free to star the repo and connect with me for collaboration!*

***Made with ❤️ and a lot of ☕ by Harsh Belekar***
