# Kramabench Local Tools Design

## Problem

Kramabench cannot run cleanly through the existing LakeQA data tools as-is.

The current tools in `strands_evaluation/tools/agent_tools.py` and
`strands_evaluation/tools/agent_tools_v2.py` are S3/data-lake tools. They assume
sources live under:

```text
s3://lakeqa-yc4103-datalake/wikipedia/...
s3://lakeqa-yc4103-datalake/datagov/...
```

Kramabench raw data is local in the cloned benchmark:

```text
other-benchmarks/Kramabench/data/<domain>/input/
```

Examples:

```text
other-benchmarks/Kramabench/data/biomedical/input/1-s2.0-S0092867420301070-mmc1.xlsx
other-benchmarks/Kramabench/data/biomedical/input/1-s2.0-S0092867420301070-mmc7.xlsx
other-benchmarks/Kramabench/data/legal/input/csn-data-book-2024-csv/CSVs/2024_CSN_Top_Three_Identity_Theft_Reports_by_Year.csv
```

The existing tools also cannot distinguish opaque biomedical workbook names like
`mmc1` and `mmc7` unless some catalog exposes sheet names and columns. For
example:

```text
mmc1 -> clinical workbook; columns include idx, Age, Histologic_type, ...
mmc7 -> molecular subtype workbook; sheet "B-APM subtypes"; columns include idx, APP_Z_score, ...
```

So the missing layer is not just file reading. It is a local Kramabench backend
that can search, describe, peek, query, and sandbox-copy Kramabench raw files.

## Decision

Do not modify or break the old LakeQA tools.

Add a separate Kramabench tool package:

```text
strands_evaluation/tools/kramabench/
  __init__.py
  catalog.py
  search_backend.py
  file_backend.py
  agent_tools.py
```

Kramabench runs should expose only Kramabench tools, but those tools should use
the same agent-facing names as the existing tools where possible:

```text
search_value
search_schema
peek_file
read_file
grep_file
query_file
download
execute_code
submit_answer
```

No `list_files` tool for Kramabench. Search should return the files/sheets the
agent needs.

Internally, the package can still have clear backend helper names:

```text
search_kramabench(query, top_k=10, domain=None)
search_kramabench_schema(query, top_k=10, domain=None)
```

The agent-facing decorated tools will call those helpers:

```text
search_value(...)  -> search_kramabench(...)
search_schema(...) -> search_kramabench_schema(...)
```

## Raw Data Root

Default:

```text
other-benchmarks/Kramabench/data
```

Configurable override:

```text
KRAMABENCH_DATA_ROOT=/absolute/path/to/Kramabench/data
```

The backend should resolve paths relative to this root. It should not expose
arbitrary filesystem reads.

## Source References

Search results should return a stable `source_ref` that subsequent Kramabench
tools can consume directly.

Proposed shape:

```json
{
  "source_ref": "kramabench://biomedical/1-s2.0-S0092867420301070-mmc7.xlsx#sheet=B-APM%20subtypes",
  "domain": "biomedical",
  "dataset_id": "biomedical-mmc7",
  "file_path": "1-s2.0-S0092867420301070-mmc7.xlsx",
  "sheet": "B-APM subtypes",
  "local_path": "other-benchmarks/Kramabench/data/biomedical/input/1-s2.0-S0092867420301070-mmc7.xlsx",
  "description": "Biomedical supplemental workbook sheet containing B-APM subtype scores by sample identifier.",
  "columns": ["idx", "APP_Z_score"],
  "score": 12.5
}
```

For non-Excel files, omit `sheet`:

```json
{
  "source_ref": "kramabench://legal/csn-data-book-2024-csv/CSVs/2024_CSN_Top_Three_Identity_Theft_Reports_by_Year.csv",
  "domain": "legal",
  "dataset_id": "legal-2024-csn-top-three-identity-theft-reports-by-year",
  "file_path": "csn-data-book-2024-csv/CSVs/2024_CSN_Top_Three_Identity_Theft_Reports_by_Year.csv",
  "description": "FTC Consumer Sentinel Network table of top identity-theft report categories by year.",
  "columns": ["Theft Type", "Year", "# of Reports"]
}
```

Tools should accept `source_ref` first. For compatibility, they can also accept
`dataset_id`, `file_path`, and optional `sheet`.

## Catalog

Create a generated local catalog:

```text
other-benchmarks/data-imports/kramabench/catalog.jsonl
```

Build command:

```text
python -m strands_evaluation.tools.kramabench.catalog \
  --root other-benchmarks/Kramabench/data \
  --output other-benchmarks/data-imports/kramabench/catalog.jsonl
```

The catalog should be generated only from raw files and non-answer metadata.
Do not read `solutions/` or task answers while building search metadata.

Each catalog row represents one searchable source unit:

- CSV/JSON/TXT/HTML/GPKG/NPZ/CDF/etc.: one row per file.
- Excel: one row per sheet, because sheet names and columns are essential for
  retrieval.
- Globs: not a catalog row by themselves. Search returns concrete files/sheets;
  task promotion can still use globs in provenance if needed.

Catalog fields:

```json
{
  "source_ref": "...",
  "domain": "biomedical",
  "dataset_id": "biomedical-mmc7",
  "file_path": "1-s2.0-S0092867420301070-mmc7.xlsx",
  "sheet": "B-APM subtypes",
  "family": "xlsx",
  "columns": ["idx", "APP_Z_score"],
  "sheet_names": ["README", "B-APM subtypes"],
  "row_count_sample": 20,
  "description": "Non-leaky description based on filename, sheet names, and columns.",
  "search_text": "biomedical mmc7 B-APM subtypes idx APP_Z_score molecular subtype score sample identifier"
}
```

## Catalog Builders

Implement format-specific inspectors in `catalog.py`:

```text
inspect_csv(path)       -> delimiter, columns, preview rows
inspect_xlsx(path)      -> one catalog row per sheet with sheet name and columns
inspect_json(path)      -> top-level keys / first-object keys
inspect_html(path)      -> table count and table headers
inspect_text(path)      -> first lines and lightweight token summary
inspect_binary(path)    -> family, size, filename-derived metadata
```

Minimum viable support:

- `.csv`
- `.xlsx`
- `.txt`
- `.html`
- `.json`

Nice-to-have later:

- `.gpkg` layer names, if `geopandas` is installed
- `.npz` array names
- `.cdf` variable names
- `.sp3`, `.tle`, `.dat`, `.lst` text previews

## Search Implementation

Use a deterministic local lexical ranker first. No embeddings are required for
the first implementation.

Normalize query and catalog text:

```text
lowercase
split on non-alphanumeric characters
preserve useful original tokens like APP_Z_score by also adding app, z, score, app_z_score
```

`search_kramabench` should search broad source metadata:

```text
description
filename
domain
sheet name
columns
preview tokens
```

`search_kramabench_schema` should weight schema fields heavily:

```text
columns
sheet name
file stem
domain
description
```

Initial scoring:

```text
score = 0
+ 10 for exact normalized column match
+ 8  for exact sheet-name match
+ 5  for filename/stem token match
+ 3  for description token match
+ 2  for domain match
+ 1  for preview/search_text token match
```

The schema search can multiply column/sheet matches by 2.

This is enough for:

```text
query: "lowest APP-Z score"
top hit: kramabench://biomedical/...mmc7.xlsx#sheet=B-APM%20subtypes
because columns include APP_Z_score
```

And:

```text
query: "age for patient identifier idx"
top hit: kramabench://biomedical/...mmc1.xlsx
because columns include Age and idx
```

## Agent-Facing Search Tools

In `strands_evaluation/tools/kramabench/agent_tools.py`:

```python
@tool
def search_value(query: str, top_k: int = 10, domain: str | None = None) -> dict:
    """Search Kramabench local source descriptions and previews."""

@tool
def search_schema(query: str, top_k: int = 10, domain: str | None = None) -> dict:
    """Search Kramabench local source schemas: columns, sheet names, and file metadata."""
```

Return shape:

```json
{
  "results": [
    {
      "source_ref": "...",
      "dataset_id": "biomedical-mmc7",
      "domain": "biomedical",
      "file_path": "1-s2.0-S0092867420301070-mmc7.xlsx",
      "sheet": "B-APM subtypes",
      "family": "xlsx",
      "description": "...",
      "columns": ["idx", "APP_Z_score"],
      "score": 12.5
    }
  ],
  "count": 1,
  "query": "lowest APP-Z score"
}
```

## File Tools

### `peek_file`

```python
@tool
def peek_file(
    source_ref: str | None = None,
    dataset_id: str | None = None,
    file_path: str | None = None,
    sheet: str | None = None,
    max_rows: int = 20,
) -> dict:
    ...
```

Behavior:

- CSV: return delimiter, columns, first rows.
- XLSX without sheet: return sheet names and per-sheet column preview.
- XLSX with sheet: return columns and first rows for that sheet.
- HTML: return table count and headers.
- Text-like files: return first lines.
- Binary/science files: return family, size, and metadata if available.

### `query_file`

```python
@tool
def query_file(
    source_ref: str | None = None,
    dataset_id: str | None = None,
    file_path: str | None = None,
    sheet: str | None = None,
    sql: str = "",
) -> dict:
    ...
```

Behavior:

- Load one source into a pandas DataFrame.
- Register it in DuckDB as table `t`.
- Execute SQL and return capped rows.
- For Excel, `sheet` is required unless the `source_ref` already includes a
  sheet fragment.

This makes the biomedical example executable without downloading:

```sql
SELECT idx
FROM t
ORDER BY APP_Z_score ASC
LIMIT 1
```

### `read_file`

Only for text-like files:

```python
@tool
def read_file(source_ref=None, dataset_id=None, file_path=None, start_line=0, max_lines=1000) -> dict:
    ...
```

For `.xlsx`, return a helpful error:

```text
Excel files are not line-readable. Use peek_file to inspect sheets or query_file with a sheet name.
```

### `grep_file`

For text-like files and CSV lines. Not for Excel unless we later add a sheet
search mode.

### `download`

Copies local raw files into the normal sandbox.

```python
@tool
def download(files: list[dict]) -> dict:
    ...
```

Accepted entries:

```json
{"source_ref": "kramabench://biomedical/...mmc7.xlsx#sheet=B-APM%20subtypes"}
{"dataset_id": "biomedical-mmc7", "file_path": "1-s2.0-S0092867420301070-mmc7.xlsx"}
```

The copied file path should look like:

```text
.sandbox/task_xxx/biomedical-mmc7/1-s2.0-S0092867420301070-mmc7.xlsx
```

### `execute_code`

Use the existing sandboxed `execute_code` implementation after Kramabench
`download` has copied files into the sandbox.

Do not expose arbitrary raw repo paths to the model by default. The fair loop is:

```text
search -> peek/query, or search -> download -> execute_code on downloaded files
```

This keeps retrieval meaningful. If the model could directly use
`other-benchmarks/Kramabench/data/...`, search would become optional and unfair.

## Agent Integration

Later, update `agent_with_mode.py` with an explicit Kramabench mode.

Do not globally alter the existing tool imports. Instead:

```python
from strands_evaluation.tools import kramabench as kramabench_tools
```

Add a search mode:

```text
search_tool_mode = "kramabench"
```

When active:

```text
search tools:
  kramabench_tools.search_value
  kramabench_tools.search_schema

data tools:
  kramabench_tools.peek_file
  kramabench_tools.read_file
  kramabench_tools.grep_file
  kramabench_tools.query_file
  kramabench_tools.download
  kramabench_tools.execute_code
  submit_answer
```

Do not expose:

```text
search_prefix
list_files
normal S3 peek/read/query/download tools
```

Implementation detail: the current `_MODES` set is shared across search,
planning, and management modes. Kramabench should not become a management mode.
Prefer splitting search mode validation from management mode validation:

```text
_SEARCH_TOOL_MODES = {"naive", "standard", "ideal", "preloaded", "kramabench"}
_MANAGEMENT_MODES = {"naive", "standard", "ideal", "preloaded"}
```

Then `build_search("kramabench")` can return the Kramabench search tools, and
`build_mode_bundle` can replace the data tools with Kramabench data tools.

## Ideal Mode

Keep `search_ideal` as-is for now.

Ideal mode already reads `source_sequence` from the relevant plan file. The only
Kramabench-specific requirement is that the returned planned source must be
readable by the active Kramabench file tools.

So if a plan contains:

```text
kramabench://biomedical/1-s2.0-S0092867420301070-mmc7.xlsx#sheet=B-APM%20subtypes
```

then `peek_file`, `query_file`, and `download` from the Kramabench package must
accept that `source_ref`.

## Task Promotion Implication

The promoted Kramabench tasks should eventually point at source refs that are
retrieval- and execution-friendly.

Current rough source:

```text
kramabench/biomedical-mmc7/files/1-s2.0-S0092867420301070-mmc7.xlsx
```

Preferred source:

```text
kramabench://biomedical/1-s2.0-S0092867420301070-mmc7.xlsx#sheet=B-APM%20subtypes
```

This makes the first hop unambiguous:

```text
Question: Which patient identifier has the lowest APP-Z score?
Search schema query: lowest APP-Z score
Hit: mmc7 sheet B-APM subtypes, columns idx and APP_Z_score
Query: SELECT idx FROM t ORDER BY APP_Z_score ASC LIMIT 1
```

Second hop:

```text
Question: What is the age of S019?
Search schema query: patient identifier idx age clinical
Hit: mmc1 clinical workbook, columns idx and Age
Query: SELECT Age FROM t WHERE idx = 'S019'
```

## Test Plan

Unit tests:

1. Catalog builder emits one row per Excel sheet.
2. Catalog for `mmc7` includes sheet `B-APM subtypes` and column `APP_Z_score`.
3. Catalog for `mmc1` includes columns `idx` and `Age`.
4. `search_schema("lowest APP-Z score", domain="biomedical")` returns mmc7 above mmc1.
5. `search_schema("patient age idx", domain="biomedical")` returns mmc1 above mmc7.
6. `peek_file` on an Excel source without sheet returns sheet names.
7. `query_file` on mmc7 sheet `B-APM subtypes` can return `S019`.
8. `query_file` on mmc1 can return age `60` for `S019`.
9. `download` copies a raw Kramabench file into the sandbox and `execute_code` can read it.
10. Normal datagov/wikipedia tools still import and behave unchanged.

Integration tests:

1. Run the five promoted Kramabench sample tasks with `search_tool_mode=kramabench`.
2. Confirm only Kramabench search/data tools are exposed.
3. Confirm no old S3 `list_files`, `search_prefix`, or datagov/wikipedia tools are present.
4. Confirm the biomedical hard-3 path works through:

```text
search_schema -> query_file -> search_schema -> query_file -> submit_answer
```

## Open Questions

1. Should `source_ref` use URI form (`kramabench://...`) or slash form
   (`kramabench/<domain>/...`) inside task JSON?
2. Should Kramabench mode be selected explicitly by CLI flag, inferred from the
   task root, or both?
3. Should `download` copy an entire glob result set, or should glob expansion
   happen only after search has returned concrete file refs?

Recommended defaults:

1. Use `kramabench://...#sheet=...` internally and allow slash-form aliases.
2. Support explicit `--search_tool kramabench` first; add auto-detect later.
3. Keep search concrete and make `download` accept concrete source refs first.
