/*
===============================================================================
SAMSUNG INDIA — DATA ENGINEERING PROJECT
DDL Script: Create Bronze Tables
===============================================================================
Script Purpose:
    This script creates tables in the 'bronze' schema, dropping existing tables 
    if they already exist.
	Run this script to re-define the DDL structure of 'bronze' Tables

Author       : Harsh Belekar
Project      : Samsung India Data Pipeline
Pipeline     : Raw → Bronze → Silver → Gold
===============================================================================
*/

-- ===============================================================================
-- Source: After-Sales Service (AS2)  
-- ===============================================================================

DROP TABLE IF EXISTS bronze.as2_complaints;
CREATE TABLE bronze.as2_complaints (
    complaint_id     TEXT,
    customer_id      TEXT,
    product_id       TEXT,
    center_id        TEXT,
    complaint_date   TEXT,
    issue_type       TEXT,
    priority         TEXT,
    status           TEXT,
    resolution_date  TEXT,
    resolution_days  TEXT,
    csat_score       TEXT,
    technician_id    TEXT
);

DROP TABLE IF EXISTS bronze.as2_returns;
CREATE TABLE bronze.as2_returns (
    return_id       TEXT,
    txn_id          TEXT,
    customer_id     TEXT,
    product_id      TEXT,
    return_date     TEXT,
    return_reason   TEXT,
    condition       TEXT,
    refund_amount   TEXT,
    refund_mode     TEXT,
    is_replacement  TEXT,
    processed_by    TEXT
);

DROP TABLE IF EXISTS bronze.as2_service_centers;
CREATE TABLE bronze.as2_service_centers (
    center_id         TEXT,   
    center_name       TEXT,  
    tier              TEXT,   
    city              TEXT,
    state             TEXT,  
    pincode           TEXT,   
    phone             TEXT, 
    email             TEXT,
    working_hours     TEXT, 
    capacity_per_day  TEXT, 
    is_active         TEXT
);


-- ===============================================================================
-- Source: Customers (CRM)  
-- ===============================================================================

DROP TABLE IF EXISTS bronze.crm_customers;
CREATE TABLE bronze.crm_customers (
    customer_id    TEXT,   
    full_name      TEXT,   
    email          TEXT,   
    phone          TEXT,   
    city           TEXT,
    state          TEXT,
    pincode        TEXT,  
    gender         TEXT,   
    dob            TEXT,   
    segment        TEXT,   
    registered_on  TEXT,   
    is_active      TEXT
);

DROP TABLE IF EXISTS bronze.crm_product_reviews;
CREATE TABLE bronze.crm_product_reviews (
    review_id          TEXT,
    customer_id        TEXT,   
    product_id         TEXT,   
    rating             TEXT,   
    review_text        TEXT,   
    review_date        TEXT,   
    verified_purchase  TEXT,   
    helpful_votes      TEXT
);


-- ===============================================================================
-- Source: Finance & Payments (FIP) 
-- ===============================================================================

DROP TABLE IF EXISTS bronze.fip_financial_transactions;
CREATE TABLE bronze.fip_financial_transactions (
    payment_id      TEXT,   
    txn_id          TEXT, 
    payment_date    TEXT,   
    payment_mode    TEXT,   
    amount_inr      TEXT,   
    gst_pct         TEXT,   
    bank_name       TEXT,   
    emi_months      TEXT,   
    upi_ref         TEXT,   
    invoice_no      TEXT,   
    payment_status  TEXT
);


-- ===============================================================================
-- Source: HR & Marketing (HRM) 
-- ===============================================================================

DROP TABLE IF EXISTS bronze.hrm_campaigns;
CREATE TABLE bronze.hrm_campaigns (
    campaign_id      TEXT, 
    campaign_name    TEXT,   
    type             TEXT,   
    start_date       TEXT,   
    end_date         TEXT,   
    budget_inr       TEXT,  
    discount_pct     TEXT,   
    target_region    TEXT,   
    target_segment   TEXT,   
    channel          TEXT,   
    status           TEXT
);

DROP TABLE IF EXISTS bronze.hrm_employees;
CREATE TABLE bronze.hrm_employees (
    employee_id  TEXT,
    full_name    TEXT,
    department   TEXT,   
    designation  TEXT,   
    location     TEXT,   
    join_date    TEXT,   
    salary_inr   TEXT,  
    manager_id   TEXT,   
    gender       TEXT,   
    pf_number    TEXT, 
    is_active    TEXT
);

DROP TABLE IF EXISTS bronze.hrm_products;
CREATE TABLE bronze.hrm_products (
    product_id        TEXT,   
    sku               TEXT,   
    product_name      TEXT,   
    category          TEXT,   
    subcategory       TEXT,   
    mrp_inr           TEXT,   
    launch_date_india TEXT,   
    ram_gb            TEXT,   
    storage_gb        TEXT,   
    display_inches    TEXT,   
    bis_certified     TEXT,   
    warranty_years    TEXT,   
    color_variants    TEXT
);


-- ===============================================================================
-- Source: Supply Chain & Inventory (SCI)
-- ===============================================================================

DROP TABLE IF EXISTS bronze.sci_inventory;
CREATE TABLE bronze.sci_inventory (
    inventory_id    TEXT, 
    product_id      TEXT,   
    warehouse_id    TEXT,   
    qty_available   TEXT,   
    qty_reserved    TEXT,   
    reorder_level   TEXT,   
    last_restocked  TEXT,   
    snapshot_date   TEXT
);

DROP TABLE IF EXISTS bronze.sci_suppliers;
CREATE TABLE bronze.sci_suppliers (
    supplier_id          TEXT, 
    supplier_name        TEXT,   
    country              TEXT,   
    city                 TEXT,
    gstin                TEXT,   
    contact_email        TEXT,
    payment_terms_days   TEXT,   
    category             TEXT,   
    rating               TEXT,   
    is_msme              TEXT,   
    contract_start       TEXT
);

DROP TABLE IF EXISTS bronze.sci_warehouses;
CREATE TABLE bronze.sci_warehouses (
    warehouse_id    TEXT,   
    warehouse_name  TEXT,   
    city            TEXT,
    state           TEXT,   
    pincode         TEXT,   
    capacity_units  TEXT,   
    latitude        TEXT,   
    longitude       TEXT,
    type            TEXT
);


-- ===============================================================================
-- Source: Sales & Distribution (SND)
-- ===============================================================================

DROP TABLE IF EXISTS bronze.snd_dealers;
CREATE TABLE bronze.snd_dealers (
    dealer_id      TEXT,   
    dealer_name    TEXT,   
    store_type     TEXT,   
    chain          TEXT,   
    city           TEXT,
    state          TEXT,
    tier           TEXT,   
    contact_phone  TEXT,
    active_since   TEXT,   
    is_exclusive   TEXT
);

DROP TABLE IF EXISTS bronze.snd_sales_transactions;
CREATE TABLE bronze.snd_sales_transactions (
    txn_id        TEXT, 
    customer_id   TEXT,   
    product_id    TEXT,   
    dealer_id     TEXT,   
    txn_date      TEXT,   
    amount_inr    TEXT,   
    gst_amount    TEXT,   
    payment_mode  TEXT,   
    channel       TEXT,   
    city          TEXT,
    state         TEXT,
    status        TEXT
);
