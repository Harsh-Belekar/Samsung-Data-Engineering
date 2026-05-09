"""
Main.py
=======
Samsung India Data Generator — main entry point.

Run this file to generate all 14 tables:
    python Main.py

All parameters (row counts, date range, quality knobs, output path)
are controlled exclusively through config.py — no edits to this file
or any generator file are needed for routine changes.

Generation order matters: later generators reference IDs produced by
earlier ones (e.g. sales_transactions needs customer_id, product_id,
and dealer_id).  The dependency chain is:

    Products ──► Inventory
    Warehouses ─►  │
    Customers ───► Sales ──► Returns
        │           │          │
    Dealers ────────┘       Financial
                            Complaints
                            Reviews
"""

import os
import time
import random
import numpy as np
import logging

# Load config first so seeds are set before any generators import
from Config import (
    NUMPY_SEED, RANDOM_SEED, OUTPUT_DIR,
    DATE_START, DATE_END, ROW_COUNTS,
)

np.random.seed(NUMPY_SEED)
random.seed(RANDOM_SEED)

# Generator imports
from Generators.Products_Warehouses        import ProductGenerator, WarehouseGenerator
from Generators.Customers_Dealers          import CustomerGenerator, DealerGenerator
from Generators.Service_Campaigns_Suppliers import (
    ServiceCenterGenerator, CampaignGenerator, SupplierGenerator,
)
from Generators.Employees_Inventory        import EmployeeGenerator, InventoryGenerator
from Generators.Transactions               import (
    SalesTransactionGenerator, ComplaintGenerator,
    ReturnGenerator, FinancialTransactionGenerator, ProductReviewGenerator,
)


# ===============================
# log Configuration
# ===============================
LOG_DIR = "Logs"
LOG_FILE = "Data_generation.log"

# Creates Logs/ folder if it doesn’t exist
os.makedirs(LOG_DIR, exist_ok=True) 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE), encoding="utf-8")
    ],
)

log = logging.getLogger(__name__)


# =====================================================================
# Main orchestrator
# =====================================================================

def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    AS2_path = OUTPUT_DIR + "/AS2" # After-Sales Service (AS2)
    CRM_path = OUTPUT_DIR + "/CRM" # Customers (CRM)
    FIP_path = OUTPUT_DIR + "/FIP" # Finance & Payments (FIN)
    HRM_path = OUTPUT_DIR + "/HRM" # HR & Marketing (HRM)
    SCI_path = OUTPUT_DIR + "/SCI" # Supply Chain & Inventory (SCI)
    SND_path = OUTPUT_DIR + "/SND" # Sales & Distribution (SND)
    
    os.makedirs(AS2_path, exist_ok=True)
    os.makedirs(CRM_path, exist_ok=True)
    os.makedirs(FIP_path, exist_ok=True)
    os.makedirs(HRM_path, exist_ok=True)
    os.makedirs(SCI_path, exist_ok=True)
    os.makedirs(SND_path, exist_ok=True)
    
    log.info("=" * 70)
    log.info("SAMSUNG RAW DATA GENERATION [INDIA]")
    log.info(f"  Date range : {DATE_START.date()}  to  {DATE_END.date()}")
    log.info(f"  Output dir : {OUTPUT_DIR}")
    log.info("=" * 70)

    print("=" * 70)
    print("  Samsung India Raw Data Generator")
    print(f"  Date range : {DATE_START.date()}  to  {DATE_END.date()}")
    print(f"  Output dir : {OUTPUT_DIR}")
    print("=" * 70)

    run_start = time.time()

    # STEP 1: Products 
    t = time.time()
    prod_gen  = ProductGenerator(HRM_path)
    prod_data = prod_gen.generate()
    prod_gen.save(prod_data)
    time_taken = time.time() - t
    print(f"[1/14] Completed Creating 'products.json'")
    log.info(f"[1/14] Completed Creating 'products.json' with {ROW_COUNTS['products']} rows in ({time_taken:.2f}s)")

    # STEP 2: Warehouses 
    t = time.time()
    wh_gen  = WarehouseGenerator(SCI_path)
    wh_data = wh_gen.generate()
    wh_gen.save(wh_data)
    time_taken = time.time() - t
    print(f"[2/14] Completed Creating 'warehouses.json'")
    log.info(f"[2/14] Completed Creating 'warehouses.json' with {ROW_COUNTS['warehouses']} rows in ({time_taken:.2f}s)")

    # STEP 3: Customers 
    t = time.time()
    cust_gen = CustomerGenerator(CRM_path)
    cust_df  = cust_gen.generate()
    cust_gen.save(cust_df)
    time_taken = time.time() - t
    print(f"[3/14] Completed Creating 'customers.csv'")
    log.info(f"[3/14] Completed Creating 'customers.csv' with {ROW_COUNTS['customers']} rows in ({time_taken:.2f}s)")

    # STEP 4: Dealers 
    t = time.time()
    dlr_gen = DealerGenerator(SND_path)
    dlr_df  = dlr_gen.generate()
    dlr_gen.save(dlr_df)
    time_taken = time.time() - t
    print(f"[4/14] Completed Creating 'dealers.csv'")
    log.info(f"[4/14] Completed Creating 'dealers.csv' with {ROW_COUNTS['dealers']} rows in ({time_taken:.2f}s)")

    # STEP 5: Service Centers 
    t = time.time()
    sc_gen  = ServiceCenterGenerator(AS2_path)
    sc_data = sc_gen.generate()
    sc_gen.save(sc_data)
    time_taken = time.time() - t
    print(f"[5/14] Completed Creating 'service_centers.json'")
    log.info(f"[5/14] Completed Creating 'service_centers.json' with {ROW_COUNTS['service_centers']} rows in ({time_taken:.2f}s)")

    # # STEP 6: Campaigns
    t = time.time()
    camp_gen = CampaignGenerator(HRM_path)
    camp_df  = camp_gen.generate()
    camp_gen.save(camp_df)
    time_taken = time.time() - t
    print(f"[6/14] Completed Creating 'campaigns.xlsx'")
    log.info(f"[6/14] Completed Creating 'campaigns.xlsx' with {ROW_COUNTS['campaigns']} rows in ({time_taken:.2f}s)")

    # STEP 7: Suppliers
    t = time.time()
    sup_gen = SupplierGenerator(SCI_path)
    sup_df  = sup_gen.generate()
    sup_gen.save(sup_df)
    time_taken = time.time() - t
    print(f"[7/14] Completed Creating 'suppliers.csv'")
    log.info(f"[7/14] Completed Creating 'suppliers.csv' with {ROW_COUNTS['suppliers']} rows in ({time_taken:.2f}s)")

    # STEP 8: Employees 
    t = time.time()
    emp_gen = EmployeeGenerator(HRM_path)
    emp_df  = emp_gen.generate()
    emp_gen.save(emp_df)
    time_taken = time.time() - t
    print(f"[8/14] Completed Creating 'employees.xlsx'")
    log.info(f"[8/14] Completed Creating 'employees.xlsx' with {ROW_COUNTS['employees']} rows in ({time_taken:.2f}s)")

    # STEP 9: Inventory (needs product + warehouse IDs)
    t = time.time()
    inv_gen = InventoryGenerator(SCI_path, prod_gen.pid_pool, wh_gen.wh_ids)
    inv_df  = inv_gen.generate()
    inv_gen.save(inv_df)
    time_taken = time.time() - t
    print(f"[9/14] Completed Creating 'inventory.xlsx'")
    log.info(f"[9/14] Completed Creating 'inventory.xlsx' with {ROW_COUNTS['inventory']} rows in ({time_taken:.2f}s)")

    # STEP 10: Sales Transactions 
    t = time.time()
    sales_gen = SalesTransactionGenerator(
        SND_path, cust_gen.cust_ids, prod_gen.pid_pool, dlr_gen.dealer_ids
    )
    sales_df = sales_gen.generate()
    sales_gen.save(sales_df)
    time_taken = time.time() - t
    print(f"[10/14] Completed Creating 'sales_transactions.csv'")
    log.info(f"[10/14] Completed Creating 'sales_transactions.csv' with {ROW_COUNTS['sales_transactions']} rows in ({time_taken:.2f}s)")

    # STEP 11: Complaints
    t = time.time()
    comp_gen = ComplaintGenerator(AS2_path, cust_gen.cust_ids, prod_gen.pid_pool)
    comp_df  = comp_gen.generate()
    comp_gen.save(comp_df)
    time_taken = time.time() - t
    print(f"[11/14] Completed Creating 'complaints.csv'")
    log.info(f"[11/14] Completed Creating 'complaints.csv' with {ROW_COUNTS['complaints']} rows in ({time_taken:.2f}s)")

    # STEP 12: Returns
    t = time.time()
    ret_gen = ReturnGenerator(
        AS2_path, sales_gen.txn_ids, cust_gen.cust_ids, prod_gen.pid_pool
    )
    ret_df = ret_gen.generate()
    ret_gen.save(ret_df)
    time_taken = time.time() - t
    print(f"[12/14] Completed Creating 'returns.xlsx'")
    log.info(f"[12/14] Completed Creating 'returns.xlsx' with {ROW_COUNTS['returns']} rows in ({time_taken:.2f}s)")

    # STEP 13: Financial Transactions
    t = time.time()
    fin_gen = FinancialTransactionGenerator(FIP_path, sales_gen.txn_ids)
    fin_df  = fin_gen.generate()
    fin_gen.save(fin_df)
    time_taken = time.time() - t
    print(f"[13/14] Completed Creating 'financial_transactions.csv'")
    log.info(f"[13/14] Completed Creating 'financial_transactions.csv' with {ROW_COUNTS['financial_transactions']} rows in ({time_taken:.2f}s)")

    # STEP 14: Product Reviews
    t = time.time()
    rev_gen = ProductReviewGenerator(CRM_path, cust_gen.cust_ids, prod_gen.pid_pool)
    rev_df  = rev_gen.generate()
    rev_gen.save(rev_df)
    time_taken = time.time() - t
    print(f"[14/14] Completed Creating 'product_reviews.csv'")
    log.info(f"[14/14] Completed Creating 'product_reviews.csv' with {ROW_COUNTS['product_reviews']} rows in ({time_taken:.2f}s)\n")

    # Summary 
    print_summary(run_start)


def print_summary(run_start: float) -> None:
    """Print a formatted file-size summary table."""
    table = [
        ("products.json",             "JSON"),
        ("warehouses.json",           "JSON"),
        ("service_centers.json",      "JSON"),
        ("customers.csv",             "CSV"),
        ("dealers.csv",               "CSV"),
        ("suppliers.csv",             "CSV"),
        ("sales_transactions.csv",    "CSV"),
        ("complaints.csv",            "CSV"),
        ("financial_transactions.csv","CSV"),
        ("product_reviews.csv",       "CSV"),
        ("campaigns.xlsx",            "XLSX"),
        ("employees.xlsx",            "XLSX"),
        ("inventory.xlsx",            "XLSX"),
        ("returns.xlsx",              "XLSX"),
    ]
    
    log.info("=" * 70)
    log.info(" GENERATION COMPLETE - File Summary")
    log.info("=" * 70)
    log.info(f"  {'FORMAT':<6}  {'FILE':<40}  {'SIZE':>8}")
    log.info(f"  {'-'*6}  {'-'*40}  {'-'*8}")

    total_mb = 0.0
    for fname, fmt in table:
        fpath = os.path.join(OUTPUT_DIR, fname)
        mb    = os.path.getsize(fpath) / (1024 * 1024) if os.path.exists(fpath) else 0.0
        total_mb += mb
        log.info(f"  {fmt:<6}  {fname:<40}  {mb:>7.2f} MB")

    elapsed = time.time() - run_start
    
    log.info(f"  {'-'*6}  {'-'*40}  {'-'*8}")
    log.info(f"  {'TOTAL':<6}  {'':<40}  {total_mb:>7.2f} MB")
    log.info(f"  Total generation time : {elapsed:.2f}s")
    log.info(f"  Output dir : {OUTPUT_DIR}")
    log.info("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log.exception("FATAL ERROR — data generation aborted: %s", exc)
        raise
