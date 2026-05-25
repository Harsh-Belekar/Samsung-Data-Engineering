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
