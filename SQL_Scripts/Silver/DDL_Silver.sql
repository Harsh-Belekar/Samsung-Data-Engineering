/*
===============================================================================
DDL Script: Create Silver Tables
===============================================================================
Script Purpose:
    This script creates tables in the 'silver' schema, dropping existing tables 
    if they already exist.
	Run this script to re-define the DDL structure of 'bronze' Tables
===============================================================================
*/


-- ===============================================================================
-- After-Sales Service (AS2) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.as2_complaints;
CREATE TABLE silver.as2_complaints (
    complaint_id     VARCHAR(50),
    customer_id      VARCHAR(50),
    product_id       VARCHAR(50),
    center_id        VARCHAR(50),
    complaint_date   DATE,
    issue_type       VARCHAR(50),
    priority         VARCHAR(50),
    status           VARCHAR(50),
    resolution_date  DATE,
    resolution_days  SMALLINT,
    csat_score       SMALLINT,
    technician_id    VARCHAR(50)
);

DROP TABLE IF EXISTS silver.as2_returns;
CREATE TABLE silver.as2_returns (
    return_id       VARCHAR(50),
    txn_id          VARCHAR(50),
    customer_id     VARCHAR(50),
    product_id      VARCHAR(50),
    return_date     DATE,
    return_reason   TEXT,
    condition       VARCHAR(50),
    refund_amount   NUMERIC(10, 2),
    refund_mode     VARCHAR(50),
    is_replacement  BOOLEAN,
    processed_by    VARCHAR(50)
);

DROP TABLE IF EXISTS silver.as2_service_centers;
CREATE TABLE silver.as2_service_centers (
    center_id         VARCHAR(50),   
    center_name       TEXT,  
    tier              VARCHAR(50),   
    city              VARCHAR(50),
    state             VARCHAR(50),  
    pincode           INT,   
    phone             BIGINT, 
    email             TEXT,
    working_hours     VARCHAR(50), 
    capacity_per_day  SMALLINT, 
    is_active         VARCHAR(50)
);


-- ===============================================================================
-- Customers (CRM) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.crm_customers;
CREATE TABLE silver.crm_customers (
    customer_id    VARCHAR(50),   
    full_name      TEXT,   
    email          TEXT,   
    phone          BIGINT,   
    city           VARCHAR(50),
    state          VARCHAR(50),
    pincode        INT,  
    gender         VARCHAR(50),   
    dob            DATE,   
    segment        VARCHAR(50),   
    registered_on  DATE,   
    is_active      BOOLEAN
);

DROP TABLE IF EXISTS silver.crm_product_reviews;
CREATE TABLE silver.crm_product_reviews (
    review_id          VARCHAR(50),
    customer_id        VARCHAR(50),   
    product_id         VARCHAR(50),   
    rating             SMALLINT,   
    review_text        TEXT,   
    review_date        DATE,   
    verified_purchase  BOOLEAN,   
    helpful_votes      INT
);


-- ===============================================================================
-- Finance & Payments (FIP) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.fip_financial_transactions;
CREATE TABLE silver.fip_financial_transactions (
    payment_id      VARCHAR(50),   
    txn_id          VARCHAR(50), 
    payment_date    DATE,   
    payment_mode    VARCHAR(50),   
    amount_inr      NUMERIC(12, 2),   
    gst_pct         SMALLINT,   
    bank_name       VARCHAR(50),   
    emi_months      SMALLINT,   
    upi_ref         TEXT,   
    invoice_no      TEXT,   
    payment_status  VARCHAR(50)
);


-- ===============================================================================
-- HR & Marketing (HRM) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.hrm_campaigns;
CREATE TABLE silver.hrm_campaigns (
    campaign_id      VARCHAR(50), 
    campaign_name    TEXT,   
    type             VARCHAR(50),   
    start_date       DATE,   
    end_date         DATE,   
    budget_inr       NUMERIC(12, 2),  
    discount_pct     NUMERIC(4, 1),   
    target_region    VARCHAR(50),   
    target_segment   VARCHAR(50),   
    channel          VARCHAR(50),   
    status           VARCHAR(50)
);

DROP TABLE IF EXISTS silver.hrm_employees;
CREATE TABLE silver.hrm_employees (
    employee_id  VARCHAR(50),
    full_name    VARCHAR(50),
    department   VARCHAR(50),   
    designation  VARCHAR(50),   
    location     TEXT,   
    join_date    DATE,   
    salary_inr   NUMERIC(12, 2),  
    manager_id   VARCHAR(50),   
    gender       VARCHAR(50),   
    pf_number    TEXT, 
    is_active    BOOLEAN
);

DROP TABLE IF EXISTS silver.hrm_products;
CREATE TABLE silver.hrm_products (
    product_id        VARCHAR(50),   
    sku               VARCHAR(50),   
    product_name      TEXT,   
    category          VARCHAR(50),   
    subcategory       TEXT,   
    mrp_inr           NUMERIC(10, 2),   
    launch_date_india DATE,   
    ram_gb            SMALLINT,   
    storage_gb        SMALLINT,   
    display_inches    NUMERIC(4, 1),   
    bis_certified     BOOLEAN,   
    warranty_years    SMALLINT,   
    color_variants    SMALLINT
);


-- ===============================================================================
-- Supply Chain & Inventory (SCI) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.sci_inventory;
CREATE TABLE silver.sci_inventory (
    inventory_id    VARCHAR(50), 
    product_id      VARCHAR(50),   
    warehouse_id    VARCHAR(50),   
    qty_available   INT,   
    qty_reserved    INT,   
    reorder_level   INT,   
    last_restocked  DATE,   
    snapshot_date   DATE
);

DROP TABLE IF EXISTS silver.sci_suppliers;
CREATE TABLE silver.sci_suppliers (
    supplier_id          VARCHAR(50), 
    supplier_name        TEXT,   
    country              VARCHAR(50),   
    city                 VARCHAR(50),
    gstin                TEXT,   
    contact_email        TEXT,
    payment_terms_days   SMALLINT,   
    category             VARCHAR(50),   
    rating               NUMERIC(3, 1),   
    is_msme              BOOLEAN,   
    contract_start       DATE
);

DROP TABLE IF EXISTS silver.sci_warehouses;
CREATE TABLE silver.sci_warehouses (
    warehouse_id    VARCHAR(50),   
    warehouse_name  TEXT,   
    city            VARCHAR(50),
    state           VARCHAR(50),   
    pincode         INT,   
    capacity_units  INT,   
    latitude        NUMERIC(9, 6),   
    longitude       NUMERIC(9, 6),
    type            VARCHAR(50)
);


-- ===============================================================================
-- Sales & Distribution (SND) Tables
-- ===============================================================================

DROP TABLE IF EXISTS silver.snd_dealers;
CREATE TABLE silver.snd_dealers (
    dealer_id      VARCHAR(50),   
    dealer_name    TEXT,   
    store_type     TEXT,   
    chain          VARCHAR(50),   
    city           VARCHAR(50),
    state          VARCHAR(50),
    tier           VARCHAR(50),   
    contact_phone  BIGINT,
    active_since   VARCHAR(50),   
    is_exclusive   BOOLEAN
);

DROP TABLE IF EXISTS silver.snd_sales_transactions;
CREATE TABLE silver.snd_sales_transactions (
    txn_id        VARCHAR(50), 
    customer_id   VARCHAR(50),   
    product_id    VARCHAR(50),   
    dealer_id     VARCHAR(50),   
    txn_date      DATE,   
    amount_inr    NUMERIC(12, 2),   
    gst_amount    NUMERIC(12, 2),   
    payment_mode  VARCHAR(50),   
    channel       VARCHAR(50),   
    city          VARCHAR(50),
    state         VARCHAR(50),
    status        VARCHAR(50)
);
