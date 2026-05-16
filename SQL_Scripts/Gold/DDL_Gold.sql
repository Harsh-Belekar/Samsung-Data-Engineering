/*
===============================================================================
DDL Script: Create Gold Views
===============================================================================
Script Purpose:
    This script creates views for the Gold layer in the Samsung data warehouse. 
    The Gold layer represents the final dimension and fact tables (Star Schema)

    Each view performs transformations and combines data from the Silver layer 
    to produce a clean, enriched, and business-ready dataset.

Usage:
    - These views can be queried directly for analytics and reporting.
===============================================================================
*/

-- =============================================================================
-- Drop VIEW IF EXISTS:
-- =============================================================================

DROP VIEW IF EXISTS gold.dim_products;
DROP VIEW IF EXISTS gold.dim_warehouses;
DROP VIEW IF EXISTS gold.dim_service_centers;
DROP VIEW IF EXISTS gold.dim_customers;
DROP VIEW IF EXISTS gold.dim_dealers;
DROP VIEW IF EXISTS gold.dim_suppliers;
DROP VIEW IF EXISTS gold.dim_campaigns;
DROP VIEW IF EXISTS gold.dim_employees;

DROP VIEW IF EXISTS gold.fact_inventory;
DROP VIEW IF EXISTS gold.fact_sales_transactions;
DROP VIEW IF EXISTS gold.fact_complaints;
DROP VIEW IF EXISTS gold.fact_returns;
DROP VIEW IF EXISTS gold.fact_financial_transactions;
DROP VIEW IF EXISTS gold.fact_product_reviews;

-- =============================================================================
-- Create Dimension: gold.dim_products
-- =============================================================================
CREATE VIEW gold.dim_products AS
SELECT 
    product_id,           
    sku,                 
    product_name,      
    category,           
    subcategory,       
    mrp_inr,           
    launch_date_india, 
    ram_gb,            
    storage_gb,        
    display_inches,    
    bis_certified,     
    warranty_years,    
    color_variants
FROM silver.hrm_products;

-- =============================================================================
-- Create Dimension: gold.dim_warehouses
-- =============================================================================
CREATE VIEW gold.dim_warehouses AS
SELECT 
    warehouse_id,   
    warehouse_name,   
    city,
    state,   
    pincode,   
    capacity_units,   
    latitude,   
    longitude,
    type
FROM silver.sci_warehouses;

-- =============================================================================
-- Create Dimension: gold.dim_service_centers
-- =============================================================================
CREATE VIEW gold.dim_service_centers AS
SELECT 
    center_id,
    center_name,
    tier,              
    city,             
    state,
    pincode,
    phone,
    email,             
    working_hours,     
    capacity_per_day, 
    is_active
FROM silver.as2_service_centers;

-- =============================================================================
-- Create Dimension: gold.dim_customers
-- =============================================================================
CREATE VIEW gold.dim_customers AS
SELECT 
    customer_id,
    full_name,
    email,
    phone,
    city,
    state,
    pincode,
    gender,
    dob,
    segment,
    registered_on,
    is_active
FROM silver.crm_customers;

-- =============================================================================
-- Create Dimension: gold.dim_dealers
-- =============================================================================
CREATE VIEW gold.dim_dealers AS
SELECT 
    dealer_id,
    dealer_name,
    store_type,
    chain,
    city,
    state,
    tier,
    contact_phone,
    active_since,
    is_exclusive
FROM silver.snd_dealers;

-- =============================================================================
-- Create Dimension: gold.dim_suppliers
-- =============================================================================
CREATE VIEW gold.dim_suppliers AS
SELECT 
    supplier_id,
    supplier_name,
    country,
    city,
    gstin,
    contact_email,
    payment_terms_days,
    category,
    rating,
    is_msme,
    contract_start
FROM silver.sci_suppliers;

-- =============================================================================
-- Create Dimension: gold.dim_campaigns
-- =============================================================================
CREATE VIEW gold.dim_campaigns AS
SELECT 
    campaign_id,
    campaign_name,
    type,
    start_date,
    end_date,
    budget_inr,
    discount_pct,
    target_region,
    target_segment,
    channel,
    status
FROM silver.hrm_campaigns;

-- =============================================================================
-- Create Dimension: gold.dim_employees
-- =============================================================================
CREATE VIEW gold.dim_employees AS
SELECT 
    employee_id,
    full_name,
    department,
    designation,
    location,
    join_date,
    salary_inr,
    manager_id,
    gender,
    pf_number,
    is_active
FROM silver.hrm_employees;

-- =============================================================================
-- Create Fact Table: gold.fact_inventory
-- =============================================================================
CREATE VIEW gold.fact_inventory AS
SELECT 
    inventory_id,
    product_id,
    warehouse_id,
    qty_available,  
    qty_reserved,
    reorder_level,
    last_restocked,
    snapshot_date
FROM silver.sci_inventory;

-- =============================================================================
-- Create Fact Table: gold.fact_sales_transactions
-- =============================================================================
CREATE VIEW gold.fact_sales_transactions AS
SELECT 
    txn_id,
    customer_id,
    product_id,
    dealer_id,
    txn_date,
    amount_inr,
    gst_amount,
    payment_mode,
    channel,
    city,
    state,
    status
FROM silver.snd_sales_transactions;

-- =============================================================================
-- Create Fact Table: gold.fact_complaints
-- =============================================================================
CREATE VIEW gold.fact_complaints AS
SELECT 
    complaint_id,
    customer_id,
    product_id,
    center_id,
    complaint_date,
    issue_type,
    priority,
    status,
    resolution_date,
    resolution_days,
    csat_score,
    technician_id
FROM silver.as2_complaints;

-- =============================================================================
-- Create Fact Table: gold.fact_returns
-- =============================================================================
CREATE VIEW gold.fact_returns AS
SELECT 
    return_id,
    txn_id,
    customer_id,
    product_id,
    return_date,
    return_reason,
    condition,
    refund_amount,
    refund_mode,
    is_replacement,
    processed_by
FROM silver.as2_returns;

-- =============================================================================
-- Create Fact Table: gold.fact_financial_transactions
-- =============================================================================
CREATE VIEW gold.fact_financial_transactions AS
SELECT 
    payment_id,
    txn_id,
    payment_date,
    payment_mode,  
    amount_inr,
    gst_pct,
    bank_name,
    emi_months,
    upi_ref, 
    invoice_no,
    payment_status
FROM silver.fip_financial_transactions;

-- =============================================================================
-- Create Fact Table: gold.fact_product_reviews
-- =============================================================================
CREATE VIEW gold.fact_product_reviews AS
SELECT 
    review_id,
    customer_id,
    product_id,
    rating,
    review_text,
    review_date,
    verified_purchase,
    helpful_votes
FROM silver.crm_product_reviews;
