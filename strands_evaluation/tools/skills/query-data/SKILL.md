---
name: query-data
description: How to extract data from files — use query_file or grep_file before downloading to save tool calls
---

## Tool Cost Ladder — Use the Cheapest That Works

| Tool | Use when | Tool calls saved |
|------|----------|-----------------|
| `query_file` | COUNT, GROUP BY, filter, aggregate on CSV/JSON | saves 2-3 vs download+execute |
| `grep_file` | find rows with a value, check column names exist | saves 2-3 vs download+execute |
| `read_file` | inspect text files, read Wikipedia content.txt | saves 1-2 vs download |
| `download + execute_code` | joins across files, complex multi-step pandas | required |

**Wrong (3+ tool calls):** download → execute_code → pd.read_csv → df.groupby()
**Right (1 tool call):** `query_file("SELECT NMCNTY, COUNT(*) FROM t WHERE STFIP='06' GROUP BY NMCNTY ORDER BY 2 DESC LIMIT 5")`

Only use `execute_code` when genuinely required: multi-file joins, complex transforms, iterative analysis.

---

## Before Writing Any Code — Verify Column Names

**Always check column names before writing any query or pandas code.** The most common failure is referencing a column that does not exist.

```sql
-- Run this first, every time:
SELECT * FROM t LIMIT 1
```

Or use `peek_file` for a quick header preview. Never assume column names from the question text — files use government codes.

**Common column name gotchas:**

| What you might guess | What it might actually be |
|---|---|
| `state` | `STFIP`, `ST_FIPS`, `state_code`, `STATE`, `st` |
| `county` | `NMCNTY`, `COUNTY`, `county_name`, `CTY_NAME`, `CTYNAME` |
| `year` | `YEAR`, `fiscal_year`, `report_year`, `YEAR_REPORTED`, `SURVEY_YEAR` |
| `count` / `value` | varies widely — always check |
| `school_name` | `SCHNAM`, `SCH_NAME`, `NAME`, `INSTNM` |

---

## Common Errors and Fixes

**"Referenced column X not found" / Binder Error**
→ Column name is wrong. Run `SELECT * FROM t LIMIT 1` to see the actual names, then rewrite.

**"maximum_object_size exceeded" (~100MB limit)**
→ File too large for direct DuckDB query. Use `download` + `execute_code` with column selection:
```python
import pandas as pd
df = pd.read_csv("/path/to/file.csv", usecols=["col1", "col2"])
```
Or add a `WHERE` clause to filter rows before the size limit is hit.

**`KeyError: 'COLUMN_NAME'` in execute_code**
→ Column name mismatch between peek preview and the actual downloaded file. Always print column names at the top of every execute_code block:
```python
print(df.columns.tolist())
```

**UTF-8 BOM or encoding error in execute_code**
→ File has a BOM marker. Use:
```python
df = pd.read_csv(filepath, encoding='utf-8-sig')
# or if that fails:
df = pd.read_csv(filepath, encoding='latin-1')
```

**Empty DataFrame after filter or merge**
→ Type mismatch. FIPS codes are often stored as strings (`"06"`) but may load as integers (`6`). Cast explicitly:
```python
df['STFIP'] = df['STFIP'].astype(str).str.zfill(2)
```

---

## execute_code Checklist

Before submitting execute_code, verify:
- [ ] Reload the file at the top — state does NOT persist between calls
- [ ] Print `df.columns.tolist()` to confirm column names
- [ ] Print `df.head(2)` before any filtering to confirm data loaded correctly
- [ ] Always `print()` the final result — silent code produces nothing
- [ ] Cast FIPS codes to `str` if comparing to string values (`"06"` not `6`)
- [ ] If joining two files, print `df1.dtypes` and `df2.dtypes` first to catch type mismatches

---

## Output Limits — query_file, read_file, execute_code

These tools cap output at ~24,000 characters (~6k tokens). If a result is too large you will get:
- `truncation_note` describing how many rows/lines fit within the limit
- `local_result_path` — path to the full result dumped in the sandbox

**Recovery options (in order of preference):**
1. Rewrite the query to return less: add `WHERE`, `GROUP BY`, select specific columns, use `LIMIT`
2. Use `grep_file` to find a specific value instead of reading all rows
3. Access the dump directly:
   ```python
   import json
   data = json.load(open('<local_result_path>'))
   rows = data['rows']    # list of lists
   cols = data['columns'] # column names
   print(cols)
   print(rows[:5])
   ```

execute_code stdout is also capped. If truncated, print a summary (`df.describe()`, `df.head()`) instead of the full dataframe.

---

## query_file Examples

```sql
-- Check column names before writing real query
SELECT * FROM t LIMIT 1

-- Count by group, top 5
SELECT NMCNTY, COUNT(*) as cnt FROM t WHERE STFIP='53' GROUP BY NMCNTY ORDER BY cnt DESC LIMIT 5

-- Filter and aggregate
SELECT SUM(beneficiaries) FROM t WHERE year=2020 AND state='CA'

-- Check distinct values
SELECT DISTINCT year FROM t ORDER BY year
```
