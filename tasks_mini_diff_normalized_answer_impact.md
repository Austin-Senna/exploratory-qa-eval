# Normalized Answer Impact Diff

Direction: `tasks_mini copy` -> `tasks_mini`.

## Criteria

- REAL_ANSWER_CHANGE: final answer or any node answer differs after normalization.
- FORMAT_ONLY_ANSWER_CHANGE: raw answer differs, but normalized value is the same, such as string vs number, case, punctuation, comma formatting, or list ordering.
- NO_ANSWER_CHANGE: no final/node answer changes after normalization.
- STRUCTURAL_ONLY: file exists only on one side.

## Counts

- REAL_ANSWER_CHANGE: 68
- FORMAT_ONLY_ANSWER_CHANGE: 11
- NO_ANSWER_CHANGE: 55
- STRUCTURAL_ONLY: 2

## Real Answer Changes

### `k-2-d-3/task_1.json`
- Reason: 2 node answer(s) changed semantically
```text
node 1 REAL: Edward -> 92
node 2 REAL: 92 -> Edward
```
- Other differences: node fields changed: answer:2, fact:4, source:2, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-2/task_1.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: Charlie -> 1839
node 2 REAL: 1 -> Charlie
node 3 REAL: 1839 -> 1
```
- Other differences: question wording changed; node fields changed: answer:3, fact:4, source:3, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-2/task_3.json`
- Reason: 2 node answer(s) changed semantically
```text
node 1 REAL: {"BRONX HIGH SCHOOL OF SCIENCE": 1.0, "BRONX SCHOOL OF LAW AND FINANCE": 6.0, "HIGH SCHOOL OF AMERICAN STUDIES AT LEHMAN COLLEGE"... -> ["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL OF AMERICAN STUDIES AT LEHMAN COLLEGE", "RIVERDALE/KINGSBRIDGE...
node 2 REAL: {"BRONX HIGH SCHOOL FOR MEDICAL SCIENCE": 8.0, "BRONX HIGH SCHOOL OF SCIENCE": 2.0, "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL ST... -> ["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "MARIE CURIE HIGH SCHOOL FOR NURSING, MEDICINE, AND ALLIED HEALTH PROFE", "...
```
- Other differences: question wording changed; node fields changed: answer:2, fact:3, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-3/task_6.json`
- Reason: 1 node answer(s) changed semantically
```text
node 6 REAL: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32} -> UNITED STATES PARK POLICE
```
- Other differences: node fields changed: answer:1, fact:6, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_1.json`
- Reason: 3 node answer(s) changed semantically
```text
node 5 REAL: Chevy Chase -> Chevy Chase, Friendship Heights
node 6 REAL: Chevy Chase, Maryland -> Montgomery County, Maryland
node 7 REAL: Montgomery County -> 20
```
- Other differences: question wording changed; node fields changed: answer:3, fact:6, node_ids/count:1, source:2, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_3.json`
- Reason: 1 node answer(s) changed semantically
```text
node 8 REAL: Whitman had population 47,973 -> Whitman had population 47,973 (lower than Kitsap's 275,611), county seat is Colfax
```
- Other differences: node fields changed: answer:1, fact:6, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_5.json`
- Reason: 5 node answer(s) changed semantically
```text
node 1 REAL: ["Herbert H Lehman High School", "Susan E. Wagner High School", "Automotive High School"] -> ["Herbert H Lehman High School", "Jhs 13 Jackie Robinson", "Susan E. Wagner High School"]
node 3 REAL: ["Susan E. Wagner High School", "Herbert H Lehman High School", "Sheepshead Bay High School"] -> ["Brooklyn Secondary School for Collaborative Studies", "Susan E. Wagner High School", "Herbert H Lehman High School"]
node 4 REAL: ["Susan E. Wagner High School", "Richmond Hill High School", "Clara Barton High School"] -> ["Susan E. Wagner High School", "Richmond Hill High School", "Acad For College Prep & Career Exploration"]
node 6 REAL: Brooklyn Bridge -> ["Brooklyn Bridge", "Williamsburg Bridge", "George Washington Bridge", "Verrazzano-Narrows Bridge", "Triborough Bridge (Suspensio...
node 7 REAL: Manhattan Bridge -> ["Verrazzano-Narrows Bridge", "Outerbridge Crossing", "Goethals Bridge", "Bayonne Bridge"]
```
- Other differences: question wording changed; node fields changed: answer:5, fact:6, node_ids/count:1, source:2, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_7.json`
- Reason: 2 node answer(s) changed semantically
```text
node 6 REAL: ["American Folk Art Museum", "American Museum of Natural History", "Children's Museum of Manhattan", "New-York Historical Society... -> ["American Museum of Natural History", "Lincoln Center for the Performing Arts"]
node 7 REAL: 1961 -> ["American Museum of Natural History", "Metropolitan Museum of Art"]
```
- Other differences: question wording changed; node fields changed: answer:2, depends_on:8, fact:8, node_ids/count:1, source:1, subquestion:3; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_8.json`
- Reason: 3 node answer(s) changed semantically
```text
node 2 REAL: ["Hamilton Heights School", "Muscota", "P.S. 004 Duke Ellington", "P.S. 005 Ellen Lurie", "P.S. 008 Luis Belliard", "P.S. 028 Wri... -> ["P.S. 153 Adam Clayton Powell", "..."]
node 3 REAL: ["P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 153 Adam Clayton Powell", "P.S. 189"] -> ["P.S. 153 Adam Clayton Powell", "..."]
node 4 REAL: ["Hamilton Heights School", "P.S. 048 P.O. Michael J. Buczek", "P.S. 153 Adam Clayton Powell", "P.S. 189"] -> ["P.S. 153 Adam Clayton Powell", "..."]
node 1 FORMAT_ONLY: ["P.S. 005 Ellen Lurie", "P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 048 P.O. Michael J. Buczek", "P.S. 128 Audub... -> ["P.S. 005 ELLEN LURIE", "P.S. 008 LUIS BELLIARD", "P.S. 028 WRIGHT BROTHERS", "P.S. 048 P.O. MICHAEL J. BUCZEK", "P.S. 128 AUDUB...
```
- Other differences: node fields changed: answer:4, fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_9.json`
- Reason: 1 node answer(s) changed semantically
```text
node 4 REAL: ["Alabama", "Arizona", "Louisiana", "Missouri", "Oregon", "South Carolina", "Tennessee", "Virginia", "Washington"] -> ["Arizona", "Alabama", "Louisiana", "Tennessee", "Missouri", "Oregon", "South Carolina", "Virginia", "Washington", "Puerto Rico"]
```
- Other differences: node fields changed: answer:1, fact:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-5/task_1.json`
- Reason: final answer changed semantically; 7 node answer(s) changed semantically
```text
final answer (real_change): 1693 -> Friesland
node 1 REAL: ["MANHATTAN BRIDGES HIGH SCHOOL", "BEDFORD ACADEMY HIGH SCHOOL", "MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOO... -> ["Manhattan Bridges High School", "Bedford Academy High School", "Marble Hill High School for International Studies", "High Schoo...
node 2 REAL: ["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATHEMATICS", "HIGH SCHOOL FOR CONTEMPORARY ... -> ["Brooklyn International High School", "Gregorio Luperon High School", "High School for Contemporary Arts", "Bedford Academy High...
node 3 REAL: ["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PREPARATORY SCHOOL", "SOUTH BRONX PREPARAT... -> ["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Preparatory School", "South Bronx Preparat...
node 4 REAL: ["Theatre Arts Production Company School", "Brooklyn International High School at Water's Edge", "Williamsburg Preparatory School... -> ["Theatre Arts Production Company School", "Brooklyn International High School", "Williamsburg Preparatory School", "Marble Hill ...
node 5 REAL: ["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village Academy", "Williamsburg High School for A... -> ["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village Academy", "Williamsburg High School for A...
node 6 REAL: ["Spuyten Duyvil", "Marble Hill"] -> Frederick Philipse
node 7 REAL: King's Bridge -> Friesland
```
- Other differences: question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:2, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-1/task_4.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: Wallops Flight Facility -> EAARL (Experimental Advanced Airborne Research Lidar)
node 2 REAL: Accomack County -> Wallops Flight Facility
node 3 REAL: Chincoteague -> Accomack County
```
- Other differences: question wording changed; node fields changed: answer:3, fact:3, node_ids/count:1, source:2, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-2/task_15.json`
- Reason: 2 node answer(s) changed semantically
```text
node 2 REAL: Whitman County borders Idaho and had a 2020 population of 47,973, so it meets both criteria. -> Whitman County: borders Idaho (YES, per adjacent counties list), population 47,973 (YES, under 300,000) → MEETS BOTH CRITERIA
node 3 REAL: Spokane County borders Idaho, but its 2020 population was 539,339, so it does not meet both criteria. -> Spokane County: borders Idaho (YES, per adjacent counties list), population 539,339 (NO, exceeds 300,000) → DOES NOT MEET BOTH CR...
```
- Other differences: question wording changed; node fields changed: answer:2, fact:5, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-2/task_4.json`
- Reason: 1 node answer(s) changed semantically
```text
node 2 REAL: 2023-02-23T00:00:00 -> 2023-01-06T00:00:00
```
- Other differences: question wording changed; node fields changed: answer:1, fact:4, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_1.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: {"Magnet School for Science & Technology": 14, "PS 130 The Parkside": 13.1, "PS 172 Beacon School of Excellence": 23.5, "PS 321 W... -> ["PS 321 William Penn", "PS 107 John W Kimball"]
node 2 REAL: {"Magnet School of Math, Science and Design Techno": 21.2, "PS 130 The Parkside": 20.5, "PS 146": 21.6, "PS 15 Patrick F. Daly": ... -> ["PS 321 William Penn", "PS 10 Magnet School"]
node 3 REAL: {"Magnet School of Math, Science and Design Techno": 21.5, "PS 107 John W. Kimball": 17.8, "PS 172 Beacon School of Excellence": ... -> ["PS 321 William Penn", "PS 10 Magnet School"]
```
- Other differences: question wording changed; node fields changed: answer:3, depends_on:6, fact:4, limit:3, subquestion:6; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_10.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: ["Erie", "Monroe", "Westchester", "Onondaga", "Nassau"] -> ["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Nassau County"]
node 2 REAL: ["Monroe", "Suffolk", "Erie", "Westchester", "Onondaga", "Orange", "Broome", "Albany", "Niagara", "Oneida"] -> ["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Suffolk County"]
node 3 REAL: ["Suffolk", "Nassau", "Erie", "Monroe"] -> ["Suffolk County", "Nassau County", "Erie County", "Monroe County"]
```
- Other differences: question wording changed; node fields changed: answer:3, fact:3, limit:1, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_11.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: ["Marshall County", "Floyd County", "Clayton County", "Crawford County", "Des Moines County", "Clinton County", "Lee County", "Ta... -> ["Allamakee County", "Appanoose County", "Benton County", "Black Hawk County", "Butler County", "Chickasaw County", "Clayton Coun...
node 2 REAL: ["Fremont", "Poweshiek", "Guthrie", "Clarke", "Floyd", "Hamilton", "Pottawattamie", "Jasper", "Scott", "Black Hawk"] -> ["Adair County", "Allamakee County", "Audubon County", "Benton County", "Black Hawk County", "Bremer County", "Calhoun County", "...
node 3 REAL: ["Polk", "Linn", "Scott", "Johnson", "Dallas", "Black Hawk", "Dubuque", "Woodbury", "Story", "Pottawattamie"] -> ["Black Hawk County", "Scott County", "Dallas County", "Dubuque County", "Johnson County", "Linn County", "Polk County", "Pottawa...
```
- Other differences: question wording changed; node fields changed: answer:3, fact:3, limit:2, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_12.json`
- Reason: 1 node answer(s) changed semantically
```text
node 3 REAL: {"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956} -> CORRECTIONS
```
- Other differences: node fields changed: answer:1, fact:1, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_2.json`
- Reason: 7 node answer(s) changed semantically
```text
node 2 REAL: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270", "PS 316"] -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 3 REAL: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270"] -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 4 REAL: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 054", "PS 056", "PS 067", "PS 256", "PS 270", "PS 316"] -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 5 REAL: ["PS 003", "PS 011", "PS 046", "PS 054", "PS 056", "PS 256", "PS 270"] -> ["PS 003 The Bedford Village", "PS 011 Purvis J. Behan", "PS 046 Edward C. Blum", "PS 054 Samuel C. Barnes", "PS 056 Lewis H. Lat...
node 6 REAL: {"Ps 11 Purvis J Behan": 24, "Ps 256 Benjamin Banneker": 2, "Ps 270 Joanne Dekalb": 4, "Ps 3 The Bedford Village": 7, "Ps 54 Samu... -> {"PS 003 The Bedford Village": 7, "PS 009 Teunis G. Bergen": 13, "PS 011 Purvis J. Behan": 24, "PS 046 Edward C. Blum": 22, "PS 0...
node 7 REAL: {"Ps 11 Purvis J Behan": 15, "Ps 256 Benjamin Banneker": 13, "Ps 270 Johann Dekalb": 5, "Ps 3 The Bedford Village": 6, "Ps 54 Sam... -> {"PS 003 The Bedford Village": 6, "PS 009 Teunis G. Bergen": 5, "PS 011 Purvis J. Behan": 15, "PS 046 Edward C. Blum": 13, "PS 05...
node 8 REAL: {"Ps 11 Purvis J Behan": 22, "Ps 256 Benjamin Banneker": 7, "Ps 270 Johann Dekalb": 4, "Ps 3 The Bedford Village": 12, "Ps 54 Sam... -> {"PS 003 The Bedford Village": 12, "PS 009 Teunis G. Bergen": 4, "PS 011 Purvis J. Behan": 22, "PS 046 Edward C. Blum": 15, "PS 0...
```
- Other differences: node fields changed: answer:7, fact:7, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_4.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE D... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE DPT-DISTRICT 1", "METROPOLITAN POLICE D...
node 2 REAL: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT ... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHORITY", "METROPOLITAN POLICE DPT-DISTRICT ...
node 3 REAL: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE D... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE DPT-DISTRICT 3", "METROPOLITAN POLICE D...
node 6 REAL: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32} -> UNITED STATES PARK POLICE
```
- Other differences: question wording changed; node fields changed: answer:4, fact:6, limit:3, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_5.json`
- Reason: 1 node answer(s) changed semantically
```text
node 3 REAL: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32} -> UNITED STATES PARK POLICE
```
- Other differences: question wording changed; node fields changed: answer:1, fact:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_7.json`
- Reason: 1 node answer(s) changed semantically
```text
node 6 REAL: Ulster County -> Ulster County, New York
```
- Other differences: question wording changed; node fields changed: answer:1, fact:4, source:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_8.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: ["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATHEMATICS", "HIGH SCHOOL FOR CONTEMPORARY ... -> ["Brooklyn International High School", "Gregorio Luperon High School", "High School for Contemporary Arts", "Bedford Academy High...
node 2 REAL: ["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PREPARATORY SCHOOL", "SOUTH BRONX PREPARAT... -> ["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Preparatory School", "South Bronx Preparat...
node 3 REAL: ["Theatre Arts Production Company School", "Brooklyn International High School at Water's Edge", "Williamsburg Preparatory School... -> ["Theatre Arts Production Company School", "Brooklyn International High School", "Williamsburg Preparatory School", "Marble Hill ...
```
- Other differences: question wording changed; node fields changed: answer:3, fact:3, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_9.json`
- Reason: 6 node answer(s) changed semantically
```text
node 1 REAL: ["Suffolk", "Monroe", "Westchester", "Onondaga", "Nassau"] -> ["Suffolk County", "Monroe County", "Westchester County", "Onondaga County", "Nassau County"]
node 2 REAL: ["ERIE", "ONONDAGA", "SUFFOLK", "ONEIDA", "MONROE"] -> ["Erie County", "Onondaga County", "Suffolk County", "Oneida County", "Monroe County"]
node 3 REAL: ["Monroe", "Erie", "Westchester", "Suffolk", "Nassau", "Onondaga"] -> ["Monroe County", "Erie County", "Westchester County", "Suffolk County", "Nassau County", "Onondaga County"]
node 4 REAL: ["Suffolk", "Onondaga", "Westchester"] -> ["Suffolk County", "Onondaga County"]
node 5 REAL: ["Monroe", "Nassau", "Onondaga"] -> ["Monroe County", "Onondaga County"]
node 6 REAL: ["Erie", "Monroe", "Onondaga", "Westchester"] -> ["Monroe County", "Onondaga County"]
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_1.json`
- Reason: 2 node answer(s) changed semantically
```text
node 5 REAL: P.S. 380 John Wayne Elementary -> ["P.S. 380 John Wayne Elementary", "P.S. 172 Beacon School of Excellence"]
node 6 REAL: 10/28 -> P.S. 380 John Wayne Elementary
```
- Other differences: question wording changed; node fields changed: answer:2, fact:2, node_ids/count:1, source:2, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_12.json`
- Reason: 2 node answer(s) changed semantically
```text
node 8 REAL: Henry Lawrence Kinney -> Fort Worth
node 9 REAL: 1850 -> Henry Lawrence Kinney
node 5 FORMAT_ONLY: ["Nueces", "Denton"] -> ["DENTON", "NUECES"]
```
- Other differences: node fields changed: answer:3, fact:5, node_ids/count:1, source:2, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_2.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: {"Abraham Lincoln Elementary School": "610038", "Alexander Graham Bell Elementary School": "609799", "Christopher Columbus Elemen... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 123 others": "..."}
node 2 REAL: {"Addams": "609772", "Armstrong, G": "609779", "Clissold": "609861", "Dixon": "609887", "Greene": "609952", "Irving": "610121", "... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 226 others": "..."}
node 3 REAL: {"Amos Alonzo Stagg Elementary School": "610339", "Arthur R Ashe Elementary School": "610268", "Edgar Allan Poe Elementary Classi... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 38 others": "..."}
node 4 REAL: {"ASHE": "610268", "BRUNSON": "609830", "CALMECA": "610353", "CLINTON": "609859", "CURTIS": "609900", "DIRKSEN": "609874", "KELLE... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "and 295 others": "..."}
node 5 FORMAT_ONLY: {"CLEVELAND": "IRVING PARK", "HAWTHORNE": "LAKE VIEW", "POE": "PULLMAN", "REINBERG": "PORTAGE PARK"} -> {"Cleveland": "Irving Park", "Hawthorne": "Lake View", "Poe": "Pullman", "Reinberg": "Portage Park"}
```
- Other differences: question wording changed; node fields changed: answer:5, fact:7, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_3.json`
- Reason: 5 node answer(s) changed semantically
```text
node 1 REAL: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 1... -> {"J.H.S. 067 Louis Pasteur": "26Q067, 84 offers", "J.H.S. 074 Nathaniel Hawthorne": "26Q074, 102 offers", "J.H.S. 216 George J. R...
node 2 REAL: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 1... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 1...
node 3 REAL: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 1... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 1...
node 4 REAL: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S. 104 SIMON BARUCH": "02M104", "J.H.S. 1... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S. 216 George J. Ryan": "26Q216", "M.S. 1...
node 9 REAL: No, he was an education/governance figure -> 1887
```
- Other differences: node fields changed: answer:5, fact:6, limit:4, node_ids/count:1, source:1, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_5.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: {"CORRECTIONS": 279877976.24, "ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HEALTH AND SENIOR SERVICES": 698796366.98, "H... -> {"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "MENTAL HEALTH": 75989...
node 2 REAL: {"CORRECTIONS": 279260171.22, "ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HEALTH AND SENIOR SERVICES": 734833032.4, "HI... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "MENTAL HEALTH": 81379...
node 3 REAL: {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HEALTH AND SENIOR SERVICES": 815631750.83, "HIGHER EDUCATION AND WORKFORCE... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "MENTAL HEALTH": 87743...
node 4 REAL: {"CORRECTIONS": 268435627.28, "ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HEALTH AND SENIOR SERVICES": 884344054.25, "H... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "MENTAL HEALTH": 92105...
```
- Other differences: question wording changed; node fields changed: answer:4, fact:2, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_6.json`
- Reason: 4 node answer(s) changed semantically
```text
node 2 REAL: {"BEXAR": 269462082.97, "DALLAS": 838316444.65, "DENTON": 186170844.17, "EL PASO": 123694754.23, "HARRIS": 1303630847.3, "HAYS": ... -> {"Bexar": 269462082.97, "Dallas": 838316444.65, "Harris": 1303630847.3, "Montgomery": 424383088.05, "Travis": 427160745.36}
node 3 REAL: {"BEXAR": 302940592.72, "DALLAS": 827510409.8, "DENTON": 260841655.76, "HARRIS": 1391779835.06, "HAYS": 154023926.62, "MONTGOMERY... -> {"Bexar": 302940592.72, "Dallas": 827510409.8, "Harris": 1391779835.06, "Montgomery": 416744287.28, "Travis": 614936080.37}
node 4 REAL: {"BEXAR": 494340352.72, "DALLAS": 1324261419.12, "DENTON": 355805325.9, "HARRIS": 1663151150.96, "HAYS": 251859833.02, "MCLENNAN"... -> {"Bexar": 494340352.72, "Dallas": 1324261419.12, "Harris": 1663151150.96, "Montgomery": 612813968.49, "Travis": 821945717.49}
node 5 REAL: {"BEXAR": 596386366.99, "DALLAS": 1171406639.17, "DENTON": 412077419.13, "EL PASO": 144869614.83, "HARRIS": 1741663003.68, "HAYS"... -> {"Bexar": 596386366.99, "Dallas": 1171406639.17, "Harris": 1741663003.68, "Montgomery": 705433711.03, "Travis": 774601022.23}
```
- Other differences: node fields changed: answer:4, fact:9, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_7.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: {"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47000000003, "Aviation": 19982790.57, "Board of Election C... -> {"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47, "Aviation": 19982790.57, "Board of Election Commission...
node 2 REAL: {"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.01, "CHICAGO DEPARTMENT OF TRANSPORTATION... -> {"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.01, "CHICAGO DEPARTMENT OF TRANSPORTATION...
node 3 REAL: {"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605.54, "CHICAGO DEPARTMENT OF TRANSPORTATIO... -> {"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605.54, "CHICAGO DEPARTMENT OF TRANSPORTATIO...
node 4 REAL: {"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4, "Chicago Department of Transportation"... -> {"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4, "Chicago Department of Transportation"...
```
- Other differences: node fields changed: answer:4, fact:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_8.json`
- Reason: 8 node answer(s) changed semantically
```text
node 1 REAL: ["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead Architects", "McKinstry Essention, LLC"... -> ["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead Architects", "McKinstry Essention, LLC"...
node 2 REAL: ["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "Imagesource Inc", "WSP USA Inc.", "HDR Engineering, Inc.", "HNTB Corpo... -> ["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "WSP USA Inc.", "Imagesource Inc", "HDR Engineering, Inc.", "HNTB Corpo...
node 3 REAL: ["Sharp Electronics Corporation", "DOC Correctional Industries", "A-1 Performance Inc", "WSP USA Inc.", "Shi International Corp",... -> ["Sharp Electronics Corporation", "DOC Correctional Industries", "WSP USA Inc.", "A-1 Performance Inc", "Parametrix, Inc.", "Imag...
node 4 REAL: ["JP Morgan Chase Bank NA", "Washington State University", "Washington State Department of Transportation", "WSP USA Inc.", "Univ... -> ["JP Morgan Chase Bank NA", "WSP USA Inc.", "University of Washington", "WA State DSHS", "HDR Engineering, Inc.", "Parametrix, In...
node 5 REAL: 1885 -> Omaha, Nebraska; 1917
node 6 REAL: Omaha, Nebraska; 1917 -> 1947
node 7 REAL: 1947 -> 1914
node 8 REAL: ["WSP USA Inc.", "HDR Engineering, Inc."] -> ["HDR Engineering, Inc.", "HNTB Corporation"]
```
- Other differences: question wording changed; node fields changed: answer:8, fact:8, source:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_1.json`
- Reason: 6 node answer(s) changed semantically
```text
node 1 REAL: ["Jefferson", "St. Lawrence", "Cayuga", "Otsego", "Suffolk", "Tompkins"] -> ["Jefferson County", "St. Lawrence County", "Tompkins County", "Suffolk County", "Otsego County", "Cayuga County"]
node 2 REAL: ["Monroe", "Erie", "Nassau", "Westchester", "Niagara", "Sullivan", "Chautauqua", "Onondaga", "Orange", "Rensselaer"] -> ["Monroe County", "Erie County", "Nassau County", "Westchester County", "Sullivan County", "Niagara County", "Chautauqua County",...
node 3 REAL: ["Suffolk", "Nassau", "Monroe", "Westchester", "Erie", "Essex", "Onondaga", "Ulster", "Orange", "Oneida"] -> ["Suffolk County", "Nassau County", "Westchester County", "Monroe County", "Erie County", "Essex County", "Onondaga County", "Uls...
node 4 REAL: ["Tompkins", "Cattaraugus", "Rockland", "Erie", "Schuyler", "Jefferson", "Livingston/Wyoming"] -> ["Tompkins County", "Cattaraugus County", "Rockland County", "Erie County", "Schuyler County", "Jefferson County", "Livingston/Wy...
node 5 REAL: ["Chautauqua", "Rensselaer", "Jefferson", "Ulster", "Saint Lawrence", "Steuben", "Wayne", "Cattaraugus", "Ontario", "Chemung"] -> ["Chautauqua County", "Rensselaer County", "Jefferson County", "Ulster County", "Saint Lawrence County", "Steuben County", "Wayne...
node 8 REAL: Jefferson -> Jefferson County
```
- Other differences: question wording changed; node fields changed: answer:6, fact:8, limit:3, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_2.json`
- Reason: 6 node answer(s) changed semantically
```text
node 1 REAL: ["Salvatore Albanese", "Anthony Andrews, Jr.", "JoAnn Ariola", "Paul Bader", "Maria Baez", "Steven Banks", "Charles Barron", "Mic... -> ["Domenic Recchia", "Leroy Comrie", "103 others"]
node 2 REAL: ["Joseph Addabbo", "Tony Avella", "Maria Baez", "Ismael Betancourt Jr", "Omar Boucher", "Everly Brown", "Leroy Comrie", "Erik Dil... -> ["Domenic Recchia", "Leroy Comrie", "45 others"]
node 3 REAL: ["Tony Avella", "Albert Baldeo", "Charles Barron", "Ismael Betancourt Jr", "Michael Beys", "Darren Bloch", "Peter Boudouvas", "Ga... -> ["Domenic Recchia", "Leroy Comrie", "67 others"]
node 4 REAL: ["Isaac Abraham", "Maria Arroyo", "Maria Baez", "Steven Anthony Behar", "Victor Bernace", "Douglas Biviano", "Tracy Boyland", "Ja... -> ["Domenic Recchia", "Leroy Comrie", "97 others"]
node 5 REAL: ["Olanike Alabi", "Pedro Alvarez", "Maria Arroyo", "Christopher Banks", "Raquel Batista", "Ken Biberaj", "Ricardo Brown", "Ralina... -> ["Domenic Recchia", "Leroy Comrie", "91 others"]
node 8 REAL: {"Brooklyn": 3889.0, "Queens": 1019.0} -> Brooklyn
```
- Other differences: question wording changed; node fields changed: answer:6, fact:9, limit:5, subquestion:9; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_3.json`
- Reason: 5 node answer(s) changed semantically
```text
node 1 REAL: {"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 5842176, "BUPRENORPH": 5008835, "BUSPIRONE": ... -> {"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 5842176, "BUPRENORPH": 5008835, "BUSPIRONE ":...
node 2 REAL: {"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 6927103, "BUSPIRONE": 6963013, "CARVEDILOL": ... -> {"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 6927103, "BUSPIRONE ": 6963013, "CARVEDILOL":...
node 3 REAL: {"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 9187146, "BUSPIRONE": 8211972, "CARVEDILOL": ... -> {"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 9187146, "BUSPIRONE ": 8211972, "CARVEDILOL":...
node 4 REAL: {"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE": 9341966, "CARVEDILOL": 5184118, "CEPHALEXIN": ... -> {"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE ": 9341966, "CARVEDILOL": 5184118, "CEPHALEXIN":...
node 5 REAL: {"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 8353098, "CITALOPRAM": 5685980, "CLINDAMYCI":... -> {"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 8353098, "CITALOPRAM": 5685980, "CLINDAMYCI":...
```
- Other differences: question wording changed; node fields changed: answer:5, fact:9, limit:5, subquestion:10; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-5/task_4.json`
- Reason: 8 node answer(s) changed semantically
```text
node 1 REAL: {"BEXAR": 622, "CAMERON": 455, "DALLAS": 1207, "EL PASO": 459, "FORT BEND": 150, "HARRIS": 1781, "HIDALGO": 878, "KAUFMAN": 232, ... -> {"BEXAR": 622, "DALLAS": 1207, "HARRIS": 1781, "HIDALGO": 878, "OTHER_COUNTIES": 190, "TARRANT": 562}
node 2 REAL: {"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "EL PASO": 524, "HARRIS": 2179, "HIDALGO": 1203, "KAUFMAN": 204, "TARRANT": 588, "... -> {"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "HARRIS": 2179, "HIDALGO": 1203, "OTHER_COUNTIES": 194}
node 3 REAL: {"BELL": 188, "BEXAR": 756, "CAMERON": 418, "DALLAS": 1120, "EL PASO": 456, "FORT BEND": 202, "HARRIS": 1709, "HIDALGO": 918, "TA... -> {"BEXAR": 756, "DALLAS": 1120, "HARRIS": 1709, "HIDALGO": 918, "OTHER_COUNTIES": 189, "TARRANT": 592}
node 4 REAL: {"BEXAR": 772, "CAMERON": 417, "DALLAS": 1269, "EL PASO": 443, "FORT BEND": 212, "HARRIS": 1871, "HIDALGO": 924, "KAUFMAN": 172, ... -> {"BEXAR": 772, "DALLAS": 1269, "HARRIS": 1871, "HIDALGO": 924, "OTHER_COUNTIES": 188, "TARRANT": 687}
node 5 REAL: {"BEXAR": 743, "CAMERON": 424, "DALLAS": 1352, "EL PASO": 452, "FORT BEND": 177, "HARRIS": 2183, "HIDALGO": 947, "TARRANT": 715, ... -> {"BEXAR": 743, "DALLAS": 1352, "HARRIS": 2183, "HIDALGO": 947, "OTHER_COUNTIES": 189, "TARRANT": 715}
node 6 REAL: {"BEXAR": 13020, "COLLIN": 3526, "DALLAS": 14192, "DENTON": 3761, "EL PASO": 4709, "HARRIS": 23468, "HIDALGO": 4984, "MONTGOMERY"... -> ["Tarrant", "Bexar", "Hidalgo"]
node 7 REAL: {"BELL": 470, "BEXAR": 1074, "DALLAS": 738, "HARRIS": 566, "LUBBOCK": 194, "MCLENNAN": 171, "NUECES": 258, "TARRANT": 555, "TAYLO... -> ["Bexar", "Dallas"]
node 10 REAL: 25 -> 1836
```
- Other differences: question wording changed; node fields changed: answer:8, fact:9, limit:7, subquestion:9; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_10.json`
- Reason: final answer changed semantically; 8 node answer(s) changed semantically
```text
final answer (real_change): 1653 -> 1724
node 1 REAL: {"ALBANY": "43.0%", "ALLEGANY": "47.2%", "BROOME": "46.0%", "CATTARAUGUS": "33.0%", "CAYUGA": "47.4%", "CHAUTAUQUA": "46.5%", "CH... -> ["Compton", "San Bernardino"]
node 2 REAL: {"ALBANY": "34.1%", "ALLEGANY": "26.3%", "BROOME": "36.6%", "CATTARAUGUS": "33.3%", "CAYUGA": "37.6%", "CHAUTAUQUA": "31.4%", "CH... -> ["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Santa Ana", "Santa Maria", "South Gate"]
node 3 REAL: {"ALBANY": "9930", "ALLEGANY": "1322", "BROOME": "5401", "CATTARAUGUS": "1950", "CAYUGA": "2291", "CHAUTAUQUA": "3001", "CHEMUNG"... -> Los Angeles County
node 4 REAL: {"ALBANY": "7564", "ALLEGANY": "1061", "BROOME": "4367", "CATTARAUGUS": "1631", "CAYUGA": "1883", "CHAUTAUQUA": "2477", "CHEMUNG"... -> San Bernardino County
node 5 REAL: Erie tribe of Native Americans -> 1850
node 6 REAL: James Monroe, the fifth president of the United States -> 1853
node 7 REAL: Westmoreland County, Virginia -> Felipe de Neve
node 8 REAL: 1653 -> 1724
```
- Other differences: question wording changed; node fields changed: answer:8, fact:8, limit:4, source:8, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-2/task_3.json`
- Reason: final answer changed semantically; 6 node answer(s) changed semantically
```text
final answer (real_change): Pittsburgh, Pennsylvania -> Gulf of Mexico
node 1 REAL: {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9} -> {"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}
node 2 REAL: {"Detroit": 47.4, "Flint": 45.4, "Gary": 49.0} -> {"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}
node 3 REAL: U.S. Steel Corporation -> {"Cameron": 7620183, "Hidalgo": 1661128}
node 4 REAL: Carnegie Steel Company -> {"Cameron": 1076746, "Hidalgo": 1477805}
node 5 REAL: Andrew Carnegie -> Brownsville
node 6 REAL: Pittsburgh, Pennsylvania -> Gulf Coast
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_4.json`
- Reason: final answer changed semantically; 6 node answer(s) changed semantically
```text
final answer (real_change): San Antonio Bay -> Pittsburgh, Pennsylvania
node 1 REAL: ["Victoria", "Comal", "Willacy", "Brooks"] -> {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}
node 2 REAL: ["Comal", "Victoria", "Atascosa", "Willacy"] -> {"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}
node 3 REAL: ["Victoria County, TX", "Comal County, TX"] -> U.S. Steel Corporation
node 4 REAL: ["Willacy County, TX", "Victoria County, TX"] -> Carnegie Steel Company
node 5 REAL: Victoria -> Andrew Carnegie
node 6 REAL: Guadalupe River -> Pittsburgh, Pennsylvania
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_5.json`
- Reason: final answer changed semantically; 7 node answer(s) changed semantically
```text
final answer (real_change): 1735 -> San Antonio Bay
node 1 REAL: ["Ward 7 (42,226)", "Ward 8 (34,959)"] -> ["Brooks County", "Willacy County", "Comal County", "Victoria County"]
node 2 REAL: ["Ward 8 (37,124)", "Ward 7 (36,113)"] -> ["Willacy County", "Comal County", "Atascosa County", "Victoria County"]
node 3 REAL: Wendell Felder -> ["Victoria County", "Comal County"]
node 4 REAL: Georgetown University -> ["Willacy County", "Victoria County"]
node 5 REAL: John Carroll -> Victoria
node 6 REAL: Patrick Francis Healy -> Guadalupe River
node 7 REAL: 1735 -> San Antonio Bay
```
- Other differences: question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:7, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_6.json`
- Reason: final answer changed semantically; 6 node answer(s) changed semantically
```text
final answer (real_change): 99357947 -> 1735
node 1 REAL: U.S. Steel Corporation -> ["Ward 7 (42,226)", "Ward 8 (34,959)"]
node 2 REAL: Carnegie Steel Company -> ["Ward 7 (36,113)", "Ward 8 (37,124)"]
node 3 REAL: Andrew Carnegie -> Wendell Felder
node 4 REAL: Pittsburgh, Pennsylvania -> Georgetown University
node 5 REAL: 98453962.68 -> John Carroll
node 6 REAL: 100261931.64 -> Patrick Francis Healy
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_7.json`
- Reason: final answer changed semantically; 6 node answer(s) changed semantically
```text
final answer (real_change): Elihu Yale -> 99357947
node 1 REAL: {"Fairfield County": 208, "Hartford County": 335, "New Haven County": 383} -> U.S. Steel Corporation
node 2 REAL: ["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"] -> Carnegie Steel Company
node 3 REAL: New Haven -> Andrew Carnegie
node 4 REAL: Bridgeport -> Pittsburgh, Pennsylvania
node 5 REAL: {"Bridgeport": "16.9%", "New Haven": "13.9%"} -> {"2017": "$98,453,962.68"}
node 6 REAL: {"Bridgeport": "19.3%", "New Haven": "15.4%"} -> {"2018": "$100,261,931.64"}
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_8.json`
- Reason: final answer changed semantically; 7 node answer(s) changed semantically
```text
final answer (real_change): Gippeswic -> Elihu Yale
node 1 REAL: {"Albany": "$19,408,513", "Dutchess": "$25,427,485", "Erie": "$70,519,223", "Monroe": "$48,278,139", "Nassau": "$62,927,542", "On... -> ["New Haven County", "Hartford County", "Fairfield County"]
node 2 REAL: {"Albany": "$19,977,245", "Dutchess": "$23,872,388", "Erie": "$81,139,374", "Monroe": "$51,731,436", "Nassau": "$63,138,172", "On... -> ["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"]
node 3 REAL: {"Erie": "621,451,910.24", "Suffolk": "537,382,172"} -> New Haven
node 4 REAL: {"Erie": "712,460,330.24", "Suffolk": "556,444,750"} -> Bridgeport
node 5 REAL: Suffolk, England -> {"Bridgeport": "16.9%", "New Haven": "13.9%"}
node 6 REAL: Ipswich -> {"Bridgeport": "19.3%", "New Haven": "15.4%"}
node 7 REAL: Gippeswic -> Yale University
```
- Other differences: question wording changed; node fields changed: answer:7, fact:7, limit:2, node_ids/count:1, source:7, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-2/task_9.json`
- Reason: final answer changed semantically; 7 node answer(s) changed semantically
```text
final answer (real_change): 1724 -> Gippeswic
node 1 REAL: ["San Bernardino", "Compton"] -> {"Erie": "$70,519,223", "Suffolk": "$92,420,995", "Westchester": "$66,346,132"}
node 2 REAL: ["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Santa Ana", "Santa Maria", "South Gate"] -> {"Erie": "$81,139,374", "Suffolk": "$87,249,830", "Westchester": "$67,149,496"}
node 3 REAL: Los Angeles County -> {"Erie": "621,451,910.24", "Suffolk": "537,382,172"}
node 4 REAL: San Bernardino County -> {"Erie": "712,460,330.24", "Suffolk": "556,444,750"}
node 5 REAL: 1850 -> Suffolk, England
node 6 REAL: 1853 -> Ipswich
node 7 REAL: Felipe de Neve -> Gippeswic
```
- Other differences: question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:7, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-3/task_1.json`
- Reason: 3 node answer(s) changed semantically
```text
node 2 REAL: ["02M047 - 47 THE AMERICAN SIGN LANGUAGE AND ENGLISH SECONDARY SCHOOL", "02M288 - FOOD AND FINANCE HIGH SCHOOL", "02M294 - ESSEX ... -> ["02M288 - FOOD AND FINANCE HIGH SCHOOL", "02M294 - ESSEX STREET ACADEMY", "02M296 - HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "02M...
node 3 REAL: ["02M047 - 47 The American Sign Language and English Secondary School", "02M288 - Food and Finance High School", "02M294 - Essex ... -> ["02M288 - Food and Finance High School", "02M294 - Essex Street Academy", "02M296 - High School of Hospitality Management", "02M...
node 4 REAL: Eleanor Roosevelt High School -> ["Eleanor Roosevelt High School"]
```
- Other differences: question wording changed; node fields changed: answer:3, fact:8, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_10.json`
- Reason: final answer changed semantically
```text
final answer (real_change): Ward 5 -> Swartekill, New York
```
- Other differences: question wording changed; node fields changed: fact:9, node_ids/count:1, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_11.json`
- Reason: 9 node answer(s) changed semantically
```text
node 1 REAL: {"Ward 2": 8286, "Ward 4": 6971, "Ward 5": 6580, "Ward 6": 8371} -> {"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685}
node 2 REAL: {"Ward 2": 8392, "Ward 4": 6525, "Ward 5": 6072, "Ward 6": 6845} -> {"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281}
node 3 REAL: {"Ward 2": 7897, "Ward 4": 6856, "Ward 5": 6213, "Ward 6": 6658} -> {"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549}
node 4 REAL: {"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685} -> {"Ward 2": 72, "Ward 5": 80}
node 5 REAL: {"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281} -> {"Ward 2": 54, "Ward 5": 83}
node 6 REAL: {"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549} -> {"Ward 2": 54, "Ward 5": 87}
node 7 REAL: {"Ward 2": 72, "Ward 5": 80} -> Sojourner Truth PCS
node 8 REAL: {"Ward 2": 54, "Ward 5": 83} -> Swartekill, New York
node 9 REAL: {"Ward 2": 54, "Ward 5": 87} -> Ulster County, New York
```
- Other differences: question wording changed; node fields changed: answer:9, fact:9, node_ids/count:1, source:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_12.json`
- Reason: 7 node answer(s) changed semantically
```text
node 1 REAL: ["University of Washington", "Washington State University", "Western Washington University", "Eastern Washington University", "Ce... -> Seattle Community College - District 6: 1,308; Green River Community College: 1,723; Community Colleges of Spokane: 1,797
node 2 REAL: {"Central Washington University": 223, "Eastern Washington University": 840, "Evergreen State College": 275, "University of Washi... -> Seattle Colleges: 1,292; Green River Community College: 633; Community Colleges of Spokane: 383
node 3 REAL: {"Central Washington University": 274, "Eastern Washington University": 600, "Evergreen State College": 231, "University of Washi... -> Seattle Community College - District 6: 5,244; Green River Community College: 872; Community Colleges of Spokane: 265
node 4 REAL: {"Central Washington University": 362, "Eastern Washington University": 505, "Evergreen State College": 207, "University of Washi... -> Seattle Colleges is located in Seattle, Washington
node 5 REAL: University of Washington is located in Seattle, Washington -> Green River College is located in Auburn, Washington
node 6 REAL: Eastern Washington University is located in Cheney, Washington -> Community Colleges of Spokane is located in Spokane, Washington
node 9 REAL: [{"BuildingName": "BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus", "avg_TotalGHGEmissions": 20835.775}] -> BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus with 20,835.8 metric tons CO2e average
```
- Other differences: question wording changed; node fields changed: answer:7, fact:7, limit:4, source:6, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_13.json`
- Reason: 3 node answer(s) changed semantically
```text
node 4 REAL: ["Los Angeles County", "San Diego County", "Orange County"] -> Los Angeles County; San Diego County; Orange County
node 5 REAL: ["Los Angeles County", "Orange County", "San Diego County"] -> Los Angeles County; Orange County; San Diego County
node 6 REAL: ["Los Angeles County", "San Diego County", "San Bernardino County"] -> Los Angeles County; San Diego County; San Bernardino County
node 7 FORMAT_ONLY: 71 -> 71
```
- Other differences: question wording changed; node fields changed: answer:4, fact:5, limit:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_14.json`
- Reason: 3 node answer(s) changed semantically
```text
node 4 REAL: ["Polk County", "Linn County", "Scott County"] -> Polk County; Linn County; Scott County
node 5 REAL: ["Polk County", "Linn County", "Sioux County"] -> Polk County; Linn County; Sioux County
node 6 REAL: ["Linn County", "Polk County", "Pottawattamie County"] -> Linn County; Polk County; Pottawattamie County
node 7 FORMAT_ONLY: 7 -> 7
```
- Other differences: question wording changed; node fields changed: answer:4, fact:5, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_15.json`
- Reason: 2 node answer(s) changed semantically
```text
node 2 REAL: ["OFFICE OF GOVERNOR", "OFFICE OF ATTORNEY GENERAL", "JUDICIARY", "OFFICE OF STATE AUDITOR", "OFFICE OF ADMINISTRATION"] -> ["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR", "OFFICE OF ADMINISTRATION"]
node 3 REAL: ["OFFICE OF STATE AUDITOR", "OFFICE OF GOVERNOR", "OFFICE OF LIEUTENANT GOVERNOR", "OFFICE OF ATTORNEY GENERAL", "JUDICIARY"] -> ["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR"]
node 9 FORMAT_ONLY: 2705988 -> 2705988
```
- Other differences: question wording changed; node fields changed: answer:3, fact:4, limit:3, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_2.json`
- Reason: 6 node answer(s) changed semantically
```text
node 1 REAL: {"BEXAR": 14728288130.02, "DALLAS": 21393532327.19, "EL PASO": 5336100417.92, "FORT BEND": 6492630042.559999, "HARRIS": 281580704... -> Travis: $29.37B; Harris: $28.16B; Dallas: $21.39B
node 2 REAL: {"BEXAR": 7513472495.969999, "DALLAS": 10578598198.67, "EL PASO": 2697075449.58, "FORT BEND": 3170751219.59, "HARRIS": 1498610384... -> Travis: $16.34B; Harris: $14.99B; Dallas: $10.58B
node 3 REAL: {"BEXAR": 8839835949.14, "DALLAS": 12496129391.79, "EL PASO": 3075321686.73, "FORT BEND": 3451437618.41, "HARRIS": 16453460156.29... -> Travis: $16.76B; Harris: $16.45B; Dallas: $12.50B
node 10 REAL: {"ALDINE ISD": 67.1557142857143, "ALIEF ISD": 64.05813953488372, "CHANNELVIEW ISD": 59.62384615384615, "GALENA PARK ISD": 62.0743... -> Sheldon ISD: 81.47% average ISP
node 11 REAL: {"ALDINE ISD": 66.54481481481481, "ALIEF ISD": 65.68209302325582, "CHANNELVIEW ISD": 59.41076923076923, "GALENA PARK ISD": 58.663... -> Sheldon ISD: 60.66% average ISP
node 12 REAL: {"ALDINE ISD": 65.33134146341463, "ALIEF ISD": 63.437441860465114, "CHANNELVIEW ISD": 64.9, "GALENA PARK ISD": 60.13083333333333,... -> Sheldon ISD: 66.11% average ISP
```
- Other differences: question wording changed; node fields changed: answer:6, fact:6, limit:6, subquestion:13; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_3.json`
- Reason: 10 node answer(s) changed semantically
```text
node 1 REAL: ["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"] -> Harris: 9,029; Dallas: 5,355; Tarrant: 4,769
node 2 REAL: ["Harris", "Dallas", "Tarrant", "Bexar", "Travis"] -> Harris: 7,059; Dallas: 4,540; Tarrant: 4,450
node 3 REAL: ["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"] -> Harris: 5,210; Dallas: 3,565; Tarrant: 3,252
node 7 REAL: San Antonio is the county seat of Bexar County -> Houston was founded on August 30, 1836
node 8 REAL: Houston was founded on August 30, 1836 -> Dallas was established in 1841
node 9 REAL: Dallas was established in 1841 -> Fort Worth was established in 1849
node 10 REAL: Fort Worth was established in 1849 -> Lake Worth ISD: 65.00% average ISP
node 11 REAL: San Antonio was established in 1718 -> Lake Worth ISD: 65.94% average ISP
node 12 REAL: {"ARLINGTON ISD": 52.73, "AZLE ISD": 40.83, "BIRDVILLE ISD": 46.24, "CASTLEBERRY ISD": 55.89, "CROWLEY ISD": 49.63, "EVERMAN ISD"... -> Lake Worth ISD: 71.65% average ISP
node 13 REAL: {"ARLINGTON ISD": 51.2, "AZLE ISD": 39.74, "BIRDVILLE ISD": 43.88, "CASTLEBERRY ISD": 52.16, "CROWLEY ISD": 47.68, "EVERMAN ISD":... -> 1916
```
- Other differences: question wording changed; node fields changed: answer:10, fact:10, limit:2, node_ids/count:1, source:7, subquestion:13; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_5.json`
- Reason: 1 node answer(s) changed semantically
```text
node 3 REAL: {"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956} -> CORRECTIONS
```
- Other differences: node fields changed: answer:1, fact:3, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_7.json`
- Reason: 1 node answer(s) changed semantically
```text
node 3 REAL: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32} -> UNITED STATES PARK POLICE
```
- Other differences: question wording changed; node fields changed: answer:1, fact:5, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_1.json`
- Reason: 5 node answer(s) changed semantically
```text
node 1 REAL: {"Erie County": 82, "Orange County": 67, "Ulster County": 84, "Westchester County": 68} -> ["Ulster County", "Erie County", "Westchester County", "Orange County"]
node 2 REAL: {"Erie County": 91, "Nassau County": 70, "Oneida County": 50, "Onondaga County": 53, "Orange County": 52, "Suffolk County": 108, ... -> ["Suffolk County", "Erie County", "Nassau County", "Westchester County", "Onondaga County", "Orange County", "Ulster County", "On...
node 3 REAL: {"Albany County": 148, "Bronx County": 158, "Dutchess County": 125, "Erie County": 244, "Kings County": 388, "Monroe County": 232... -> ["New York County", "Nassau County", "Suffolk County", "Queens County", "Kings County", "Westchester County", "Erie County", "Mon...
node 4 REAL: {"Albany County": 20.0, "Broome County": 111.8, "Chautauqua County": 185.9, "Chenango County": 20.0, "Cortland County": 20.0, "Er... -> ["Steuben County", "Chautauqua County", "Lewis County", "Livingston County", "Montgomery County", "Broome County", "Franklin Coun...
node 7 REAL: {"Erie County": 3493, "Westchester County": 1520} -> Erie County
```
- Other differences: node fields changed: answer:5, fact:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_2.json`
- Reason: 8 node answer(s) changed semantically
```text
node 1 REAL: {"AGRICULTURE": 31813546.32, "COMMERCE AND INSURANCE": 2009267.01, "CONSERVATION": 68648122.91, "CORRECTIONS": 279877976.24, "ECO... -> {"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV": 1062578010.95, "MENTAL HEALTH": 75989...
node 2 REAL: {"AGRICULTURE": 37088287.9, "COMMERCE AND INSURANCE": 6346960.76, "CONSERVATION": 71467088.65, "CORRECTIONS": 279260171.22, "ECON... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV": 1220312581.65, "MENTAL HEALTH": 81379...
node 3 REAL: {"AGRICULTURE": 45903725.15, "COMMERCE AND INSURANCE": 6514041.0, "CONSERVATION": 68528448.2, "CORRECTIONS": 286079463.35, "ECONO... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV": 1291298943.33, "MENTAL HEALTH": 87743...
node 4 REAL: {"AGRICULTURE": 40395382.19, "COMMERCE AND INSURANCE": 5910088.04, "CONSERVATION": 61908035.44, "CORRECTIONS": 268435627.28, "ECO... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV": 1320888790.61, "MENTAL HEALTH": 92105...
node 9 REAL: {"Administrative Hearings": 78.45, "Animal Care and Control": 490423.37, "Aviation": 13147383.4, "Board of Election Commissioners... -> {"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}
node 10 REAL: {"Animal Care and Control": 460788.49, "Aviation": 10028911.51, "Board of Election Commissioners": 337421.14, "Buildings": 512654... -> {"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}
node 11 REAL: {"Animal Care and Control": 514031.65, "Aviation": 12881495.76, "Board of Election Commissioners": 600083.73, "Buildings": 553205... -> {"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}
node 12 REAL: {"Administrative Hearings": 13472.0, "Animal Care and Control": 530063.0, "Aviation": 14884756.0, "Board of Election Commissioner... -> {"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}
```
- Other differences: node fields changed: answer:8, fact:12, subquestion:12; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_3.json`
- Reason: 4 node answer(s) changed semantically
```text
node 5 REAL: {"Aviation": 13147383.4, "Fire": 63941565.36, "Police": 101460132.24, "Streets and Sanitation": 15393693.24, "Water Management": ... -> {"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}
node 6 REAL: {"Emergency Management and Communications": 10945883.57, "Fire": 43847384.3, "Police": 116144553.32, "Streets and Sanitation": 16... -> {"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}
node 7 REAL: {"Aviation": 12881495.76, "Fire": 50604010.67, "Police": 143032724.45, "Streets and Sanitation": 13836742.94, "Water Management":... -> {"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}
node 8 REAL: {"Aviation": 14884756.0, "Fire": 49571354.0, "Police": 156732988.0, "Streets and Sanitation": 10718299.0, "Water Management": 200... -> {"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}
```
- Other differences: node fields changed: answer:4, fact:9, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_4.json`
- Reason: 4 node answer(s) changed semantically
```text
node 5 REAL: {"BEXAR": 1805014.14, "COLLIN": 825207.4400000001, "DALLAS": 2835278.75, "DENTON": 882025.85, "EL PASO": 1551768.98, "FORT BEND":... -> {"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}
node 6 REAL: {"BELL": 611323.37, "BEXAR": 1419344.89, "COLLIN": 832593.43, "DALLAS": 2393411.26, "DENTON": 839300.91, "EL PASO": 1302944.72, "... -> {"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}
node 7 REAL: {"BEXAR": 1579009, "CAMERON": 7620183, "DALLAS": 1615421, "EL PASO": 1586612, "HARRIS": 3543992, "HIDALGO": 1661128, "KAUFMAN": 3... -> {"Cameron": 7620183, "Hidalgo": 1661128}
node 8 REAL: {"BEXAR": 1602569, "BRAZORIA": 466678, "CAMERON": 1076746, "DALLAS": 1768090, "EL PASO": 1116732, "FORT BEND": 443344, "HARRIS": ... -> {"Cameron": 1076746, "Hidalgo": 1477805}
node 1 FORMAT_ONLY: ["HARRIS", "HIDALGO", "DALLAS", "CAMERON", "EL PASO"] -> ["Harris", "Hidalgo", "Dallas", "Cameron", "El Paso"]
node 2 FORMAT_ONLY: ["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"] -> ["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]
node 3 FORMAT_ONLY: ["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"] -> ["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]
node 4 FORMAT_ONLY: ["HIDALGO", "HARRIS", "DALLAS", "BEXAR", "CAMERON"] -> ["Hidalgo", "Harris", "Dallas", "Bexar", "Cameron"]
```
- Other differences: question wording changed; node fields changed: answer:8, fact:10, limit:4, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_5.json`
- Reason: 8 node answer(s) changed semantically
```text
node 1 REAL: {"BEE": 602056.1175, "BEXAR": 1976511.21, "CAMERON": 4343483.48, "DALLAS": 1337723.91, "EL PASO": 1820860.48, "HARRIS": 3679408.0... -> {"Atascosa County": 141083.37, "Brooks County": 60454.65, "Comal County": 112322.52, "Victoria County": 95559.47, "Willacy County...
node 2 REAL: {"BEE": 570655.59, "BEXAR": 2001499.64, "CAMERON": 4324920.055, "DALLAS": 1544675.66, "EL PASO": 2080749.0275, "HARRIS": 3708737.... -> {"Atascosa County": 142115.25, "Brooks County": 66250.97, "Comal County": 88868.98, "Victoria County": 89291.24, "Willacy County"...
node 3 REAL: {"BEE": 595756.985, "BEXAR": 2011461.89, "CAMERON": 4404181.145, "DALLAS": 1705207.2, "EL PASO": 2320209.535, "HARRIS": 3969441.2... -> {"Atascosa County": 139933.33, "Brooks County": 78426.43, "Comal County": 78748.11, "Victoria County": 88676.32, "Willacy County"...
node 4 REAL: {"ATASCOSA": 52913.23, "BROOKS": 0.0, "COMAL": 37371.2, "VICTORIA": 40390.435, "WILLACY": 5005.3} -> {"Atascosa County": 52913.23, "Brooks County": 0, "Comal County": 37371.2, "Victoria County": 40390.435, "Willacy County": 5005.3}
node 5 REAL: {"Atascosa": 0, "Brooks": 1, "Comal": 5, "Victoria": 6, "Willacy": 2} -> ["Brooks County", "Willacy County", "Comal County", "Victoria County"]
node 6 REAL: {"Atascosa": 6, "Brooks": 1, "Comal": 16, "Victoria": 11, "Willacy": 3} -> ["Willacy County", "Comal County", "Atascosa County", "Victoria County"]
node 7 REAL: {"Comal County, TX": 19.21235, "Victoria County, TX": 19.51998, "Willacy County, TX": 10.24776} -> ["Victoria County", "Comal County"]
node 8 REAL: {"Comal County, TX": "14-15.9", "Victoria County, TX": "10-11.9", "Willacy County, TX": "6-7.9"} -> ["Willacy County", "Victoria County"]
```
- Other differences: node fields changed: answer:8, fact:10, limit:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_7.json`
- Reason: 2 node answer(s) changed semantically
```text
node 5 REAL: ["Whitman", "Spokane"] -> Whitman and Spokane
node 8 REAL: Pullman -> Pullman is the most populous city in Whitman County (2020 census), located in southeastern Washington within the Palouse region o...
node 1 FORMAT_ONLY: ["Blaine School District (Whatcom)", "Camas School District (Clark)", "Carbonado School District (Pierce)", "Chehalis School Dist... -> ["Riverside School District (Spokane)", "Index Elementary School District 63 (Snohomish)", "Port Townsend School District (Jeffer...
node 2 FORMAT_ONLY: ["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island School District (Kitsap)", "Bainbri... -> ["Edmonds School District (Snohomish)", "Fife School District (Pierce)", "West Valley School District (Spokane) (Spokane)", "Bain...
node 3 FORMAT_ONLY: ["Adna School District (Lewis)", "Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island Sch... -> ["Enumclaw School District (King)", "Snohomish School District (Snohomish)", "Centralia School District (Lewis)", "Mercer Island ...
node 4 FORMAT_ONLY: ["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Island School District (Kitsap)", "Bellevu... -> ["University Place School District (Pierce)", "Enumclaw School District (King)", "Mercer Island School District (King)", "Bainbri...
node 9 FORMAT_ONLY: 2941 -> 2941
```
- Other differences: node fields changed: answer:7, fact:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_8.json`
- Reason: 6 node answer(s) changed semantically
```text
node 1 REAL: ["Bexar", "Hidalgo", "Travis", "El Paso", "Montgomery", "McLennan", "Collin", "Smith", "Galveston", "Jefferson"] -> ["Bexar", "El Paso", "Hidalgo", "Montgomery", "Travis", "McLennan", "Collin", "Smith", "Galveston", "Jefferson", "Taylor", "Nuece...
node 4 REAL: ["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "McLennan", "El Paso"] -> ["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "McLennan", "El Paso", "Johnson"]
node 6 REAL: Montgomery -> ["El Paso", "Hidalgo"]
node 7 REAL: El Paso -> El Paso County is in West Texas
node 8 REAL: Edinburg -> Hidalgo County is in South Texas, county seat is Edinburg
node 9 REAL: University of Texas Rio Grande Valley -> University of Texas Rio Grande Valley (UTRGV)
node 5 FORMAT_ONLY: ["Hidalgo", "El Paso", "Montgomery"] -> ["El Paso", "Hidalgo", "Montgomery"]
```
- Other differences: node fields changed: answer:7, fact:9, limit:2, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_1.json`
- Reason: 3 node answer(s) changed semantically
```text
node 1 REAL: ["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414", "02M416"] -> ["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414", "02M416", "02M418", "02M439", "02M475"...
node 2 REAL: ["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407", "02M411"] -> ["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407", "02M411", "02M412", "02M413", "02M414"...
node 3 REAL: 02M475 -> ["02M475"]
```
- Other differences: question wording changed; node fields changed: answer:3, fact:4, limit:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-6-d-2/task_3.json`
- Reason: 1 node answer(s) changed semantically
```text
node 1 REAL: ["Erie", "Monroe"] -> ["Erie County", "Monroe County"]
node 8 FORMAT_ONLY: 359.8 -> 359.8
```
- Other differences: question wording changed; node fields changed: answer:2, fact:8, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_4.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: {"Camden, New Jersey": 42.2, "Cleveland, Ohio": 42.1, "Dayton, Ohio": 47.2, "Detroit, Michigan": 45.2, "Flint, Michigan": 42.7, "... -> {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}
node 2 REAL: {"Brownsville, Texas": 44.4, "Camden, New Jersey": 44.1, "Dayton, Ohio": 43.5, "Detroit, Michigan": 47.4, "Flint, Michigan": 45.4... -> {"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}
node 7 REAL: 98453962.68 -> {"2017": "$98,453,962.68"}
node 8 REAL: 100261931.64 -> {"2018": "$100,261,931.64"}
```
- Other differences: question wording changed; node fields changed: answer:4, fact:8, limit:2, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_5.json`
- Reason: final answer changed semantically
```text
final answer (real_change): San Francisco Bay -> Pacific Ocean
```
- Other differences: question wording changed; node fields changed: fact:6, node_ids/count:1, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-3/task_2.json`
- Reason: 1 node answer(s) changed semantically
```text
node 6 REAL: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE UNIFORM DIVISION": 32} -> UNITED STATES PARK POLICE
```
- Other differences: node fields changed: answer:1, fact:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-7-d-4/task_1.json`
- Reason: 4 node answer(s) changed semantically
```text
node 1 REAL: {"BEXAR": 4545, "DALLAS": 5355, "EL PASO": 1261, "HARRIS": 9029, "HIDALGO": 1861, "MCLENNAN": 1002, "MONTGOMERY": 1315, "SMITH": ... -> {"Bexar": 4545, "Dallas": 5355, "Harris": 9029, "Hidalgo": 1861, "Tarrant": 4769}
node 2 REAL: {"BEXAR": 3917, "DALLAS": 4540, "EL PASO": 1121, "HARRIS": 7059, "HIDALGO": 1572, "MCLENNAN": 994, "MONTGOMERY": 1250, "SMITH": 8... -> {"Bexar": 3917, "Dallas": 4540, "Harris": 7059, "Hidalgo": 1572, "Tarrant": 4450}
node 3 REAL: {"BEXAR": 3236, "DALLAS": 3565, "EL PASO": 967, "HARRIS": 5210, "HIDALGO": 1147, "MCLENNAN": 726, "MONTGOMERY": 797, "SMITH": 763... -> {"Bexar": 3236, "Dallas": 3565, "Harris": 5210, "Hidalgo": 1147, "Tarrant": 3252}
node 4 REAL: {"BEXAR": 2918, "DALLAS": 3557, "EL PASO": 834, "HARRIS": 4988, "HIDALGO": 1015, "JEFFERSON": 714, "MONTGOMERY": 874, "SMITH": 78... -> {"Bexar": 2918, "Dallas": 3557, "Harris": 4988, "Hidalgo": 1015, "Tarrant": 3231}
node 10 FORMAT_ONLY: 82 -> 82
node 11 FORMAT_ONLY: 898 -> 898
```
- Other differences: question wording changed; node fields changed: answer:6, fact:11, limit:4, subquestion:11; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

## Format-Only Answer Changes

### `k-4-d-2/task_3.json`
- Reason: 2 node answer(s) differ only by formatting/type/order/case
```text
node 5 FORMAT_ONLY: 7871 -> 7871
node 6 FORMAT_ONLY: 8701 -> 8701
```

### `k-4-d-4/task_10.json`
- Reason: 4 node answer(s) differ only by formatting/type/order/case
```text
node 6 FORMAT_ONLY: 130 -> 130
node 7 FORMAT_ONLY: 19 -> 19
node 8 FORMAT_ONLY: 12 -> 12
node 9 FORMAT_ONLY: 14 -> 14
```

### `k-4-d-4/task_11.json`
- Reason: 4 node answer(s) differ only by formatting/type/order/case
```text
node 6 FORMAT_ONLY: 288 -> 288
node 7 FORMAT_ONLY: 91 -> 91
node 8 FORMAT_ONLY: 81 -> 81
node 9 FORMAT_ONLY: 16 -> 16
```

### `k-4-d-5/task_5.json`
- Reason: 1 node answer(s) differ only by formatting/type/order/case
```text
node 6 FORMAT_ONLY: ["Tarrant", "Travis"] -> ["TRAVIS", "TARRANT"]
```

### `k-5-d-1/task_2.json`
- Reason: 2 node answer(s) differ only by formatting/type/order/case
```text
node 3 FORMAT_ONLY: 4 -> 4
node 5 FORMAT_ONLY: 52 -> 52
```

### `k-5-d-2/task_2.json`
- Reason: 2 node answer(s) differ only by formatting/type/order/case
```text
node 5 FORMAT_ONLY: 82 -> 82
node 6 FORMAT_ONLY: 898 -> 898
```

### `k-5-d-3/task_9.json`
- Reason: 1 node answer(s) differ only by formatting/type/order/case
```text
node 11 FORMAT_ONLY: 4 -> 4
```

### `k-5-d-4/task_6.json`
- Reason: 6 node answer(s) differ only by formatting/type/order/case
```text
node 1 FORMAT_ONLY: ["Brownsville", "Pharr", "El Paso", "Laredo", "McAllen", "Mission", "Beaumont", "San Antonio", "Corpus Christi", "Edinburg"] -> ["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "McAllen", "Mission", "Pharr", "San Antonio"]
node 2 FORMAT_ONLY: ["Pharr", "Brownsville", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus Christi", "Houston", "Baytown", "Edinburg... -> ["Baytown", "Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Houston", "Laredo", "McAllen", "Mission", "Pharr...
node 3 FORMAT_ONLY: ["Brownsville", "Laredo", "Corpus Christi", "El Paso", "Pharr", "Beaumont", "McAllen", "San Antonio", "Mission", "Longview", "Hou... -> ["Beaumont", "Brownsville", "Corpus Christi", "El Paso", "Houston", "Laredo", "Longview", "McAllen", "Mission", "Pharr", "San Ant...
node 4 FORMAT_ONLY: ["Brownsville", "Pharr", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus Christi", "Edinburg", "San Antonio", "Lon... -> ["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "Longview", "McAllen", "Mission", "Pharr", "San An...
node 5 FORMAT_ONLY: ["Pharr", "Mission"] -> ["Mission", "Pharr"]
node 9 FORMAT_ONLY: 12.3 -> 12.3
```

### `k-6-d-2/task_2.json`
- Reason: 1 node answer(s) differ only by formatting/type/order/case
```text
node 4 FORMAT_ONLY: ["Ward 8 (37,124)", "Ward 7 (36,113)"] -> ["Ward 7 (36,113)", "Ward 8 (37,124)"]
```

### `k-6-d-3/task_3.json`
- Reason: 2 node answer(s) differ only by formatting/type/order/case
```text
node 11 FORMAT_ONLY: 4 -> 4
node 12 FORMAT_ONLY: 35503 -> 35503
```

### `k-6-d-3/task_5.json`
- Reason: 1 node answer(s) differ only by formatting/type/order/case
```text
node 8 FORMAT_ONLY: 16 -> 16
```

## Structural Only

- `k-4-d-4/task_14.json`: file exists only in tasks_mini copy; copy question: Across years 2015-16 to 2018-19, which Texas county is consistently in the top five for total lunch serves in Seamless Summer Option program? Among those counties, identify the two with the largest percentage decreases ...
- `k-5-d-2/task_11.json`: file exists only in tasks_mini; tasks_mini question: Find the New York counties (excluding NYC boroughs) satisfying both criteria: (1) average ratio of being sent back to jail between 38% and 40% in 2018-2019 in New York, and (2) average motor vehicle crashes above 15,000...

## No Answer Change

- `k-1-d-1/task_1.json`: node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-1-d-1/task_2.json`: node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-1-d-1/task_3.json`: question wording changed; node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-1/task_1.json`: node fields changed: fact:2, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-2/task_10.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-2/task_11.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-2/task_12.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-2/task_2.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-2/task_4.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-2/task_5.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-2/task_6.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-2/task_7.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-2/task_8.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-2/task_9.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-3/task_1.json`: question wording changed; node fields changed: fact:3, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-3/task_2.json`: question wording changed; node fields changed: fact:7, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-3/task_3.json`: node fields changed: depends_on:6, fact:4, subquestion:3; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-3/task_4.json`: node fields changed: fact:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-3/task_5.json`: node fields changed: fact:7, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-4/task_10.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-4/task_2.json`: node fields changed: fact:8, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-4/task_4.json`: node fields changed: fact:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-3-d-4/task_6.json`: node fields changed: fact:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-1/task_1.json`: datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-1/task_2.json`: node fields changed: subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-1/task_3.json`: node fields changed: subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-1/task_5.json`: datasets_used changed; reasoning_chain changed
- `k-4-d-1/task_6.json`: question wording changed; node fields changed: fact:4, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-2/task_1.json`: node fields changed: fact:1, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_10.json`: node fields changed: depends_on:6, fact:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_11.json`: question wording changed; node fields changed: depends_on:6, fact:4, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_12.json`: question wording changed; node fields changed: fact:2, subquestion:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_13.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_14.json`: question wording changed; node fields changed: fact:4, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-2/task_2.json`: question wording changed; node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_5.json`: question wording changed; node fields changed: fact:2, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_6.json`: question wording changed; node fields changed: fact:4, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_7.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_8.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_9.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-3/task_3.json`: question wording changed; node fields changed: fact:2, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-3/task_6.json`: question wording changed; node fields changed: subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_13.json`: question wording changed; node fields changed: subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_4.json`: question wording changed; node fields changed: limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_9.json`: node fields changed: fact:4, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-1/task_1.json`: question wording changed; node fields changed: fact:5, source:1, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-1/task_3.json`: node fields changed: fact:4, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-1/task_4.json`: question wording changed; node fields changed: fact:5, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-2/task_1.json`: question wording changed; node fields changed: fact:3, subquestion:6; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-3/task_4.json`: question wording changed; node fields changed: fact:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-3/task_6.json`: node fields changed: fact:3, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-3/task_8.json`: question wording changed; node fields changed: fact:10, limit:3, subquestion:11; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-4/task_9.json`: question wording changed; node fields changed: fact:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-6-d-3/task_1.json`: node fields changed: fact:4, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-6-d-3/task_4.json`: node fields changed: fact:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed