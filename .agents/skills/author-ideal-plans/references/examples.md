# Examples

## Clean Example 1

Source style: `plans_mini/k-2-d-4/task_1.json`

```text
1. Filter NY counties with at least 65 poor bridges.
2. From those, keep counties with at least 50 fire departments.
3. From that subset, keep counties with at least 100 bank ATMs.
4. From that subset, keep counties with at least 1.0 MW operational renewable capacity.
5. Compare 2021 violent-crime counts for the remaining counties and return the county with the higher value.
```

Why it is clean:
- each step is necessary and non-repetitive
- no leaked county names
- no copied node labels
- safe as prompt scaffolding

## Clean Example 2

Source style: `plans_mini/k-3-d-4/task_6.json`

```text
1. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2020.
2. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2021.
3. Identify U.S. states with between 150 and 300 VA pension recipients in FY 2023.
4. Determine which states are in New England.
5. Find the capital of the state that remains after intersecting the qualifying sets.
6. Return the year in which that capital city was chartered.
```

Why it is clean:
- yearly steps are explicit
- intersection is described without leaking the surviving state
- no final answer is embedded
- the step wording describes each source by function, not by unnecessary dataset branding

## Style Example

Too dataset-literal:

```text
6. Using the Chicago census data, keep the schools whose community area has per capita income above $50,000.
7. On the Wrigley Field page, identify the Chicago Cubs.
8. On the Chicago Cubs page, record the year the team was founded.
```

Too generic:

```text
6. Using the community-level income data, keep the schools whose community area has per capita income above $50,000.
7. On the reference page for the stadium in that qualifying community area, identify the MLB team that plays there.
8. On the reference page for that team, record the year the team was founded.
```

Preferred rewrite:

```text
6. From those schools, keep the ones in a Chicago community area with per capita income above $50,000.
7. Identify the MLB team that plays in the stadium located in that same Chicago community area.
8. Return the year that MLB team was founded.
```

Why the preferred rewrite is better:
- it stays grounded in the actual task
- it avoids turning the plan into an index of source names
- it is more readable than generic labels like `community-level income data`

## Dirty Example 1

Current noisy pattern from `plans_mini/k-4-d-3/task_7.json`

```text
1. Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)
2. Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)
3. Among CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION, which had the highest average employee count across 2021-2023? (Filter for this node: Agency Name in {CORRECTIONS, SOCIAL SERVICES, TRANSPORTATION}; count rows by Agency Name.)
```

Why it is dirty:
- steps are exact duplicates
- years are not separated by dataset step
- braces and `node` phrasing drift toward audit-log style

Clean rewrite shape:

```text
1. For 2021 state employee pay data, count employees for CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION.
2. For 2022 state employee pay data, count employees for CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION.
3. For 2023 state employee pay data, count employees for CORRECTIONS, SOCIAL SERVICES, and TRANSPORTATION.
4. Compute the average employee count across 2021-2023 and identify the agency with the highest average.
5. Determine the headquarters city of that agency.
6. Identify who founded the historically Black university in that city.
```

## Dirty Example 3

Oversplit and sequence-aware wording:

```text
4. For one of the three counties from step 3, determine its county seat.
5. For a second county from step 3, determine its county seat.
6. For the remaining county from step 3, determine its county seat.
7. Using the university article in dataset position 6, verify it matches the university from step 5 and determine who founded it.
```

Why it is dirty:
- it leaks hidden dataset sequencing into the prompt scaffolding
- it turns one logical subtask into repetitive bookkeeping
- `verify it matches` adds audit narration instead of a clean instruction

Clean rewrite shape:

```text
4. For the counties from step 3, determine each county seat.
5. For the county seats from step 4, determine when each was incorporated and keep the earliest one.
6. Determine who founded the historically Black university identified in step 5.
```

## Dirty Example 2

Current noisy pattern from `plans_mini/k-3-d-4/task_3.json`

```text
5. In which neighborhood is <intersection of node_1, node_2, node_3, node_4: PS 009 Sarah Anderson> located?
6. What are some notable structures that is a museum in <node_5 answer: Upper West Side>?
7. Which museums are located adjacent to Central Park?
8. In what year was <intersection of node_6, node_7: American Museum of Natural History> established?
```

Why it is dirty:
- leaks discovered entity names
- uses angle-bracket placeholders
- carries forward solved intersections rather than clean scaffolding

Clean rewrite shape:

```text
5. Determine the neighborhood of the school that remains after intersecting the four yearly top-three lists.
6. Identify museums that are notable structures in that neighborhood.
7. Identify museums adjacent to Central Park.
8. Return the year in which the museum appearing in both museum lists was established.
```
