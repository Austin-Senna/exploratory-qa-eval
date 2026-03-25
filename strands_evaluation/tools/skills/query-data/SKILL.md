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

## Output Limits — query_file, read_file, execute_code

These tools cap output at ~16,000 characters. If a result is too large you will get:
- `truncation_note` describing how many rows/lines fit within the limit
- `local_result_path` — path to the full result dumped in the sandbox
- As many rows/lines as fit within the 16k limit

**Recovery options (in order of preference):**
1. Rewrite the query to return less: add `WHERE`, `GROUP BY`, select specific columns, use `LIMIT`
2. Use `grep_file` to find a specific value instead of reading all rows
3. Access the dump directly:
   ```python
   execute_code("""
   import json
   data = json.load(open('<local_result_path>'))
   rows = data['rows']          # list of lists
   cols = data['columns']       # column names
   print(cols)
   print(rows[:5])
   """)
   ```

execute_code stdout is also capped. If truncated, print a summary (`df.describe()`, `df.head()`) instead of the full dataframe.

---

## Context Management — summarize_context

If you have made many tool calls and the conversation is getting long, call `summarize_context` before large queries:
```
summarize_context(
  summary="Found dataset X (id: ...). Column Y contains the target values. Computed Z=42 for sub-task 1. Still need: sub-task 2.",
  drop_messages=16
)
```
- Write your findings thoroughly — this replaces the dropped messages as your memory
- Your summary is anchored permanently and won't be truncated
- Use `drop_messages=10` for light cleanup, `20+` for heavy cleanup

---

## Before Writing Code — Verify Column Names

Never assume column names. Always check first:
```
query_file(dataset_id, file_path, "SELECT * FROM t LIMIT 1")
```
or `peek_file` for a quick header preview. Common gotchas:
- `STFIP` vs `ST_FIPS` vs `state_code` vs `FIPS`
- `NMCNTY` vs `county_name` vs `COUNTY`
- String `"06"` vs integer `6` for FIPS codes — mismatches cause silent empty results

---

## query_file Examples

```sql
-- Count by group, top 5
SELECT NMCNTY, COUNT(*) as cnt FROM t WHERE STFIP='53' GROUP BY NMCNTY ORDER BY cnt DESC LIMIT 5

-- Filter and aggregate
SELECT SUM(beneficiaries) FROM t WHERE year=2020 AND state='CA'

-- Check distinct values
SELECT DISTINCT year FROM t ORDER BY year
```

---

## execute_code Rules

- State does NOT persist between calls — always reload files at the top of every block
- Always `print()` to see output — silent code produces nothing
- If a DataFrame is empty after a join, key types likely mismatched — print dtypes and sample values first
- Never download all files from a large dataset; filter to the specific state/year needed
