"""
Generators/Employees_Inventory.py
===================================
Generates two XLSX tables:
    1. employees.xlsx   — 15,000 rows (configurable)
    2. inventory.xlsx   — 100,000 rows (configurable)

Messiness injected
------------------
Employees  : salary stored in mixed formats (LPA, monthly, "15L"),
                mixed department casing, null PF numbers, various
                is_active encodings.
Inventory  : negative qty_available values, epoch timestamps mixed
                with ISO dates, null warehouse IDs.
"""

import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from Config      import ROW_COUNTS, DATE_START, DATE_END, DATE_FORMATS, QUALITY
from Master_data import (
    FIRST_NAMES, LAST_NAMES, DEPARTMENTS, DESIGNATIONS, LOCATIONS_OFFICE,
)
from Utils import rnd_date, add_messy


class EmployeeGenerator:
    """
    Generates the employee HR master table.

    Salary is deliberately stored in three different formats to
    simulate a realistic data-cleaning challenge:
        - "18 LPA"       (annual CTC in Lakhs Per Annum)
        - "150000"       (monthly gross as plain integer string)
        - "18L"          (shorthand LPA)
        - None           (~5 % of rows)
    """

    def __init__(self, out_dir: str):
        self.n        = ROW_COUNTS["employees"]
        self.out_path = f"{out_dir}/employees.xlsx"

    def generate(self) -> pd.DataFrame:
        n = self.n

        fn = np.random.choice(FIRST_NAMES, n)
        ln = np.random.choice(LAST_NAMES,  n)

        depts  = np.random.choice(DEPARTMENTS,       n)
        desigs = np.random.choice(DESIGNATIONS,      n)
        locs   = np.random.choice(LOCATIONS_OFFICE,  n)

        # Salary: mix of annual-LPA strings, monthly-rupee strings, shorthand
        salaries = []
        for _ in range(n):
            r    = random.random()
            base = random.randint(3, 80)   # LPA value
            if r < 0.70:
                salaries.append(f"{base} LPA")
            elif r < 0.88:
                salaries.append(str(int(base * 100_000 / 12)))   # monthly gross
            elif r < 0.95:
                salaries.append(f"{base}L")
            else:
                salaries.append(None)

        # Manager IDs sample from the first 2,000 employees (realistic hierarchy)
        mgr_pool = [f"EMP{i + 1:06d}" for i in range(min(2000, n))]
        managers = [
            random.choice(mgr_pool) if random.random() > 0.08 else None
            for _ in range(n)
        ]

        # PF numbers in Maharashtra format; ~6 % null
        pf_numbers = [
            f"MH/{random.randint(10000, 99999)}/{random.randint(100, 999)}"
            if random.random() > 0.06 else None
            for _ in range(n)
        ]

        return pd.DataFrame({
            "employee_id" : [f"EMP{i + 1:06d}" for i in range(n)],
            "full_name"   : [f"{f} {l}" for f, l in zip(fn, ln)],
            "department"  : add_messy(
                [d if random.random() > 0.05 else d.upper() for d in depts],
                null_pct=QUALITY["null_pct_default"],
            ),
            "designation" : desigs,
            "location"    : locs,
            "join_date"   : rnd_date(
                datetime(2010, 1, 1), datetime(2024, 12, 31), n, DATE_FORMATS
            ),
            "salary_inr"  : salaries,
            "manager_id"  : managers,
            "gender"      : np.random.choice(
                ["Male", "Female", "Other", "M", "F"],
                n, p=[0.55, 0.38, 0.03, 0.02, 0.02],
            ),
            "pf_number"   : pf_numbers,
            "is_active"   : np.random.choice(
                ["Active", "Inactive", "1", "0", "Yes"],
                n, p=[0.82, 0.08, 0.05, 0.03, 0.02],
            ),
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_excel(self.out_path, index=False, engine="openpyxl")


class InventoryGenerator:
    """
    Generates the inventory snapshot table.

    Foreign keys required from upstream generators:
        pid_pool : list[str]   — product IDs from ProductGenerator
        wh_ids   : list[str]   — warehouse IDs from WarehouseGenerator

    Messiness: some qty_available values are negative (over-allocation
    bug simulation), ~5 % of snapshot_date values are Unix epoch
    timestamps instead of ISO date strings.
    """

    def __init__(self, out_dir: str, pid_pool: list, wh_ids: list):
        self.n        = ROW_COUNTS["inventory"]
        self.out_path = f"{out_dir}/inventory.xlsx"
        self.pid_pool = pid_pool
        self.wh_ids   = wh_ids

    def generate(self) -> pd.DataFrame:
        n = self.n

        # qty_available: allow some negatives to simulate over-allocation
        qty_available = np.random.randint(-50, 5000, n)
        qty_reserved  = np.random.randint(0,   500,  n)
        reorder_level = np.random.randint(10,  300,  n)

        # snapshot_date: ~5 % stored as Unix epoch integers (messy)
        snap_dates = []
        for d in rnd_date(DATE_START, DATE_END, n):
            if random.random() < 0.05:
                dt = datetime.strptime(d, "%Y-%m-%d")
                snap_dates.append(str(int(dt.timestamp())))   # epoch string
            else:
                snap_dates.append(d)

        return pd.DataFrame({
            "inventory_id"  : [f"INV{i + 1:07d}" for i in range(n)],
            "product_id"    : np.random.choice(self.pid_pool, n),
            "warehouse_id"  : add_messy(
                list(np.random.choice(self.wh_ids, n)),
                null_pct=QUALITY["null_pct_default"],
            ),
            "qty_available" : add_messy(
                list(qty_available.astype(str)),
                null_pct=QUALITY["null_pct_default"],
            ),
            "qty_reserved"  : qty_reserved.astype(str),
            "reorder_level" : reorder_level.astype(str),
            "last_restocked": rnd_date(DATE_START, DATE_END, n),
            "snapshot_date" : snap_dates,
        })

    def save(self, df: pd.DataFrame) -> None:
        df.to_excel(self.out_path, index=False, engine="openpyxl")
