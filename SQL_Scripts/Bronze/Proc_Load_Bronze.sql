/*
===============================================================================
Stored Procedure: Load Bronze Layer (Source -> Bronze)
===============================================================================
Script Purpose:
    This stored procedure loads data into the 'bronze' schema from external CSV files. 
    It performs the following actions:
    - Truncates the bronze tables before loading data.
    - Uses the `COPY FROM` command to load data from csv Files to bronze tables.

Database:
    PostgreSQL

Parameters:
    None. 
	This stored procedure does not accept any parameters or return any values.

Usage Example:
    CALL bronze.load_bronze();
===============================================================================
*/

CREATE OR REPLACE PROCEDURE bronze.load_bronze()
LANGUAGE PLPGSQL
AS $$
DECLARE 
    start_time TIMESTAMP; 
    end_time TIMESTAMP; 
    batch_start_time TIMESTAMP;
    batch_end_time TIMESTAMP;
    duration_seconds NUMERIC;
BEGIN
	batch_start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '================================================';
	RAISE NOTICE 'Loading Bronze Layer';
	RAISE NOTICE '================================================';
	
	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading After-Sales Service (AS2) Tables';
	RAISE NOTICE '------------------------------------------------';

    start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.as2_complaints';
	TRUNCATE TABLE bronze.as2_complaints;
	RAISE NOTICE '>> Inserting Data Into: bronze.as2_complaints';
	COPY bronze.as2_complaints (complaint_id,customer_id,product_id,center_id,complaint_date,
                                issue_type,priority,status,resolution_date,resolution_days,
                                csat_score,technician_id)
	FROM 'D:\Samsung_Data\AS2\complaints.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.as2_returns';
	TRUNCATE TABLE bronze.as2_returns;
	RAISE NOTICE '>> Inserting Data Into: bronze.as2_returns';
	COPY bronze.as2_returns (return_id,txn_id,customer_id,product_id,return_date,
							return_reason,condition,refund_amount,refund_mode,
							is_replacement,processed_by)
	FROM 'D:\Samsung_Data\AS2\returns.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.as2_service_centers';
	TRUNCATE TABLE bronze.as2_service_centers;
	RAISE NOTICE '>> Inserting Data Into: bronze.as2_service_centers';
	COPY bronze.as2_service_centers (center_id,center_name,tier,city,state,pincode,
									phone,email,working_hours,capacity_per_day,is_active)
	FROM 'D:\Samsung_Data\AS2\service_centers.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading Customers (CRM) Tables';
	RAISE NOTICE '------------------------------------------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.crm_customers';
	TRUNCATE TABLE bronze.crm_customers;
	RAISE NOTICE '>> Inserting Data Into: bronze.crm_customers';
	COPY bronze.crm_customers (customer_id,full_name,email,phone,city,state,
								pincode,gender,dob,segment,registered_on,is_active)
	FROM 'D:\Samsung_Data\CRM\customers.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.crm_product_reviews';
	TRUNCATE TABLE bronze.crm_product_reviews;
	RAISE NOTICE '>> Inserting Data Into: bronze.crm_product_reviews';
	COPY bronze.crm_product_reviews (review_id,customer_id,product_id,rating,review_text,
										review_date,verified_purchase,helpful_votes)
	FROM 'D:\Samsung_Data\CRM\product_reviews.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading Finance & Payments (FIP) Tables';
	RAISE NOTICE '------------------------------------------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.fip_financial_transactions';
	TRUNCATE TABLE bronze.fip_financial_transactions;
	RAISE NOTICE '>> Inserting Data Into: bronze.fip_financial_transactions';
	COPY bronze.fip_financial_transactions (payment_id,txn_id,payment_date,payment_mode,  
											amount_inr,gst_pct,bank_name,emi_months,upi_ref, 
											invoice_no,payment_status)
	FROM 'D:\Samsung_Data\FIP\financial_transactions.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading HR & Marketing (HRM) Tables';
	RAISE NOTICE '------------------------------------------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.hrm_campaigns';
	TRUNCATE TABLE bronze.hrm_campaigns;
	RAISE NOTICE '>> Inserting Data Into: bronze.hrm_campaigns';
	COPY bronze.hrm_campaigns (campaign_id,campaign_name,type,start_date,end_date,budget_inr,
								discount_pct,target_region,target_segment,channel,status)
	FROM 'D:\Samsung_Data\HRM\campaigns.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.hrm_employees';
	TRUNCATE TABLE bronze.hrm_employees;
	RAISE NOTICE '>> Inserting Data Into: bronze.hrm_employees';
	COPY bronze.hrm_employees (employee_id,full_name,department,designation,location,
								join_date,salary_inr,manager_id,gender,pf_number,
								is_active)
	FROM 'D:\Samsung_Data\HRM\employees.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.hrm_products';
	TRUNCATE TABLE bronze.hrm_products;
	RAISE NOTICE '>> Inserting Data Into: bronze.hrm_products';
	COPY bronze.hrm_products (product_id,sku,product_name,category,subcategory,mrp_inr, 
							launch_date_india,ram_gb,storage_gb,display_inches,bis_certified,
							warranty_years,color_variants)
	FROM 'D:\Samsung_Data\HRM\products.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading Supply Chain & Inventory (SCI) Tables';
	RAISE NOTICE '------------------------------------------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.sci_inventory';
	TRUNCATE TABLE bronze.sci_inventory;
	RAISE NOTICE '>> Inserting Data Into: bronze.sci_inventory';
	COPY bronze.sci_inventory (inventory_id,product_id,warehouse_id,qty_available,  
								qty_reserved,reorder_level,last_restocked,snapshot_date)
	FROM 'D:\Samsung_Data\SCI\inventory.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.sci_suppliers';
	TRUNCATE TABLE bronze.sci_suppliers;
	RAISE NOTICE '>> Inserting Data Into: bronze.sci_suppliers';
	COPY bronze.sci_suppliers (supplier_id,supplier_name,country,city,gstin,contact_email,
								payment_terms_days,category,rating,is_msme,contract_start)
	FROM 'D:\Samsung_Data\SCI\suppliers.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.sci_warehouses';
	TRUNCATE TABLE bronze.sci_warehouses;
	RAISE NOTICE '>> Inserting Data Into: bronze.sci_warehouses';
	COPY bronze.sci_warehouses (warehouse_id,warehouse_name,city,state,pincode,capacity_units,
								latitude,longitude,type)
	FROM 'D:\Samsung_Data\SCI\warehouses.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


	RAISE NOTICE '------------------------------------------------';
	RAISE NOTICE 'Loading Sales & Distribution (SND) Tables';
	RAISE NOTICE '------------------------------------------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.snd_dealers';
	TRUNCATE TABLE bronze.snd_dealers;
	RAISE NOTICE '>> Inserting Data Into: bronze.snd_dealers';
	COPY bronze.snd_dealers (dealer_id,dealer_name,store_type,chain,city,state,
							tier,contact_phone,active_since,is_exclusive)
	FROM 'D:\Samsung_Data\SND\dealers.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';

	start_time := clock_timestamp(); -- Record start time
	RAISE NOTICE '>> Truncating Table: bronze.snd_sales_transactions';
	TRUNCATE TABLE bronze.snd_sales_transactions;
	RAISE NOTICE '>> Inserting Data Into: bronze.snd_sales_transactions';
	COPY bronze.snd_sales_transactions (txn_id,customer_id,product_id,dealer_id,txn_date,
										amount_inr,gst_amount,payment_mode,channel,city,
										state,status)
	FROM 'D:\Samsung_Data\SND\sales_transactions.csv'
	DELIMITER ','
	CSV
	HEADER;
	end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (end_time - start_time));
	RAISE NOTICE '>> Load Duration: % seconds', duration_seconds;
    RAISE NOTICE '>> -------------';


    batch_end_time := clock_timestamp(); -- Record end time
	duration_seconds := EXTRACT(EPOCH FROM (batch_end_time - batch_start_time));
	RAISE NOTICE '==========================================';
	RAISE NOTICE '>> Loading Bronze Layer is Completed';
    RAISE NOTICE '>> Total Load Duration: % seconds ', duration_seconds;
	RAISE NOTICE '==========================================';

EXCEPTION
	WHEN others THEN
		RAISE NOTICE '==========================================';
		RAISE NOTICE '❌ ERROR OCCURED DURING LOADING BRONZE LAYER';
		RAISE NOTICE 'Error Message %', SQLERRM;
		RAISE NOTICE 'Error SQL State Code: %' , SQLSTATE;
		RAISE NOTICE '==========================================';
END
$$;
