# Diff Classification By Answer Changes Only

Direction: `tasks_mini copy` -> `tasks_mini`.

## Criteria

- SUBSTANTIVE_ANSWER_CHANGE: top-level final `answer` changed, or at least one `nodes[*].answer` changed.
- NON_SUBSTANTIVE_UNDER_ANSWER_RULE: files differ, but neither final answer nor node/subquestion answers changed.
- STRUCTURAL_ONLY: file exists only on one side, so there is no paired answer comparison.

## Counts

- SUBSTANTIVE_ANSWER_CHANGE: 79
- NON_SUBSTANTIVE_UNDER_ANSWER_RULE: 55
- STRUCTURAL_ONLY: 2
- Files with final answer changed: 11
- Files with any node/subquestion answer changed: 77

## Substantive Answer Changes

### `k-2-d-3/task_1.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 1 answer: Edward -> 92
node 2 answer: 92 -> Edward
```
- Other differences also present: node fields changed: answer:2, fact:4, source:2, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-2/task_1.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: Charlie -> 1839
node 2 answer: 1 -> Charlie
node 3 answer: 1839 -> 1
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:4, source:3, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-2/task_3.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 1 answer: {"BRONX HIGH SCHOOL OF SCIENCE": 1.0, "BRONX SCHOOL OF LAW AND FINANCE": 6.0, "HIGH SCHOO... -> ["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "HIGH SCHOOL OF AMERICAN STUDIES AT...
node 2 answer: {"BRONX HIGH SCHOOL FOR MEDICAL SCIENCE": 8.0, "BRONX HIGH SCHOOL OF SCIENCE": 2.0, "MARB... -> ["MARBLE HILL HIGH SCHOOL FOR INTERNATIONAL STUDIES", "MARIE CURIE HIGH SCHOOL FOR NURSIN...
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:3, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-3/task_6.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 6 answer: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE... -> UNITED STATES PARK POLICE
```
- Other differences also present: node fields changed: answer:1, fact:6, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_1.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 5 answer: Chevy Chase -> Chevy Chase, Friendship Heights
node 6 answer: Chevy Chase, Maryland -> Montgomery County, Maryland
node 7 answer: Montgomery County -> 20
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:6, node_ids/count:1, source:2, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_3.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 8 answer: Whitman had population 47,973 -> Whitman had population 47,973 (lower than Kitsap's 275,611), county seat is Colfax
```
- Other differences also present: node fields changed: answer:1, fact:6, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-3-d-4/task_5.json`
- Reason: 5 node/subquestion answer(s) changed
```text
node 1 answer: ["Herbert H Lehman High School", "Susan E. Wagner High School", "Automotive High School"] -> ["Herbert H Lehman High School", "Jhs 13 Jackie Robinson", "Susan E. Wagner High School"]
node 3 answer: ["Susan E. Wagner High School", "Herbert H Lehman High School", "Sheepshead Bay High Scho... -> ["Brooklyn Secondary School for Collaborative Studies", "Susan E. Wagner High School", "H...
node 4 answer: ["Susan E. Wagner High School", "Richmond Hill High School", "Clara Barton High School"] -> ["Susan E. Wagner High School", "Richmond Hill High School", "Acad For College Prep & Car...
node 6 answer: Brooklyn Bridge -> ["Brooklyn Bridge", "Williamsburg Bridge", "George Washington Bridge", "Verrazzano-Narrow...
node 7 answer: Manhattan Bridge -> ["Verrazzano-Narrows Bridge", "Outerbridge Crossing", "Goethals Bridge", "Bayonne Bridge"]
```
- Other differences also present: final question wording changed; node fields changed: answer:5, fact:6, node_ids/count:1, source:2, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_7.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 6 answer: ["American Folk Art Museum", "American Museum of Natural History", "Children's Museum of ... -> ["American Museum of Natural History", "Lincoln Center for the Performing Arts"]
node 7 answer: 1961 -> ["American Museum of Natural History", "Metropolitan Museum of Art"]
```
- Other differences also present: final question wording changed; node fields changed: answer:2, depends_on:8, fact:8, node_ids/count:1, source:1, subquestion:3; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_8.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 1 answer: ["P.S. 005 Ellen Lurie", "P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 048 ... -> ["P.S. 005 ELLEN LURIE", "P.S. 008 LUIS BELLIARD", "P.S. 028 WRIGHT BROTHERS", "P.S. 048 ...
node 2 answer: ["Hamilton Heights School", "Muscota", "P.S. 004 Duke Ellington", "P.S. 005 Ellen Lurie",... -> ["P.S. 153 Adam Clayton Powell", "..."]
node 3 answer: ["P.S. 008 Luis Belliard", "P.S. 028 Wright Brothers", "P.S. 153 Adam Clayton Powell", "P... -> ["P.S. 153 Adam Clayton Powell", "..."]
node 4 answer: ["Hamilton Heights School", "P.S. 048 P.O. Michael J. Buczek", "P.S. 153 Adam Clayton Pow... -> ["P.S. 153 Adam Clayton Powell", "..."]
```
- Other differences also present: node fields changed: answer:4, fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-4/task_9.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 4 answer: ["Alabama", "Arizona", "Louisiana", "Missouri", "Oregon", "South Carolina", "Tennessee", ... -> ["Arizona", "Alabama", "Louisiana", "Tennessee", "Missouri", "Oregon", "South Carolina", ...
```
- Other differences also present: node fields changed: answer:1, fact:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-3-d-5/task_1.json`
- Reason: final answer changed; 7 node/subquestion answer(s) changed
```text
final answer: 1693 -> Friesland
node 1 answer: ["MANHATTAN BRIDGES HIGH SCHOOL", "BEDFORD ACADEMY HIGH SCHOOL", "MARBLE HILL HIGH SCHOOL... -> ["Manhattan Bridges High School", "Bedford Academy High School", "Marble Hill High School...
node 2 answer: ["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATH... -> ["Brooklyn International High School", "Gregorio Luperon High School", "High School for C...
node 3 answer: ["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PR... -> ["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Pr...
node 4 answer: ["Theatre Arts Production Company School", "Brooklyn International High School at Water's... -> ["Theatre Arts Production Company School", "Brooklyn International High School", "William...
node 5 answer: ["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village A... -> ["Brooklyn International High School", "Manhattan Village Academy", "It Takes a Village A...
node 6 answer: ["Spuyten Duyvil", "Marble Hill"] -> Frederick Philipse
node 7 answer: King's Bridge -> Friesland
```
- Other differences also present: final question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:2, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-1/task_4.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: Wallops Flight Facility -> EAARL (Experimental Advanced Airborne Research Lidar)
node 2 answer: Accomack County -> Wallops Flight Facility
node 3 answer: Chincoteague -> Accomack County
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:3, node_ids/count:1, source:2, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-2/task_15.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 2 answer: Whitman County borders Idaho and had a 2020 population of 47,973, so it meets both criter... -> Whitman County: borders Idaho (YES, per adjacent counties list), population 47,973 (YES, ...
node 3 answer: Spokane County borders Idaho, but its 2020 population was 539,339, so it does not meet bo... -> Spokane County: borders Idaho (YES, per adjacent counties list), population 539,339 (NO, ...
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:5, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-2/task_3.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 5 answer: 7871 -> 7871
node 6 answer: 8701 -> 8701
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:6, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-2/task_4.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 2 answer: 2023-02-23T00:00:00 -> 2023-01-06T00:00:00
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:4, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_1.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: {"Magnet School for Science & Technology": 14, "PS 130 The Parkside": 13.1, "PS 172 Beaco... -> ["PS 321 William Penn", "PS 107 John W Kimball"]
node 2 answer: {"Magnet School of Math, Science and Design Techno": 21.2, "PS 130 The Parkside": 20.5, "... -> ["PS 321 William Penn", "PS 10 Magnet School"]
node 3 answer: {"Magnet School of Math, Science and Design Techno": 21.5, "PS 107 John W. Kimball": 17.8... -> ["PS 321 William Penn", "PS 10 Magnet School"]
```
- Other differences also present: final question wording changed; node fields changed: answer:3, depends_on:6, fact:4, limit:3, subquestion:6; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_10.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: ["Erie", "Monroe", "Westchester", "Onondaga", "Nassau"] -> ["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Nassau County"]
node 2 answer: ["Monroe", "Suffolk", "Erie", "Westchester", "Onondaga", "Orange", "Broome", "Albany", "N... -> ["Erie County", "Monroe County", "Westchester County", "Onondaga County", "Suffolk County...
node 3 answer: ["Suffolk", "Nassau", "Erie", "Monroe"] -> ["Suffolk County", "Nassau County", "Erie County", "Monroe County"]
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:3, limit:1, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_11.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: ["Marshall County", "Floyd County", "Clayton County", "Crawford County", "Des Moines Coun... -> ["Allamakee County", "Appanoose County", "Benton County", "Black Hawk County", "Butler Co...
node 2 answer: ["Fremont", "Poweshiek", "Guthrie", "Clarke", "Floyd", "Hamilton", "Pottawattamie", "Jasp... -> ["Adair County", "Allamakee County", "Audubon County", "Benton County", "Black Hawk Count...
node 3 answer: ["Polk", "Linn", "Scott", "Johnson", "Dallas", "Black Hawk", "Dubuque", "Woodbury", "Stor... -> ["Black Hawk County", "Scott County", "Dallas County", "Dubuque County", "Johnson County"...
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:3, limit:2, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_12.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 3 answer: {"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956} -> CORRECTIONS
```
- Other differences also present: node fields changed: answer:1, fact:1, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_2.json`
- Reason: 7 node/subquestion answer(s) changed
```text
node 2 answer: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067"... -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 3 answer: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 046", "PS 054", "PS 056", "PS 067"... -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 4 answer: ["PS 003", "PS 009", "PS 011", "PS 016", "PS 020", "PS 054", "PS 056", "PS 067", "PS 256"... -> ["PS 003", "PS 009", "PS 011", "PS 046", "PS 056", "PS 067", "PS 270", "..."]
node 5 answer: ["PS 003", "PS 011", "PS 046", "PS 054", "PS 056", "PS 256", "PS 270"] -> ["PS 003 The Bedford Village", "PS 011 Purvis J. Behan", "PS 046 Edward C. Blum", "PS 054...
node 6 answer: {"Ps 11 Purvis J Behan": 24, "Ps 256 Benjamin Banneker": 2, "Ps 270 Joanne Dekalb": 4, "P... -> {"PS 003 The Bedford Village": 7, "PS 009 Teunis G. Bergen": 13, "PS 011 Purvis J. Behan"...
node 7 answer: {"Ps 11 Purvis J Behan": 15, "Ps 256 Benjamin Banneker": 13, "Ps 270 Johann Dekalb": 5, "... -> {"PS 003 The Bedford Village": 6, "PS 009 Teunis G. Bergen": 5, "PS 011 Purvis J. Behan":...
node 8 answer: {"Ps 11 Purvis J Behan": 22, "Ps 256 Benjamin Banneker": 7, "Ps 270 Johann Dekalb": 4, "P... -> {"PS 003 The Bedford Village": 12, "PS 009 Teunis G. Bergen": 4, "PS 011 Purvis J. Behan"...
```
- Other differences also present: node fields changed: answer:7, fact:7, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-3/task_4.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 1 answer: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "METROPOLITAN POLICE...
node 2 answer: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHOR... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 2", "D.C. HOUSING AUTHOR...
node 3 answer: ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE... -> ["DEPARTMENT OF PUBLIC WORKS", "METROPOLITAN POLICE DPT-DISTRICT 7", "METROPOLITAN POLICE...
node 6 answer: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE... -> UNITED STATES PARK POLICE
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:6, limit:3, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_5.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 3 answer: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE... -> UNITED STATES PARK POLICE
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_7.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 6 answer: Ulster County -> Ulster County, New York
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:4, source:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_8.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: ["BROOKLYN INTERNATIONAL HIGH SCHOOL", "GREGORIO LUPERON HIGH SCHOOL FOR SCIENCE AND MATH... -> ["Brooklyn International High School", "Gregorio Luperon High School", "High School for C...
node 2 answer: ["HIGH SCHOOL OF HOSPITALITY MANAGEMENT", "BEDFORD ACADEMY HIGH SCHOOL", "WILLIAMSBURG PR... -> ["High School of Hospitality Management", "Bedford Academy High School", "Williamsburg Pr...
node 3 answer: ["Theatre Arts Production Company School", "Brooklyn International High School at Water's... -> ["Theatre Arts Production Company School", "Brooklyn International High School", "William...
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:3, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-3/task_9.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: ["Suffolk", "Monroe", "Westchester", "Onondaga", "Nassau"] -> ["Suffolk County", "Monroe County", "Westchester County", "Onondaga County", "Nassau Coun...
node 2 answer: ["ERIE", "ONONDAGA", "SUFFOLK", "ONEIDA", "MONROE"] -> ["Erie County", "Onondaga County", "Suffolk County", "Oneida County", "Monroe County"]
node 3 answer: ["Monroe", "Erie", "Westchester", "Suffolk", "Nassau", "Onondaga"] -> ["Monroe County", "Erie County", "Westchester County", "Suffolk County", "Nassau County",...
node 4 answer: ["Suffolk", "Onondaga", "Westchester"] -> ["Suffolk County", "Onondaga County"]
node 5 answer: ["Monroe", "Nassau", "Onondaga"] -> ["Monroe County", "Onondaga County"]
node 6 answer: ["Erie", "Monroe", "Onondaga", "Westchester"] -> ["Monroe County", "Onondaga County"]
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_1.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 5 answer: P.S. 380 John Wayne Elementary -> ["P.S. 380 John Wayne Elementary", "P.S. 172 Beacon School of Excellence"]
node 6 answer: 10/28 -> P.S. 380 John Wayne Elementary
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:2, node_ids/count:1, source:2, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_10.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 6 answer: 130 -> 130
node 7 answer: 19 -> 19
node 8 answer: 12 -> 12
node 9 answer: 14 -> 14
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:4, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_11.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 6 answer: 288 -> 288
node 7 answer: 91 -> 91
node 8 answer: 81 -> 81
node 9 answer: 16 -> 16
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:4, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_12.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 5 answer: ["Nueces", "Denton"] -> ["DENTON", "NUECES"]
node 8 answer: Henry Lawrence Kinney -> Fort Worth
node 9 answer: 1850 -> Henry Lawrence Kinney
```
- Other differences also present: node fields changed: answer:3, fact:5, node_ids/count:1, source:2, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_2.json`
- Reason: 5 node/subquestion answer(s) changed
```text
node 1 answer: {"Abraham Lincoln Elementary School": "610038", "Alexander Graham Bell Elementary School"... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "an...
node 2 answer: {"Addams": "609772", "Armstrong, G": "609779", "Clissold": "609861", "Dixon": "609887", "... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "an...
node 3 answer: {"Amos Alonzo Stagg Elementary School": "610339", "Arthur R Ashe Elementary School": "610... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "an...
node 4 answer: {"ASHE": "610268", "BRUNSON": "609830", "CALMECA": "610353", "CLINTON": "609859", "CURTIS... -> {"Cleveland": "609857", "Hawthorne": "609974", "Poe": "610132", "Reinberg": "610145", "an...
node 5 answer: {"CLEVELAND": "IRVING PARK", "HAWTHORNE": "LAKE VIEW", "POE": "PULLMAN", "REINBERG": "POR... -> {"Cleveland": "Irving Park", "Hawthorne": "Lake View", "Poe": "Pullman", "Reinberg": "Por...
```
- Other differences also present: final question wording changed; node fields changed: answer:5, fact:7, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_3.json`
- Reason: 5 node/subquestion answer(s) changed
```text
node 1 answer: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S... -> {"J.H.S. 067 Louis Pasteur": "26Q067, 84 offers", "J.H.S. 074 Nathaniel Hawthorne": "26Q0...
node 2 answer: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S...
node 3 answer: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S...
node 4 answer: {"EAST SIDE MIDDLE SCHOOL": "02M114", "J.H.S. 054 BOOKER T. WASHINGTON": "03M054", "J.H.S... -> {"J.H.S. 067 Louis Pasteur": "26Q067", "J.H.S. 074 Nathaniel Hawthorne": "26Q074", "J.H.S...
node 9 answer: No, he was an education/governance figure -> 1887
```
- Other differences also present: node fields changed: answer:5, fact:6, limit:4, node_ids/count:1, source:1, subquestion:2; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_5.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 1 answer: {"CORRECTIONS": 279877976.24, "ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HEALT... -> {"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV...
node 2 answer: {"CORRECTIONS": 279260171.22, "ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HEALT... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV...
node 3 answer: {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HEALTH AND SENIOR SERVICES": 81563... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV...
node 4 answer: {"CORRECTIONS": 268435627.28, "ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HEALT... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV...
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:2, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_6.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 2 answer: {"BEXAR": 269462082.97, "DALLAS": 838316444.65, "DENTON": 186170844.17, "EL PASO": 123694... -> {"Bexar": 269462082.97, "Dallas": 838316444.65, "Harris": 1303630847.3, "Montgomery": 424...
node 3 answer: {"BEXAR": 302940592.72, "DALLAS": 827510409.8, "DENTON": 260841655.76, "HARRIS": 13917798... -> {"Bexar": 302940592.72, "Dallas": 827510409.8, "Harris": 1391779835.06, "Montgomery": 416...
node 4 answer: {"BEXAR": 494340352.72, "DALLAS": 1324261419.12, "DENTON": 355805325.9, "HARRIS": 1663151... -> {"Bexar": 494340352.72, "Dallas": 1324261419.12, "Harris": 1663151150.96, "Montgomery": 6...
node 5 answer: {"BEXAR": 596386366.99, "DALLAS": 1171406639.17, "DENTON": 412077419.13, "EL PASO": 14486... -> {"Bexar": 596386366.99, "Dallas": 1171406639.17, "Harris": 1741663003.68, "Montgomery": 7...
```
- Other differences also present: node fields changed: answer:4, fact:9, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_7.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 1 answer: {"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47000000003, "Avia... -> {"Administrative Hearings": 4367.66, "Animal Care and Control": 463673.47, "Aviation": 19...
node 2 answer: {"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.0... -> {"BOARD OF ELECTION COMMISSIONERS": 415998.4, "CHICAGO ANIMAL CARE AND CONTROL": 517835.0...
node 3 answer: {"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605.... -> {"BOARD OF ELECTION COMMISSIONERS": 721104.36, "CHICAGO ANIMAL CARE AND CONTROL": 337605....
node 4 answer: {"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4... -> {"Board of Election Commissioners": 58463.48, "Chicago Animal Care and Control": 378040.4...
```
- Other differences also present: node fields changed: answer:4, fact:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-4/task_8.json`
- Reason: 8 node/subquestion answer(s) changed
```text
node 1 answer: ["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead... -> ["ARAMARK UNIFORM SERVICES, INC.", "McGranahan Architects", "Schreiber Starling Whitehead...
node 2 answer: ["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "Imagesource Inc", "WSP USA Inc... -> ["A-1 Performance Inc", "Jacobs Engineering Group, Inc.", "WSP USA Inc.", "Imagesource In...
node 3 answer: ["Sharp Electronics Corporation", "DOC Correctional Industries", "A-1 Performance Inc", "... -> ["Sharp Electronics Corporation", "DOC Correctional Industries", "WSP USA Inc.", "A-1 Per...
node 4 answer: ["JP Morgan Chase Bank NA", "Washington State University", "Washington State Department o... -> ["JP Morgan Chase Bank NA", "WSP USA Inc.", "University of Washington", "WA State DSHS", ...
node 5 answer: 1885 -> Omaha, Nebraska; 1917
node 6 answer: Omaha, Nebraska; 1917 -> 1947
node 7 answer: 1947 -> 1914
node 8 answer: ["WSP USA Inc.", "HDR Engineering, Inc."] -> ["HDR Engineering, Inc.", "HNTB Corporation"]
```
- Other differences also present: final question wording changed; node fields changed: answer:8, fact:8, source:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_1.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: ["Jefferson", "St. Lawrence", "Cayuga", "Otsego", "Suffolk", "Tompkins"] -> ["Jefferson County", "St. Lawrence County", "Tompkins County", "Suffolk County", "Otsego ...
node 2 answer: ["Monroe", "Erie", "Nassau", "Westchester", "Niagara", "Sullivan", "Chautauqua", "Onondag... -> ["Monroe County", "Erie County", "Nassau County", "Westchester County", "Sullivan County"...
node 3 answer: ["Suffolk", "Nassau", "Monroe", "Westchester", "Erie", "Essex", "Onondaga", "Ulster", "Or... -> ["Suffolk County", "Nassau County", "Westchester County", "Monroe County", "Erie County",...
node 4 answer: ["Tompkins", "Cattaraugus", "Rockland", "Erie", "Schuyler", "Jefferson", "Livingston/Wyom... -> ["Tompkins County", "Cattaraugus County", "Rockland County", "Erie County", "Schuyler Cou...
node 5 answer: ["Chautauqua", "Rensselaer", "Jefferson", "Ulster", "Saint Lawrence", "Steuben", "Wayne",... -> ["Chautauqua County", "Rensselaer County", "Jefferson County", "Ulster County", "Saint La...
node 8 answer: Jefferson -> Jefferson County
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:8, limit:3, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_2.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: ["Salvatore Albanese", "Anthony Andrews, Jr.", "JoAnn Ariola", "Paul Bader", "Maria Baez"... -> ["Domenic Recchia", "Leroy Comrie", "103 others"]
node 2 answer: ["Joseph Addabbo", "Tony Avella", "Maria Baez", "Ismael Betancourt Jr", "Omar Boucher", "... -> ["Domenic Recchia", "Leroy Comrie", "45 others"]
node 3 answer: ["Tony Avella", "Albert Baldeo", "Charles Barron", "Ismael Betancourt Jr", "Michael Beys"... -> ["Domenic Recchia", "Leroy Comrie", "67 others"]
node 4 answer: ["Isaac Abraham", "Maria Arroyo", "Maria Baez", "Steven Anthony Behar", "Victor Bernace",... -> ["Domenic Recchia", "Leroy Comrie", "97 others"]
node 5 answer: ["Olanike Alabi", "Pedro Alvarez", "Maria Arroyo", "Christopher Banks", "Raquel Batista",... -> ["Domenic Recchia", "Leroy Comrie", "91 others"]
node 8 answer: {"Brooklyn": 3889.0, "Queens": 1019.0} -> Brooklyn
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:9, limit:5, subquestion:9; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_3.json`
- Reason: 5 node/subquestion answer(s) changed
```text
node 1 answer: {"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 58421... -> {"ACETAMINOP": 7414105, "ALPRAZOLAM": 9133057, "AMITRIPTYL": 5232115, "ARIPIPRAZO": 58421...
node 2 answer: {"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 69271... -> {"ALPRAZOLAM": 7934584, "AMITRIPTYL": 5072673, "ARIPIPRAZO": 6707069, "BUPRENORPH": 69271...
node 3 answer: {"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 91871... -> {"ALPRAZOLAM": 7857439, "ARIPIPRAZO": 7935761, "AZITHROMYC": 9749242, "BUPRENORPH": 91871...
node 4 answer: {"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE": 934196... -> {"ALPRAZOLAM": 7881792, "ARIPIPRAZO": 8697286, "BUPRENORPH": 9827552, "BUSPIRONE ": 93419...
node 5 answer: {"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 83530... -> {"ACETAMINOP": 6467768, "ALPRAZOLAM": 7550347, "ARIPIPRAZO": 9245571, "CEPHALEXIN": 83530...
```
- Other differences also present: final question wording changed; node fields changed: answer:5, fact:9, limit:5, subquestion:10; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-4-d-5/task_4.json`
- Reason: 8 node/subquestion answer(s) changed
```text
node 1 answer: {"BEXAR": 622, "CAMERON": 455, "DALLAS": 1207, "EL PASO": 459, "FORT BEND": 150, "HARRIS"... -> {"BEXAR": 622, "DALLAS": 1207, "HARRIS": 1781, "HIDALGO": 878, "OTHER_COUNTIES": 190, "TA...
node 2 answer: {"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "EL PASO": 524, "HARRIS": 2179, "HIDALGO":... -> {"BEXAR": 888, "CAMERON": 592, "DALLAS": 1435, "HARRIS": 2179, "HIDALGO": 1203, "OTHER_CO...
node 3 answer: {"BELL": 188, "BEXAR": 756, "CAMERON": 418, "DALLAS": 1120, "EL PASO": 456, "FORT BEND": ... -> {"BEXAR": 756, "DALLAS": 1120, "HARRIS": 1709, "HIDALGO": 918, "OTHER_COUNTIES": 189, "TA...
node 4 answer: {"BEXAR": 772, "CAMERON": 417, "DALLAS": 1269, "EL PASO": 443, "FORT BEND": 212, "HARRIS"... -> {"BEXAR": 772, "DALLAS": 1269, "HARRIS": 1871, "HIDALGO": 924, "OTHER_COUNTIES": 188, "TA...
node 5 answer: {"BEXAR": 743, "CAMERON": 424, "DALLAS": 1352, "EL PASO": 452, "FORT BEND": 177, "HARRIS"... -> {"BEXAR": 743, "DALLAS": 1352, "HARRIS": 2183, "HIDALGO": 947, "OTHER_COUNTIES": 189, "TA...
node 6 answer: {"BEXAR": 13020, "COLLIN": 3526, "DALLAS": 14192, "DENTON": 3761, "EL PASO": 4709, "HARRI... -> ["Tarrant", "Bexar", "Hidalgo"]
node 7 answer: {"BELL": 470, "BEXAR": 1074, "DALLAS": 738, "HARRIS": 566, "LUBBOCK": 194, "MCLENNAN": 17... -> ["Bexar", "Dallas"]
node 10 answer: 25 -> 1836
```
- Other differences also present: final question wording changed; node fields changed: answer:8, fact:9, limit:7, subquestion:9; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-4-d-5/task_5.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 6 answer: ["Tarrant", "Travis"] -> ["TRAVIS", "TARRANT"]
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:10, subquestion:10; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-1/task_2.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 3 answer: 4 -> 4
node 5 answer: 52 -> 52
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:5, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-2/task_10.json`
- Reason: final answer changed; 8 node/subquestion answer(s) changed
```text
final answer: 1653 -> 1724
node 1 answer: {"ALBANY": "43.0%", "ALLEGANY": "47.2%", "BROOME": "46.0%", "CATTARAUGUS": "33.0%", "CAYU... -> ["Compton", "San Bernardino"]
node 2 answer: {"ALBANY": "34.1%", "ALLEGANY": "26.3%", "BROOME": "36.6%", "CATTARAUGUS": "33.3%", "CAYU... -> ["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Sant...
node 3 answer: {"ALBANY": "9930", "ALLEGANY": "1322", "BROOME": "5401", "CATTARAUGUS": "1950", "CAYUGA":... -> Los Angeles County
node 4 answer: {"ALBANY": "7564", "ALLEGANY": "1061", "BROOME": "4367", "CATTARAUGUS": "1631", "CAYUGA":... -> San Bernardino County
node 5 answer: Erie tribe of Native Americans -> 1850
node 6 answer: James Monroe, the fifth president of the United States -> 1853
node 7 answer: Westmoreland County, Virginia -> Felipe de Neve
node 8 answer: 1653 -> 1724
```
- Other differences also present: final question wording changed; node fields changed: answer:8, fact:8, limit:4, source:8, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-2/task_2.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 5 answer: 82 -> 82
node 6 answer: 898 -> 898
```
- Other differences also present: node fields changed: answer:2, fact:4, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_3.json`
- Reason: final answer changed; 6 node/subquestion answer(s) changed
```text
final answer: Pittsburgh, Pennsylvania -> Gulf of Mexico
node 1 answer: {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9} -> {"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}
node 2 answer: {"Detroit": 47.4, "Flint": 45.4, "Gary": 49.0} -> {"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}
node 3 answer: U.S. Steel Corporation -> {"Cameron": 7620183, "Hidalgo": 1661128}
node 4 answer: Carnegie Steel Company -> {"Cameron": 1076746, "Hidalgo": 1477805}
node 5 answer: Andrew Carnegie -> Brownsville
node 6 answer: Pittsburgh, Pennsylvania -> Gulf Coast
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_4.json`
- Reason: final answer changed; 6 node/subquestion answer(s) changed
```text
final answer: San Antonio Bay -> Pittsburgh, Pennsylvania
node 1 answer: ["Victoria", "Comal", "Willacy", "Brooks"] -> {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}
node 2 answer: ["Comal", "Victoria", "Atascosa", "Willacy"] -> {"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}
node 3 answer: ["Victoria County, TX", "Comal County, TX"] -> U.S. Steel Corporation
node 4 answer: ["Willacy County, TX", "Victoria County, TX"] -> Carnegie Steel Company
node 5 answer: Victoria -> Andrew Carnegie
node 6 answer: Guadalupe River -> Pittsburgh, Pennsylvania
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_5.json`
- Reason: final answer changed; 7 node/subquestion answer(s) changed
```text
final answer: 1735 -> San Antonio Bay
node 1 answer: ["Ward 7 (42,226)", "Ward 8 (34,959)"] -> ["Brooks County", "Willacy County", "Comal County", "Victoria County"]
node 2 answer: ["Ward 8 (37,124)", "Ward 7 (36,113)"] -> ["Willacy County", "Comal County", "Atascosa County", "Victoria County"]
node 3 answer: Wendell Felder -> ["Victoria County", "Comal County"]
node 4 answer: Georgetown University -> ["Willacy County", "Victoria County"]
node 5 answer: John Carroll -> Victoria
node 6 answer: Patrick Francis Healy -> Guadalupe River
node 7 answer: 1735 -> San Antonio Bay
```
- Other differences also present: final question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:7, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_6.json`
- Reason: final answer changed; 6 node/subquestion answer(s) changed
```text
final answer: 99357947 -> 1735
node 1 answer: U.S. Steel Corporation -> ["Ward 7 (42,226)", "Ward 8 (34,959)"]
node 2 answer: Carnegie Steel Company -> ["Ward 7 (36,113)", "Ward 8 (37,124)"]
node 3 answer: Andrew Carnegie -> Wendell Felder
node 4 answer: Pittsburgh, Pennsylvania -> Georgetown University
node 5 answer: 98453962.68 -> John Carroll
node 6 answer: 100261931.64 -> Patrick Francis Healy
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_7.json`
- Reason: final answer changed; 6 node/subquestion answer(s) changed
```text
final answer: Elihu Yale -> 99357947
node 1 answer: {"Fairfield County": 208, "Hartford County": 335, "New Haven County": 383} -> U.S. Steel Corporation
node 2 answer: ["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"] -> Carnegie Steel Company
node 3 answer: New Haven -> Andrew Carnegie
node 4 answer: Bridgeport -> Pittsburgh, Pennsylvania
node 5 answer: {"Bridgeport": "16.9%", "New Haven": "13.9%"} -> {"2017": "$98,453,962.68"}
node 6 answer: {"Bridgeport": "19.3%", "New Haven": "15.4%"} -> {"2018": "$100,261,931.64"}
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, node_ids/count:1, source:6, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-2/task_8.json`
- Reason: final answer changed; 7 node/subquestion answer(s) changed
```text
final answer: Gippeswic -> Elihu Yale
node 1 answer: {"Albany": "$19,408,513", "Dutchess": "$25,427,485", "Erie": "$70,519,223", "Monroe": "$4... -> ["New Haven County", "Hartford County", "Fairfield County"]
node 2 answer: {"Albany": "$19,977,245", "Dutchess": "$23,872,388", "Erie": "$81,139,374", "Monroe": "$5... -> ["Fairfield County", "New Haven County", "Middlesex County", "Litchfield County"]
node 3 answer: {"Erie": "621,451,910.24", "Suffolk": "537,382,172"} -> New Haven
node 4 answer: {"Erie": "712,460,330.24", "Suffolk": "556,444,750"} -> Bridgeport
node 5 answer: Suffolk, England -> {"Bridgeport": "16.9%", "New Haven": "13.9%"}
node 6 answer: Ipswich -> {"Bridgeport": "19.3%", "New Haven": "15.4%"}
node 7 answer: Gippeswic -> Yale University
```
- Other differences also present: final question wording changed; node fields changed: answer:7, fact:7, limit:2, node_ids/count:1, source:7, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-2/task_9.json`
- Reason: final answer changed; 7 node/subquestion answer(s) changed
```text
final answer: 1724 -> Gippeswic
node 1 answer: ["San Bernardino", "Compton"] -> {"Erie": "$70,519,223", "Suffolk": "$92,420,995", "Westchester": "$66,346,132"}
node 2 answer: ["Compton", "Hesperia", "Lynwood", "Merced", "Perris", "Salinas", "San Bernardino", "Sant... -> {"Erie": "$81,139,374", "Suffolk": "$87,249,830", "Westchester": "$67,149,496"}
node 3 answer: Los Angeles County -> {"Erie": "621,451,910.24", "Suffolk": "537,382,172"}
node 4 answer: San Bernardino County -> {"Erie": "712,460,330.24", "Suffolk": "556,444,750"}
node 5 answer: 1850 -> Suffolk, England
node 6 answer: 1853 -> Ipswich
node 7 answer: Felipe de Neve -> Gippeswic
```
- Other differences also present: final question wording changed; node fields changed: answer:7, fact:7, node_ids/count:1, source:7, subquestion:7; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed

### `k-5-d-3/task_1.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 2 answer: ["02M047 - 47 THE AMERICAN SIGN LANGUAGE AND ENGLISH SECONDARY SCHOOL", "02M288 - FOOD AN... -> ["02M288 - FOOD AND FINANCE HIGH SCHOOL", "02M294 - ESSEX STREET ACADEMY", "02M296 - HIGH...
node 3 answer: ["02M047 - 47 The American Sign Language and English Secondary School", "02M288 - Food an... -> ["02M288 - Food and Finance High School", "02M294 - Essex Street Academy", "02M296 - High...
node 4 answer: Eleanor Roosevelt High School -> ["Eleanor Roosevelt High School"]
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:8, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_10.json`
- Reason: final answer changed
```text
final answer: Ward 5 -> Swartekill, New York
```
- Other differences also present: final question wording changed; node fields changed: fact:9, node_ids/count:1, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_11.json`
- Reason: 9 node/subquestion answer(s) changed
```text
node 1 answer: {"Ward 2": 8286, "Ward 4": 6971, "Ward 5": 6580, "Ward 6": 8371} -> {"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685}
node 2 answer: {"Ward 2": 8392, "Ward 4": 6525, "Ward 5": 6072, "Ward 6": 6845} -> {"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281}
node 3 answer: {"Ward 2": 7897, "Ward 4": 6856, "Ward 5": 6213, "Ward 6": 6658} -> {"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549}
node 4 answer: {"Ward 2": 4794, "Ward 4": 2547, "Ward 5": 4497, "Ward 6": 3685} -> {"Ward 2": 72, "Ward 5": 80}
node 5 answer: {"Ward 2": 5469, "Ward 4": 3135, "Ward 5": 5629, "Ward 6": 4281} -> {"Ward 2": 54, "Ward 5": 83}
node 6 answer: {"Ward 2": 4420, "Ward 4": 2595, "Ward 5": 4585, "Ward 6": 3549} -> {"Ward 2": 54, "Ward 5": 87}
node 7 answer: {"Ward 2": 72, "Ward 5": 80} -> Sojourner Truth PCS
node 8 answer: {"Ward 2": 54, "Ward 5": 83} -> Swartekill, New York
... 1 more node answer changes
```
- Other differences also present: final question wording changed; node fields changed: answer:9, fact:9, node_ids/count:1, source:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_12.json`
- Reason: 7 node/subquestion answer(s) changed
```text
node 1 answer: ["University of Washington", "Washington State University", "Western Washington Universit... -> Seattle Community College - District 6: 1,308; Green River Community College: 1,723; Comm...
node 2 answer: {"Central Washington University": 223, "Eastern Washington University": 840, "Evergreen S... -> Seattle Colleges: 1,292; Green River Community College: 633; Community Colleges of Spokan...
node 3 answer: {"Central Washington University": 274, "Eastern Washington University": 600, "Evergreen S... -> Seattle Community College - District 6: 5,244; Green River Community College: 872; Commun...
node 4 answer: {"Central Washington University": 362, "Eastern Washington University": 505, "Evergreen S... -> Seattle Colleges is located in Seattle, Washington
node 5 answer: University of Washington is located in Seattle, Washington -> Green River College is located in Auburn, Washington
node 6 answer: Eastern Washington University is located in Cheney, Washington -> Community Colleges of Spokane is located in Spokane, Washington
node 9 answer: [{"BuildingName": "BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus", "avg_Tota... -> BOEING PLANT 2 ISAL (BLDG 2-122)-North Boeing Field Campus with 20,835.8 metric tons CO2e...
```
- Other differences also present: final question wording changed; node fields changed: answer:7, fact:7, limit:4, source:6, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_13.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 4 answer: ["Los Angeles County", "San Diego County", "Orange County"] -> Los Angeles County; San Diego County; Orange County
node 5 answer: ["Los Angeles County", "Orange County", "San Diego County"] -> Los Angeles County; Orange County; San Diego County
node 6 answer: ["Los Angeles County", "San Diego County", "San Bernardino County"] -> Los Angeles County; San Diego County; San Bernardino County
node 7 answer: 71 -> 71
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:5, limit:3, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_14.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 4 answer: ["Polk County", "Linn County", "Scott County"] -> Polk County; Linn County; Scott County
node 5 answer: ["Polk County", "Linn County", "Sioux County"] -> Polk County; Linn County; Sioux County
node 6 answer: ["Linn County", "Polk County", "Pottawattamie County"] -> Linn County; Polk County; Pottawattamie County
node 7 answer: 7 -> 7
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:5, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_15.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 2 answer: ["OFFICE OF GOVERNOR", "OFFICE OF ATTORNEY GENERAL", "JUDICIARY", "OFFICE OF STATE AUDITO... -> ["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR", "OFFICE OF ADMINISTRATION"]
node 3 answer: ["OFFICE OF STATE AUDITOR", "OFFICE OF GOVERNOR", "OFFICE OF LIEUTENANT GOVERNOR", "OFFIC... -> ["OFFICE OF ATTORNEY GENERAL", "OFFICE OF STATE AUDITOR"]
node 9 answer: 2705988 -> 2705988
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:4, limit:3, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_2.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: {"BEXAR": 14728288130.02, "DALLAS": 21393532327.19, "EL PASO": 5336100417.92, "FORT BEND"... -> Travis: $29.37B; Harris: $28.16B; Dallas: $21.39B
node 2 answer: {"BEXAR": 7513472495.969999, "DALLAS": 10578598198.67, "EL PASO": 2697075449.58, "FORT BE... -> Travis: $16.34B; Harris: $14.99B; Dallas: $10.58B
node 3 answer: {"BEXAR": 8839835949.14, "DALLAS": 12496129391.79, "EL PASO": 3075321686.73, "FORT BEND":... -> Travis: $16.76B; Harris: $16.45B; Dallas: $12.50B
node 10 answer: {"ALDINE ISD": 67.1557142857143, "ALIEF ISD": 64.05813953488372, "CHANNELVIEW ISD": 59.62... -> Sheldon ISD: 81.47% average ISP
node 11 answer: {"ALDINE ISD": 66.54481481481481, "ALIEF ISD": 65.68209302325582, "CHANNELVIEW ISD": 59.4... -> Sheldon ISD: 60.66% average ISP
node 12 answer: {"ALDINE ISD": 65.33134146341463, "ALIEF ISD": 63.437441860465114, "CHANNELVIEW ISD": 64.... -> Sheldon ISD: 66.11% average ISP
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:6, limit:6, subquestion:13; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_3.json`
- Reason: 10 node/subquestion answer(s) changed
```text
node 1 answer: ["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"] -> Harris: 9,029; Dallas: 5,355; Tarrant: 4,769
node 2 answer: ["Harris", "Dallas", "Tarrant", "Bexar", "Travis"] -> Harris: 7,059; Dallas: 4,540; Tarrant: 4,450
node 3 answer: ["Harris", "Dallas", "Tarrant", "Bexar", "Hidalgo"] -> Harris: 5,210; Dallas: 3,565; Tarrant: 3,252
node 7 answer: San Antonio is the county seat of Bexar County -> Houston was founded on August 30, 1836
node 8 answer: Houston was founded on August 30, 1836 -> Dallas was established in 1841
node 9 answer: Dallas was established in 1841 -> Fort Worth was established in 1849
node 10 answer: Fort Worth was established in 1849 -> Lake Worth ISD: 65.00% average ISP
node 11 answer: San Antonio was established in 1718 -> Lake Worth ISD: 65.94% average ISP
... 2 more node answer changes
```
- Other differences also present: final question wording changed; node fields changed: answer:10, fact:10, limit:2, node_ids/count:1, source:7, subquestion:13; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_5.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 3 answer: {"CORRECTIONS": 13107, "SOCIAL SERVICES": 8932, "TRANSPORTATION": 6956} -> CORRECTIONS
```
- Other differences also present: node fields changed: answer:1, fact:3, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_7.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 3 answer: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE... -> UNITED STATES PARK POLICE
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:5, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-3/task_9.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 11 answer: 4 -> 4
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:11, limit:9, subquestion:11; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_1.json`
- Reason: 5 node/subquestion answer(s) changed
```text
node 1 answer: {"Erie County": 82, "Orange County": 67, "Ulster County": 84, "Westchester County": 68} -> ["Ulster County", "Erie County", "Westchester County", "Orange County"]
node 2 answer: {"Erie County": 91, "Nassau County": 70, "Oneida County": 50, "Onondaga County": 53, "Ora... -> ["Suffolk County", "Erie County", "Nassau County", "Westchester County", "Onondaga County...
node 3 answer: {"Albany County": 148, "Bronx County": 158, "Dutchess County": 125, "Erie County": 244, "... -> ["New York County", "Nassau County", "Suffolk County", "Queens County", "Kings County", "...
node 4 answer: {"Albany County": 20.0, "Broome County": 111.8, "Chautauqua County": 185.9, "Chenango Cou... -> ["Steuben County", "Chautauqua County", "Lewis County", "Livingston County", "Montgomery ...
node 7 answer: {"Erie County": 3493, "Westchester County": 1520} -> Erie County
```
- Other differences also present: node fields changed: answer:5, fact:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_2.json`
- Reason: 8 node/subquestion answer(s) changed
```text
node 1 answer: {"AGRICULTURE": 31813546.32, "COMMERCE AND INSURANCE": 2009267.01, "CONSERVATION": 686481... -> {"ELEMENTARY AND SECONDARY EDUCATION": 4893252163.41, "HIGHER EDUCATION AND WORKFORCE DEV...
node 2 answer: {"AGRICULTURE": 37088287.9, "COMMERCE AND INSURANCE": 6346960.76, "CONSERVATION": 7146708... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5048553721.08, "HIGHER EDUCATION AND WORKFORCE DEV...
node 3 answer: {"AGRICULTURE": 45903725.15, "COMMERCE AND INSURANCE": 6514041.0, "CONSERVATION": 6852844... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5170194688.51, "HIGHER EDUCATION AND WORKFORCE DEV...
node 4 answer: {"AGRICULTURE": 40395382.19, "COMMERCE AND INSURANCE": 5910088.04, "CONSERVATION": 619080... -> {"ELEMENTARY AND SECONDARY EDUCATION": 5351561573.54, "HIGHER EDUCATION AND WORKFORCE DEV...
node 9 answer: {"Administrative Hearings": 78.45, "Animal Care and Control": 490423.37, "Aviation": 1314... -> {"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}
node 10 answer: {"Animal Care and Control": 460788.49, "Aviation": 10028911.51, "Board of Election Commis... -> {"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}
node 11 answer: {"Animal Care and Control": 514031.65, "Aviation": 12881495.76, "Board of Election Commis... -> {"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}
node 12 answer: {"Administrative Hearings": 13472.0, "Animal Care and Control": 530063.0, "Aviation": 148... -> {"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}
```
- Other differences also present: node fields changed: answer:8, fact:12, subquestion:12; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_3.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 5 answer: {"Aviation": 13147383.4, "Fire": 63941565.36, "Police": 101460132.24, "Streets and Sanita... -> {"Fire": 63941565.36, "Police": 101460132.24, "Water Management": 23507061.7}
node 6 answer: {"Emergency Management and Communications": 10945883.57, "Fire": 43847384.3, "Police": 11... -> {"Fire": 43847384.3, "Police": 116144553.32, "Water Management": 19954056.68}
node 7 answer: {"Aviation": 12881495.76, "Fire": 50604010.67, "Police": 143032724.45, "Streets and Sanit... -> {"Fire": 50604010.67, "Police": 143032724.45, "Water Management": 21335912.52}
node 8 answer: {"Aviation": 14884756.0, "Fire": 49571354.0, "Police": 156732988.0, "Streets and Sanitati... -> {"Fire": 49571354, "Police": 156732988, "Water Management": 20049910}
```
- Other differences also present: node fields changed: answer:4, fact:9, limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_4.json`
- Reason: 8 node/subquestion answer(s) changed
```text
node 1 answer: ["HARRIS", "HIDALGO", "DALLAS", "CAMERON", "EL PASO"] -> ["Harris", "Hidalgo", "Dallas", "Cameron", "El Paso"]
node 2 answer: ["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"] -> ["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]
node 3 answer: ["HIDALGO", "HARRIS", "DALLAS", "CAMERON", "BEXAR"] -> ["Hidalgo", "Harris", "Dallas", "Cameron", "Bexar"]
node 4 answer: ["HIDALGO", "HARRIS", "DALLAS", "BEXAR", "CAMERON"] -> ["Hidalgo", "Harris", "Dallas", "Bexar", "Cameron"]
node 5 answer: {"BEXAR": 1805014.14, "COLLIN": 825207.4400000001, "DALLAS": 2835278.75, "DENTON": 882025... -> {"Cameron": 392489.51, "Dallas": 2835278.75, "Harris": 8757796.13, "Hidalgo": 1202699.73}
node 6 answer: {"BELL": 611323.37, "BEXAR": 1419344.89, "COLLIN": 832593.43, "DALLAS": 2393411.26, "DENT... -> {"Cameron": 330003.06, "Dallas": 2393411.26, "Harris": 7558597.77, "Hidalgo": 971063.56}
node 7 answer: {"BEXAR": 1579009, "CAMERON": 7620183, "DALLAS": 1615421, "EL PASO": 1586612, "HARRIS": 3... -> {"Cameron": 7620183, "Hidalgo": 1661128}
node 8 answer: {"BEXAR": 1602569, "BRAZORIA": 466678, "CAMERON": 1076746, "DALLAS": 1768090, "EL PASO": ... -> {"Cameron": 1076746, "Hidalgo": 1477805}
```
- Other differences also present: final question wording changed; node fields changed: answer:8, fact:10, limit:4, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_5.json`
- Reason: 8 node/subquestion answer(s) changed
```text
node 1 answer: {"BEE": 602056.1175, "BEXAR": 1976511.21, "CAMERON": 4343483.48, "DALLAS": 1337723.91, "E... -> {"Atascosa County": 141083.37, "Brooks County": 60454.65, "Comal County": 112322.52, "Vic...
node 2 answer: {"BEE": 570655.59, "BEXAR": 2001499.64, "CAMERON": 4324920.055, "DALLAS": 1544675.66, "EL... -> {"Atascosa County": 142115.25, "Brooks County": 66250.97, "Comal County": 88868.98, "Vict...
node 3 answer: {"BEE": 595756.985, "BEXAR": 2011461.89, "CAMERON": 4404181.145, "DALLAS": 1705207.2, "EL... -> {"Atascosa County": 139933.33, "Brooks County": 78426.43, "Comal County": 78748.11, "Vict...
node 4 answer: {"ATASCOSA": 52913.23, "BROOKS": 0.0, "COMAL": 37371.2, "VICTORIA": 40390.435, "WILLACY":... -> {"Atascosa County": 52913.23, "Brooks County": 0, "Comal County": 37371.2, "Victoria Coun...
node 5 answer: {"Atascosa": 0, "Brooks": 1, "Comal": 5, "Victoria": 6, "Willacy": 2} -> ["Brooks County", "Willacy County", "Comal County", "Victoria County"]
node 6 answer: {"Atascosa": 6, "Brooks": 1, "Comal": 16, "Victoria": 11, "Willacy": 3} -> ["Willacy County", "Comal County", "Atascosa County", "Victoria County"]
node 7 answer: {"Comal County, TX": 19.21235, "Victoria County, TX": 19.51998, "Willacy County, TX": 10.... -> ["Victoria County", "Comal County"]
node 8 answer: {"Comal County, TX": "14-15.9", "Victoria County, TX": "10-11.9", "Willacy County, TX": "... -> ["Willacy County", "Victoria County"]
```
- Other differences also present: node fields changed: answer:8, fact:10, limit:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_6.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: ["Brownsville", "Pharr", "El Paso", "Laredo", "McAllen", "Mission", "Beaumont", "San Anto... -> ["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "McAllen",...
node 2 answer: ["Pharr", "Brownsville", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus C... -> ["Baytown", "Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Houston"...
node 3 answer: ["Brownsville", "Laredo", "Corpus Christi", "El Paso", "Pharr", "Beaumont", "McAllen", "S... -> ["Beaumont", "Brownsville", "Corpus Christi", "El Paso", "Houston", "Laredo", "Longview",...
node 4 answer: ["Brownsville", "Pharr", "Laredo", "McAllen", "Mission", "El Paso", "Beaumont", "Corpus C... -> ["Beaumont", "Brownsville", "Corpus Christi", "Edinburg", "El Paso", "Laredo", "Longview"...
node 5 answer: ["Pharr", "Mission"] -> ["Mission", "Pharr"]
node 9 answer: 12.3 -> 12.3
```
- Other differences also present: node fields changed: answer:6, fact:9, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_7.json`
- Reason: 7 node/subquestion answer(s) changed
```text
node 1 answer: ["Blaine School District (Whatcom)", "Camas School District (Clark)", "Carbonado School D... -> ["Riverside School District (Spokane)", "Index Elementary School District 63 (Snohomish)"...
node 2 answer: ["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Is... -> ["Edmonds School District (Snohomish)", "Fife School District (Pierce)", "West Valley Sch...
node 3 answer: ["Adna School District (Lewis)", "Almira School District (Lincoln)", "Anacortes School Di... -> ["Enumclaw School District (King)", "Snohomish School District (Snohomish)", "Centralia S...
node 4 answer: ["Almira School District (Lincoln)", "Anacortes School District (Skagit)", "Bainbridge Is... -> ["University Place School District (Pierce)", "Enumclaw School District (King)", "Mercer ...
node 5 answer: ["Whitman", "Spokane"] -> Whitman and Spokane
node 8 answer: Pullman -> Pullman is the most populous city in Whitman County (2020 census), located in southeaster...
node 9 answer: 2941 -> 2941
```
- Other differences also present: node fields changed: answer:7, fact:9, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-5-d-4/task_8.json`
- Reason: 7 node/subquestion answer(s) changed
```text
node 1 answer: ["Bexar", "Hidalgo", "Travis", "El Paso", "Montgomery", "McLennan", "Collin", "Smith", "G... -> ["Bexar", "El Paso", "Hidalgo", "Montgomery", "Travis", "McLennan", "Collin", "Smith", "G...
node 4 answer: ["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "... -> ["Tarrant", "Dallas", "Bexar", "Hidalgo", "Montgomery", "Smith", "Jefferson", "Collin", "...
node 5 answer: ["Hidalgo", "El Paso", "Montgomery"] -> ["El Paso", "Hidalgo", "Montgomery"]
node 6 answer: Montgomery -> ["El Paso", "Hidalgo"]
node 7 answer: El Paso -> El Paso County is in West Texas
node 8 answer: Edinburg -> Hidalgo County is in South Texas, county seat is Edinburg
node 9 answer: University of Texas Rio Grande Valley -> University of Texas Rio Grande Valley (UTRGV)
```
- Other differences also present: node fields changed: answer:7, fact:9, limit:2, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_1.json`
- Reason: 3 node/subquestion answer(s) changed
```text
node 1 answer: ["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414"... -> ["01M450", "01M539", "02M288", "02M296", "02M298", "02M308", "02M411", "02M412", "02M414"...
node 2 answer: ["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407"... -> ["01M450", "01M539", "02M288", "02M296", "02M298", "02M303", "02M305", "02M308", "02M407"...
node 3 answer: 02M475 -> ["02M475"]
```
- Other differences also present: final question wording changed; node fields changed: answer:3, fact:4, limit:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed

### `k-6-d-2/task_2.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 4 answer: ["Ward 8 (37,124)", "Ward 7 (36,113)"] -> ["Ward 7 (36,113)", "Ward 8 (37,124)"]
```
- Other differences also present: final question wording changed; node fields changed: answer:1, fact:10, limit:4, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_3.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 1 answer: ["Erie", "Monroe"] -> ["Erie County", "Monroe County"]
node 8 answer: 359.8 -> 359.8
```
- Other differences also present: final question wording changed; node fields changed: answer:2, fact:8, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_4.json`
- Reason: 4 node/subquestion answer(s) changed
```text
node 1 answer: {"Camden, New Jersey": 42.2, "Cleveland, Ohio": 42.1, "Dayton, Ohio": 47.2, "Detroit, Mic... -> {"Dayton": 47.2, "Detroit": 45.2, "Gary": 46.9}
node 2 answer: {"Brownsville, Texas": 44.4, "Camden, New Jersey": 44.1, "Dayton, Ohio": 43.5, "Detroit, ... -> {"Dayton": 43.5, "Detroit": 47.4, "Gary": 49.0}
node 7 answer: 98453962.68 -> {"2017": "$98,453,962.68"}
node 8 answer: 100261931.64 -> {"2018": "$100,261,931.64"}
```
- Other differences also present: final question wording changed; node fields changed: answer:4, fact:8, limit:2, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-2/task_5.json`
- Reason: final answer changed
```text
final answer: San Francisco Bay -> Pacific Ocean
```
- Other differences also present: final question wording changed; node fields changed: fact:6, node_ids/count:1, subquestion:8; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-3/task_2.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 6 answer: {"UNITED STATES CAPITOL POLICE": 30, "UNITED STATES PARK POLICE": 71, "US. SECRET SERVICE... -> UNITED STATES PARK POLICE
```
- Other differences also present: node fields changed: answer:1, fact:3, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-3/task_3.json`
- Reason: 2 node/subquestion answer(s) changed
```text
node 11 answer: 4 -> 4
node 12 answer: 35503 -> 35503
```
- Other differences also present: node fields changed: answer:2, fact:3, limit:9, subquestion:12; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-6-d-3/task_5.json`
- Reason: 1 node/subquestion answer(s) changed
```text
node 8 answer: 16 -> 16
```
- Other differences also present: node fields changed: answer:1, fact:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

### `k-7-d-4/task_1.json`
- Reason: 6 node/subquestion answer(s) changed
```text
node 1 answer: {"BEXAR": 4545, "DALLAS": 5355, "EL PASO": 1261, "HARRIS": 9029, "HIDALGO": 1861, "MCLENN... -> {"Bexar": 4545, "Dallas": 5355, "Harris": 9029, "Hidalgo": 1861, "Tarrant": 4769}
node 2 answer: {"BEXAR": 3917, "DALLAS": 4540, "EL PASO": 1121, "HARRIS": 7059, "HIDALGO": 1572, "MCLENN... -> {"Bexar": 3917, "Dallas": 4540, "Harris": 7059, "Hidalgo": 1572, "Tarrant": 4450}
node 3 answer: {"BEXAR": 3236, "DALLAS": 3565, "EL PASO": 967, "HARRIS": 5210, "HIDALGO": 1147, "MCLENNA... -> {"Bexar": 3236, "Dallas": 3565, "Harris": 5210, "Hidalgo": 1147, "Tarrant": 3252}
node 4 answer: {"BEXAR": 2918, "DALLAS": 3557, "EL PASO": 834, "HARRIS": 4988, "HIDALGO": 1015, "JEFFERS... -> {"Bexar": 2918, "Dallas": 3557, "Harris": 4988, "Hidalgo": 1015, "Tarrant": 3231}
node 10 answer: 82 -> 82
node 11 answer: 898 -> 898
```
- Other differences also present: final question wording changed; node fields changed: answer:6, fact:11, limit:4, subquestion:11; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed

## Structural Only

- `k-4-d-4/task_14.json`: file exists only in tasks_mini copy; no paired answers to compare; copy question: Across years 2015-16 to 2018-19, which Texas county is consistently in the top five for total lunch serves in Seamless Summer Option program? Among those counties, identify the tw...
- `k-5-d-2/task_11.json`: file exists only in tasks_mini; no paired answers to compare; tasks_mini question: Find the New York counties (excluding NYC boroughs) satisfying both criteria: (1) average ratio of being sent back to jail between 38% and 40% in 2018-2019 in New York, and (2) av...

## Non-Substantive Under Answer Rule

- `k-1-d-1/task_1.json`: node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-1-d-1/task_2.json`: node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-1-d-1/task_3.json`: final question wording changed; node fields changed: fact:1, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
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
- `k-3-d-3/task_1.json`: final question wording changed; node fields changed: fact:3, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-3-d-3/task_2.json`: final question wording changed; node fields changed: fact:7, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
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
- `k-4-d-1/task_6.json`: final question wording changed; node fields changed: fact:4, subquestion:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-2/task_1.json`: node fields changed: fact:1, subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_10.json`: node fields changed: depends_on:6, fact:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_11.json`: final question wording changed; node fields changed: depends_on:6, fact:4, subquestion:1; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_12.json`: final question wording changed; node fields changed: fact:2, subquestion:2; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_13.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_14.json`: final question wording changed; node fields changed: fact:4, subquestion:6; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-2/task_2.json`: final question wording changed; node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_5.json`: final question wording changed; node fields changed: fact:2, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_6.json`: final question wording changed; node fields changed: fact:4, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_7.json`: node fields changed: fact:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_8.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-2/task_9.json`: node fields changed: fact:4; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-4-d-3/task_3.json`: final question wording changed; node fields changed: fact:2, subquestion:1; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-3/task_6.json`: final question wording changed; node fields changed: subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_13.json`: final question wording changed; node fields changed: subquestion:3; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_4.json`: final question wording changed; node fields changed: limit:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-4-d-4/task_9.json`: node fields changed: fact:4, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-1/task_1.json`: final question wording changed; node fields changed: fact:5, source:1, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-1/task_3.json`: node fields changed: fact:4, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-1/task_4.json`: final question wording changed; node fields changed: fact:5, subquestion:5; datasets_used changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-2/task_1.json`: final question wording changed; node fields changed: fact:3, subquestion:6; datasets_used changed; practical_motivation changed; reasoning_chain changed; reasoning_hops changed
- `k-5-d-3/task_4.json`: final question wording changed; node fields changed: fact:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-3/task_6.json`: node fields changed: fact:3, subquestion:9; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-3/task_8.json`: final question wording changed; node fields changed: fact:10, limit:3, subquestion:11; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-5-d-4/task_9.json`: final question wording changed; node fields changed: fact:4, subquestion:8; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-6-d-3/task_1.json`: node fields changed: fact:4, subquestion:10; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed
- `k-6-d-3/task_4.json`: node fields changed: fact:2, subquestion:7; datasets_used changed; reasoning_chain changed; reasoning_hops changed; verdict changed