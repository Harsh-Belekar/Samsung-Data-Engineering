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
