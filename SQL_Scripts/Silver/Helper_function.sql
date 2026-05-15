-- ============================================================
-- SETUP — Create cleaning schema
-- ============================================================
CREATE SCHEMA IF NOT EXISTS cleaning;

-- ============================================================
-- SHARED HELPER FUNCTIONS
-- ============================================================

-- ── fn_to_boolean ─────────────────────────────────────────
-- Converts all boolean-like strings to TRUE / FALSE / NULL
-- Handles: Yes/No, 1/0, True/False, Active/Inactive,
--          TRUE/FALSE, true/false, Verified Purchase
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_to_boolean(raw_val TEXT)
RETURNS BOOLEAN
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT CASE
        WHEN TRIM(LOWER(raw_val)) IN ('yes','1','true','active','verified purchase') THEN TRUE
        WHEN TRIM(LOWER(raw_val)) IN ('no','0','false','inactive')                  THEN FALSE
        ELSE NULL
    END;
$$;

-- ── fn_clean_phone ────────────────────────────────────────
-- Strips +91 prefix and leading 0 from Indian mobile numbers
-- Returns 10-digit string, or NULL if result is not valid
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_clean_phone(raw_phone TEXT)
RETURNS CHAR(10)
LANGUAGE SQL
IMMUTABLE
AS $$
    SELECT CASE
        WHEN raw_phone IS NULL THEN NULL
        WHEN TRIM(raw_phone) ~ '^\+91[6-9][0-9]{9}$'  THEN SUBSTRING(TRIM(raw_phone), 4, 10)
        WHEN TRIM(raw_phone) ~ '^0[6-9][0-9]{9}$'     THEN SUBSTRING(TRIM(raw_phone), 2, 10)
        WHEN TRIM(raw_phone) ~ '^[6-9][0-9]{9}$'       THEN TRIM(raw_phone)
        ELSE NULL   -- Invalid format — set to NULL
    END;
$$;

-- ── fn_parse_date ─────────────────────────────────────────
-- Parses 6 mixed date formats into a DATE type
-- Handles: YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY,
--          MM/DD/YYYY, YYYY/MM/DD, DD Mon YYYY
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_parse_date(raw_date TEXT)
RETURNS DATE
LANGUAGE PLPGSQL
IMMUTABLE
AS $$
BEGIN
    IF raw_date IS NULL OR TRIM(raw_date) = '' THEN RETURN NULL; END IF;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'YYYY-MM-DD'); EXCEPTION WHEN OTHERS THEN NULL; END;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'DD/MM/YYYY'); EXCEPTION WHEN OTHERS THEN NULL; END;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'DD-MM-YYYY'); EXCEPTION WHEN OTHERS THEN NULL; END;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'MM/DD/YYYY'); EXCEPTION WHEN OTHERS THEN NULL; END;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'YYYY/MM/DD'); EXCEPTION WHEN OTHERS THEN NULL; END;
    BEGIN RETURN TO_DATE(TRIM(raw_date), 'DD Mon YYYY'); EXCEPTION WHEN OTHERS THEN NULL; END;
    RETURN NULL;
END;
$$;

-- ── fn_parse_epoch_or_date ────────────────────────────────
-- Handles snapshot_date in inventory which is sometimes a
-- Unix epoch integer string instead of a date string
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_parse_epoch_or_date(raw_val TEXT)
RETURNS DATE
LANGUAGE PLPGSQL
IMMUTABLE
AS $$
BEGIN
    IF raw_val IS NULL THEN RETURN NULL; END IF;
    -- If it looks like an epoch (all digits, 10 chars)
    IF raw_val ~ '^[0-9]{9,11}$' THEN
        RETURN TO_TIMESTAMP(raw_val::BIGINT)::DATE;
    END IF;
    RETURN cleaning.fn_parse_date(raw_val);
END;
$$;

-- ── fn_parse_gst_pct ──────────────────────────────────────
-- Extracts numeric GST rate from messy strings
-- Handles: "18%", "12%", "28%", "5%", "18", "28%", "GST@18"
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_parse_gst_pct(raw_gst TEXT)
RETURNS NUMERIC(4,1)
LANGUAGE PLPGSQL
IMMUTABLE
AS $$
DECLARE
    cleaned TEXT;
    result  NUMERIC;
BEGIN
    IF raw_gst IS NULL THEN RETURN NULL; END IF;
    cleaned := TRIM(UPPER(raw_gst));
    -- Handle "GST@18" format
    IF cleaned LIKE 'GST@%' THEN cleaned := REPLACE(cleaned, 'GST@', ''); END IF;
    -- Strip % suffix
    cleaned := REPLACE(cleaned, '%', '');
    BEGIN
        result := cleaned::NUMERIC;
        -- Only accept valid Indian GST rates
        IF result IN (5, 12, 18, 28) THEN RETURN result;
        ELSE RETURN NULL;
        END IF;
    EXCEPTION WHEN OTHERS THEN RETURN NULL;
    END;
END;
$$;

-- ── fn_salary_to_annual ───────────────────────────────────
-- Converts mixed salary formats to annual INR amount
-- Handles: "18 LPA" → 1800000
--          "150000" → 1800000 (assumes monthly, × 12)
--          "18L"    → 1800000
--          NULL     → NULL
-- ----------------------------------------------------------
CREATE OR REPLACE FUNCTION cleaning.fn_salary_to_annual(raw_salary TEXT)
RETURNS NUMERIC(12,2)
LANGUAGE PLPGSQL
IMMUTABLE
AS $$
DECLARE
    cleaned TEXT;
    num     NUMERIC;
BEGIN
    IF raw_salary IS NULL OR TRIM(raw_salary) = '' THEN RETURN NULL; END IF;
    cleaned := TRIM(UPPER(raw_salary));

    -- Format: "18 LPA" or "18LPA"
    IF cleaned LIKE '%LPA%' THEN
        num := REGEXP_REPLACE(cleaned, '[^0-9.]', '', 'g')::NUMERIC;
        RETURN ROUND(num * 100000, 2);   -- Convert Lakhs to rupees
    END IF;

    -- Format: "18L" (shorthand Lakhs)
    IF cleaned LIKE '%L' AND cleaned NOT LIKE '%LPA%' THEN
        num := REGEXP_REPLACE(cleaned, '[^0-9.]', '', 'g')::NUMERIC;
        RETURN ROUND(num * 100000, 2);
    END IF;

    -- Format: plain number → assume monthly salary × 12
    IF cleaned ~ '^[0-9]+(\.[0-9]+)?$' THEN
        num := cleaned::NUMERIC;
        -- Heuristic: if > 200000 it is likely already annual, else monthly
        IF num > 200000 THEN RETURN ROUND(num, 2);
        ELSE RETURN ROUND(num * 12, 2);
        END IF;
    END IF;

    RETURN NULL;
END;
$$;
