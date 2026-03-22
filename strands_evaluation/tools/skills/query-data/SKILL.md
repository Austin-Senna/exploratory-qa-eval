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
