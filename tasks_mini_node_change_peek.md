# Node Change Peek

Direction: `tasks_mini copy` -> `tasks_mini`.

## How to read this

- `node.fact` is the executable code string used to compute that node result. The report shows a compact unified diff of changed code lines.
- `node.depends_on` changes the dependency graph: which previous node outputs this node is allowed or expected to use.
- `node.subquestion` changes the natural-language intermediate question for that node.
- `node.answer` changes the expected intermediate answer for that node.
- `node.source` changes the dataset/file attached to the node.
- `node.limit` changes constraints on how much evidence/tool work the node should use.

## Counts

- `answer` changes: 319
- `depends_on` changes: 32
- `fact` changes: 669
- `limit` changes: 119
- `source` changes: 101
- `subquestion` changes: 726

## By task

### `k-1-d-1/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `For each year from 2016 through 2023, compute a growth-amplified overdose burden score as annual drug overdose deaths across all U.S. states multiplied by (1 + year-over-year growth rate). Which year has the highest score?`
  - tasks_mini: `For each year from 2016 through 2023, compute a growth-amplified overdose burden score: annual drug overdose deaths across all U.S. states multiplied by (1 + year-over-year growth rate).`

- Node 1 `fact`

```diff
@@ -2,19 +2,19 @@
-df = pd.read_csv("datagov/vsrr-provisional-drug-overdose-death-counts/files/rows.txt", sep=None, engine="python")
-df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
-df["Data Value"] = pd.to_numeric(df["Data Value"], errors="coerce")
+df = pd.read_csv('datagov/vsrr-provisional-drug-overdose-death-counts/files/rows.txt', low_memory=False)
+df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
+df['Data Value'] = pd.to_numeric(df['Data Value'], errors='coerce')
```

### `k-1-d-1/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `For each year from 2005 through 2010, define Bonus Volatility-Adjusted Level (BVAL) as the draws' average New York Lotto bonus ball number plus half of the standard deviation of bonus ball numbers. Which year has the highest BVAL? If there is a tie, choose the earlier year.`
  - tasks_mini: `For each year from 2005 through 2010, compute BVAL (Bonus Volatility-Adjusted Level) as the draws' average bonus ball number plus half of the standard deviation of bonus ball numbers. Which year has the highest BVAL? If there is a tie, choose the earlier year.`

- Node 1 `fact`

```diff
@@ -2,18 +2,11 @@
-df = pd.read_csv("datagov/lottery-ny-lotto-winning-numbers-beginning-2001/files/rows.txt", sep=None, engine="python")
-df["Draw Date"] = pd.to_datetime(df["Draw Date"], errors="coerce")
-df["Bonus #"] = pd.to_numeric(df["Bonus #"], errors="coerce")
-df["Year"] = df["Draw Date"].dt.year
+df = pd.read_csv('datagov/lottery-ny-lotto-winning-numbers-beginning-2001/files/rows.txt')
+df['Draw Date'] = pd.to_datetime(df['Draw Date'], errors='coerce')
```

### `k-1-d-1/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Define a yearly Passenger Instability-Adjusted Load (PIAL) as annual total CTA bus passengers across all routes multiplied by (1 + absolute year-over-year percentage change in that annual total). For years 2006 through 2010, which year has the lowest PIAL? If there is a tie, choose the earlier year.`
  - tasks_mini: `For each year from 2006 through 2010, compute PIAL (Passenger Instability-Adjusted Load) as annual total CTA bus passengers across all routes times (1 + absolute year-over-year percentage change in that annual total). Which year has the lowest PIAL?`

- Node 1 `fact`

```diff
@@ -2,13 +2,12 @@
-df = pd.read_csv("datagov/cta-ridership-bus-routes-monthly-day-type-averages-totals/files/rows.txt", sep=None, engine="python")
-df["Month_Beginning"] = pd.to_datetime(df["Month_Beginning"], errors="coerce")
-df["MonthTotal"] = pd.to_numeric(df["MonthTotal"], errors="coerce")
-df["Year"] = df["Month_Beginning"].dt.year
+df = pd.read_csv('datagov/cta-ridership-bus-routes-monthly-day-type-averages-totals/files/rows.txt')
+df['Month_Beginning'] = pd.to_datetime(df['Month_Beginning'], errors='coerce')
```

### `k-2-d-3/task_1.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/apd-searches-by-type/files/rows.txt`
  - tasks_mini: `datagov/nopd-use-of-force-incidents/files/rows.txt`

- Node 1 `subquestion`
  - copy: `In 2022, which APD patrol sector had the most searches due to illegal items in plain view?`
  - tasks_mini: `In 2022, what is the highest number of incidents where an officer applies weapon across any NOPD divisions?`

- Node 1 `answer`
  - copy: `Edward`
  - tasks_mini: `92`

- Node 1 `fact`

```diff
@@ -3,16 +3,11 @@
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/apd-searches-by-type/files/rows.txt"
+source = "datagov/nopd-use-of-force-incidents/files/rows.txt"
-obj = boto3.client("s3").get_object(Bucket=bucket, Key=source)
+obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `source`
  - copy: `datagov/nopd-use-of-force-incidents/files/rows.txt`
  - tasks_mini: `datagov/apd-searches-by-type/files/rows.txt`

- Node 2 `subquestion`
  - copy: `In 2022, what is the highest number of incidents where an officer applies weapon across any NOPD divisions?`
  - tasks_mini: `In 2022, which APD patrol sector had the most searches due to illegal items?`

- Node 2 `answer`
  - copy: `92`
  - tasks_mini: `Edward`

- Node 2 `fact`

```diff
@@ -3,9 +3,18 @@
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/nopd-use-of-force-incidents/files/rows.txt"
+source = "datagov/apd-searches-by-type/files/rows.txt"
-obj = boto3.client("s3").get_object(Bucket=bucket, Key=source)
+obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `subquestion`
  - copy: `In 2022, how many APD call logs were labeled as mental health incidents in patrol sector <node_1 answer>?`
  - tasks_mini: `In 2022, how many APD call logs were labeled as mental health incidents in patrol sector <node_2 answer>?`

- Node 3 `fact`

```diff
@@ -1,5 +1,10 @@
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
-node_1_answer = "Edward"
+bucket = "lakeqa-yc4103-datalake"
+obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -3,2 +3,4 @@
+from botocore import UNSIGNED
+from botocore.config import Config
@@ -6,3 +8,3 @@
-obj = boto3.client("s3").get_object(Bucket=bucket, Key=source)
+obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-1/task_1.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `In 2023 NYPD complaint data, within borough <node_1 answer>, how many complaints were filed for the most common offense description?`
  - tasks_mini: `In 2023 NYPD complaint data, within borough <node_1 answer>, how many complaints were filed for the most common offense description (OFNS_DESC)?`

- Node 2 `fact`

```diff
@@ -1,22 +1,15 @@
-import io
-import boto3
+from collections import Counter
-source = 'datagov/nypd-complaint-data-historic/files/rows.txt'
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3").get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -1,23 +1,8 @@
-import io
-import boto3
-try:
-    from dotenv import load_dotenv
-    load_dotenv()
-except Exception:
```

### `k-3-d-2/task_1.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/apd-searches-by-type/files/rows.txt`
  - tasks_mini: `wikipedia/Austin,_Texas/content.txt`

- Node 1 `subquestion`
  - copy: `In 2023 APD searches-by-type data (excluding Sector = "Unknown"), which sector has the most searches?`
  - tasks_mini: `According to the Austin, Texas article, in what year was Austin founded?`

- Node 1 `answer`
  - copy: `Charlie`
  - tasks_mini: `1839`

- Node 1 `fact`

```diff
@@ -1,19 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 2 `source`
  - copy: `datagov/apd-computer-aided-dispatch-incidents/files/rows.txt`
  - tasks_mini: `datagov/apd-searches-by-type/files/rows.txt`

- Node 2 `subquestion`
  - copy: `In 2023 APD computer-aided-dispatch incidents data, within sector <node_1 answer>, which council district has the most incidents?`
  - tasks_mini: `In 2023 APD searches-by-type data (excluding Sector = "Unknown"), which sector has the most searches?`

- Node 2 `answer`
  - copy: `1`
  - tasks_mini: `Charlie`

- Node 2 `fact`

```diff
@@ -6,25 +6,13 @@
-source = "datagov/apd-computer-aided-dispatch-incidents/files/rows.txt"
+source = "datagov/apd-searches-by-type/files/rows.txt"
-csv_path = io.BytesIO(obj["Body"].read())
-
-node_1_answer = "Charlie"
-
```

- Node 3 `source`
  - copy: `wikipedia/Austin,_Texas/content.txt`
  - tasks_mini: `datagov/apd-computer-aided-dispatch-incidents/files/rows.txt`

- Node 3 `subquestion`
  - copy: `According to the Austin, Texas article, in what year was Austin founded?`
  - tasks_mini: `In 2023 APD computer-aided-dispatch incidents data, within sector <node_2 answer>, which council district has the most incidents?`

- Node 3 `answer`
  - copy: `1839`
  - tasks_mini: `1`

- Node 3 `fact`

```diff
@@ -1 +1,27 @@
-The Austin, Texas article states that Austin was founded in 1839.
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
+
```

- Node 4 `subquestion`
  - copy: `In 2023 APD use-of-force data, how many incidents with Used Taser(s) > 0 occurred in council district <node_2 answer>?`
  - tasks_mini: `In 2023 APD use-of-force data, how many incidents with Used Taser(s) > 0 occurred in council district <node_3 answer>?`

- Node 4 `fact`

```diff
@@ -9,5 +9,4 @@
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), sep=",", engine="c", low_memory=False)
-
-node_2_answer = "1"
+df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+node_3_answer = "1"
@@ -15,3 +14,3 @@
-filtered = filtered[filtered["Council District Numeric"].eq(pd.to_numeric(node_2_answer, errors="coerce"))]
```

### `k-3-d-2/task_10.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_11.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -1,17 +1,9 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/fy-2019-disability-pension-recipient-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 2 `fact`

```diff
@@ -1,17 +1,9 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Big Horn County's county seat is Basin.
+Big Horn County's county seat is Basin. The county was created in March 1890 and was named for the Big Horn Mountains which form its eastern boundary.
```

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Basin had the highest temperature ever recorded in Wyoming, 115°F (46.1°C), on August 8, 1983.
+Basin had the highest temperature ever recorded in Wyoming, 115°F (46.1°C), on August 8, 1983. Basin also holds the state record high temperatures for April (95°F in 1948) and July (114°F in 1900).
```

### `k-3-d-2/task_12.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -1,17 +1,9 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/fy-2019-disability-pension-recipient-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 2 `fact`

```diff
@@ -1,17 +1,9 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Glacier County's county seat is Cut Bank, located in eastern Glacier County on the edge of the Great Plains.
+Glacier County's county seat is Cut Bank, located in eastern Glacier County on the edge of the Great Plains. The county includes the Blackfeet Indian Reservation and borders Canada.
```

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Cut Bank is home to the world's largest statue of a penguin.
+Cut Bank is home to the world's largest statue of a penguin. The statue features a penguin on an iceberg with the text 'Welcome to Cut Bank MT, Coldest Spot in the Nation', referencing Cut Bank's reputation for being frequently the coldest location in the lower 48 U.S. States.
```

### `k-3-d-2/task_2.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -10,6 +10,4 @@
-
-
```

- Node 3 `fact`

```diff
@@ -10,6 +10,4 @@
-
-
```

- Node 4 `fact`

```diff
@@ -10,6 +10,4 @@
-
-
```

### `k-3-d-2/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NYC high schools in District 10 were in the top 6 by overall score in 2006-07, and what were their additional-credit values?`
  - tasks_mini: `Which NYC high schools in District 10 were in the top 6 by overall score in 2006-07?`

- Node 1 `answer`
  - copy: `{"BRONX HIGH SCHOOL OF SCIENCE": 1.0, "BRONX SCHOOL OF LAW AND FINANCE": 6.0, "HIGH SCHOOL OF AMERICAN STUDIES AT LEHMAN COLLEGE": 3.0, "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES": 9.0, "RIVERDALE/KINGSBRIDGE ACADEMY (MS/HS 141)": 12.0, "UNIVERSITY HEIGHTS SECONDARY SCHOOL AT BRONX COMMU": 12.0}`
  - tasks_mini: `["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL OF AMERICAN STUDIES AT LEHMAN COLLEGE", "RIVERDALE/KINGSBRIDGE ACADEMY (MS/HS 141)", "BRONX SCHOOL OF LAW AND FINANCE", "UNIVERSITY HEIGHTS SECONDARY SCHOOL AT BRONX COMMU"]`

- Node 1 `fact`

```diff
@@ -1,21 +1,10 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/2006-2007-school-progress-report/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 2 `subquestion`
  - copy: `Which NYC high schools in District 10 were in the top 6 by overall score in 2007-08, and what were their additional-credit values?`
  - tasks_mini: `Which NYC high schools in District 10 were in the top 6 by overall score in 2007-08?`

- Node 2 `answer`
  - copy: `{"BRONX HIGH SCHOOL FOR MEDICAL SCIENCE": 8.0, "BRONX HIGH SCHOOL OF SCIENCE": 2.0, "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES": 12.0, "MARIE CURIE HIGH SCHOOL FOR NURSING, MEDICINE, AND ALLIED HEALTH PROFE": 10.0, "RIVERDALE / KINGSBRIDGE ACADEMY (MIDDLE SCHOOL / HIGH SCHOOL 141)": 12.0, "UNIVERSITY HEIGHTS SECONDARY SCHOOL AT BRONX COMMUNITY COLLE...`
  - tasks_mini: `["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "MARIE CURIE HIGH SCHOOL FOR NURSING, MEDICINE, AND ALLIED HEALTH PROFE", "RIVERDALE / KINGSBRIDGE ACADEMY (MIDDLE SCHOOL / HIGH SCHOOL 141)", "BRONX HIGH SCHOOL FOR MEDICAL SCIENCE", "BRONX HIGH SCHOOL OF SCIENCE"]`

- Node 2 `fact`

```diff
@@ -1,21 +1,10 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/2007-2008-school-progress-report/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 4 `subquestion`
  - copy: `Which University does <node_3 answer> received his Ph.D. from?`
  - tasks_mini: `Which University does <node_4 answer> received his Ph.D. from?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-in mathematics from Princeton University in 1954.
+He received a B.A. in mathematics from Harvard University in 1950 and a Ph.D. in mathematics from Princeton University in 1954.
```

### `k-3-d-2/task_4.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,18 +2,18 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/crime-incidents-in-2019/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/crime-incidents-in-2020/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/crime-incidents-in-2021/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_5.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_6.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_7.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_8.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-2/task_9.json`
- Impact: moderate
- Node 2 `fact`

```diff
@@ -2,20 +2,13 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `fact`

```diff
@@ -2,22 +2,12 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-3/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which high schools were in the top 7 by overall score in 2006-07?`
  - tasks_mini: `Which high schools ranked in the top 7 based on the comprehensive ranking in 2006-07?`

- Node 1 `fact`

```diff
@@ -1,36 +1,26 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2006-2007-school-progress-report/files/rows.txt"
```

- Node 2 `subquestion`
  - copy: `Which high schools were in the top 7 by overall score in 2009-10?`
  - tasks_mini: `Which high schools ranked in the top 7 based on the comprehensive ranking in 2009-10?`

- Node 2 `fact`

```diff
@@ -1,36 +1,26 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2009-2010-school-progress-report/files/rows.txt"
```

- Node 3 `subquestion`
  - copy: `Which high schools were in the top 7 by overall score in 2010-11?`
  - tasks_mini: `Which high schools ranked in the top 7 based on the comprehensive ranking in 2010-11?`

- Node 3 `fact`

```diff
@@ -1,33 +1,26 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2010-2011-school-progress-report/files/rows.txt"
```

- Node 4 `subquestion`
  - copy: `Who built the earliest constructed bridge that connects <hop 1 answer> with the mainland?`
  - tasks_mini: `Who built the earliest constructed bridge that connects the neighborhood named after <intersection of node_1, node_2, node_3> with the mainland?`

- Node 5 `subquestion`
  - copy: `In which village is <hop 2 answer> buried?`
  - tasks_mini: `In which village is <node_4 answer> buried?`

### `k-3-d-3/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which branches were in the top 5 by YTD visitors in the given year?`
  - tasks_mini: `In 2019, which Chicago library branches were in the top 5 by total visitors?`

- Node 1 `fact`

```diff
@@ -1,19 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 2 `subquestion`
  - copy: `Which branches were in the top 5 by YTD visitors in the given year?`
  - tasks_mini: `In 2020, which Chicago library branches were in the top 5 by total visitors?`

- Node 2 `fact`

```diff
@@ -1,19 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 3 `subquestion`
  - copy: `Which branches were in the top 5 by YTD visitors in the given year?`
  - tasks_mini: `In 2021, which Chicago library branches were in the top 5 by total visitors?`

- Node 3 `fact`

```diff
@@ -1,19 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 4 `subquestion`
  - copy: `Which branches were in the top 3 by YTD computer sessions in the given year?`
  - tasks_mini: `In 2019, which Chicago library branches were in the top 3 by total reserved public-computer time slots (each at most 60 minutes)?`

- Node 4 `fact`

```diff
@@ -1,23 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 5 `subquestion`
  - copy: `Which branches were in the top 3 by YTD computer sessions in the given year?`
  - tasks_mini: `In 2020, which Chicago library branches were in the top 3 by total reserved public-computer time slots (each at most 60 minutes)?`

- Node 5 `fact`

```diff
@@ -1,23 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 6 `subquestion`
  - copy: `Which branches were in the top 3 by YTD computer sessions in the given year?`
  - tasks_mini: `In 2021, which Chicago library branches were in the top 3 by total reserved public-computer time slots (each at most 60 minutes)?`

- Node 6 `fact`

```diff
@@ -1,23 +1,21 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 7 `subquestion`
  - copy: `Which Chicago neighborhood is the library branch (from hop 2) located in? (Lookup: Conrad Sulzer Regional Library article.).`
  - tasks_mini: `Which neighborhood is Conrad Sulzer Regional Library located in?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-According to the Wikipedia article for Conrad Sulzer Regional Library, the library is located in the Lincoln Square neighborhood at 4455 N.
+According to the Wikipedia article for Conrad Sulzer Regional Library, the library is located in the Lincoln Square neighborhood at 4455 N. Lincoln Avenue.
```

### `k-3-d-3/task_3.json`
- Impact: major
- Node 1 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 1 `fact`

```diff
@@ -1,38 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2010-2011-school-progress-report/files/rows.txt"
```

- Node 2 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 2 `fact`

```diff
@@ -1,38 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2011-2012-school-progress-report-all-schools/files/rows.txt"
```

- Node 3 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 3 `fact`

```diff
@@ -1,38 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2012-2013-citywide-progress-report/files/rows.txt"
```

- Node 4 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2_3"]`

- Node 4 `subquestion`
  - copy: `In which Manhattan neighborhood is <hop 1 answer> located?`
  - tasks_mini: `In which Manhattan neighborhood is <intersection of node_1, node_2, node_3: PS 77 Lower Lab School> located?`

- Node 4 `fact`

```diff
@@ -1,32 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
-source = "datagov/2013-2014-school-locations/files/rows.txt"
```

- Node 5 `depends_on`
  - copy: ``
  - tasks_mini: `["node_4"]`

- Node 5 `subquestion`
  - copy: `After whom is <hop 2 answer> named?`
  - tasks_mini: `After whom is <node_4 answer> named?`

- Node 6 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

- Node 6 `subquestion`
  - copy: `In what year was <hop 3 answer> born?`
  - tasks_mini: `In what year was <node_5 answer> born?`

### `k-3-d-3/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending?`
  - tasks_mini: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending? (Filter for this node: Major Spending Category == 'Capital Outlay'; group by County; sum Amount; normalize County to uppercase; rank desc; take top 5.)`

- Node 1 `fact`

```diff
@@ -1,20 +1,23 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 2 `subquestion`
  - copy: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending?`
  - tasks_mini: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending? (Filter for this node: Major Spending Category == 'Capital Outlay'; group by County; sum Amount; normalize County to uppercase; rank desc; take top 5.)`

- Node 2 `fact`

```diff
@@ -1,20 +1,23 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 3 `subquestion`
  - copy: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending?`
  - tasks_mini: `In this fiscal year, which Texas counties were in the top 5 for Capital Outlay spending? (Filter for this node: Major Spending Category == 'Capital Outlay'; group by County; sum Amount; normalize County to uppercase; rank desc; take top 5.)`

- Node 3 `fact`

```diff
@@ -1,20 +1,23 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import defaultdict
```

- Node 4 `subquestion`
  - copy: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in hop 1 list.)`

- Node 4 `fact`

```diff
@@ -1,31 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 5 `subquestion`
  - copy: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in hop 1 list.)`

- Node 5 `fact`

```diff
@@ -1,31 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 6 `subquestion`
  - copy: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In this fiscal year, among the counties from hop 1, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in hop 1 list.)`

- Node 6 `fact`

```diff
@@ -1,31 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 7 `subquestion`
  - copy: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2?`
  - tasks_mini: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2? (Filter for this node: County in hop 2 list; normalize County to uppercase; count rows by County.)`

- Node 7 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 8 `subquestion`
  - copy: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2?`
  - tasks_mini: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2? (Filter for this node: County in hop 2 list; normalize County to uppercase; count rows by County.)`

- Node 8 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 9 `subquestion`
  - copy: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2?`
  - tasks_mini: `In this fiscal year, what were the intake counts from the Department of Criminal Justice for the counties from hop 2? (Filter for this node: County in hop 2 list; normalize County to uppercase; count rows by County.)`

- Node 9 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

### `k-3-d-3/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In 2019, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2019, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 1 `fact`

```diff
@@ -1,27 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 2 `subquestion`
  - copy: `In 2020, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2020, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 2 `fact`

```diff
@@ -1,27 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 3 `subquestion`
  - copy: `In 2021, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2021, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 3 `fact`

```diff
@@ -1,27 +1,12 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 4 `subquestion`
  - copy: `In 2019, what were the intake counts from the Department of Criminal Justice for the counties from hop 1?`
  - tasks_mini: `In 2019, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 4 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 5 `subquestion`
  - copy: `In 2020, what were the intake counts from the Department of Criminal Justice for the counties from hop 1?`
  - tasks_mini: `In 2020, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 5 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 6 `subquestion`
  - copy: `In 2021, what were the intake counts from the Department of Criminal Justice for the counties from hop 1?`
  - tasks_mini: `In 2021, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 6 `fact`

```diff
@@ -1,46 +1,11 @@
-import os
-import io
-import pandas as pd
-import boto3
+import csv
+from collections import Counter
```

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The county seat is Houston, which is also the largest city in Texas and the fourth-largest city in the United States.
+Harris County is the most populous county in Texas and the third-most populous in the United States. The county seat is Houston, which is also the largest city in Texas and the fourth-largest city in the United States.
```

### `k-3-d-3/task_6.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 1 `fact`

```diff
@@ -1,23 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+from collections import defaultdict
-source = "datagov/parking-violations-issued-in-january-2019/files/data.txt"
```

- Node 2 `subquestion`
  - copy: `Which agencies were in the top 20 for total January parking-violation fine amount in 2020?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 2 `fact`

```diff
@@ -1,23 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+from collections import defaultdict
-source = "datagov/parking-violations-issued-in-january-2020/files/data.txt"
```

- Node 3 `subquestion`
  - copy: `Which agencies were in the top 20 for total January parking-violation fine amount in 2021?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 3 `fact`

```diff
@@ -1,23 +1,20 @@
-import os
-import io
-import pandas as pd
-import boto3
+from collections import defaultdict
-source = "datagov/parking-violations-issued-in-january-2021/files/data.txt"
```

- Node 4 `subquestion`
  - copy: `What were the January moving-violation counts in 2019 for the U.S. national law-enforcement bodies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 4 `fact`

```diff
@@ -1,42 +1,20 @@
-import os
-import io
-import re
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
```

- Node 5 `subquestion`
  - copy: `What were the January moving-violation counts in 2020 for the U.S. national law-enforcement bodies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 5 `fact`

```diff
@@ -1,42 +1,20 @@
-import os
-import io
-import re
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
```

- Node 6 `subquestion`
  - copy: `What were the January moving-violation counts in 2021 for the U.S. national law-enforcement bodies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 6 `answer`
  - copy: `{"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32}`
  - tasks_mini: `UNITED STATES PARK POLICE`

- Node 6 `fact`

```diff
@@ -1,42 +1,26 @@
-import os
-import io
-import re
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
```

- Node 7 `subquestion`
  - copy: `Which federal agency operates <hop 2 answer>?`
  - tasks_mini: `Which federal agency operates the United States Park Police (from hop 2)?`

### `k-3-d-4/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which DC Ward had the lowest average total crime count across 2018-2021?`
  - tasks_mini: `Which DC Ward had the lowest average total crime count across 2018-2021? (Filter for this node: 2018 file; group by WARD in feature properties; count incidents per ward.)`

- Node 1 `fact`

```diff
@@ -2,12 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-source = 'datagov/crime-incidents-in-2018/files/data.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `subquestion`
  - copy: `Which DC Ward had the lowest average total crime count across 2018-2021?`
  - tasks_mini: `Which DC Ward had the lowest average total crime count across 2018-2021? (Filter for this node: 2019 file; group by WARD in feature properties; count incidents per ward.)`

- Node 2 `fact`

```diff
@@ -2,12 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-source = 'datagov/crime-incidents-in-2019/files/data.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `subquestion`
  - copy: `Which DC Ward had the lowest average total crime count across 2018-2021?`
  - tasks_mini: `Which DC Ward had the lowest average total crime count across 2018-2021? (Filter for this node: 2020 file; group by WARD in feature properties; count incidents per ward.)`

- Node 3 `fact`

```diff
@@ -2,12 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-source = 'datagov/crime-incidents-in-2020/files/data.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `subquestion`
  - copy: `Which DC Ward had the lowest average total crime count across 2018-2021?`
  - tasks_mini: `Which DC Ward had the lowest average total crime count across 2018-2021? (Filter for this node: 2021 file; group by WARD in feature properties; count incidents per ward.)`

- Node 4 `fact`

```diff
@@ -2,12 +2,11 @@
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-source = 'datagov/crime-incidents-in-2021/files/data.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 5 `subquestion`
  - copy: `In Ward 3 (<aggregation of nodes 1-4>), which neighborhoods share the same name with other wards?`
  - tasks_mini: `In the ward with the lowest average total crime count across 2018-2021 (from <aggregation of nodes 1-4>), which neighborhoods listed for that ward shares its name with the area in Maryland? (Lookup: Ward 3 neighborhood list in the Neighborhoods in Washington, D.C. article.)`

- Node 5 `answer`
  - copy: `Chevy Chase`
  - tasks_mini: `Chevy Chase, Friendship Heights`

- Node 6 `source`
  - copy: `wikipedia/Chevy_Chase_(Washington,_D.C.)/content.txt`
  - tasks_mini: `wikipedia/Chevy_Chase,_Maryland/content.txt`

- Node 6 `subquestion`
  - copy: `Which Maryland area borders the Ward 3 neighborhood identified in node 5? (Lookup: Chevy Chase (Washington, D.C.) article line stating it borders Chevy Chase, Maryland.)`
  - tasks_mini: `Which Maryland county contains the area described here? (Lookup: Chevy Chase/Friendship Heights, Maryland article line describing the area in southern Montgomery County.)`

- Node 6 `answer`
  - copy: `Chevy Chase, Maryland`
  - tasks_mini: `Montgomery County, Maryland`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Chevy Chase is a neighborhood in northwest Washington, D.C. It borders Chevy Chase, Maryland.
+Chevy Chase is the colloquial name of an area that includes a town, several incorporated villages, and an unincorporated census-designated place in southern Montgomery County, Maryland; and one adjoining neighborhood in northwest Washington, D.C.
```

- Node 7 `source`
  - copy: `wikipedia/Chevy_Chase,_Maryland/content.txt`
  - tasks_mini: `wikipedia/Montgomery_County,_Maryland/content.txt`

- Node 7 `subquestion`
  - copy: `Which Maryland county contains Chevy Chase, Maryland? (Lookup: Chevy Chase, Maryland article line describing the area in southern Montgomery County.)`
  - tasks_mini: `What is the rank of the average household income for <node_6 answer> among U.S. counties as of 2020?`

- Node 7 `answer`
  - copy: `Montgomery County`
  - tasks_mini: `20`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Chevy Chase is the colloquial name of an area that includes a town, several incorporated villages, and an unincorporated census-designated place in southern Montgomery County, Maryland; and one adjoining neighborhood in northwest Washington, D.C.
+The average household income in Montgomery County is the 20th-highest among U.S. counties as of 2020.
```

### `k-3-d-4/task_10.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -1,14 +1,7 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `fact`

```diff
@@ -1,14 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `fact`

```diff
@@ -1,14 +1,7 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-4/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In 2018, which Texas counties were in the top 5 by average Capital Outlay expenditures?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2018; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 1 `fact`

```diff
@@ -1,21 +1,14 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `subquestion`
  - copy: `In 2019, which Texas counties were in the top 5 by average Capital Outlay expenditures?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2019; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 2 `fact`

```diff
@@ -1,21 +1,14 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `subquestion`
  - copy: `In 2020, which Texas counties were in the top 5 by average Capital Outlay expenditures?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2020; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 3 `fact`

```diff
@@ -1,21 +1,14 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `subquestion`
  - copy: `In 2021, which Texas counties were in the top 5 by average Capital Outlay expenditures?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2021; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 4 `fact`

```diff
@@ -1,21 +1,14 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 5 `subquestion`
  - copy: `In 2019, among the counties from the capital outlay set, which two had the highest average TDCJ releases?`
  - tasks_mini: `Among the counties from the capital outlay set, which two had the highest average TDCJ releases across 2019-2020? (Filter for this node: count rows by County; County normalized to uppercase; restrict to Harris/Dallas/Bexar/Travis/Montgomery.)`

- Node 5 `fact`

```diff
@@ -1,14 +1,11 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 6 `subquestion`
  - copy: `In 2020, among the counties from the capital outlay set, which two had the highest average TDCJ releases?`
  - tasks_mini: `Among the counties from the capital outlay set, which two had the highest average TDCJ releases across 2019-2020? (Filter for this node: count rows by County; County normalized to uppercase; restrict to Harris/Dallas/Bexar/Travis/Montgomery.)`

- Node 6 `fact`

```diff
@@ -1,14 +1,11 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 7 `subquestion`
  - copy: `For the two counties from the releases comparison, what were the disability compensation recipient counts in 2020?`
  - tasks_mini: `For the two counties from the releases comparison, what were the disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name in {Harris, Dallas}; use Total: Disability Compensation Recipients.)`

- Node 7 `fact`

```diff
@@ -1,17 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 8 `subquestion`
  - copy: `For the two counties from the releases comparison, what were the disability compensation recipient counts in 2023?`
  - tasks_mini: `For the two counties from the releases comparison, what were the disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name in {Harris, Dallas}; use Total: Disability Compensation Recipients.)`

- Node 8 `fact`

```diff
@@ -1,17 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-4/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in the 2018-19 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 1 `fact`

```diff
@@ -1,26 +1,10 @@
-import io
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/report-card-enrollment-2018-19-school-year/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 2 `subquestion`
  - copy: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in the 2019-20 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 2 `fact`

```diff
@@ -1,26 +1,10 @@
-import io
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/report-card-enrollment-2019-20-school-year/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 3 `subquestion`
  - copy: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in the 2020-21 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 3 `fact`

```diff
@@ -1,26 +1,10 @@
-import io
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/report-card-enrollment-2020-21-school-year/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 4 `subquestion`
  - copy: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in the 2021-22 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 4 `fact`

```diff
@@ -1,26 +1,10 @@
-import io
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/report-card-enrollment-2021-22-school-year/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 5 `subquestion`
  - copy: `Among {King, Kitsap, San Juan, Whitman} (from hop 1), which counties had district-average Math proficiency above 40% in 2021-22?`
  - tasks_mini: `Among {King, Kitsap, San Juan, Whitman} (from hop 1), which counties had district-average Math proficiency above 40% in 2021-22? (Filter: OrganizationLevel=District; StudentGroup=All Students; GradeLevel=All Grades; TestSubject=Math; compute unweighted mean of PercentMetStandard by County; keep >40%.)`

- Node 5 `fact`

```diff
@@ -1,26 +1,11 @@
-import io
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/report-card-assessment-data-2021-22-school-year/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 7 `subquestion`
  - copy: `What was Kitsap County's 2020 census population?`
  - tasks_mini: `Among {Kitsap, Whitman} (from hop 2), which county had the lower 2020 census population?`

- Node 8 `subquestion`
  - copy: `What was Whitman County's 2020 census population?`
  - tasks_mini: `Among {Kitsap, Whitman} (from hop 2), which county had the lower 2020 census population?`

- Node 8 `answer`
  - copy: `Whitman had population 47,973`
  - tasks_mini: `Whitman had population 47,973 (lower than Kitsap's 275,611), county seat is Colfax`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-According to the Wikipedia article for Whitman County, Washington, 'As of the 2020 census, the population was 47,973.'
+According to the Wikipedia article for Whitman County, Washington, 'As of the 2020 census, the population was 47,973.' Also, 'The county seat is Colfax.'
```

### `k-3-d-4/task_4.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -2,26 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `fact`

```diff
@@ -2,25 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `fact`

```diff
@@ -2,25 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/school-district-office-locations-2022-23/files/data-8V0eVK.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `fact`

```diff
@@ -2,35 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/postsecondary-school-locations-2022-23/files/data-sh56Ar.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_1_answer = "Los Angeles County; San Diego County; Orange County"
```

- Node 5 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Los Angeles County"
```

- Node 6 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Los Angeles County"
```

- Node 7 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Los Angeles County"
```

- Node 8 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/postsecondary-school-locations-current-5a74c/files/Postsecondary_School_Locations_Current_-3631565628879840217.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Los Angeles County"
```

### `k-3-d-4/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NYC senior high schools were in the top 3 by total VADIR incidents in 2010-11?`
  - tasks_mini: `Which NYC high schools were in the top 3 by total VADIR incidents in 2010-11?`

- Node 1 `answer`
  - copy: `["Herbert H Lehman High School", "Susan E. Wagner High School", "Automotive High School"]`
  - tasks_mini: `["Herbert H Lehman High School", "Jhs 13 Jackie Robinson", "Susan E. Wagner High School"]`

- Node 1 `fact`

```diff
@@ -1,19 +1,22 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `subquestion`
  - copy: `Which NYC senior high schools were in the top 3 by total VADIR incidents in 2011-12?`
  - tasks_mini: `Which NYC high schools were in the top 3 by total VADIR incidents in 2011-12?`

- Node 2 `fact`

```diff
@@ -1,19 +1,22 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `subquestion`
  - copy: `Which NYC senior high schools were in the top 3 by total VADIR incidents in 2012-13?`
  - tasks_mini: `Which NYC high schools were in the top 3 by total VADIR incidents in 2012-13?`

- Node 3 `answer`
  - copy: `["Susan E. Wagner High School", "Herbert H Lehman High School", "Sheepshead Bay High School"]`
  - tasks_mini: `["Brooklyn Secondary School for Collaborative Studies", "Susan E. Wagner High School", "Herbert H Lehman High School"]`

- Node 3 `fact`

```diff
@@ -1,19 +1,22 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `subquestion`
  - copy: `Which NYC senior high schools were in the top 3 by total VADIR incidents in 2013-14?`
  - tasks_mini: `Which NYC high schools were in the top 3 by total VADIR incidents in 2013-14?`

- Node 4 `answer`
  - copy: `["Susan E. Wagner High School", "Richmond Hill High School", "Clara Barton High School"]`
  - tasks_mini: `["Susan E. Wagner High School", "Richmond Hill High School", "Acad For College Prep & Career Exploration"]`

- Node 4 `fact`

```diff
@@ -1,19 +1,22 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 6 `source`
  - copy: `wikipedia/Brooklyn_Bridge/content.txt`
  - tasks_mini: `wikipedia/List_of_bridges_and_tunnels_in_New_York_City/content.txt`

- Node 6 `subquestion`
  - copy: `Which NYC bridge is described as a cable-stayed suspension bridge spanning the East River between Manhattan and Brooklyn?`
  - tasks_mini: `Which bridges in NYC are suspension bridges?`

- Node 6 `answer`
  - copy: `Brooklyn Bridge`
  - tasks_mini: `["Brooklyn Bridge", "Williamsburg Bridge", "George Washington Bridge", "Verrazzano-Narrows Bridge", "Triborough Bridge (Suspension Span)"]`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The Brooklyn Bridge is a cable-stayed suspension bridge in New York City, spanning the East River between the boroughs of Manhattan and Brooklyn.
+The suspension bridges in NYC include the Brooklyn Bridge (1883), Williamsburg Bridge (1903), Manhattan Bridge (1909), George Washington Bridge (1931), Bronx-Whitestone Bridge (1939), Throgs Neck Bridge (1961), and Verrazzano-Narrows Bridge (1964).
```

- Node 7 `source`
  - copy: `wikipedia/Manhattan_Bridge/content.txt`
  - tasks_mini: `wikipedia/Staten_Island/content.txt`

- Node 7 `subquestion`
  - copy: `Which NYC bridge is described as a suspension bridge crossing the East River between Lower Manhattan and Downtown Brooklyn?`
  - tasks_mini: `Which bridges connect to <node_5 answer>?`

- Node 7 `answer`
  - copy: `Manhattan Bridge`
  - tasks_mini: `["Verrazzano-Narrows Bridge", "Outerbridge Crossing", "Goethals Bridge", "Bayonne Bridge"]`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The Manhattan Bridge is a suspension bridge that crosses the East River in New York City, connecting Lower Manhattan at Canal Street with Downtown Brooklyn at the Flatbush Avenue Extension.
+Motor traffic can reach Staten Island from Brooklyn by the Verrazzano-Narrows Bridge and from New Jersey by the Outerbridge Crossing, Goethals Bridge and Bayonne Bridge.
```

### `k-3-d-4/task_6.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -2,24 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/public-school-locations-2018-19-42360/files/data-F2nGlG.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `fact`

```diff
@@ -2,24 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/private-school-locations-2017-18-f49f6/files/data-dqdQDP.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `fact`

```diff
@@ -2,24 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/school-district-office-locations-2020-21-d8df0/files/data-UDaCeM.txt"
-bucket = "lakeqa-yc4103-datalake"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `fact`

```diff
@@ -2,32 +2,12 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/postsecondary-school-locations-2019-20-64b31/files/data-cbxYz6.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_1_answer = "Polk County; Linn County; Scott County"
```

- Node 5 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/public-school-locations-2018-19-42360/files/data-F2nGlG.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Polk County"
```

- Node 6 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/private-school-locations-2017-18-f49f6/files/data-dqdQDP.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Polk County"
```

- Node 7 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/school-district-office-locations-current-c8f9d/files/data-ghDEVP.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Polk County"
```

- Node 8 `fact`

```diff
@@ -2,17 +2,10 @@
-import boto3
-from botocore.config import Config
-from botocore import UNSIGNED
-source = "datagov/postsecondary-school-locations-2017-18-fa280/files/data-7AG3Nw.txt"
-bucket = "lakeqa-yc4103-datalake"
-node_4_answer = "Polk County"
```

### `k-3-d-4/task_7.json`
- Impact: major
- Node 1 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 1 `fact`

```diff
@@ -1,18 +1,12 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 2 `fact`

```diff
@@ -1,18 +1,12 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 3 `fact`

```diff
@@ -1,18 +1,12 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 4 `fact`

```diff
@@ -1,18 +1,12 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 5 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2_3_4"]`

- Node 5 `fact`

```diff
@@ -1,12 +1,6 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 6 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

- Node 6 `subquestion`
  - copy: `Which notable museums are in <node_5 answer: Upper West Side>?`
  - tasks_mini: `What are some notable structures that is a museum in <node_5 answer: Upper West Side>?`

- Node 6 `answer`
  - copy: `["American Folk Art Museum", "American Museum of Natural History", "Children's Museum of Manhattan", "New-York Historical Society", "Nicholas Roerich Museum"]`
  - tasks_mini: `["American Museum of Natural History", "Lincoln Center for the Performing Arts"]`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Cultural institutions in the Upper West Side include the American Folk Art Museum, the American Museum of Natural History, the Children's Museum of Manhattan, the New-York Historical Society, and the Nicholas Roerich Museum.
+The Upper West Side is considered one of Manhattan's cultural and intellectual hubs, with the American Museum of Natural History located near its center, and Lincoln Center for the Performing Arts at its south end.
```

- Node 7 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

- Node 7 `source`
  - copy: `wikipedia/American_Folk_Art_Museum/content.txt`
  - tasks_mini: `wikipedia/Central_Park/content.txt`

- Node 7 `subquestion`
  - copy: `In what year did the American Folk Art Museum receive its provisional charter?`
  - tasks_mini: `Which museums are located adjacent to Central Park?`

- Node 7 `answer`
  - copy: `1961`
  - tasks_mini: `["American Museum of Natural History", "Metropolitan Museum of Art"]`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Since receiving a provisional charter in 1961, the American Folk Art Museum has continually expanded its mission and purview.
+Manhattan Square on the west side was reserved for the American Museum of Natural History, while a corresponding area on the East Side became the Metropolitan Museum of Art. Both museums are major cultural institutions adjacent to Central Park.
```

- Node 8 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_6_7"]`

- Node 8 `subquestion`
  - copy: `In what year was the American Museum of Natural History created?`
  - tasks_mini: `In what year was <intersection of node_6, node_7: American Museum of Natural History> established?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-The legislation creating the American Museum of Natural History was signed by Governor John Thompson Hoffman on April 6, 1869.
+The American Museum of Natural History (AMNH) is a natural history museum on the Upper West Side of Manhattan in New York City. Located in Theodore Roosevelt Park, across the street from Central Park, the museum complex comprises 21 interconnected buildings. The legislation creating the museum was signed by Governor John Thompson Hoffman on April 6, 1869.
```

### `k-3-d-4/task_8.json`
- Impact: major
- Node 1 `answer`
  - copy: `["P.S. 005 Ellen Lurie", "P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 048 P.O. Michael J. Buczek", "P.S. 128 Audubon", "P.S. 152 Dyckman Valley", "P.S. 153 Adam Clayton Powell", "P.S. 192 Jacob H. Schiff"]`
  - tasks_mini: `["P.S. 005 ELLEN LURIE", "P.S. 008 LUIS BELLIARD", "P.S. 028 WRIGHT BROTHERS", "P.S. 048 P.O. MICHAEL J. BUCZEK", "P.S. 128 AUDUBON", "P.S. 152 DYCKMAN VALLEY", "P.S. 153 ADAM CLAYTON POWELL", "P.S. 192 JACOB H. SCHIFF"]`

- Node 1 `fact`

```diff
@@ -1,37 +1,7 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `answer`
  - copy: `["Hamilton Heights School", "Muscota", "P.S. 004 Duke Ellington", "P.S. 005 Ellen Lurie", "P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 048 P.O. Michael J. Buczek", "P.S. 098 Shorac Kappock", "P.S. 115 Alexander Humboldt", "P.S. 128 Audubon", "P.S. 132 Juan Pablo Duarte", "P.S. 152 Dyckman Valley", "P.S. 153 Adam Clayton Powell", "P.S. 173", "...`
  - tasks_mini: `["P.S. 153 Adam Clayton Powell", "..."]`

- Node 2 `fact`

```diff
@@ -1,46 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 3 `answer`
  - copy: `["P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 153 Adam Clayton Powell", "P.S. 189"]`
  - tasks_mini: `["P.S. 153 Adam Clayton Powell", "..."]`

- Node 3 `fact`

```diff
@@ -1,33 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 4 `answer`
  - copy: `["Hamilton Heights School", "P.S. 048 P.O. Michael J. Buczek", "P.S. 153 Adam Clayton Powell", "P.S. 189"]`
  - tasks_mini: `["P.S. 153 Adam Clayton Powell", "..."]`

- Node 4 `fact`

```diff
@@ -1,33 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

### `k-3-d-4/task_9.json`
- Impact: major
- Node 4 `answer`
  - copy: `["Alabama", "Arizona", "Louisiana", "Missouri", "Oregon", "South Carolina", "Tennessee", "Virginia", "Washington"]`
  - tasks_mini: `["Arizona", "Alabama", "Louisiana", "Tennessee", "Missouri", "Oregon", "South Carolina", "Virginia", "Washington", "Puerto Rico"]`

- Node 4 `fact`

```diff
@@ -1,28 +1,8 @@
-import io
-import boto3
-from botocore import UNSIGNED
-from botocore.client import Config
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 5 `fact`

```diff
@@ -1 +1,8 @@
-In FY 2023, Maricopa County, Arizona had 69,974 VA disability compensation recipients, the most of any county in Arizona. Pima County was second with 25,745, and Pinal County was third with 10,403.
+import pandas as pd
+
+source = 'datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt'
+df = pd.read_csv(source)
+df['Total: Disability Compensation Recipients'] = pd.to_numeric(df['Total: Disability Compensation Recipients'], errors='coerce')
```

### `k-3-d-5/task_1.json`
- Impact: major
- Node 1 `answer`
  - copy: `["MANHATTAN BRIDGES HIGH SCHOOL", "BEDFORD ACADEMY HIGH SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL FOR CONTEMPORARY ARTS", "BRONX AEROSPACE HIGH SCHOOL", "ELEANOR ROOSEVELT HIGH SCHOOL", "BRONX ACADEMY OF LETTERS", "NEW EXPLORATIONS INTO SCIENCE, TECHNOLOGY AND MATH"]`
  - tasks_mini: `["Manhattan Bridges High School", "Bedford Academy High School", "Marble Hill High School for International Studies", "High School for Contemporary Arts", "Bronx Aerospace High School", "Eleanor Roosevelt High School", "Bronx Academy of Letters"]`

- Node 1 `fact`

```diff
@@ -1,17 +1,27 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
+import csv
```

- Node 2 `answer`
  - copy: `["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATHEMATICS", "HIGH SCHOOL FOR CONTEMPORARY ARTS", "BEDFORD ACADEMY HIGH SCHOOL", "MANHATTAN BRIDGES HIGH SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "NEW WORLD HIGH SCHOOL", "BRONX AEROSPACE HIGH SCHOOL"]`
  - tasks_mini: `["Brooklyn International High School", "Gregorio Luperon High School", "High School for Contemporary Arts", "Bedford Academy High School", "Manhattan Bridges High School", "Marble Hill High School for International Studies", "New World High School"]`

- Node 2 `fact`

```diff
@@ -1,17 +1,27 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
+import csv
```

- Node 3 `answer`
  - copy: `["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PREPARATORY SCHOOL", "SOUTH BRONX PREPARATORY: A COLLEGE BOARD SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL FOR VIOLIN AND DANCE", "ESSEX STREET ACADEMY", "BELMONT PREPARATORY HIGH SCHOOL"]`
  - tasks_mini: `["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Preparatory School", "South Bronx Preparatory", "Marble Hill High School for International Studies", "High School for Violin and Dance", "Essex Street Academy"]`

- Node 3 `fact`

```diff
@@ -1,17 +1,27 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
+import csv
```

- Node 4 `answer`
  - copy: `["Theatre Arts Production Company School", "Brooklyn International High School at Water's Edge", "Williamsburg Preparatory School", "Marble Hill High School for International Studies", "Williamsburg High School for Architecture and Design", "Manhattan Village Academy", "High School for Violin and Dance", "Manhattan Bridges High School"]`
  - tasks_mini: `["Theatre Arts Production Company School", "Brooklyn International High School", "Williamsburg Preparatory School", "Marble Hill High School for International Studies", "Williamsburg High School for Architecture and Design", "Manhattan Village Academy", "High School for Violin and Dance"]`

- Node 4 `fact`

```diff
@@ -1,17 +1,27 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
+import csv
```

- Node 5 `answer`
  - copy: `["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village Academy", "Williamsburg High School for Architecture and Design", "Manhattan Bridges High School", "Academy of Finance and Enterprise", "Urban Assembly School for Media Studies, The", "Marble Hill High School for International Studies"]`
  - tasks_mini: `["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village Academy", "Williamsburg High School for Architecture and Design", "Manhattan Bridges High School", "Academy of Finance and Enterprise", "Marble Hill High School for International Studies"]`

- Node 5 `fact`

```diff
@@ -1,17 +1,27 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
+import csv
```

- Node 6 `source`
  - copy: `wikipedia/John_F._Kennedy_High_School_(New_York_City)/content.txt`
  - tasks_mini: `wikipedia/Marble_Hill,_Manhattan/content.txt`

- Node 6 `subquestion`
  - copy: `Which neighborhoods are <intersection of node_1, node_2, node_3, node_4, node_5> located in?`
  - tasks_mini: `Who built the first bridge at <intersection of node_1, node_2, node_3, node_4, node_5> neighborhood in 1693?`

- Node 6 `answer`
  - copy: `["Spuyten Duyvil", "Marble Hill"]`
  - tasks_mini: `Frederick Philipse`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-John F. Kennedy Educational Campus houses Marble Hill High School for International Studies among its co-located schools. The campus is located at 99 Terrace View Avenue, on the border of the Spuyten Duyvil neighborhood of the Bronx and the Marble Hill neighborhood of Manhattan.
+King's Bridge was built in 1693 by Frederick Philipse, a Frisian-born merchant. It was the first bridge connecting New York City to the mainland, located near Marble Hill at what is now West 230th Street.
```

- Node 7 `source`
  - copy: `wikipedia/Spuyten_Duyvil,_Bronx/content.txt`
  - tasks_mini: `wikipedia/Frederick_Philipse/content.txt`

- Node 7 `subquestion`
  - copy: `What is the earliest bridge connecting the neighborhoods in <node_6 answer> to NYC?`
  - tasks_mini: `From which area of the Netherlands did <node_6 answer> emigrate?`

- Node 7 `answer`
  - copy: `King's Bridge`
  - tasks_mini: `Friesland`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-In the late 17th century, Frederick Philipse received permission to construct a bridge across Spuyten Duyvil Creek and charge tolls. King's Bridge, located roughly south of and parallel to where West 230th Street lies today, later opened there.
+Frederick Philipse (1626-1702) was a Dutch-American merchant who emigrated from Friesland in the Netherlands. He became one of the wealthiest men in colonial New York.
```

### `k-4-d-1/task_2.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `In 2019 arrest data, which Area Name has the most arrests where Charge Group Description is "Homicide"?`
  - tasks_mini: `In <node_1 answer> arrest data, which area has the most Homicide arrests?`

### `k-4-d-1/task_3.json`
- Impact: major
- Node 3 `subquestion`
  - copy: `In 2021, within borough <node_1 answer> and precinct <node_2 answer>, which non-null location-position category was most common in NYPD complaint incidents?`
  - tasks_mini: `In the 2021 NYPD complaint data, within borough <node_1 answer> and precinct <node_2 answer>, which non-null location description (LOC_OF_OCCUR_DESC) is most common?`

- Node 4 `subquestion`
  - copy: `In 2022, within borough <node_1 answer>, how many NYPD shooting incidents occurred in the location-position category from node 3?`
  - tasks_mini: `In the 2022 NYPD shooting incident data, within borough <node_1 answer>, how many shooting incidents occurred with LOC_OF_OCCUR_DESC = <node_3 answer>?`

### `k-4-d-1/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NASA facility developed the system used to survey Assateague Island National Seashore in the 2010 USGS survey?`
  - tasks_mini: `What system was used to survey Assateague Island National Seashore in the 2010 USGS survey?`

- Node 1 `answer`
  - copy: `Wallops Flight Facility`
  - tasks_mini: `EAARL (Experimental Advanced Airborne Research Lidar)`

- Node 1 `fact`

```diff
@@ -1 +1,57 @@
-Elevation measurements were collected over Assateague Island National Seashore on March 19 and 24, 2010, using the Experimental Advanced Airborne Research Lidar (EAARL), a pulsed laser ranging system mounted onboard an aircraft. The EAARL, developed originally by the National Aeronautics and Space Administration (NASA) at Wallops Flight Facility in Virginia, measures ground elevation with a vertical resolution of +/-15 centimeters.
+import os
+import re
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
```

- Node 2 `source`
  - copy: `wikipedia/Wallops_Flight_Facility/content.txt`
  - tasks_mini: `datagov/eaarl-coastal-topography-assateague-island-national-seashore-maryland-and-virginia-2010/files/USGS.b40f54c8-02fd-4152-8883-b7131059f8af.txt`

- Node 2 `subquestion`
  - copy: `In which Virginia county is <node_1 answer> located?`
  - tasks_mini: `At which NASA facility was <node_1 answer> developed?`

- Node 2 `answer`
  - copy: `Accomack County`
  - tasks_mini: `Wallops Flight Facility`

- Node 2 `fact`

```diff
@@ -1 +1,77 @@
-Wallops Flight Facility is a NASA rocket launch site on Wallops Island on the Eastern Shore of Virginia, located in Accomack County.
+import os
+import re
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
```

- Node 3 `source`
  - copy: `wikipedia/Accomack_County,_Virginia/content.txt`
  - tasks_mini: `wikipedia/Wallops_Flight_Facility/content.txt`

- Node 3 `subquestion`
  - copy: `What is the largest town in <node_2 answer>?`
  - tasks_mini: `In which Virginia county is <node_2 answer> located?`

- Node 3 `answer`
  - copy: `Chincoteague`
  - tasks_mini: `Accomack County`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Accomack County is a county on the Eastern Shore of Virginia. The town of Accomac serves as the county seat, while Chincoteague is the largest town in the county.
+Wallops Flight Facility is a NASA rocket launch site on Wallops Island on the Eastern Shore of Virginia, located in Accomack County.
```

### `k-4-d-1/task_6.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which airport most directly serves Pittsburgh for commercial passenger travel?`
  - tasks_mini: `What is the largest airport in Pittsburgh?`

- Node 1 `fact`

```diff
@@ -1 +1 @@
-Pittsburgh International Airport provides commercial passenger service from over 15 airlines to the Pittsburgh metropolitan area. Arnold Palmer Regional Airport also provides limited commercial passenger service and is east of Pittsburgh.
+Pittsburgh International Airport is the largest airport in Pittsburgh.
```

- Node 2 `subquestion`
  - copy: `For <hop 1 answer>, which destination had the most scheduled seats in March 2019?`
  - tasks_mini: `For Pittsburgh International Airport, which destination had the most scheduled seats in March 2019? (Filter for this node: group by Destination Code; sum Seats March 2019; select max.)`

- Node 2 `fact`

```diff
@@ -1 +1,22 @@
-In the March 2019 Pittsburgh International scheduled traffic report, Atlanta (ATL) has 44,912 total seats, the highest of any destination (next highest is Chicago O'Hare with 35,699).
+import csv
+from collections import defaultdict
+
+with open('datagov/pittsburgh-international-airport-scheduled-passenger-traffic/files/pittsburgh-international-traffic-report-march-2019.txt', 'r', encoding='utf-8', newline='') as f:
+    rows = list(csv.DictReader(f))
```

- Node 3 `subquestion`
  - copy: `In the airports dataset, what city and state correspond to <hop 2 answer>?`
  - tasks_mini: `In the airports dataset, what city and state correspond to the destination airport code from hop 2? (Filter for this node: Loc_Id == <destination code from hop 2>; read City and State_Post.)`

- Node 3 `fact`

```diff
@@ -1 +1,12 @@
-In the airports dataset, the entry with Loc_Id ATL lists City ATLANTA and State_Post GA (Hartsfield - Jackson Atlanta Intl).
+import csv
+
+with open('datagov/airports-5e97a/files/rows.txt', 'r', encoding='utf-8', newline='') as f:
+    rows = list(csv.DictReader(f))
+
```

- Node 4 `subquestion`
  - copy: `In the ZIP code boundaries dataset, what is the largest land area in square miles among ZIP codes in <hop 3 answer>?`
  - tasks_mini: `In the ZIP code boundaries dataset, what is the largest land area (SQMI) among ZIP codes in the city and state from hop 3? (Filter for this node: CITY == Atlanta; STATE == GA; rank by SQMI; return max SQMI.)`

- Node 4 `fact`

```diff
@@ -1 +1,18 @@
-In the boundaries-us-zip-codes dataset, among ZIP codes with CITY = Atlanta and STATE = GA, ZIP 30349 has the largest land area (SQMI 45.68).
+import csv
+
+with open('datagov/boundaries-us-zip-codes/files/rows.txt', 'r', encoding='utf-8', newline='') as f:
+    rows = list(csv.DictReader(f))
+
```

### `k-4-d-2/task_1.json`
- Impact: major
- Node 3 `subquestion`
  - copy: `Which schools in <hop 1 answer> had an A grade in the 2010-11 Progress Report?`
  - tasks_mini: `Which schools from <intersection of node_1, node_2> had an A grade in the 2010-11 Progress Report?`

- Node 4 `subquestion`
  - copy: `What is the ZIP code of <hop 2 answer>?`
  - tasks_mini: `What is the ZIP code of <node_3 answer>?`

- Node 4 `fact`

```diff
@@ -38 +38,2 @@
+answer = str(answer)
```

- Node 5 `subquestion`
  - copy: `What percentage does White people contribute to the racial makeup of the neighborhood whose primary ZIP code is <hop 3 answer> based on data in 2010 census?`
  - tasks_mini: `What percentage does White people contribute to the racial makeup of the neighborhood whose primary ZIP code is <node_4 answer> based on data in 2010 census?`

### `k-4-d-2/task_10.json`
- Impact: moderate
- Node 1 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 1 `fact`

```diff
@@ -18 +18,9 @@
+name_map = {
+    "ELEANOR ROOSEVELT HIGH SCHOOL": "Eleanor Roosevelt High School",
+    "YOUNG WOMEN'S LEADERSHIP SCHOOL": "Young Women's Leadership School",
+    "HIGH SCHOOL OF AMERICAN STUDIES AT LEHMAN COLLEGE": "High School of American Studies at Lehman College",
+    "TOWNSEND HARRIS HIGH SCHOOL": "Townsend Harris High School",
+    "SCHOLARS' ACADEMY": "Scholars' Academy",
```

- Node 2 `depends_on`
  - copy: ``
  - tasks_mini: `["node_1"]`

- Node 2 `fact`

```diff
@@ -18 +18,10 @@
+name_map = {
+    "BARUCH COLLEGE CAMPUS HIGH SCHOOL": "Baruch College Campus High School",
+    "ELEANOR ROOSEVELT HIGH SCHOOL": "Eleanor Roosevelt High School",
+    "BROOKLYN COLLEGE ACADEMY": "Brooklyn College Academy",
+    "TOWNSEND HARRIS HIGH SCHOOL": "Townsend Harris High School",
+    "SCHOLARS' ACADEMY": "Scholars' Academy",
```

- Node 3 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2"]`

- Node 4 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2"]`

- Node 5 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_3_4"]`

- Node 6 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

### `k-4-d-2/task_11.json`
- Impact: major
- Node 1 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 1 `fact`

```diff
@@ -17,2 +17,3 @@
+answer = [f"{county} County" for county in answer]
```

- Node 2 `depends_on`
  - copy: ``
  - tasks_mini: `["node_1"]`

- Node 2 `subquestion`
  - copy: `Which of <node_1 answer> had total state payments for homeowners' school taxes greater than $100 million in 2015?`
  - tasks_mini: `Which of <node_1 answer> had STAR tax relief reimbursement greater than $100 million in 2015?`

- Node 2 `fact`

```diff
@@ -16,5 +16,6 @@
-    & (df["Total Amount of Reimbursement "] > 100000000),
+    & (df["Total Amount of Reimbursement"] > 100000000),
+answer = [f"{county} County" for county in answer]
```

- Node 3 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2"]`

- Node 3 `fact`

```diff
@@ -21,3 +21,3 @@
-answer = [county for county, total in county_totals.items() if total < 1200]
+answer = [f"{county} County" for county, total in county_totals.items() if total < 1200]
```

- Node 4 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2"]`

- Node 4 `fact`

```diff
@@ -23,3 +23,3 @@
-answer = county_totals.loc[county_totals["Total Incidents"] > 20, "County"].tolist()
+answer = [f"{county} County" for county in county_totals.loc[county_totals["Total Incidents"] > 20, "County"].tolist()]
```

- Node 5 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_3_4"]`

- Node 6 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

### `k-4-d-2/task_12.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `Which New York counties had more than 100 youth sent to jail in 2015?`
  - tasks_mini: `Which New York counties had more than 100 secure or mixed juvenile detention admissions in 2015?`

- Node 2 `fact`

```diff
@@ -11,3 +11,3 @@
-df[" Year "] = pd.to_numeric(df[" Year "], errors="coerce")
+df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
@@ -16,3 +16,3 @@
-        (df[" Year "] == 2015)
+        (df["Year"] == 2015)
```

- Node 3 `subquestion`
  - copy: `From <intersection of node_1, node_2>, which counties received between $60 million and $90 million in total state payments for homeowners' school taxes in 2023?`
  - tasks_mini: `From <intersection of node_1, node_2>, which counties received between $60 million and $90 million in total STAR tax relief reimbursement in 2023?`

- Node 3 `fact`

```diff
@@ -12,3 +12,3 @@
-df["Total Amount of Reimbursement "] = pd.to_numeric(df["Total Amount of Reimbursement "], errors="coerce")
+df["Total Amount of Reimbursement"] = pd.to_numeric(df["Total Amount of Reimbursement"], errors="coerce")
@@ -17,4 +17,4 @@
-        & (df["Total Amount of Reimbursement "] >= 60000000)
-        & (df["Total Amount of Reimbursement "] <= 90000000),
+        & (df["Total Amount of Reimbursement"] >= 60000000)
+        & (df["Total Amount of Reimbursement"] <= 90000000),
```

### `k-4-d-2/task_13.json`
- Impact: moderate
- Node 3 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_14.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Chicago city departments had 2018 budgets between $400 million and $700 million?`
  - tasks_mini: `Which Chicago city department had a budget between $400 million and $700 million in 2018 AND between $600 million and $700 million in 2019? (Filter for this node: group by DEPARTMENT DESCRIPTION; sum 2018 ORDINANCE (AMOUNT $); keep totals between 400000000 and 700000000.)`

- Node 1 `fact`

```diff
@@ -1 +1,20 @@
-In the 2018 Chicago Budget Ordinance totals by department, CFD ($642,620,615) and CDOT ($459,129,158) are the only departments with total appropriations between $400 million and $700 million.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 2 `subquestion`
  - copy: `Which Chicago city departments had 2019 budgets between $600 million and $700 million?`
  - tasks_mini: `Which Chicago city department had a budget between $400 million and $700 million in 2018 AND between $600 million and $700 million in 2019? (Filter for this node: group by DEPARTMENT DESCRIPTION; sum 2019 ORDINANCE (AMOUNT $); keep totals between 600000000 and 700000000.)`

- Node 2 `fact`

```diff
@@ -1 +1,20 @@
-In the 2019 Chicago Budget Ordinance totals by department, CFD ($652,282,316) and DFSS ($633,571,744) are the only departments with total appropriations between $600 million and $700 million.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 3 `subquestion`
  - copy: `On what date was <hop 1 answer> organized as a paid department?`
  - tasks_mini: `Which fire department became a paid professional department later, the department identified in hop 1 (from hop 1) or the Pittsburgh Bureau of Fire?`

- Node 4 `subquestion`
  - copy: `On what date did the Pittsburgh Bureau of Fire become a fully paid department?`
  - tasks_mini: `Which fire department became a paid professional department later, the department identified in hop 1 (from hop 1) or the Pittsburgh Bureau of Fire?`

- Node 5 `subquestion`
  - copy: `Which airport most directly serves <hop 2 answer> for commercial passenger travel?`
  - tasks_mini: `What is the largest airport in the city from hop 2 (from hop 2)?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Pittsburgh International Airport provides commercial passenger service from over 15 airlines to the Pittsburgh metropolitan area. Arnold Palmer Regional Airport also provides limited commercial passenger service and is east of Pittsburgh.
+Pittsburgh International Airport is the largest airport in Pittsburgh.
```

- Node 6 `subquestion`
  - copy: `For <hop 3 answer>, how many total seats did the top destination have in March 2019?`
  - tasks_mini: `For the airport identified in hop 3 (from hop 3), how many total scheduled seats did the top destination have in March 2019? (Filter for this node: group by Destination Code; sum Seats March 2019; select max; return seats.)`

- Node 6 `fact`

```diff
@@ -1 +1,12 @@
-In the March 2019 Pittsburgh International scheduled traffic report, Atlanta (ATL) has 44,912 total seats, the highest of any destination (next highest is Chicago O'Hare with 35,699).
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

### `k-4-d-2/task_15.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1,4 +1 @@
-Spokane
- Stevens
- Walla Walla
- Whitman
+The Eastern Washington article lists Whitman and Spokane among the counties in Eastern Washington.
```

- Node 2 `subquestion`
  - copy: `Does Whitman County border Idaho, and what was its 2020 census population?`
  - tasks_mini: `Among counties from <hop 1 answer: Whitman, Spokane>, which county borders Idaho AND has 2020 census population under 300,000?`

- Node 2 `answer`
  - copy: `Whitman County borders Idaho and had a 2020 population of 47,973, so it meets both criteria.`
  - tasks_mini: `Whitman County: borders Idaho (YES, per adjacent counties list), population 47,973 (YES, under 300,000) → MEETS BOTH CRITERIA`

- Node 2 `fact`

```diff
@@ -1,14 +1 @@
-Whitman County is a county located in the U.S. state of Washington. As of the 2020 census, the population was 47,973. The county seat is Colfax, and its largest city is Pullman.
-
-Adjacent counties
-
-Spokane County - north
-Benewah County, Idaho - northeast
```

- Node 3 `subquestion`
  - copy: `Does Spokane County border Idaho, and what was its 2020 census population?`
  - tasks_mini: `Among counties from <hop 1 answer: Whitman, Spokane>, which county borders Idaho AND has 2020 census population under 300,000?`

- Node 3 `answer`
  - copy: `Spokane County borders Idaho, but its 2020 population was 539,339, so it does not meet both criteria.`
  - tasks_mini: `Spokane County: borders Idaho (YES, per adjacent counties list), population 539,339 (NO, exceeds 300,000) → DOES NOT MEET BOTH CRITERIA`

- Node 3 `fact`

```diff
@@ -1,11 +1 @@
-Spokane County is a county located in the U.S. state of Washington. As of the 2020 census, its population was 539,339, and was estimated to be 555,947 in 2024, making it the fourth-most populous county in Washington. The county seat and largest city is Spokane, the second largest city in the state after Seattle. The county is named after the Spokane people.
-
-Adjacent counties
-
- Stevens County – northwest
- Pend Oreille County – north
```

- Node 4 `subquestion`
  - copy: `What is the most populous city in <hop 2 answer> according to the 2020 census?`
  - tasks_mini: `What is the most populous city in <hop 2 answer: Whitman County> according to the 2020 census, located in southeastern Washington within the Palouse region of the Pacific Northwest?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Pullman is the most populous city in Whitman County, located in southeastern Washington within the Palouse region of the Pacific Northwest. The population was 32,901 at the 2020 census
+According to the Wikipedia article for Pullman, Washington, Pullman is the most populous city in Whitman County as of the 2020 census and is located in southeastern Washington within the Palouse region of the Pacific Northwest.
```

- Node 5 `subquestion`
  - copy: `What was the total enrollment for the school district serving <hop 3 answer> in 2017-18?`
  - tasks_mini: `What is the 2017-18 total student enrollment for the school district in <hop 3 answer: Pullman>? (Filter: OrganizationLevel=District; DistrictName=Pullman School District; GradeLevel=All Grades; column=All Students.)`

- Node 5 `fact`

```diff
@@ -19 +19,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_2.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -21 +21,2 @@
+answer = str(answer)
```

- Node 3 `fact`

```diff
@@ -15 +15,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -19 +19,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_3.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1 +1 @@
-In 1960, the municipal government created a five-member police board charged with nominating a superintendent to be the chief authority over police officers, drafting and adopting rules and regulations governing the police system, submitting budget requests to the city council, and hearing and deciding disciplinary cases involving police officers. Criminologist O. W. Wilson was brought on as Superintendent of Police, and served until 1967 when he retired.
+According to the Wikipedia article for Chicago Police Department, 'Orlando W. Wilson, the first civilian superintendent, was appointed by the mayor in 1960.' Wilson served as Superintendent of Police until 1967.
```

- Node 2 `subquestion`
  - copy: `In which cities did <hop 1 answer> serve as police chief before coming to Chicago?`
  - tasks_mini: `In which cities did <node_1 answer: O. W. Wilson> hold leadership positions before coming to Chicago?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-In 1925, Wilson became chief of police of the Fullerton Police Department for two years.  He then spent two years as an investigator with the Pacific Finance Corporation.  In 1928, at age 28, he became chief of police of the Wichita Police Department, where he served until 1939.
+According to the Wikipedia article for O. W. Wilson, 'In 1925, Wilson became chief of police of the Fullerton Police Department for two years... In 1928, at age 28, he became chief of police of the Wichita Police Department, where he served until 1939.'
```

- Node 3 `subquestion`
  - copy: `In which city from <node 2 answer> did <hop 1 answer> start a criminal justice program at a local university?`
  - tasks_mini: `In which city from <cities from node 2: Fullerton, Wichita> did O. W. Wilson establish a criminal justice program at a university?`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-The Wichita Police Department was created on April 13, 1871.  A notable figure in the Department’s history was O.W. Wilson, who was considered an innovative police reformer.  Wilson was credited with starting the Criminal Justice Program at Wichita State University, previously called the Municipal University of Wichita in 1937.
+According to the Wikipedia article for Wichita Police Department, 'A notable figure in the Department's history was O.W. Wilson, who was considered an innovative police reformer. Wilson was credited with starting the Criminal Justice Program at Wichita State University, previously called the Municipal University of Wichita in 1937.'
```

- Node 4 `subquestion`
  - copy: `What county is <hop 2 answer> located in?`
  - tasks_mini: `What county is <city from node 3: Wichita> located in?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-is the most populous city in the U.S. state of Kansas and the county seat of Sedgwick County.
+According to the Wikipedia article for Wichita, Kansas, 'Wichita... is the most populous city in the U.S. state of Kansas and the county seat of Sedgwick County.'
```

- Node 5 `subquestion`
  - copy: `How many veterans received disability benefits in <hop 3 answer> in 2020?`
  - tasks_mini: `How many VA disability compensation recipients were in <county from node 4: Sedgwick County, Kansas> in FY 2020?`

- Node 5 `answer`
  - copy: `7871`
  - tasks_mini: `7871`

- Node 5 `fact`

```diff
@@ -12 +12,2 @@
+answer = str(answer)
```

- Node 6 `subquestion`
  - copy: `How many veterans received disability benefits in <hop 3 answer> in 2023?`
  - tasks_mini: `How many VA disability compensation recipients were in <county from node 4: Sedgwick County, Kansas> in FY 2023?`

- Node 6 `answer`
  - copy: `8701`
  - tasks_mini: `8701`

- Node 6 `fact`

```diff
@@ -12 +12,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Zohaib Qadri represents which Austin City Council district?`
  - tasks_mini: `Zohaib "Zo" Qadri represents which Austin City Council district?`

- Node 1 `fact`

```diff
@@ -1 +1 @@
-The Austin City Council article lists Zohaib 'Zo' Qadri as the council member for District 9.
+The Austin City Council article lists Zohaib "Zo" Qadri as the council member for District 9.
```

- Node 2 `subquestion`
  - copy: `In the Austin City Council voting record, on what date did the council vote on approving a legal settlement in the Claudia Ford case against the City of Austin?`
  - tasks_mini: `In the Austin City Council voting record, what is the earliest meeting date listed for council district <node_1 answer>?`

- Node 2 `answer`
  - copy: `2023-02-23T00:00:00`
  - tasks_mini: `2023-01-06T00:00:00`

- Node 2 `fact`

```diff
@@ -36,3 +36,3 @@
-text_match = "Approve a settlement in Claudia Ford v. City of Austin, Cause No. D-1-GN-19-004771 in the 250th District Court, Travis County, Texas."
-answer = records.loc[records["item_text"] == text_match, "meeting_date"].min().isoformat()
+filtered = records[records["council_district"].astype(str).str.strip() == "9"]
+answer = filtered["meeting_date"].min().isoformat()
```

- Node 4 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -15 +15,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_5.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `In 2019 arrest records, within area <node_1 answer>, identify the most common arrest charge; then, for that charge, which area has the most arrests? Answer with the area name.`
  - tasks_mini: `In 2019 arrest records, within area <node_1 answer>, identify the most common charge group; then, for that charge group, which area has the most arrests? Answer with the area name.`

- Node 3 `fact`

```diff
@@ -13 +13,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -17 +17,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_6.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -22 +22,2 @@
+answer = str(answer)
```

- Node 2 `subquestion`
  - copy: `In <node_1 answer> Los Angeles arrest records, which area has the most arrests in the catch-all charge category?`
  - tasks_mini: `In <node_1 answer> Los Angeles arrest records, which area has the most arrests in the charge group "Miscellaneous Other Violations"?`

- Node 3 `fact`

```diff
@@ -17 +17,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -17 +17,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -21 +21,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_7.json`
- Impact: moderate
- Node 3 `fact`

```diff
@@ -20 +20,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -16 +16,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -16 +16,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_8.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -22 +22,2 @@
+answer = str(answer)
```

- Node 3 `fact`

```diff
@@ -17 +17,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -17 +17,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -19 +19,2 @@
+answer = str(answer)
```

### `k-4-d-2/task_9.json`
- Impact: moderate
- Node 1 `fact`

```diff
@@ -16 +16,2 @@
+answer = str(answer)
```

- Node 3 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 4 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 5 `fact`

```diff
@@ -19 +19,2 @@
+answer = str(answer)
```

### `k-4-d-3/task_1.json`
- Impact: major
- Node 1 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 1 `subquestion`
  - copy: `Which NYC elementary schools in District 15 and their performance category scores in 2010-11?`
  - tasks_mini: `Which NYC elementary schools in District 15 ranked in the top 2 by performance category score in 2010-11?`

- Node 1 `answer`
  - copy: `{"Magnet School for Science & Technology": 14, "PS 130 The Parkside": 13.1, "PS 172 Beacon School of Excellence": 23.5, "PS 321 William Penn": 15.3, "The Children's School": 16.8}`
  - tasks_mini: `["PS 321 William Penn", "PS 107 John W Kimball"]`

- Node 1 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1,5 +1,6 @@
-import os
+import boto3
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
@@ -7,35 +8,9 @@
-local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 2 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 2 `subquestion`
  - copy: `Which NYC elementary schools in District 15 and their performance category scores in 2011-12?`
  - tasks_mini: `Which NYC elementary schools in District 15 ranked in the top 2 by performance category score in 2011-12?`

- Node 2 `answer`
  - copy: `{"Magnet School of Math, Science and Design Techno": 21.2, "PS 130 The Parkside": 20.5, "PS 146": 21.6, "PS 15 Patrick F. Daly": 22.3, "PS 172 Beacon School of Excellence": 25}`
  - tasks_mini: `["PS 321 William Penn", "PS 10 Magnet School"]`

- Node 2 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1,5 +1,6 @@
-import os
+import boto3
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
@@ -7,35 +8,9 @@
-local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 3 `depends_on`
  - copy: ``
  - tasks_mini: `[]`

- Node 3 `subquestion`
  - copy: `Which NYC elementary schools in District 15 and their performance category scores in 2012-13?`
  - tasks_mini: `Which NYC elementary schools in District 15 ranked in the top 2 by performance category score in 2012-13?`

- Node 3 `answer`
  - copy: `{"Magnet School of Math, Science and Design Techno": 21.5, "PS 107 John W. Kimball": 17.8, "PS 172 Beacon School of Excellence": 25, "PS 321 William Penn": 18.9, "PS 39 Henry Bristow": 17.7}`
  - tasks_mini: `["PS 321 William Penn", "PS 10 Magnet School"]`

- Node 3 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1,5 +1,6 @@
-import os
+import boto3
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
@@ -7,35 +8,9 @@
-local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 4 `depends_on`
  - copy: ``
  - tasks_mini: `["intersection_of_1_2_3"]`

- Node 4 `subquestion`
  - copy: `What is the ZIP code of <hop 1 answer>?`
  - tasks_mini: `What is the zip code where is <intersection of node_1, node_2, node_3: PS 321 William Penn> located?`

- Node 4 `fact`

```diff
@@ -1,5 +1,7 @@
-import os
+import re
+import boto3
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 5 `depends_on`
  - copy: ``
  - tasks_mini: `["node_4"]`

- Node 5 `subquestion`
  - copy: `Which park is the neighborhood corresponding to the ZIP code in <hop 2 answer> bounded by?`
  - tasks_mini: `Which park is the neighborhood corresponding to the zip code in <node_4 answer> bounded by?`

- Node 6 `depends_on`
  - copy: ``
  - tasks_mini: `["node_5"]`

- Node 6 `subquestion`
  - copy: `What is the size of <hop 3 answer>? Answer in acres.`
  - tasks_mini: `What is the size of the park in <node_5 answer>? Answer in acre`

### `k-4-d-3/task_10.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which non-NYC New York counties had over 90 youth sent to jail in 2015?`
  - tasks_mini: `Which Non-NYC NY counties had over 90 youth detention secure/mixed admissions in 2015?`

- Node 1 `answer`
  - copy: `["Erie", "Monroe", "Westchester", "Onondaga", "Nassau"]`
  - tasks_mini: `["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Nassau County"]`

- Node 1 `fact`

```diff
@@ -19 +19,2 @@
+answer = [str(x) + " County" for x in answer]
```

- Node 2 `subquestion`
  - copy: `Which NY counties had a total jail census under 750 in 2021?`
  - tasks_mini: `Which NY counties had jail census under 750 in 2021?`

- Node 2 `answer`
  - copy: `["Monroe", "Suffolk", "Erie", "Westchester", "Onondaga", "Orange", "Broome", "Albany", "Niagara", "Oneida"]`
  - tasks_mini: `["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Suffolk County"]`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -16,4 +16,4 @@
-df = df[df["Census"] < 750].copy()
-df = df.sort_values("Census", ascending=False)
-answer = df["County"].head(10).tolist()
+order = ["Erie", "Monroe", "Westchester", "Onondaga", "Suffolk"]
+qualifying = set(df[df["Census"] < 750]["County"].astype(str))
+answer = [county + " County" for county in order if county in qualifying]
```

- Node 3 `subquestion`
  - copy: `Which Non-NYC NY counties had over 65,500 homeowner school-tax relief exemptions in 2022?`
  - tasks_mini: `Which Non-NYC NY counties had over 65,500 basic STAR exemptions in 2022?`

- Node 3 `answer`
  - copy: `["Suffolk", "Nassau", "Erie", "Monroe"]`
  - tasks_mini: `["Suffolk County", "Nassau County", "Erie County", "Monroe County"]`

- Node 3 `fact`

```diff
@@ -18 +18,2 @@
+answer = [str(x) + " County" for x in answer]
```

- Node 4 `subquestion`
  - copy: `What is the county seat of Erie County?`
  - tasks_mini: `What is the county seat of Erie County (from <intersection of nodes 1-3>)?`

- Node 5 `subquestion`
  - copy: `What is the county seat of Monroe County?`
  - tasks_mini: `What is the county seat of Monroe County (from <intersection of nodes 1-3>)?`

- Node 6 `subquestion`
  - copy: `How many violent crimes did Erie County have in 2021?`
  - tasks_mini: `How many violent crimes did Erie County (the county whose seat is <node_4 answer>) have in 2021?`

- Node 7 `subquestion`
  - copy: `How many violent crimes did Monroe County have in 2021?`
  - tasks_mini: `How many violent crimes did Monroe County (the county whose seat is <node_5 answer>) have in 2021?`

- Node 8 `subquestion`
  - copy: `In what year was <hop 3 answer> incorporated as a city?`
  - tasks_mini: `In what year was <comparative of nodes 6-7: Buffalo, the county seat of Erie which had higher violent crime (3,493 > 2,320)> incorporated as a city?`

### `k-4-d-3/task_11.json`
- Impact: major
- Node 1 `answer`
  - copy: `["Marshall County", "Floyd County", "Clayton County", "Crawford County", "Des Moines County", "Clinton County", "Lee County", "Tama County", "Scott County", "Black Hawk County"]`
  - tasks_mini: `["Allamakee County", "Appanoose County", "Benton County", "Black Hawk County", "Butler County", "Chickasaw County", "Clayton County", "Clinton County", "Crawford County", "Des Moines County", "Dickinson County", "Fayette County", "Floyd County", "Jackson County", "Jones County", "Keokuk County", "Lee County", "Louisa County", "Madison County", "Marshall Cou...`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -18,6 +18,2 @@
-df = df.sort_values("UNEMPLOYMENT RATE", ascending=False)
-top = df["AREA NAME"].tolist()
-priority = top[:8]
-extras = [x for x in ["Scott County", "Black Hawk County"] if x in top and x not in priority]
-answer = (priority + extras)[:10]
+answer = sorted(df["AREA NAME"].dropna().astype(str).tolist())
```

- Node 2 `subquestion`
  - copy: `Which Iowa counties had more than 12% of their motor-fuel sales coming from biofuels in 2019?`
  - tasks_mini: `Which Iowa counties had biofuel distribution above 12% in 2019?`

- Node 2 `answer`
  - copy: `["Fremont", "Poweshiek", "Guthrie", "Clarke", "Floyd", "Hamilton", "Pottawattamie", "Jasper", "Scott", "Black Hawk"]`
  - tasks_mini: `["Adair County", "Allamakee County", "Audubon County", "Benton County", "Black Hawk County", "Bremer County", "Calhoun County", "Cedar County", "Cerro Gordo County", "Chickasaw County", "Clarke County", "Clayton County", "Clinton County", "Dallas County", "Floyd County", "Franklin County", "Fremont County", "Greene County", "Grundy County", "Guthrie County"...`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -11,10 +11,3 @@
-df = df[
-    (df["Calendar Year"] == 2019)
-    & (df["Biofuel Distribution Percentage"] > 12)
-].copy()
-df = df.sort_values("Biofuel Distribution Percentage", ascending=False)
-top = df["County"].tolist()
```

- Node 3 `subquestion`
  - copy: `Which Iowa counties had residents who collectively received more than $4 billion in income in 2019?`
  - tasks_mini: `Which Iowa counties had personal income above $4 billion in 2019?`

- Node 3 `answer`
  - copy: `["Polk", "Linn", "Scott", "Johnson", "Dallas", "Black Hawk", "Dubuque", "Woodbury", "Story", "Pottawattamie"]`
  - tasks_mini: `["Black Hawk County", "Scott County", "Dallas County", "Dubuque County", "Johnson County", "Linn County", "Polk County", "Pottawattamie County", "Story County", "Woodbury County"]`

- Node 3 `fact`

```diff
@@ -13,8 +13,5 @@
-df = df[
-    (df["Variable"] == "Personal income")
-    & (df["Date"].dt.year == 2019)
-    & (df["Value"] > 4000000)
-].copy()
-df = df.sort_values("Value", ascending=False)
```

- Node 4 `subquestion`
  - copy: `What is the county seat of Black Hawk County?`
  - tasks_mini: `What is the county seat of Black Hawk County (from <intersection of nodes 1-3>)?`

- Node 5 `subquestion`
  - copy: `What is the county seat of Scott County?`
  - tasks_mini: `What is the county seat of Scott County (from <intersection of nodes 1-3>)?`

- Node 6 `subquestion`
  - copy: `What was the 2020 census population of Waterloo?`
  - tasks_mini: `What was the 2020 census population of Waterloo (the county seat of <node_4 source county>)?`

- Node 7 `subquestion`
  - copy: `What was the 2020 census population of Davenport?`
  - tasks_mini: `What was the 2020 census population of Davenport (the county seat of <node_5 source county>)?`

- Node 8 `subquestion`
  - copy: `What was the July 2019 population of <hop 3 answer>?`
  - tasks_mini: `What was the July 2019 population of Scott County (the county whose seat <comparative of nodes 6-7: Davenport with 101,724 > Waterloo with 67,314>)?`

### `k-4-d-3/task_12.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `For 2021, how many employees were there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 2 `subquestion`
  - copy: `For 2022, how many employees were there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 3 `subquestion`
  - copy: `For 2023, how many employees were there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 3 `answer`
  - copy: `{"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956}`
  - tasks_mini: `CORRECTIONS`

- Node 3 `fact`

```diff
@@ -9,2 +9,7 @@
+prior_counts = {
+    "CORRECTIONS": [12530, 12380],
+    "SOCIAL SERVICES": [8362, 8723],
+    "TRANSPORTATION": [7170, 6917],
+}
@@ -12,3 +17,3 @@
-answer = (
```

- Node 4 `subquestion`
  - copy: `What city is the headquarters of <hop 1 answer>?`
  - tasks_mini: `What city is the headquarters of the agency with the highest average employee count located in?`

- Node 5 `subquestion`
  - copy: `What historically Black university is located in <hop 2 answer>?`
  - tasks_mini: `What is the historically Black university located in Jefferson City?`

- Node 6 `subquestion`
  - copy: `Who founded <hop 3 answer>?`
  - tasks_mini: `Who founded Lincoln University?`

### `k-4-d-3/task_2.json`
- Impact: major
- Node 2 `answer`
  - copy: `["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270", "PS 316"]`
  - tasks_mini: `["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]`

- Node 2 `fact`

```diff
@@ -1,4 +1,5 @@
+import re
+import boto3
-import boto3
@@ -11,39 +12,11 @@
-node_1_answer = [
-    "Clinton Hill",
-    "Bedford-Stuyvesant",
```

- Node 3 `subquestion`
  - copy: `Which schools from <node_2 answer> had kindergarten class size at most 10 in 2008-09?`
  - tasks_mini: `Which schools from <node_2 answer> had kindergarten class size <= 10 in 2008-09?`

- Node 3 `answer`
  - copy: `["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270"]`
  - tasks_mini: `["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]`

- Node 3 `fact`

```diff
@@ -2,4 +2,4 @@
+import boto3
-import boto3
@@ -12,41 +12,15 @@
-node_2_answer = [
-    "PS 003",
-    "PS 009",
-    "PS 011",
```

- Node 4 `subquestion`
  - copy: `Which schools from <node_2 answer> had kindergarten class size at most 10 in 2009-10?`
  - tasks_mini: `Which schools from <node_2 answer> had kindergarten class size <= 10 in 2009-10?`

- Node 4 `answer`
  - copy: `["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270", "PS 316"]`
  - tasks_mini: `["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]`

- Node 4 `fact`

```diff
@@ -1,5 +1,4 @@
-import re
+import boto3
-import boto3
@@ -12,41 +11,15 @@
-node_2_answer = [
-    "PS 003",
-    "PS 009",
```

- Node 5 `subquestion`
  - copy: `Which schools from <node_2 answer> had kindergarten class size at most 10 in 2010-11?`
  - tasks_mini: `Which schools from <node_2 answer> had kindergarten class size <= 10 in 2010-11?`

- Node 5 `answer`
  - copy: `["PS 003", "PS 011", "PS 046", "PS 054", "PS 056", "PS 256", "PS 270"]`
  - tasks_mini: `["PS 003 The Bedford Village", "PS 011 Purvis J. Behan", "PS 046 Edward C. Blum", "PS 054 Samuel C. Barnes", "PS 056 Lewis H. Latimer", "PS 256 Benjamin Banneker", "PS 270 Johann DeKalb"]`

- Node 5 `fact`

```diff
@@ -1,5 +1,4 @@
-import re
+import boto3
-import boto3
@@ -12,41 +11,21 @@
-node_2_answer = [
-    "PS 003",
-    "PS 009",
```

- Node 6 `answer`
  - copy: `{"Ps 11 Purvis J Behan": 24, "Ps 256 Benjamin Banneker": 2, "Ps 270 Joanne Dekalb": 4, "Ps 3 The Bedford Village": 7, "Ps 54 Samuel C Barnes": 15, "Ps 56 Lewis H Latimer": 2}`
  - tasks_mini: `{"PS 003 The Bedford Village": 7, "PS 009 Teunis G. Bergen": 13, "PS 011 Purvis J. Behan": 24, "PS 046 Edward C. Blum": 22, "PS 056 Lewis H. Latimer": 2, "PS 067 Charles A. Dorsey": 7, "PS 270 Johann DeKalb": 4}`

- Node 6 `fact`

```diff
@@ -2,4 +2,4 @@
+import boto3
-import boto3
@@ -12,77 +12,19 @@
-node_3_answer = [
-    "PS 003",
-    "PS 009",
-    "PS 011",
```

- Node 7 `answer`
  - copy: `{"Ps 11 Purvis J Behan": 15, "Ps 256 Benjamin Banneker": 13, "Ps 270 Johann Dekalb": 5, "Ps 3 The Bedford Village": 6, "Ps 54 Samuel C Barnes": 7, "Ps 56 Lewis H Latimer": 2}`
  - tasks_mini: `{"PS 003 The Bedford Village": 6, "PS 009 Teunis G. Bergen": 5, "PS 011 Purvis J. Behan": 15, "PS 046 Edward C. Blum": 13, "PS 056 Lewis H. Latimer": 2, "PS 067 Charles A. Dorsey": 3, "PS 270 Johann DeKalb": 5}`

- Node 7 `fact`

```diff
@@ -2,4 +2,4 @@
+import boto3
-import boto3
@@ -12,77 +12,19 @@
-node_3_answer = [
-    "PS 003",
-    "PS 009",
-    "PS 011",
```

- Node 8 `answer`
  - copy: `{"Ps 11 Purvis J Behan": 22, "Ps 256 Benjamin Banneker": 7, "Ps 270 Johann Dekalb": 4, "Ps 3 The Bedford Village": 12, "Ps 54 Samuel C Barnes": 9, "Ps 56 Lewis H Latimer": 5}`
  - tasks_mini: `{"PS 003 The Bedford Village": 12, "PS 009 Teunis G. Bergen": 4, "PS 011 Purvis J. Behan": 22, "PS 046 Edward C. Blum": 15, "PS 056 Lewis H. Latimer": 5, "PS 067 Charles A. Dorsey": 10, "PS 270 Johann DeKalb": 4}`

- Node 8 `fact`

```diff
@@ -2,4 +2,4 @@
+import boto3
-import boto3
@@ -12,77 +12,19 @@
-node_3_answer = [
-    "PS 003",
-    "PS 009",
-    "PS 011",
```

### `k-4-d-3/task_3.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1,3 +1 @@
-Eight: Virginia
-
-PresidentImageHistoric siteGeorge WashingtonGeorge Washington Birthplace National Monument, Colonial Beach, VirginiaJohn AdamsJohn Adams Birthplace, Quincy, MassachusettsJames MadisonBelle Grove Plantation, Port Conway, VirginiaJames MonroeJames Monroe Birthplace Park & Museum, Colonial Beach, VirginiaJohn Quincy AdamsJohn Quincy Adams Birthplace, Quincy, MassachusettsWilliam Henry HarrisonBerkeley Plantation, Charles City County, VirginiaZachary Taylor100pxHare Forest Farm, Orange County, VirginiaZachary Taylor House, Louisville, KentuckyJohn TylerGreenway Plantation, Charles City County, Virginia
+Eight U.S. presidents were born in Virginia: George Washington, Thomas Jefferson, James Madison, James Monroe, William Henry Harrison, John Tyler, Zachary Taylor, and Woodrow Wilson.
```

- Node 5 `subquestion`
  - copy: `At which NASA facility was equipment used collect the bare earth elevation data for <node_4 answer> in USGS's survey in 2007 developed?`
  - tasks_mini: `At which NASA facility was the EAARL system used in the 2007 USGS survey of <node_4 answer> developed?`

- Node 5 `fact`

```diff
@@ -1 +1,44 @@
-In 2007, USGS published Open File Report 1179 containing bare earth elevation data for George Washington Birthplace National Monument, collected using the NASA EAARL (Experimental Advanced Airborne Research Lidar) system. The EAARL was developed by NASA at Wallops Flight Facility in Virginia.
+import os
+import re
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
```

### `k-4-d-3/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which agencies issued the largest total amount of parking fines in January 2019?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 1 `answer`
  - copy: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 4", "METROPOLITAN POLICE DPT-DISTRICT 5", "METROPOLITAN POLICE DPT-DISTRICT 7", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 6", "SPECIAL OPERATION DIV & TRAFFIC DIV...`
  - tasks_mini: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 4", "METROPOLITAN POLICE DPT-DISTRICT 5", "METROPOLITAN POLICE DPT-DISTRICT 7", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 6", "SPECIAL OPERATION DIV & TRAFFIC DIV...`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,20 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 2 `subquestion`
  - copy: `Which agencies issued the largest total amount of parking fines in January 2020?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 2 `answer`
  - copy: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT 6", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 4", "DDOT", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 5"]`
  - tasks_mini: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT 6", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 4", "DDOT", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 5", "METRO POLICE", "SPECIAL OPE...`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,20 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 3 `subquestion`
  - copy: `Which agencies issued the largest total amount of parking fines in January 2021?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 3 `answer`
  - copy: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 6", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 4", "METROPOLITAN POLICE DPT-DISTRICT 5", "SPECIAL OPERATION DIV & TRAFFIC DIV", "D.C. HOUSING AUTHORITY...`
  - tasks_mini: `["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE DPT-DISTRICT 6", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 4", "METROPOLITAN POLICE DPT-DISTRICT 5", "SPECIAL OPERATION DIV & TRAFFIC DIV", "D.C. HOUSING AUTHORITY...`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,20 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 4 `subquestion`
  - copy: `In January 2019, how many driving-related violations did each agency in <hop 1 answer> issue?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 4 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 5 `subquestion`
  - copy: `In January 2020, how many driving-related violations did each agency in <hop 1 answer> issue?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 5 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 6 `subquestion`
  - copy: `In January 2021, how many driving-related violations did each agency in <hop 1 answer> issue?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 6 `answer`
  - copy: `{"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32}`
  - tasks_mini: `UNITED STATES PARK POLICE`

- Node 6 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 7 `subquestion`
  - copy: `Which federal agency operates <hop 2 answer>?`
  - tasks_mini: `Which federal agency operates the United States Park Police (from hop 2)?`

- Node 8 `subquestion`
  - copy: `<hop 3 answer> is within which U.S. department?`
  - tasks_mini: `The agency (from hop 3) is within which U.S. department?`

### `k-4-d-3/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In January 2019, how many driving-related violations did each of the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 1 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 2 `subquestion`
  - copy: `In January 2020, how many driving-related violations did each of the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 2 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 3 `subquestion`
  - copy: `In January 2021, how many driving-related violations did each of the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 3 `answer`
  - copy: `{"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32}`
  - tasks_mini: `UNITED STATES PARK POLICE`

- Node 3 `fact`

```diff
@@ -1,2 +1,2 @@
-import boto3
+import os
@@ -4,19 +4,42 @@
-from botocore import UNSIGNED
-from botocore.config import Config
+import boto3
-bucket_name = "lakeqa-yc4103-datalake"
```

- Node 4 `subquestion`
  - copy: `Which federal agency operates <hop 1 answer>?`
  - tasks_mini: `Which federal agency operates the United States Park Police (from hop 1)?`

- Node 5 `subquestion`
  - copy: `<hop 2 answer> is within which U.S. department?`
  - tasks_mini: `The agency (from hop 2) is within which U.S. department?`

- Node 6 `subquestion`
  - copy: `Who is the head of <hop 3 answer>?`
  - tasks_mini: `Who is the head of the department (from hop 3)?`

### `k-4-d-3/task_6.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2019?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2019 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 2 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2020?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2020 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 3 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2021?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2021 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 4 `subquestion`
  - copy: `For 2019, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 5 `subquestion`
  - copy: `For 2020, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 6 `subquestion`
  - copy: `For 2021, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 7 `subquestion`
  - copy: `For 2019, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 8 `subquestion`
  - copy: `For 2020, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 9 `subquestion`
  - copy: `For 2021, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 10 `subquestion`
  - copy: `Who was brought on as Superintendent of Police when the position (current iteration) was established as head of <hop 3 answer>?`
  - tasks_mini: `Who was brought on as Superintendent of Police when the position (current iteration) was established as head of the department (from hop 3)?`

### `k-4-d-3/task_7.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/street-sweeping-schedule-2022/files/rows.txt`
  - tasks_mini: `datagov/street-sweeping-schedule-2022/files/data.txt`

- Node 1 `subquestion`
  - copy: `For Wards 2 and 5, how many scheduled street-cleaning events were listed in 2022?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2022 file; WARD in {2,5}; count rows by WARD.)`

- Node 1 `fact`

```diff
@@ -1,3 +1,3 @@
+import json
-import io
@@ -6,15 +6,22 @@
-bucket_name = "lakeqa-yc4103-datalake"
-object_key = "datagov/street-sweeping-schedule-2022/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
-obj = s3.get_object(Bucket=bucket_name, Key=object_key)
```

- Node 2 `source`
  - copy: `datagov/street-sweeping-schedule-2023/files/rows.txt`
  - tasks_mini: `datagov/street-sweeping-schedule-2023/files/data.txt`

- Node 2 `subquestion`
  - copy: `For Wards 2 and 5, how many scheduled street-cleaning events were listed in 2023?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2023 file; WARD in {2,5}; count rows by WARD.)`

- Node 2 `fact`

```diff
@@ -1,3 +1,3 @@
+import json
-import io
@@ -6,15 +6,22 @@
-bucket_name = "lakeqa-yc4103-datalake"
-object_key = "datagov/street-sweeping-schedule-2023/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
-obj = s3.get_object(Bucket=bucket_name, Key=object_key)
```

- Node 3 `source`
  - copy: `datagov/street-sweeping-schedule-2024/files/rows.txt`
  - tasks_mini: `datagov/street-sweeping-schedule-2024/files/data.txt`

- Node 3 `subquestion`
  - copy: `For Wards 2 and 5, how many scheduled street-cleaning events were listed in 2024?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2024 file; WARD in {2,5}; count rows by WARD.)`

- Node 3 `fact`

```diff
@@ -1,3 +1,3 @@
+import json
-import io
@@ -6,15 +6,22 @@
-bucket_name = "lakeqa-yc4103-datalake"
-object_key = "datagov/street-sweeping-schedule-2024/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
-obj = s3.get_object(Bucket=bucket_name, Key=object_key)
```

- Node 4 `subquestion`
  - copy: `Which charter school in <hop 1 answer> spans grades 8 and 9?`
  - tasks_mini: `Which charter school in the ward (from hop 1) spans grade 8 and grade 9? (Filter for this node: WARD == 5; GRADES include 8 and 9 in the range.)`

- Node 4 `fact`

```diff
@@ -1,5 +1,3 @@
+import json
-import io
-import json
-import pandas as pd
@@ -7,43 +5,13 @@
-bucket_name = "lakeqa-yc4103-datalake"
-object_key = "datagov/dc-charter-schools/files/data.txt"
```

- Node 5 `subquestion`
  - copy: `According to the biography of <hop 2 answer>, where was that person born?`
  - tasks_mini: `The charter school identified (from hop 2) includes the name 'Sojourner Truth'. According to her biography, where was she born?`

- Node 6 `subquestion`
  - copy: `According to the Rifton, New York article, what county is <hop 3 answer> located in?`
  - tasks_mini: `Swartekill, New York (from hop 3) is described in the Rifton, New York article; what county is Rifton in?`

- Node 6 `answer`
  - copy: `Ulster County`
  - tasks_mini: `Ulster County, New York`

### `k-4-d-3/task_8.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NYC high schools were in the top 7 by the school's comprehensive score in 2007-08?`
  - tasks_mini: `Which NYC high schools were in the top 7 by overall score in 2007-08?`

- Node 1 `answer`
  - copy: `["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATHEMATICS", "HIGH SCHOOL FOR CONTEMPORARY ARTS", "BEDFORD ACADEMY HIGH SCHOOL", "MANHATTAN BRIDGES HIGH SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "NEW WORLD HIGH SCHOOL"]`
  - tasks_mini: `["Brooklyn International High School", "Gregorio Luperon High School", "High School for Contemporary Arts", "Bedford Academy High School", "Manhattan Bridges High School", "Marble Hill High School for International Studies", "New World High School"]`

- Node 1 `fact`

```diff
@@ -1 +1,3 @@
+import io
+import re
@@ -4,12 +6,20 @@
-from io import StringIO
+source = "datagov/2007-2008-school-progress-report/files/rows.txt"
-key = "datagov/2007-2008-school-progress-report/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `subquestion`
  - copy: `Which NYC high schools were in the top 7 by the school's comprehensive score in 2008-09?`
  - tasks_mini: `Which NYC high schools were in the top 7 by overall score in 2008-09?`

- Node 2 `answer`
  - copy: `["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PREPARATORY SCHOOL", "SOUTH BRONX PREPARATORY: A COLLEGE BOARD SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL FOR VIOLIN AND DANCE", "ESSEX STREET ACADEMY"]`
  - tasks_mini: `["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Preparatory School", "South Bronx Preparatory", "Marble Hill High School for International Studies", "High School for Violin and Dance", "Essex Street Academy"]`

- Node 2 `fact`

```diff
@@ -1 +1,3 @@
+import io
+import re
@@ -4,12 +6,21 @@
-from io import StringIO
+source = "datagov/2008-2009-school-progress-report/files/rows.txt"
-key = "datagov/2008-2009-school-progress-report/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `subquestion`
  - copy: `Which NYC high schools were in the top 7 by the school's comprehensive score in 2009-10?`
  - tasks_mini: `Which NYC high schools were in the top 7 by overall score in 2009-10?`

- Node 3 `answer`
  - copy: `["Theatre Arts Production Company School", "Brooklyn International High School at Water's Edge", "Williamsburg Preparatory School", "Marble Hill High School for International Studies", "Williamsburg High School for Architecture and Design", "Manhattan Village Academy", "High School for Violin and Dance"]`
  - tasks_mini: `["Theatre Arts Production Company School", "Brooklyn International High School", "Williamsburg Preparatory School", "Marble Hill High School for International Studies", "Williamsburg High School for Architecture and Design", "Manhattan Village Academy", "High School for Violin and Dance"]`

- Node 3 `fact`

```diff
@@ -1 +1,3 @@
+import io
+import re
@@ -4,12 +6,20 @@
-from io import StringIO
+source = "datagov/2009-2010-school-progress-report/files/rows.txt"
-key = "datagov/2009-2010-school-progress-report/files/rows.txt"
-s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `subquestion`
  - copy: `What is the neighborhood containing <hop 1 answer> named after?`
  - tasks_mini: `What is the neighborhood containing <intersection of node_1, node_2, node_3> named after?`

- Node 7 `subquestion`
  - copy: `In what year was <hop 3 answer> designed?`
  - tasks_mini: `In what year is <intersection of node_5, node_6> designed?`

### `k-4-d-3/task_9.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NY counties had between 29,000 and 75,000 households enrolled in the federal program that provides eligible low-income households with monthly benefits to buy groceries in February 2023?`
  - tasks_mini: `Which NY counties had SNAP households between 29,000 and 75,000 in February 2023?`

- Node 1 `answer`
  - copy: `["Suffolk", "Monroe", "Westchester", "Onondaga", "Nassau"]`
  - tasks_mini: `["Suffolk County", "Monroe County", "Westchester County", "Onondaga County", "Nassau County"]`

- Node 1 `fact`

```diff
@@ -7,3 +7,3 @@
-key = "datagov/supplemental-nutrition-assistance-program-snap-caseloads-and-expenditures-beginning-2002/files/rows.txt"
+key = "datagov/annual-youth-detention-admissions-by-county-beginning-2006/files/rows.txt"
@@ -11,8 +11,10 @@
+df.columns = [c.strip() for c in df.columns]
-    (df["Year"] == 2023)
-    & (df["Month"] == "February")
-    & (df["Total SNAP Households"].between(29000, 75000))
```

- Node 2 `subquestion`
  - copy: `Which NY counties had between 350 and 600 children placed in out-of-home care in 2023?`
  - tasks_mini: `Which NY counties had between 350 and 600 children in foster care in 2023?`

- Node 2 `answer`
  - copy: `["ERIE", "ONONDAGA", "SUFFOLK", "ONEIDA", "MONROE"]`
  - tasks_mini: `["Erie County", "Onondaga County", "Suffolk County", "Oneida County", "Monroe County"]`

- Node 2 `fact`

```diff
@@ -7,3 +7,3 @@
-key = "datagov/children-in-foster-care-annually-beginning-1994/files/rows.txt"
+key = "datagov/jail-population-by-county-beginning-1997/files/rows.txt"
@@ -11,7 +11,10 @@
-df = df[
-    (df["Year"] == 2023)
-    & (df["Children In Care"].between(350, 600))
-].copy()
```

- Node 3 `answer`
  - copy: `["Monroe", "Erie", "Westchester", "Suffolk", "Nassau", "Onondaga"]`
  - tasks_mini: `["Monroe County", "Erie County", "Westchester County", "Suffolk County", "Nassau County", "Onondaga County"]`

- Node 3 `fact`

```diff
@@ -7,3 +7,3 @@
-key = "datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt"
+key = "datagov/nys-school-tax-relief-star-reimbursement-by-county-beginning-levy-year-1998/files/rows.txt"
@@ -12,8 +12,8 @@
-    (df["Service Year"] == 2015)
-    & (df["Age Group"] == "Adult")
-    & (df["Rate Code Group"] == "OMH Licensed Clinic Treatment")
-    & (df["Count of Recipients by Rate Code Group and County"].between(5000, 18000))
```

- Node 4 `subquestion`
  - copy: `Which NY counties had between 4,000 and 6,000 temporary cash-assistance cases for low-income people and families in February 2023?`
  - tasks_mini: `Which of <intersection of nodes 1-3> had Temporary Assistance cases between 4,000 and 6,000 in February 2023?`

- Node 4 `answer`
  - copy: `["Suffolk", "Onondaga", "Westchester"]`
  - tasks_mini: `["Suffolk County", "Onondaga County"]`

- Node 4 `fact`

```diff
@@ -11,2 +11,3 @@
+candidates = ["Suffolk", "Monroe", "Onondaga"]
@@ -14,2 +15,3 @@
+    & (df["District"].isin(candidates))
@@ -17,2 +19,2 @@
-answer = df["District"].tolist()
+answer = [str(x) + " County" for x in df["District"].tolist()]
```

- Node 5 `subquestion`
  - copy: `Which NY counties had social services staff between 600 and 1,000 total staff in the county's social-services agency in 2017?`
  - tasks_mini: `Which of <intersection of nodes 1-3> had social services staff between 600 and 1,000 in 2017?`

- Node 5 `answer`
  - copy: `["Monroe", "Nassau", "Onondaga"]`
  - tasks_mini: `["Monroe County", "Onondaga County"]`

- Node 5 `fact`

```diff
@@ -11,4 +11,6 @@
+candidates = ["Suffolk", "Monroe", "Onondaga"]
+    & (df["District"].isin(candidates))
@@ -16,2 +18,2 @@
-answer = df["District"].tolist()
+answer = [str(x) + " County" for x in df["District"].tolist()]
```

- Node 6 `subquestion`
  - copy: `Which NY counties had opening public-assistance cash-benefit cases between 200 and 400 in March 2021?`
  - tasks_mini: `Which of <intersection of nodes 1-3> had Public Assistance case openings between 200 and 400 in March 2021?`

- Node 6 `answer`
  - copy: `["Erie", "Monroe", "Onondaga", "Westchester"]`
  - tasks_mini: `["Monroe County", "Onondaga County"]`

- Node 6 `fact`

```diff
@@ -11,2 +11,3 @@
+candidates = ["Suffolk", "Monroe", "Onondaga"]
@@ -14,2 +15,3 @@
+    & (df["District"].isin(candidates))
@@ -17,2 +19,2 @@
-answer = df["District"].tolist()
+answer = [str(x) + " County" for x in df["District"].tolist()]
```

- Node 7 `subquestion`
  - copy: `What is the county seat of <hop 2 answer> County?`
  - tasks_mini: `What is the county seat of <intersection of nodes 4-6>?`

- Node 8 `subquestion`
  - copy: `In what year was <hop 3 answer> incorporated as a city?`
  - tasks_mini: `In what year was <node_7 answer> incorporated as a city?`

### `k-4-d-4/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NYC elementary schools were in the top 5 by their learning environments in 2006-07?`
  - tasks_mini: `Which NYC elementary schools were in the top 5 by environment category score in 2006-07? (Filter SCHOOL LEVEL* contains 'Elementary'; break ties by SCHOOL name Z-A.)`

- Node 2 `subquestion`
  - copy: `Which NYC elementary schools were in the top 5 by their learning environments in 2007-08?`
  - tasks_mini: `Which NYC elementary schools were in the top 5 by environment category score in 2007-08? (Filter SCHOOL LEVEL* contains 'Elementary'; break ties by SCHOOL name Z-A.)`

- Node 3 `subquestion`
  - copy: `Which NYC elementary schools were in the top 5 by their learning environments in 2008-09?`
  - tasks_mini: `Which NYC elementary schools were in the top 5 by environment category score in 2008-09? (Filter SCHOOL LEVEL* contains 'Elementary'; break ties by SCHOOL name Z-A.)`

- Node 4 `subquestion`
  - copy: `Which NYC elementary schools were in the top 5 by their learning environments in 2009-10?`
  - tasks_mini: `Which NYC elementary schools were in the top 5 by environment category score in 2009-10? (Filter SCHOOL LEVEL* contains 'Elementary'; break ties by SCHOOL name Z-A.)`

- Node 5 `source`
  - copy: `datagov/2013-2014-school-locations/files/rows.txt`
  - tasks_mini: `datagov/2006-2007-school-progress-report/files/rows.txt`

- Node 5 `subquestion`
  - copy: `Which school from <hop 1 answer> is located in the Bedford neighborhood according to the 2013-14 school locations data?`
  - tasks_mini: `Which schools appear in the top-5 lists in at least three of the four years from nodes 1-4?`

- Node 5 `answer`
  - copy: `P.S. 380 John Wayne Elementary`
  - tasks_mini: `["P.S. 380 John Wayne Elementary", "P.S. 172 Beacon School of Excellence"]`

- Node 5 `fact`

```diff
@@ -1,2 +1,3 @@
+import re
@@ -6,13 +7,35 @@
-candidate_schools = [
-    "P.S. 380 John Wayne Elementary",
-    "P.S. 172 Beacon School of Excellence",
+bucket = "lakeqa-yc4103-datalake"
+sources = [
```

- Node 6 `source`
  - copy: `wikipedia/John_Wayne_Elementary_School/content.txt`
  - tasks_mini: `datagov/2013-2014-school-locations/files/rows.txt`

- Node 6 `subquestion`
  - copy: `What day is <hop 2 answer>'s school day? Answer in MM/DD format`
  - tasks_mini: `Which school from node_5 is located in the Bedford NTA according to the 2013-14 school locations data?`

- Node 6 `answer`
  - copy: `10/28`
  - tasks_mini: `P.S. 380 John Wayne Elementary`

- Node 6 `fact`

```diff
@@ -1 +1,18 @@
-John Wayne Elementary School Day is on October 28
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

### `k-4-d-4/task_10.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In the school district office listings, entries with CITY equal to Iowa City and NMCNTY equal to Johnson County share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='Iowa City' and NMCNTY='Johnson County' share what two-digit state FIPS code (STFIP)?`

- Node 2 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most public schools? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 3 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most private schools? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 4 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most school district offices? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 5 `subquestion`
  - copy: `Among <hop 2 answer>, which single county has the most postsecondary institutions in STFIP equal to <node 1 answer>? Answer with the county name including the word County.`
  - tasks_mini: `Let A be the set of counties in <node_2 answer>, B be the set of counties in <node_3 answer>, and C be the set of counties in <node_4 answer>. Consider the intersection of C with the union of A and B. Among those counties, which single county has the most postsecondary institutions in STFIP='<node_1 answer>'? Answer with the county name including the word '...`

- Node 6 `subquestion`
  - copy: `How many public schools have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many public schools have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 6 `answer`
  - copy: `130`
  - tasks_mini: `130`

- Node 6 `fact`

```diff
@@ -13 +13,2 @@
+answer = str(answer)
```

- Node 7 `subquestion`
  - copy: `How many private schools have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many private schools have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 7 `answer`
  - copy: `19`
  - tasks_mini: `19`

- Node 7 `fact`

```diff
@@ -13 +13,2 @@
+answer = str(answer)
```

- Node 8 `subquestion`
  - copy: `How many school district offices have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many school district offices have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 8 `answer`
  - copy: `12`
  - tasks_mini: `12`

- Node 8 `fact`

```diff
@@ -13 +13,2 @@
+answer = str(answer)
```

- Node 9 `subquestion`
  - copy: `How many postsecondary institutions have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many postsecondary institutions have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 9 `answer`
  - copy: `14`
  - tasks_mini: `14`

- Node 9 `fact`

```diff
@@ -13 +13,2 @@
+answer = str(answer)
```

### `k-4-d-4/task_11.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In the school district office listings, entries with CITY equal to Princeton and NMCNTY equal to Mercer County share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='Princeton' and NMCNTY='Mercer County' share what two-digit state FIPS code (STFIP)?`

- Node 2 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most public schools? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 3 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most private schools? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 4 `subquestion`
  - copy: `For STFIP equal to <node 1 answer>, which 3 county names have the most school district offices? Return the county names separated by;.`
  - tasks_mini: `For STFIP='<node_1 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 5 `subquestion`
  - copy: `Among <hop 2 answer>, which single county has the most postsecondary institutions in STFIP equal to <node 1 answer>? Answer with the county name including the word County.`
  - tasks_mini: `Let A be the set of counties in <node_2 answer>, B be the set of counties in <node_3 answer>, and C be the set of counties in <node_4 answer>. Consider the intersection of A, B, and C. Among those counties, which single county has the most postsecondary institutions in STFIP='<node_1 answer>'? Answer with the county name including the word 'County'.`

- Node 6 `subquestion`
  - copy: `How many public schools have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many public schools have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 6 `answer`
  - copy: `288`
  - tasks_mini: `288`

- Node 6 `fact`

```diff
@@ -20 +20,2 @@
+answer = str(answer)
```

- Node 7 `subquestion`
  - copy: `How many private schools have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many private schools have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 7 `answer`
  - copy: `91`
  - tasks_mini: `91`

- Node 7 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 8 `subquestion`
  - copy: `How many school district offices have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many school district offices have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 8 `answer`
  - copy: `81`
  - tasks_mini: `81`

- Node 8 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

- Node 9 `subquestion`
  - copy: `How many postsecondary institutions have NMCNTY equal to <hop 3 answer> and STFIP equal to <node 1 answer>?`
  - tasks_mini: `How many postsecondary institutions have NMCNTY='<node_5 answer>' and STFIP='<node_1 answer>'?`

- Node 9 `answer`
  - copy: `16`
  - tasks_mini: `16`

- Node 9 `fact`

```diff
@@ -14 +14,2 @@
+answer = str(answer)
```

### `k-4-d-4/task_12.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Texas counties had highway construction expenditures between $150 million and $500 million in fiscal year 2018?`
  - tasks_mini: `Which Texas counties had highway construction expenditures between $150 million and $500 million in fiscal year 2018? (Filter Fiscal Year == 2018; Major Spending Category == 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'; sum Amount by County.)`

- Node 5 `subquestion`
  - copy: `Among <hop 1 answer>, which Texas counties had fewer than 15,000 VA disability compensation recipients in FY 2023?`
  - tasks_mini: `Of the four Texas counties in the intersection (BEXAR, DENTON, NUECES, TARRANT), which had fewer than 15,000 VA disability compensation recipients in FY 2023?`

- Node 5 `answer`
  - copy: `["Nueces", "Denton"]`
  - tasks_mini: `["DENTON", "NUECES"]`

- Node 5 `fact`

```diff
@@ -6,9 +6,13 @@
-source = 'datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj['Body'].read()), low_memory=False)
-
-counties = ['Bexar', 'Denton', 'Nueces', 'Tarrant']
```

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The county seat is Denton.
+Denton County is located in the U.S. state of Texas. The county seat is Denton, which has the same name as the county itself.
```

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The county seat is Corpus Christi
+Nueces County is located in the southern part of Texas. The county seat is Corpus Christi, which has a different name than the county.
```

- Node 8 `source`
  - copy: `wikipedia/Corpus_Christi,_Texas/content.txt`
  - tasks_mini: `wikipedia/Tarrant_County,_Texas/content.txt`

- Node 8 `subquestion`
  - copy: `Who founded the first permanent settlement in the county seat of <hop 2 answer>?`
  - tasks_mini: `What is the county seat of Tarrant County, Texas?`

- Node 8 `answer`
  - copy: `Henry Lawrence Kinney`
  - tasks_mini: `Fort Worth`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-In 1839, the first known permanent settlement of Corpus Christi was established by Colonel Henry Lawrence Kinney and William P. Aubrey as Kinney's Trading Post, or Kinney's Ranch.
+Tarrant County is located in Texas with a 2020 census population of 2,110,640. Its county seat is Fort Worth, which has a different name than the county.
```

- Node 9 `source`
  - copy: `wikipedia/Kinney_County,_Texas/content.txt`
  - tasks_mini: `wikipedia/Corpus_Christi,_Texas/content.txt`

- Node 9 `subquestion`
  - copy: `In what year was the Texas county named after <hop 3 answer> created?`
  - tasks_mini: `Who founded the first permanent settlement in <intersection result: NUECES County>'s county seat (Corpus Christi)?`

- Node 9 `answer`
  - copy: `1850`
  - tasks_mini: `Henry Lawrence Kinney`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The county was created in 1850 and later organized in 1874. It is named for Henry Lawrence Kinney, an early settler.
+In 1839, the first known permanent settlement of Corpus Christi was established by Colonel Henry Lawrence Kinney and William P. Aubrey as Kinney's Trading Post, or Kinney's Ranch. The settlement was incorporated as Corpus Christi on September 9, 1852.
```

### `k-4-d-4/task_13.json`
- Impact: major
- Node 5 `subquestion`
  - copy: `Among the Providence properties from <hop 1 answer>, which have owner names that match incorporated places in Rhode Island according to the national-incorporated-places dataset?`
  - tasks_mini: `Of the three properties in the intersection (City of Providence, RI Hospital, Brown University), which have owner names that match incorporated places in Rhode Island according to the national-incorporated-places dataset?`

- Node 7 `subquestion`
  - copy: `Who created a bequest that provided early funding for <hop 2 answer>?`
  - tasks_mini: `Who created a bequest that provided early funding for Rhode Island Hospital?`

- Node 8 `subquestion`
  - copy: `Who was the grandfather of the person after whom <hop 3 answer> was named?`
  - tasks_mini: `Who was the grandfather of Moses Brown, after whom <node_7 answer> was named?`

### `k-4-d-4/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which CPS public elementary schools in the 2011-2012 progress report cards had CPS Performance Policy Level "Level 1"?`
  - tasks_mini: `Which elementary schools had CPS Performance Policy Level "Level 1" in the 2011-2012 CPS Progress Report Cards?`

- Node 1 `answer`
  - copy: `{"Abraham Lincoln Elementary School": "610038", "Alexander Graham Bell Elementary School": "609799", "Christopher Columbus Elementary School": "609863", "Durkin Park Elementary School": "610352", "Edison Park Elementary School": "610523", "Eliza Chappell Elementary School": "609852", "Frank W Gunsaulus Elementary Scholastic Academy": "609958", "John Calhoun...`
  - tasks_mini: `{"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 123 others": "..."}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/chicago-public-schools-progress-report-cards-2011-2012/files/rows.txt"
+source = 'datagov/chicago-public-schools-progress-report-cards-2011-2012/files/rows.txt'
@@ -10,14 +10,13 @@
-
-mask = (
-    (df["Elementary, Middle, or High School"] == "ES")
-    & (df["CPS Performance Policy Level"] == "Level 1")
```

- Node 2 `subquestion`
  - copy: `Which schools in the 2012-2013 CPS elementary progress report card had Growth Overall Level "Above Average"?`
  - tasks_mini: `Which schools in the 2012-2013 CPS elementary progress report card have Growth Overall Level "Above Average"?`

- Node 2 `answer`
  - copy: `{"Addams": "609772", "Armstrong, G": "609779", "Clissold": "609861", "Dixon": "609887", "Greene": "609952", "Irving": "610121", "Lasalle Ii": "610520", "Mays": "610290", "Nash": "610092", "Thorp, O": "610201"}`
  - tasks_mini: `{"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 226 others": "..."}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/chicago-public-schools-elementary-school-progress-report-card-2012-2013/files/rows.txt"
+source = 'datagov/chicago-public-schools-elementary-school-progress-report-card-2012-2013/files/rows.txt'
@@ -10,11 +10,12 @@
-
-mask = df["Growth Overall Level"] == "Above Average"
-
-answer = dict(
```

- Node 3 `subquestion`
  - copy: `Which schools in the 2013-2014 CPS progress report source had My Voice, My School Overall Rating "MODERATELY ORGANIZED"?`
  - tasks_mini: `Which schools in the 2013-2014 CPS elementary progress report have My Voice, My School Overall Rating "MODERATELY ORGANIZED"?`

- Node 3 `answer`
  - copy: `{"Amos Alonzo Stagg Elementary School": "610339", "Arthur R Ashe Elementary School": "610268", "Edgar Allan Poe Elementary Classical School": "610132", "Federico Garcia Lorca Elementary School": "610541", "Frederic Chopin Elementary School": "609854", "Jacob Beidler Elementary School": "609797", "Lyman A Budlong Elementary School": "609817", "Mildred I Lavi...`
  - tasks_mini: `{"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 38 others": "..."}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/chicago-public-schools-elementary-school-progress-report-2013-2014/files/rows.txt"
+source = 'datagov/chicago-public-schools-elementary-school-progress-report-2013-2014/files/rows.txt'
@@ -10,11 +10,12 @@
-
-mask = df["My Voice, My School Overall Rating"] == "MODERATELY ORGANIZED"
-
-answer = dict(
```

- Node 4 `subquestion`
  - copy: `Which schools showed above-average or far-above-average student growth in 2017-18?`
  - tasks_mini: `Which Chicago Public Schools had Student_Growth_Rating "ABOVE AVERAGE" or "FAR ABOVE AVERAGE" in school year 2017-18?`

- Node 4 `answer`
  - copy: `{"ASHE": "610268", "BRUNSON": "609830", "CALMECA": "610353", "CLINTON": "609859", "CURTIS": "609900", "DIRKSEN": "609874", "KELLER": "610084", "LAVIZZO": "610208", "MURRAY": "610090", "NIGHTINGALE": "610096"}`
  - tasks_mini: `{"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 295 others": "..."}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/chicago-public-schools-school-progress-reports-sy1718/files/rows.txt"
+source = 'datagov/chicago-public-schools-school-progress-reports-sy1718/files/rows.txt'
@@ -10,11 +10,12 @@
-
-mask = df["Student_Growth_Rating"].isin(["ABOVE AVERAGE", "FAR ABOVE AVERAGE"])
-
-answer = dict(
```

- Node 5 `subquestion`
  - copy: `In which community areas are the schools from <hop 1 answer> located, according to CPS School Locations SY2015-16?`
  - tasks_mini: `In which community areas are the schools that meet all four progress-report criteria located, according to CPS School Locations SY2015-16?`

- Node 5 `answer`
  - copy: `{"CLEVELAND": "IRVING PARK", "HAWTHORNE": "LAKE VIEW", "POE": "PULLMAN", "REINBERG": "PORTAGE PARK"}`
  - tasks_mini: `{"Cleveland": "Irving Park", "Hawthorne": "Lake View", "Poe": "Pullman", "Reinberg": "Portage Park"}`

- Node 5 `fact`

```diff
@@ -10,12 +10,9 @@
-
-
-answer = dict(
-    zip(
-        df.loc[mask, "Short_Name"],
-        df.loc[mask, "COMMAREA"]
```

- Node 6 `subquestion`
  - copy: `Among the community areas from <node_5 answer>, which have per capita income above $50,000 in the 2008-2012 Chicago census dataset?`
  - tasks_mini: `Which of those community areas has per capita income above $50,000?`

- Node 7 `subquestion`
  - copy: `Which MLB team plays at the stadium located in <hop 3 answer>?`
  - tasks_mini: `Which MLB team plays at the MLB stadium in the Lakeview community area (<node_6 answer>)?`

- Node 7 `fact`

```diff
@@ -1,3 +1 @@
-Wrigley Field () is a ballpark on the North Side of Chicago, Illinois, United States. It is the home ballpark of Major League Baseball's Chicago Cubs, one of the city's two MLB franchises. It first opened in 1914 as Weeghman Park for Charles Weeghman's Chicago Whales of the Federal League, which folded after the 1915 baseball season. The Cubs played their first home game at the park on April 20, 1916. Chewing gum magnate William Wrigley Jr. of the Wrigley Company acquired the Cubs in 1921. It was named Cubs Park from 1920 to 1926, before changing its name to Wrigley Field in 1927. The stadium currently seats 41,649 people.
-
-In the North Side community area of Lakeview in the Wrigleyville neighborhood, Wrigley Field
+Wrigley Field is a ballpark on the North Side of Chicago and is the home ballpark of Major League Baseball's Chicago Cubs. It is in the North Side community area of Lakeview in Chicago.
```

- Node 8 `subquestion`
  - copy: `In what year was <hop 3 answer> established?`
  - tasks_mini: `In what year was that MLB team (<node_7 answer>) established?`

- Node 8 `fact`

```diff
@@ -1,2 +1 @@
-Category:1876 establishments in Illinois
-Category:Baseball teams established in 1876
+The Chicago Cubs article includes the category "Baseball teams established in 1876" (and "1876 establishments in Illinois"), indicating the team was established in 1876.
```

### `k-4-d-4/task_3.json`
- Impact: major
- Node 1 `answer`
  - copy: `{"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 167 ROBERT F. WAGNER": "02M167", "M.S. 255 SALK SCHOOL OF SCIENCE": "02M255", "M.S. 51 WILLIAM ALEXANDER": "15K051", "NEW EXPLORATIONS INTO SCIENCE, TECHNOLOGY AND MATH SCHOOL": "01M539", "NEW YORK CITY LAB MIDDLE SCHOOL FOR COLLAB...`
  - tasks_mini: `{"J.H.S. 067 Louis Pasteur": "26Q067, 84 offers", "J.H.S. 074 Nathaniel Hawthorne": "26Q074, 102 offers", "J.H.S. 216 George J. Ryan": "26Q216, 92 offers", "M.S. 158 Marie Curie": "26Q158, 104 offers", "and 23 others": "..."}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/2015-2016-shsat-admissions-test-offers-by-sending-school/files/rows.txt"
+source = 'datagov/2015-2016-shsat-admissions-test-offers-by-sending-school/files/rows.txt'
@@ -10,7 +10,9 @@
-
-offers = pd.to_numeric(df["Count of Offers"], errors="coerce")
-mask = offers >= 50
-
```

- Node 2 `answer`
  - copy: `{"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 167 ROBERT F. WAGNER": "02M167", "M.S. 255 SALK SCHOOL OF SCIENCE": "02M255", "M.S. 51 WILLIAM ALEXANDER": "15K051", "NEW EXPLORATIONS INTO SCIENCE, TECHNOLOGY AND MATH SCHOOL": "01M539", "NEW YORK CITY LAB MIDDLE SCHOOL FOR COLLAB...`
  - tasks_mini: `{"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 158 Marie Curie": "26Q158", "and 23 others": "..."}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/2016-2017-shsat-admissions-test-offers-by-sending-school/files/rows.txt"
+source = 'datagov/2016-2017-shsat-admissions-test-offers-by-sending-school/files/rows.txt'
@@ -10,7 +10,9 @@
-
-offers = pd.to_numeric(df["Count of Offers"], errors="coerce")
-mask = offers >= 50
-
```

- Node 3 `answer`
  - copy: `{"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 167 ROBERT F. WAGNER": "02M167", "M.S. 255 SALK SCHOOL OF SCIENCE": "02M255", "M.S. 51 WILLIAM ALEXANDER": "15K051", "NEW EXPLORATIONS INTO SCIENCE, TECHNOLOGY AND MATH SCHOOL": "01M539", "NEW YORK CITY LAB MIDDLE SCHOOL FOR COLLAB...`
  - tasks_mini: `{"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 158 Marie Curie": "26Q158", "and 24 others": "..."}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/2017-2018-shsat-admissions-test-offers-by-sending-school/files/rows.txt"
+source = 'datagov/2017-2018-shsat-admissions-test-offers-by-sending-school/files/rows.txt'
@@ -10,7 +10,9 @@
-
-offers = pd.to_numeric(df["Count of Offers"], errors="coerce")
-mask = offers >= 50
-
```

- Node 4 `answer`
  - copy: `{"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 167 ROBERT F. WAGNER": "02M167", "M.S. 255 SALK SCHOOL OF SCIENCE": "02M255", "M.S. 51 WILLIAM ALEXANDER": "15K051", "NEW EXPLORATIONS INTO SCIENCE, TECHNOLOGY AND MATH HIGH SCHOOL": "01M539", "NEW YORK CITY LAB MIDDLE SCHOOL FOR C...`
  - tasks_mini: `{"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 158 Marie Curie": "26Q158", "and 19 others": "..."}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -6,3 +6,3 @@
-source = "datagov/2018-2019-shsat-admissions-test-offers-by-sending-school/files/rows.txt"
+source = 'datagov/2018-2019-shsat-admissions-test-offers-by-sending-school/files/rows.txt'
@@ -10,7 +10,9 @@
-
-offers = pd.to_numeric(df["Number of Offers"], errors="coerce")
-mask = offers >= 50
-
```

- Node 5 `subquestion`
  - copy: `Which of the schools with at least 50 specialized high school admissions test offers in all four years are located in Queens District 26?`
  - tasks_mini: `Which of the 21 schools with >= 50 SHSAT offers in all 4 years are located in Queens District 26?`

- Node 5 `fact`

```diff
@@ -1 +1,16 @@
-According to NYC DOE School Locations data for 2016-17, four schools from the intersection are in Queens District 26: J.H.S. 067 Louis Pasteur (26Q067) in Douglas Manor-Douglaston-Little Neck (NTA QN45), J.H.S. 074 Nathaniel Hawthorne (26Q074) in Oakland Gardens (NTA QN42), M.S. 158 Marie Curie (26Q158) in Bayside-Bayside Hills (NTA QN46), and J.H.S. 216 George J. Ryan (26Q216) in Fresh Meadows-Utopia (NTA QN41). The GEOGRAPHICAL_DISTRICT_CODE for all four is 26.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 9 `source`
  - copy: `wikipedia/Board_of_Regents_of_the_University_of_the_State_of_New_York/content.txt`
  - tasks_mini: `wikipedia/Pasteur_Institute/content.txt`

- Node 9 `subquestion`
  - copy: `Was George J. Ryan a scientist?`
  - tasks_mini: `In what year was the research institute named after <the older scientist from nodes 6-7: Louis Pasteur> founded?`

- Node 9 `answer`
  - copy: `No, he was an education/governance figure`
  - tasks_mini: `1887`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-At Large Seat 2 George J. Ryan February 10, 1937 replaced Robert W. Higbie March 31, 1941 term ended.
+The Pasteur Institute is a French non-profit private foundation dedicated to the study of biology, micro-organisms, diseases, and vaccines. It is named after Louis Pasteur. The institute was founded on 4 June 1887 and inaugurated on 14 November 1888.
```

### `k-4-d-4/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the terminus cities of Route 66?`
  - tasks_mini: `What are the terminus cities of the highway that was born in Springfield, Missouri?`

- Node 2 `subquestion`
  - copy: `For the Route 66 terminus cities from <hop 1 answer>, what was the city-level crude prevalence of binge drinking in the 2016 release?`
  - tasks_mini: `Which terminus city (from <node_1 answer>) had higher average binge drinking prevalence across the 2016 and 2018 city health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 3 `subquestion`
  - copy: `For the Route 66 terminus cities from <hop 1 answer>, what was the city-level crude prevalence of binge drinking in the 2018 release?`
  - tasks_mini: `Which terminus city (from <node_1 answer>) had higher average binge drinking prevalence across the 2016 and 2018 city health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 4 `subquestion`
  - copy: `In <hop 2 answer>, what were the total overtime costs by department in 2014?`
  - tasks_mini: `Which city department had the highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 4 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 5 `subquestion`
  - copy: `In <hop 2 answer>, what were the total overtime costs by department in 2015?`
  - tasks_mini: `Which city department had the highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 5 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 6 `subquestion`
  - copy: `In <hop 2 answer>, what were the total overtime costs by department in 2016?`
  - tasks_mini: `Which city department had the highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 6 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 7 `subquestion`
  - copy: `In <hop 2 answer>, what were the total overtime costs by department in 2017?`
  - tasks_mini: `Which city department had the highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 7 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 8 `subquestion`
  - copy: `What is the starting salary in 2025 for officers in <hop 3 answer>?`
  - tasks_mini: `What is the starting salary in 2025 for officers in the department identified in the overtime comparison?`

### `k-4-d-4/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What were the total expenditures by Missouri state agency in FY2007?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2007; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 1 `answer`
  - copy: `{"CORRECTIONS": 279877976.24, "ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HEALTH AND SENIOR SERVICES": 698796366.98, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "MENTAL HEALTH": 759892459.14, "OFFICE OF ADMINISTRATION": 369596080.22, "PUBLIC SAFETY": 247925806.08, "REVENUE": 373724618.79, "SOCIAL SERVICES": 5528171459.84, "TRANSPORTATION"...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "MENTAL HEALTH": 759892459.14, "SOCIAL SERVICES": 5528171459.84, "TRANSPORTATION": 1922237354.88}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `subquestion`
  - copy: `What were the total expenditures by Missouri state agency in FY2008?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2008; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 2 `answer`
  - copy: `{"CORRECTIONS": 279260171.22, "ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HEALTH AND SENIOR SERVICES": 734833032.4, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "MENTAL HEALTH": 813799778.73, "OFFICE OF ADMINISTRATION": 466398986.98, "PUBLIC SAFETY": 293606432.85, "REVENUE": 387774187.98, "SOCIAL SERVICES": 5988522037.62, "TRANSPORTATION":...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "MENTAL HEALTH": 813799778.73, "SOCIAL SERVICES": 5988522037.62, "TRANSPORTATION": 1786534604.37}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `subquestion`
  - copy: `What were the total expenditures by Missouri state agency in FY2009?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2009; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 3 `answer`
  - copy: `{"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HEALTH AND SENIOR SERVICES": 815631750.83, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "MENTAL HEALTH": 877438429.19, "NATURAL RESOURCES": 292863341.01, "OFFICE OF ADMINISTRATION": 497442735.68, "PUBLIC SAFETY": 301774658.68, "REVENUE": 371129680.47, "SOCIAL SERVICES": 6707806742.86, "TRANSPORT...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "MENTAL HEALTH": 877438429.19, "SOCIAL SERVICES": 6707806742.86, "TRANSPORTATION": 2000940522.19}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `subquestion`
  - copy: `What were the total expenditures by Missouri state agency in FY2010?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2010; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 4 `answer`
  - copy: `{"CORRECTIONS": 268435627.28, "ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HEALTH AND SENIOR SERVICES": 884344054.25, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "MENTAL HEALTH": 921056914.52, "OFFICE OF ADMINISTRATION": 439597907.95, "PUBLIC SAFETY": 333299335.44, "REVENUE": 370228371.58, "SOCIAL SERVICES": 7141666880.32, "TRANSPORTATION"...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "MENTAL HEALTH": 921056914.52, "SOCIAL SERVICES": 7141666880.32, "TRANSPORTATION": 2144139919.08}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `subquestion`
  - copy: `In which city is the Southwest district of <hop 1 answer> based?`
  - tasks_mini: `In which city is the Southwest district of the agency (from hop 1: TRANSPORTATION/MoDOT) based?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Southwest, based in Springfield
+According to the Wikipedia article for Missouri Department of Transportation, 'MoDOT operates seven districts throughout the state: Northwest, based in St. Joseph; Northeast, based in Hannibal; Kansas City, based in Lee's Summit; Central, based in Jefferson City; St. Louis, based in Chesterfield; Southwest, based in Springfield; and Southeast, based in Sikeston.'
```

- Node 6 `subquestion`
  - copy: `What are the terminus cities of the highway that was born in <hop 2 answer>?`
  - tasks_mini: `What are the terminus cities of the highway that was born in the city identified in the previous step?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.
+According to the Wikipedia article for Springfield, Missouri, 'Springfield's nicknames include "Queen City of the Ozarks" and "The Birthplace of Route 66"...Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.'
```

- Node 7 `subquestion`
  - copy: `For the Route 66 terminus cities from <hop 3 answer>, what was the city-level crude prevalence of binge drinking in the 2016 release?`
  - tasks_mini: `Which terminus city (from <node_6 answer>) had lower average binge drinking prevalence across the 2016 and 2018 city health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 8 `subquestion`
  - copy: `For the Route 66 terminus cities from <hop 3 answer>, what was the city-level crude prevalence of binge drinking in the 2018 release?`
  - tasks_mini: `Which terminus city (from <node_6 answer>) had lower average binge drinking prevalence across the 2016 and 2018 city health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

### `k-4-d-4/task_6.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1 +1 @@
-In the Wikipedia county table, Austin, Bastrop, Bexar, Brazoria, Colorado, Fayette, Goliad, Gonzales, Harris, Jackson, Jasper, Jefferson, Liberty, Matagorda, Milam, Nacogdoches, Red River, Refugio, Sabine, San Augustine, San Patricio, Shelby, and Victoria are marked as one of the original 23 counties.
+The Republic of Texas created 23 original counties in 1836: Austin, Bastrop, Bexar, Brazoria, Colorado, Fayette, Goliad, Gonzales, Harris, Jackson, Jasper, Jefferson, Liberty, Matagorda, Milam, Nacogdoches, Red River, Refugio, Sabine, San Augustine, San Patricio, Shelby, and Victoria.
```

- Node 2 `subquestion`
  - copy: `What were the FY2018 capital outlay expenditure totals by Texas county?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2018; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 2 `answer`
  - copy: `{"BEXAR": 269462082.97, "DALLAS": 838316444.65, "DENTON": 186170844.17, "EL PASO": 123694754.23, "HARRIS": 1303630847.3, "HAYS": 180311763.03, "MONTGOMERY": 424383088.05, "NUECES": 180007685.62, "TARRANT": 195326742.86, "TRAVIS": 427160745.36}`
  - tasks_mini: `{"Bexar": 269462082.97, "Dallas": 838316444.65, "Harris": 1303630847.3, "Montgomery": 424383088.05, "Travis": 427160745.36}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-state-expenditures-by-county-2018/files/rows.txt"
+
+source = 'datagov/texas-state-expenditures-by-county-2018/files/rows.txt'
@@ -9,3 +10,8 @@
-mask = ((df["Fiscal Year"] == 2018) & df["County"].notna() & (df["County"].astype(str).str.strip() != "") & df["Major Spending Category"].astype(str).str.contains("CAPITAL OUTLAY", na=False))
-answer = (df.loc[mask].groupby("County")["Amount"].sum().sort_values(ascending=False).round(2).to_dict())
+df["Fiscal Year"] = pd.to_numeric(df["Fiscal Year"], errors="coerce")
```

- Node 3 `subquestion`
  - copy: `What were the FY2019 capital outlay expenditure totals by Texas county?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2019; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 3 `answer`
  - copy: `{"BEXAR": 302940592.72, "DALLAS": 827510409.8, "DENTON": 260841655.76, "HARRIS": 1391779835.06, "HAYS": 154023926.62, "MONTGOMERY": 416744287.28, "NUECES": 243549894.71, "TARRANT": 180443982.39, "TRAVIS": 614936080.37, "WILLIAMSON": 162099329.96}`
  - tasks_mini: `{"Bexar": 302940592.72, "Dallas": 827510409.8, "Harris": 1391779835.06, "Montgomery": 416744287.28, "Travis": 614936080.37}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-state-expenditures-by-county-2019/files/rows.txt"
+
+source = 'datagov/texas-state-expenditures-by-county-2019/files/rows.txt'
@@ -9,3 +10,8 @@
-mask = ((df["Fiscal Year"] == 2019) & df["County"].notna() & (df["County"].astype(str).str.strip() != "") & df["Major Spending Category"].astype(str).str.contains("CAPITAL OUTLAY", na=False))
-answer = (df.loc[mask].groupby("County")["Amount"].sum().sort_values(ascending=False).round(2).to_dict())
+df["Fiscal Year"] = pd.to_numeric(df["Fiscal Year"], errors="coerce")
```

- Node 4 `subquestion`
  - copy: `What were the FY2020 capital outlay expenditure totals by Texas county?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2020; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 4 `answer`
  - copy: `{"BEXAR": 494340352.72, "DALLAS": 1324261419.12, "DENTON": 355805325.9, "HARRIS": 1663151150.96, "HAYS": 251859833.02, "MCLENNAN": 171511743.04, "MONTGOMERY": 612813968.49, "NUECES": 350680573.97, "TARRANT": 189569631.26, "TRAVIS": 821945717.49}`
  - tasks_mini: `{"Bexar": 494340352.72, "Dallas": 1324261419.12, "Harris": 1663151150.96, "Montgomery": 612813968.49, "Travis": 821945717.49}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-state-expenditures-by-county-2020/files/rows.txt"
+
+source = 'datagov/texas-state-expenditures-by-county-2020/files/rows.txt'
@@ -9,3 +10,8 @@
-mask = ((df["Fiscal Year"] == 2020) & df["County"].notna() & (df["County"].astype(str).str.strip() != "") & df["Major Spending Category"].astype(str).str.contains("CAPITAL OUTLAY", na=False))
-answer = (df.loc[mask].groupby("County")["Amount"].sum().sort_values(ascending=False).round(2).to_dict())
+df["Fiscal Year"] = pd.to_numeric(df["Fiscal Year"], errors="coerce")
```

- Node 5 `subquestion`
  - copy: `What were the FY2021 capital outlay expenditure totals by Texas county?`
  - tasks_mini: `Which Texas counties were in the top 5 by average Capital Outlay expenditures across 2018-2021? (Filter for this node: Fiscal Year == 2021; Major Spending Category contains 'CAPITAL OUTLAY' (including 'HIGHWAY CONSTRUCTION-CAPITAL OUTLAY'); non-empty County; sum Amount by County.)`

- Node 5 `answer`
  - copy: `{"BEXAR": 596386366.99, "DALLAS": 1171406639.17, "DENTON": 412077419.13, "EL PASO": 144869614.83, "HARRIS": 1741663003.68, "HAYS": 242238383.67, "MONTGOMERY": 705433711.03, "NUECES": 165289397.9, "TARRANT": 228788736.63, "TRAVIS": 774601022.23}`
  - tasks_mini: `{"Bexar": 596386366.99, "Dallas": 1171406639.17, "Harris": 1741663003.68, "Montgomery": 705433711.03, "Travis": 774601022.23}`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-state-expenditures-by-county-2021/files/rows.txt"
+
+source = 'datagov/texas-state-expenditures-by-county-2021/files/rows.txt'
@@ -9,3 +10,8 @@
-mask = ((df["Fiscal Year"] == 2021) & df["County"].notna() & (df["County"].astype(str).str.strip() != "") & df["Major Spending Category"].astype(str).str.contains("CAPITAL OUTLAY", na=False))
-answer = (df.loc[mask].groupby("County")["Amount"].sum().sort_values(ascending=False).round(2).to_dict())
+df["Fiscal Year"] = pd.to_numeric(df["Fiscal Year"], errors="coerce")
```

- Node 6 `subquestion`
  - copy: `For the counties from <hop 1 answer>, what were the TDCJ release counts in FY2019?`
  - tasks_mini: `For counties in <aggregation of nodes 2-5> that are not among <node_1>, what were the Texas Department of Criminal Justice release counts in 2019 and 2020? (Filter for this node: County in {Dallas, Travis, Montgomery}; count rows by County.)`

- Node 6 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2019/files/rows.txt"
+
+source = 'datagov/texas-department-of-criminal-justice-releases-fy-2019/files/rows.txt'
@@ -9,5 +10,9 @@
-candidates = ["Dallas", "Travis", "Montgomery"]
-county = df["County"].astype(str).str.strip().str.title()
-counts = county[county.isin(candidates)].value_counts()
```

- Node 7 `subquestion`
  - copy: `For the counties from <hop 1 answer>, what were the TDCJ release counts in FY2020?`
  - tasks_mini: `For counties in <aggregation of nodes 2-5> that are not among <node_1>, what were the Texas Department of Criminal Justice release counts in 2019 and 2020? (Filter for this node: County in {Dallas, Travis, Montgomery}; count rows by County.)`

- Node 7 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2020/files/rows.txt"
+
+source = 'datagov/texas-department-of-criminal-justice-releases-fy-2020/files/rows.txt'
@@ -9,5 +10,9 @@
-candidates = ["Dallas", "Travis", "Montgomery"]
-county = df["County"].astype(str).str.strip().str.title()
-counts = county[county.isin(candidates)].value_counts()
```

- Node 8 `subquestion`
  - copy: `For <hop 2 answer>, how many disability compensation recipients were recorded in FY2020?`
  - tasks_mini: `For the county with the highest average releases, what were the U.S. Department of Veterans Affairs disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name == Dallas; use Total: Disability Compensation Recipients.)`

- Node 8 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/fy-2020-disability-compensation-recipients-by-county/files/rows.txt"
+
+source = 'datagov/fy-2020-disability-compensation-recipients-by-county/files/rows.txt'
@@ -9,2 +10,5 @@
-answer = int(df.loc[(df["State"] == "Texas") & (df["County Name"] == "Dallas"), "Total: Disability Compensation Recipients"].iloc[0])
+mask = (df["State"].astype(str) == "Texas") & (df["County Name"].astype(str).str.lower().str.startswith("dallas"))
+value_col = "TOTAL" if "TOTAL" in df.columns else "Total"
```

- Node 9 `subquestion`
  - copy: `For <hop 2 answer>, how many disability compensation recipients were recorded in FY2023?`
  - tasks_mini: `For the county with the highest average releases, what were the U.S. Department of Veterans Affairs disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name == Dallas; use Total: Disability Compensation Recipients.)`

- Node 9 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt"
+
+source = 'datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt'
@@ -9,2 +10,5 @@
-answer = int(df.loc[(df["State"] == "Texas") & (df["County Name"] == "Dallas"), "Total: Disability Compensation Recipients"].iloc[0])
+mask = (df["State"].astype(str) == "Texas") & (df["County Name"].astype(str).str.lower().str.startswith("dallas"))
+value_col = "TOTAL" if "TOTAL" in df.columns else "Total"
```

### `k-4-d-4/task_7.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What was the total overtime for each Chicago department in 2018, so it can be combined with 2019-2021 to identify the department with the highest 2018-2021 average overtime?`
  - tasks_mini: `What was the total overtime for each Chicago department in 2018?`

- Node 1 `answer`
  - copy: `{"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47000000003, "Aviation": 19982790.57, "Board of Election Commissioners": 440272.38, "Buildings": 794904.4199999999, "City Clerk": 124444.24, "Civilian Office of Police Accountability": 34097.009999999995, "Emergency Management and Communications": 9791878.49, "Family and Support Services...`
  - tasks_mini: `{"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47, "Aviation": 19982790.57, "Board of Election Commissioners": 440272.38, "Buildings": 794904.42, "City Clerk": 124444.24, "Civilian Office of Police Accountability": 34097.01, "Emergency Management and Communications": 9791878.49, "Family and Support Services": 74560.11, "Finance": 234...`

- Node 2 `subquestion`
  - copy: `What was the total overtime for each Chicago department in 2019, so it can be combined with 2018, 2020, and 2021 to identify the department with the highest 2018-2021 average overtime?`
  - tasks_mini: `What was the total overtime for each Chicago department in 2019?`

- Node 2 `answer`
  - copy: `{"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.01, "CHICAGO DEPARTMENT OF TRANSPORTATION": 8372582.5200000005, "CHICAGO FIRE DEPARTMENT": 85821080.71, "CHICAGO POLICE DEPARTMENT": 139560316.72, "CHICAGO PUBLIC LIBRARY": 819490.63, "CITY CLERK": 69224.75, "CITY COUNCIL": 1695.88, "CIVILIAN OFFICE OF POLICE ACCOUNTABIL...`
  - tasks_mini: `{"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.01, "CHICAGO DEPARTMENT OF TRANSPORTATION": 8372582.52, "CHICAGO FIRE DEPARTMENT": 85821080.71, "CHICAGO POLICE DEPARTMENT": 139560316.72, "CHICAGO PUBLIC LIBRARY": 819490.63, "CITY CLERK": 69224.75, "CITY COUNCIL": 1695.88, "CIVILIAN OFFICE OF POLICE ACCOUNTABILITY": 39...`

- Node 3 `subquestion`
  - copy: `What was the total overtime for each Chicago department in 2020, so it can be combined with 2018, 2019, and 2021 to identify the department with the highest 2018-2021 average overtime?`
  - tasks_mini: `What was the total overtime for each Chicago department in 2020?`

- Node 3 `answer`
  - copy: `{"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605.54, "CHICAGO DEPARTMENT OF TRANSPORTATION": 9632321.67, "CHICAGO FIRE DEPARTMENT": 95352235.07, "CHICAGO POLICE DEPARTMENT": 177486176.09, "CHICAGO PUBLIC LIBRARY": 292667.06, "CITY CLERK": 30310.92, "CIVILIAN OFFICE OF POLICE ACCOUNTABILITY": 59757.02, "DEPARTMENT OF A...`
  - tasks_mini: `{"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605.54, "CHICAGO DEPARTMENT OF TRANSPORTATION": 9632321.67, "CHICAGO FIRE DEPARTMENT": 95352235.07, "CHICAGO POLICE DEPARTMENT": 177486176.09, "CHICAGO PUBLIC LIBRARY": 292667.06, "CITY CLERK": 30310.92, "CIVILIAN OFFICE OF POLICE ACCOUNTABILITY": 59757.02, "DEPARTMENT OF A...`

- Node 4 `subquestion`
  - copy: `What was the total overtime for each Chicago department in 2021, so it can be combined with 2018-2020 to identify the department with the highest 2018-2021 average overtime?`
  - tasks_mini: `What was the total overtime for each Chicago department in 2021?`

- Node 4 `answer`
  - copy: `{"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4, "Chicago Department of Transportation": 10080051.62, "Chicago Fire Department": 82732370.06, "Chicago Police Department": 134342334.79, "Chicago Public Library": 355400.96, "City Clerk": 67303.82, "Civilian Office of Police Accountability": 20023.52, "Department of Ad...`
  - tasks_mini: `{"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4, "Chicago Department of Transportation": 10080051.62, "Chicago Fire Department": 82732370.06, "Chicago Police Department": 134342334.79, "Chicago Public Library": 355400.96, "City Clerk": 67303.82, "Civilian Office of Police Accountability": 20023.52, "Department of Ad...`

- Node 5 `subquestion`
  - copy: `Who was the first civilian superintendent of <hop 1 answer>?`
  - tasks_mini: `Who was the first civilian head of <department with highest average overtime from nodes 1-4>?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Orlando W. Wilson, the first civilian superintendent, was appointed by the mayor in 1960.
+According to the Wikipedia article for Chicago Police Department, 'Orlando W. Wilson, the first civilian superintendent, was appointed by the mayor in 1960.' Wilson served as Superintendent of Police until 1967.
```

- Node 6 `subquestion`
  - copy: `In which cities did <node_5 answer> serve as police chief before becoming head of <hop 1 answer>?`
  - tasks_mini: `In which cities did <person from node 5: O. W. Wilson> hold leadership positions before coming to Chicago?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-In 1925, Wilson became chief of police of the Fullerton Police Department for two years.  He then spent two years as an investigator with the Pacific Finance Corporation.  In 1928, at age 28, he became chief of police of the Wichita Police Department, where he served until 1939.
+According to the Wikipedia article for O. W. Wilson, 'In 1925, Wilson became chief of police of the Fullerton Police Department for two years... In 1928, at age 28, he became chief of police of the Wichita Police Department, where he served until 1939.'
```

- Node 7 `subquestion`
  - copy: `Which city from <hop 3 answer> was the one where <node_5 answer> started a criminal justice program at a local university?`
  - tasks_mini: `In which city from <cities from node 6: Fullerton, Wichita> did O. W. Wilson establish a criminal justice program at a university?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-A notable figure in the Department’s history was O.W. Wilson, who was considered an innovative police reformer.  Wilson was credited with starting the Criminal Justice Program at Wichita State University, previously called the Municipal University of Wichita in 1937.
+According to the Wikipedia article for Wichita Police Department, 'A notable figure in the Department's history was O.W. Wilson, who was considered an innovative police reformer. Wilson was credited with starting the Criminal Justice Program at Wichita State University, previously called the Municipal University of Wichita in 1937.'
```

- Node 8 `subquestion`
  - copy: `What county is <hop 4 answer> located in?`
  - tasks_mini: `What county is <city from node 7: Wichita> located in?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-is the most populous city in the U.S. state of Kansas and the county seat of Sedgwick County.
+According to the Wikipedia article for Wichita, Kansas, 'Wichita... is the most populous city in the U.S. state of Kansas and the county seat of Sedgwick County.'
```

### `k-4-d-4/task_8.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2017? Use semantic alias resolution for obvious same-contractor name variants before counting.`
  - tasks_mini: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2017?`

- Node 1 `answer`
  - copy: `["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead Architects", "McKinstry Essention, LLC", "Liberty Business Forms", "PBS Engineering+Environmental - Seattle", "WSP USA Inc.", "HDR Engineering, Inc.", "Schacht/Aslani Architects", "KMB architects", "Phoenix Protective Corp.", "Jacobs Engineering Group, Inc.", "MSGS Arc...`
  - tasks_mini: `["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead Architects", "McKinstry Essention, LLC", "Liberty Business Forms", "PBS Engineering+Environmental - Seattle", "WSP USA, Inc.", "HDR Engineering, Inc.", "Schacht/Aslani Architects", "KMB architects", "Phoenix Protective Corp.", "MSGS Architects", "KolorKraze", "Jacobs E...`

- Node 1 `fact`

```diff
@@ -6,15 +6,6 @@
-ALIASES = {'WSP USA Inc.': ['WSP USA, Inc.', 'WSP USA Inc.'], 'HDR Engineering, Inc.': ['HDR Engineering, Inc.', 'HDR Engineering', 'HDR ENGINEERING INC', 'Hdr Engineering Inc', 'HDR, INC'], 'Jacobs Engineering Group, Inc.': ['Jacobs Engineering Group, Inc.', 'Jacobs Engineering Group Inc', 'Jacobs Engineering Group'], 'A-1 Performance Inc': ['A-1 Performance Inc', 'A-1 Performance INC', 'A-1 Performance', 'A-1 Performance Inc.', 'A-1 Performance, Inc.', 'A-1 PERFORMANCE'], 'Imagesource Inc': ['Imagesource Inc', 'ImageSource, Inc.', 'ImageSource, Inc', 'ImageSource Inc.', 'IMAGESOURCE INC', 'ImageSource'], 'CenturyLink': ['CenturyLink', 'Centurylink', 'CENTURYLINK'], 'Shi International Corp': ['Shi International Corp', 'SHI International Corp', 'SHI INTERNATIONAL CORP.', 'SHI International Corp.', 'Shi International Corporation', 'SHI INTERNATIONAL CORP'], 'CodeSmart Inc': ['Codesmart Inc', 'Codesmart INC', 'CodeSmart Inc', 'CodeSmart', 'Codesmart', 'CodeSmart, Inc.', 'CodeSmart, Inc', 'Codesmart, INC.', 'Codesmart, Inc.', 'CODESMART INC'], 'Ricoh USA Inc': ['Ricoh Usa Inc', 'Ricoh USA', 'Ricoh USA, Inc.', 'RICOH USA INC', 'Ricoh USA Inc', 'RICOH USA', 'RICOH']...
```

- Node 2 `subquestion`
  - copy: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2018? Use semantic alias resolution for obvious same-contractor name variants before counting.`
  - tasks_mini: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2018?`

- Node 2 `answer`
  - copy: `["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "Imagesource Inc", "WSP USA Inc.", "HDR Engineering, Inc.", "HNTB Corporation", "GENUINE PARTS CO", "CodeSmart Inc", "Sharp Electronics Corporation", "SMS Cleaning Inc", "Correctional Industries-DOC", "Pioneer Human Services", "Ricoh USA Inc", "Puget Sound Executive Srvces Inc", "DOC Correctional Ind...`
  - tasks_mini: `["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "WSP USA Inc.", "Imagesource Inc", "HDR Engineering, Inc.", "HNTB Corporation", "GENUINE PARTS CO", "Sharp Electronics Corporation", "A-1 Performance INC", "Correctional Industries-DOC", "Pioneer Human Services", "Puget Sound Executive Srvces Inc", "Client Network Services Inc", "DOC Correctional Ind...`

- Node 2 `fact`

```diff
@@ -6,15 +6,6 @@
-ALIASES = {'WSP USA Inc.': ['WSP USA, Inc.', 'WSP USA Inc.'], 'HDR Engineering, Inc.': ['HDR Engineering, Inc.', 'HDR Engineering', 'HDR ENGINEERING INC', 'Hdr Engineering Inc', 'HDR, INC'], 'Jacobs Engineering Group, Inc.': ['Jacobs Engineering Group, Inc.', 'Jacobs Engineering Group Inc', 'Jacobs Engineering Group'], 'A-1 Performance Inc': ['A-1 Performance Inc', 'A-1 Performance INC', 'A-1 Performance', 'A-1 Performance Inc.', 'A-1 Performance, Inc.', 'A-1 PERFORMANCE'], 'Imagesource Inc': ['Imagesource Inc', 'ImageSource, Inc.', 'ImageSource, Inc', 'ImageSource Inc.', 'IMAGESOURCE INC', 'ImageSource'], 'CenturyLink': ['CenturyLink', 'Centurylink', 'CENTURYLINK'], 'Shi International Corp': ['Shi International Corp', 'SHI International Corp', 'SHI INTERNATIONAL CORP.', 'SHI International Corp.', 'Shi International Corporation', 'SHI INTERNATIONAL CORP'], 'CodeSmart Inc': ['Codesmart Inc', 'Codesmart INC', 'CodeSmart Inc', 'CodeSmart', 'Codesmart', 'CodeSmart, Inc.', 'CodeSmart, Inc', 'Codesmart, INC.', 'Codesmart, Inc.', 'CODESMART INC'], 'Ricoh USA Inc': ['Ricoh Usa Inc', 'Ricoh USA', 'Ricoh USA, Inc.', 'RICOH USA INC', 'Ricoh USA Inc', 'RICOH USA', 'RICOH']...
```

- Node 3 `subquestion`
  - copy: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2019? Use semantic alias resolution for obvious same-contractor name variants before counting.`
  - tasks_mini: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2019?`

- Node 3 `answer`
  - copy: `["Sharp Electronics Corporation", "DOC Correctional Industries", "A-1 Performance Inc", "WSP USA Inc.", "Shi International Corp", "Parametrix, Inc.", "Imagesource Inc", "Northwest Envirometrics Inc", "Regence Blueshield", "CodeSmart Inc", "Capital Business Machines Inc", "Phoenix Protective Corp.", "DES", "Jacobs Engineering Group, Inc.", "HDR Engineering, ...`
  - tasks_mini: `["Sharp Electronics Corporation", "DOC Correctional Industries", "WSP USA Inc.", "A-1 Performance Inc", "Parametrix, Inc.", "Imagesource Inc", "Northwest Envirometrics Inc", "Regence Blueshield", "Shi International Corp", "Capital Business Machines Inc", "DES", "Phoenix Protective Corp.", "Jacobs Engineering Group, Inc.", "Client Network Services Llc", "HDR...`

- Node 3 `fact`

```diff
@@ -6,15 +6,6 @@
-ALIASES = {'WSP USA Inc.': ['WSP USA, Inc.', 'WSP USA Inc.'], 'HDR Engineering, Inc.': ['HDR Engineering, Inc.', 'HDR Engineering', 'HDR ENGINEERING INC', 'Hdr Engineering Inc', 'HDR, INC'], 'Jacobs Engineering Group, Inc.': ['Jacobs Engineering Group, Inc.', 'Jacobs Engineering Group Inc', 'Jacobs Engineering Group'], 'A-1 Performance Inc': ['A-1 Performance Inc', 'A-1 Performance INC', 'A-1 Performance', 'A-1 Performance Inc.', 'A-1 Performance, Inc.', 'A-1 PERFORMANCE'], 'Imagesource Inc': ['Imagesource Inc', 'ImageSource, Inc.', 'ImageSource, Inc', 'ImageSource Inc.', 'IMAGESOURCE INC', 'ImageSource'], 'CenturyLink': ['CenturyLink', 'Centurylink', 'CENTURYLINK'], 'Shi International Corp': ['Shi International Corp', 'SHI International Corp', 'SHI INTERNATIONAL CORP.', 'SHI International Corp.', 'Shi International Corporation', 'SHI INTERNATIONAL CORP'], 'CodeSmart Inc': ['Codesmart Inc', 'Codesmart INC', 'CodeSmart Inc', 'CodeSmart', 'Codesmart', 'CodeSmart, Inc.', 'CodeSmart, Inc', 'Codesmart, INC.', 'Codesmart, Inc.', 'CODESMART INC'], 'Ricoh USA Inc': ['Ricoh Usa Inc', 'Ricoh USA', 'Ricoh USA, Inc.', 'RICOH USA INC', 'Ricoh USA Inc', 'RICOH USA', 'RICOH']...
```

- Node 4 `subquestion`
  - copy: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2020? Use semantic alias resolution for obvious same-contractor name variants before counting.`
  - tasks_mini: `Which contractors ranked in the top 20 by contract count in Washington State agency contracts in fiscal year 2020?`

- Node 4 `answer`
  - copy: `["JP Morgan Chase Bank NA", "Washington State University", "Washington State Department of Transportation", "WSP USA Inc.", "University of Washington", "Washington State Department of Social and Health Services", "Shi International Corp", "HDR Engineering, Inc.", "Parametrix, Inc.", "HNTB Corporation", "King County", "Regence Blueshield", "Jacobs Engineerin...`
  - tasks_mini: `["JP Morgan Chase Bank NA", "WSP USA Inc.", "University of Washington", "WA State DSHS", "HDR Engineering, Inc.", "Parametrix, Inc.", "Washington State University", "Shi International Corp", "Department of Transportation", "HNTB Corporation", "King County", "Regence Blueshield", "South Puget Sound Comm College", "Jacobs Engineering Group, Inc.", "WA State U...`

- Node 4 `fact`

```diff
@@ -6,15 +6,6 @@
-ALIASES = {'WSP USA Inc.': ['WSP USA, Inc.', 'WSP USA Inc.'], 'HDR Engineering, Inc.': ['HDR Engineering, Inc.', 'HDR Engineering', 'HDR ENGINEERING INC', 'Hdr Engineering Inc', 'HDR, INC'], 'Jacobs Engineering Group, Inc.': ['Jacobs Engineering Group, Inc.', 'Jacobs Engineering Group Inc', 'Jacobs Engineering Group'], 'A-1 Performance Inc': ['A-1 Performance Inc', 'A-1 Performance INC', 'A-1 Performance', 'A-1 Performance Inc.', 'A-1 Performance, Inc.', 'A-1 PERFORMANCE'], 'Imagesource Inc': ['Imagesource Inc', 'ImageSource, Inc.', 'ImageSource, Inc', 'ImageSource Inc.', 'IMAGESOURCE INC', 'ImageSource'], 'CenturyLink': ['CenturyLink', 'Centurylink', 'CENTURYLINK'], 'Shi International Corp': ['Shi International Corp', 'SHI International Corp', 'SHI INTERNATIONAL CORP.', 'SHI International Corp.', 'Shi International Corporation', 'SHI INTERNATIONAL CORP'], 'CodeSmart Inc': ['Codesmart Inc', 'Codesmart INC', 'CodeSmart Inc', 'CodeSmart', 'Codesmart', 'CodeSmart, Inc.', 'CodeSmart, Inc', 'Codesmart, INC.', 'Codesmart, Inc.', 'CODESMART INC'], 'Ricoh USA Inc': ['Ricoh Usa Inc', 'Ricoh USA', 'Ricoh USA, Inc.', 'RICOH USA INC', 'Ricoh USA Inc', 'RICOH USA', 'RICOH']...
```

- Node 5 `source`
  - copy: `wikipedia/WSP_USA/content.txt`
  - tasks_mini: `wikipedia/HDR,_Inc./content.txt`

- Node 5 `subquestion`
  - copy: `For WSP USA (from the intersection of nodes 1-4), in what year was it founded?`
  - tasks_mini: `For HDR Engineering (one of the contractors in the intersection of nodes 1-4), where is it based and in what year did the company start?`

- Node 5 `answer`
  - copy: `1885`
  - tasks_mini: `Omaha, Nebraska; 1917`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-WSP USA, formerly Parsons Brinckerhoff, is an American multinational engineering and design firm. Founded in 1885 in New York City by civil engineer William Barclay Parsons, among Parsons Brinckerhoff's earliest projects was the original IRT line of the New York City Subway.
+HDR, Inc. is an American design and engineering company based in Omaha, Nebraska. In 1917, the Henningson Engineering Company started as a civil engineering firm in Omaha, where HDR's headquarters remain.
```

- Node 6 `source`
  - copy: `wikipedia/HDR,_Inc./content.txt`
  - tasks_mini: `wikipedia/Jacobs_Solutions/content.txt`

- Node 6 `subquestion`
  - copy: `For HDR Engineering (from the intersection of nodes 1-4), where is it based and in what year did the company start?`
  - tasks_mini: `For Jacobs Engineering Group (from the intersection of nodes 1-4), in what year was it founded?`

- Node 6 `answer`
  - copy: `Omaha, Nebraska; 1917`
  - tasks_mini: `1947`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-HDR, Inc. is an American design and engineering company based in Omaha, Nebraska. In 1917, the Henningson Engineering Company started as a civil engineering firm in Omaha, where HDR's headquarters remain.
+Jacobs Engineering was founded in 1947, by Joseph J. Jacobs.
```

- Node 7 `source`
  - copy: `wikipedia/Jacobs_Solutions/content.txt`
  - tasks_mini: `wikipedia/HNTB/content.txt`

- Node 7 `subquestion`
  - copy: `For Jacobs Engineering Group (from the intersection of nodes 1-4), in what year was it founded?`
  - tasks_mini: `For HNTB Corporation (from the intersection of nodes 1-4), in what year was it founded?`

- Node 7 `answer`
  - copy: `1947`
  - tasks_mini: `1914`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Jacobs Engineering was founded in 1947, by Joseph J. Jacobs.
+HNTB Corporation is an American architectural and infrastructure design firm. Founded in 1914 in Kansas City, Missouri, HNTB began with the partnership made by Ernest Emmanuel Howard with the firm Waddell & Harrington, founded in 1907.
```

- Node 8 `subquestion`
  - copy: `Among the engineering contractors from <hop 1 answer>, which have zero current NY State construction manager projects?`
  - tasks_mini: `Of the three engineering contractors in the intersection (Jacobs Engineering Group, HNTB Corporation, HDR Engineering), which have zero NY State construction manager projects?`

- Node 8 `answer`
  - copy: `["WSP USA Inc.", "HDR Engineering, Inc."]`
  - tasks_mini: `["HDR Engineering, Inc.", "HNTB Corporation"]`

- Node 8 `fact`

```diff
@@ -6,12 +6,9 @@
-source = 'datagov/active-construction-projects/files/rows.txt'
-bucket = 'lakeqa-yc4103-datalake'
-obj = boto3.client('s3', config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj['Body'].read()), low_memory=False)
-
-counts = {
```

- Node 9 `subquestion`
  - copy: `In the city where <hop 4 answer> is based, which Native American interpreter helped negotiate the 1853-1854 land cession that led to the city's founding?`
  - tasks_mini: `In the city where the company identified by intersecting the founded-after-1914 companies (from nodes 5-7) with the zero-CM-projects companies (from node 8) is based, which Native American interpreter helped negotiate the 1853-1854 land cession that led to the city's founding?`

- Node 10 `subquestion`
  - copy: `In what year was <hop 5 answer> born?`
  - tasks_mini: `In what year was <node_9 answer> born?`

### `k-4-d-4/task_9.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Washington counties had district-level All Grades Low-Income enrollment percentage between 32% and 40% in the 2018-19 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 2 `subquestion`
  - copy: `Which Washington counties had district-level All Grades Low-Income enrollment percentage between 32% and 40% in the 2019-20 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 3 `subquestion`
  - copy: `Which Washington counties had district-level All Grades Low-Income enrollment percentage between 32% and 40% in the 2020-21 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 4 `subquestion`
  - copy: `Which Washington counties had district-level All Grades Low-Income enrollment percentage between 32% and 40% in the 2021-22 school year?`
  - tasks_mini: `Which Washington counties had Low-Income student enrollment percentage between 32-40% in every school year from 2018-19 through 2021-22? (Filter: OrganizationLevel=District; GradeLevel=All Grades; group by County; Low-Income% = Low-Income / All Students * 100; keep 32-40%.)`

- Node 5 `subquestion`
  - copy: `Among <hop 1 answer>, which counties had district-average Math proficiency above 40% in 2021-22?`
  - tasks_mini: `Among {King, Kitsap, San Juan, Whitman} (from hop 1), which counties had district-average Math proficiency above 40% in 2021-22? (Filter: OrganizationLevel=District; StudentGroup=All Students; GradeLevel=All Grades; TestSubject=Math; compute unweighted mean of PercentMetStandard by County; keep >40%.)`

- Node 6 `subquestion`
  - copy: `Does the King County, Washington article state that King County is the most populous county in Washington?`
  - tasks_mini: `Among {King, Kitsap, San Juan, Whitman} (from hop 1), which counties are NOT the most populous in Washington?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The population was 2,269,675 in the 2020 census, making it the most populous county in Washington
+According to the Wikipedia article for King County, Washington, 'The population was 2,269,675 in the 2020 census, making it the most populous county in Washington.'
```

- Node 7 `subquestion`
  - copy: `What 2020 census population does the Kitsap County, Washington article report for Kitsap County?`
  - tasks_mini: `Among {Kitsap, Whitman} (from hop 2), which county had the lower 2020 census population?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-As of the 2020 census, its population was 275,611.
+According to the Wikipedia article for Kitsap County, Washington, 'As of the 2020 census, its population was 275,611.'
```

- Node 8 `subquestion`
  - copy: `What 2020 census population and county seat does the Whitman County, Washington article report for Whitman County?`
  - tasks_mini: `Among {Kitsap, Whitman} (from hop 2), which county had the lower 2020 census population?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-As of the 2020 census, the population was 47,973. The county seat is Colfax, and its largest city is Pullman.
+According to the Wikipedia article for Whitman County, Washington, 'As of the 2020 census, the population was 47,973.' Also, 'The county seat is Colfax.'
```

- Node 9 `subquestion`
  - copy: `What agricultural college does the Colfax article identify, and which town did it say ultimately received the site?`
  - tasks_mini: `What agricultural college did Colfax (from hop 3) compete to host, and which town won the site selection?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-In 1889–90, the town vied with several other finalists to become the site of a new state agricultural college, present-day Washington State University.  The honor ultimately fell to nearby Pullman,
+According to the Wikipedia article for Colfax, Washington, 'In 1889-90, the town vied with several other finalists to become the site of a new state agricultural college, present-day Washington State University. The honor ultimately fell to nearby Pullman.'
```

### `k-4-d-5/task_1.json`
- Impact: major
- Node 1 `answer`
  - copy: `["Jefferson", "St. Lawrence", "Cayuga", "Otsego", "Suffolk", "Tompkins"]`
  - tasks_mini: `["Jefferson County", "St. Lawrence County", "Tompkins County", "Suffolk County", "Otsego County", "Cayuga County"]`

- Node 1 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,7 +7,15 @@
-source = "datagov/campgrounds-by-county-outside-adirondack-catskill-forest-preserve/files/rows.txt"
+source = 'datagov/campgrounds-by-county-outside-adirondack-catskill-forest-preserve/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 2 `subquestion`
  - copy: `For each non-NYC New York county, how many farmers markets are listed in this dataset? Keep the counties with at least 6 markets.`
  - tasks_mini: `Which Non-NYC NY counties have at least 6 farmers markets?`

- Node 2 `answer`
  - copy: `["Monroe", "Erie", "Nassau", "Westchester", "Niagara", "Sullivan", "Chautauqua", "Onondaga", "Orange", "Rensselaer"]`
  - tasks_mini: `["Monroe County", "Erie County", "Nassau County", "Westchester County", "Sullivan County", "Niagara County", "Chautauqua County", "Orange County", "Onondaga County", "Suffolk County", "Saratoga County", "Rensselaer County", "Albany County", "Steuben County", "Ulster County", "Cattaraugus County", "Washington County", "Oneida County", "Madison County", "Fran...`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,16 +7,18 @@
-source = "datagov/farmers-markets-in-new-york-state/files/rows.txt"
+source = 'datagov/farmers-markets-in-new-york-state/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 3 `subquestion`
  - copy: `For each non-NYC New York county, how many counties have at least 40 endangered species?`
  - tasks_mini: `Which Non-NYC NY counties have at least 40 endangered species per the NY Natural Heritage Program? (Filter: NY Listing Status == 'Endangered'; exclude NYC counties; count by County; keep >= 40.)`

- Node 3 `answer`
  - copy: `["Suffolk", "Nassau", "Monroe", "Westchester", "Erie", "Essex", "Onondaga", "Ulster", "Orange", "Oneida"]`
  - tasks_mini: `["Suffolk County", "Nassau County", "Westchester County", "Monroe County", "Erie County", "Essex County", "Onondaga County", "Ulster County", "Orange County", "Oneida County", "St. Lawrence County", "Dutchess County", "Tompkins County", "Cattaraugus County", "Albany County", "Jefferson County", "Washington County", "Rockland County", "Chautauqua County", "G...`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,19 +7,22 @@
-source = "datagov/biodiversity-by-county-distribution-of-animals-plants-and-natural-communities/files/rows.txt"
+source = 'datagov/biodiversity-by-county-distribution-of-animals-plants-and-natural-communities/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 4 `subquestion`
  - copy: `For each non-NYC New York county, what is the total 2019 state park attendance across all facilities in this dataset? Keep the counties whose totals are between 800,000 and 2,000,000 inclusive.`
  - tasks_mini: `Which Non-NYC NY counties had total state park attendance between 800,000 and 2,000,000 in 2019? (Filter: Year == 2019; sum Attendance by County; exclude NYC counties; keep totals between 800,000 and 2,000,000.)`

- Node 4 `answer`
  - copy: `["Tompkins", "Cattaraugus", "Rockland", "Erie", "Schuyler", "Jefferson", "Livingston/Wyoming"]`
  - tasks_mini: `["Tompkins County", "Cattaraugus County", "Rockland County", "Erie County", "Schuyler County", "Jefferson County", "Livingston/Wyoming County"]`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,21 +7,20 @@
-source = "datagov/state-park-annual-attendance-figures-by-facility-beginning-2003/files/rows.txt"
+source = 'datagov/state-park-annual-attendance-figures-by-facility-beginning-2003/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 5 `subquestion`
  - copy: `For each non-NYC New York county, what is the total amount of lottery-funded education aid amount in 2019-2020? Keep the counties whose totals are between $10,000,000 and $35,000,000 inclusive.`
  - tasks_mini: `Which Non-NYC NY counties received between $10 million and $35 million in lottery aid to education in fiscal year 2019-2020?`

- Node 5 `answer`
  - copy: `["Chautauqua", "Rensselaer", "Jefferson", "Ulster", "Saint Lawrence", "Steuben", "Wayne", "Cattaraugus", "Ontario", "Chemung"]`
  - tasks_mini: `["Chautauqua County", "Rensselaer County", "Jefferson County", "Ulster County", "Saint Lawrence County", "Steuben County", "Wayne County", "Cattaraugus County", "Ontario County", "Chemung County", "Clinton County", "Herkimer County", "Madison County", "Cayuga County", "Chenango County", "Washington County", "Montgomery County", "Genesee County", "Putnam Cou...`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,8 +7,16 @@
-source = "datagov/lottery-aid-to-education-beginning-2002/files/rows.txt"
+source = 'datagov/lottery-aid-to-education-beginning-2002/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 6 `subquestion`
  - copy: `What is the county seat of Jefferson County in <hop 1 answer>?`
  - tasks_mini: `What is the county seat of Jefferson County (from <intersection of nodes 1-5>)?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Its county seat is Watertown.
+Jefferson County's county seat is Watertown.
```

- Node 7 `subquestion`
  - copy: `What is the county seat of Tompkins County in <hop 1 answer>?`
  - tasks_mini: `What is the county seat of Tompkins County (from <intersection of nodes 1-5>)?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The county seat is Ithaca.
+Tompkins County's county seat is Ithaca.
```

- Node 8 `subquestion`
  - copy: `Among <hop 1 answer>, which county had more violent crimes in 2020?`
  - tasks_mini: `Which county had more violent crimes in 2020: Jefferson County (seat: <node_6 answer>) or Tompkins County (seat: <node_7 answer>)?`

- Node 8 `answer`
  - copy: `Jefferson`
  - tasks_mini: `Jefferson County`

- Node 8 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,7 +7,15 @@
-source = "datagov/index-violent-property-and-firearm-rates-by-county-beginning-1990/files/rows.txt"
+source = 'datagov/index-violent-property-and-firearm-rates-by-county-beginning-1990/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 9 `subquestion`
  - copy: `What year was the county seat of <hop 3 answer> incorporated as a city?`
  - tasks_mini: `What year was the Watertown (the county seat of <node_8 answer>) incorporated as a city?`

### `k-4-d-5/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which candidates had total campaign spendings between $103,000 and $251,000 in the 2001 election cycle?`
  - tasks_mini: `Which NYC municipal candidates filed campaign expenditures between $103,000 and $251,000 in the 2001 election cycle? (Filter: sum AMNT by candidate (CANDID, CANDFIRST, CANDLAST); keep totals between $103,000 and $251,000.)`

- Node 1 `answer`
  - copy: `["Salvatore Albanese", "Anthony Andrews, Jr.", "JoAnn Ariola", "Paul Bader", "Maria Baez", "Steven Banks", "Charles Barron", "Michael Benjamin", "James Blake", "Michelle Bouchard"]`
  - tasks_mini: `["Domenic Recchia", "Leroy Comrie", "103 others"]`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,14 +7,25 @@
-source = "datagov/2001-campaign-expenditures/files/rows.txt"
+source = 'datagov/2001-campaign-expenditures/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 2 `subquestion`
  - copy: `Which candidates had total campaign spendings between $103,000 and $251,000 in the 2003 election cycle?`
  - tasks_mini: `Which NYC municipal candidates filed campaign expenditures between $103,000 and $251,000 in the 2003 election cycle? (Filter: sum AMNT by candidate (CANDID, CANDFIRST, CANDLAST); keep totals between $103,000 and $251,000.)`

- Node 2 `answer`
  - copy: `["Joseph Addabbo", "Tony Avella", "Maria Baez", "Ismael Betancourt Jr", "Omar Boucher", "Everly Brown", "Leroy Comrie", "Erik Dilan", "Simcha Felder", "Lewis Fidler"]`
  - tasks_mini: `["Domenic Recchia", "Leroy Comrie", "45 others"]`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,14 +7,25 @@
-source = "datagov/2003-campaign-expenditures/files/rows.txt"
+source = 'datagov/2003-campaign-expenditures/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 3 `subquestion`
  - copy: `Which candidates had total campaign spendings between $103,000 and $251,000 in the 2005 election cycle?`
  - tasks_mini: `Which NYC municipal candidates filed campaign expenditures between $103,000 and $251,000 in the 2005 election cycle? (Filter: sum AMNT by candidate (CANDID, CANDFIRST, CANDLAST); keep totals between $103,000 and $251,000.)`

- Node 3 `answer`
  - copy: `["Tony Avella", "Albert Baldeo", "Charles Barron", "Ismael Betancourt Jr", "Michael Beys", "Darren Bloch", "Peter Boudouvas", "Gale Brewer", "Rodney Carroll", "Yvette Clarke"]`
  - tasks_mini: `["Domenic Recchia", "Leroy Comrie", "67 others"]`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,14 +7,25 @@
-source = "datagov/2005-campaign-expenditures/files/rows.txt"
+source = 'datagov/2005-campaign-expenditures/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 4 `subquestion`
  - copy: `Which candidates had total campaign spendings between $103,000 and $251,000 in the 2009 election cycle?`
  - tasks_mini: `Which NYC municipal candidates filed campaign expenditures between $103,000 and $251,000 in the 2009 election cycle? (Filter: sum AMNT by candidate (CANDID, CANDFIRST, CANDLAST); keep totals between $103,000 and $251,000.)`

- Node 4 `answer`
  - copy: `["Isaac Abraham", "Maria Arroyo", "Maria Baez", "Steven Anthony Behar", "Victor Bernace", "Douglas Biviano", "Tracy Boyland", "James Brennan", "Fernando Cabrera", "Robert Capano"]`
  - tasks_mini: `["Domenic Recchia", "Leroy Comrie", "97 others"]`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,14 +7,25 @@
-source = "datagov/2009-campaign-expenditures/files/rows.txt"
+source = 'datagov/2009-campaign-expenditures/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 5 `subquestion`
  - copy: `Which candidates had total campaign spendings between $103,000 and $251,000 in the 2013 election cycle?`
  - tasks_mini: `Which NYC municipal candidates filed campaign expenditures between $103,000 and $251,000 in the 2013 election cycle? (Filter: sum AMNT by candidate (CANDID, CANDFIRST, CANDLAST); keep totals between $103,000 and $251,000.)`

- Node 5 `answer`
  - copy: `["Olanike Alabi", "Pedro Alvarez", "Maria Arroyo", "Christopher Banks", "Raquel Batista", "Ken Biberaj", "Ricardo Brown", "Ralina Cardona", "Craig Caruana", "Manuel Caughman"]`
  - tasks_mini: `["Domenic Recchia", "Leroy Comrie", "91 others"]`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,14 +7,25 @@
-source = "datagov/2013-campaign-expenditures/files/rows.txt"
+source = 'datagov/2013-campaign-expenditures/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 6 `subquestion`
  - copy: `Which NYC borough did Leroy Comrie represent?`
  - tasks_mini: `Which NYC borough did Leroy Comrie (from <intersection of nodes 1-5>) represent?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-He represents district 14 in the New York State Senate, which comprises St. Albans, Cambria Heights, Jamaica, Hollis, Rosedale, Laurelton, Kew Gardens, Queens Village and other neighborhoods within the borough of Queens.
+Leroy George Comrie Jr. represents district 14 in the New York State Senate, which comprises neighborhoods within the borough of Queens.
```

- Node 7 `subquestion`
  - copy: `Which NYC borough did Domenic Recchia represent?`
  - tasks_mini: `Which NYC borough did Domenic Recchia (from <intersection of nodes 1-5>) represent?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Recchia formerly represented the 47th district of the New York City Council, which included areas of Bensonhurst, Brighton Beach, Coney Island, and Gravesend in south Brooklyn.
+Domenic Michael Recchia Jr. formerly represented the 47th district of the New York City Council, which included areas of Bensonhurst, Brighton Beach, Coney Island, and Gravesend in south Brooklyn.
```

- Node 8 `subquestion`
  - copy: `For the boroughs in <hop 2 answer>, how many residents living in New York City public housing were accepted and enrolled in the city's summer jobs program for young people in 2019?`
  - tasks_mini: `Which borough had more NYCHA residents enrolled in SYEP in 2019: Queens (<node_6 answer>) or Brooklyn (<node_7 answer>)? (Filter: Year == 2019; compare 'Were accepted and enrolled' for Queens vs Brooklyn.)`

- Node 8 `answer`
  - copy: `{"Brooklyn": 3889.0, "Queens": 1019.0}`
  - tasks_mini: `Brooklyn`

- Node 8 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,7 +7,14 @@
-source = "datagov/summer-youth-employment-program-syep-for-nycha-residents-by-borough-local-law-163/files/rows.txt"
+source = 'datagov/summer-youth-employment-program-syep-for-nycha-residents-by-borough-local-law-163/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 9 `subquestion`
  - copy: `In what year was the candidate representing <hop 3 answer> born?`
  - tasks_mini: `In what year was Domenic Recchia (the candidate representing <node_8 answer>) born?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-Domenic Michael Recchia Jr. (born July 25, 1959) is an American attorney and politician from New York City.
+Domenic Michael Recchia Jr. was born on July 25, 1959.
```

### `k-4-d-5/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which drugs had between 5,000,000 and 10,000,000 total Medicaid prescriptions across U.S. states in 2018, and what were those totals?`
  - tasks_mini: `What were the total prescriptions for drugs with between 5 and 10 million prescriptions across all US states in 2018? (Filter: sum Number of Prescriptions by Product Name; keep totals between 5,000,000 and 10,000,000.)`

- Node 1 `answer`
  - copy: `{"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 5842176, "BUPRENORPH": 5008835, "BUSPIRONE": 6570260, "CARVEDILOL": 5476593, "CEPHALEXIN": 8302749, "CITALOPRAM": 8017063, "CLINDAMYCI": 6613061}`
  - tasks_mini: `{"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 5842176, "BUPRENORPH": 5008835, "BUSPIRONE ": 6570260, "CARVEDILOL": 5476593, "CEPHALEXIN": 8302749, "CITALOPRAM": 8017063, "CLINDAMYCI": 6613061, "CLONAZEPAM": 8894975, "DEXTROAMPH": 6588490, "DIVALPROEX": 6058018, "DULOXETINE": 7846188, "ERGOCALCIF": 9185356, "ESCITALOPR":...`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,8 +7,17 @@
-source = "datagov/state-drug-utilization-data-2018-b2fe5/files/StateDrugUtilizationData2018.txt"
+source = 'datagov/state-drug-utilization-data-2018-b2fe5/files/StateDrugUtilizationData2018.txt'
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"]
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 2 `subquestion`
  - copy: `Which drugs had between 5,000,000 and 10,000,000 total Medicaid prescriptions across U.S. states in 2019, and what were those totals?`
  - tasks_mini: `What were the total prescriptions for drugs with between 5 and 10 million prescriptions across all US states in 2019? (Filter: sum Number of Prescriptions by Product Name; keep totals between 5,000,000 and 10,000,000.)`

- Node 2 `answer`
  - copy: `{"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 6927103, "BUSPIRONE": 6963013, "CARVEDILOL": 5399167, "CEPHALEXIN": 8180606, "CITALOPRAM": 6970176, "CLINDAMYCI": 6503376, "CLONAZEPAM": 8120719}`
  - tasks_mini: `{"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 6927103, "BUSPIRONE ": 6963013, "CARVEDILOL": 5399167, "CEPHALEXIN": 8180606, "CITALOPRAM": 6970176, "CLINDAMYCI": 6503376, "CLONAZEPAM": 8120719, "CYCLOBENZA": 9623284, "DEXTROAMPH": 6699361, "DICLOFENAC": 5245404, "DIVALPROEX": 5990171, "DULOXETINE": 8307336, "ERGOCALCIF":...`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,8 +7,17 @@
-source = "datagov/state-drug-utilization-data-2019/files/StateDrugUtilizationData2019.txt"
+source = 'datagov/state-drug-utilization-data-2019/files/StateDrugUtilizationData2019.txt'
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"]
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 3 `subquestion`
  - copy: `Which drugs had between 5,000,000 and 10,000,000 total Medicaid prescriptions across U.S. states in 2020, and what were those totals?`
  - tasks_mini: `What were the total prescriptions for drugs with between 5 and 10 million prescriptions across all US states in 2020? (Filter: sum Number of Prescriptions by Product Name; keep totals between 5,000,000 and 10,000,000.)`

- Node 3 `answer`
  - copy: `{"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 9187146, "BUSPIRONE": 8211972, "CARVEDILOL": 5278160, "CEPHALEXIN": 7183268, "CITALOPRAM": 6534226, "CLINDAMYCI": 6289786, "CLONAZEPAM": 8184145}`
  - tasks_mini: `{"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 9187146, "BUSPIRONE ": 8211972, "CARVEDILOL": 5278160, "CEPHALEXIN": 7183268, "CITALOPRAM": 6534226, "CLINDAMYCI": 6289786, "CLONAZEPAM": 8184145, "CYCLOBENZA": 9491303, "DEXTROAMPH": 6973855, "DICLOFENAC": 6577126, "DIVALPROEX": 5990934, "DULOXETINE": 8714249, "FAMOTIDINE":...`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,8 +7,17 @@
-source = "datagov/state-drug-utilization-data-2020-3e746/files/StateDrugUtilizationData2020.txt"
+source = 'datagov/state-drug-utilization-data-2020-3e746/files/StateDrugUtilizationData2020.txt'
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"]
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 4 `subquestion`
  - copy: `Which drugs had between 5,000,000 and 10,000,000 total Medicaid prescriptions across U.S. states in 2021, and what were those totals?`
  - tasks_mini: `What were the total prescriptions for drugs with between 5 and 10 million prescriptions across all US states in 2021? (Filter: sum Number of Prescriptions by Product Name; keep totals between 5,000,000 and 10,000,000.)`

- Node 4 `answer`
  - copy: `{"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE": 9341966, "CARVEDILOL": 5184118, "CEPHALEXIN": 7847935, "CITALOPRAM": 6229548, "CLINDAMYCI": 7126931, "CLONAZEPAM": 8270464, "DEXTROAMPH": 7237437}`
  - tasks_mini: `{"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE ": 9341966, "CARVEDILOL": 5184118, "CEPHALEXIN": 7847935, "CITALOPRAM": 6229548, "CLINDAMYCI": 7126931, "CLONAZEPAM": 8270464, "DEXTROAMPH": 7237437, "DICLOFENAC": 7525666, "DIVALPROEX": 5887199, "DOCUSATE S": 5037805, "DOXYCYCLIN": 5993452, "DULOXETINE": 9181333, "FLOVENT HF":...`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,8 +7,17 @@
-source = "datagov/state-drug-utilization-data-2021-f9419/files/StateDrugUtilizationData2021.txt"
+source = 'datagov/state-drug-utilization-data-2021-f9419/files/StateDrugUtilizationData2021.txt'
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"]
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 5 `subquestion`
  - copy: `Which drugs had between 5,000,000 and 10,000,000 total Medicaid prescriptions across U.S. states in 2022, and what were those totals?`
  - tasks_mini: `What were the total prescriptions for drugs with between 5 and 10 million prescriptions across all US states in 2022? (Filter: sum Number of Prescriptions by Product Name; keep totals between 5,000,000 and 10,000,000.)`

- Node 5 `answer`
  - copy: `{"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 8353098, "CITALOPRAM": 5685980, "CLINDAMYCI": 7097389, "CLONAZEPAM": 8066255, "DEXTROAMPH": 6711926, "DICLOFENAC": 7920135, "DIVALPROEX": 5732831}`
  - tasks_mini: `{"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 8353098, "CITALOPRAM": 5685980, "CLINDAMYCI": 7097389, "CLONAZEPAM": 8066255, "DEXTROAMPH": 6711926, "DICLOFENAC": 7920135, "DIVALPROEX": 5732831, "DOCUSATE S": 5313785, "DOXYCYCLIN": 6770856, "DULOXETINE": 9371705, "FLUCONAZOL": 7645713, "FOLIC ACID": 6862851, "FUROSEMIDE":...`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,8 +7,17 @@
-source = "datagov/state-drug-utilization-data-2022/files/StateDrugUtilizationData2022.txt"
+source = 'datagov/state-drug-utilization-data-2022/files/StateDrugUtilizationData2022.txt'
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"]
+local_path = source if os.path.exists(source) else "/tmp/k123_data_cache/" + source
```

- Node 6 `subquestion`
  - copy: `In what year did <hop 1 answer> first come into medical use?`
  - tasks_mini: `In what year did <superlative of nodes 1-5: TRIAMCINOLONE, the drug with highest average prescriptions in 5-10M range> come into medical use?`

- Node 7 `subquestion`
  - copy: `What were the top 3 leading causes of death in <hop 2 answer>?`
  - tasks_mini: `According to NCHS Age-Adjusted Death Rates data, what were the top 3 leading causes of death in <node 6: 1958>? (Filter: Year == 1958; sort by Age Adjusted Death Rate; take top 3.)`

- Node 7 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,9 +6,18 @@
-source = "datagov/nchs-age-adjusted-death-rates-for-selected-major-causes-of-death/files/rows.txt"
+
+source = 'datagov/nchs-age-adjusted-death-rates-for-selected-major-causes-of-death/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 8 `subquestion`
  - copy: `What was the most significant risk factor for Heart Disease?`
  - tasks_mini: `What is the most significant risk factor for <node 7: Heart Disease> according to Wikipedia?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Age is the most important risk factor in developing cardiovascular or heart diseases, with approximately a tripling of risk with each decade of life.
+According to Wikipedia, 'Age is the most important risk factor in developing cardiovascular or heart diseases, with approximately a tripling of risk with each decade of life.'
```

- Node 9 `subquestion`
  - copy: `What was the most significant risk factor for Cancer?`
  - tasks_mini: `What is the most significant risk factor for <node 7: Cancer> according to Wikipedia?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The most significant risk factor for developing cancer is age. Although it is possible for cancer to strike at any age, most patients with invasive cancer are over 65.
+According to Wikipedia, 'The most significant risk factor for developing cancer is age. Although it is possible for cancer to strike at any age, most patients with invasive cancer are over 65.'
```

- Node 10 `subquestion`
  - copy: `What was the most significant risk factor for Stroke, and who first described this condition?`
  - tasks_mini: `What is the most significant risk factor for <node 7: Stroke> according to Wikipedia, and who first described this condition?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-The most significant risk factor for stroke is high blood pressure. Hippocrates (460 to 370 BC) was first to describe the phenomenon of sudden paralysis associated with stroke.
+According to Wikipedia, 'The most significant risk factor for stroke is high blood pressure.' Hippocrates (460 to 370 BC) was first to describe the phenomenon of sudden paralysis associated with stroke.
```

### `k-4-d-5/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What is the number of child care center sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2018-2019?`
  - tasks_mini: `How many CACFP childcare center sites did each Texas county have in 2018-2019? (Filter: ProgramYear == '2018-2019'; count sites by SiteCounty.)`

- Node 1 `answer`
  - copy: `{"BEXAR": 622, "CAMERON": 455, "DALLAS": 1207, "EL PASO": 459, "FORT BEND": 150, "HARRIS": 1781, "HIDALGO": 878, "KAUFMAN": 232, "TARRANT": 562, "TRAVIS": 306}`
  - tasks_mini: `{"BEXAR": 622, "DALLAS": 1207, "HARRIS": 1781, "HIDALGO": 878, "OTHER_COUNTIES": 190, "TARRANT": 562}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,13 +7,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2018/files/rows.txt"
+source = 'datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2018/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
```

- Node 2 `subquestion`
  - copy: `What is the number of child care center sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2019-2020?`
  - tasks_mini: `How many CACFP childcare center sites did each Texas county have in 2019-2020? (Filter: ProgramYear == '2019-2020'; count sites by SiteCounty.)`

- Node 2 `answer`
  - copy: `{"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "EL PASO": 524, "HARRIS": 2179, "HIDALGO": 1203, "KAUFMAN": 204, "TARRANT": 588, "TRAVIS": 343, "WEBB": 200}`
  - tasks_mini: `{"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "HARRIS": 2179, "HIDALGO": 1203, "OTHER_COUNTIES": 194}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,13 +7,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2019/files/rows.txt"
+source = 'datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2019/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
```

- Node 3 `subquestion`
  - copy: `What is the number of child care center sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2020-2021?`
  - tasks_mini: `How many CACFP childcare center sites did each Texas county have in 2020-2021? (Filter: ProgramYear == '2020-2021'; count sites by SiteCounty.)`

- Node 3 `answer`
  - copy: `{"BELL": 188, "BEXAR": 756, "CAMERON": 418, "DALLAS": 1120, "EL PASO": 456, "FORT BEND": 202, "HARRIS": 1709, "HIDALGO": 918, "TARRANT": 592, "TRAVIS": 267}`
  - tasks_mini: `{"BEXAR": 756, "DALLAS": 1120, "HARRIS": 1709, "HIDALGO": 918, "OTHER_COUNTIES": 189, "TARRANT": 592}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,13 +7,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2020/files/rows.txt"
+source = 'datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2020/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
```

- Node 4 `subquestion`
  - copy: `What is the number of child care center sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2021-2022?`
  - tasks_mini: `How many CACFP childcare center sites did each Texas county have in 2021-2022? (Filter: ProgramYear == '2021-2022'; count sites by SiteCounty.)`

- Node 4 `answer`
  - copy: `{"BEXAR": 772, "CAMERON": 417, "DALLAS": 1269, "EL PASO": 443, "FORT BEND": 212, "HARRIS": 1871, "HIDALGO": 924, "KAUFMAN": 172, "TARRANT": 687, "TRAVIS": 301}`
  - tasks_mini: `{"BEXAR": 772, "DALLAS": 1269, "HARRIS": 1871, "HIDALGO": 924, "OTHER_COUNTIES": 188, "TARRANT": 687}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,13 +7,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2021/files/rows.txt"
+source = 'datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2021/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
```

- Node 5 `subquestion`
  - copy: `What is the number of child care center sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2022-2023?`
  - tasks_mini: `How many CACFP childcare center sites did each Texas county have in 2022-2023? (Filter: ProgramYear == '2022-2023'; count sites by SiteCounty.)`

- Node 5 `answer`
  - copy: `{"BEXAR": 743, "CAMERON": 424, "DALLAS": 1352, "EL PASO": 452, "FORT BEND": 177, "HARRIS": 2183, "HIDALGO": 947, "TARRANT": 715, "TRAVIS": 328, "WEBB": 225}`
  - tasks_mini: `{"BEXAR": 743, "DALLAS": 1352, "HARRIS": 2183, "HIDALGO": 947, "OTHER_COUNTIES": 189, "TARRANT": 715}`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,13 +7,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2022/files/rows.txt"
+source = 'datagov/child-and-adult-care-food-programs-cacfp-centers-site-level-contact-and-program-parti-2022/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
```

- Node 6 `subquestion`
  - copy: `What is the 2022 total number of completed investigations into possible child abuse or neglect for each county?`
  - tasks_mini: `Which counties from <nodes 1-5 top 5 by average: Harris, Dallas, Hidalgo, Bexar, Tarrant> had less than 14,000 completed child abuse/neglect investigations in FY2022? (Filter: Fiscal Year == 2022; sum Completed Investigations by County; keep < 14,000.)`

- Node 6 `answer`
  - copy: `{"BEXAR": 13020, "COLLIN": 3526, "DALLAS": 14192, "DENTON": 3761, "EL PASO": 4709, "HARRIS": 23468, "HIDALGO": 4984, "MONTGOMERY": 3484, "TARRANT": 13286, "TRAVIS": 5315}`
  - tasks_mini: `["Tarrant", "Bexar", "Hidalgo"]`

- Node 6 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 6 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,15 +7,22 @@
-source = "datagov/cpi-3-1-completed-abuse-neglect-investigations-by-county-fy2013-fy2022/files/rows.txt"
+source = 'datagov/cpi-3-1-completed-abuse-neglect-investigations-by-county-fy2013-fy2022/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-df["County_norm"] = df["County"].astype(str).str.strip().str.upper()
```

- Node 7 `subquestion`
  - copy: `What is the 2022 total number of children removed from their homes by child protective services for each county?`
  - tasks_mini: `Which counties from <nodes 1-5 top 5 by average: Harris, Dallas, Hidalgo, Bexar, Tarrant> had more than 600 CPS removals in FY2022? (Filter: Fiscal Year == 2022; sum Removals by County; keep > 600.)`

- Node 7 `answer`
  - copy: `{"BELL": 470, "BEXAR": 1074, "DALLAS": 738, "HARRIS": 566, "LUBBOCK": 194, "MCLENNAN": 171, "NUECES": 258, "TARRANT": 555, "TAYLOR": 205, "TRAVIS": 273}`
  - tasks_mini: `["Bexar", "Dallas"]`

- Node 7 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 7 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,15 +7,21 @@
-source = "datagov/cps-2-1-removals-by-county-fy2013-2022/files/rows.txt"
+source = 'datagov/cps-2-1-removals-by-county-fy2013-2022/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-df["County_norm"] = df["County"].astype(str).str.strip().str.upper()
```

- Node 8 `subquestion`
  - copy: `When was <hop 2 answer> created?`
  - tasks_mini: `When was <intersection of nodes 6-7: Bexar County> created?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Bexar County was created on December 20, 1836, as one of the original counties of the Republic of Texas.
+According to Wikipedia, Bexar County 'was created on December 20, 1836' as one of the original counties of the Republic of Texas.
```

- Node 9 `fact`

```diff
@@ -1 +1 @@
-Tarrant County was established in 1849.
+According to Wikipedia, Tarrant County was established in 1849.
```

- Node 10 `subquestion`
  - copy: `What admission order number did the U.S. state admitted in <hop 3 answer> have?`
  - tasks_mini: `When was the 25th US state admitted to the Union?`

- Node 10 `answer`
  - copy: `25`
  - tasks_mini: `1836`

### `k-4-d-5/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What is the number of home-based day care sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2018-2019?`
  - tasks_mini: `How many CACFP day care homes were in each Texas county in 2018-2019? (Filter: ProgramYear == '2018-2019'; count sites by CECounty.)`

- Node 1 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,11 +6,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2018/files/rows.txt"
+
+source = 'datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2018/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 2 `subquestion`
  - copy: `What is the number of home-based day care sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2019-2020?`
  - tasks_mini: `How many CACFP day care homes were in each Texas county in 2019-2020? (Filter: ProgramYear == '2019-2020'; count sites by CECounty.)`

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,11 +6,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2019/files/rows.txt"
+
+source = 'datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2019/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 3 `subquestion`
  - copy: `What is the number of home-based day care sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2020-2021?`
  - tasks_mini: `How many CACFP day care homes were in each Texas county in 2020-2021? (Filter: ProgramYear == '2020-2021'; count sites by CECounty.)`

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,11 +6,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2020/files/rows.txt"
+
+source = 'datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2020/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 4 `subquestion`
  - copy: `What is the number of home-based day care sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2021-2022?`
  - tasks_mini: `How many CACFP day care homes were in each Texas county in 2021-2022? (Filter: ProgramYear == '2021-2022'; count sites by CECounty.)`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,11 +6,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2021/files/rows.txt"
+
+source = 'datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2021/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 5 `subquestion`
  - copy: `What is the number of home-based day care sites in each Texas county participating in the federal meal-reimbursement program for children and adults for 2022-2023?`
  - tasks_mini: `How many CACFP day care homes were in each Texas county in 2022-2023? (Filter: ProgramYear == '2022-2023'; count sites by CECounty.)`

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,11 +6,18 @@
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2022/files/rows.txt"
+
+source = 'datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-site-level-contact-and-progra-2022/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 6 `subquestion`
  - copy: `Among <hop 1 answer>, which counties had less than 14.5% of reported adult-protection victims involved in repeat investigations in 2022?`
  - tasks_mini: `Which counties from <nodes 1-5 top 5 by average: Travis, Harris, Taylor, Tarrant, Hidalgo> had an APS recidivism rate below 14.5% in FY2022? (Filter: Fiscal Year == 2022; use Recidivism < 0.145.)`

- Node 6 `answer`
  - copy: `["Tarrant", "Travis"]`
  - tasks_mini: `["TRAVIS", "TARRANT"]`

- Node 6 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -5,15 +6,23 @@
-source = "datagov/aps-5-2-outcomes-recidivism-by-county-fy2013-2022/files/rows.txt"
+
+source = 'datagov/aps-5-2-outcomes-recidivism-by-county-fy2013-2022/files/rows.txt'
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 7 `subquestion`
  - copy: `Who is Travis County from <node 6 answer> named after?`
  - tasks_mini: `Who is <node 6 result: Travis County> named after?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The county was established in 1840 and is named in honor of William Barret Travis, the commander of the Republic of Texas forces at the Battle of the Alamo.
+According to Wikipedia, Travis County 'was established in 1840 and is named in honor of William Barret Travis, the commander of the Republic of Texas forces at the Battle of the Alamo.'
```

- Node 8 `subquestion`
  - copy: `Who is Tarrant County from <node 6 answer> named after?`
  - tasks_mini: `Who is <node 6 result: Tarrant County> named after?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-It is named after Edward H. Tarrant, a lawyer, politician, and militia leader.
+According to Wikipedia, Tarrant County 'was established in 1849' and 'is named after Edward H. Tarrant, a lawyer, politician, and militia leader.'
```

- Node 9 `subquestion`
  - copy: `In what year was <node 7 answer> born?`
  - tasks_mini: `In what year was <node 7: William Barret Travis> born?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-William Barret "Buck" Travis (August 1, 1809 – March 6, 1836)
+According to Wikipedia, 'William Barret "Buck" Travis (August 1, 1809 – March 6, 1836) was a Texian Army officer and lawyer.'
```

- Node 10 `subquestion`
  - copy: `In what year was <node 8 answer> born?`
  - tasks_mini: `In what year was <node 8: Edward H. Tarrant> born?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-Edward H. Tarrant (1796 – August 2, 1858)
+According to Wikipedia, 'Edward H. Tarrant (1796 – August 2, 1858) was an American politician and general.'
```

### `k-5-d-1/task_1.json`
- Impact: major
- Node 1 `source`
  - copy: `wikipedia/LAPD_Rampart_Division/content.txt`
  - tasks_mini: `wikipedia/Rampart_Division/content.txt`

- Node 1 `subquestion`
  - copy: `Which LAPD area name serves neighborhoods including Echo Park and Silver Lake?`
  - tasks_mini: `What LAPD area name corresponds to the Rampart Division?`

- Node 1 `fact`

```diff
@@ -1 +1 @@
-The LAPD Rampart area/division serves neighborhoods including Echo Park and Silver Lake.
+The LAPD Rampart Division corresponds to the LAPD area name Rampart.
```

- Node 2 `subquestion`
  - copy: `In LAPD stop-incident records, what police area number corresponds to <hop 1 answer>?`
  - tasks_mini: `In LAPD stop-incident entries, what Area ID corresponds to area name <node_1 answer> (answer as an integer)?`

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,8 +7,17 @@
-source = "datagov/lapd-ripa-ab-953-stop-incident-details-from-7-1-2018-to-present/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/lapd-ripa-ab-953-stop-incident-details-from-7-1-2018-to-present/files/rows.txt'
```

- Node 3 `subquestion`
  - copy: `In 2020 crime records for police area <hop 2 answer>, which crime code was most common?`
  - tasks_mini: `In 2020 crime entries for Area ID <node_2 answer>, which crime code is most common?`

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,10 +7,24 @@
-source = "datagov/crime-data-from-2020-to-present/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/crime-data-from-2020-to-present/files/rows.txt'
```

- Node 4 `subquestion`
  - copy: `In the 2010-2019 crime records, what crime description corresponds to code <hop 3 answer>?`
  - tasks_mini: `In 2010 to 2019 crime entries, what crime description corresponds to crime code <node_3 answer>?`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,9 +7,23 @@
-source = "datagov/crime-data-from-2010-to-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/crime-data-from-2010-to-2019/files/rows.txt'
```

- Node 5 `subquestion`
  - copy: `In 2020 crime records, how many incidents were recorded with crime description <hop 4 answer>?`
  - tasks_mini: `In 2020 crime entries, how many incidents had crime description <node_4 answer>?`

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,9 +7,20 @@
-source = "datagov/crime-data-from-2020-to-present/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/crime-data-from-2020-to-present/files/rows.txt'
```

### `k-5-d-1/task_2.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1 +1 @@
-Austin is the capital city of the U.S. state of Texas.
+Austin is the capital of Texas.
```

- Node 2 `subquestion`
  - copy: `For 2023 <hop 1 answer> police dispatch incidents, which sector has the most incidents?`
  - tasks_mini: `In 2023 CAD incidents in <node_1 answer>, which sector has the most incidents?`

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,16 +7,20 @@
-source = "datagov/apd-computer-aided-dispatch-incidents/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/apd-computer-aided-dispatch-incidents/files/rows.txt'
```

- Node 3 `subquestion`
  - copy: `In 2023 APD use-of-force entries within sector <hop 2 answer>, which council district has the most incidents?`
  - tasks_mini: `In 2023 use-of-force entries within sector <node_2 answer>, which council district has the most incidents?`

- Node 3 `answer`
  - copy: `4`
  - tasks_mini: `4`

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,18 +7,24 @@
-source = "datagov/apd-use-of-force/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/apd-use-of-force/files/rows.txt'
```

- Node 4 `subquestion`
  - copy: `In 2023 APD search entries within council district <hop 3 answer>, which sector has the most searches?`
  - tasks_mini: `In 2023 search entries within council district <node_3 answer>, which sector has the most searches?`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,16 +7,24 @@
-source = "datagov/apd-searches-by-type/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/apd-searches-by-type/files/rows.txt'
```

- Node 5 `subquestion`
  - copy: `In 2024 complaints-by-sector data, what is the total number of complaints for sector <hop 4 answer>?`
  - tasks_mini: `In 2024 complaints-by-sector data, what is the total number of complaints for sector <node_4 answer>?`

- Node 5 `answer`
  - copy: `52`
  - tasks_mini: `52`

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,7 +7,19 @@
-source = "datagov/apd-complaints-by-sector/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/apd-complaints-by-sector/files/rows.txt'
```

### `k-5-d-1/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Washington, D.C. ward contains Adams Morgan?`
  - tasks_mini: `Adams Morgan is part of which ward of Washington, D.C.?`

- Node 2 `subquestion`
  - copy: `In 2017, within Ward <hop 1 answer>, which offense was most common?`
  - tasks_mini: `In 2017, within Ward <node_1 answer>, which offense is most common?`

- Node 2 `fact`

```diff
@@ -1,2 +1,5 @@
+import os
+import io
+from collections import Counter
@@ -4,15 +7,22 @@
-from collections import Counter
-source = "datagov/crime-incidents-in-2017/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 3 `subquestion`
  - copy: `In 2018, which ward had the most <hop 2 answer> incidents?`
  - tasks_mini: `In 2018, which ward has the most <node_2 answer> incidents?`

- Node 3 `fact`

```diff
@@ -1,2 +1,5 @@
+import os
+import io
+from collections import Counter
@@ -4,15 +7,22 @@
-from collections import Counter
-source = "datagov/crime-incidents-in-2018/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 4 `subquestion`
  - copy: `In 2019, within Ward <hop 3 answer>, which offense was most common?`
  - tasks_mini: `In 2019, within Ward <node_3 answer>, which offense is most common?`

- Node 4 `fact`

```diff
@@ -1,2 +1,5 @@
+import os
+import io
+from collections import Counter
@@ -4,15 +7,22 @@
-from collections import Counter
-source = "datagov/crime-incidents-in-2019/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
```

- Node 5 `subquestion`
  - copy: `In 2020, how many incidents were recorded with offense <hop 4 answer>?`
  - tasks_mini: `In 2020, how many incidents had OFFENSE = <node_4 answer>?`

- Node 5 `fact`

```diff
@@ -1 +1,3 @@
+import os
+import io
@@ -5,9 +7,22 @@
-source = "datagov/crime-incidents-in-2020/files/data.txt"
-bucket = "lakeqa-yc4103-datalake"
-body = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)["Body"].read()
-payload = json.loads(body)
```

### `k-5-d-1/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which borough of New York City is the largest by area?`
  - tasks_mini: `Which borough of New York City is Queens?`

- Node 1 `fact`

```diff
@@ -1 +1 @@
-Queens is the largest by area of the five boroughs of New York City, coextensive with Queens County, in the U.S. state of New York.
+Queens is a borough of New York City.
```

- Node 2 `subquestion`
  - copy: `In 2022 complaint records for <hop 1 answer>, which precinct received the most complaints?`
  - tasks_mini: `In 2022 complaint entries for <node_1 answer>, which precinct has the most complaints?`

- Node 2 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,18 +7,24 @@
-source = "datagov/nypd-complaint-data-historic/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/nypd-complaint-data-historic/files/rows.txt'
```

- Node 3 `subquestion`
  - copy: `In 2022 shooting incidents within precinct <hop 2 answer>, was it more common for the shooting to happen inside or outside?`
  - tasks_mini: `In 2022 shooting incident entries within precinct <node_2 answer>, which location descriptor is most common?`

- Node 3 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,18 +7,24 @@
-source = "datagov/nypd-shooting-incident-data-historic/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/nypd-shooting-incident-data-historic/files/rows.txt'
```

- Node 4 `subquestion`
  - copy: `In 2022 complaint records in <hop 1 answer> where the incident happened <hop 3 answer>, which precinct received the most complaints?`
  - tasks_mini: `In 2022 complaint entries in Queens where the location descriptor is <node_3 answer>, which precinct has the most complaints?`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,22 +7,25 @@
-source = "datagov/nypd-complaint-data-historic/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/nypd-complaint-data-historic/files/rows.txt'
```

- Node 5 `subquestion`
  - copy: `In 2024, how many incidents involving officers using force occurred in precinct <hop 4 answer>?`
  - tasks_mini: `In 2024 use-of-force incidents, how many incidents occurred in precinct <node_4 answer>?`

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import os
@@ -6,10 +7,21 @@
-source = "datagov/nypd-use-of-force-incidents/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/nypd-use-of-force-incidents/files/rows.txt'
```

### `k-5-d-2/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Texas counties had at least 10% adult disabled population and at least 23% elderly population in 2023?`
  - tasks_mini: `Which Texas counties had at least 10% adult disabled population and at least 23% elderly population in FY2023?`

- Node 2 `subquestion`
  - copy: `Which Texas counties in the Abilene region had 150 or more completed adult-protection investigations in 2023?`
  - tasks_mini: `Which Texas counties in Region 2-Abilene had 150 or more completed APS investigations in FY2023?`

- Node 3 `subquestion`
  - copy: `How many completed investigations into possible child abuse or neglect were recorded in Eastland County in 2023?`
  - tasks_mini: `How many completed child abuse/neglect investigations did Eastland County have in FY2023?`

- Node 4 `subquestion`
  - copy: `How many completed investigations into possible child abuse or neglect were recorded in Montague County in 2023?`
  - tasks_mini: `How many completed child abuse/neglect investigations did Montague County have in FY2023?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-The Regulators would go through three different leaders, all but one being killed. Although Billy the Kid would achieve fame as a member of the Regulators, he never led them. Their first leader was Richard "Dick" Brewer, killed later by Buckshot Roberts and replaced by Frank McNab, who was killed by members of the Seven Rivers Warriors. McNab was replaced by the Regulators final leader, Doc Scurlock.
+The Lincoln County Regulators had three leaders: Richard "Dick" Brewer (first), Frank McNab (second), and Doc Scurlock (third and final).
```

- Node 6 `subquestion`
  - copy: `Which of <hop 3 answer> died in <hop 2 answer>, and what county was he born in?`
  - tasks_mini: `Which of <node_5 answer> died in the county seat of the county with fewer CPI investigations (Eastland County, 149 < 193)?`

- Node 6 `fact`

```diff
@@ -1,3 +1 @@
-He was born in Tallapoosa County, Alabama, January 11, 1849, the sixth of 11 children born to Priestly Norman Scurlock (July 3, 1806 – June 22, 1876) and Esther Ann Brown (May 19, 1819 – June 1, 1903). Josiah was said to have studied medicine in New Orleans, thus receiving his nickname "Doc".
-
-Doc Scurlock died at age 80 from a heart attack in Eastland, Texas. He is interred in Eastland City Cemetery, along with his wife and other family members.
+Doc Scurlock died in Eastland, Texas. He was born in Tallapoosa County, Alabama.
```

- Node 7 `subquestion`
  - copy: `What is the county seat of the Alabama county where <node 6 answer> was born?`
  - tasks_mini: `What is the county seat of the Alabama county where <node_6 answer> was born?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Tallapoosa County is a county located in the east-central portion of the U.S. state of Alabama."ACES Tallapoosa County Office" (links/history), Alabama Cooperative Extension System (ACES), 2007, webpage: ACES-Tallapoosa. As of the 2020 census, the population was 41,311. Its county seat is Dadeville.
+Tallapoosa County's county seat is Dadeville.
```

### `k-5-d-2/task_10.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/recidivism-beginning-2008/files/rows.txt`
  - tasks_mini: `datagov/500-cities-city-level-data-gis-friendly-format-2016-release/files/rows.txt`

- Node 1 `subquestion`
  - copy: `What were the 2018 rates of being sent back to prison or jail for New York counties excluding NYC boroughs?`
  - tasks_mini: `Which California cities had teeth loss crude prevalence (TEETHLOST_CrudePrev) above 19% in the 2016 CDC 500 Cities data (StateAbbr = CA)?`

- Node 1 `answer`
  - copy: `{"ALBANY": "43.0%", "ALLEGANY": "47.2%", "BROOME": "46.0%", "CATTARAUGUS": "33.0%", "CAYUGA": "47.4%", "CHAUTAUQUA": "46.5%", "CHEMUNG": "43.0%", "CHENANGO": "39.1%", "CLINTON": "27.9%", "COLUMBIA": "32.0%"}`
  - tasks_mini: `["Compton", "San Bernardino"]`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -5,4 +5,3 @@
-
-source = "datagov/recidivism-beginning-2008/files/rows.txt"
+source = "datagov/500-cities-city-level-data-gis-friendly-format-2016-release/files/rows.txt"
@@ -10,12 +9,6 @@
-
-exclude_counties = {"BRONX", "KINGS", "NEW YORK", "QUEENS", "RICHMOND", "UNKNOWN"}
-returned_statuses = {"Returned Parole Violation", "New Felony Offense"}
```

- Node 2 `source`
  - copy: `datagov/recidivism-beginning-2008/files/rows.txt`
  - tasks_mini: `datagov/500-cities-city-level-data-gis-friendly-format-2017-release/files/rows.txt`

- Node 2 `subquestion`
  - copy: `What were the 2019 rates of being sent back to prison or jail for New York counties excluding NYC boroughs?`
  - tasks_mini: `Which California cities had mental health crude prevalence (MHLTH_CrudePrev) above 15% in the 2017 CDC 500 Cities data (StateAbbr = CA)?`

- Node 2 `answer`
  - copy: `{"ALBANY": "34.1%", "ALLEGANY": "26.3%", "BROOME": "36.6%", "CATTARAUGUS": "33.3%", "CAYUGA": "37.6%", "CHAUTAUQUA": "31.4%", "CHEMUNG": "36.5%", "CHENANGO": "29.3%", "CLINTON": "26.4%", "COLUMBIA": "21.8%"}`
  - tasks_mini: `["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Santa Ana", "Santa Maria", "South Gate"]`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -5,4 +5,3 @@
-
-source = "datagov/recidivism-beginning-2008/files/rows.txt"
+source = "datagov/500-cities-city-level-data-gis-friendly-format-2017-release/files/rows.txt"
@@ -10,12 +9,7 @@
-
-exclude_counties = {"BRONX", "KINGS", "NEW YORK", "QUEENS", "RICHMOND", "UNKNOWN"}
-returned_statuses = {"Returned Parole Violation", "New Felony Offense"}
```

- Node 3 `source`
  - copy: `datagov/motor-vehicle-crashes-case-information-three-year-window/files/rows.txt`
  - tasks_mini: `wikipedia/Compton,_California/content.txt`

- Node 3 `subquestion`
  - copy: `What were the 2019 counts of traffic crashes for New York counties excluding NYC boroughs?`
  - tasks_mini: `What county is <intersection of nodes 1-2: Compton> in?`

- Node 3 `answer`
  - copy: `{"ALBANY": "9930", "ALLEGANY": "1322", "BROOME": "5401", "CATTARAUGUS": "1950", "CAYUGA": "2291", "CHAUTAUQUA": "3001", "CHEMUNG": "2190", "CHENANGO": "1399", "CLINTON": "2362", "COLUMBIA": "2087"}`
  - tasks_mini: `Los Angeles County`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1,22 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 4 `source`
  - copy: `datagov/motor-vehicle-crashes-case-information-three-year-window/files/rows.txt`
  - tasks_mini: `wikipedia/San_Bernardino,_California/content.txt`

- Node 4 `subquestion`
  - copy: `What were the 2020 counts of traffic crashes for New York counties excluding NYC boroughs?`
  - tasks_mini: `What county is <intersection of nodes 1-2: San Bernardino> in?`

- Node 4 `answer`
  - copy: `{"ALBANY": "7564", "ALLEGANY": "1061", "BROOME": "4367", "CATTARAUGUS": "1631", "CAYUGA": "1883", "CHAUTAUQUA": "2477", "CHEMUNG": "1929", "CHENANGO": "1270", "CLINTON": "1711", "COLUMBIA": "1720"}`
  - tasks_mini: `San Bernardino County`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1,22 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 5 `source`
  - copy: `wikipedia/Erie_County,_New_York/content.txt`
  - tasks_mini: `wikipedia/Los_Angeles_County,_California/content.txt`

- Node 5 `subquestion`
  - copy: `After whom or what is Erie from <hop 2 answer> named?`
  - tasks_mini: `When was <node 3: Los Angeles County> formed?`

- Node 5 `answer`
  - copy: `Erie tribe of Native Americans`
  - tasks_mini: `1850`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Both the county and Lake Erie were named for the regional Iroquoian language-speaking Erie tribe of Native Americans, who lived in the area before 1654.
+Los Angeles County is one of the original counties of California, created at the time of statehood in 1850. It is the most populous county in the United States. The county's seat is Los Angeles.
```

- Node 6 `source`
  - copy: `wikipedia/Monroe_County,_New_York/content.txt`
  - tasks_mini: `wikipedia/San_Bernardino_County,_California/content.txt`

- Node 6 `subquestion`
  - copy: `After whom or what is Monroe from <hop 2 answer> named?`
  - tasks_mini: `When was <node 4: San Bernardino County> formed?`

- Node 6 `answer`
  - copy: `James Monroe, the fifth president of the United States`
  - tasks_mini: `1853`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The county is named after James Monroe, the fifth president of the United States.
+San Bernardino County was formed in 1853 from parts of Los Angeles County.
```

- Node 7 `source`
  - copy: `wikipedia/James_Monroe/content.txt`
  - tasks_mini: `wikipedia/Los_Angeles/content.txt`

- Node 7 `subquestion`
  - copy: `In which county was <hop 3 answer> born?`
  - tasks_mini: `Under which Spanish governor was <comparative of nodes 5-6: Los Angeles County, formed earlier (1850 < 1853)>'s county seat founded?`

- Node 7 `answer`
  - copy: `Westmoreland County, Virginia`
  - tasks_mini: `Felipe de Neve`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-James Monroe was born on April 28, 1758, in his parents' house in a wooded area of Westmoreland County in the Colony of Virginia
+Los Angeles, the county seat of Los Angeles County, was founded on September 4, 1781, under Spanish governor Felipe de Neve, on the village of Yaanga.
```

- Node 8 `source`
  - copy: `wikipedia/Westmoreland_County,_Virginia/content.txt`
  - tasks_mini: `wikipedia/Felipe_de_Neve/content.txt`

- Node 8 `subquestion`
  - copy: `In what year was <hop 4 answer> established?`
  - tasks_mini: `In what year was <node 7: Felipe de Neve> born?`

- Node 8 `answer`
  - copy: `1653`
  - tasks_mini: `1724`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-As originally established by the Virginia colony's House of Burgesses, this area was separated from Northumberland County in 1653 and named for the English county of Westmorland
+Felipe de Neve y Padilla (1724 - 3 November 1784) was a Spanish soldier who served as the 4th Governor of the Californias, from 1775 to 1782. He was born in Bailen, Spain.
```

### `k-5-d-2/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which five-time NBA champion team is based in San Antonio?`
  - tasks_mini: `What five-time NBA champion team is based in San Antonio?`

- Node 1 `fact`

```diff
@@ -1 +1 @@
-is home to the five-time NBA champion San Antonio Spurs.
+According to the Wikipedia article for San Antonio, 'San Antonio is also home to the five-time NBA champion San Antonio Spurs.'
```

- Node 2 `subquestion`
  - copy: `Which team did <hop 1 answer> defeat in its first NBA Finals championship?`
  - tasks_mini: `Which team did <node_1 answer> defeat in their first NBA Finals championship?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-In the NBA Finals, they faced the New York Knicks, who had made history by becoming the first eighth seed to ever make the NBA Finals.
+According to the Wikipedia article for San Antonio Spurs. For their first championship in 1999, the article states they 'defeated the New York Knicks' in the NBA Finals.
```

- Node 3 `subquestion`
  - copy: `Which New York City borough is <hop 2 answer> based in?`
  - tasks_mini: `In which New York City borough is <node_2 answer> based?`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-based in the New York City borough of Manhattan.
+According to the Wikipedia article for New York Knicks, 'The New York Knickerbockers, commonly known as the New York Knicks, are an American professional basketball team based in the New York City borough of Manhattan.'
```

- Node 4 `subquestion`
  - copy: `Which county is the same geographic area as <hop 3 answer>?`
  - tasks_mini: `Which county is coextensive with <node_3 answer>?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Coextensive with New York County, Manhattan is the smallest county by area in the U.S. state of New York.
+According to the Wikipedia article for Manhattan, Manhattan is coextensive with New York County.
```

- Node 5 `subquestion`
  - copy: `How many total hate crime incidents were reported in <hop 4 answer> in 2020 across crimes against persons and property crimes?`
  - tasks_mini: `How many total hate crime incidents were there in <node_4 answer> in 2020? (Filter: Year == 2020; County == New York; Crime Type in {Crimes Against Persons, Property Crimes}; sum Total Incidents.)`

- Node 5 `answer`
  - copy: `82`
  - tasks_mini: `82`

- Node 6 `subquestion`
  - copy: `How many firearm crimes were reported in <hop 4 answer> in 2020?`
  - tasks_mini: `How many firearm crimes were there in <node_4 answer> in 2020? (Filter: Year == 2020; County == New York; use Firearm Count.)`

- Node 6 `answer`
  - copy: `898`
  - tasks_mini: `898`

### `k-5-d-2/task_3.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/500-cities-local-data-for-better-health-2016-release/files/rows.txt`
  - tasks_mini: `datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-meal-reimbursement-program-ye-2018/files/rows.txt`

- Node 1 `subquestion`
  - copy: `What are the top-ranked US cities in the 2016 release by age-adjusted adult obesity prevalence, while preserving the full city-level obesity table needed for the later 2016+2018 comparison?`
  - tasks_mini: `Among {Harris, Hidalgo, Dallas, Cameron}, which counties had the largest percentage decrease in day care home meal reimbursements between the 2018-2019 and 2020-2021 program years? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum TotalMealReimbursement.)`

- Node 1 `answer`
  - copy: `{"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}`
  - tasks_mini: `{"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}`

- Node 1 `fact`

```diff
@@ -4,21 +4,13 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/500-cities-local-data-for-better-health-2016-release/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 2 `source`
  - copy: `datagov/500-cities-local-data-for-better-health-2018-release/files/rows.txt`
  - tasks_mini: `datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-meal-reimbursement-program-ye-2020/files/rows.txt`

- Node 2 `subquestion`
  - copy: `What are the top-ranked US cities in the 2018 release by age-adjusted adult obesity prevalence, while preserving the full city-level obesity table needed for the later 2016+2018 comparison?`
  - tasks_mini: `Among {Harris, Hidalgo, Dallas, Cameron}, which counties had the largest percentage decrease in day care home meal reimbursements between the 2018-2019 and 2020-2021 program years? (Filter for this node: ProgramYear == 2020-2021; group by SiteCounty; sum TotalMealReimbursement.)`

- Node 2 `answer`
  - copy: `{"Detroit": 47.4, "Flint": 45.4, "Gary": 49.0}`
  - tasks_mini: `{"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}`

- Node 2 `fact`

```diff
@@ -4,21 +4,13 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/500-cities-local-data-for-better-health-2018-release/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 3 `source`
  - copy: `wikipedia/Gary,_Indiana/content.txt`
  - tasks_mini: `datagov/child-and-adult-care-food-program-cacfp-child-centers-meal-reimbursement-program-year-2018/files/rows.txt`

- Node 3 `subquestion`
  - copy: `What corporation founded <hop 1 answer>?`
  - tasks_mini: `Among {Hidalgo, Cameron}, which county had the higher average child center enrollment across the 2018-2019 and 2019-2020 program years? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum EnrollmentQty.)`

- Node 3 `answer`
  - copy: `U.S. Steel Corporation`
  - tasks_mini: `{"Cameron": 7620183, "Hidalgo": 1661128}`

- Node 3 `fact`

```diff
@@ -1 +1,16 @@
-founded in 1906 by the U.S. Steel corporation as the home for its new plant, Gary Works.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.client import Config
```

- Node 4 `source`
  - copy: `wikipedia/U.S._Steel/content.txt`
  - tasks_mini: `datagov/child-and-adult-care-food-program-cacfp-child-centers-meal-reimbursement-program-year-2019/files/rows.txt`

- Node 4 `subquestion`
  - copy: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create <hop 2 answer>?`
  - tasks_mini: `Among {Hidalgo, Cameron}, which county had the higher average child center enrollment across the 2018-2019 and 2019-2020 program years? (Filter for this node: ProgramYear == 2019-2020; group by SiteCounty; sum EnrollmentQty.)`

- Node 4 `answer`
  - copy: `Carnegie Steel Company`
  - tasks_mini: `{"Cameron": 1076746, "Hidalgo": 1477805}`

- Node 4 `fact`

```diff
@@ -1 +1,16 @@
-In 1901, J. P. Morgan created U.S. Steel by merging Carnegie Steel, Federal Steel, and National Steel
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.client import Config
```

- Node 5 `source`
  - copy: `wikipedia/Carnegie_Steel_Company/content.txt`
  - tasks_mini: `wikipedia/Cameron_County,_Texas/content.txt`

- Node 5 `subquestion`
  - copy: `Who founded <hop 3 answer>?`
  - tasks_mini: `What is the county seat of Cameron County, Texas (from the higher-enrollment county in the previous step)?`

- Node 5 `answer`
  - copy: `Andrew Carnegie`
  - tasks_mini: `Brownsville`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie
+Cameron County's county seat is Brownsville.
```

- Node 6 `source`
  - copy: `wikipedia/Andrew_Carnegie/content.txt`
  - tasks_mini: `wikipedia/Brownsville,_Texas/content.txt`

- Node 6 `subquestion`
  - copy: `Where was <hop 4 answer> based?`
  - tasks_mini: `On which coast is Brownsville located?`

- Node 6 `answer`
  - copy: `Pittsburgh, Pennsylvania`
  - tasks_mini: `Gulf Coast`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Pittsburgh, Pennsylvania, with his parents in 1848 at the age of 12.
+Brownsville is located on the western Gulf Coast in South Texas.
```

### `k-5-d-2/task_4.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/ocs-1-1-abuse-neglect-related-texas-child-fatalities-fy2013-fy2022/files/rows.txt`
  - tasks_mini: `datagov/500-cities-local-data-for-better-health-2016-release/files/rows.txt`

- Node 1 `subquestion`
  - copy: `Among Brooks, Willacy, Comal, Atascosa, and Victoria counties, which had at least 1 abuse/neglect-related child fatality (2018-2022)?`
  - tasks_mini: `What is the US city with the highest average age-adjusted adult obesity rate (2016-2018)? (Filter for this node: GeographicLevel == City; Measure == "Obesity among adults aged >=18 Years"; Data_Value_Type == "Age-adjusted prevalence"; rank by Data_Value; keep top 3.)`

- Node 1 `answer`
  - copy: `["Victoria", "Comal", "Willacy", "Brooks"]`
  - tasks_mini: `{"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}`

- Node 1 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/ocs-1-1-abuse-neglect-related-texas-child-fatalities-fy2013-fy2022/files/rows.txt"
+
+source = "datagov/500-cities-local-data-for-better-health-2016-release/files/rows.txt"
@@ -10,10 +11,14 @@
-target_counties = ["Brooks", "Willacy", "Comal", "Atascosa", "Victoria"]
-
-county_totals = (
```

- Node 2 `source`
  - copy: `datagov/ocs-1-2-non-abuse-neglect-related-texas-child-fatality-investigations-fy2013-fy2022/files/rows.txt`
  - tasks_mini: `datagov/500-cities-local-data-for-better-health-2018-release/files/rows.txt`

- Node 2 `subquestion`
  - copy: `Among Brooks, Willacy, Comal, Atascosa, and Victoria counties, which had at least 3 non-abuse/neglect child fatality investigations (2018-2022)?`
  - tasks_mini: `What is the US city with the highest average age-adjusted adult obesity rate (2016-2018)? (Filter for this node: GeographicLevel == City; Measure == "Obesity among adults aged >=18 Years"; Data_Value_Type == "Age-adjusted prevalence"; rank by Data_Value; keep top 3.)`

- Node 2 `answer`
  - copy: `["Comal", "Victoria", "Atascosa", "Willacy"]`
  - tasks_mini: `{"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}`

- Node 2 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/ocs-1-2-non-abuse-neglect-related-texas-child-fatality-investigations-fy2013-fy2022/files/rows.txt"
+
+source = "datagov/500-cities-local-data-for-better-health-2018-release/files/rows.txt"
@@ -10,10 +11,14 @@
-target_counties = ["Brooks", "Willacy", "Comal", "Atascosa", "Victoria"]
-
-county_totals = (
```

- Node 3 `source`
  - copy: `datagov/nchs-drug-poisoning-mortality-by-county-united-states/files/rows.txt`
  - tasks_mini: `wikipedia/Gary,_Indiana/content.txt`

- Node 3 `subquestion`
  - copy: `For the counties that remain after applying <hop 1 answer>, what are their 2021 model-based drug poisoning death rates in Texas, and which two counties rank highest?`
  - tasks_mini: `What corporation founded the highest obesity city (Gary, Indiana)?`

- Node 3 `answer`
  - copy: `["Victoria County, TX", "Comal County, TX"]`
  - tasks_mini: `U.S. Steel Corporation`

- Node 3 `fact`

```diff
@@ -1,20 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/nchs-drug-poisoning-mortality-by-county-united-states/files/rows.txt"
```

- Node 4 `source`
  - copy: `datagov/nchs-drug-poisoning-mortality-by-county-united-states-20278/files/rows.txt`
  - tasks_mini: `wikipedia/U.S._Steel/content.txt`

- Node 4 `subquestion`
  - copy: `For the counties that remain after applying <hop 1 answer>, what are their 2016 estimated age-adjusted drug poisoning death rate categories in Texas, and which two counties rank lowest?`
  - tasks_mini: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create U.S. Steel?`

- Node 4 `answer`
  - copy: `["Willacy County, TX", "Victoria County, TX"]`
  - tasks_mini: `Carnegie Steel Company`

- Node 4 `fact`

```diff
@@ -1,22 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/nchs-drug-poisoning-mortality-by-county-united-states-20278/files/rows.txt"
```

- Node 5 `source`
  - copy: `wikipedia/Victoria_County,_Texas/content.txt`
  - tasks_mini: `wikipedia/Carnegie_Steel_Company/content.txt`

- Node 5 `subquestion`
  - copy: `What is the county seat of <hop 2 answer>?`
  - tasks_mini: `Who founded Carnegie Steel Company?`

- Node 5 `answer`
  - copy: `Victoria`
  - tasks_mini: `Andrew Carnegie`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Its county seat is also named Victoria.
+Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie to manage businesses at steel mills in the Pittsburgh, Pennsylvania area.
```

- Node 6 `source`
  - copy: `wikipedia/Victoria,_Texas/content.txt`
  - tasks_mini: `wikipedia/Andrew_Carnegie/content.txt`

- Node 6 `subquestion`
  - copy: `What river does <hop 3 answer> lie along and just to the east of?`
  - tasks_mini: `Where was Andrew Carnegie based?`

- Node 6 `answer`
  - copy: `Guadalupe River`
  - tasks_mini: `Pittsburgh, Pennsylvania`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-It lies along and just to the east of the Guadalupe River.
+Andrew Carnegie immigrated to Pittsburgh, Pennsylvania, with his parents in 1848. He built Pittsburgh's Carnegie Steel Company, which he sold to J.P. Morgan in 1901.
```

### `k-5-d-2/task_5.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/311-city-service-requests-in-2019/files/data.txt`
  - tasks_mini: `datagov/ocs-1-1-abuse-neglect-related-texas-child-fatalities-fy2013-fy2022/files/rows.txt`

- Node 1 `subquestion`
  - copy: `For 2019, how many 311 service requests were recorded in Ward 7 and Ward 8?`
  - tasks_mini: `Among Brooks, Willacy, Comal, Atascosa, and Victoria counties, which had at least 1 abuse/neglect-related child fatality (2018-2022)? (Filter for this node: Fiscal Year in 2018-2022; group by County; sum Abuse Neglect Fatalities.)`

- Node 1 `answer`
  - copy: `["Ward 7 (42,226)", "Ward 8 (34,959)"]`
  - tasks_mini: `["Brooks County", "Willacy County", "Comal County", "Victoria County"]`

- Node 1 `fact`

```diff
@@ -1,3 +1,2 @@
-import json
@@ -6,16 +5,15 @@
-source = "datagov/311-city-service-requests-in-2019/files/data.txt"
+source = "datagov/ocs-1-1-abuse-neglect-related-texas-child-fatalities-fy2013-fy2022/files/rows.txt"
-data = json.load(io.TextIOWrapper(obj["Body"], encoding="utf-8"))
-df = pd.json_normalize(data["features"])
-ward_col = "properties.WARD"
```

- Node 2 `source`
  - copy: `datagov/311-city-service-requests-in-2020/files/data.txt`
  - tasks_mini: `datagov/ocs-1-2-non-abuse-neglect-related-texas-child-fatality-investigations-fy2013-fy2022/files/rows.txt`

- Node 2 `subquestion`
  - copy: `For 2020, how many 311 service requests were recorded in Ward 7 and Ward 8?`
  - tasks_mini: `Among Brooks, Willacy, Comal, Atascosa, and Victoria counties, which had at least 3 non-abuse/neglect child fatality investigations (2018-2022)? (Filter for this node: Fiscal Year in 2018-2022; group by County; sum Non-Abuse/Neglect Fatalities Investigated.)`

- Node 2 `answer`
  - copy: `["Ward 8 (37,124)", "Ward 7 (36,113)"]`
  - tasks_mini: `["Willacy County", "Comal County", "Atascosa County", "Victoria County"]`

- Node 2 `fact`

```diff
@@ -1,3 +1,2 @@
-import json
@@ -6,16 +5,15 @@
-source = "datagov/311-city-service-requests-in-2020/files/data.txt"
+source = "datagov/ocs-1-2-non-abuse-neglect-related-texas-child-fatality-investigations-fy2013-fy2022/files/rows.txt"
-data = json.load(io.TextIOWrapper(obj["Body"], encoding="utf-8"))
-df = pd.json_normalize(data["features"])
-ward_col = "properties.WARD"
```

- Node 3 `source`
  - copy: `wikipedia/Neighborhoods_in_Washington,_D.C./content.txt`
  - tasks_mini: `datagov/nchs-drug-poisoning-mortality-by-county-united-states/files/rows.txt`

- Node 3 `subquestion`
  - copy: `Who represents <hop 1 answer> on the DC Council?`
  - tasks_mini: `Among the counties from hop 1, which two had the highest model-based drug poisoning death rates in 2021? (Filter for this node: Year == 2021; State == Texas; County in {Comal County, TX, Victoria County, TX, Willacy County, TX}; use Model-based Death Rate.)`

- Node 3 `answer`
  - copy: `Wendell Felder`
  - tasks_mini: `["Victoria County", "Comal County"]`

- Node 3 `fact`

```diff
@@ -1 +1,20 @@
-Ward 7 Councilmember: Wendell Felder
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 4 `source`
  - copy: `wikipedia/Wendell_Felder/content.txt`
  - tasks_mini: `datagov/nchs-drug-poisoning-mortality-by-county-united-states-20278/files/rows.txt`

- Node 4 `subquestion`
  - copy: `Which university did <hop 2 answer> attend for graduate studies?`
  - tasks_mini: `Among the counties from hop 1, which two had the lowest age-adjusted drug poisoning death rate categories in 2016? (Filter for this node: Year == 2016; State == Texas; County in {Comal County, TX, Victoria County, TX, Willacy County, TX}; use Estimated Age-adjusted Death Rate, 16 Categories (in ranges).)`

- Node 4 `answer`
  - copy: `Georgetown University`
  - tasks_mini: `["Willacy County", "Victoria County"]`

- Node 4 `fact`

```diff
@@ -1 +1,22 @@
-received a B.S. from Bowie State University and a M.A. from Georgetown University
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 5 `source`
  - copy: `wikipedia/Georgetown_University/content.txt`
  - tasks_mini: `wikipedia/Victoria_County,_Texas/content.txt`

- Node 5 `subquestion`
  - copy: `Who founded <hop 3 answer>?`
  - tasks_mini: `What is the county seat of the county identified in hop 2? (Lookup: county seat statement in the Victoria County, Texas article.)`

- Node 5 `answer`
  - copy: `John Carroll`
  - tasks_mini: `Victoria`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Founded by Bishop John Carroll in 1789,
+Victoria County's county seat is Victoria.
```

- Node 6 `source`
  - copy: `wikipedia/Patrick_Francis_Healy/content.txt`
  - tasks_mini: `wikipedia/Victoria,_Texas/content.txt`

- Node 6 `subquestion`
  - copy: `Who is the flagship building of <hop 3 answer>, a National Historic Landmark, named after?`
  - tasks_mini: `What river does the city from hop 3 lie along and just to the east of? (Lookup: Victoria, Texas article location description.)`

- Node 6 `answer`
  - copy: `Patrick Francis Healy`
  - tasks_mini: `Guadalupe River`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The university's flagship building, Healy Hall, bears his name.
+Victoria lies along and just to the east of the Guadalupe River.
```

- Node 7 `source`
  - copy: `wikipedia/John_Carroll_(archbishop_of_Baltimore)/content.txt`
  - tasks_mini: `wikipedia/Guadalupe_River_(Texas)/content.txt`

- Node 7 `subquestion`
  - copy: `In what year was <node 5 answer> born?`
  - tasks_mini: `What bay on the Gulf Coast does the river from hop 4 run to? (Lookup: Guadalupe River (Texas) article statement about San Antonio Bay.)`

- Node 7 `answer`
  - copy: `1735`
  - tasks_mini: `San Antonio Bay`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-John Carroll (January 8, 1735 – December 3, 1815)
+The Guadalupe River runs from Kerr County, Texas, to San Antonio Bay on the Gulf Coast.
```

### `k-5-d-2/task_6.json`
- Impact: major
- Node 1 `source`
  - copy: `wikipedia/Gary,_Indiana/content.txt`
  - tasks_mini: `datagov/311-city-service-requests-in-2019/files/data.txt`

- Node 1 `subquestion`
  - copy: `What corporation founded Gary, Indiana?`
  - tasks_mini: `Between DC wards 7 and 8, which had higher average 311 service requests (2019-2020)? (Filter for this node: WARD in {7, 8}; group by WARD; count records.)`

- Node 1 `answer`
  - copy: `U.S. Steel Corporation`
  - tasks_mini: `["Ward 7 (42,226)", "Ward 8 (34,959)"]`

- Node 1 `fact`

```diff
@@ -1 +1,17 @@
-Gary, Indiana was founded in 1906 by the U.S. Steel corporation as the home for its new plant, Gary Works.
+import json
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 2 `source`
  - copy: `wikipedia/U.S._Steel/content.txt`
  - tasks_mini: `datagov/311-city-service-requests-in-2020/files/data.txt`

- Node 2 `subquestion`
  - copy: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create <hop 1 answer>?`
  - tasks_mini: `Between DC wards 7 and 8, which had higher average 311 service requests (2019-2020)? (Filter for this node: WARD in {7, 8}; group by WARD; count records.)`

- Node 2 `answer`
  - copy: `Carnegie Steel Company`
  - tasks_mini: `["Ward 7 (36,113)", "Ward 8 (37,124)"]`

- Node 2 `fact`

```diff
@@ -1 +1,17 @@
-In 1901, J. P. Morgan created U.S. Steel by merging Carnegie Steel, Federal Steel, and National Steel.
+import json
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 3 `source`
  - copy: `wikipedia/Carnegie_Steel_Company/content.txt`
  - tasks_mini: `wikipedia/Neighborhoods_in_Washington,_D.C./content.txt`

- Node 3 `subquestion`
  - copy: `Who founded <hop 2 answer>?`
  - tasks_mini: `Who represents the selected ward (from hop 1) on the DC Council?`

- Node 3 `answer`
  - copy: `Andrew Carnegie`
  - tasks_mini: `Wendell Felder`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie to manage businesses at steel mills in the Pittsburgh, Pennsylvania area.
+Ward 7 Councilmember: Wendell Felder. Ward 7 has a population of 77,456 (2022).
```

- Node 4 `source`
  - copy: `wikipedia/Andrew_Carnegie/content.txt`
  - tasks_mini: `wikipedia/Wendell_Felder/content.txt`

- Node 4 `subquestion`
  - copy: `Where was <hop 3 answer> based?`
  - tasks_mini: `Which university did the council member (from hop 2) attend for graduate studies?`

- Node 4 `answer`
  - copy: `Pittsburgh, Pennsylvania`
  - tasks_mini: `Georgetown University`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Andrew Carnegie immigrated to Pittsburgh, Pennsylvania, with his parents in 1848. He built Pittsburgh's Carnegie Steel Company, which he sold to J.P. Morgan in 1901.
+Wendell Felder received a B.S. from Bowie State University and a M.A. from Georgetown University.
```

- Node 5 `source`
  - copy: `datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2017-operating.txt`
  - tasks_mini: `wikipedia/Georgetown_University/content.txt`

- Node 5 `subquestion`
  - copy: `In <hop 4 answer>, what was the total 2017 expenditure for the Police Bureau?`
  - tasks_mini: `Who founded the university (from hop 3), and who is its flagship building (a National Historic Landmark) named after?`

- Node 5 `answer`
  - copy: `98453962.68`
  - tasks_mini: `John Carroll`

- Node 5 `fact`

```diff
@@ -1,17 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 6 `source`
  - copy: `datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2018-operating.txt`
  - tasks_mini: `wikipedia/Georgetown_University/content.txt`

- Node 6 `subquestion`
  - copy: `In <hop 4 answer>, what was the total 2018 expenditure for the Police Bureau?`
  - tasks_mini: `Who founded the university (from hop 3), and who is its flagship building (a National Historic Landmark) named after?`

- Node 6 `answer`
  - copy: `100261931.64`
  - tasks_mini: `Patrick Francis Healy`

- Node 6 `fact`

```diff
@@ -1,17 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

### `k-5-d-2/task_7.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/accidental-drug-related-deaths-2012-2018/files/rows.txt`
  - tasks_mini: `wikipedia/Gary,_Indiana/content.txt`

- Node 1 `subquestion`
  - copy: `Which Connecticut counties had more than 200 accidental overdose deaths in 2020, and what were those totals?`
  - tasks_mini: `What corporation founded Gary, Indiana?`

- Node 1 `answer`
  - copy: `{"Fairfield County": 208, "Hartford County": 335, "New Haven County": 383}`
  - tasks_mini: `U.S. Steel Corporation`

- Node 1 `fact`

```diff
@@ -1,24 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 2 `source`
  - copy: `datagov/connecticut-covid-19-community-levels-by-county-as-originally-posted/files/rows.txt`
  - tasks_mini: `wikipedia/U.S._Steel/content.txt`

- Node 2 `subquestion`
  - copy: `Which Connecticut counties were assigned to a COVID health-service region with a number above 80?`
  - tasks_mini: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create U.S. Steel?`

- Node 2 `answer`
  - copy: `["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"]`
  - tasks_mini: `Carnegie Steel Company`

- Node 2 `fact`

```diff
@@ -1,13 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 3 `source`
  - copy: `wikipedia/New_Haven_County,_Connecticut/content.txt`
  - tasks_mini: `wikipedia/Carnegie_Steel_Company/content.txt`

- Node 3 `subquestion`
  - copy: `Which city in the higher-accidental-drug-death county from <hop 1 answer> is the largest?`
  - tasks_mini: `Who founded Carnegie Steel Company?`

- Node 3 `answer`
  - copy: `New Haven`
  - tasks_mini: `Andrew Carnegie`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Two of the state's five largest cities, New Haven (3rd) and Waterbury (5th), are part of New Haven County.
+Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie to manage businesses at steel mills in the Pittsburgh, Pennsylvania area.
```

- Node 4 `source`
  - copy: `wikipedia/Fairfield_County,_Connecticut/content.txt`
  - tasks_mini: `wikipedia/Andrew_Carnegie/content.txt`

- Node 4 `subquestion`
  - copy: `Which city in the lower-accidental-drug-death county from <hop 1 answer> is the largest?`
  - tasks_mini: `Where was Andrew Carnegie based?`

- Node 4 `answer`
  - copy: `Bridgeport`
  - tasks_mini: `Pittsburgh, Pennsylvania`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-the county contains four of the state's seven largest cities—Bridgeport (first), Stamford (second), Norwalk (sixth) and Danbury (seventh)—whose combined population of 433,368 is nearly half the county's total population.
+Andrew Carnegie immigrated to Pittsburgh, Pennsylvania, with his parents in 1848. He built Pittsburgh's Carnegie Steel Company, which he sold to J.P. Morgan in 1901.
```

- Node 5 `source`
  - copy: `datagov/500-cities-city-level-data-gis-friendly-format-2018-release/files/rows.txt`
  - tasks_mini: `datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2017-operating.txt`

- Node 5 `subquestion`
  - copy: `What was the unadjusted percentage of adults ages 18-64 in <hop 2 answer> who currently did not have health insurance in 2018?`
  - tasks_mini: `What was Pittsburgh's average Police Bureau expenditure in 2017-2018? (Filter for this node: Year == 2017; Type == Expenditure; Department == "PS - Police Bureau"; sum Amount.)`

- Node 5 `answer`
  - copy: `{"Bridgeport": "16.9%", "New Haven": "13.9%"}`
  - tasks_mini: `{"2017": "$98,453,962.68"}`

- Node 5 `fact`

```diff
@@ -6,8 +6,17 @@
-source = "datagov/500-cities-city-level-data-gis-friendly-format-2018-release/files/rows.txt"
+source = "datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2017-operating.txt"
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+df = pd.read_csv(io.BytesIO(obj["Body"].read()), sep=",", engine="c", low_memory=False)
+node_2_answer = 'Pittsburgh, Pennsylvania'
-filtered = df[(df["StateAbbr"] == "CT") & (df["PlaceName"].isin(["New Haven", "Bridgeport"]))].copy()
```

- Node 6 `source`
  - copy: `datagov/500-cities-city-level-data-gis-friendly-format-2019-release/files/rows.txt`
  - tasks_mini: `datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2018-operating.txt`

- Node 6 `subquestion`
  - copy: `What was the unadjusted percentage of adults ages 18-64 in <hop 2 answer> who currently did not have health insurance in 2019?`
  - tasks_mini: `What was Pittsburgh's average Police Bureau expenditure in 2017-2018? (Filter for this node: Year == 2018; Type == Expenditure; Department == "PS - Police Bureau"; sum Amount.)`

- Node 6 `answer`
  - copy: `{"Bridgeport": "19.3%", "New Haven": "15.4%"}`
  - tasks_mini: `{"2018": "$100,261,931.64"}`

- Node 6 `fact`

```diff
@@ -6,8 +6,17 @@
-source = "datagov/500-cities-city-level-data-gis-friendly-format-2019-release/files/rows.txt"
+source = "datagov/2011-2023-city-of-pittsburgh-operating-budget/files/2018-operating.txt"
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+df = pd.read_csv(io.BytesIO(obj["Body"].read()), sep=",", engine="c", low_memory=False)
+node_2_answer = 'Pittsburgh, Pennsylvania'
-filtered = df[(df["StateAbbr"] == "CT") & (df["PlaceName"].isin(["New Haven", "Bridgeport"]))].copy()
```

### `k-5-d-2/task_8.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt`
  - tasks_mini: `datagov/accidental-drug-related-deaths-2012-2018/files/rows.txt`

- Node 1 `subquestion`
  - copy: `What were the 2017 total Medicaid-paid amounts for adult mental health claims in each New York county, excluding NYC boroughs?`
  - tasks_mini: `Which Connecticut counties had over 200 accidental drug deaths in 2020?`

- Node 1 `answer`
  - copy: `{"Albany": "$19,408,513", "Dutchess": "$25,427,485", "Erie": "$70,519,223", "Monroe": "$48,278,139", "Nassau": "$62,927,542", "Onondaga": "$29,668,203", "Orange": "$19,039,890", "Rockland": "$19,216,083", "Suffolk": "$92,420,995", "Westchester": "$66,346,132"}`
  - tasks_mini: `["New Haven County", "Hartford County", "Fairfield County"]`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt"
+
+source = "datagov/accidental-drug-related-deaths-2012-2018/files/rows.txt"
@@ -10,18 +11,7 @@
-nyc_boroughs = ["Bronx", "Kings", "New York", "Queens", "Richmond"]
-result = (
-    df[
```

- Node 2 `source`
  - copy: `datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt`
  - tasks_mini: `datagov/connecticut-covid-19-community-levels-by-county-as-originally-posted/files/rows.txt`

- Node 2 `subquestion`
  - copy: `What were the 2018 total Medicaid-paid amounts for adult mental health claims in each New York county, excluding NYC boroughs?`
  - tasks_mini: `Which Connecticut counties have a COVID-19 health service area number above 80?`

- Node 2 `answer`
  - copy: `{"Albany": "$19,977,245", "Dutchess": "$23,872,388", "Erie": "$81,139,374", "Monroe": "$51,731,436", "Nassau": "$63,138,172", "Onondaga": "$33,679,773", "Orange": "$17,551,508", "Rockland": "$21,794,986", "Suffolk": "$87,249,830", "Westchester": "$67,149,496"}`
  - tasks_mini: `["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"]`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -5,3 +5,4 @@
-source = "datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt"
+
+source = "datagov/connecticut-covid-19-community-levels-by-county-as-originally-posted/files/rows.txt"
@@ -10,18 +11,3 @@
-nyc_boroughs = ["Bronx", "Kings", "New York", "Queens", "Richmond"]
-result = (
-    df[
```

- Node 3 `source`
  - copy: `datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt`
  - tasks_mini: `wikipedia/New_Haven_County,_Connecticut/content.txt`

- Node 3 `subquestion`
  - copy: `What was the total natural gas consumption for the counties in <hop 1 answer> in 2017?`
  - tasks_mini: `Which city in <hop 1 answer: New Haven County> is ranked 3rd among Connecticut's five largest cities?`

- Node 3 `answer`
  - copy: `{"Erie": "621,451,910.24", "Suffolk": "537,382,172"}`
  - tasks_mini: `New Haven`

- Node 3 `fact`

```diff
@@ -1,33 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt"
```

- Node 4 `source`
  - copy: `datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt`
  - tasks_mini: `wikipedia/Fairfield_County,_Connecticut/content.txt`

- Node 4 `subquestion`
  - copy: `What was the total natural gas consumption for the counties in <hop 1 answer> in 2018?`
  - tasks_mini: `Which city in <hop 1 answer: Fairfield County> is ranked first among Connecticut's seven largest cities?`

- Node 4 `answer`
  - copy: `{"Erie": "712,460,330.24", "Suffolk": "556,444,750"}`
  - tasks_mini: `Bridgeport`

- Node 4 `fact`

```diff
@@ -1,33 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt"
```

- Node 5 `source`
  - copy: `wikipedia/Suffolk_County,_New_York/content.txt`
  - tasks_mini: `datagov/500-cities-city-level-data-gis-friendly-format-2018-release/files/rows.txt`

- Node 5 `subquestion`
  - copy: `After which English county is the lower-average-natural-gas-consumption county from <hop 2 answer> named?`
  - tasks_mini: `What was the ACCESS2 (lack of health insurance) rate for <hop 2 answer: New Haven and Bridgeport> in 2018?`

- Node 5 `answer`
  - copy: `Suffolk, England`
  - tasks_mini: `{"Bridgeport": "16.9%", "New Haven": "13.9%"}`

- Node 5 `fact`

```diff
@@ -1 +1,16 @@
-The county was named after the county of Suffolk in England, the origin of its earliest European settlers.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 6 `source`
  - copy: `wikipedia/Ipswich/content.txt`
  - tasks_mini: `datagov/500-cities-city-level-data-gis-friendly-format-2019-release/files/rows.txt`

- Node 6 `subquestion`
  - copy: `What is the county town of <hop 3 answer>?`
  - tasks_mini: `What was the ACCESS2 (lack of health insurance) rate for <hop 2 answer: New Haven and Bridgeport> in 2019?`

- Node 6 `answer`
  - copy: `Ipswich`
  - tasks_mini: `{"Bridgeport": "19.3%", "New Haven": "15.4%"}`

- Node 6 `fact`

```diff
@@ -1 +1,16 @@
-Ipswich () is a port town and borough in Suffolk, England. It is the county town, and largest in Suffolk, followed by Lowestoft and Bury St Edmunds
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 7 `source`
  - copy: `wikipedia/Ipswich/content.txt`
  - tasks_mini: `wikipedia/New_Haven,_Connecticut/content.txt`

- Node 7 `subquestion`
  - copy: `What was the medieval name of <hop 4 answer>?`
  - tasks_mini: `What is the largest employer in <hop 3 answer: New Haven, the city with lower average ACCESS2>?`

- Node 7 `answer`
  - copy: `Gippeswic`
  - tasks_mini: `Yale University`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Ipswich was first recorded during the medieval period as Gippeswic, the town has also been recorded as Gyppewicus and Yppswyche.
+Yale is the city's largest employer, followed by Yale-New Haven Hospital.
```

### `k-5-d-2/task_9.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/500-cities-city-level-data-gis-friendly-format-2016-release/files/rows.txt`
  - tasks_mini: `datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt`

- Node 1 `subquestion`
  - copy: `Which California cities had the unadjusted percentage of older adults with major tooth loss above 19% in 2016?`
  - tasks_mini: `What were the adult mental health Medicaid paid claims for New York counties in 2017?`

- Node 1 `answer`
  - copy: `["San Bernardino", "Compton"]`
  - tasks_mini: `{"Erie": "$70,519,223", "Suffolk": "$92,420,995", "Westchester": "$66,346,132"}`

- Node 1 `fact`

```diff
@@ -5,3 +5,3 @@
-source = "datagov/500-cities-city-level-data-gis-friendly-format-2016-release/files/rows.txt"
+source = "datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt"
@@ -9,7 +9,6 @@
-result = (
-    df.loc[(df["StateAbbr"] == "CA") & (df["TEETHLOST_CrudePrev"] > 19), ["PlaceName", "TEETHLOST_CrudePrev"]]
-    .sort_values(["TEETHLOST_CrudePrev", "PlaceName"], ascending=[False, True])
-    .reset_index(drop=True)
```

- Node 2 `source`
  - copy: `datagov/500-cities-city-level-data-gis-friendly-format-2017-release/files/rows.txt`
  - tasks_mini: `datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt`

- Node 2 `subquestion`
  - copy: `Which California cities had the unadjusted percentage of adults with frequent poor mental health above 15% in 2017?`
  - tasks_mini: `What were the adult mental health Medicaid paid claims for New York counties in 2018?`

- Node 2 `answer`
  - copy: `["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Santa Ana", "Santa Maria", "South Gate"]`
  - tasks_mini: `{"Erie": "$81,139,374", "Suffolk": "$87,249,830", "Westchester": "$67,149,496"}`

- Node 2 `fact`

```diff
@@ -5,3 +5,3 @@
-source = "datagov/500-cities-city-level-data-gis-friendly-format-2017-release/files/rows.txt"
+source = "datagov/county-mental-health-profiles-phase-2-beginning-2014/files/rows.txt"
@@ -9,7 +9,6 @@
-result = (
-    df.loc[(df["StateAbbr"] == "CA") & (df["MHLTH_CrudePrev"] > 15), ["PlaceName", "MHLTH_CrudePrev"]]
-    .sort_values(["PlaceName", "MHLTH_CrudePrev"], ascending=[True, False])
-    .reset_index(drop=True)
```

- Node 3 `source`
  - copy: `wikipedia/Compton,_California/content.txt`
  - tasks_mini: `datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt`

- Node 3 `subquestion`
  - copy: `What county is Compton from <hop 1 answer> in?`
  - tasks_mini: `What was the total natural gas consumption (Total Consumption (T), Therms; data_class=natural_gas) for Erie and Suffolk counties (from <aggregation of nodes 1-2: counties with avg $75M-$95M>) in 2017?`

- Node 3 `answer`
  - copy: `Los Angeles County`
  - tasks_mini: `{"Erie": "621,451,910.24", "Suffolk": "537,382,172"}`

- Node 3 `fact`

```diff
@@ -1 +1,33 @@
-Compton is a city located in the Gateway Cities region of southern Los Angeles County, California, United States
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 4 `source`
  - copy: `wikipedia/San_Bernardino,_California/content.txt`
  - tasks_mini: `datagov/utility-energy-registry-monthly-county-energy-use-beginning-2016/files/rows.txt`

- Node 4 `subquestion`
  - copy: `What county is San Bernardino from <hop 1 answer> in?`
  - tasks_mini: `What was the total natural gas consumption (Total Consumption (T), Therms; data_class=natural_gas) for Erie and Suffolk counties (from <aggregation of nodes 1-2: counties with avg $75M-$95M>) in 2018?`

- Node 4 `answer`
  - copy: `San Bernardino County`
  - tasks_mini: `{"Erie": "712,460,330.24", "Suffolk": "556,444,750"}`

- Node 4 `fact`

```diff
@@ -1 +1,33 @@
-San Bernardino ( ) is a city in and the county seat of San Bernardino County, California, United States.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 5 `source`
  - copy: `wikipedia/Los_Angeles_County,_California/content.txt`
  - tasks_mini: `wikipedia/Suffolk_County,_New_York/content.txt`

- Node 5 `subquestion`
  - copy: `When was <hop 2 answer> Los Angeles County formed?`
  - tasks_mini: `After which English county is <aggregation of nodes 3-4: Suffolk, which has lower average energy (1.42B < 2.14B)> named?`

- Node 5 `answer`
  - copy: `1850`
  - tasks_mini: `Suffolk, England`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Los Angeles County is one of the original counties of California, created at the time of statehood in 1850.
+Suffolk County was named after the county of Suffolk in England, the origin of its earliest European settlers.
```

- Node 6 `source`
  - copy: `wikipedia/San_Bernardino_County,_California/content.txt`
  - tasks_mini: `wikipedia/Ipswich/content.txt`

- Node 6 `subquestion`
  - copy: `When was <hop 2 answer> San Bernardino County formed?`
  - tasks_mini: `What is the county town of <node 5: Suffolk, England>?`

- Node 6 `answer`
  - copy: `1853`
  - tasks_mini: `Ipswich`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-San Bernardino County was formed in 1853 from parts of Los Angeles County.
+Ipswich is a port town and borough in Suffolk, England. It is the county town and largest settlement in Suffolk, followed by Lowestoft and Bury St Edmunds.
```

- Node 7 `source`
  - copy: `wikipedia/Los_Angeles/content.txt`
  - tasks_mini: `wikipedia/Ipswich/content.txt`

- Node 7 `subquestion`
  - copy: `Under which Spanish governor was the county seat of the earlier-formed county from <hop 3 answer> founded?`
  - tasks_mini: `What was the medieval name of <node 6: Ipswich>?`

- Node 7 `answer`
  - copy: `Felipe de Neve`
  - tasks_mini: `Gippeswic`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The city was founded on September 4, 1781, under Spanish governor Felipe de Neve, on the village of Yaanga.
+Ipswich was first recorded during the medieval period as Gippeswic. The town has also been recorded as Gyppewicus and Yppswyche.
```

### `k-5-d-3/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Manhattan District 2 high schools received an A grade for comprehensive performance in 2007-08?`
  - tasks_mini: `Which District 02 Manhattan high schools (DBN starts with '02M') received an OVERALL GRADE of 'A' in 2007-08? (Filter: DBN starts with '02M'; SCHOOL LEVEL* == 'High School'; OVERALL GRADE == 'A'.)`

- Node 1 `fact`

```diff
@@ -6,15 +6,16 @@
-source = "datagov/2007-2008-school-progress-report/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2007-2008-school-progress-report/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 2 `subquestion`
  - copy: `Which Manhattan District 2 high schools received an A grade for comprehensive performance in 2008-09?`
  - tasks_mini: `Which of <hop_1 answer> (match by DBN) also received OVERALL GRADE 'A' in 2008-09? (Filter: DBN in hop_1; DBN starts with '02M'; SCHOOL LEVEL* == 'High School'; OVERALL GRADE == 'A'.)`

- Node 2 `answer`
  - copy: `["02M047 - 47 THE AMERICAN SIGN LANGUAGE AND ENGLISH SECONDARY SCHOOL", "02M288 - FOOD AND FINANCE HIGH SCHOOL", "02M294 - ESSEX STREET ACADEMY", "02M296 - HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "02M298 - PACE HIGH SCHOOL", "02M300 - URBAN ASSEMBLY SCHOOL OF DESIGN AND CONSTRUCTION, THE", "02M303 - FACING HISTORY SCHOOL, THE", "02M308 - LOWER MANHATTAN ART...`
  - tasks_mini: `["02M288 - FOOD AND FINANCE HIGH SCHOOL", "02M294 - ESSEX STREET ACADEMY", "02M296 - HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "02M298 - PACE HIGH SCHOOL", "02M407 - INSTITUTE FOR COLLABORATIVE EDUCATION", "02M408 - PROFESSIONAL PERFORMING ARTS HIGH SCHOOL", "02M411 - BARUCH COLLEGE CAMPUS HIGH SCHOOL", "02M412 - N.Y.C. LAB SCHOOL FOR COLLABORATIVE STUDIES", ...`

- Node 2 `fact`

```diff
@@ -5,15 +5,19 @@
-source = "datagov/2008-2009-school-progress-report/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/2008-2009-school-progress-report/files/rows.txt'
```

- Node 3 `subquestion`
  - copy: `Which Manhattan District 2 high schools received an A grade for comprehensive performance in 2009-10?`
  - tasks_mini: `Which of <hop_2 answer> (match by DBN) also received 2009-2010 OVERALL GRADE 'A' in 2009-10? (Filter: DBN in hop_2; DBN starts with '02M'; SCHOOL LEVEL* == 'High School'; 2009-2010 OVERALL GRADE == 'A'.)`

- Node 3 `answer`
  - copy: `["02M047 - 47 The American Sign Language and English Secondary School", "02M288 - Food and Finance High School", "02M294 - Essex Street Academy", "02M296 - High School of Hospitality Management", "02M298 - Pace High School", "02M308 - Lower Manhattan Arts Academy", "02M408 - Professional Performing Arts High School", "02M411 - Baruch College Campus High Sch...`
  - tasks_mini: `["02M288 - Food and Finance High School", "02M294 - Essex Street Academy", "02M296 - High School of Hospitality Management", "02M298 - Pace High School", "02M408 - Professional Performing Arts High School", "02M411 - Baruch College Campus High School", "02M412 - N.Y.C. Lab School for Collaborative Studies", "02M413 - School of the Future High School", "02M4...`

- Node 3 `fact`

```diff
@@ -5,15 +5,19 @@
-source = "datagov/2009-2010-school-progress-report/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/2009-2010-school-progress-report/files/rows.txt'
```

- Node 4 `subquestion`
  - copy: `Which school from <hop 1 answer> is named after a relative of a U.S. president?`
  - tasks_mini: `Which District 02 Manhattan high schools from <intersection of hop_1, hop_2, hop_3> are named after U.S. First Ladies listed in the first-lady roster?`

- Node 4 `answer`
  - copy: `Eleanor Roosevelt High School`
  - tasks_mini: `["Eleanor Roosevelt High School"]`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Portrait of Eleanor RooseveltEleanor RooseveltMarch 4, 1933–April 12, 1945Franklin D. Roosevelt
+The list of first ladies includes Eleanor Roosevelt and Jacqueline "Jackie" Kennedy. Matching first-lady names to the District 02 Manhattan high schools from hops 1-3 yields Eleanor Roosevelt High School.
```

- Node 5 `subquestion`
  - copy: `Which U.S. Presidents were related to <hop 2 answer>'s namesake?`
  - tasks_mini: `Which U.S. Presidents were related to <hop_2 answer> namesake?`

- Node 5 `fact`

```diff
@@ -1,3 +1 @@
-Anna Eleanor Roosevelt ( ; October 11, 1884November 7, 1962) was an American political figure, diplomat, and activist. She was the longest-serving first lady of the United States, during her husband Franklin D. Roosevelt's four terms as president from 1933 to 1945. Through her travels, public engagement, and advocacy, she largely redefined the role. Widowed in 1945, she served as a United States delegate to the United Nations General Assembly from 1945 to 1952, and took a leading role in designing the text and gaining international support for the Universal Declaration of Human Rights. President Harry S. Truman called her the "First Lady of the World" in tribute to her human rights achievements.
-
-Roosevelt was a member of the prominent and wealthy Roosevelt and Livingston families and a niece of President Theodore Roosevelt. She had an unhappy childhood, having suffered the deaths of both parents and one of her brothers at a young age.
+Eleanor Roosevelt was related to two U.S. Presidents: Theodore Roosevelt (her uncle) and Franklin D. Roosevelt (her husband).
```

- Node 6 `subquestion`
  - copy: `From <hop 3 answer>, what years did Theodore Roosevelt serve as U.S. president?`
  - tasks_mini: `From <hop_3 answer>, what years did Theodore Roosevelt serve as U.S. president?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Theodore Roosevelt Jr. (October 27, 1858 – January 6, 1919), also known as Teddy or T.R., was the 26th president of the United States, serving from 1901 to 1909.
+Theodore Roosevelt was the 26th president of the United States, serving from 1901 to 1909.
```

- Node 7 `subquestion`
  - copy: `From <hop 3 answer>, what years did Franklin D. Roosevelt serve as U.S. president?`
  - tasks_mini: `From <hop_3 answer>, what years did Franklin D. Roosevelt serve as U.S. president?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Franklin Delano Roosevelt (January 30, 1882April 12, 1945), also known as FDR, was the 32nd president of the United States, serving from 1933 until his death in 1945.
+Franklin D. Roosevelt was the 32nd president of the United States, serving from 1933 until his death in 1945.
```

- Node 8 `subquestion`
  - copy: `What is the population in 2020 in the city where <hop 4 answer> died?`
  - tasks_mini: `What is the population in 2020 in the city where <hop_4 answer> died?`

- Node 8 `fact`

```diff
@@ -1,6 +1 @@
-
-History
-thumb|right|Warm Springs 1935
-thumb|right|Warm Springs 1933
-Warm Springs, originally named "Bullochville" (after the Bulloch family, which began after Stephen Bullock moved to Meriwether County in 1806 from Edgecombe County, North Carolina), first came to prominence in the 19th century as a spa town whose attraction was a permanent  natural spring. President Franklin D. Roosevelt first came to Warm Springs in 1924, hoping to find a cure for his polio. Although there was no cure, he did find that the warm water from the spring brought temporary relief, so he bought the resort and 1700 acres (6.9 km2) of land. It became a foundation for his charity, the Georgia Warm Springs Foundation, which later became the Roosevelt Warm Springs Institute for Rehabilitation, a rehabilitation hospital that continues today. Roosevelt learned to swim as a form of exercise to help him regain mobility. He became so fond of the place that he built a home on Pine Mountain nearby, which would become known as the Little White House. Roosevelt had a cottage built in 1932 that became famous as the Little White House, where he vacationed while president, because of his illness. H...
```

### `k-5-d-3/task_10.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Washington, DC wards were in the top 4 by number of building permits in 2022?`
  - tasks_mini: `Which Washington, DC wards were in the top 4 by number of building permits across 2022-2024? (Filter for this node: 2022 file; WARD not null; count permits by WARD; rank desc; take top 4.)`

- Node 1 `fact`

```diff
@@ -1,29 +1,20 @@
-import os
+import io
+import xml.etree.ElementTree as ET
+from collections import Counter
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 2 `subquestion`
  - copy: `Which Washington, DC wards were in the top 4 by number of building permits in 2023?`
  - tasks_mini: `Which Washington, DC wards were in the top 4 by number of building permits across 2022-2024? (Filter for this node: 2023 file; WARD not null; count permits by WARD; rank desc; take top 4.)`

- Node 2 `fact`

```diff
@@ -1,2 +1,2 @@
-import os
+import boto3
@@ -4,18 +4,19 @@
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/building-permits-in-2023/files/data.txt"
```

- Node 3 `subquestion`
  - copy: `Which Washington, DC wards were in the top 4 by number of building permits in 2024?`
  - tasks_mini: `Which Washington, DC wards were in the top 4 by number of building permits across 2022-2024? (Filter for this node: 2024 file; WARD not null; count permits by WARD; rank desc; take top 4.)`

- Node 3 `fact`

```diff
@@ -1,29 +1,20 @@
-import os
+import io
+import xml.etree.ElementTree as ET
+from collections import Counter
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 4 `subquestion`
  - copy: `For wards in <hop 1 answer>, what were the crime-incident counts in 2022?`
  - tasks_mini: `Among the wards (from hop 1), which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2022 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 4 `fact`

```diff
@@ -1,2 +1,2 @@
-import os
+import boto3
@@ -4,31 +4,18 @@
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/crime-incidents-in-2022/files/data.txt"
```

- Node 5 `subquestion`
  - copy: `For wards in <hop 1 answer>, what were the crime-incident counts in 2023?`
  - tasks_mini: `Among the wards (from hop 1), which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2023 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 5 `fact`

```diff
@@ -1,2 +1,2 @@
-import os
+import boto3
@@ -4,31 +4,18 @@
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/crime-incidents-in-2023/files/data.txt"
```

- Node 6 `subquestion`
  - copy: `For wards in <hop 1 answer>, what were the crime-incident counts in 2024?`
  - tasks_mini: `Among the wards (from hop 1), which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2024 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 6 `fact`

```diff
@@ -1,2 +1,2 @@
-import os
+import boto3
@@ -4,31 +4,18 @@
-import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/crime-incidents-in-2024/files/data.txt"
```

- Node 7 `subquestion`
  - copy: `For wards in <hop 2 answer>, what were the street-sweeping schedule entry counts in 2022?`
  - tasks_mini: `Among the wards (from hop 2), which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2022 file; WARD in {2,5}; count rows by WARD.)`

- Node 7 `fact`

```diff
@@ -1,49 +1,27 @@
-import os
-import io
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/street-sweeping-schedule-2022/files/data.txt"
```

- Node 8 `subquestion`
  - copy: `For wards in <hop 2 answer>, what were the street-sweeping schedule entry counts in 2023?`
  - tasks_mini: `Among the wards (from hop 2), which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2023 file; WARD in {2,5}; count rows by WARD.)`

- Node 8 `fact`

```diff
@@ -1,49 +1,27 @@
-import os
-import io
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/street-sweeping-schedule-2023/files/data.txt"
```

- Node 9 `subquestion`
  - copy: `For wards in <hop 2 answer>, what were the street-sweeping schedule entry counts in 2024?`
  - tasks_mini: `Among the wards (from hop 2), which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2024 file; WARD in {2,5}; count rows by WARD.)`

- Node 9 `fact`

```diff
@@ -1,49 +1,27 @@
-import os
-import io
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
-source = "datagov/street-sweeping-schedule-2024/files/data.txt"
```

### `k-5-d-3/task_11.json`
- Impact: major
- Node 1 `source`
  - copy: `datagov/building-permits-in-2022/v1/files/data.csv`
  - tasks_mini: `datagov/crime-incidents-in-2022/files/data.txt`

- Node 1 `subquestion`
  - copy: `What are the 2022 building-permit counts by ward in Washington, DC, so the top four wards for 2022 can be identified for the cross-year intersection?`
  - tasks_mini: `Among the wards 2, 4, 5, and 6, which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2022 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 1 `answer`
  - copy: `{"Ward 2": 8286, "Ward 4": 6971, "Ward 5": 6580, "Ward 6": 8371}`
  - tasks_mini: `{"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685}`

- Node 1 `fact`

```diff
@@ -1 +1,21 @@
-answer not derivable
+import boto3
+import io
+import json
+import pandas as pd
+from botocore import UNSIGNED
```

- Node 2 `source`
  - copy: `datagov/building-permits-in-2023/v1/files/data.csv`
  - tasks_mini: `datagov/crime-incidents-in-2023/files/data.txt`

- Node 2 `subquestion`
  - copy: `What are the 2023 building-permit counts by ward in Washington, DC, so the top four wards for 2023 can be identified for the cross-year intersection?`
  - tasks_mini: `Among the wards 2, 4, 5, and 6, which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2023 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 2 `answer`
  - copy: `{"Ward 2": 8392, "Ward 4": 6525, "Ward 5": 6072, "Ward 6": 6845}`
  - tasks_mini: `{"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281}`

- Node 2 `fact`

```diff
@@ -1 +1,21 @@
-answer not derivable
+import boto3
+import io
+import json
+import pandas as pd
+from botocore import UNSIGNED
```

- Node 3 `source`
  - copy: `datagov/building-permits-in-2024/v1/files/data.csv`
  - tasks_mini: `datagov/crime-incidents-in-2024/files/data.txt`

- Node 3 `subquestion`
  - copy: `What are the 2024 building-permit counts by ward in Washington, DC, so the top four wards for 2024 can be identified for the cross-year intersection?`
  - tasks_mini: `Among the wards 2, 4, 5, and 6, which two had the highest average crime-incident counts across 2022-2024? (Filter for this node: 2024 file; WARD in {2,4,5,6}; count incidents by WARD.)`

- Node 3 `answer`
  - copy: `{"Ward 2": 7897, "Ward 4": 6856, "Ward 5": 6213, "Ward 6": 6658}`
  - tasks_mini: `{"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549}`

- Node 3 `fact`

```diff
@@ -1 +1,21 @@
-answer not derivable
+import boto3
+import io
+import json
+import pandas as pd
+from botocore import UNSIGNED
```

- Node 4 `source`
  - copy: `datagov/crime-incidents-in-2022/v1/files/data.csv`
  - tasks_mini: `datagov/street-sweeping-schedule-2022/files/data.txt`

- Node 4 `subquestion`
  - copy: `What are the 2022 crime-incident counts for each of Wards 2, 4, 5, and 6, so their average incident counts across 2022-2024 can be compared?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2022 file; WARD in {2,5}; count rows by WARD.)`

- Node 4 `answer`
  - copy: `{"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685}`
  - tasks_mini: `{"Ward 2": 72, "Ward 5": 80}`

- Node 4 `fact`

```diff
@@ -1 +1,27 @@
-answer not derivable
+import json
+import boto3
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 5 `source`
  - copy: `datagov/crime-incidents-in-2023/v1/files/data.csv`
  - tasks_mini: `datagov/street-sweeping-schedule-2023/files/data.txt`

- Node 5 `subquestion`
  - copy: `What are the 2023 crime-incident counts for each of Wards 2, 4, 5, and 6, so their average incident counts across 2022-2024 can be compared?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2023 file; WARD in {2,5}; count rows by WARD.)`

- Node 5 `answer`
  - copy: `{"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281}`
  - tasks_mini: `{"Ward 2": 54, "Ward 5": 83}`

- Node 5 `fact`

```diff
@@ -1 +1,27 @@
-answer not derivable
+import json
+import boto3
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 6 `source`
  - copy: `datagov/crime-incidents-in-2024/v1/files/data.csv`
  - tasks_mini: `datagov/street-sweeping-schedule-2024/files/data.txt`

- Node 6 `subquestion`
  - copy: `What are the 2024 crime-incident counts for each of Wards 2, 4, 5, and 6, so their average incident counts across 2022-2024 can be compared?`
  - tasks_mini: `Among the wards 2 and 5, which ward had the higher average number of street-sweeping schedule entries across 2022-2024? (Filter for this node: 2024 file; WARD in {2,5}; count rows by WARD.)`

- Node 6 `answer`
  - copy: `{"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549}`
  - tasks_mini: `{"Ward 2": 54, "Ward 5": 87}`

- Node 6 `fact`

```diff
@@ -1 +1,27 @@
-answer not derivable
+import json
+import boto3
+import pandas as pd
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 7 `source`
  - copy: `datagov/street-sweeping-schedule-2022/v1/files/data.csv`
  - tasks_mini: `datagov/dc-charter-schools/files/data.txt`

- Node 7 `subquestion`
  - copy: `What are the 2022 street-sweeping schedule entry counts for Wards 2 and 5, so their average counts across 2022-2024 can be compared?`
  - tasks_mini: `Which charter school in the ward (from hop 2) spans grade 8 and grade 9? (Filter for this node: WARD == 5; GRADES include 8 and 9 in the range.)`

- Node 7 `answer`
  - copy: `{"Ward 2": 72, "Ward 5": 80}`
  - tasks_mini: `Sojourner Truth PCS`

- Node 7 `fact`

```diff
@@ -1 +1,49 @@
-answer not derivable
+import boto3
+import io
+import json
+import pandas as pd
+from botocore import UNSIGNED
```

- Node 8 `source`
  - copy: `datagov/street-sweeping-schedule-2023/v1/files/data.csv`
  - tasks_mini: `wikipedia/Sojourner_Truth/content.txt`

- Node 8 `subquestion`
  - copy: `What are the 2023 street-sweeping schedule entry counts for Wards 2 and 5, so their average counts across 2022-2024 can be compared?`
  - tasks_mini: `The charter school identified (from hop 3) includes the name 'Sojourner Truth'. According to her biography, where was she born?`

- Node 8 `answer`
  - copy: `{"Ward 2": 54, "Ward 5": 83}`
  - tasks_mini: `Swartekill, New York`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-answer not derivable
+Sojourner Truth was born into slavery in Swartekill, New York.
```

- Node 9 `source`
  - copy: `datagov/street-sweeping-schedule-2024/v1/files/data.csv`
  - tasks_mini: `wikipedia/Rifton,_New_York/content.txt`

- Node 9 `subquestion`
  - copy: `What are the 2024 street-sweeping schedule entry counts for Wards 2 and 5, so their average counts across 2022-2024 can be compared?`
  - tasks_mini: `Swartekill, New York (from hop 4) is described in the Rifton, New York article; what county is Rifton in?`

- Node 9 `answer`
  - copy: `{"Ward 2": 54, "Ward 5": 87}`
  - tasks_mini: `Ulster County, New York`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-answer not derivable
+Rifton is a hamlet (and census-designated place) in Ulster County, New York, and Swartekill was one of the hamlets encompassed in Rifton's former village.
```

### `k-5-d-3/task_12.json`
- Impact: major
- Node 1 `source`
  - copy: `wikipedia/List_of_colleges_and_universities_in_Washington_(state)/content.txt`
  - tasks_mini: `datagov/agency-contracts-fiscal-year-2014/files/rows.txt`

- Node 1 `subquestion`
  - copy: `According to the list of colleges and universities in Washington state, which public four-year universities are in Washington?`
  - tasks_mini: `How many contracts did Seattle Community College - District 6 (SCCD-6), Green River Community College (GRC), and Spokane, Community Colleges of SCCD-17 have in FY 2014?`

- Node 1 `answer`
  - copy: `["University of Washington", "Washington State University", "Western Washington University", "Eastern Washington University", "Central Washington University", "Evergreen State College"]`
  - tasks_mini: `Seattle Community College - District 6: 1,308; Green River Community College: 1,723; Community Colleges of Spokane: 1,797`

- Node 1 `fact`

```diff
@@ -1 +1,15 @@
-The Wikipedia list of colleges and universities in Washington state lists the public four-year universities as University of Washington, Washington State University, Western Washington University, Eastern Washington University, Central Washington University, and Evergreen State College.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 2 `source`
  - copy: `datagov/agency-contracts-fiscal-year-2014/files/rows.txt`
  - tasks_mini: `datagov/agency-contracts-fiscal-year-2015/files/rows.txt`

- Node 2 `subquestion`
  - copy: `What were the FY 2014 contract counts for the Washington public four-year universities from <hop 1 answer>?`
  - tasks_mini: `How many contracts did Seattle Colleges, Green River Community College (GRC), and Spokane, Community Colleges of SCCD-17 have in FY 2015?`

- Node 2 `answer`
  - copy: `{"Central Washington University": 223, "Eastern Washington University": 840, "Evergreen State College": 275, "University of Washington": 3679, "Washington State University": 484, "Western Washington University": 799}`
  - tasks_mini: `Seattle Colleges: 1,292; Green River Community College: 633; Community Colleges of Spokane: 383`

- Node 2 `limit`
  - copy: `6`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,27 +6,10 @@
-source = "datagov/agency-contracts-fiscal-year-2014/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/agency-contracts-fiscal-year-2015/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `source`
  - copy: `datagov/agency-contracts-fiscal-year-2015/files/rows.txt`
  - tasks_mini: `datagov/agency-contracts-fiscal-year-2016/files/rows.txt`

- Node 3 `subquestion`
  - copy: `What were the FY 2015 contract counts for the Washington public four-year universities from <hop 1 answer>?`
  - tasks_mini: `How many contracts did Seattle Community College - District 6 (SCCD-6), Green River Community College (GRC), and Spokane, Community Colleges of SCCD-17 have in FY 2016?`

- Node 3 `answer`
  - copy: `{"Central Washington University": 274, "Eastern Washington University": 600, "Evergreen State College": 231, "University of Washington": 212, "Washington State University": 498, "Western Washington University": 605}`
  - tasks_mini: `Seattle Community College - District 6: 5,244; Green River Community College: 872; Community Colleges of Spokane: 265`

- Node 3 `limit`
  - copy: `6`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -6,27 +6,10 @@
-source = "datagov/agency-contracts-fiscal-year-2015/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/agency-contracts-fiscal-year-2016/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 4 `source`
  - copy: `datagov/agency-contracts-fiscal-year-2016/files/rows.txt`
  - tasks_mini: `wikipedia/Seattle_Colleges_District/content.txt`

- Node 4 `subquestion`
  - copy: `What were the FY 2016 contract counts for the Washington public four-year universities from <hop 1 answer>?`
  - tasks_mini: `Where is Seattle Colleges District (the #1 community college by average contracts from nodes 1-3) located?`

- Node 4 `answer`
  - copy: `{"Central Washington University": 362, "Eastern Washington University": 505, "Evergreen State College": 207, "University of Washington": 23, "Washington State University": 466, "Western Washington University": 132}`
  - tasks_mini: `Seattle Colleges is located in Seattle, Washington`

- Node 4 `limit`
  - copy: `6`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1,32 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-
```

- Node 5 `source`
  - copy: `wikipedia/University_of_Washington/content.txt`
  - tasks_mini: `wikipedia/Green_River_College/content.txt`

- Node 5 `subquestion`
  - copy: `Where is the #1 public four-year university by average contracts from <hop 2 answer> located?`
  - tasks_mini: `Where is Green River College (the #2 community college by average contracts from nodes 1-3) located?`

- Node 5 `answer`
  - copy: `University of Washington is located in Seattle, Washington`
  - tasks_mini: `Green River College is located in Auburn, Washington`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-The University of Washington is a public research university in Seattle, Washington, United States.
+Green River College is a public community college in Auburn, Washington, United States.
```

- Node 6 `source`
  - copy: `wikipedia/Eastern_Washington_University/content.txt`
  - tasks_mini: `wikipedia/Community_Colleges_of_Spokane/content.txt`

- Node 6 `subquestion`
  - copy: `Where is the #2 public four-year university by average contracts from <hop 2 answer> located?`
  - tasks_mini: `Where is Community Colleges of Spokane (the #3 community college by average contracts from nodes 1-3) located?`

- Node 6 `answer`
  - copy: `Eastern Washington University is located in Cheney, Washington`
  - tasks_mini: `Community Colleges of Spokane is located in Spokane, Washington`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Eastern Washington University is a public university in Cheney, Washington, United States.
+Community Colleges of Spokane is a community college district based in Spokane, Washington.
```

- Node 7 `subquestion`
  - copy: `What is the 2020 census population and county seat of the county in <hop 3 answer> that contains Seattle?`
  - tasks_mini: `What is the 2020 census population and county seat of King County, Washington (containing Seattle and Auburn from nodes 4-5)?`

- Node 8 `subquestion`
  - copy: `What is the 2020 census population and county seat of the county in <hop 3 answer> that contains Cheney?`
  - tasks_mini: `What is the 2020 census population and county seat of Spokane County, Washington (containing Spokane from node 6)?`

- Node 9 `subquestion`
  - copy: `Which Seattle building, the county seat of the more populous county from <hop 4 answer>, has the highest average TotalGHGEmissions from 2015 to 2023?`
  - tasks_mini: `Which Seattle building (from nodes 7-8: the county seat of the most populous county) has the highest average TotalGHGEmissions from 2015 to 2023? (Filter DataYear between 2015 and 2023 inclusive; group by BuildingName; average TotalGHGEmissions.)`

- Node 9 `answer`
  - copy: `[{"BuildingName": "BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus", "avg_TotalGHGEmissions": 20835.775}]`
  - tasks_mini: `BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus with 20,835.8 metric tons CO2e average`

- Node 9 `limit`
  - copy: `1`
  - tasks_mini: ``

- Node 9 `fact`

```diff
@@ -6,24 +6,23 @@
-source = "datagov/building-energy-benchmarking-data-2015-present/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/building-energy-benchmarking-data-2015-present/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 10 `subquestion`
  - copy: `In what year was <hop 5 answer> built?`
  - tasks_mini: `In what year was Boeing Plant 2 (the Boeing Plant 2 ISAL (BLDG 2-122)-North Boeing Field Campus from node 9) built?`

### `k-5-d-3/task_13.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `<hop 1 answer> is a city in which county?`
  - tasks_mini: `<node_1 answer> is a city in which county?`

- Node 3 `subquestion`
  - copy: `In the school district office listings, entries with CITY='<hop 1 answer>' and NMCNTY='<hop 2 answer>' share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='<node_1 answer>' and NMCNTY='<node_2 answer>' share what two-digit state FIPS code (STFIP)?`

- Node 3 `fact`

```diff
@@ -1,2 +1,4 @@
+import io
+import pandas as pd
@@ -5,17 +7,10 @@
-source = "datagov/school-district-office-locations-current-d848f/files/nces::school-district-office-locations-current-1.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
```

- Node 4 `subquestion`
  - copy: `For STFIP='06', what are the public school counts by county, and which three counties have the highest counts?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 4 `answer`
  - copy: `["Los Angeles County", "San Diego County", "Orange County"]`
  - tasks_mini: `Los Angeles County; San Diego County; Orange County`

- Node 4 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -7,19 +7,13 @@
-source = "datagov/public-school-locations-current-23297/files/data-oyCYxF.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
-df.columns = [col.replace("properties.", "") for col in df.columns]
```

- Node 5 `subquestion`
  - copy: `For STFIP='06', what are the private school counts for each county, and which three counties have the highest counts?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 5 `answer`
  - copy: `["Los Angeles County", "Orange County", "San Diego County"]`
  - tasks_mini: `Los Angeles County; Orange County; San Diego County`

- Node 5 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -7,19 +7,13 @@
-source = "datagov/private-school-locations-current-f7d96/files/data-FGgJBu.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
-df.columns = [col.replace("properties.", "") for col in df.columns]
```

- Node 6 `subquestion`
  - copy: `For STFIP='06', what are the school district office counts for each county, and which three counties have the highest counts?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 6 `answer`
  - copy: `["Los Angeles County", "San Diego County", "San Bernardino County"]`
  - tasks_mini: `Los Angeles County; San Diego County; San Bernardino County`

- Node 6 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 6 `fact`

```diff
@@ -7,19 +7,13 @@
-source = "datagov/school-district-office-locations-2022-23/files/data-8V0eVK.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
-df.columns = [col.replace("properties.", "") for col in df.columns]
```

- Node 7 `subquestion`
  - copy: `For STFIP='06', what are the postsecondary institution counts for each county in the intersection of the top-three public-school counties, top-three private-school counties, and top-three school-district-office counties?`
  - tasks_mini: `Let A be the set of counties in <node_4 answer>, B be the set of counties in <node_5 answer>, and C be the set of counties in <node_6 answer>. Consider the intersection of A, B, and C. Among those counties, what is the smaller postsecondary institution count in STFIP='<node_3 answer>'? Answer with the number only.`

- Node 7 `answer`
  - copy: `71`
  - tasks_mini: `71`

- Node 7 `fact`

```diff
@@ -7,38 +7,13 @@
-source = "datagov/postsecondary-school-locations-2022-23/files/data-sh56Ar.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
-df.columns = [col.replace("properties.", "") for col in df.columns]
```

### `k-5-d-3/task_14.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `<hop 1 answer> is located in which county?`
  - tasks_mini: `<node_1 answer> is located in which county?`

- Node 3 `subquestion`
  - copy: `In the school district office listings, entries with CITY='<hop 1 answer>' and NMCNTY='<hop 2 answer>' share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='<node_1 answer>' and NMCNTY='<node_2 answer>' share what two-digit state FIPS code (STFIP)?`

- Node 3 `fact`

```diff
@@ -1,2 +1,4 @@
+import io
+import pandas as pd
@@ -5,17 +7,10 @@
-source = "datagov/school-district-office-locations-current-d848f/files/nces::school-district-office-locations-current-1.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
```

- Node 4 `subquestion`
  - copy: `For STFIP='<hop 3 answer>', which 3 county names have the most public schools?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 4 `answer`
  - copy: `["Polk County", "Linn County", "Scott County"]`
  - tasks_mini: `Polk County; Linn County; Scott County`

- Node 4 `fact`

```diff
@@ -1 +1,2 @@
+import io
@@ -6,18 +7,13 @@
-source = "datagov/public-school-locations-2018-19-42360/files/data-F2nGlG.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
```

- Node 5 `subquestion`
  - copy: `For STFIP='<hop 3 answer>', which 3 county names have the most private schools?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 5 `answer`
  - copy: `["Polk County", "Linn County", "Sioux County"]`
  - tasks_mini: `Polk County; Linn County; Sioux County`

- Node 5 `fact`

```diff
@@ -1 +1,2 @@
+import io
@@ -6,18 +7,13 @@
-source = "datagov/private-school-locations-2017-18-f49f6/files/data-dqdQDP.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
```

- Node 6 `subquestion`
  - copy: `For STFIP='<hop 3 answer>', which 3 county names have the most school district offices?`
  - tasks_mini: `For STFIP='<node_3 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 6 `answer`
  - copy: `["Linn County", "Polk County", "Pottawattamie County"]`
  - tasks_mini: `Linn County; Polk County; Pottawattamie County`

- Node 6 `fact`

```diff
@@ -1 +1,2 @@
+import io
@@ -6,18 +7,13 @@
-source = "datagov/school-district-office-locations-2020-21-d8df0/files/data-UDaCeM.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
```

- Node 7 `subquestion`
  - copy: `For STFIP='<hop 3 answer>', what is the smaller postsecondary institution count among the counties in <hop 4 answer>?`
  - tasks_mini: `Let A be the set of counties in <node_4 answer>, B be the set of counties in <node_5 answer>, and C be the set of counties in <node_6 answer>. Consider the intersection of C with the union of A and B. Among those counties, what is the smaller postsecondary institution count in STFIP='<node_3 answer>'? Answer with the number only.`

- Node 7 `answer`
  - copy: `7`
  - tasks_mini: `7`

- Node 7 `fact`

```diff
@@ -1 +1,2 @@
+import io
@@ -6,24 +7,13 @@
-source = "datagov/postsecondary-school-locations-2019-20-64b31/files/data-cbxYz6.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-payload = json.loads(obj["Body"].read())
-df = pd.json_normalize(payload["features"])
```

### `k-5-d-3/task_15.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Missouri state agencies had the highest average employee salary in 2018?`
  - tasks_mini: `Which Missouri state agencies had the highest average employee pay in 2018?`

- Node 1 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -6,12 +6,9 @@
-source = "datagov/2018-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2018-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 2 `subquestion`
  - copy: `Which Missouri state agencies had the highest average employee salary in 2019?`
  - tasks_mini: `Which of <node_1 answer> remained in the top 5 by average employee pay in 2019?`

- Node 2 `answer`
  - copy: `["OFFICE OF GOVERNOR", "OFFICE OF ATTORNEY GENERAL", "JUDICIARY", "OFFICE OF STATE AUDITOR", "OFFICE OF ADMINISTRATION"]`
  - tasks_mini: `["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR", "OFFICE OF ADMINISTRATION"]`

- Node 2 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,12 +6,10 @@
-source = "datagov/2019-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2019-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `subquestion`
  - copy: `Which Missouri state agencies had the highest average employee salary in 2020?`
  - tasks_mini: `Which of <node_2 answer> remained in the top 5 by average employee pay in 2020?`

- Node 3 `answer`
  - copy: `["OFFICE OF STATE AUDITOR", "OFFICE OF GOVERNOR", "OFFICE OF LIEUTENANT GOVERNOR", "OFFICE OF ATTORNEY GENERAL", "JUDICIARY"]`
  - tasks_mini: `["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR"]`

- Node 3 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -6,12 +6,10 @@
-source = "datagov/2020-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2020-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 6 `subquestion`
  - copy: `Which office in <hop 1 answer> had <node 5 answer> as its first officeholder and thus matches the U.S. Attorney General condition?`
  - tasks_mini: `Which office in <node_3 answer> has a first officeholder who served as U.S. Attorney General? (Use <node_4 answer> and <node_5 answer> for first officeholders.)`

- Node 7 `subquestion`
  - copy: `From the <hop 2 answer> notable list, which Missouri Attorney General is listed as both a U.S. Attorney General and a U.S. Senator?`
  - tasks_mini: `From the <node_6 answer> notable list, which Missouri Attorney General is listed as both a U.S. Attorney General and a U.S. Senator?`

- Node 8 `subquestion`
  - copy: `Where was <hop 3 answer> born?`
  - tasks_mini: `Where was <node_7 answer> born?`

- Node 9 `subquestion`
  - copy: `What was the 2018 population of <hop 4 answer>?`
  - tasks_mini: `What was the 2018 citywide population of <node_8 answer>?`

- Node 9 `answer`
  - copy: `2705988`
  - tasks_mini: `2705988`

- Node 9 `fact`

```diff
@@ -6,12 +6,8 @@
-source = "datagov/chicago-population-counts/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/chicago-population-counts/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

### `k-5-d-3/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What was the total state-government spending by Texas county in 2018?`
  - tasks_mini: `What were the total state expenditures in 2018 for Travis, Harris, and Dallas counties? (Filter County in {TRAVIS, HARRIS, DALLAS}; exclude County == 'INTEX' or null; group by County; sum Amount.)`

- Node 1 `answer`
  - copy: `{"BEXAR": 14728288130.02, "DALLAS": 21393532327.19, "EL PASO": 5336100417.92, "FORT BEND": 6492630042.559999, "HARRIS": 28158070491.58, "HIDALGO": 6972525635.8, "NUECES": 3565913161.02, "TARRANT": 9271248309.9, "TRAVIS": 29374677347.44, "WILLIAMSON": 3183082660.11}`
  - tasks_mini: `Travis: $29.37B; Harris: $28.16B; Dallas: $21.39B`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -6,17 +6,12 @@
-source = "datagov/texas-state-expenditures-by-county-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-state-expenditures-by-county-2018/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 2 `subquestion`
  - copy: `What was the total state-government spending by Texas county in 2019?`
  - tasks_mini: `What were the total state expenditures in 2019 for Travis, Harris, and Dallas counties? (Filter County in {TRAVIS, HARRIS, DALLAS}; exclude County == 'INTEX' or null; group by County; sum Amount.)`

- Node 2 `answer`
  - copy: `{"BEXAR": 7513472495.969999, "DALLAS": 10578598198.67, "EL PASO": 2697075449.58, "FORT BEND": 3170751219.59, "HARRIS": 14986103849.57, "HIDALGO": 3806412724.5899997, "NUECES": 1908938199.46, "TARRANT": 4521857907.47, "TRAVIS": 16338507938.35, "WILLIAMSON": 1731549869.92}`
  - tasks_mini: `Travis: $16.34B; Harris: $14.99B; Dallas: $10.58B`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,17 +6,12 @@
-source = "datagov/texas-state-expenditures-by-county-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-state-expenditures-by-county-2019/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `subquestion`
  - copy: `What was the total state-government spending by Texas county in 2020?`
  - tasks_mini: `What were the total state expenditures in 2020 for Travis, Harris, and Dallas counties? (Filter County in {TRAVIS, HARRIS, DALLAS}; exclude County == 'INTEX' or null; group by County; sum Amount.)`

- Node 3 `answer`
  - copy: `{"BEXAR": 8839835949.14, "DALLAS": 12496129391.79, "EL PASO": 3075321686.73, "FORT BEND": 3451437618.41, "HARRIS": 16453460156.29, "HIDALGO": 4146048814.13, "NUECES": 2219759682.6899996, "TARRANT": 5064124303.04, "TRAVIS": 16762053530.27, "WILLIAMSON": 2122362176.09}`
  - tasks_mini: `Travis: $16.76B; Harris: $16.45B; Dallas: $12.50B`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -6,17 +6,12 @@
-source = "datagov/texas-state-expenditures-by-county-2020/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-state-expenditures-by-county-2020/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 4 `subquestion`
  - copy: `What is the county seat of Travis County?`
  - tasks_mini: `What is the county seat of each of the top 3 counties (from hop 1)?`

- Node 5 `subquestion`
  - copy: `What is the county seat of Harris County?`
  - tasks_mini: `What is the county seat of each of the top 3 counties (from hop 1)?`

- Node 6 `subquestion`
  - copy: `What is the county seat of Dallas County?`
  - tasks_mini: `What is the county seat of each of the top 3 counties (from hop 1)?`

- Node 7 `subquestion`
  - copy: `When was Austin incorporated?`
  - tasks_mini: `When was each county seat (from hop 2) incorporated?`

- Node 8 `subquestion`
  - copy: `When was Houston incorporated?`
  - tasks_mini: `When was each county seat (from hop 2) incorporated?`

- Node 9 `subquestion`
  - copy: `When was Dallas incorporated?`
  - tasks_mini: `When was each county seat (from hop 2) incorporated?`

- Node 10 `subquestion`
  - copy: `For <hop 3 answer> in 2018-2019, what is the average percentage across each district's sites of students automatically recognized as eligible for free school meals without submitting a household meal application?`
  - tasks_mini: `For Harris County in 2018-2019, what is the average SiteISP for each ISD? (Filter SiteCounty == 'HARRIS'; filter CEName contains 'ISD'; group by CEName; average SiteISP.)`

- Node 10 `answer`
  - copy: `{"ALDINE ISD": 67.1557142857143, "ALIEF ISD": 64.05813953488372, "CHANNELVIEW ISD": 59.62384615384615, "GALENA PARK ISD": 62.07434782608696, "GOOSE CREEK CISD": 56.779999999999994, "HOUSTON ISD": 67.64794964028778, "PASADENA ISD": 66.74057971014493, "SHELDON ISD": 81.465, "SPRING BRANCH ISD": 49.11022727272727, "SPRING ISD": 59.761842105263156}`
  - tasks_mini: `Sheldon ISD: 81.47% average ISP`

- Node 10 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 10 `fact`

```diff
@@ -6,17 +6,10 @@
-source = "datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2018/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 11 `subquestion`
  - copy: `For <hop 3 answer> in 2019-2020, what is the average percentage across each district's sites of students automatically recognized as eligible for free school meals without submitting a household meal application?`
  - tasks_mini: `For Harris County in 2019-2020, what is the average SiteISP for each ISD? (Filter SiteCounty == 'HARRIS'; filter CEName contains 'ISD'; group by CEName; average SiteISP.)`

- Node 11 `answer`
  - copy: `{"ALDINE ISD": 66.54481481481481, "ALIEF ISD": 65.68209302325582, "CHANNELVIEW ISD": 59.41076923076923, "GALENA PARK ISD": 58.66375, "GOOSE CREEK CISD": 50.4475, "HOUSTON ISD": 60.60494699646643, "PASADENA ISD": 60.71072463768116, "SHELDON ISD": 60.66363636363636, "SPRING BRANCH ISD": 49.97113636363636, "SPRING ISD": 57.32684210526316}`
  - tasks_mini: `Sheldon ISD: 60.66% average ISP`

- Node 11 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 11 `fact`

```diff
@@ -6,17 +6,10 @@
-source = "datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2019/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 12 `subquestion`
  - copy: `For <hop 3 answer> in 2020-2021, what is the average percentage across each district's sites of students automatically recognized as eligible for free school meals without submitting a household meal application?`
  - tasks_mini: `For Harris County in 2020-2021, what is the average SiteISP for each ISD? (Filter SiteCounty == 'HARRIS'; filter CEName contains 'ISD'; group by CEName; average SiteISP.)`

- Node 12 `answer`
  - copy: `{"ALDINE ISD": 65.33134146341463, "ALIEF ISD": 63.437441860465114, "CHANNELVIEW ISD": 64.9, "GALENA PARK ISD": 60.13083333333333, "GOOSE CREEK CISD": 51.05785714285714, "HOUSTON ISD": 62.95017543859649, "PASADENA ISD": 60.05231884057971, "SHELDON ISD": 66.11, "SPRING BRANCH ISD": 51.434090909090905, "SPRING ISD": 58.710249999999995}`
  - tasks_mini: `Sheldon ISD: 66.11% average ISP`

- Node 12 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 12 `fact`

```diff
@@ -6,17 +6,10 @@
-source = "datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2020/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2020/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 13 `subquestion`
  - copy: `In what year did <hop 4 answer> become an independent school district?`
  - tasks_mini: `In what year did the ISD with highest average ISP (from hop 4) become an independent school district?`

### `k-5-d-3/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which counties were in the statewide top 5 for releases from the Texas state prison system in 2019?`
  - tasks_mini: `How many TDCJ releases did Harris, Dallas, and Tarrant counties have in FY 2019? (Filter County in {Harris, Dallas, Tarrant}; count rows.)`

- Node 1 `answer`
  - copy: `["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"]`
  - tasks_mini: `Harris: 9,029; Dallas: 5,355; Tarrant: 4,769`

- Node 1 `fact`

```diff
@@ -6,13 +6,9 @@
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-department-of-criminal-justice-releases-fy-2019/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 2 `subquestion`
  - copy: `Which counties were in the statewide top 5 for releases from the Texas state prison system in 2020?`
  - tasks_mini: `How many TDCJ releases did Harris, Dallas, and Tarrant counties have in FY 2020? (Filter County in {Harris, Dallas, Tarrant}; count rows.)`

- Node 2 `answer`
  - copy: `["Harris", "Dallas", "Tarrant", "Bexar", "Travis"]`
  - tasks_mini: `Harris: 7,059; Dallas: 4,540; Tarrant: 4,450`

- Node 2 `fact`

```diff
@@ -6,13 +6,9 @@
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2020/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-department-of-criminal-justice-releases-fy-2020/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `subquestion`
  - copy: `Which counties were in the statewide top 5 for releases from the Texas state prison system in 2021?`
  - tasks_mini: `How many TDCJ releases did Harris, Dallas, and Tarrant counties have in FY 2021? (Filter County in {Harris, Dallas, Tarrant}; count rows.)`

- Node 3 `answer`
  - copy: `["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"]`
  - tasks_mini: `Harris: 5,210; Dallas: 3,565; Tarrant: 3,252`

- Node 3 `fact`

```diff
@@ -6,13 +6,9 @@
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2021/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/texas-department-of-criminal-justice-releases-fy-2021/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 4 `subquestion`
  - copy: `What is the county seat of Harris County, Texas?`
  - tasks_mini: `What is the county seat of Harris County, Texas (the #1 county by average TDCJ releases from nodes 1-3)?`

- Node 5 `subquestion`
  - copy: `What is the county seat of Dallas County, Texas?`
  - tasks_mini: `What is the county seat of Dallas County, Texas (the #2 county by average TDCJ releases from nodes 1-3)?`

- Node 6 `subquestion`
  - copy: `What is the county seat of Tarrant County, Texas?`
  - tasks_mini: `What is the county seat of Tarrant County, Texas (the #3 county by average TDCJ releases from nodes 1-3)?`

- Node 7 `source`
  - copy: `wikipedia/Bexar_County,_Texas/content.txt`
  - tasks_mini: `wikipedia/Houston/content.txt`

- Node 7 `subquestion`
  - copy: `What is the county seat of Bexar County, Texas?`
  - tasks_mini: `When was Houston (county seat of Harris County from node 4) founded/established?`

- Node 7 `answer`
  - copy: `San Antonio is the county seat of Bexar County`
  - tasks_mini: `Houston was founded on August 30, 1836`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Bexar County is a county in the U.S. state of Texas. The county seat is San Antonio.
+Houston was founded by land investors on August 30, 1836, at the confluence of Buffalo Bayou and White Oak Bayou.
```

- Node 8 `source`
  - copy: `wikipedia/Houston/content.txt`
  - tasks_mini: `wikipedia/Dallas/content.txt`

- Node 8 `subquestion`
  - copy: `When was Houston founded?`
  - tasks_mini: `When was Dallas (county seat of Dallas County from node 5) established?`

- Node 8 `answer`
  - copy: `Houston was founded on August 30, 1836`
  - tasks_mini: `Dallas was established in 1841`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Houston was founded by land investors on August 30, 1836, at the confluence of Buffalo Bayou and White Oak Bayou.
+In 1841, John Neely Bryan established a permanent settlement named Dallas.
```

- Node 9 `source`
  - copy: `wikipedia/Dallas/content.txt`
  - tasks_mini: `wikipedia/Fort_Worth,_Texas/content.txt`

- Node 9 `subquestion`
  - copy: `When was Dallas established?`
  - tasks_mini: `When was Fort Worth (county seat of Tarrant County from node 6) established?`

- Node 9 `answer`
  - copy: `Dallas was established in 1841`
  - tasks_mini: `Fort Worth was established in 1849`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-In 1841, John Neely Bryan established a permanent settlement named Dallas.
+The city of Fort Worth was established in 1849 as an army outpost on a bluff overlooking the Trinity River.
```

- Node 10 `source`
  - copy: `wikipedia/Fort_Worth,_Texas/content.txt`
  - tasks_mini: `datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2019/files/rows.txt`

- Node 10 `subquestion`
  - copy: `When was Fort Worth established?`
  - tasks_mini: `Which ISD had the highest average ISP in Tarrant County (from nodes 7-9: the county with the newest county seat) in the 2019-2020 program year? (Filter SiteCounty == 'TARRANT'; filter CEName contains 'ISD'; group by CEName; average SiteISP.)`

- Node 10 `answer`
  - copy: `Fort Worth was established in 1849`
  - tasks_mini: `Lake Worth ISD: 65.00% average ISP`

- Node 10 `fact`

```diff
@@ -1 +1,20 @@
-The city of Fort Worth was established in 1849 as an army outpost on a bluff overlooking the Trinity River.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 11 `source`
  - copy: `wikipedia/San_Antonio/content.txt`
  - tasks_mini: `datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2020/files/rows.txt`

- Node 11 `subquestion`
  - copy: `When was San Antonio established?`
  - tasks_mini: `What was the average ISP for Lake Worth ISD in Tarrant County in the 2020-2021 program year? (Filter SiteCounty == 'TARRANT'; filter CEName == 'LAKE WORTH ISD'; average SiteISP.)`

- Node 11 `answer`
  - copy: `San Antonio was established in 1718`
  - tasks_mini: `Lake Worth ISD: 65.94% average ISP`

- Node 11 `fact`

```diff
@@ -1 +1,15 @@
-A Spanish expedition from Mexico founded the municipality and presidio of San Antonio in 1718.
+import io
+import pandas as pd
+import boto3
+from botocore import UNSIGNED
+from botocore.config import Config
```

- Node 12 `source`
  - copy: `datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2019/files/rows.txt`
  - tasks_mini: `datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2021/files/rows.txt`

- Node 12 `subquestion`
  - copy: `For <hop 3 answer> in 2019-2020, what is the average percentage across each district's sites of students automatically recognized as eligible for free school meals without submitting a household meal application?`
  - tasks_mini: `What was the average ISP for Lake Worth ISD in Tarrant County in the 2021-2022 program year? (Filter SiteCounty == 'TARRANT'; filter CEName == 'LAKE WORTH ISD'; average SiteISP.)`

- Node 12 `answer`
  - copy: `{"ARLINGTON ISD": 52.73, "AZLE ISD": 40.83, "BIRDVILLE ISD": 46.24, "CASTLEBERRY ISD": 55.89, "CROWLEY ISD": 49.63, "EVERMAN ISD": 40.87, "FORT WORTH ISD": 59.0, "HURST-EULESS-BEDFORD ISD": 40.21, "LAKE WORTH ISD": 65.0, "WHITE SETTLEMENT ISD": 43.16}`
  - tasks_mini: `Lake Worth ISD: 71.65% average ISP`

- Node 12 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 12 `fact`

```diff
@@ -5,16 +5,11 @@
-source = "datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
-    df[
```

- Node 13 `source`
  - copy: `datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2020/files/rows.txt`
  - tasks_mini: `wikipedia/Lake_Worth_Independent_School_District/content.txt`

- Node 13 `subquestion`
  - copy: `For <hop 3 answer> in 2020-2021, what is the average percentage across each district's sites of students automatically recognized as eligible for free school meals without submitting a household meal application?`
  - tasks_mini: `In what year was Lake Worth ISD (from nodes 10-12: the ISD with highest average ISP in Tarrant County) established?`

- Node 13 `answer`
  - copy: `{"ARLINGTON ISD": 51.2, "AZLE ISD": 39.74, "BIRDVILLE ISD": 43.88, "CASTLEBERRY ISD": 52.16, "CROWLEY ISD": 47.68, "EVERMAN ISD": 66.81, "FORT WORTH ISD": 57.62, "HURST-EULESS-BEDFORD ISD": 40.11, "LAKE WORTH ISD": 65.94, "WHITE SETTLEMENT ISD": 43.51}`
  - tasks_mini: `1916`

- Node 13 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 13 `fact`

```diff
@@ -1,20 +1 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/school-nutrition-programs-contact-information-and-site-level-program-participation-pr-2020/files/rows.txt"
```

### `k-5-d-3/task_4.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `For <hop 1 answer>, what were the number of veterans receiving disability compensation in 2020?`
  - tasks_mini: `For the two counties from <node_1 answer>, what were the disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name in {Harris, Dallas}; use Total: Disability Compensation Recipients.)`

- Node 2 `fact`

```diff
@@ -6,13 +6,15 @@
-source = "datagov/fy-2020-disability-compensation-recipients-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/fy-2020-disability-compensation-recipients-by-county/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `subquestion`
  - copy: `For <hop 1 answer>, what were the number of veterans receiving disability compensation in 2023?`
  - tasks_mini: `For the two counties from <node_1 answer>, what were the disability compensation recipient counts in 2020 and 2023? (Filter for this node: State == Texas; County Name in {Harris, Dallas}; use Total: Disability Compensation Recipients.)`

- Node 3 `fact`

```diff
@@ -6,13 +6,15 @@
-source = "datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/fy-2023-disability-compensation-recipients-by-county/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 4 `subquestion`
  - copy: `What is the county seat of <hop 2 answer>?`
  - tasks_mini: `What is the county seat of the county with the larger increase in recipients?`

- Node 5 `subquestion`
  - copy: `Which University of Houston System universities are identified in <hop 3 answer> as being in that city?`
  - tasks_mini: `Which University of Houston System universities are located in the county seat from <node_4 answer>?`

- Node 6 `subquestion`
  - copy: `When was University of Houston established?`
  - tasks_mini: `When was each University of Houston System university in <node_5 answer> established?`

- Node 7 `subquestion`
  - copy: `When was University of Houston–Clear Lake established?`
  - tasks_mini: `When was each University of Houston System university in <node_5 answer> established?`

- Node 8 `subquestion`
  - copy: `When was University of Houston–Downtown established?`
  - tasks_mini: `When was each University of Houston System university in <node_5 answer> established?`

### `k-5-d-3/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `For calendar year 2021, how many employee rows are there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 1 `fact`

```diff
@@ -6,12 +6,14 @@
-source = "datagov/2021-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2021-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 2 `subquestion`
  - copy: `For calendar year 2022, how many employee rows are there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 2 `fact`

```diff
@@ -6,12 +6,14 @@
-source = "datagov/2022-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2022-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 3 `subquestion`
  - copy: `For calendar year 2023, how many employee rows are there for each of CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION?`
  - tasks_mini: `Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)`

- Node 3 `answer`
  - copy: `{"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956}`
  - tasks_mini: `CORRECTIONS`

- Node 3 `fact`

```diff
@@ -6,12 +6,19 @@
-source = "datagov/2023-state-employee-pay/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+source = 'datagov/2023-state-employee-pay/files/rows.txt'
+bucket = 'lakeqa-yc4103-datalake'
```

- Node 4 `subquestion`
  - copy: `What city is the headquarters of <hop 1 answer>?`
  - tasks_mini: `What city is the headquarters of the agency with the highest average employee count located in?`

- Node 5 `subquestion`
  - copy: `What is the historically Black university located in <hop 2 answer>?`
  - tasks_mini: `What is the historically Black university located in Jefferson City?`

- Node 6 `subquestion`
  - copy: `Who founded <hop 3 answer>?`
  - tasks_mini: `Who founded Lincoln University?`

- Node 7 `subquestion`
  - copy: `In what year did <hop 4 answer> die?`
  - tasks_mini: `In what year did James Milton Turner die?`

### `k-5-d-3/task_6.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In 2019, among Harris, Travis, Dallas, and Bexar counties, which were in the statewide top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2019, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 2 `subquestion`
  - copy: `In 2020, among Harris, Travis, Dallas, and Bexar counties, which were in the statewide top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2020, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 3 `subquestion`
  - copy: `In 2021, among Harris, Travis, Dallas, and Bexar counties, which were in the statewide top 5 for releases from the Department of Criminal Justice?`
  - tasks_mini: `In 2021, among Harris, Travis, Dallas, and Bexar counties, which were in the overall top 5 for releases from the Department of Criminal Justice? (Filter for this node: count rows by County; normalize County to uppercase; rank desc; take top 5 overall; then keep counties in the given list.)`

- Node 4 `subquestion`
  - copy: `In 2019, what were the intake counts from the Department of Criminal Justice for <hop 1 answer>?`
  - tasks_mini: `In 2019, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 5 `subquestion`
  - copy: `In 2020, what were the intake counts from the Department of Criminal Justice for <hop 1 answer>?`
  - tasks_mini: `In 2020, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 6 `subquestion`
  - copy: `In 2021, what were the intake counts from the Department of Criminal Justice for <hop 1 answer>?`
  - tasks_mini: `In 2021, what were the intake counts from the Department of Criminal Justice for the counties from hop 1? (Filter for this node: County in hop 1 list; normalize County to uppercase; count rows by County.)`

- Node 7 `subquestion`
  - copy: `What city is the county seat of <hop 2 answer>?`
  - tasks_mini: `What city is the county seat of the county from hop 2?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Its county seat is Houston, the most populous city in Texas and the fourth-most populous city in the United States.
+Harris County is the most populous county in Texas and the third-most populous in the United States. The county seat is Houston, which is also the largest city in Texas and the fourth-largest city in the United States.
```

- Node 8 `subquestion`
  - copy: `Which National Basketball Association franchise is based in <hop 3 answer> and has been there since 1971?`
  - tasks_mini: `Which National Basketball Association franchise is based in the city from hop 3 and has been there since 1971?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-The Houston Rockets are a National Basketball Association  franchise based in the city since 1971.
+The Houston Rockets are a National Basketball Association franchise based in the city since 1971.
```

- Node 9 `subquestion`
  - copy: `Who founded <hop 4 answer>?`
  - tasks_mini: `Who founded the Houston Rockets?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The Rockets were founded in 1967 in San Diego by Robert Breitbard, who paid an entry fee of US$1.75 million to join the NBA as an expansion team for the 1967-68 season.
+The Rockets were founded in 1967 in San Diego by Robert Breitbard.
```

### `k-5-d-3/task_7.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `In January 2019, how many driving-related violations did the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 2 `subquestion`
  - copy: `In January 2020, how many driving-related violations did the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 3 `subquestion`
  - copy: `In January 2021, how many driving-related violations did the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division issue?`
  - tasks_mini: `Among the United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division, which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPITOL POLICE, US. SECRET SERVICE UNIFORM DIVISION}; count rows by ISSUING_AGEN...`

- Node 3 `answer`
  - copy: `{"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32}`
  - tasks_mini: `UNITED STATES PARK POLICE`

- Node 3 `fact`

```diff
@@ -16,3 +16,5 @@
-answer = (
+counts_2019 = {"UNITED STATES PARK POLICE": 103, "UNITED STATES CAPITOL POLICE": 176, "US. SECRET SERVICE UNIFORM DIVISION": 145}
+counts_2020 = {"UNITED STATES PARK POLICE": 204, "UNITED STATES CAPITOL POLICE": 139, "US. SECRET SERVICE UNIFORM DIVISION": 118}
+counts_2021 = (
@@ -22 +24,3 @@
+averages = {agency: (counts_2019[agency] + counts_2020[agency] + counts_2021[agency]) / 3 for agency in target_agencies}
+answer = sorted(averages, key=lambda agency: (-averages[agency], agency))[0]
```

- Node 4 `subquestion`
  - copy: `Which federal agency operates <hop 1 answer>?`
  - tasks_mini: `Which federal agency operates the United States Park Police (from hop 1)?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-The Park Police is an operation of the National Park Service, which is an agency of the Department of the Interior.
+The United States Park Police is an operation of the National Park Service.
```

- Node 5 `subquestion`
  - copy: `<hop 2 answer> is within which U.S. department?`
  - tasks_mini: `The agency (from hop 2) is within which U.S. department?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-The National Park Service (NPS) is an agency of the United States federal government, within the United States Department of the Interior.
+The National Park Service is an agency within the United States Department of the Interior.
```

- Node 6 `subquestion`
  - copy: `Who is the head of <hop 3 answer>?`
  - tasks_mini: `Who is the head of the department (from hop 3)?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The department is headed by the secretary of the interior, who reports directly to the president of the United States and is a member of the president's Cabinet. The current interior secretary is Doug Burgum, who was sworn in on February 1, 2025.
+The department is headed by the secretary of the interior, who reports directly to the president of the United States and is a member of the president's Cabinet. The current interior secretary is Doug Burgum.
```

- Node 7 `subquestion`
  - copy: `Which university did <hop 4 answer> graduate from?`
  - tasks_mini: `Which university did the head of the department (from hop 4) graduate from?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-After graduating from North Dakota State University in 1978 with a bachelor's degree in university studies and earning an MBA from Stanford University two years later,
+After graduating from North Dakota State University in 1978 with a bachelor's degree in university studies and earning an MBA from Stanford University two years later.
```

### `k-5-d-3/task_8.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2019?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2019 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 1 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -5,12 +5,12 @@
-source = "datagov/budget-2019-budget-ordinance-appropriations/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
-    df.groupby("DEPARTMENT NUMBER", as_index=False)["2019 ORDINANCE (AMOUNT $)"]
```

- Node 2 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2020?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2020 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 2 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -5,12 +5,12 @@
-source = "datagov/budget-2020-budget-ordinance-appropriations/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
-    df.groupby("DEPARTMENT NUMBER", as_index=False)["2020 ORDINANCE (AMOUNT $)"]
```

- Node 3 `subquestion`
  - copy: `Which department numbers were in the top 5 by total funding in the officially approved city budget in 2021?`
  - tasks_mini: `Which department numbers were in the top 5 by total ordinance appropriation in each year 2019-2021? (Filter for this node: group by DEPARTMENT NUMBER; sum 2021 ORDINANCE (AMOUNT $); rank desc; take top 5.)`

- Node 3 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -5,12 +5,12 @@
-source = "datagov/budget-2021-budget-ordinance-appropriations/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-result = (
-    df.groupby("DEPARTMENT NUMBER", as_index=False)["2021 ORDINANCE (AMOUNT $)"]
```

- Node 4 `subquestion`
  - copy: `For 2019, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 4 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2019-budget-ordinance-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [99, 57, 85, 50]
+
```

- Node 5 `subquestion`
  - copy: `For 2020, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 5 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2020-budget-ordinance-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [99, 57, 85, 50]
+
```

- Node 6 `subquestion`
  - copy: `For 2021, what were the total salary budgets in the officially approved city budget for each department code in <hop 1 answer>?`
  - tasks_mini: `For the department numbers (from hop 1), what were the total budgeted amounts in the Budget Ordinance Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 1 intersection {99, 57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 6 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2021-budget-ordinance-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [99, 57, 85, 50]
+
```

- Node 7 `subquestion`
  - copy: `For 2019, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 7 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2019-budget-recommendations-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [57, 85, 50]
+
```

- Node 8 `subquestion`
  - copy: `For 2020, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 8 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2020-budget-recommendations-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [57, 85, 50]
+
```

- Node 9 `subquestion`
  - copy: `For 2021, what were the total salary budget recommendations for each department code in <hop 2 answer>?`
  - tasks_mini: `For the department codes (from hop 2), what were the total budgeted amounts in the Budget Recommendations Positions and Salaries dataset for each year 2019-2021? (Filter for this node: DEPARTMENT CODE in hop 2 list {57, 85, 50}; sum TOTAL BUDGETED AMOUNT by DEPARTMENT CODE.)`

- Node 9 `fact`

```diff
@@ -5,10 +5,13 @@
-source = "datagov/budget-2021-budget-recommendations-positions-and-salaries/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-department_codes = [57, 85, 50]
+
```

- Node 10 `subquestion`
  - copy: `Who was brought on as Superintendent of Police when the current-iteration head position of the Chicago Police Department was established in 1960?`
  - tasks_mini: `Who was brought on as Superintendent of Police when the position (current iteration) was established as head of the department (from hop 3)?`

- Node 11 `subquestion`
  - copy: `At which university did <hop 4 answer> obtain his bachelor's degree?`
  - tasks_mini: `At which university did O. W. Wilson (from hop 4) obtain his bachelor's degree?`

- Node 11 `fact`

```diff
@@ -1 +1 @@
-In 1921, Wilson enrolled in the University of California, Berkeley, majoring in criminology and studying under August Vollmer. Wilson graduated in 1924, with a Bachelor of Arts degree.
+O. W. Wilson received his B.A. from the University of California, Berkeley.
```

### `k-5-d-3/task_9.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Chicago library branches were in the top 5 by total number of items checked out over the year in 2019?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 5.)`

- Node 1 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2019-circulation-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2019-circulation-by-location/files/rows.txt'
```

- Node 2 `subquestion`
  - copy: `Which Chicago library branches were in the top 5 by total number of items checked out over the year in 2020?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5.)`

- Node 2 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2020-circulation-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2020-circulation-by-location/files/rows.txt'
```

- Node 3 `subquestion`
  - copy: `Which Chicago library branches were in the top 5 by total number of items checked out over the year in 2021?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5.)`

- Node 3 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2021-circulation-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2021-circulation-by-location/files/rows.txt'
```

- Node 4 `subquestion`
  - copy: `Which Chicago library branches with physical addresses were in the top 5 by total visitors in 2019?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 4 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2019-visitors-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2019-visitors-by-location/files/rows.txt'
```

- Node 5 `subquestion`
  - copy: `Which Chicago library branches were in the top 5 by total visitors in 2020?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 5 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2020-visitors-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2020-visitors-by-location/files/rows.txt'
```

- Node 6 `subquestion`
  - copy: `Which Chicago library branches were in the top 5 by total visitors in 2021?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 6 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 6 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2021-visitors-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2021-visitors-by-location/files/rows.txt'
```

- Node 7 `subquestion`
  - copy: `Which Chicago library branches were in the top 3 by total public-computer logins in 2019?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 7 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 7 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2019-computer-sessions-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2019-computer-sessions-by-location/files/rows.txt'
```

- Node 8 `subquestion`
  - copy: `Which Chicago library branches were in the top 3 by total public-computer logins in 2020?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 8 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 8 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2020-computer-sessions-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2020-computer-sessions-by-location/files/rows.txt'
```

- Node 9 `subquestion`
  - copy: `Which Chicago library branches were in the top 3 by total public-computer logins in 2021?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 9 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 9 `fact`

```diff
@@ -5,12 +5,15 @@
-source = "datagov/libraries-2021-computer-sessions-by-location/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+
+source = 'datagov/libraries-2021-computer-sessions-by-location/files/rows.txt'
```

- Node 10 `subquestion`
  - copy: `Which Chicago neighborhood is <hop 3 answer> located in?`
  - tasks_mini: `Which Chicago neighborhood is the library branch (from hop 3) located in? (Lookup: Conrad Sulzer Regional Library article.)`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-is located in the Lincoln Square neighborhood at 4455 N. Lincoln Avenue.
+According to the Wikipedia article for Conrad Sulzer Regional Library, the library is located in the Lincoln Square neighborhood at 4455 N. Lincoln Avenue.
```

- Node 11 `subquestion`
  - copy: `What community area number corresponds to <hop 4 answer>?`
  - tasks_mini: `What community area number corresponds to the neighborhood from hop 4? (Filter for this node: Community Area == 'Lincoln Square'; return Community Area Number.)`

- Node 11 `answer`
  - copy: `4`
  - tasks_mini: `4`

- Node 11 `fact`

```diff
@@ -5,6 +5,8 @@
-source = "datagov/public-health-statistics-life-expectancy-by-community-area/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-answer = int(df.loc[df["Community Area"] == "Lincoln Square", "Community Area Number"].iloc[0])
+
```

### `k-5-d-4/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which New York counties have at least 65 bridges with Poor Status = Y, and what is each qualifying county's poor-bridge count?`
  - tasks_mini: `Which NY counties have at least 65 bridges rated 'Poor' status?`

- Node 1 `answer`
  - copy: `{"Erie County": 82, "Orange County": 67, "Ulster County": 84, "Westchester County": 68}`
  - tasks_mini: `["Ulster County", "Erie County", "Westchester County", "Orange County"]`

- Node 1 `fact`

```diff
@@ -3,16 +3,15 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `subquestion`
  - copy: `Which New York counties have at least 50 fire departments, and what is each qualifying county's fire department count?`
  - tasks_mini: `Which NY counties have at least 50 fire departments?`

- Node 2 `answer`
  - copy: `{"Erie County": 91, "Nassau County": 70, "Oneida County": 50, "Onondaga County": 53, "Orange County": 52, "Suffolk County": 108, "Ulster County": 51, "Westchester County": 57}`
  - tasks_mini: `["Suffolk County", "Erie County", "Nassau County", "Westchester County", "Onondaga County", "Orange County", "Ulster County", "Oneida County"]`

- Node 2 `fact`

```diff
@@ -3,15 +3,14 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `subquestion`
  - copy: `Which New York counties have at least 100 bank-owned ATM locations, and what is each qualifying county's ATM count?`
  - tasks_mini: `Which NY counties have at least 100 bank ATMs?`

- Node 3 `answer`
  - copy: `{"Albany County": 148, "Bronx County": 158, "Dutchess County": 125, "Erie County": 244, "Kings County": 388, "Monroe County": 232, "Nassau County": 515, "New York County": 676, "Onondaga County": 182, "Orange County": 128, "Queens County": 429, "Richmond County": 115, "Suffolk County": 494, "Westchester County": 335}`
  - tasks_mini: `["New York County", "Nassau County", "Suffolk County", "Queens County", "Kings County", "Westchester County", "Erie County", "Monroe County", "Onondaga County", "Bronx County", "Albany County", "Orange County", "Dutchess County", "Richmond County"]`

- Node 3 `fact`

```diff
@@ -3,15 +3,14 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `subquestion`
  - copy: `Which New York counties have at least 1.0 MW of total New Renewable Capacity (MW) among projects whose Project Status is Operational, and what is each qualifying county's operational renewable capacity?`
  - tasks_mini: `Which NY counties have at least 1.0 MW of operational renewable energy capacity?`

- Node 4 `answer`
  - copy: `{"Albany County": 20.0, "Broome County": 111.8, "Chautauqua County": 185.9, "Chenango County": 20.0, "Cortland County": 20.0, "Erie County": 11.48, "Franklin County": 79.3, "Jefferson County": 7.35, "Lewis County": 183.99, "Livingston County": 177.0, "Montgomery County": 130.0, "Oswego County": 1.32, "Saratoga County": 20.0, "Schenectady County": 19.99, "Sc...`
  - tasks_mini: `["Steuben County", "Chautauqua County", "Lewis County", "Livingston County", "Montgomery County", "Broome County", "Franklin County", "Schoharie County", "Washington County", "Saratoga County", "Albany County", "Cortland County", "Chenango County", "Schenectady County", "Erie County", "Jefferson County", "Westchester County", "Sullivan County", "Oswego Coun...`

- Node 4 `fact`

```diff
@@ -5,2 +5,3 @@
+
@@ -9,11 +10,19 @@
-df["New Renewable Capacity (MW)"] = pd.to_numeric(df["New Renewable Capacity (MW)"], errors="coerce")
-result = (
-    df[df["Project Status"].eq("Operational")]
-    .groupby("County/Province", dropna=False)["New Renewable Capacity (MW)"]
-    .sum()
```

- Node 5 `subquestion`
  - copy: `What is the county seat of Erie County from <hop 1 answer>?`
  - tasks_mini: `What is the county seat of Erie County (from <intersection of nodes 1-4>)?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-The county seat is Buffalo, which makes up about 28% of the county's population.
+Erie County's county seat is Buffalo, which makes up about 28% of the county's population.
```

- Node 6 `subquestion`
  - copy: `What is the county seat of Westchester County from <hop 1 answer>?`
  - tasks_mini: `What is the county seat of Westchester County (from <intersection of nodes 1-4>)?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The county seat is the city of White Plains, while the most populous municipality in the county is the city of Yonkers, with 211,569 residents per the 2020 census.
+Westchester County's county seat is the city of White Plains.
```

- Node 7 `subquestion`
  - copy: `Between Erie County and Westchester County from <hop 1 answer>, what are the 2021 Violent Count totals, and which county is higher?`
  - tasks_mini: `Which county had more violent crimes in 2021: Erie County (seat: <node_5 answer>) or Westchester County (seat: <node_6 answer>)?`

- Node 7 `answer`
  - copy: `{"Erie County": 3493, "Westchester County": 1520}`
  - tasks_mini: `Erie County`

- Node 7 `fact`

```diff
@@ -5,2 +5,3 @@
+
@@ -9,9 +10,11 @@
+
+df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
+df["Violent Count"] = pd.to_numeric(df["Violent Count"], errors="coerce")
-    df[(df["Year"] == 2021) & (df["County"].isin(["Erie", "Westchester"]))]
-    [["County", "Year", "Violent Count"]]
```

- Node 8 `subquestion`
  - copy: `According to the Wikipedia article for <node 5 answer>, what land company acquired the land that became the seat of <hop 3 answer>?`
  - tasks_mini: `What land company acquired the land that became Buffalo (<node_5 answer>, the seat of <node_7 answer>)?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-The rights to the Massachusetts territories were sold to Robert Morris in 1791. Despite objections from Seneca chief Red Jacket, Morris brokered a deal between fellow chief Cornplanter and the Dutch dummy corporation Holland Land Company. The Holland Land Purchase gave the Senecas three reservations, and the Holland Land Company received
+The rights to the Massachusetts territories were sold to Robert Morris in 1791. Morris brokered a deal with the Dutch dummy corporation Holland Land Company. The Holland Land Purchase gave the Senecas three reservations, and the Holland Land Company received the land for about thirty-three cents per acre.
```

- Node 9 `subquestion`
  - copy: `In what year was <hop 4 answer> founded?`
  - tasks_mini: `In what year was <node_8 answer> founded?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-In 1789, four Dutch firms, Pieter Stadnitski and Son,  Nicolaas and Jacob Van Staphorst, P. & C. Van Eeghen, and Ten Cate & Vollenhoven, joined together and hired Dutch financier Theophile Cazenove as their purchasing agent to engage in land speculation.
+In 1789, four Dutch firms, Pieter Stadnitski and Son, Nicolaas and Jacob Van Staphorst, P. & C. Van Eeghen, and Ten Cate & Vollenhoven, joined together and hired Dutch financier Theophile Cazenove as their purchasing agent to engage in land speculation.
```

### `k-5-d-4/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the total FY2007 expenditures by Missouri state agency, so this year's agency totals can be combined with FY2008-FY2010 to rank agencies by average expenditure across FY2007-FY2010?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2007; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 1 `answer`
  - copy: `{"AGRICULTURE": 31813546.32, "COMMERCE AND INSURANCE": 2009267.01, "CONSERVATION": 68648122.91, "CORRECTIONS": 279877976.24, "ECONOMIC DEVELOPMENT": 174094167.56, "ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HEALTH AND SENIOR SERVICES": 698796366.98, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "JUDICIARY": 44966740.94, "LABOR AND INDUSTRIA...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "MENTAL HEALTH": 759892459.14, "SOCIAL SERVICES": 5528171459.84, "TRANSPORTATION": 1922237354.88}`

- Node 1 `fact`

```diff
@@ -1,2 +1 @@
-import io
@@ -5,17 +4,21 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/2007-state-expenditures/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
```

- Node 2 `subquestion`
  - copy: `What are the total FY2008 expenditures by Missouri state agency, so this year's agency totals can be combined with FY2007, FY2009, and FY2010 to rank agencies by average expenditure across FY2007-FY2010?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2008; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 2 `answer`
  - copy: `{"AGRICULTURE": 37088287.9, "COMMERCE AND INSURANCE": 6346960.76, "CONSERVATION": 71467088.65, "CORRECTIONS": 279260171.22, "ECONOMIC DEVELOPMENT": 205680617.98, "ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HEALTH AND SENIOR SERVICES": 734833032.4, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "JUDICIARY": 47543796.72, "LABOR AND INDUSTRIAL ...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "MENTAL HEALTH": 813799778.73, "SOCIAL SERVICES": 5988522037.62, "TRANSPORTATION": 1786534604.37}`

- Node 2 `fact`

```diff
@@ -4,15 +4,12 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/2008-state-expenditures/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 3 `subquestion`
  - copy: `What are the total FY2009 expenditures by Missouri state agency, so this year's agency totals can be combined with FY2007, FY2008, and FY2010 to rank agencies by average expenditure across FY2007-FY2010?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2009; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 3 `answer`
  - copy: `{"AGRICULTURE": 45903725.15, "COMMERCE AND INSURANCE": 6514041.0, "CONSERVATION": 68528448.2, "CORRECTIONS": 286079463.35, "ECONOMIC DEVELOPMENT": 224463661.07, "ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HEALTH AND SENIOR SERVICES": 815631750.83, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "JUDICIARY": 45870978.11, "LABOR AND INDUSTRIAL ...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "MENTAL HEALTH": 877438429.19, "SOCIAL SERVICES": 6707806742.86, "TRANSPORTATION": 2000940522.19}`

- Node 3 `fact`

```diff
@@ -4,15 +4,12 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/2009-state-expenditures/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 4 `subquestion`
  - copy: `What are the total FY2010 expenditures by Missouri state agency, so this year's agency totals can be combined with FY2007, FY2008, and FY2009 to rank agencies by average expenditure across FY2007-FY2010?`
  - tasks_mini: `Which Missouri state agency had the 3rd highest average expenditure from FY2007-FY2010? (Filter for this node: Fiscal Year == 2010; group by Agency Name; sum Payments Total; rank by total; keep top 5.)`

- Node 4 `answer`
  - copy: `{"AGRICULTURE": 40395382.19, "COMMERCE AND INSURANCE": 5910088.04, "CONSERVATION": 61908035.44, "CORRECTIONS": 268435627.28, "ECONOMIC DEVELOPMENT": 263220946.8, "ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HEALTH AND SENIOR SERVICES": 884344054.2500001, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "JUDICIARY": 45794975.93, "LABOR AND INDUS...`
  - tasks_mini: `{"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "MENTAL HEALTH": 921056914.52, "SOCIAL SERVICES": 7141666880.32, "TRANSPORTATION": 2144139919.08}`

- Node 4 `fact`

```diff
@@ -4,15 +4,12 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/2010-state-expenditures/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 5 `subquestion`
  - copy: `In which city is the Southwest district of <hop 1 answer> based?`
  - tasks_mini: `In which city is the Southwest district of the agency (from hop 1: TRANSPORTATION/MoDOT) based? (Lookup: find the district list and Southwest base city in the MoDOT article.)`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-MoDOT operates seven districts throughout the state: Northwest, based in St. Joseph; Northeast, based in Hannibal; Kansas City, based in Lee's Summit; Central, based in Jefferson City; St. Louis, based in Chesterfield; Southwest, based in Springfield; and Southeast, based in Sikeston.
+According to the Wikipedia article for Missouri Department of Transportation, 'MoDOT operates seven districts throughout the state: Northwest, based in St. Joseph; Northeast, based in Hannibal; Kansas City, based in Lee's Summit; Central, based in Jefferson City; St. Louis, based in Chesterfield; Southwest, based in Springfield; and Southeast, based in Sikeston.'
```

- Node 6 `subquestion`
  - copy: `What are the terminus cities of the highway whose name was first proposed in <hop 2 answer>?`
  - tasks_mini: `What are the terminus cities of the highway that was born in the city (from hop 2: Springfield)? (Lookup: Springfield article line describing Route 66 as the Chicago-to-Los Angeles highway.)`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.
+According to the Wikipedia article for Springfield, Missouri, 'Springfield's nicknames include "Queen City of the Ozarks" and "The Birthplace of Route 66"...Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.'
```

- Node 7 `subquestion`
  - copy: `What is the 2016 city-level crude binge drinking prevalence for each of the two Route 66 terminus cities, Chicago and Los Angeles, so their 2016 and 2018 values can be compared across both releases?`
  - tasks_mini: `Which terminus city (from hop 3: Chicago or Los Angeles) had higher average binge drinking prevalence across the 2016 and 2018 500-Cities health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 7 `fact`

```diff
@@ -1,3 +1,3 @@
-import pandas as pd
+import csv
@@ -9,16 +9,13 @@
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-df["Data_Value"] = pd.to_numeric(df["Data_Value"], errors="coerce")
-answer = (
-    df.loc[
```

- Node 8 `subquestion`
  - copy: `What is the 2018 city-level crude binge drinking prevalence for each of the two Route 66 terminus cities, Chicago and Los Angeles, so their 2016 and 2018 values can be compared across both releases?`
  - tasks_mini: `Which terminus city (from hop 3: Chicago or Los Angeles) had higher average binge drinking prevalence across the 2016 and 2018 500-Cities health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 8 `fact`

```diff
@@ -1,3 +1,3 @@
-import pandas as pd
+import csv
@@ -9,16 +9,13 @@
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-df["Data_Value"] = pd.to_numeric(df["Data_Value"], errors="coerce")
-answer = (
-    df.loc[
```

- Node 9 `subquestion`
  - copy: `What is each Chicago department's total overtime cost in 2014, so the department totals can be combined with 2015-2017 to determine which department ranks second by total overtime across 2014-2017?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city (from hop 4: Chicago)? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 9 `answer`
  - copy: `{"Administrative Hearings": 78.45, "Animal Care and Control": 490423.37, "Aviation": 13147383.4, "Board of Election Commissioners": 447070.65, "Buildings": 336975.7, "City Clerk": 133299.31, "Emergency Management and Communications": 10051342.17, "Family and Support Services": 70553.37, "Finance": 49766.22, "Fire": 63941565.36, "Fleet and Facility Managemen...`
  - tasks_mini: `{"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}`

- Node 9 `fact`

```diff
@@ -10,10 +10,5 @@
+
-answer = (
-    df.loc[:, ["DEPARTMENT NAME", "TOTAL"]]
-    .dropna(subset=["TOTAL"])
-    .groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
```

- Node 10 `subquestion`
  - copy: `What is each Chicago department's total overtime cost in 2015, so the department totals can be combined with 2014, 2016, and 2017 to determine which department ranks second by total overtime across 2014-2017?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city (from hop 4: Chicago)? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 10 `answer`
  - copy: `{"Animal Care and Control": 460788.49, "Aviation": 10028911.51, "Board of Election Commissioners": 337421.14, "Buildings": 512654.06, "City Clerk": 108099.77, "Emergency Management and Communications": 10945883.57, "Family & Support Services": 35247.94, "Finance": 22754.81, "Fire": 43847384.3, "Fleet and Facility Management": 4336312.0, "Independent Police ...`
  - tasks_mini: `{"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}`

- Node 10 `fact`

```diff
@@ -10,10 +10,5 @@
+
-answer = (
-    df.loc[:, ["DEPARTMENT NAME", "TOTAL"]]
-    .dropna(subset=["TOTAL"])
-    .groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
```

- Node 11 `subquestion`
  - copy: `What is each Chicago department's total overtime cost in 2016, so the department totals can be combined with 2014, 2015, and 2017 to determine which department ranks second by total overtime across 2014-2017?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city (from hop 4: Chicago)? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 11 `answer`
  - copy: `{"Animal Care and Control": 514031.65, "Aviation": 12881495.76, "Board of Election Commissioners": 600083.73, "Buildings": 553205.3, "Business Affairs and Consumer Protection": 1.71, "City Clerk": 62226.92, "City Council": 3352.47, "Emergency Management and Communications": 11031421.65, "Family and Support Services": 48187.91, "Finance": 74180.33, "Fire": 5...`
  - tasks_mini: `{"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}`

- Node 11 `fact`

```diff
@@ -10,10 +10,5 @@
+
-answer = (
-    df.loc[:, ["DEPARTMENT NAME", "TOTAL"]]
-    .dropna(subset=["TOTAL"])
-    .groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
```

- Node 12 `subquestion`
  - copy: `What is each Chicago department's total overtime cost in 2017, so the department totals can be combined with 2014-2016 to determine which department ranks second by total overtime across 2014-2017?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city (from hop 4: Chicago)? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 12 `answer`
  - copy: `{"Administrative Hearings": 13472.0, "Animal Care and Control": 530063.0, "Aviation": 14884756.0, "Board of Election Commissioners": 6882.0, "Buildings": 665130.0, "City Clerk": 80427.0, "Civilian Office of Police Accountability": 26415.0, "Emergency Management and Communications": 10619207.0, "Family and Support Services": 66390.0, "Finance": 161744.0, "Fi...`
  - tasks_mini: `{"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}`

- Node 12 `fact`

```diff
@@ -10,10 +10,5 @@
+
-answer = (
-    df.loc[:, ["DEPARTMENT NAME", "TOTAL"]]
-    .dropna(subset=["TOTAL"])
-    .groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
```

### `k-5-d-4/task_3.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1 +1 @@
-Southwest, based in Springfield;
+According to the Wikipedia article for Missouri Department of Transportation, 'MoDOT operates seven districts throughout the state: Northwest, based in St. Joseph; Northeast, based in Hannibal; Kansas City, based in Lee's Summit; Central, based in Jefferson City; St. Louis, based in Chesterfield; Southwest, based in Springfield; and Southeast, based in Sikeston.'
```

- Node 2 `subquestion`
  - copy: `What are the terminus cities of the highway whose name was first proposed in <hop 1 answer>?`
  - tasks_mini: `What are the terminus cities of the highway that was born in <node_1 answer>?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.
+According to the Wikipedia article for Springfield, Missouri, 'Springfield's nicknames include "Queen City of the Ozarks" and "The Birthplace of Route 66"...Officially recognized as the birthplace of Route 66, it was in Springfield on April 30, 1926, that officials first proposed the name of the new Chicago-to-Los Angeles highway.'
```

- Node 3 `subquestion`
  - copy: `What was the 2016 city-level crude prevalence of binge drinking for the cities in <hop 2 answer>?`
  - tasks_mini: `Which terminus city (from <node_2 answer>) had higher average binge drinking prevalence across the 2016 and 2018 500-Cities health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 3 `fact`

```diff
@@ -1,3 +1,3 @@
-import pandas as pd
+import csv
@@ -9,14 +9,13 @@
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-
-answer = (
-    df[
```

- Node 4 `subquestion`
  - copy: `What was the 2018 city-level crude prevalence of binge drinking for the cities in <hop 2 answer>?`
  - tasks_mini: `Which terminus city (from <node_2 answer>) had higher average binge drinking prevalence across the 2016 and 2018 500-Cities health releases? (Filter for this node: Short_Question_Text == 'Binge Drinking'; GeographicLevel == 'City'; Data_Value_Type == 'Crude prevalence'; CityName in {Chicago, Los Angeles}; use Data_Value.)`

- Node 4 `fact`

```diff
@@ -1,3 +1,3 @@
-import pandas as pd
+import csv
@@ -9,14 +9,13 @@
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-
-answer = (
-    df[
```

- Node 5 `subquestion`
  - copy: `What was each department's total overtime cost in <hop 3 answer> in 2014?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 5 `answer`
  - copy: `{"Aviation": 13147383.4, "Fire": 63941565.36, "Police": 101460132.24, "Streets and Sanitation": 15393693.24, "Water Management": 23507061.7}`
  - tasks_mini: `{"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}`

- Node 5 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -12,8 +12,3 @@
-
-answer = (
-    df.groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
-    .sort_values(ascending=False)
-    .to_dict()
```

- Node 6 `subquestion`
  - copy: `What was each department's total overtime cost in <hop 3 answer> in 2015?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 6 `answer`
  - copy: `{"Emergency Management and Communications": 10945883.57, "Fire": 43847384.3, "Police": 116144553.32, "Streets and Sanitation": 16582331.52, "Water Management": 19954056.68}`
  - tasks_mini: `{"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}`

- Node 6 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 6 `fact`

```diff
@@ -12,8 +12,3 @@
-
-answer = (
-    df.groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
-    .sort_values(ascending=False)
-    .to_dict()
```

- Node 7 `subquestion`
  - copy: `What was each department's total overtime cost in <hop 3 answer> in 2016?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 7 `answer`
  - copy: `{"Aviation": 12881495.76, "Fire": 50604010.67, "Police": 143032724.45, "Streets and Sanitation": 13836742.94, "Water Management": 21335912.52}`
  - tasks_mini: `{"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}`

- Node 7 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 7 `fact`

```diff
@@ -12,8 +12,3 @@
-
-answer = (
-    df.groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
-    .sort_values(ascending=False)
-    .to_dict()
```

- Node 8 `subquestion`
  - copy: `What was each department's total overtime cost in <hop 3 answer> in 2017?`
  - tasks_mini: `Which city department had the 2nd highest total overtime from 2014-2017 in the city identified from the binge drinking comparison? (Filter for this node: group by DEPARTMENT NAME; sum TOTAL; rank by total; keep top departments.)`

- Node 8 `answer`
  - copy: `{"Aviation": 14884756.0, "Fire": 49571354.0, "Police": 156732988.0, "Streets and Sanitation": 10718299.0, "Water Management": 20049910.0}`
  - tasks_mini: `{"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}`

- Node 8 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 8 `fact`

```diff
@@ -12,8 +12,3 @@
-
-answer = (
-    df.groupby("DEPARTMENT NAME", dropna=False)["TOTAL"]
-    .sum()
-    .sort_values(ascending=False)
-    .to_dict()
```

- Node 9 `subquestion`
  - copy: `In what year was the paid City of Chicago Fire Department, corresponding to <hop 4 answer>, organized?`
  - tasks_mini: `In what year was the department identified in the overtime comparison founded?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The volunteer fire department was disestablished on August 2, 1858, when the city council passed the ordinance organizing the paid City of Chicago Fire Department.
+According to the Wikipedia article for Chicago Fire Department, 'The volunteer fire department was disestablished on August 2, 1858, when the city council passed the ordinance organizing the paid City of Chicago Fire Department.' The department was founded in 1858.
```

### `k-5-d-4/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the top five SiteCounty values by total LunchTotal in the 2015-2016 SSO dataset?`
  - tasks_mini: `Which Texas counties were in the top five for SSO LunchTotal in every program year from 2015-2016 through 2018-2019? (Filter for this node: ProgramYear == 2015-2016; group by SiteCounty; sum LunchTotal; rank by total; keep top 5.)`

- Node 1 `answer`
  - copy: `["HARRIS", "HIDALGO", "DALLAS", "CAMERON", "EL PASO"]`
  - tasks_mini: `["Harris", "Hidalgo", "Dallas", "Cameron", "El Paso"]`

- Node 1 `fact`

```diff
@@ -4,15 +4,13 @@
-from botocore.config import Config
-source = "datagov/summer-meal-programs-seamless-summer-option-sso-meal-count-information-program-period-2016/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 2 `subquestion`
  - copy: `What are the top five SiteCounty values by total LunchTotal in the 2016-2017 SSO dataset?`
  - tasks_mini: `Which Texas counties were in the top five for SSO LunchTotal in every program year from 2015-2016 through 2018-2019? (Filter for this node: ProgramYear == 2016-2017; group by SiteCounty; sum LunchTotal; rank by total; keep top 5.)`

- Node 2 `answer`
  - copy: `["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"]`
  - tasks_mini: `["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]`

- Node 2 `fact`

```diff
@@ -4,15 +4,13 @@
-from botocore.config import Config
-source = "datagov/summer-meal-programs-seamless-summer-option-sso-meal-count-information-program-period-2017/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 3 `subquestion`
  - copy: `What are the top five SiteCounty values by total LunchTotal in the 2017-2018 SSO dataset?`
  - tasks_mini: `Which Texas counties were in the top five for SSO LunchTotal in every program year from 2015-2016 through 2018-2019? (Filter for this node: ProgramYear == 2017-2018; group by SiteCounty; sum LunchTotal; rank by total; keep top 5.)`

- Node 3 `answer`
  - copy: `["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"]`
  - tasks_mini: `["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]`

- Node 3 `fact`

```diff
@@ -4,15 +4,13 @@
-from botocore.config import Config
-source = "datagov/summer-meal-programs-seamless-summer-option-sso-meal-count-information-program-period-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 4 `subquestion`
  - copy: `What are the top five SiteCounty values by total LunchTotal in the 2018-2019 SSO dataset?`
  - tasks_mini: `Which Texas counties were in the top five for SSO LunchTotal in every program year from 2015-2016 through 2018-2019? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum LunchTotal; rank by total; keep top 5.)`

- Node 4 `answer`
  - copy: `["HIDALGO", "HARRIS", "DALLAS", "BEXAR", "CAMERON"]`
  - tasks_mini: `["Hidalgo", "Harris", "Dallas", "Bexar", "Cameron"]`

- Node 4 `fact`

```diff
@@ -4,15 +4,13 @@
-from botocore.config import Config
-source = "datagov/summer-meal-programs-seamless-summer-option-sso-meal-count-information-program-period-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 5 `subquestion`
  - copy: `What is the total TotalMealReimbursement for each SiteCounty in the 2018-2019 CACFP day care homes dataset?`
  - tasks_mini: `Among {Harris, Hidalgo, Dallas, Cameron} (from hop 1), which counties had the largest percentage decrease in CACFP day care home meal reimbursements between the 2018-2019 and 2020-2021 program years? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum TotalMealReimbursement.)`

- Node 5 `answer`
  - copy: `{"BEXAR": 1805014.14, "COLLIN": 825207.4400000001, "DALLAS": 2835278.75, "DENTON": 882025.85, "EL PASO": 1551768.98, "FORT BEND": 1298515.91, "HARRIS": 8757796.13, "HIDALGO": 1202699.73, "TARRANT": 2844452.79, "TRAVIS": 714664.26}`
  - tasks_mini: `{"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}`

- Node 5 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 5 `fact`

```diff
@@ -4,14 +4,14 @@
-from botocore.config import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-meal-reimbursement-program-ye-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 6 `subquestion`
  - copy: `What is the total TotalMealReimbursement for each SiteCounty in the 2020-2021 CACFP day care homes dataset?`
  - tasks_mini: `Among {Harris, Hidalgo, Dallas, Cameron} (from hop 1), which counties had the largest percentage decrease in CACFP day care home meal reimbursements between the 2018-2019 and 2020-2021 program years? (Filter for this node: ProgramYear == 2020-2021; group by SiteCounty; sum TotalMealReimbursement.)`

- Node 6 `answer`
  - copy: `{"BELL": 611323.37, "BEXAR": 1419344.89, "COLLIN": 832593.43, "DALLAS": 2393411.26, "DENTON": 839300.91, "EL PASO": 1302944.72, "FORT BEND": 1191854.65, "HARRIS": 7558597.77, "HIDALGO": 971063.56, "TARRANT": 2155296.17}`
  - tasks_mini: `{"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}`

- Node 6 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 6 `fact`

```diff
@@ -4,14 +4,14 @@
-from botocore.config import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-day-care-homes-meal-reimbursement-program-ye-2020/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 7 `subquestion`
  - copy: `What is the total EnrollmentQty for each SiteCounty in the 2018-2019 CACFP child centers dataset?`
  - tasks_mini: `Among {Hidalgo, Cameron} (from hop 2), which county had the higher average CACFP child-center EnrollmentQty across the 2018-2019 and 2019-2020 program years? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum EnrollmentQty.)`

- Node 7 `answer`
  - copy: `{"BEXAR": 1579009, "CAMERON": 7620183, "DALLAS": 1615421, "EL PASO": 1586612, "HARRIS": 3543992, "HIDALGO": 1661128, "KAUFMAN": 355356, "NUECES": 712050, "TARRANT": 724543, "TRAVIS": 493040}`
  - tasks_mini: `{"Cameron": 7620183, "Hidalgo": 1661128}`

- Node 7 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 7 `fact`

```diff
@@ -4,14 +4,14 @@
-from botocore.config import Config
-source = "datagov/child-and-adult-care-food-program-cacfp-child-centers-meal-reimbursement-program-year-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 8 `subquestion`
  - copy: `What is the total EnrollmentQty for each SiteCounty in the 2019-2020 CACFP child centers dataset?`
  - tasks_mini: `Among {Hidalgo, Cameron} (from hop 2), which county had the higher average CACFP child-center EnrollmentQty across the 2018-2019 and 2019-2020 program years? (Filter for this node: ProgramYear == 2019-2020; group by SiteCounty; sum EnrollmentQty.)`

- Node 8 `answer`
  - copy: `{"BEXAR": 1602569, "BRAZORIA": 466678, "CAMERON": 1076746, "DALLAS": 1768090, "EL PASO": 1116732, "FORT BEND": 443344, "HARRIS": 4473140, "HIDALGO": 1477805, "NUECES": 761234, "TARRANT": 1038036}`
  - tasks_mini: `{"Cameron": 1076746, "Hidalgo": 1477805}`

- Node 8 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 8 `fact`

```diff
@@ -4,14 +4,14 @@
-from botocore.config import Config
-source = "datagov/child-and-adult-care-food-program-cacfp-child-centers-meal-reimbursement-program-year-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
+from botocore.client import Config
```

- Node 9 `subquestion`
  - copy: `What is the county seat of <hop 3 answer>?`
  - tasks_mini: `What is the county seat of Cameron County, Texas (from hop 3)? (Lookup: county seat statement in the Cameron County, Texas article.)`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-Its county seat is Brownsville.
+Cameron County's county seat is Brownsville.
```

- Node 10 `subquestion`
  - copy: `On which coast is <hop 4 answer> located?`
  - tasks_mini: `On which coast is Brownsville (from hop 4) located? (Lookup: Brownsville, Texas article location description.)`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-located on the western Gulf Coast in South Texas
+Brownsville is located on the western Gulf Coast in South Texas.
```

### `k-5-d-4/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What is the total adult day care meal reimbursement in 2016-2017 for each SiteCounty?`
  - tasks_mini: `Which Texas counties had the five largest percent decreases in total adult day care meal reimbursements from 2016-2019 among counties averaging at least $50,000 across 2016-2019? (Filter for this node: ProgramYear == 2016-2017; group by SiteCounty; sum TotalReimbursement.)`

- Node 1 `answer`
  - copy: `{"BEE": 602056.1175, "BEXAR": 1976511.21, "CAMERON": 4343483.48, "DALLAS": 1337723.91, "EL PASO": 1820860.48, "HARRIS": 3679408.0625, "HIDALGO": 17696191.32, "MAVERICK": 691767.64, "STARR": 1391135.61, "WEBB": 973942.41}`
  - tasks_mini: `{"Atascosa County": 141083.37, "Brooks County": 60454.65, "Comal County": 112322.52, "Victoria County": 95559.47, "Willacy County": 158153.77}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -4,16 +4,25 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-adult-day-care-centers-meal-reimbursement-pr-2016/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 2 `subquestion`
  - copy: `What is the total adult day care meal reimbursement in 2017-2018 for each SiteCounty?`
  - tasks_mini: `Which Texas counties had the five largest percent decreases in total adult day care meal reimbursements from 2016-2019 among counties averaging at least $50,000 across 2016-2019? (Filter for this node: ProgramYear == 2017-2018; group by SiteCounty; sum TotalReimbursement.)`

- Node 2 `answer`
  - copy: `{"BEE": 570655.59, "BEXAR": 2001499.64, "CAMERON": 4324920.055, "DALLAS": 1544675.66, "EL PASO": 2080749.0275, "HARRIS": 3708737.04, "HIDALGO": 17691217.5075, "MAVERICK": 739907.22, "STARR": 1456837.1, "WEBB": 860851.4225}`
  - tasks_mini: `{"Atascosa County": 142115.25, "Brooks County": 66250.97, "Comal County": 88868.98, "Victoria County": 89291.24, "Willacy County": 160898.5925}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -4,16 +4,25 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-adult-day-care-centers-meal-reimbursement-pr-2017/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 3 `subquestion`
  - copy: `What is the total adult day care meal reimbursement in 2018-2019 for each SiteCounty?`
  - tasks_mini: `Which Texas counties had the five largest percent decreases in total adult day care meal reimbursements from 2016-2019 among counties averaging at least $50,000 across 2016-2019? (Filter for this node: ProgramYear == 2018-2019; group by SiteCounty; sum TotalReimbursement.)`

- Node 3 `answer`
  - copy: `{"BEE": 595756.985, "BEXAR": 2011461.89, "CAMERON": 4404181.145, "DALLAS": 1705207.2, "EL PASO": 2320209.535, "HARRIS": 3969441.2625, "HIDALGO": 18004813.5775, "MAVERICK": 748749.75, "STARR": 1470270.14, "WEBB": 869702.53}`
  - tasks_mini: `{"Atascosa County": 139933.33, "Brooks County": 78426.43, "Comal County": 78748.11, "Victoria County": 88676.32, "Willacy County": 143725.8525}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -4,16 +4,25 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-adult-day-care-centers-meal-reimbursement-pr-2018/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 4 `subquestion`
  - copy: `What is the total adult day care meal reimbursement in 2019-2020 for BROOKS, WILLACY, COMAL, ATASCOSA, and VICTORIA, treating counties absent from this file as 0?`
  - tasks_mini: `Which Texas counties had the five largest percent decreases in total adult day care meal reimbursements from 2016-2019 among counties averaging at least $50,000 across 2016-2019? (Filter for this node: ProgramYear == 2019-2020; group by SiteCounty; sum TotalReimbursement; treat missing counties as 0.)`

- Node 4 `answer`
  - copy: `{"ATASCOSA": 52913.23, "BROOKS": 0.0, "COMAL": 37371.2, "VICTORIA": 40390.435, "WILLACY": 5005.3}`
  - tasks_mini: `{"Atascosa County": 52913.23, "Brooks County": 0, "Comal County": 37371.2, "Victoria County": 40390.435, "Willacy County": 5005.3}`

- Node 4 `fact`

```diff
@@ -4,16 +4,25 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/child-and-adult-care-food-programs-cacfp-adult-day-care-centers-meal-reimbursement-pr-2019/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 5 `subquestion`
  - copy: `How many abuse/neglect-related child fatalities were recorded from 2018 through 2022 for each county in <hop 1 answer>?`
  - tasks_mini: `Among the counties from hop 1, which had at least 1 abuse/neglect-related child fatality (2018-2022)? (Filter for this node: Fiscal Year in 2018-2022; group by County; sum Abuse Neglect Fatalities.)`

- Node 5 `answer`
  - copy: `{"Atascosa": 0, "Brooks": 1, "Comal": 5, "Victoria": 6, "Willacy": 2}`
  - tasks_mini: `["Brooks County", "Willacy County", "Comal County", "Victoria County"]`

- Node 5 `fact`

```diff
@@ -4,16 +4,14 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/ocs-1-1-abuse-neglect-related-texas-child-fatalities-fy2013-fy2022/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 6 `subquestion`
  - copy: `How many non-abuse/neglect child fatality investigations were recorded from 2018 through 2022 for each county in <hop 1 answer>?`
  - tasks_mini: `Among the counties from hop 1, which had at least 3 non-abuse/neglect child fatality investigations (2018-2022)? (Filter for this node: Fiscal Year in 2018-2022; group by County; sum Non-Abuse/Neglect Fatalities Investigated.)`

- Node 6 `answer`
  - copy: `{"Atascosa": 6, "Brooks": 1, "Comal": 16, "Victoria": 11, "Willacy": 3}`
  - tasks_mini: `["Willacy County", "Comal County", "Atascosa County", "Victoria County"]`

- Node 6 `fact`

```diff
@@ -4,16 +4,14 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/ocs-1-2-non-abuse-neglect-related-texas-child-fatality-investigations-fy2013-fy2022/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 7 `subquestion`
  - copy: `What was the 2021 model-based drug poisoning death rate for each county in <hop 2 answer>?`
  - tasks_mini: `Among the counties from hop 2, which two had the highest model-based drug poisoning death rates in 2021? (Filter for this node: Year == 2021; State == Texas; County in {Comal County, TX, Victoria County, TX, Willacy County, TX}; use Model-based Death Rate.)`

- Node 7 `answer`
  - copy: `{"Comal County, TX": 19.21235, "Victoria County, TX": 19.51998, "Willacy County, TX": 10.24776}`
  - tasks_mini: `["Victoria County", "Comal County"]`

- Node 7 `fact`

```diff
@@ -4,19 +4,16 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/nchs-drug-poisoning-mortality-by-county-united-states/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 8 `subquestion`
  - copy: `What was the 2016 estimated age-adjusted drug poisoning death rate category for each county in <hop 2 answer>?`
  - tasks_mini: `Among the counties from hop 2, which two had the lowest age-adjusted drug poisoning death rate categories in 2016? (Filter for this node: Year == 2016; State == Texas; County in {Comal County, TX, Victoria County, TX, Willacy County, TX}; use Estimated Age-adjusted Death Rate, 16 Categories (in ranges).)`

- Node 8 `answer`
  - copy: `{"Comal County, TX": "14-15.9", "Victoria County, TX": "10-11.9", "Willacy County, TX": "6-7.9"}`
  - tasks_mini: `["Willacy County", "Victoria County"]`

- Node 8 `fact`

```diff
@@ -4,19 +4,17 @@
-from botocore.config import Config
+from botocore.client import Config
-source = "datagov/nchs-drug-poisoning-mortality-by-county-united-states-20278/files/rows.txt"
-bucket = "lakeqa-yc4103-datalake"
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
```

- Node 9 `subquestion`
  - copy: `What is the county seat of <hop 3 answer>?`
  - tasks_mini: `What is the county seat of the county identified in hop 3? (Lookup: county seat statement in the Victoria County, Texas article.)`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-Its county seat is also named Victoria.
+Victoria County's county seat is Victoria.
```

- Node 10 `subquestion`
  - copy: `What river does <hop 4 answer> lie along and just to the east of?`
  - tasks_mini: `What river does the city from hop 4 lie along and just to the east of? (Lookup: Victoria, Texas article location description.)`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-It lies along and just to the east of the Guadalupe River.
+Victoria lies along and just to the east of the Guadalupe River.
```

### `k-5-d-4/task_6.json`
- Impact: major
- Node 1 `answer`
  - copy: `["Brownsville", "Pharr", "El Paso", "Laredo", "McAllen", "Mission", "Beaumont", "San Antonio", "Corpus Christi", "Edinburg"]`
  - tasks_mini: `["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "McAllen", "Mission", "Pharr", "San Antonio"]`

- Node 1 `fact`

```diff
@@ -3,18 +3,15 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `answer`
  - copy: `["Pharr", "Brownsville", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus Christi", "Houston", "Baytown", "Edinburg", "San Antonio"]`
  - tasks_mini: `["Baytown", "Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Houston", "Laredo", "McAllen", "Mission", "Pharr", "San Antonio"]`

- Node 2 `fact`

```diff
@@ -3,18 +3,15 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `answer`
  - copy: `["Brownsville", "Laredo", "Corpus Christi", "El Paso", "Pharr", "Beaumont", "McAllen", "San Antonio", "Mission", "Longview", "Houston", "Tyler"]`
  - tasks_mini: `["Beaumont", "Brownsville", "Corpus Christi", "El Paso", "Houston", "Laredo", "Longview", "McAllen", "Mission", "Pharr", "San Antonio", "Tyler"]`

- Node 3 `fact`

```diff
@@ -3,18 +3,15 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `answer`
  - copy: `["Brownsville", "Pharr", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus Christi", "Edinburg", "San Antonio", "Longview", "Tyler", "Waco"]`
  - tasks_mini: `["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "Longview", "McAllen", "Mission", "Pharr", "San Antonio", "Tyler", "Waco"]`

- Node 4 `fact`

```diff
@@ -3,18 +3,15 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 5 `subquestion`
  - copy: `Which cities from <hop 1 answer> had population under 100,000 in the 2020 Census?`
  - tasks_mini: `Which cities from <intersection of nodes 1-4: Beaumont, Brownsville, Corpus Christi, El Paso, Laredo, McAllen, Mission, Pharr, San Antonio> had population under 100,000 in the 2020 Census?`

- Node 5 `answer`
  - copy: `["Pharr", "Mission"]`
  - tasks_mini: `["Mission", "Pharr"]`

- Node 5 `fact`

```diff
@@ -3,10 +3,8 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
-df = pd.read_csv(io.BytesIO(obj["Body"].read()), low_memory=False)
-
```

- Node 6 `subquestion`
  - copy: `Which cities border Pharr from <hop 2 answer>?`
  - tasks_mini: `Which cities border <city from node 5: Pharr>?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-It is bordered to the west by the city of McAllen, to the north by Edinburg, the county seat, to the east by San Juan, and to the southwest by Hidalgo.
+According to the Wikipedia article for Pharr, Texas, the city 'borders McAllen to the west, Edinburg to the north, San Juan to the east, and Hidalgo to the southwest.'
```

- Node 7 `subquestion`
  - copy: `Which cities border Mission from <hop 2 answer>?`
  - tasks_mini: `Which cities border <city from node 5: Mission>?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Mission is in southern Hidalgo County. It is bordered to the east by McAllen, the largest city in the county, to the north by Palmhurst, to the west by Palmview, and to the south by the Mexico–United States border along the Rio Grande.
+According to the Wikipedia article for Mission, Texas, the city borders 'McAllen to the east, Palmhurst to the north, and Palmview to the west.'
```

- Node 8 `subquestion`
  - copy: `Which Texas county is <hop 3 answer> located in?`
  - tasks_mini: `Which Texas county is <intersection of nodes 6-7: McAllen> located in?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-McAllen is a city in the U.S. state of Texas and the most populous city in Hidalgo County.
+According to the Wikipedia article for McAllen, Texas: 'McAllen is a city in Hidalgo County in the Rio Grande Valley of the southern tip of the U.S. state of Texas.' McAllen is the most populous city in Hidalgo County, though the county seat is Edinburg.
```

- Node 9 `subquestion`
  - copy: `What percentage of the population was aged 65 and older in 2022 in <hop 4 answer>?`
  - tasks_mini: `What percentage of the population was aged 65 and older in 2022 in <county from node 8: Hidalgo County>?`

- Node 9 `answer`
  - copy: `12.3`
  - tasks_mini: `12.3`

- Node 9 `fact`

```diff
@@ -5,2 +5,3 @@
+
@@ -10,10 +11,7 @@
-result = (
-    df.loc[
-        (df["County"] == "Hidalgo")
-        & (pd.to_numeric(df["Fiscal Year"], errors="coerce") == 2022),
-        ["County", "Fiscal Year", "65 and older: % of Population"]
```

### `k-5-d-4/task_7.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Washington school districts had at least 68% English language arts performance for all students and all grades in 2014-15?`
  - tasks_mini: `Which Washington school districts had ELA performance >= 68% for All Students, All Grades from 2014-15 to 2017-18? (Filter: OrganizationLevel=District; TestSubject=ELA; StudentGroup=All Students; GradeLevel=All Grades; PercentMetStandard>=68.)`

- Node 1 `answer`
  - copy: `["Blaine School District (Whatcom)", "Camas School District (Clark)", "Carbonado School District (Pierce)", "Chehalis School District (Lewis)", "Colfax School District (Whitman)", "Damman School District (Kittitas)", "Deer Park School District (Spokane)", "Dieringer School District (Pierce)", "Freeman School District (Spokane)", "Griffin School District (Th...`
  - tasks_mini: `["Riverside School District (Spokane)", "Index Elementary School District 63 (Snohomish)", "Port Townsend School District (Jefferson)", "Woodland School District (Cowlitz)", "Deer Park School District (Spokane)", "Damman School District (Kittitas)", "Camas School District (Clark)", "Lake Washington School District (King)", "Blaine School District (Whatcom)"...`

- Node 1 `fact`

```diff
@@ -3,7 +3,10 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 2 `subquestion`
  - copy: `Which Washington school districts had at least 68% English language arts performance for all students and all grades in 2015-16?`
  - tasks_mini: `Which Washington school districts had ELA performance >= 68% for All Students, All Grades from 2014-15 to 2017-18? (Filter: OrganizationLevel=District; TestSubject=ELA; StudentGroup=All Students; GradeLevel=All Grades; PercentMetStandard>=68.)`

- Node 2 `answer`
  - copy: `["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island School District (Kitsap)", "Bainbridge Island School District (Kitsap)", "Bellevue School District (King)", "Bellingham School District (Whatcom)", "Blaine School District (Whatcom)", "Camas School District (Clark)", "Carbonado School District (Pierce)", "Central K...`
  - tasks_mini: `["Edmonds School District (Snohomish)", "Fife School District (Pierce)", "West Valley School District (Spokane) (Spokane)", "Bainbridge Island School District (Kitsap)", "Sedro-Woolley School District (Skagit)", "Walla Walla Public Schools (Walla Walla)", "Enumclaw School District (King)", "Hockinson School District (Clark)", "Snohomish School District (Sno...`

- Node 2 `fact`

```diff
@@ -3,7 +3,10 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 3 `subquestion`
  - copy: `Which Washington school districts had at least 68% English language arts performance for all students and all grades in 2016-17?`
  - tasks_mini: `Which Washington school districts had ELA performance >= 68% for All Students, All Grades from 2014-15 to 2017-18? (Filter: OrganizationLevel=District; TestSubject=ELA; StudentGroup=All Students; GradeLevel=All Grades; PercentMetStandard>=68.)`

- Node 3 `answer`
  - copy: `["Adna School District (Lewis)", "Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island School District (Kitsap)", "Bainbridge Island School District (Kitsap)", "Bellevue School District (King)", "Bickleton School District (Klickitat)", "Camas School District (Clark)", "Carbonado School District (Pierce)", "Central Kits...`
  - tasks_mini: `["Enumclaw School District (King)", "Snohomish School District (Snohomish)", "Centralia School District (Lewis)", "Mercer Island School District (King)", "Prosser School District (Benton)", "Mercer Island School District (King)", "East Valley School District (Spokane) (Spokane)", "Clover Park School District (Pierce)", "Clarkston School District (Asotin)", ...`

- Node 3 `fact`

```diff
@@ -3,7 +3,10 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 4 `subquestion`
  - copy: `Which Washington school districts had at least 68% English language arts performance for all students and all grades in 2017-18?`
  - tasks_mini: `Which Washington school districts had ELA performance >= 68% for All Students, All Grades from 2014-15 to 2017-18? (Filter: OrganizationLevel=District; TestSubject=ELA; StudentGroup=All Students; GradeLevel=All Grades; PercentMetStandard>=68.)`

- Node 4 `answer`
  - copy: `["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island School District (Kitsap)", "Bellevue School District (King)", "Blaine School District (Whatcom)", "Camas School District (Clark)", "Carbonado School District (Pierce)", "Central Kitsap School District (Kitsap)", "Centralia School District (Lewis)", "Colfax School D...`
  - tasks_mini: `["University Place School District (Pierce)", "Enumclaw School District (King)", "Mercer Island School District (King)", "Bainbridge Island School District (Kitsap)", "Lake Washington School District (King)", "Camas School District (Clark)", "Sunnyside School District (Yakima)", "Colfax School District (Whitman)", "Issaquah School District (King)", "Blaine ...`

- Node 4 `fact`

```diff
@@ -3,7 +3,10 @@
+from botocore.config import Config
-from botocore.config import Config
+
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 5 `subquestion`
  - copy: `Among the counties represented by districts in <hop 1 answer>, which are in Eastern Washington?`
  - tasks_mini: `Among counties from <hop 1 answer: King, Clark, Pierce, Whitman, Thurston, Spokane>, which are in Eastern Washington?`

- Node 5 `answer`
  - copy: `["Whitman", "Spokane"]`
  - tasks_mini: `Whitman and Spokane`

- Node 5 `fact`

```diff
@@ -1,20 +1 @@
- Adams
- Asotin
- Benton
- Chelan
- Columbia
- Douglas
```

- Node 6 `subquestion`
  - copy: `Among the counties in <hop 2 answer>, which county borders Idaho and had a 2020 population under 300,000?`
  - tasks_mini: `Among counties from <hop 2 answer: Whitman, Spokane>, which county borders Idaho AND has 2020 census population under 300,000?`

- Node 6 `fact`

```diff
@@ -1,33 +1 @@
-Adjacent counties
-
-Spokane County - north
-Benewah County, Idaho - northeast
-Latah County, Idaho - east
-Nez Perce County, Idaho - southeast
```

- Node 7 `subquestion`
  - copy: `Among the counties in <hop 2 answer>, which county borders Idaho and had a 2020 population under 300,000?`
  - tasks_mini: `Among counties from <hop 2 answer: Whitman, Spokane>, which county borders Idaho AND has 2020 census population under 300,000?`

- Node 7 `fact`

```diff
@@ -1,15 +1 @@
-Adjacent counties
-
-Stevens County - north
-Pend Oreille County - north/northeast
-Bonner County, Idaho - northeast
-Kootenai County, Idaho - east
```

- Node 8 `subquestion`
  - copy: `What is the most populous city in <hop 3 answer> according to the 2020 census?`
  - tasks_mini: `What is the most populous city in <hop 3 answer: Whitman County> according to the 2020 census, located in southeastern Washington within the Palouse region of the Pacific Northwest?`

- Node 8 `answer`
  - copy: `Pullman`
  - tasks_mini: `Pullman is the most populous city in Whitman County (2020 census), located in southeastern Washington within the Palouse region of the Pacific Northwest`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Pullman is the most populous city in Whitman County, located in southeastern Washington within the Palouse region of the Pacific Northwest. The population was 32,901 at the 2020 census
+According to the Wikipedia article for Pullman, Washington, Pullman is the most populous city in Whitman County as of the 2020 census and is located in southeastern Washington within the Palouse region of the Pacific Northwest.
```

- Node 9 `subquestion`
  - copy: `What is the 2017-18 total student enrollment for the school district in <hop 4 answer>?`
  - tasks_mini: `What is the 2017-18 total student enrollment for the school district in <hop 4 answer: Pullman>? (Filter: OrganizationLevel=District; DistrictName=Pullman School District; GradeLevel=All Grades; column=All Students.)`

- Node 9 `answer`
  - copy: `2941`
  - tasks_mini: `2941`

- Node 9 `fact`

```diff
@@ -5,2 +5,3 @@
+
@@ -11,6 +12,8 @@
-    (df["OrganizationLevel"] == "District")
+    (df["SchoolYear"] == "2017-18")
+    & (df["OrganizationLevel"] == "District")
-][["DistrictName", "County", "GradeLevel", "All Students"]].reset_index(drop=True)
+]
```

### `k-5-d-4/task_8.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Texas counties had between 700 and 4,600 TDCJ criminal intakes in FY 2019? Keep the full set of qualifying counties (with their FY2019 intake counts) for later intersection across FY 2019-2022.`
  - tasks_mini: `Which Texas counties had TDCJ criminal intakes between 700-4,600 in each fiscal year from FY 2019-2022? (Filter: group by County; count rows; keep 700 <= count <= 4600.)`

- Node 1 `answer`
  - copy: `["Bexar", "Hidalgo", "Travis", "El Paso", "Montgomery", "McLennan", "Collin", "Smith", "Galveston", "Jefferson"]`
  - tasks_mini: `["Bexar", "El Paso", "Hidalgo", "Montgomery", "Travis", "McLennan", "Collin", "Smith", "Galveston", "Jefferson", "Taylor", "Nueces", "Brazoria", "Ector", "Johnson", "Bell", "Lubbock", "Denton"]`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -14,14 +14,15 @@
-    .reset_index(name="intake_count")
+    .reset_index(name="receive_count")
-
-result = (
-    county_counts[
-        county_counts["County"].notna()
```

- Node 2 `subquestion`
  - copy: `Which Texas counties had between 700 and 4,600 TDCJ criminal intakes in FY 2020? Keep the full set of qualifying counties (with their FY2020 intake counts) for later intersection across FY 2019-2022.`
  - tasks_mini: `Which Texas counties had TDCJ criminal intakes between 700-4,600 in each fiscal year from FY 2019-2022? (Filter: group by County; count rows; keep 700 <= count <= 4600.)`

- Node 2 `fact`

```diff
@@ -3,4 +3,4 @@
+from botocore.config import Config
-from botocore.config import Config
@@ -8,20 +8,9 @@
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
+obj = s3.get_object(Bucket=bucket, Key=source)
```

- Node 3 `subquestion`
  - copy: `Which Texas counties had between 700 and 4,600 TDCJ criminal intakes in FY 2021? Keep the full set of qualifying counties (with their FY2021 intake counts) for later intersection across FY 2019-2022.`
  - tasks_mini: `Which Texas counties had TDCJ criminal intakes between 700-4,600 in each fiscal year from FY 2019-2022? (Filter: group by County; count rows; keep 700 <= count <= 4600.)`

- Node 3 `fact`

```diff
@@ -3,4 +3,4 @@
+from botocore.config import Config
-from botocore.config import Config
@@ -8,20 +8,9 @@
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
+obj = s3.get_object(Bucket=bucket, Key=source)
```

- Node 4 `subquestion`
  - copy: `Which Texas counties had between 700 and 4,600 TDCJ criminal intakes in FY 2022? Keep the full set of qualifying counties (with their FY2022 intake counts) for later intersection across FY 2019-2022.`
  - tasks_mini: `Which Texas counties had TDCJ criminal intakes between 700-4,600 in each fiscal year from FY 2019-2022? (Filter: group by County; count rows; keep 700 <= count <= 4600.)`

- Node 4 `answer`
  - copy: `["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "McLennan", "El Paso"]`
  - tasks_mini: `["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "McLennan", "El Paso", "Johnson"]`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -3,4 +3,4 @@
+from botocore.config import Config
-from botocore.config import Config
@@ -8,20 +8,9 @@
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
+obj = s3.get_object(Bucket=bucket, Key=source)
```

- Node 5 `subquestion`
  - copy: `Among <hop 1 answer>, which Texas counties have 2020 census population under 900,000?`
  - tasks_mini: `Among <hop 1 answer: Bexar, El Paso, Hidalgo, Montgomery>, which counties have 2020 census population under 900,000? (Filter: SUMLEV=50; BASENAME in {Bexar, El Paso, Hidalgo, Montgomery}; POP100 < 900000.)`

- Node 5 `answer`
  - copy: `["Hidalgo", "El Paso", "Montgomery"]`
  - tasks_mini: `["El Paso", "Hidalgo", "Montgomery"]`

- Node 5 `fact`

```diff
@@ -3,4 +3,4 @@
+from botocore.config import Config
-from botocore.config import Config
@@ -8,17 +8,15 @@
-obj = boto3.client("s3", config=Config(signature_version=UNSIGNED)).get_object(Bucket=bucket, Key=source)
+candidates = ["Bexar", "El Paso", "Hidalgo", "Montgomery"]
+
+s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
```

- Node 6 `subquestion`
  - copy: `Which county in <hop 2 answer> is part of the Houston metropolitan area?`
  - tasks_mini: `Among <hop 2 answer: El Paso, Hidalgo, Montgomery>, which counties are NOT in the Houston metropolitan area?`

- Node 6 `answer`
  - copy: `Montgomery`
  - tasks_mini: `["El Paso", "Hidalgo"]`

- Node 7 `subquestion`
  - copy: `Among the counties remaining after removing <node 6 answer> from <hop 2 answer>, which county is in West Texas?`
  - tasks_mini: `Among <hop 2 answer: El Paso, Hidalgo>, which county is in West Texas?`

- Node 7 `answer`
  - copy: `El Paso`
  - tasks_mini: `El Paso County is in West Texas`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-counties of West Texas are Andrews, Bailey, Borden, Brewster, Brown, Callahan, Cochran, Coke, Coleman, Comanche, Concho, Crane, Crockett, Crosby, Culberson, Dawson, Dickens, Eastland, Ector, El Paso, Fisher, Floyd, Gaines, Garza, Glasscock, Hale, Haskell, Hockley, Howard, Hudspeth, Irion, Jeff Davis
+According to the Wikipedia article for West Texas, the list of West Texas counties includes El Paso.
```

- Node 8 `subquestion`
  - copy: `What is the county seat of the county from <hop 2 answer> that is in South Texas rather than West Texas?`
  - tasks_mini: `Among <hop 2 answer: El Paso, Hidalgo>, which county is located in South Texas (not West Texas)?`

- Node 8 `answer`
  - copy: `Edinburg`
  - tasks_mini: `Hidalgo County is in South Texas, county seat is Edinburg`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-The county seat is Edinburg and the largest city is McAllen. The county is named for Miguel Hidalgo y Costilla, the priest who raised the call for Mexico's independence from Spain.  It is located in the Rio Grande Valley of South Texas
+According to the Wikipedia article for Hidalgo County, Texas, 'It is located in the Rio Grande Valley of South Texas.' The county seat is Edinburg.
```

- Node 9 `subquestion`
  - copy: `What is the University of Texas System university with its main campus in <hop 3 answer>?`
  - tasks_mini: `What is the UT System university with its main campus in <hop 3 answer: Edinburg>?`

- Node 9 `answer`
  - copy: `University of Texas Rio Grande Valley`
  - tasks_mini: `University of Texas Rio Grande Valley (UTRGV)`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The University of Texas Rio Grande Valley (UTRGV) is a public research university with its main campus in Edinburg, Texas, United States, and multiple other campuses throughout the Rio Grande Valley. It is the southernmost member of the University of Texas System.
+According to the Wikipedia article for University of Texas Rio Grande Valley, UTRGV is a public research university with its main campus in Edinburg, Texas, and it is the southernmost member of the University of Texas System.
```

- Node 10 `subquestion`
  - copy: `What was the Fall 2024 total student enrollment at <hop 4 answer>?`
  - tasks_mini: `What was the Fall 2024 total student enrollment at <hop 4 answer: UTRGV>?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-In the fall of 2024, the University of Texas Rio Grande Valley enrolled 33,881 students
+According to the Wikipedia article for University of Texas Rio Grande Valley, 'In the fall of 2024, the University of Texas Rio Grande Valley enrolled 33,881 students.'
```

### `k-5-d-4/task_9.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the FY2019 state prison release counts for every county in the FY2019 TDCJ releases dataset, with County normalized to uppercase, so hop-level reasoning can compute the top five counties by average releases across FY2019-FY2022 and then read this year's counts for those counties?`
  - tasks_mini: `For FY2019, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2019 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 2 `subquestion`
  - copy: `What are the FY2020 state prison release counts for every county in the FY2020 TDCJ releases dataset, with County normalized to uppercase, so hop-level reasoning can compute the top five counties by average releases across FY2019-FY2022 and then read this year's counts for those counties?`
  - tasks_mini: `For FY2020, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2020 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 3 `subquestion`
  - copy: `What are the FY2021 state prison release counts for every county in the FY2021 TDCJ releases dataset, with County normalized to uppercase, so hop-level reasoning can compute the top five counties by average releases across FY2019-FY2022 and then read this year's counts for those counties?`
  - tasks_mini: `For FY2021, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2021 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 4 `subquestion`
  - copy: `What are the FY2022 state prison release counts for every county in the FY2022 TDCJ releases dataset, with County normalized to uppercase, so hop-level reasoning can compute the top five counties by average releases across FY2019-FY2022 and then read this year's counts for those counties?`
  - tasks_mini: `For FY2022, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2022 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 5 `subquestion`
  - copy: `What is the county seat of <hop 1 answer>?`
  - tasks_mini: `What is the county seat of <county from aggregation of nodes 1-4: Bexar County>? (Lookup: find the county seat statement in the Bexar County, Texas article.)`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Bexar County (  or  ;  ) is a county in the U.S. state of Texas. It is in South Texas and its county seat is San Antonio.
+According to the Wikipedia article for Bexar County, Texas, 'Its county seat is San Antonio.'
```

- Node 6 `subquestion`
  - copy: `Which NBA champion team is based in <node 5 answer>?`
  - tasks_mini: `What five-time NBA champion team is based in <city from node 5: San Antonio>? (Lookup: find the sentence naming the five-time NBA champion team in the San Antonio article.)`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The city also hosts the San Antonio Stock Show & Rodeo and is home to the five-time NBA champion San Antonio Spurs.
+According to the Wikipedia article for San Antonio, 'San Antonio is also home to the five-time NBA champion San Antonio Spurs.'
```

- Node 7 `subquestion`
  - copy: `Which team did <node 6 answer> defeat in its first NBA Finals championship?`
  - tasks_mini: `Which team did <team from node 6: San Antonio Spurs> defeat in their first NBA Finals championship? (Lookup: Spurs article; first championship opponent.)`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-In the NBA Finals, they faced the New York Knicks, who had made history by becoming the first eighth seed to ever make the NBA Finals. The Spurs won the series 4-1 and the franchise's first NBA Championship in Game 5 at the Knicks' home arena, Madison Square Garden.
+According to the Wikipedia article for San Antonio Spurs. For their first championship in 1999, the article states they 'defeated the New York Knicks' in the NBA Finals.
```

- Node 8 `subquestion`
  - copy: `In which New York City borough is <node 7 answer> based?`
  - tasks_mini: `In which New York City borough is <team from node 7: New York Knicks> based? (Lookup: Knicks article; borough of Manhattan.)`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-The New York Knickerbockers, shortened and more commonly referred to as the New York Knicks, are an American professional basketball team based in the New York City borough of Manhattan.
+According to the Wikipedia article for New York Knicks, 'The New York Knickerbockers, commonly known as the New York Knicks, are an American professional basketball team based in the New York City borough of Manhattan.'
```

### `k-6-d-2/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which NYC high schools received an overall A rating and were also given an A for student graduation and diploma outcomes in 2010-11?`
  - tasks_mini: `Which NYC high school DBNs had 'A' Progress Report AND 'A' Performance Grade in 2010-11?`

- Node 1 `answer`
  - copy: `["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414", "02M416"]`
  - tasks_mini: `["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414", "02M416", "02M418", "02M439", "02M475", "02M545", "02M600", "03M307", "03M485", "03M492", "04M435", "04M610", "05M670", "05M692", "06M467", "07X221", "07X334", "07X548", "07X551", "09X241", "09X543", "10X141", "10X374", "10X434", "10X437", "10X445", "10X477", "10X549"...`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `subquestion`
  - copy: `Which NYC high schools received an overall A rating in 2011-12?`
  - tasks_mini: `Which NYC high school DBNs had 'A' Progress Report Grade in 2011-12?`

- Node 2 `answer`
  - copy: `["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407", "02M411"]`
  - tasks_mini: `["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407", "02M411", "02M412", "02M413", "02M414", "02M416", "02M418", "02M439", "02M449", "02M459", "02M475", "02M500", "02M519", "02M531", "02M542", "02M543", "02M545", "02M551", "02M600", "03M479", "03M485", "03M492", "03M541", "03M860", "04M555", "04M610", "05M692", "06M293"...`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `subquestion`
  - copy: `Which NYC high schools had the percentage of students considered prepared for college or careers between 98-99% in both 2012 and 2013, with a 2013 graduation rate below 100%?`
  - tasks_mini: `Which of <intersection of nodes 1-2> had college_career_rate_2012 and college_career_rate_2013 between 98-99% (not 100%) and graduation_rate_2013 below 100%?`

- Node 3 `answer`
  - copy: `02M475`
  - tasks_mini: `["02M475"]`

- Node 3 `fact`

```diff
@@ -11,2 +11,6 @@
+node_1_answer = ['01M450', '01M539', '02M288', '02M296', '02M298', '02M308', '02M411', '02M412', '02M414', '02M416', '02M418', '02M439', '02M475', '02M545', '02M600', '03M307', '03M485', '03M492', '04M435', '04M610', '05M670', '05M692', '06M467', '07X221', '07X334', '07X548', '07X551', '09X241', '09X543', '10X141', '10X374', '10X434', '10X437', '10X445', '10X477', '10X549', '10X696', '11X249', '11X275', '11X544', '12X248', '12X267', '12X682', '13K419', '13K439', '13K595', '14K478', '14K558', '14K561', '15K448', '17K539', '17K546', '18K563', '18K567', '18K576', '19K404', '20K485', '22K555', '23K514', '23K697', '24Q264', '24Q530', '24Q610', '25Q285', '25Q525', '27Q262', '27Q323', '27Q650', '28Q620', '28Q687', '29Q248', '30Q555', '31R047', '31R080', '31R605', '32K403', '32K554']
+node_2_answer = ['01M450', '01M539', '02M288', '02M296', '02M298', '02M303', '02M305', '02M308', '02M407', '02M411', '02M412', '02M413', '02M414', '02M416', '02M418', '02M439', '02M449', '02M459', '02M475', '02M500', '02M519', '02M531', '02M542', '02M543', '02M545', '02M551', '02M600', '03M479', '03M485', '03M492', '03M541', '03M860', '04M555', '04M610', '05M692', '06M293', '06M348', '06...
```

- Node 4 `subquestion`
  - copy: `What is the name of the NYC high school with DBN <hop 1 answer>?`
  - tasks_mini: `What is the school name for <node_3 answer> (DBN) in the 2011-2012 high school progress report?`

- Node 5 `subquestion`
  - copy: `After whom is <hop 2 answer> named?`
  - tasks_mini: `After whom is <node_4 answer> named?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-the new school would be "designated as the Stuyvesant High School, as being reminiscent of the locality". Stuyvesant Square, Stuyvesant Street, and later Stuyvesant Town (which was built in 1947) are all near the proposed 15th Street school building. All these locations were named after Peter Stuyvesant
+Stuyvesant High School is a specialized high school in Manhattan named after Peter Stuyvesant, the last Dutch Director of New Netherland.
```

- Node 6 `subquestion`
  - copy: `Which university did <hop 3 answer> study at?`
  - tasks_mini: `Where did <node_5 answer> study?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-At the age of 20, Stuyvesant went to the University of Franeker, where he studied languages and philosophy
+Peter Stuyvesant (c. 1610-1672) was a Dutch colonial administrator who served as the director-general of New Netherland. At the age of 20, Stuyvesant went to the University of Franeker, where he studied languages and philosophy.
```

- Node 7 `subquestion`
  - copy: `In what year was <hop 4 answer> founded?`
  - tasks_mini: `In what year was <node_6 answer> founded?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-The University of Franeker (1585–1811) was a university in Franeker, Friesland, the Netherlands.
+The University of Franeker (1585-1811) was a university in Franeker, Friesland, the Netherlands. It was the second-oldest university of the Netherlands, founded shortly after Leiden University.
```

### `k-6-d-2/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the 2019 violent crime counts by ward for offenses in {HOMICIDE, ASSAULT W/DANGEROUS WEAPON, ROBBERY, SEX ABUSE}, so they can be combined with 2020 to identify the top two wards by average violent crimes?`
  - tasks_mini: `Which DC wards had the top 2 average violent crimes between 2019 and 2020? (Filter for this node: OFFENSE in {HOMICIDE, ASSAULT W/DANGEROUS WEAPON, ROBBERY, SEX ABUSE}; group by WARD; count records; rank by count; keep top 2.)`

- Node 1 `limit`
  - copy: `2`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -6,2 +6,3 @@
+
@@ -9,3 +10,3 @@
-data = json.loads(obj["Body"].read())
+data = json.load(io.BytesIO(obj["Body"].read()))
@@ -21,5 +22,5 @@
-    .sort_values(["violent_crime_count", "properties.WARD"], ascending=[False, True])
-    .reset_index(drop=True)
-answer = [f"Ward {int(row['properties.WARD'])} ({row['violent_crime_count']})" for _, row in result.iterrows()]
```

- Node 2 `subquestion`
  - copy: `What are the 2020 violent crime counts by ward for offenses in {HOMICIDE, ASSAULT W/DANGEROUS WEAPON, ROBBERY, SEX ABUSE}, so they can be combined with 2019 to identify the top two wards by average violent crimes?`
  - tasks_mini: `Which DC wards had the top 2 average violent crimes between 2019 and 2020? (Filter for this node: OFFENSE in {HOMICIDE, ASSAULT W/DANGEROUS WEAPON, ROBBERY, SEX ABUSE}; group by WARD; count records; rank by count; keep top 2.)`

- Node 2 `limit`
  - copy: `2`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -6,2 +6,3 @@
+
@@ -9,3 +10,3 @@
-data = json.loads(obj["Body"].read())
+data = json.load(io.BytesIO(obj["Body"].read()))
@@ -21,5 +22,5 @@
-    .sort_values(["violent_crime_count", "properties.WARD"], ascending=[False, True])
-    .reset_index(drop=True)
-answer = [f"Ward {int(row['properties.WARD'])} ({row['violent_crime_count']})" for _, row in result.iterrows()]
```

- Node 3 `subquestion`
  - copy: `What are the 2019 311 service request counts for the wards in <hop 1 answer>, so they can be averaged with 2020 to determine which ward had the higher average 311 request volume?`
  - tasks_mini: `Between the top 2 crime wards (from hop 1), which had higher average 311 service requests (2019-2020)? (Filter for this node: WARD in {7, 8}; group by WARD; count records.)`

- Node 3 `limit`
  - copy: `2`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -2,3 +2,3 @@
-import pandas as pd
+from collections import Counter
@@ -6,2 +6,3 @@
+
@@ -9,13 +10,11 @@
-data = json.loads(obj["Body"].read())
-df = pd.json_normalize(data["features"])
+data = json.load(io.BytesIO(obj["Body"].read()))
```

- Node 4 `subquestion`
  - copy: `What are the 2020 311 service request counts for the wards in <hop 1 answer>, so they can be averaged with 2019 to determine which ward had the higher average 311 request volume?`
  - tasks_mini: `Between the top 2 crime wards (from hop 1), which had higher average 311 service requests (2019-2020)? (Filter for this node: WARD in {7, 8}; group by WARD; count records.)`

- Node 4 `answer`
  - copy: `["Ward 8 (37,124)", "Ward 7 (36,113)"]`
  - tasks_mini: `["Ward 7 (36,113)", "Ward 8 (37,124)"]`

- Node 4 `limit`
  - copy: `2`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -2,3 +2,3 @@
-import pandas as pd
+from collections import Counter
@@ -6,2 +6,3 @@
+
@@ -9,13 +10,11 @@
-data = json.loads(obj["Body"].read())
-df = pd.json_normalize(data["features"])
+data = json.load(io.BytesIO(obj["Body"].read()))
```

- Node 5 `subquestion`
  - copy: `Who is the DC Council member for <hop 2 answer>?`
  - tasks_mini: `Who represents the selected ward (from hop 2) on the DC Council?`

- Node 5 `fact`

```diff
@@ -1,2 +1 @@
-Ward 7 Councilmember: Wendell Felder
-Population (2022): 77,456
+Ward 7 Councilmember: Wendell Felder. Ward 7 has a population of 77,456 (2022).
```

- Node 6 `subquestion`
  - copy: `Which university did <hop 3 answer> attend for graduate studies?`
  - tasks_mini: `Which university did the council member (from hop 3) attend for graduate studies?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-Felder went on to receive a B.S. from Bowie State University and a M.A. from Georgetown University.
+Wendell Felder received a B.S. from Bowie State University and a M.A. from Georgetown University.
```

- Node 7 `subquestion`
  - copy: `Who founded <hop 4 answer>?`
  - tasks_mini: `Who founded the university (from hop 4), and who is its flagship building (a National Historic Landmark) named after?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Founded by Bishop John Carroll in 1789, it is the oldest Catholic institution of higher education in the United States, the oldest university in Washington, D.C., and the nation's first federally chartered university.
+Georgetown University was founded by Bishop John Carroll in 1789. It is the oldest Catholic institution of higher education in the United States.
```

- Node 8 `subquestion`
  - copy: `After whom is Healy Hall, the flagship building of <hop 4 answer> and a National Historic Landmark, named?`
  - tasks_mini: `Who founded the university (from hop 4), and who is its flagship building (a National Historic Landmark) named after?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Enrollment did not recover until the late 19th century, during the presidency of Patrick Francis Healy from 1873 to 1881. Born in Athens, Georgia as a slave by law and mixed-race by ancestry, Healy was the first person of African descent to head a predominantly white American university. He identified as Irish Catholic, like his father, and was educated in Catholic schools in the United States and France. He is credited with reforming the undergraduate curriculum, lengthening the medical and law programs, and creating the Alumni Association. One of his largest undertakings was the construction of a major new building, subsequently named Healy Hall in his honor.
+Healy Hall is the flagship building of Georgetown University and a National Historic Landmark. The structure is named after Patrick Francis Healy, who was the President of Georgetown University at the time of its construction.
```

- Node 9 `subquestion`
  - copy: `What birth year does <node 7 answer> have for the final comparison against <node 8 answer>?`
  - tasks_mini: `In what year was the earlier-born of the two figures (from hop 5) born?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-John Carroll  (January 8, 1735 – December 3, 1815) was an American Catholic prelate who served as the first Bishop of Baltimore, then the only diocese in the nascent United States, from 1789 to 1815.
+John Carroll (January 8, 1735 - December 3, 1815) was an American Catholic prelate who served as the first Bishop of Baltimore and founded Georgetown University.
```

- Node 10 `subquestion`
  - copy: `What birth year does <node 8 answer> have for the final comparison against <node 7 answer>?`
  - tasks_mini: `In what year was the earlier-born of the two figures (from hop 5) born?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-Patrick Francis Healy  (February 27, 1834January 10, 1910) was an American Catholic priest and Jesuit who was an influential president of Georgetown University, becoming known as its "second founder".
+Patrick Francis Healy (February 27, 1834 - January 10, 1910) was an American Catholic priest and Jesuit who was an influential president of Georgetown University. The university's flagship building, Healy Hall, bears his name.
```

### `k-6-d-2/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which non-NYC New York counties have the highest total mental health service recipients across service years 2017 and 2018, keeping county-level totals so the top two can be identified?`
  - tasks_mini: `Which non-NYC NY counties are in the top 2 by total mental health service recipients (2017-2018)? (Filter for this node: Service Year in {2017, 2018}; group by County Label; sum Count of Recipients by Rate Code Group and County; exclude NYC counties {Bronx, Kings, New York, Queens, Richmond}; rank by total; keep top 2.)`

- Node 1 `answer`
  - copy: `["Erie", "Monroe"]`
  - tasks_mini: `["Erie County", "Monroe County"]`

- Node 1 `fact`

```diff
@@ -25,3 +25,2 @@
-answer = result.head(2)["County Label"].tolist()
-print(answer)
+answer = [f"{county} County" for county in result.head(2)["County Label"].tolist()]
```

- Node 2 `subquestion`
  - copy: `What is the county seat of Erie County, New York?`
  - tasks_mini: `What is the county seat of each county (from hop 1)?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-Erie County is a county along the shore of Lake Erie in western New York State. As of the 2020 census, the population was 954,236. However, in 2023 the estimated population was 946,147. The county seat is Buffalo, which makes up about 28% of the county's population.
+The county seat of Erie County, New York is Buffalo.
```

- Node 3 `subquestion`
  - copy: `What is the county seat of Monroe County, New York?`
  - tasks_mini: `What is the county seat of each county (from hop 1)?`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Monroe County is a county in the Finger Lakes region of the U.S. state of New York. Along the southern shore of Lake Ontario, it is east of Buffalo and northwest of Syracuse. As of the 2020 census, the population was 759,443. Its county seat is the city of Rochester.
+The county seat of Monroe County, New York is Rochester.
```

- Node 4 `subquestion`
  - copy: `In what year was Buffalo incorporated as a city?`
  - tasks_mini: `When was each county seat (from hop 2) incorporated as a city?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-Buffalo was selected as the terminus of the Erie Canal in 1825, which led to its incorporation in 1832 and stimulated its growth as the primary inland port between the Great Lakes and Atlantic Ocean.
+Buffalo was selected as the terminus of the Erie Canal in 1825, which led to its incorporation in 1832.
```

- Node 5 `subquestion`
  - copy: `In what year was Rochester rechartered as a city?`
  - tasks_mini: `When was each county seat (from hop 2) incorporated as a city?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-By 1821, Rochesterville became the seat of Monroe County.Peck, p. 59 In 1823, the Erie Canal aqueduct over the Genesee River was completed, connecting the city to the Hudson River to the east.Peck, p. 60 New commerce from the canal turned the village into America's first boomtown. By 1830, Rochester's population had grown to 9,200, page 36 and in 1834, it was rechartered as a city.
+Rochester was rechartered as a city in 1834.
```

- Node 6 `subquestion`
  - copy: `What city was at the Erie Canal terminus opposite Buffalo?`
  - tasks_mini: `What city is at the other terminus of the canal identified in hop 3 (the Erie Canal, where the older-incorporated city Buffalo is at the terminus)?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-The original canal was  long, from Albany on the Hudson to Buffalo on Lake Erie.
+The original Erie Canal was from Albany on the Hudson to Buffalo on Lake Erie, making Albany the eastern terminus.
```

- Node 7 `subquestion`
  - copy: `What county is Albany, New York in?`
  - tasks_mini: `What county is the city (from hop 4) in?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-Albany ( ) is the capital city of the U.S. state of New York, and the county seat of – and most populous city in – Albany County.
+Albany is the capital city of the U.S. state of New York, and the county seat of Albany County.
```

- Node 8 `subquestion`
  - copy: `What was the 2018 violent crime rate per 100,000 population for Albany County?`
  - tasks_mini: `What was the violent crime rate per 100,000 population in 2018 for the county (from hop 5)? (Filter for this node: County == Albany; Year == 2018; read Violent Rate.)`

- Node 8 `answer`
  - copy: `359.8`
  - tasks_mini: `359.8`

- Node 8 `fact`

```diff
@@ -12,3 +12,2 @@
-answer = result["Violent Rate"].iloc[0]
-print(answer)
+answer = str(result["Violent Rate"].iloc[0])
```

### `k-6-d-2/task_4.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What are the city-level percentages of adults age 18 and older who were obese, after accounting for differences in age, in 2014?`
  - tasks_mini: `What is the US city with the highest average age-adjusted adult obesity rate (2016-2018)? (Filter for this node: GeographicLevel == City; Measure == "Obesity among adults aged >=18 Years"; Data_Value_Type == "Age-adjusted prevalence"; rank by Data_Value; keep top 3.)`

- Node 1 `answer`
  - copy: `{"Camden, New Jersey": 42.2, "Cleveland, Ohio": 42.1, "Dayton, Ohio": 47.2, "Detroit, Michigan": 45.2, "Flint, Michigan": 42.7, "Gary, Indiana": 46.9, "Kalamazoo, Michigan": 41.2, "Macon, Georgia": 42.9, "Reading, Pennsylvania": 41.7, "Youngstown, Ohio": 43.8}`
  - tasks_mini: `{"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -11,12 +11,14 @@
-result = df[
-    (df["Year"] == 2014)
-    & (df["GeographicLevel"] == "City")
-    & (df["Measure"] == "Obesity among adults aged >=18 Years")
-    & (df["Data_Value_Type"] == "Age-adjusted prevalence")
-][["StateDesc", "CityName", "Data_Value"]].sort_values(["Data_Value", "StateDesc", "CityName"], ascending=[False, True, True]).reset_index(drop=True)
```

- Node 2 `subquestion`
  - copy: `What are the city-level percentages of adults age 18 and older who were obese, after accounting for differences in age, in 2016?`
  - tasks_mini: `What is the US city with the highest average age-adjusted adult obesity rate (2016-2018)? (Filter for this node: GeographicLevel == City; Measure == "Obesity among adults aged >=18 Years"; Data_Value_Type == "Age-adjusted prevalence"; rank by Data_Value; keep top 3.)`

- Node 2 `answer`
  - copy: `{"Brownsville, Texas": 44.4, "Camden, New Jersey": 44.1, "Dayton, Ohio": 43.5, "Detroit, Michigan": 47.4, "Flint, Michigan": 45.4, "Gary, Indiana": 49.0, "Jackson, Mississippi": 44.5, "Kansas City, Kansas": 43.8, "Macon, Georgia": 44.0, "Shreveport, Louisiana": 43.4}`
  - tasks_mini: `{"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -11,12 +11,15 @@
-result = df[
-    (df["Year"] == 2016)
-    & (df["GeographicLevel"] == "City")
-    & (df["Measure"] == "Obesity among adults aged >=18 Years")
-    & (df["Data_Value_Type"] == "Age-adjusted prevalence")
-][["StateDesc", "CityName", "Data_Value"]].sort_values(["Data_Value", "StateDesc", "CityName"], ascending=[False, True, True]).reset_index(drop=True)
```

- Node 3 `subquestion`
  - copy: `What corporation founded <hop 1 answer>?`
  - tasks_mini: `What corporation founded the highest obesity city (Gary, Indiana)?`

- Node 3 `fact`

```diff
@@ -1 +1 @@
-Gary, Indiana, was founded in 1906 by the U.S. Steel corporation as the home for its new plant, Gary Works.
+Gary, Indiana was founded in 1906 by the U.S. Steel corporation as the home for its new plant, Gary Works.
```

- Node 4 `subquestion`
  - copy: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create <node 3 answer>?`
  - tasks_mini: `Which company did J. P. Morgan merge with Federal Steel and National Steel to create U.S. Steel?`

- Node 4 `fact`

```diff
@@ -1 +1 @@
-In 1901, J. P. Morgan created U.S. Steel by merging Carnegie Steel, Federal Steel, and National Steel
+In 1901, J. P. Morgan created U.S. Steel by merging Carnegie Steel, Federal Steel, and National Steel.
```

- Node 5 `subquestion`
  - copy: `Who founded <node 4 answer>?`
  - tasks_mini: `Who founded Carnegie Steel Company?`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie
+Carnegie Steel Company was a steel-producing company primarily created by Andrew Carnegie to manage businesses at steel mills in the Pittsburgh, Pennsylvania area.
```

- Node 6 `subquestion`
  - copy: `Which city was <node 5 answer> based in?`
  - tasks_mini: `Where was Andrew Carnegie based?`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-He immigrated to what is now Pittsburgh, Pennsylvania, with his parents in 1848
+Andrew Carnegie immigrated to Pittsburgh, Pennsylvania, with his parents in 1848. He built Pittsburgh's Carnegie Steel Company, which he sold to J.P. Morgan in 1901.
```

- Node 7 `subquestion`
  - copy: `What is the total 2017 expenditure for the Police Bureau of <node 6 answer>?`
  - tasks_mini: `What was Pittsburgh's average Police Bureau expenditure in 2017-2018? (Filter for this node: Year == 2017; Type == Expenditure; Department == "PS - Police Bureau"; sum Amount.)`

- Node 7 `answer`
  - copy: `98453962.68`
  - tasks_mini: `{"2017": "$98,453,962.68"}`

- Node 7 `fact`

```diff
@@ -11,3 +11,3 @@
-answer = round(float(df[
+amount = round(float(df[
@@ -16 +16,2 @@
+answer = {"2017": f"${amount:,.2f}"}
```

- Node 8 `subquestion`
  - copy: `What is the total 2018 expenditure for the Police Bureau of <node 6 answer>?`
  - tasks_mini: `What was Pittsburgh's average Police Bureau expenditure in 2017-2018? (Filter for this node: Year == 2018; Type == Expenditure; Department == "PS - Police Bureau"; sum Amount.)`

- Node 8 `answer`
  - copy: `100261931.64`
  - tasks_mini: `{"2018": "$100,261,931.64"}`

- Node 8 `fact`

```diff
@@ -11,3 +11,3 @@
-answer = round(float(df[
+amount = round(float(df[
@@ -16 +16,2 @@
+answer = {"2018": f"${amount:,.2f}"}
```

### `k-6-d-2/task_5.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which California counties had an Area Median Income of at least $142,800 in 2022?`
  - tasks_mini: `Which counties have AMI >= 142800 in the 2022 income limits data? (Filter: AMI >= 142800; list County and AMI.)`

- Node 1 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 2 `subquestion`
  - copy: `Which California counties had an Area Median Income of at least $147,900 in 2023?`
  - tasks_mini: `Which counties have AMI >= 147900 in the 2023 income limits data? (Filter: AMI >= 147900; list County and AMI.)`

- Node 2 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 3 `subquestion`
  - copy: `Among <hop 1 answer>, which counties had a WIC average cost per family of at least $570 in 2018?`
  - tasks_mini: `Among the counties from hop 1, which have Average Cost per Family >= $570 in the 2018 WIC redemptions data? (Filter: Obligation Year and Month == 2018; Vendor County in <hop 1>; parse Average Cost per Family; keep >= 570.)`

- Node 3 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 4 `subquestion`
  - copy: `Among <hop 1 answer>, which counties had a WIC average cost per family of at least $700 in 2020?`
  - tasks_mini: `Among the counties from hop 1, which have Average Cost per Family >= $700 in the 2020 WIC redemptions data? (Filter: Obligation Year and Month == 2020; Vendor County in <hop 1>; parse Average Cost per Family; keep >= 700.)`

- Node 4 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 5 `subquestion`
  - copy: `Among <hop 2 answer>, which counties had a perioperative hemorrhage or hematoma observed rate of at least 19 in 2015?`
  - tasks_mini: `Among the counties from hop 2, which have ObsRate >= 19 for PSI 27 (Perioperative Hemorrhage or Hematoma) in 2015? (Filter: Year == 2015; PSI == 27; County in <hop 2>; read ObsRate; keep >= 19.)`

- Node 5 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 6 `subquestion`
  - copy: `Among <hop 2 answer>, which counties had a geographical shape area of at least 3 billion square meters?`
  - tasks_mini: `Among the counties from hop 2, which have Shape__Area >= 3000000000 in the California county boundaries data? (Filter: COUNTY_NAME in <hop 2>; read Shape__Area; keep >= 3000000000.)`

- Node 6 `fact`

```diff
fact changed, but no compact line diff was found
```

- Node 7 `subquestion`
  - copy: `What is the county seat of <hop 3 answer>?`
  - tasks_mini: `What is the county seat of the county identified in hop 3?`

- Node 8 `subquestion`
  - copy: `On which bay's southern shore is <hop 4 answer> located?`
  - tasks_mini: `On which bay's southern shore is the county seat from hop 4 located?`

### `k-6-d-3/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which Missouri state agencies were in the top 5 for Professional Services spending in fiscal year 2021?`
  - tasks_mini: `Which Missouri state agencies were in the top 5 for Professional Services spending every year from 2021 to 2023? (Filter for this node: Category Description == 'PROFESSIONAL SERVICES'; group by Agency Name; sum Payments Total; rank desc; take top 5.)`

- Node 2 `subquestion`
  - copy: `Which Missouri state agencies were in the top 5 for Professional Services spending in fiscal year 2022?`
  - tasks_mini: `Which Missouri state agencies were in the top 5 for Professional Services spending every year from 2021 to 2023? (Filter for this node: Category Description == 'PROFESSIONAL SERVICES'; group by Agency Name; sum Payments Total; rank desc; take top 5.)`

- Node 3 `subquestion`
  - copy: `Which Missouri state agencies were in the top 5 for Professional Services spending in fiscal year 2023?`
  - tasks_mini: `Which Missouri state agencies were in the top 5 for Professional Services spending every year from 2021 to 2023? (Filter for this node: Category Description == 'PROFESSIONAL SERVICES'; group by Agency Name; sum Payments Total; rank desc; take top 5.)`

- Node 4 `subquestion`
  - copy: `For calendar year 2021, what is the employee count for each agency in <hop 1 answer>?`
  - tasks_mini: `Among <answer from hop 1>, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in the hop 1 intersection {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name (employee records) in this file.)`

- Node 5 `subquestion`
  - copy: `For calendar year 2022, what is the employee count for each agency in <hop 1 answer>?`
  - tasks_mini: `Among <answer from hop 1>, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in the hop 1 intersection {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name (employee records) in this file.)`

- Node 6 `subquestion`
  - copy: `Using the 2023 employee counts from this file together with <node 4 answer> and <node 5 answer>, which agency in <hop 1 answer> had the highest average employee count across 2021-2023?`
  - tasks_mini: `Among <answer from hop 1>, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in the hop 1 intersection {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name (employee records) in this file.)`

- Node 7 `subquestion`
  - copy: `What city is the headquarters of <node 6 answer> located in?`
  - tasks_mini: `What city is the headquarters of <answer from hop 2> located in?`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-It has its headquarters in Missouri's capital of Jefferson City.
+The Missouri Department of Corrections has its headquarters in Missouri's capital of Jefferson City.
```

- Node 8 `subquestion`
  - copy: `What is the historically Black university located in <node 7 answer>?`
  - tasks_mini: `What is the historically Black university located in <answer from hop 3>?`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-Jefferson City is also home to Lincoln University, a public historically black and federal land-grant university
+Jefferson City is home to Lincoln University, a public historically Black university founded in 1866 by Union Army Black veterans of the First Missouri Regiment of Colored Infantry and 62nd Regiment of U.S. Colored Troops.
```

- Node 9 `subquestion`
  - copy: `Who founded <node 8 answer>?`
  - tasks_mini: `Who founded <answer from hop 4>?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-founded by James Milton Turner
+Lincoln University was founded in 1866. The 62nd Colored Infantry regiment raised $6,300 to set up a Black school, headed by a white abolitionist officer, Richard Foster, and founded by James Milton Turner.
```

- Node 10 `subquestion`
  - copy: `In what year did <node 9 answer> die?`
  - tasks_mini: `In what year did <answer from hop 5> die?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-November 1, 1915
+James Milton Turner (c. 1840 - November 1, 1915) was an American political leader, activist, educator, and diplomat during the Reconstruction era.
```

### `k-6-d-3/task_2.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which agencies are the top 20 issuing agencies in January 2019 by total parking-violation fine amount?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 2 `subquestion`
  - copy: `Which agencies are the top 20 issuing agencies in January 2020 by total parking-violation fine amount?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 3 `subquestion`
  - copy: `Which agencies are the top 20 issuing agencies in January 2021 by total parking-violation fine amount?`
  - tasks_mini: `Which agencies were in the top 20 for total January parking-violation fine amount in 2019-2021? (Filter for this node: group by ISSUING_AGENCY_NAME; sum FINE_AMOUNT; rank desc; take top 20.)`

- Node 4 `subquestion`
  - copy: `For January 2019, how many moving violations were issued by the agencies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 5 `subquestion`
  - copy: `For January 2020, how many moving violations were issued by the agencies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 6 `subquestion`
  - copy: `For January 2021, how many moving violations were issued by the agencies in <hop 1 answer>?`
  - tasks_mini: `Among the hop 1 intersection agencies that are U.S. national law-enforcement bodies (United States Park Police, United States Capitol Police, and U.S. Secret Service Uniform Division), which had the highest average number of January moving violations from 2019-2021? (Filter for this node: ISSUING_AGENCY_NAME in {UNITED STATES PARK POLICE, UNITED STATES CAPI...`

- Node 6 `answer`
  - copy: `{"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32}`
  - tasks_mini: `UNITED STATES PARK POLICE`

- Node 6 `fact`

```diff
@@ -18,4 +18,13 @@
-
-result = (
+counts_2019 = {
+    "UNITED STATES PARK POLICE": 103,
+    "UNITED STATES CAPITOL POLICE": 176,
+    "US. SECRET SERVICE UNIFORM DIVISION": 145,
```

- Node 7 `subquestion`
  - copy: `Which federal agency operates <hop 2 answer>?`
  - tasks_mini: `Which federal agency operates the United States Park Police (from hop 2)?`

- Node 8 `subquestion`
  - copy: `Which U.S. department is <hop 3 answer> within?`
  - tasks_mini: `The agency (from hop 3) is within which U.S. department?`

- Node 9 `subquestion`
  - copy: `Who is the current head of <hop 4 answer>?`
  - tasks_mini: `Who is the head of the department (from hop 4)?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-The current interior secretary is Doug Burgum.
+The department is headed by the secretary of the interior, who reports directly to the president of the United States and is a member of the president's Cabinet. The current interior secretary is Doug Burgum.
```

- Node 10 `subquestion`
  - copy: `Which university did <hop 5 answer> graduate from in 1978?`
  - tasks_mini: `Which university did the head of the department (from hop 5) graduate from in 1978?`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-graduating from North Dakota State University in 1978
+After graduating from North Dakota State University in 1978 with a bachelor's degree in university studies and earning an MBA from Stanford University two years later.
```

### `k-6-d-3/task_3.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `Which 2019 Chicago library branches with non-null physical addresses are ranked highest by total YTD circulation, so the top-5 circulation branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 5.)`

- Node 1 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 2 `subquestion`
  - copy: `Which 2020 Chicago library branches with non-null physical addresses are ranked highest by total YTD circulation, so the top-5 circulation branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5.)`

- Node 2 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 3 `subquestion`
  - copy: `Which 2021 Chicago library branches with non-null physical addresses are ranked highest by total YTD circulation, so the top-5 circulation branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Which branches (with physical addresses) were in the top 5 by YTD circulation in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5.)`

- Node 3 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 4 `subquestion`
  - copy: `Which 2019 Chicago library branches with non-null physical addresses are ranked highest by total YTD visitors, so the top-5 visitor branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 4 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 5 `subquestion`
  - copy: `Which 2020 Chicago library branches with non-null physical addresses are ranked highest by total YTD visitors, so the top-5 visitor branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 5 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 6 `subquestion`
  - copy: `Which 2021 Chicago library branches with non-null physical addresses are ranked highest by total YTD visitors, so the top-5 visitor branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 1), which were in the top 5 by YTD visitors in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 5 overall.)`

- Node 6 `limit`
  - copy: `5`
  - tasks_mini: ``

- Node 7 `subquestion`
  - copy: `Which 2019 Chicago library branches with non-null physical addresses are ranked highest by total YTD computer sessions, so the top-3 computer-session branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by LOCATION; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 7 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 8 `subquestion`
  - copy: `Which 2020 Chicago library branches with non-null physical addresses are ranked highest by total YTD computer sessions, so the top-3 computer-session branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 8 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 9 `subquestion`
  - copy: `Which 2021 Chicago library branches with non-null physical addresses are ranked highest by total YTD computer sessions, so the top-3 computer-session branches for this year can be compared against the other yearly circulation, visitors, and computer-session rankings?`
  - tasks_mini: `Among the branches (from hop 2), which were in the top 3 by YTD computer sessions in the given year? (Filter for this node: keep rows with non-null ADDRESS; group by BRANCH; sum YTD; sort YTD desc; take top 3 overall.)`

- Node 9 `limit`
  - copy: `3`
  - tasks_mini: ``

- Node 10 `subquestion`
  - copy: `Which Chicago neighborhood is <hop 3 answer> located in?`
  - tasks_mini: `Which Chicago neighborhood is the library branch (from hop 3) located in? (Lookup: Conrad Sulzer Regional Library article.)`

- Node 10 `fact`

```diff
@@ -1 +1 @@
-The library is located in the Lincoln Square neighborhood at 4455 N. Lincoln Avenue.
+According to the Wikipedia article for Conrad Sulzer Regional Library, the library is located in the Lincoln Square neighborhood at 4455 N. Lincoln Avenue.
```

- Node 11 `subquestion`
  - copy: `What community area number corresponds to <hop 4 answer>?`
  - tasks_mini: `What community area number corresponds to the neighborhood from hop 4? (Filter for this node: Community Area == 'Lincoln Square'; return Community Area Number.)`

- Node 11 `answer`
  - copy: `4`
  - tasks_mini: `4`

- Node 11 `fact`

```diff
@@ -12,2 +12,2 @@
-answer = int(result["Community Area Number"].iloc[0])
+answer = str(int(result["Community Area Number"].iloc[0]))
```

- Node 12 `subquestion`
  - copy: `What is the Per Capita Income for community area <hop 5 answer>?`
  - tasks_mini: `What is the per capita income for the community area from hop 5? (Filter for this node: Community Area == 4; return Per Capita Income.)`

- Node 12 `answer`
  - copy: `35503`
  - tasks_mini: `35503`

- Node 12 `fact`

```diff
@@ -12,2 +12,2 @@
-answer = int(result["Per Capita Income"].iloc[0])
+answer = str(int(result["Per Capita Income"].iloc[0]))
```

### `k-6-d-3/task_4.json`
- Impact: major
- Node 1 `fact`

```diff
@@ -1 +1 @@
-chief executive officer of ACT, Inc. (2010–2015)
+Jon Scott Whitmore was the chief executive officer of ACT, Inc. (2010–2015).
```

- Node 2 `subquestion`
  - copy: `In what city was <hop 1 answer> founded?`
  - tasks_mini: `In what city was <node_1 answer> founded?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-Founded in Iowa City, Iowa, in 1959
+ACT, Inc. is a for-profit educational company founded in Iowa City, Iowa.
```

- Node 3 `subquestion`
  - copy: `In which county is <hop 2 answer> located?`
  - tasks_mini: `<node_2 answer> is located in which county?`

- Node 4 `subquestion`
  - copy: `In the school district office listings, entries with CITY='<hop 2 answer>' and NMCNTY='<hop 3 answer>' share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='<node_2 answer>' and NMCNTY='<node_3 answer>' share what two-digit state FIPS code (STFIP)?`

- Node 5 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 6 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 7 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 8 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', among the counties in <hop 5 answer>, what is the highest postsecondary institution count? Answer with the number only.`
  - tasks_mini: `Let A be the set of counties in <node_5 answer>, B be the set of counties in <node_6 answer>, and C be the set of counties in <node_7 answer>. Consider the intersection of C with the union of A and B. Among those counties, what is the highest postsecondary institution count in STFIP='<node_4 answer>'? Answer with the number only.`

### `k-6-d-3/task_5.json`
- Impact: major
- Node 2 `subquestion`
  - copy: `<hop 1 answer> has a New Jersey address. What city appears in that address?`
  - tasks_mini: `<node_1 answer> has a New Jersey address. What city appears in that address?`

- Node 2 `fact`

```diff
@@ -1 +1 @@
-It is headquartered in Lawrence Township, Mercer County, New Jersey, but has a Princeton, New Jersey, address.
+Educational Testing Service (ETS) is headquartered in Mercer County, New Jersey, but has a Princeton, New Jersey, address.
```

- Node 3 `subquestion`
  - copy: `<hop 2 answer> is a borough in which county?`
  - tasks_mini: `<node_2 answer> is a borough in which county?`

- Node 4 `subquestion`
  - copy: `In the school district office listings, entries with CITY='<hop 2 answer>' and NMCNTY='<hop 3 answer>' share what two-digit state FIPS code (STFIP)?`
  - tasks_mini: `In the school district office listings, entries with CITY='<node_2 answer>' and NMCNTY='<node_3 answer>' share what two-digit state FIPS code (STFIP)?`

- Node 5 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most public schools? Return the county names separated by '; '.`

- Node 6 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most private schools? Return the county names separated by '; '.`

- Node 7 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`
  - tasks_mini: `For STFIP='<node_4 answer>', which 3 county names have the most school district offices? Return the county names separated by '; '.`

- Node 8 `subquestion`
  - copy: `For STFIP='<hop 4 answer>', what is the postsecondary institution count for <hop 5 answer>?`
  - tasks_mini: `Let A be the set of counties in <node_5 answer>, B be the set of counties in <node_6 answer>, and C be the set of counties in <node_7 answer>. Consider the intersection of A, B, and C. Among those counties, what is the highest postsecondary institution count in STFIP='<node_4 answer>'? Answer with the number only.`

- Node 8 `answer`
  - copy: `16`
  - tasks_mini: `16`

- Node 8 `fact`

```diff
@@ -22,2 +22,2 @@
-answer = int(county_counts.iloc[0]["postsecondary_institution_count"])
+answer = str(int(county_counts.iloc[0]["postsecondary_institution_count"]))
```

### `k-7-d-4/task_1.json`
- Impact: major
- Node 1 `subquestion`
  - copy: `What were the FY2019 state prison release counts for every Texas county, with county names normalized to uppercase?`
  - tasks_mini: `For FY2019, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2019 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 1 `answer`
  - copy: `{"BEXAR": 4545, "DALLAS": 5355, "EL PASO": 1261, "HARRIS": 9029, "HIDALGO": 1861, "MCLENNAN": 1002, "MONTGOMERY": 1315, "SMITH": 954, "TARRANT": 4769, "TRAVIS": 1857}`
  - tasks_mini: `{"Bexar": 4545, "Dallas": 5355, "Harris": 9029, "Hidalgo": 1861, "Tarrant": 4769}`

- Node 1 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 1 `fact`

```diff
@@ -1,20 +1,12 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2019/files/rows.txt"
```

- Node 2 `subquestion`
  - copy: `What were the FY2020 state prison release counts for every Texas county, with county names normalized to uppercase?`
  - tasks_mini: `For FY2020, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2020 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 2 `answer`
  - copy: `{"BEXAR": 3917, "DALLAS": 4540, "EL PASO": 1121, "HARRIS": 7059, "HIDALGO": 1572, "MCLENNAN": 994, "MONTGOMERY": 1250, "SMITH": 897, "TARRANT": 4450, "TRAVIS": 1596}`
  - tasks_mini: `{"Bexar": 3917, "Dallas": 4540, "Harris": 7059, "Hidalgo": 1572, "Tarrant": 4450}`

- Node 2 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 2 `fact`

```diff
@@ -1,20 +1,12 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2020/files/rows.txt"
```

- Node 3 `subquestion`
  - copy: `What were the FY2021 state prison release counts for every Texas county, with county names normalized to uppercase?`
  - tasks_mini: `For FY2021, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2021 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 3 `answer`
  - copy: `{"BEXAR": 3236, "DALLAS": 3565, "EL PASO": 967, "HARRIS": 5210, "HIDALGO": 1147, "MCLENNAN": 726, "MONTGOMERY": 797, "SMITH": 763, "TARRANT": 3252, "TRAVIS": 1036}`
  - tasks_mini: `{"Bexar": 3236, "Dallas": 3565, "Harris": 5210, "Hidalgo": 1147, "Tarrant": 3252}`

- Node 3 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 3 `fact`

```diff
@@ -1,20 +1,12 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2021/files/rows.txt"
```

- Node 4 `subquestion`
  - copy: `What were the FY2022 state prison release counts for every Texas county, with county names normalized to uppercase?`
  - tasks_mini: `For FY2022, what were release counts for the counties that rank in the top five by average releases across FY2019-FY2022? (Filter for this node: count rows by County in the FY2022 file; normalize County to uppercase; keep counties in the hop 1 average top five set.)`

- Node 4 `answer`
  - copy: `{"BEXAR": 2918, "DALLAS": 3557, "EL PASO": 834, "HARRIS": 4988, "HIDALGO": 1015, "JEFFERSON": 714, "MONTGOMERY": 874, "SMITH": 783, "TARRANT": 3231, "TRAVIS": 790}`
  - tasks_mini: `{"Bexar": 2918, "Dallas": 3557, "Harris": 4988, "Hidalgo": 1015, "Tarrant": 3231}`

- Node 4 `limit`
  - copy: `10`
  - tasks_mini: ``

- Node 4 `fact`

```diff
@@ -1,20 +1,12 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/texas-department-of-criminal-justice-releases-fy-2022/files/rows.txt"
```

- Node 5 `subquestion`
  - copy: `What is the county seat of <hop 1 answer>?`
  - tasks_mini: `What is the county seat of <county from aggregation of nodes 1-4: Bexar County>? (Lookup: find the county seat statement in the Bexar County, Texas article.)`

- Node 5 `fact`

```diff
@@ -1 +1 @@
-its county seat is San Antonio
+According to the Wikipedia article for Bexar County, Texas, 'Its county seat is San Antonio.'
```

- Node 6 `subquestion`
  - copy: `What five-time NBA champion team is based in <hop 2 answer>?`
  - tasks_mini: `What five-time NBA champion team is based in <city from node 5: San Antonio>? (Lookup: find the sentence naming the five-time NBA champion team in the San Antonio article.)`

- Node 6 `fact`

```diff
@@ -1 +1 @@
-is home to the five-time NBA champion San Antonio Spurs
+According to the Wikipedia article for San Antonio, 'San Antonio is also home to the five-time NBA champion San Antonio Spurs.'
```

- Node 7 `subquestion`
  - copy: `Which team did <hop 3 answer> defeat in its first NBA championship?`
  - tasks_mini: `Which team did <team from node 6: San Antonio Spurs> defeat in their first NBA Finals championship? (Lookup: Spurs article; first championship opponent.)`

- Node 7 `fact`

```diff
@@ -1 +1 @@
-they faced the New York Knicks, who had made history by becoming the first eighth seed to ever make the NBA Finals. The Spurs won the series 4-1 and the franchise's first NBA Championship
+According to the Wikipedia article for San Antonio Spurs. For their first championship in 1999, the article states they 'defeated the New York Knicks' in the NBA Finals.
```

- Node 8 `subquestion`
  - copy: `In which borough is <hop 4 answer> based?`
  - tasks_mini: `In which borough is <team from node 7: New York Knicks> based? (Lookup: Knicks article; borough of Manhattan.)`

- Node 8 `fact`

```diff
@@ -1 +1 @@
-based in the New York City borough of Manhattan
+According to the Wikipedia article for New York Knicks, 'The New York Knickerbockers, commonly known as the New York Knicks, are an American professional basketball team based in the New York City borough of Manhattan.'
```

- Node 9 `subquestion`
  - copy: `Which county is coextensive with <hop 5 answer>?`
  - tasks_mini: `Which county is coextensive with <borough from node 8: Manhattan>?`

- Node 9 `fact`

```diff
@@ -1 +1 @@
-Coextensive with New York County
+According to the Wikipedia article for Manhattan, Manhattan is coextensive with New York County.
```

- Node 10 `subquestion`
  - copy: `How many total hate crime incidents were there in <hop 6 answer> in 2020?`
  - tasks_mini: `How many total hate crime incidents were there in <county from node 9: New York County> in 2020? (Filter: Year == 2020; County == New York; Crime Type in {Crimes Against Persons, Property Crimes}; sum Total Incidents.)`

- Node 10 `answer`
  - copy: `82`
  - tasks_mini: `82`

- Node 10 `fact`

```diff
@@ -1,16 +1,17 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/hate-crimes-by-county-and-bias-type-beginning-2010/files/rows.txt"
```

- Node 11 `subquestion`
  - copy: `How many firearm crimes were there in <hop 6 answer> in 2020?`
  - tasks_mini: `How many firearm crimes were there in <county from node 9: New York County> in 2020? (Filter: Year == 2020; County == New York; use Firearm Count.)`

- Node 11 `answer`
  - copy: `898`
  - tasks_mini: `898`

- Node 11 `fact`

```diff
@@ -1,12 +1,19 @@
-import io
-import pandas as pd
-import boto3
-from botocore import UNSIGNED
-from botocore.config import Config
-source = "datagov/index-violent-property-and-firearm-rates-by-county-beginning-1990/files/rows.txt"
```
