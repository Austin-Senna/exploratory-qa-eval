# Data Lake Skills Reference

## Data Lake Organization

The data lake contains two major corpus segments:

**wikipedia/** — Wikipedia article dumps as structured documents.
- Useful for background knowledge, entity descriptions, and contextual lookups.
- Not directly queryable as tabular data; use as reference only.

**datagov/** — Public government datasets from data.gov.
- Primary source for answering factual questions about government data.
- Datasets are organized as: `datagov/{dataset-slug}/files/{filename}`
- Common subdirectories: `files/`, `resources/`, `data/`

## Common Dataset Naming Patterns (Data.gov)

Government datasets on data.gov follow predictable naming patterns:
- **[Topic]-[geography]-[year]**: e.g., `unemployment-county-2019`
- **[Agency abbreviation]-[topic]**: e.g., `va-disability-compensation`, `hud-fair-market-rents`
- **[Program name]-data**: e.g., `snap-participation-data`, `medicare-enrollment`
- Underscores and hyphens are interchangeable; try both
- Year suffixes vary: `_2020`, `-2020`, `2020`, `fy2020`

## Key Government Agencies and Their Topic Areas

- **VA** (Veterans Affairs): disability compensation, benefits, healthcare
- **HUD** (Housing): fair market rents, housing assistance, homelessness
- **BLS** (Bureau of Labor Statistics): employment, wages, CPI, industry
- **CDC / NCHS**: health statistics, mortality, disease surveillance
- **Census Bureau**: population, demographics, ACS, decennial
- **FEMA**: disaster declarations, flood maps, emergency management
- **DOE / EIA**: energy consumption, electricity, fuel prices
- **EPA**: emissions, air quality, water quality, Superfund
- **USDA / NASS**: agriculture, crop production, farm statistics
- **FEC**: campaign finance, political donations
- **IRS / Treasury**: tax statistics, SOI data

## Metadata Fields Available in Search Index

Each dataset document in the search index may contain:
- Dataset title and description
- Publisher / agency name
- Geographic coverage (national, state, county, city)
- Time period / year range
- File formats available (CSV, JSON, XML, Parquet)
- Column names and schema hints (where pre-indexed)

## Search Strategies

### When to use specific query types:
- **Exact dataset name lookup**: Use the full or partial official dataset name
  - e.g., `search_sparse("Veteran Population Projection Model")`
- **Topic + geography**: Combine subject with geographic scope
  - e.g., `search_sparse("housing cost burden county level")`
- **Agency + topic**: Use the publishing agency acronym
  - e.g., `search_sparse("CDC mortality statistics state")`
- **Year-specific data**: Include the year in the query
  - e.g., `search_sparse("SNAP participation 2021 monthly")`

### Query reformulation ladder (from specific to broad):
1. Official dataset name or program name
2. Topic + geography + year
3. Agency acronym + topic
4. Broad topic only
5. Related concept or synonym

### What metadata fields exist (to guide column-level search):
- After finding a dataset, use `list_files` to see available files
- Use `peek_file` to preview column names without downloading
- Use `query_file` for SQL-like filtering on large files
- Only `download` + `execute_code` when you need full computation

## Notes
- Dataset slugs in search results are path components, not full S3 URIs
- The S3 prefix `s3://lakeqa-yc4103-datalake/` is prepended at download time
- File sizes vary widely; always peek before downloading large files
