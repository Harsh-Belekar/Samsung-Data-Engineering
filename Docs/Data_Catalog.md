# 📖 SAMSUNG DATA ENGINEERING — GOLD LAYER DATA CATALOG

**Prepared by:** Harsh Belekar
**Layer:** Gold — Analytics & Reporting
**Schema:** `gold`
**Upstream Layer:** Silver (`silver.hrm_*` | `silver.sci_*` | `silver.as2_*` | `silver.crm_*` | `silver.snd_*` | `silver.fip_*`)
**Implementation:** PostgreSQL Views (no storage — live reads from Silver)
**Total Views:** 14 (8 Dimensions + 6 Facts)
**Last Updated:** May 2026

---

## TABLE OF CONTENTS

1. [Catalog Overview](#1--catalog-overview)
2. [Architecture — Bronze → Silver → Gold](#2-️-architecture--bronze--silver--gold)
3. [Silver Domain Prefix Reference](#3-️-silver-domain-prefix-reference)
4. [Gold Layer — Schema Map](#4-️-gold-layer--schema)
5. [Dimension Tables](#5--dimension-tables)
   - [dim_products](#51-dim_products)
   - [dim_warehouses](#52-dim_warehouses)
   - [dim_service_centers](#53-dim_service_centers)
   - [dim_customers](#54-dim_customers)
   - [dim_dealers](#55-dim_dealers)
   - [dim_suppliers](#56-dim_suppliers)
   - [dim_campaigns](#57-dim_campaigns)
   - [dim_employees](#58-dim_employees)
6. [Fact Tables](#6--fact-tables)
   - [fact_inventory](#61-fact_inventory)
   - [fact_sales_transactions](#62-fact_sales_transactions)
   - [fact_complaints](#63-fact_complaints)
   - [fact_returns](#64-fact_returns)
   - [fact_financial_transactions](#65-fact_financial_transactions)
   - [fact_product_reviews](#66-fact_product_reviews)
7. [Relationships & Join Guide](#7--relationships--join-guide)
8. [Sample Queries](#8--sample-queries)
9. [Data Governance](#9--data-governance)

---

## 1. 🚀 CATALOG OVERVIEW

This Data Catalog is the **single source of truth** for every analyst, data scientist, and Power BI developer working with Samsung India's Gold layer. It documents every view, every column, every data type, and every business rule applied during the Silver → Gold transformation.

The Gold layer is implemented as **PostgreSQL views** — not physical tables. Every query against a Gold view reads live, cleaned data directly from the Silver layer in real time. This means the Gold layer is always current and requires no scheduled refresh job.

**What the Gold layer is designed for:**

The Gold layer serves two consumer groups simultaneously. The first group is **Power BI dashboard developers** who connect directly to Gold views to build revenue dashboards, after-sales health reports, and inventory monitoring panels. The second group is **SQL analysts** who write ad-hoc queries against Gold views to answer business questions without needing to understand the underlying Bronze messiness or Silver cleaning logic.

**What the Gold layer is NOT:**

The Gold layer does not store pre-aggregated data. It does not contain mart tables, rollups, or KPI summaries — those belong in a separate analytical layer above Gold. Every row in a Gold fact view corresponds to exactly one source transaction.

---

## 2. 🏗️ ARCHITECTURE — BRONZE → SILVER → GOLD

```
┌─────────────────────────────────────────────────────────┐
│  RAW FILES  (CSV / JSON / XLSX)                         │
│  14 files · ~2,000,000 rows · Mixed formats & nulls     │
└────────────────────────┬────────────────────────────────┘
                         │  Python Generator (Main.py)
                         ▼
┌─────────────────────────────────────────────────────────┐
│  BRONZE SCHEMA   (bronze.*)                             │
│  14 tables · All columns TEXT · No constraints          │
│  Raw ingestion — exactly as received                    │
└────────────────────────┬────────────────────────────────┘
                         │  SQL Cleaning Views (cleaning.*)
                         │  fn_to_boolean · fn_clean_phone
                         │  fn_parse_date · fn_salary_to_annual
                         │  fn_parse_gst_pct · Deduplication
                         ▼
┌─────────────────────────────────────────────────────────┐
│  SILVER SCHEMA   (silver.hrm_* | sci_* | as2_* | ...)   │
│  14 tables · Typed columns · FK constraints             │
│  Cleaned, standardised, deduplicated                    │
└────────────────────────┬────────────────────────────────┘
                         │  Gold DDL Views (no transformation)
                         │  Semantic renaming + column selection
                         ▼
┌─────────────────────────────────────────────────────────┐
│  GOLD SCHEMA   (gold.*)                ← YOU ARE HERE   │
│  14 views · Star Schema                                 │
│  8 Dimensions + 6 Facts                                 │
│  Business-ready · Analytics & Reporting                 │
└─────────────────────────────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Power BI Reports      Ad-hoc SQL Analysis
```

### Data Warehouse Architecture

![Warehouse Architecture](../Images/Data_Warehouse_Architecture.png)

---

## 3. 🏷️ SILVER DOMAIN PREFIX REFERENCE

Silver layer tables are named with a **3-letter domain prefix** that indicates which business domain owns the data. Gold views map directly onto these Silver tables.

| Prefix | Domain | Business Area | Silver Tables |
|---|---|---|---|
| `hrm_` | Human Resources & Marketing | People + Campaigns + Products | `hrm_products`, `hrm_employees`, `hrm_campaigns` |
| `sci_` | Supply Chain & Inventory | Warehouses + Suppliers + Stock | `sci_warehouses`, `sci_suppliers`, `sci_inventory` |
| `as2_` | After-Sales Service | Complaints + Returns + Centres | `as2_service_centers`, `as2_complaints`, `as2_returns` |
| `crm_` | Customer Relationship | Customers + Reviews | `crm_customers`, `crm_product_reviews` |
| `snd_` | Sales & Distribution | Transactions + Dealers | `snd_dealers`, `snd_sales_transactions` |
| `fip_` | Finance & Payments | Payments + GST | `fip_financial_transactions` |

> **Note for analysts:** You never need to query Silver directly. All Silver tables are fully exposed through Gold views with clean, business-friendly column names.

---

## 4. 🗺️ GOLD LAYER — SCHEMA

![Warehouse Schema](../Images/Schema.png)

### Views at a Glance

| View Name | Type | Rows (approx.) | Source Silver Table | Business Domain |
|---|---|---|---|---|
| `dim_products` | Dimension | 2,000 | `hrm_products` | Product Catalogue |
| `dim_warehouses` | Dimension | 25 | `sci_warehouses` | Supply Chain |
| `dim_service_centers` | Dimension | 1,200 | `as2_service_centers` | After-Sales |
| `dim_customers` | Dimension | 200,000 | `crm_customers` | CRM |
| `dim_dealers` | Dimension | 10,000 | `snd_dealers` | Sales |
| `dim_suppliers` | Dimension | 500 | `sci_suppliers` | Procurement |
| `dim_campaigns` | Dimension | 1,000 | `hrm_campaigns` | Marketing |
| `dim_employees` | Dimension | 15,000 | `hrm_employees` | HR |
| `fact_inventory` | Fact | 100,000 | `sci_inventory` | Supply Chain |
| `fact_sales_transactions` | Fact | 750,000 | `snd_sales_transactions` | Sales |
| `fact_complaints` | Fact | 200,000 | `as2_complaints` | After-Sales |
| `fact_returns` | Fact | ~77,250 | `as2_returns` | After-Sales |
| `fact_financial_transactions` | Fact | ~663,000 | `fip_financial_transactions` | Finance |
| `fact_product_reviews` | Fact | 50,000 | `crm_product_reviews` | CRM |

---
