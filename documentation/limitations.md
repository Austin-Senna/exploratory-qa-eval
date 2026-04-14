# Limitations

## Schema ↔ Description matching (`hybrid_search/process.py`)

The hybrid index joins `table_descriptions.jsonl` (or `.parquet`) with
`datagov_table_schemas_full.jsonl` using an exact **file-level stem** key:

- description side (`_uri_to_stem` in `hybrid_search/process.py`): strip
  `s3://<bucket>/` and the file extension.
- schema side (`load_table_schemas` in `s3_loader/parquet_cache.py`): strip
  `/v1/` from `s3_key` and the file extension.

Both sides normalize to e.g. `datagov/<slug>/files/<name>`.

### Match rate on the current 10k-row descriptions file

| Category | Count | Notes |
|---|---|---|
| Matched | 5,999 (60.0%) | |
| `wikipedia/...` descriptions | 331 | schemas file is datagov-only, expected |
| datagov dataset absent from schemas file | 3,021 | upstream extraction gap, not a matcher issue |
| datagov dataset present but different filename | 649 (~6.5%) | **design gap** |

### The 649-row gap

These rows have a description for one file (e.g. `.../files/data.txt`) while
the schemas file only catalogs a sibling file for the same dataset
(e.g. `.../files/rows.csv`). Because the matcher keys on the full filename
stem, the schema is never attached even though a usable one exists for the
same `datagov/<slug>`.

Examples:

- desc `.../2021-state-expenditures/files/data.txt` → schema only has `.../files/rows.csv`
- desc `.../2016-property-tax-roll/files/columns.txt` → schema only has `.../files/rows.csv`
- desc `.../postsecondary-school-locations-current-5a74c/files/nces::postsecondary-school-locations-current-1.txt`
  → schema only has `.../files/Postsecondary_School_Locations_Current_<id>.csv`

### Possible fallback (not implemented)

If schemas are meant as dataset-level context rather than strictly the
same-file schema, add a secondary lookup keyed on `datagov/<slug>` when the
file-stem lookup misses. This would recover roughly 6.5% of rows, at the
cost of occasionally attaching a sibling file's columns.
