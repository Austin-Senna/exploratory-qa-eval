# Combined Turn-Waste Global Report

Grouped root: `results_semantic_turn_waste_grouped`
Combined CSV: `combined_turn_waste_global_failures.csv`
Total grouped failure rows: 98

## Counts by Model

| Model | Errors |
| --- | --- |
| openai_gpt-5-mini | 49 |
| openai_gpt-5.4-nano | 49 |

## Counts by Global Group

| Global Group | Errors | Errors by Model |
| --- | --- | --- |
| Structured Data Extraction Loop | 19 | openai_gpt-5-mini: 19 |
| Redundant Intermediate Re-querying | 17 | openai_gpt-5.4-nano: 17 |
| Source and Query-Shape Churn | 17 | openai_gpt-5.4-nano: 17 |
| Candidate Overconfirmation | 8 | openai_gpt-5.4-nano: 8 |
| Redundant Revalidation After Progress | 8 | openai_gpt-5-mini: 8 |
| Missing Source Search Loop | 7 | openai_gpt-5-mini: 7 |
| Wrong-Branch Or Off-Path Drift | 6 | openai_gpt-5-mini: 6 |
| Post-Answer Or Source Non-Submission | 5 | openai_gpt-5-mini: 5 |
| Downstream Deferral and Chain Crowd-Out | 4 | openai_gpt-5.4-nano: 4 |
| Partial Component Stall | 4 | openai_gpt-5-mini: 4 |
| Post-Answer Verification Churn | 3 | openai_gpt-5.4-nano: 3 |

## Counts by Global Group and Subtype

| Global Group | Subtype | Errors | Errors by Model |
| --- | --- | --- | --- |
| Missing Source Search Loop | Final-hop census source search | 2 | openai_gpt-5-mini: 2 |
| Post-Answer Or Source Non-Submission | Final source not inspected | 2 | openai_gpt-5-mini: 2 |
| Redundant Intermediate Re-querying | Duplicate quantitative reruns | 2 | openai_gpt-5.4-nano: 2 |
| Redundant Intermediate Re-querying | Repeated top-list aggregation | 2 | openai_gpt-5.4-nano: 2 |
| Candidate Overconfirmation | County/filter confirmation loop | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | Demographic candidate retesting | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | Department mapping overcheck | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | Membership/ranking rechecks | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | Over-narrow text/filter checks | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | SHSAT school-name confirmation | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | SHSAT threshold confirmation | 1 | openai_gpt-5.4-nano: 1 |
| Candidate Overconfirmation | School candidate rechecks | 1 | openai_gpt-5.4-nano: 1 |
| Downstream Deferral and Chain Crowd-Out | First-hop aggregation crowd-out | 1 | openai_gpt-5.4-nano: 1 |
| Downstream Deferral and Chain Crowd-Out | First-hop recomputation crowd-out | 1 | openai_gpt-5.4-nano: 1 |
| Downstream Deferral and Chain Crowd-Out | Side-query detours before final hop | 1 | openai_gpt-5.4-nano: 1 |
| Downstream Deferral and Chain Crowd-Out | Upstream year rework | 1 | openai_gpt-5.4-nano: 1 |
| Missing Source Search Loop | Final-hop leadership source search | 1 | openai_gpt-5-mini: 1 |
| Missing Source Search Loop | Final-hop salary source search | 1 | openai_gpt-5-mini: 1 |
| Missing Source Search Loop | Final-hop street-sweeping source search | 1 | openai_gpt-5-mini: 1 |
| Missing Source Search Loop | TEA identified-student dataset search loop | 1 | openai_gpt-5-mini: 1 |
| Missing Source Search Loop | ZIP/ZCTA land-area source search | 1 | openai_gpt-5-mini: 1 |
| Partial Component Stall | Fragmented multi-hop counting | 1 | openai_gpt-5-mini: 1 |
| Partial Component Stall | Health and overtime chain left incomplete | 1 | openai_gpt-5-mini: 1 |
| Partial Component Stall | Private-school component unresolved | 1 | openai_gpt-5-mini: 1 |
| Partial Component Stall | Unresolved final lookup after earlier components | 1 | openai_gpt-5-mini: 1 |
| Post-Answer Or Source Non-Submission | Failure to submit after answer found | 1 | openai_gpt-5-mini: 1 |
| Post-Answer Or Source Non-Submission | Final salary source not used | 1 | openai_gpt-5-mini: 1 |
| Post-Answer Or Source Non-Submission | Post-answer verification loop | 1 | openai_gpt-5-mini: 1 |
| Post-Answer Verification Churn | Final value rechecks | 1 | openai_gpt-5.4-nano: 1 |
| Post-Answer Verification Churn | Post-winner validation | 1 | openai_gpt-5.4-nano: 1 |
| Post-Answer Verification Churn | Redundant arithmetic after final computation | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Class-size candidate reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | County count recomputation | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | County-ranking/code reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Duplicate ranking reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Intermediate recomputation | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Library ranking reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Library top-list reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Parking count reconfirmation | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Ranking rechecks before later hops | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Ranking reruns with format repair | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Release ranking rechecks | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | School ranking rechecks | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Intermediate Re-querying | Top-county reruns | 1 | openai_gpt-5.4-nano: 1 |
| Redundant Revalidation After Progress | Binge-drinking comparison rechecked after result found | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Broad sanity queries before final county lookup | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Candidate county revalidation | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Candidate-set rechecking before final filters | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Intersection and schema redebugging | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Repeated dataset revalidation before next hop | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Repeated intermediate recomputation before final count | 1 | openai_gpt-5-mini: 1 |
| Redundant Revalidation After Progress | Score-list reruns after candidate found | 1 | openai_gpt-5-mini: 1 |
| Source and Query-Shape Churn | Catalog inspection loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | County query-shape churn | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Dataset/file-path probing | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Date/filter query repair loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Failed ideal repair loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Ideal-query repair and file inspection | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Ideal/regex repair loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Location source recovery churn | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Metadata and schema probing | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Metadata file as rows | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Mis-targeted health-data probing | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Parser and GeoJSON access churn | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Schema repair during annual aggregation | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Schema/ranking query loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Schema/sample repair loop | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Wrong file and ambiguous dataset recovery | 1 | openai_gpt-5.4-nano: 1 |
| Source and Query-Shape Churn | Wrong-file probing | 1 | openai_gpt-5.4-nano: 1 |
| Structured Data Extraction Loop | 500 Cities obesity extraction loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | 500 Cities obesity schema mismatch loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Broad county aggregation and schema probing | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | CAD and school count extraction loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Capital-outlay computation and county extraction loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | County-field and metadata probing | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | GeoJSON offense aggregation repair loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | JSON/GeoJSON aggregation retries | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Large-file complaint numerator extraction loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Large-file execution workaround cycling | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Metadata and grep-result extraction loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Multi-year GeoJSON aggregation repair loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | NCES district-office count repair loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Postsecondary count extraction retries | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Rejected combined computation workaround loop | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | School-count parser mismatch | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | School-count schema and parser retries | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | School-location schema and format probing | 1 | openai_gpt-5-mini: 1 |
| Structured Data Extraction Loop | Use-of-force schema repair loop | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Off-path benefactor clue branch | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Off-target ZIP search after school identified | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Wrong dataset and scope drift | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Wrong-city final-hop drift | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Wrong-source Medicare computation path | 1 | openai_gpt-5-mini: 1 |
| Wrong-Branch Or Off-Path Drift | Wrong-year APD path | 1 | openai_gpt-5-mini: 1 |

## Counts by Error Bucket

| Error Bucket | Errors | Errors by Model |
| --- | --- | --- |
| error_tools_limit | 74 | openai_gpt-5-mini: 30; openai_gpt-5.4-nano: 44 |
| error_turns_exhausted | 16 | openai_gpt-5-mini: 14; openai_gpt-5.4-nano: 2 |
| error_unknown | 4 | openai_gpt-5-mini: 3; openai_gpt-5.4-nano: 1 |
| error_event_loop | 2 | openai_gpt-5-mini: 2 |
| error_tokens_reached | 2 | openai_gpt-5.4-nano: 2 |

## Representative Evidence

### Candidate Overconfirmation

- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-2/task_10.json` (error_tools_limit, wasted turns: 11): Turn 17 | Executing: query_ideal({"dataset_id": "2005-2019-graduation-rates-all", "file_path": "files/rows.txt"; Turn 20 | Executing: peek_file({"dataset_id": "2011-2016-demographic-snapshot", "file_path": "files/rows.txt", "max_rows": 20}); Turn 22 | Execu...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-3/task_6.json` (error_tools_limit, wasted turns: 10): Turn 22 | Tool result: {"dataset_id": "budget-2019-budget-recommendations-positions-and-salaries", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/budget-2019-budget-recommendations-positions-and-salaries/files/rows.txt", "colu...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-3/task_8.json` (error_tools_limit, wasted turns: 9): Turn 17 | Executing: query_ideal({"dataset_id": "2009-2010-school-progress-report", "file_path": "files/rows.txt"; Turn 18 | "intent": "Find what OVERALL SCORE values exist for the top rank in 2009-10 to ensure we can rank."; Turn 22 | Tool result: Tool cal...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-4/task_3.json` (error_tools_limit, wasted turns: 9): Turn 23 | Tool result: Tool call cancelled. Note: you have used 'execute' tools 7 times in a row.; Turn 24 | "intent": "intersection dbns 2015-19 >=50 and in 26Q"; Turn 25 | "intent": "show intersection dbns"; Turn 27 | "intent": "count intersection dbns";...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-4/task_3.json` (error_tools_limit, wasted turns: 7): Turn 10 | Executing: query_ideal({"dataset_id": "2015-2016-shsat-admissions-test-offers-by-sending-school", "file_path": "files/rows.txt", "sql": "SELECT \"Feeder School DBN\" as dbn, \"Feeder School Name\" as name, \"Count of Offers\" as offers FROM t WHER...

### Downstream Deferral and Chain Crowd-Out

- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-3/task_5.json` (error_tools_limit, wasted turns: 19): Turn 13 | Tool result: {"dataset_id": "2023-state-employee-pay", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/2023-state-employee-pay/files/rows.txt", "columns": ["answer"], "rows": [["CORRECTIONS"]], "row_count": 1, "trunca...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-2/task_7.json` (error_tools_limit, wasted turns: 15): Turn 5 | Tool result: {"dataset_id": "crime-incidents-in-2017", "file_path": "files/data.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/crime-incidents-in-2017/files/data.txt", "columns": ["answer"], "rows": [["THEFT/OTHER"]], "row_count": 1, "truncat...
- `openai_gpt-5.4-nano` `tasks_mini/k-3-d-4/task_1.json` (error_turns_exhausted, wasted turns: 6): Turn 3 | Executing: query_ideal({"dataset_id": "crime-incidents-in-2021", "file_path": "files/data.txt", "intent": "Compute total number of crime incidents by DC ward for 2021."; Turn 4 | Executing: query_ideal({"dataset_id": "crime-incidents-in-2021", "fil...
- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-4/task_2.json` (error_tools_limit, wasted turns: 5): Turn 8 | Tool result: {"dataset_id": "2007-state-expenditures", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/2007-state-expenditures/files/rows.txt", "columns": ["answer"], "rows": [["{\"SOCIAL SERVICES\":5528171459.84,\"ELE...

### Missing Source Search Loop

- `openai_gpt-5-mini` `tasks_mini/k-4-d-2/task_1.json` (error_tools_limit, wasted turns: 18): Turn 14 | Tool result: {"dataset_id": "2012-2013-school-locations", "file_path": "files/rows.txt"; Turn 16 | Executing: search_ideal({"query": "Census 2010 ZIP code demographics percent White 2010 New York City 11203 dataset 'zip code tabulation area' 'race...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-1/task_6.json` (error_event_loop, wasted turns: 12): Turn 3 | Executing: query_file({"s3_uri": "s3://lakeqa-yc4103-datalake/datagov/pittsburgh-international-airport-scheduled-passenger-traffic/files/pittsburgh-international-traffic-report-march-2019.txt", "sql": "SELECT \"Destination\", \"Destination Code\",...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-3/task_7.json` (error_tools_limit, wasted turns: 11): Turn 2 | Executing: search_ideal({"query": "District of Columbia street sweeping schedule 2022 2023 2024 'street sweeping schedule' 'DC Department of Public Works' 'sweeping' 'ward'"}); Turn 19 | Executing: read_file({"dataset_id": "dc-charter-schools", "fi...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-3/task_3.json` (error_tools_limit, wasted turns: 11): Turn 22 | Executing: search_ideal({"query": "Texas school district 'Identified Students' percentage 2019 2020 2021 'Identified Students' 'district' 'percentage' dataset Texas 'Identified' 'school district' '2019' '2020' '2021'"}); Turn 22 | Tool result: {"r...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-2/task_1.json` (error_tools_limit, wasted turns: 10): Turn 21 | Executing: search_ideal({"query": "2010 census race by ZIP code percentage White 2010 'ZIP Code Tabulation Area' 'ZCTA' 'White' '2010' dataset NYC 'race by zip 2010'"}); Turn 22 | Tool result: {"results": [], "count": 0, "query": "2010 Census ZCTA...

### Partial Component Stall

- `openai_gpt-5-mini` `tasks_mini/k-3-d-2/task_7.json` (error_tools_limit, wasted turns: 15): Turn 17 | Tool result: {"success": true, "dataset_id": "postsecondary-school-locations-current-5a74c", "file_path": "files/Postsecondary_School_Locations_Current_-3631565628879840217.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/postsecondary-school-...
- `openai_gpt-5-mini` `tasks_mini/k-2-d-3/task_1.json` (error_tools_limit, wasted turns: 5): Turn 15 | Tool logical error (status=error): {"success": false, "error": "Cannot execute SQL: file is too big (1377 MB >= 500 MB limit)."; Turn 22 | Executing: query_ideal({"dataset_id": "apd-use-of-force", "file_path": "files/rows.txt", "sql": "SELECT COUN...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-4/task_6.json` (error_tools_limit, wasted turns: 4): Turn 19 | Executing: query_ideal({"dataset_id": "texas-state-expenditures-by-county-2018"; Turn 28 | Tool result: {"success": true, "dataset_id": "texas-department-of-criminal-justice-releases-fy-2019"; Turn 29 | Executing: query_ideal({"dataset_id": "texas...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-4/task_2.json` (error_turns_exhausted, wasted turns: 4): Turn 24 | Tool result: {"dataset_id": "500-cities-local-data-for-better-health-2018-release", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/500-cities-local-data-for-better-health-2018-release/files/rows.txt"; Turn 28 | Execu...

### Post-Answer Or Source Non-Submission

- `openai_gpt-5-mini` `tasks_mini/k-4-d-4/task_4.json` (error_tools_limit, wasted turns: 17): Turn 10 | Tool result: {"dataset_id": "employee-overtime-and-supplemental-earnings-2017"; Turn 11 | Executing: query_ideal({"dataset_id": "employee-overtime-and-supplemental-earnings-2014", "file_path": "files/rows.txt", "sql": "SELECT SUM(\"TOTAL\") AS tot...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-3/task_11.json` (error_unknown, wasted turns: 11): Turn 15 | Tool result: {"dataset_id": "county-population-in-iowa-by-year", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/county-population-in-iowa-by-year/files/rows.txt", "columns": ["answer"], "rows": [["172943"]]; Turn 16...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-3/task_11.json` (error_tools_limit, wasted turns: 10): Turn 22 | Executing: search_ideal({"query": "DC street sweeping schedule dataset 2022 2023 2024 Department of Public Works street sweeping schedule ward 'sweeping' 'street sweeping' 'schedule' 'ward'"}); Turn 23 | Executing: search_ideal({"query": "Washingt...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-4/task_4.json` (error_turns_exhausted, wasted turns: 6): Turn 24 | Executing: search_ideal({"query": "Chicago Police starting salary 2025 \"starting salary\" Police 2025 city of Chicago salary schedule 'Police' 'starting salary' 2025 dataset"}); Turn 24 | Tool result: {"results": [{"dataset_id": "Chicago_Police_D...
- `openai_gpt-5-mini` `tasks_mini/k-6-d-3/task_4.json` (error_turns_exhausted, wasted turns: 2): Turn 28 | Tool result: {"dataset_id": "postsecondary-school-locations-2019-20-64b31"; Turn 28 | "rows": [["11"]]; Turn 29 | Executing: parse_xml_records({"dataset_id": "public-school-locations-2018-19-42360"; Turn 30 | Executing: query_ideal({"dataset_id":...

### Post-Answer Verification Churn

- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-3/task_6.json` (error_tools_limit, wasted turns: 8): Turn 23 | Executing: query_ideal({"dataset_id": "texas-department-of-criminal-justice-receives-fy-2019", "file_path": "files/rows.txt", "intent": "Get intake counts for Harris/Travis/Dallas/Bexar FY2019 as separate rows."; Turn 24 | Executing: query_ideal({...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-2/task_5.json` (error_tools_limit, wasted turns: 7): Turn 12 | Tool result: {"success": true, "dataset_id": "crime-data-from-2020-to-present", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/crime-data-from-2020-to-present/files/rows.txt", "columns": ["answer"], "rows": [["BURGLA...
- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-3/task_7.json` (error_tools_limit, wasted turns: 4): Turn 17 | Tool result: {"dataset_id": "moving-violations-issued-in-january-2021", "file_path": "files/data.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/moving-violations-issued-in-january-2021/files/data.txt", "columns": ["answer"], "rows": [["UNITE...

### Redundant Intermediate Re-querying

- `openai_gpt-5.4-nano` `tasks_mini/k-3-d-4/task_7.json` (error_tools_limit, wasted turns: 18): Turn 12 | Tool result: {"success": true, "dataset_id": "2009-2010-school-progress-report"; Turn 13 | Executing: query_ideal({"dataset_id": "2006-2007-school-progress-report", "file_path": "files/rows.txt", "intent": "Get top-3 school DBNs in District 3 by p...
- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-3/task_9.json` (error_tools_limit, wasted turns: 17): Turn 7 | Executing: query_ideal({"dataset_id": "libraries-2021-computer-sessions-by-location", "file_path": "files/rows.txt", "intent": "Top 10 branches by YTD computer sessions in 2021"; Turn 8 | Executing: query_ideal({"dataset_id": "libraries-2020-visito...
- `openai_gpt-5.4-nano` `tasks_mini/k-6-d-3/task_1.json` (error_tools_limit, wasted turns: 15): Turn 12 | "columns": ["fiscal_year", "agency", "professional_services_spend"]; Turn 17 | "intent": "Capture 2021 top agencies again with string match."; Turn 18 | Tool result: Tool call cancelled. Note: you have used 'execute' tools 7 times in a row. If you...
- `openai_gpt-5.4-nano` `tasks_mini/k-6-d-3/task_3.json` (error_tools_limit, wasted turns: 14): Turn 1 | Executing: pick({"s3_uris": ["s3://lakeqa-yc4103-datalake/datagov/libraries-2019-computer-sessions-by-location/files/rows.txt", "s3://lakeqa-yc4103-datalake/datagov/libraries-2020-computer-sessions-by-location/files/rows.txt", "s3://lakeqa-yc4103-d...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-4/task_10.json` (error_tools_limit, wasted turns: 11): Turn 10 | Executing: parse_xml_records({"dataset_id": "public-school-locations-2018-19-42360", "file_path": "files/data.txt", "record_tag": "Placemark", "group_by": ["STFIP", "NMCNTY"], "fields": ["STFIP", "NMCNTY"], "limit": 3}); Turn 12 | Executing: parse...

### Redundant Revalidation After Progress

- `openai_gpt-5-mini` `tasks_mini/k-4-d-2/task_9.json` (error_tools_limit, wasted turns: 17): Turn 8 | Tool result: {"output": "2016", "success": true, "dataset_id": "crime-data-from-2010-to-2019"; Turn 11 | Tool result: {"dataset_id": "arrest-data-from-2010-to-2019", "file_path": "files/rows.txt"; Turn 12 | "intent": "Count DUI-type arrests in 2016...
- `openai_gpt-5-mini` `tasks_mini/k-6-d-2/task_4.json` (error_tools_limit, wasted turns: 11): Turn 18 | Executing: search_ideal({"query": "dataset '500-cities' 'Local Data for Better Health' 2020 release 'rows.txt' 2018 obesity 'OBESITY' Year 2018 'MeasureId' 'OBESITY'"}); Turn 20 | Executing: search_ideal({"query": "500-cities-local-data-for-better...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-3/task_10.json` (error_turns_exhausted, wasted turns: 9): Turn 22 | Executing: query_ideal({"dataset_id": "index-crimes-by-county-and-agency-beginning-1990", "file_path": "files/rows.txt"; Turn 23 | Executing: query_ideal({"dataset_id": "nys-school-tax-relief-star-reimbursement-by-county-beginning-levy-year-1998",...
- `openai_gpt-5-mini` `tasks_mini/k-3-d-4/task_3.json` (error_unknown, wasted turns: 6): Turn 23 | Executing: query_file({"dataset_id": "report-card-enrollment-2018-19-school-year", "file_path": "files/rows.txt", "sql": "SELECT \"County\" FROM (\n  SELECT \"County\", COUNT(*) AS yrs; Turn 23 | Tool result: {"dataset_id": "report-card-enrollment...
- `openai_gpt-5-mini` `tasks_mini/k-3-d-5/task_1.json` (error_tools_limit, wasted turns: 6): Turn 20 | Executing: query_file({"dataset_id": "2007-2008-school-progress-report", "file_path": "files/rows.txt", "sql": "SELECT \"DBN\",\"SCHOOL\",\"OVERALL SCORE\" FROM t WHERE \"PROGRESS REPORT TYPE\"='HS' AND \"OVERALL SCORE\"!='Under Review' ORDER BY C...

### Source and Query-Shape Churn

- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-4/task_5.json` (error_turns_exhausted, wasted turns: 17): Turn 2 | Tool result: {"dataset_id": "2010-state-expenditures", "file_path": "files/rows.txt", "s3_uri": "s3://lakeqa-yc4103-datalake/datagov/2010-state-expenditures/files/rows.txt", "columns": ["Agency Name", "total_expenditure"], "rows": [["SOCIAL SERVICE...
- `openai_gpt-5.4-nano` `tasks_mini/k-5-d-4/task_3.json` (error_tools_limit, wasted turns: 13): Turn 8 | Executing: query_ideal({"dataset_id": "500-cities-local-data-for-better-health-2016-release", "file_path": "files/rows.txt", "sql": "SELECT DISTINCT \"Short_Question_Text\"; Turn 9 | Tool result: {"dataset_id": "500-cities-local-data-for-better-hea...
- `openai_gpt-5.4-nano` `tasks_mini/k-3-d-5/task_1.json` (error_tools_limit, wasted turns: 9): Turn 16 | Executing: query_ideal({"dataset_id": "2006-2007-school-progress-report", "file_path": "files/rows.txt", "intent": "Find neighborhood column name existence for Manhattan Bridges High School by selecting possible location columns."; Turn 16 | Tool...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-5/task_2.json` (error_tools_limit, wasted turns: 9): Turn 12 | Executing: query_file({"dataset_id": "2001-campaign-expenditures", "file_path": "files/data.txt", "sql": "SELECT * FROM t LIMIT 1"}); Turn 14 | Tool logical error (status=error): {"error": "Query failed: Binder Error: Referenced column \"AMNT\" no...
- `openai_gpt-5.4-nano` `tasks_mini/k-4-d-2/task_15.json` (error_unknown, wasted turns: 7): Turn 1 | Executing: plan_ideal({"plan_text": "1) Identify which of King, Clark, Pierce, Whitman, Thurston, Spokane are in Eastern Washington.; Turn 3 | Executing: search_value({"query": "2020 population King County WA Idaho border county population dataset"...

### Structured Data Extraction Loop

- `openai_gpt-5-mini` `tasks_mini/k-6-d-2/task_4.json` (error_turns_exhausted, wasted turns: 19): Turn 6 | Executing: query_ideal({"dataset_id": "500-cities-local-data-for-better-health-2016-release", "file_path": "files/rows.txt", "sql": "SELECT DISTINCT \"GeographicLevel\" FROM s3object WHERE \"Measure\" LIKE '%Obesity%';"; Turn 11 | Executing: query_...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-4/task_10.json` (error_tools_limit, wasted turns: 16): Turn 13 | Executing: parse_xml_records({"dataset_id": "public-school-locations-2018-19-42360", "file_path": "files/data.txt", "record_tag": "Placemark"; Turn 17 | Executing: search_ideal({"query": "dataset county counts public schools by county 'group by' '...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-1/task_4.json` (error_turns_exhausted, wasted turns: 16): Turn 1 | Executing: search_ideal({"query": "Queens precinct complaints 2022 NYPD complaint data precinct complaints 2022 dataset use-of-force 2024 Queens 'location descriptor' shootings 'complaint' '2022' dataset site:data.cityofnewyork or data.cityofnewyor...
- `openai_gpt-5-mini` `tasks_mini/k-3-d-2/task_9.json` (error_tools_limit, wasted turns: 15): Turn 4 | Executing: search_value({"query": "public school locations 2022-23 NCES public school locations 2022-2023 dataset Michigan files 'public school locations' '2022' 'NCES'"}); Turn 11 | Executing: search_value({"query": "public school locations 2022-2...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-2/task_6.json` (error_tools_limit, wasted turns: 15): Turn 11 | Executing: download({}); Turn 11 | Tool result: Error: Validation failed for input parameters: 1 validation error for DownloadTool; Turn 17 | Tool result: {"output": "{'counts': [(2010, 20); Turn 21 | Executing: query_ideal({"dataset_id": "lapd-ri...

### Wrong-Branch Or Off-Path Drift

- `openai_gpt-5-mini` `tasks_mini/k-4-d-2/task_4.json` (error_tools_limit, wasted turns: 18): Turn 3 | Executing: search_value({"query": "Zohaib Qadri 'Zo' 'Zo Qadri' Austin district"}); Turn 8 | Tool result: Tool call cancelled. Note: you have used 'search' tools 7 times in a row.; Turn 15 | Executing: grep_file({"dataset_id": "city-of-austin-counc...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-4/task_2.json` (error_turns_exhausted, wasted turns: 12): Turn 5 | Executing: peek_multiple({"max_rows": 5}); Turn 10 | Model response #10 [role=assistant block=1 tool_use] query_ideal({"sql": "WITH t2007 AS (SELECT \"Agency\" AS agency, SUM(CAST(\"Expenditures\" AS DOUBLE)) AS total_2007 FROM 's3://lakeqa-yc4103-...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-5/task_3.json` (error_unknown, wasted turns: 11): Turn 9 | Executing: execute_ideal({"code": "import pandas as pd\nfn = '/home/ec2-user/eval_eqa/exploratory-qa-eval/.sandbox_isolated/task_1289399_1778877619699/medicare-part-d-spending-by-drug-401d2/files/DSD_PTD_RY24_P04_V10_DY22_BGM.txt'; Turn 9 | Submitt...
- `openai_gpt-5-mini` `tasks_mini/k-4-d-4/task_13.json` (error_tools_limit, wasted turns: 10): Turn 21 | Executing: search_value({"query": "Rhode Island Hospital 'named in honor' 'named for' benefactor 'Rhode Island Hospital' 'named after' Providence wing 'named' 'benefactor'"}); Turn 21 | Moses_Brown_Ives", "s3_uri": "s3://lakeqa-yc4103-datalake/wik...
- `openai_gpt-5-mini` `tasks_mini/k-5-d-2/task_5.json` (error_turns_exhausted, wasted turns: 10): Turn 14 | Executing: query_ideal({"dataset_id": "nchs-drug-poisoning-mortality-by-county-united-states-20278", "file_path": "files/rows.txt"; Turn 18 | Tool result: {"dataset_id": "nchs-drug-poisoning-mortality-by-county-united-states-20278", "file_path": "...
