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
