---
name: query-data
description: How to extract data from files — use query_file or grep_file before downloading. Load this skill before any query_file, grep_file, read_file, or execute_code call. Reload after query failures or before your final extraction step.
---

## Rule #1: Use the Cheapest Tool That Works

| Tool | When to use | Calls saved |
|---|---|---|
| `query_file` | COUNT, GROUP BY, filter, aggregate on CSV/JSON | 2–3 |
| `grep_file` | Find rows by value, check if a column exists | 2–3 |
| `read_file` | Inspect text files, read Wikipedia content | 1–2 |
| `download` + `execute_code` | Multi-file joins, complex pandas transforms | 0 (last resort) |

Do NOT download a file just to run a simple aggregation. `query_file` does it in one call.

---

## Rule #2: Check Column Names First — Every Time

Never assume column names from the question text. Government files use codes. Two equally good ways to check:

- **`peek_file`** (one file) or **`peek_multiple`** (many files at once) — fast if you already have dataset IDs from search. Shows headers and first rows. `peek_multiple` requires `files=[{dataset_id, file_path}, ...]`.
- **`SELECT * FROM t LIMIT 1`** — use via `query_file` when you're already in query mode or need to see actual values alongside column names.

Common name mismatches:

| You might guess | It might actually be |
|---|---|
| `state` | `STFIP`, `ST_FIPS`, `state_code`, `STATE` |
| `county` | `NMCNTY`, `COUNTY`, `CTY_NAME`, `CTYNAME` |
| `year` | `YEAR`, `fiscal_year`, `SURVEY_YEAR` |
| `school_name` | `SCHNAM`, `SCH_NAME`, `INSTNM` |

---

## Common Errors and Fixes

**"Referenced column X not found"**
-> You guessed a column name. Check columns with `peek_file` (or `peek_multiple` for several files) or `SELECT * FROM t LIMIT 1` and rewrite.

**"maximum_object_size exceeded" (~100MB)**
-> File too large for DuckDB. Download it, then use `pd.read_csv(path, usecols=[...])` to load only the columns you need.

**Empty DataFrame after filter**
-> Type mismatch. FIPS codes load as integers (`6`) but are stored as strings (`"06"`). Cast explicitly:
```python
df['STFIP'] = df['STFIP'].astype(str).str.zfill(2)
```

**Encoding errors**
-> Try `encoding='utf-8-sig'`, then `encoding='latin-1'`.

---

## execute_code Checklist

Before submitting any `execute_code` call, verify:

1. Reload the file at the top — state does NOT persist between calls
2. Print `df.columns.tolist()` immediately after loading
3. Print `df.head(2)` before any filtering
4. Always `print()` your final result — silent code produces nothing
5. Cast FIPS codes to `str` before comparing

---

## Handling Truncated Output

`query_file`, `read_file`, and `execute_code` cap output at ~24K characters. If you see a `truncation_note`:

1. **Tighten the query** — add `WHERE`, `GROUP BY`, select fewer columns, use `LIMIT`
2. **Use `grep_file`** to find a specific value instead of reading all rows
3. **Read the full dump** from `local_result_path`:
```python
import json
data = json.load(open('<local_result_path>'))
print(data['columns'])
print(data['rows'][:5])
```
