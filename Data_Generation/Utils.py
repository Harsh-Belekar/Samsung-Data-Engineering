"""
Utils.py
========
Shared helper functions used by every generator module.

Functions
---------
rnd_phone()         — Generate a realistic Indian mobile number
rnd_upi()           — Generate a UPI VPA string
rnd_gstin()         — Generate a plausible (but fake) GSTIN
rnd_date()          — Vectorised random-date generator with optional messy formats
add_messy()         — Inject nulls and bad values into a list
mess_case()         — Randomly alter string casing to simulate ingestion errors
"""

import random
import string
from datetime import datetime, timedelta
import numpy as np


# =====================================================================
# PHONE / UPI / GSTIN helpers
# =====================================================================

def rnd_phone() -> str:
    """
    Return a 10-digit Indian mobile number.
    Valid Indian numbers start with 6, 7, 8, or 9.
    """
    prefix = random.choice(["6", "7", "8", "9"])
    digits = "".join(str(random.randint(0, 9)) for _ in range(9))
    return prefix + digits


def rnd_upi() -> str:
    """
    Return a UPI Virtual Payment Address (VPA) in the form
    <name><digits>@<bank_handle>.
    Example: 'priya42@okhdfc'
    """
    from Master_data import FIRST_NAMES
    bank_handles = ["okaxis", "okhdfcbank", "oksbi", "okicici",
                    "ybl", "paytm", "apl", "upi"]
    name = random.choice(FIRST_NAMES).lower()
    return f"{name}{random.randint(1, 999)}@{random.choice(bank_handles)}"


def rnd_gstin() -> str:
    """
    Return a plausible (but fictitious) 15-character GSTIN.
    Format: <state_code(2)><PAN_alpha(5)><entity(4)><checksum(4)>
    """
    state_codes = [
        "01","02","03","04","06","07","08","09","10",
        "11","12","13","14","15","16","17","18","19","20",
        "21","22","24","25","27","28","29","30","32","33","34","36",
    ]
    alpha = string.ascii_uppercase
    return (
        f"{random.choice(state_codes)}"
        f"{''.join(random.choices(alpha, k=5))}"
        f"{random.randint(1000, 9999)}"
        f"{random.choice(alpha)}"
        f"{random.randint(1, 9)}"
        f"{random.choice(alpha)}"
        f"{random.randint(1, 9)}"
    )


# =====================================================================
# DATE helpers 
# =====================================================================

def rnd_date(
    start: datetime,
    end: datetime,
    n: int,
    fmt_variants: list[str] | None = None,
) -> list[str]:
    """
    Generate *n* random dates between *start* and *end* (inclusive).

    Parameters
    ----------
    start        : Start of the date range.
    end          : End of the date range.
    n            : Number of dates to generate.
    fmt_variants : If provided, each date is formatted using a
                    randomly chosen format from this list — useful
                    for simulating mixed-format ingestion issues.
                    If None, all dates use ISO-8601 ("%Y-%m-%d").

    Returns
    -------
    List of date strings.
    """
    delta = (end - start).days
    day_offsets = np.random.randint(0, delta + 1, n)
    dates = [start + timedelta(days=int(d)) for d in day_offsets]

    if fmt_variants:
        formats = np.random.choice(fmt_variants, n)
        return [d.strftime(f) for d, f in zip(dates, formats)]

    return [d.strftime("%Y-%m-%d") for d in dates]


# =====================================================================
# DATA-QUALITY helpers
# =====================================================================

def add_messy(
    arr: list,
    null_pct: float = 0.03,
    bad_vals: list | None = None,
    bad_pct: float = 0.02,
) -> list:
    """
    Inject realistic data-quality issues into a list.

    Parameters
    ----------
    arr      : Input list (will be copied — original not mutated).
    null_pct : Fraction of elements to replace with None.
    bad_vals : Optional list of "bad" strings to inject (e.g. "N/A", "?").
    bad_pct  : Fraction of elements to replace with a random bad_val.

    Returns
    -------
    New list with nulls and/or bad values injected.
    """
    result = list(arr)
    n = len(result)

    # Inject nulls
    null_indices = np.random.choice(n, max(1, int(n * null_pct)), replace=False)
    for i in null_indices:
        result[i] = None

    # Inject bad values (if any supplied)
    if bad_vals:
        bad_indices = np.random.choice(n, max(1, int(n * bad_pct)), replace=False)
        for i in bad_indices:
            result[i] = random.choice(bad_vals)

    return result


def mess_case(names: list[str], mess_pct: float = 0.10) -> list[str]:
    """
    Randomly alter string casing to simulate upstream ingestion errors.

    Approximately *mess_pct / 2* of entries become UPPERCASE and
    the same fraction become lowercase; the rest stay Title Case.

    Parameters
    ----------
    names    : List of name strings.
    mess_pct : Total fraction of entries to alter.

    Returns
    -------
    New list with some entries' casing changed.
    """
    result = []
    half = mess_pct / 2
    for name in names:
        r = random.random()
        if r < half:
            result.append(name.upper())
        elif r < mess_pct:
            result.append(name.lower())
        else:
            result.append(name)
    return result
