"""
Generators/Transactions.py
============================
Generates the five large transactional tables:
    1. sales_transactions.csv      — 750,000 rows  → CSV
    2. complaints.csv              — 200,000 rows  → CSV
    3. returns.xlsx                —  75,000 rows  → XLSX  (+ ~3 % dups)
    4. financial_transactions.csv  — 650,000 rows  → CSV   (+ ~2 % dups)
    5. product_reviews.csv         —  50,000 rows  → CSV

Every class requires upstream ID pools as constructor arguments so
foreign-key relationships are maintained across tables.
"""

import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from Config      import ROW_COUNTS, DATE_START, DATE_END, DATE_FORMATS, QUALITY
from Master_data import (
    PAYMENT_MODES, CHANNELS, CITIES, CITIES_STATES, BANKS,
    ISSUE_TYPES, RETURN_REASONS, COMPLAINT_STATUS, REVIEW_TEXTS,
)
from Utils import rnd_date, rnd_upi, add_messy


class SalesTransactionGenerator:
    """
    Generates the primary sales-transaction fact table.

    Foreign keys required:
        cust_ids   : list[str]  — from CustomerGenerator
        pid_pool   : list[str]  — from ProductGenerator
        dealer_ids : list[str]  — from DealerGenerator

    Messiness: negative amounts (~2 %), wrong-currency prefix ("USD"),
    null amounts, null GST amounts, mixed payment-mode casing/spelling,
    mixed date formats, mixed status casing.

    Attributes
    ----------
    txn_ids : List of generated txn_id strings — used as FK by
                FinancialTransactionGenerator and ReturnGenerator.
    """

    def __init__(self, out_dir: str, cust_ids: list, pid_pool: list, dealer_ids: list):
        self.n          = ROW_COUNTS["sales_transactions"]
        self.out_path   = f"{out_dir}/sales_transactions.csv"
        self.cust_ids   = cust_ids
        self.pid_pool   = pid_pool
        self.dealer_ids = dealer_ids
        self.txn_ids: list = []

    def generate(self) -> pd.DataFrame:
        n = self.n
        self.txn_ids = [f"TXN{i + 1:08d}" for i in range(n)]

        amounts_raw = np.random.randint(5_000, 200_000, n)

        # Inject messy amount values
        amounts = []
        for a in amounts_raw:
            r = random.random()
            if r < 0.02:
                amounts.append(str(-a))          # negative (data error)
            elif r < 0.04:
                amounts.append(f"USD {a}")       # wrong currency prefix
            elif r < 0.06:
                amounts.append(None)             # missing
            else:
                amounts.append(str(a))

        gst_amounts = [
            str(int(a * 0.18)) if isinstance(a, (int, float)) else None
            for a in amounts_raw
        ]

        pay_modes = np.random.choice(
            PAYMENT_MODES, n, p=[0.35, 0.20, 0.15, 0.08, 0.12, 0.07, 0.03]
        )
        pay_modes_messy = add_messy(
            list(pay_modes), null_pct=0.04,
            bad_vals=["upi", "CREDIT", "debit card", "cod"], bad_pct=0.03,
        )

        # Channel distribution: Flipkart & Amazon most popular in India
        channels = np.random.choice(
            CHANNELS, n, p=[0.08, 0.28, 0.22, 0.12, 0.10, 0.07, 0.09, 0.04]
        )
        cities_txn = np.random.choice(CITIES, n)
        states_txn = [
            CITIES_STATES[CITIES.index(c)][1] if c in CITIES else "Unknown"
            for c in cities_txn
        ]

        return pd.DataFrame({
            "txn_id"       : self.txn_ids,
            "customer_id"  : np.random.choice(self.cust_ids,   n),
            "product_id"   : np.random.choice(self.pid_pool,   n),
            "dealer_id"    : np.random.choice(self.dealer_ids, n),
            "txn_date"     : rnd_date(DATE_START, DATE_END, n, DATE_FORMATS),
            "amount_inr"   : amounts,
            "gst_amount"   : add_messy(gst_amounts, null_pct=QUALITY["null_pct_default"]),
            "payment_mode" : pay_modes_messy,
            "channel"      : channels,
            "city"         : cities_txn,
            "state"        : states_txn,
            "status"       : np.random.choice(
                ["Completed","Pending","Failed","Returned","Cancelled","completed","FAILED"],
                n, p=[0.78, 0.08, 0.04, 0.04, 0.03, 0.02, 0.01],
            ),
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)


class ComplaintGenerator:
    """
    Generates the customer-complaint / after-sales service table.

    Foreign keys required:
        cust_ids : list[str]
        pid_pool : list[str]

    Messiness: mixed priority encodings (High/high/P1/URGENT),
    null issue types, null CSAT scores, null resolution dates for
    unresolved complaints.
    """

    def __init__(self, out_dir: str, cust_ids: list, pid_pool: list):
        self.n        = ROW_COUNTS["complaints"]
        self.out_path = f"{out_dir}/complaints.csv"
        self.cust_ids = cust_ids
        self.pid_pool = pid_pool

    def generate(self) -> pd.DataFrame:
        n = self.n

        comp_dates = rnd_date(DATE_START, DATE_END, n)
        statuses   = np.random.choice(
            COMPLAINT_STATUS, n, p=[0.15, 0.20, 0.35, 0.20, 0.05, 0.03, 0.02]
        )

        # Resolution date/days: only populated for resolved/closed complaints
        res_days  = []
        res_dates = []
        for i in range(n):
            if statuses[i] in ("Resolved", "Closed") and random.random() > 0.05:
                days = int(np.random.exponential(5)) + 1
                res_days.append(str(days))
                base = datetime.strptime(comp_dates[i], "%Y-%m-%d")
                res_dates.append((base + timedelta(days=days)).strftime("%Y-%m-%d"))
            else:
                res_days.append(None)
                res_dates.append(None)

        return pd.DataFrame({
            "complaint_id"    : [f"CMP{i + 1:08d}" for i in range(n)],
            "customer_id"     : np.random.choice(self.cust_ids, n),
            "product_id"      : np.random.choice(self.pid_pool, n),
            # Service centre IDs reference the 1,200 centres generated
            "center_id"       : [f"SC{np.random.randint(1, 1201):04d}" for _ in range(n)],
            "complaint_date"  : comp_dates,
            "issue_type"      : add_messy(
                list(np.random.choice(ISSUE_TYPES, n)),
                null_pct=QUALITY["null_pct_default"],
            ),
            "priority"        : add_messy(
                list(np.random.choice(
                    ["High","Medium","Low","URGENT","high","medium","P1","P2","P3"],
                    n, p=[0.20, 0.45, 0.25, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01],
                )),
                null_pct=QUALITY["null_pct_default"],
            ),
            "status"          : statuses,
            "resolution_date" : res_dates,
            "resolution_days" : res_days,
            "csat_score"      : [
                str(random.randint(1, 5)) if random.random() > 0.15 else None
                for _ in range(n)
            ],
            "technician_id"   : [
                f"TECH{random.randint(1, 500):04d}" if random.random() > 0.08 else None
                for _ in range(n)
            ],
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)


class ReturnGenerator:
    """
    Generates the product-return table.

    ~3 % duplicate rows are appended to simulate ETL double-loading.

    Foreign keys required:
        txn_ids  : list[str]  — from SalesTransactionGenerator
        cust_ids : list[str]
        pid_pool : list[str]
    """

    def __init__(self, out_dir: str, txn_ids: list, cust_ids: list, pid_pool: list):
        self.n        = ROW_COUNTS["returns"]
        self.out_path = f"{out_dir}/returns.xlsx"
        self.txn_ids  = txn_ids
        self.cust_ids = cust_ids
        self.pid_pool = pid_pool

    def generate(self) -> pd.DataFrame:
        n = self.n

        df = pd.DataFrame({
            "return_id"      : [f"RET{i + 1:07d}" for i in range(n)],
            "txn_id"         : np.random.choice(self.txn_ids,  n),
            "customer_id"    : np.random.choice(self.cust_ids, n),
            "product_id"     : np.random.choice(self.pid_pool, n),
            "return_date"    : rnd_date(DATE_START, DATE_END, n, DATE_FORMATS),
            "return_reason"  : add_messy(
                list(np.random.choice(RETURN_REASONS, n)),
                null_pct=0.04, bad_vals=["N/A", "?", "other"], bad_pct=0.03,
            ),
            "condition"      : np.random.choice(
                ["Good","Fair","Damaged","Opened","Sealed","damaged","GOOD","fair"], n
            ),
            "refund_amount"  : [
                str(np.random.randint(1_000, 180_000)) if random.random() > 0.07 else None
                for _ in range(n)
            ],
            "refund_mode"    : np.random.choice(
                ["Original Payment Mode","Bank Transfer","Wallet Credit",
                    "Gift Card","upi","bank transfer","NEFT"], n
            ),
            "is_replacement" : np.random.choice(
                ["Yes","No","1","0","TRUE","FALSE","true"],
                n, p=[0.30, 0.40, 0.10, 0.10, 0.04, 0.04, 0.02],
            ),
            "processed_by"   : [
                f"EMP{np.random.randint(1, ROW_COUNTS['employees'] + 1):06d}"
                for _ in range(n)
            ],
        })

        # Inject ~3 % duplicate rows to simulate double-loading
        dup_rows = df.sample(int(n * QUALITY["returns_dup_pct"]))
        return pd.concat([df, dup_rows], ignore_index=True)

    def save(self, df: pd.DataFrame) -> None:
        df.to_excel(self.out_path, index=False, engine="openpyxl")


class FinancialTransactionGenerator:
    """
    Generates the payment / financial-ledger table.

    ~2 % duplicate rows are appended to simulate ETL double-loading.
    UPI reference VPAs are only populated for UPI payments.
    EMI tenure (months) is only populated for EMI payments.

    Foreign keys required:
        txn_ids : list[str]  — from SalesTransactionGenerator
    """

    def __init__(self, out_dir: str, txn_ids: list):
        self.n        = ROW_COUNTS["financial_transactions"]
        self.out_path = f"{out_dir}/financial_transactions.csv"
        self.txn_ids  = txn_ids

    def generate(self) -> pd.DataFrame:
        n         = self.n
        pay_modes = np.random.choice(
            PAYMENT_MODES, n, p=[0.35, 0.20, 0.15, 0.08, 0.12, 0.07, 0.03]
        )
        amounts = np.random.randint(1_000, 200_000, n)
        amounts_messy = add_messy(
            list(amounts.astype(str)), null_pct=0.02,
            bad_vals=["-100", "0", "abc"], bad_pct=0.01,
        )

        # EMI months: only for EMI payments
        emi_months = [
            str(random.choice([3, 6, 9, 12, 18, 24])) if m == "EMI" else None
            for m in pay_modes
        ]
        # UPI reference VPA: only for UPI payments
        upi_refs = []
        for m in pay_modes:
            if m == "UPI":
                upi_refs.append(rnd_upi() if random.random() > 0.06 else None)
            else:
                upi_refs.append(None)

        df = pd.DataFrame({
            "payment_id"    : [f"PAY{i + 1:08d}" for i in range(n)],
            "txn_id"        : np.random.choice(self.txn_ids, n),
            "payment_date"  : rnd_date(DATE_START, DATE_END, n),
            "payment_mode"  : pay_modes,
            "amount_inr"    : amounts_messy,
            "gst_pct"       : np.random.choice(
                ["18%","12%","28%","5%","18","28%","GST@18"], n
            ),
            "bank_name"     : np.random.choice(BANKS, n),
            "emi_months"    : emi_months,
            "upi_ref"       : upi_refs,
            "invoice_no"    : [
                f"INV/2024-25/{random.randint(10_000, 9_999_999):07d}"
                if random.random() > 0.05 else None
                for _ in range(n)
            ],
            "payment_status": np.random.choice(
                ["Success","Failed","Pending","Refunded","Disputed","success","SUCCESS","failed"],
                n, p=[0.82, 0.05, 0.05, 0.04, 0.02, 0.01, 0.005, 0.005],
            ),
        })

        # Inject ~2 % duplicate rows
        dup_rows = df.sample(int(n * QUALITY["fin_dup_pct"]))
        return pd.concat([df, dup_rows], ignore_index=True)

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)


class ProductReviewGenerator:
    """
    Generates customer product reviews.

    Foreign keys required:
        cust_ids : list[str]
        pid_pool : list[str]

    Messiness: ~1 % of ratings are out-of-range (0, 6, -1),
    ~2 % of ratings are null, mixed verified-purchase encodings.
    """

    def __init__(self, out_dir: str, cust_ids: list, pid_pool: list):
        self.n        = ROW_COUNTS["product_reviews"]
        self.out_path = f"{out_dir}/product_reviews.csv"
        self.cust_ids = cust_ids
        self.pid_pool = pid_pool

    def generate(self) -> pd.DataFrame:
        n = self.n

        ratings = np.random.choice(
            [1, 2, 3, 4, 5], n, p=[0.05, 0.08, 0.15, 0.35, 0.37]
        )

        return pd.DataFrame({
            "review_id"        : [f"REV{i + 1:07d}" for i in range(n)],
            "customer_id"      : np.random.choice(self.cust_ids, n),
            "product_id"       : np.random.choice(self.pid_pool, n),
            "rating"           : add_messy(
                list(ratings.astype(str)),
                null_pct=QUALITY["null_pct_default"],
                bad_vals=["6", "0", "-1"],
                bad_pct=0.01,
            ),
            "review_text"      : np.random.choice(REVIEW_TEXTS, n),
            "review_date"      : rnd_date(DATE_START, DATE_END, n),
            "verified_purchase": np.random.choice(
                ["Yes","No","1","0","Verified Purchase","true"],
                n, p=[0.70, 0.10, 0.08, 0.05, 0.05, 0.02],
            ),
            "helpful_votes"    : np.random.randint(0, 500, n),
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_csv(self.out_path, index=False)
