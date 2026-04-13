# Examples

## Passing Example

Original chain shape:

```text
Node 1: 2020 pension recipients ...
Node 2: 2021 pension recipients ...
Node 3: 2023 pension recipients ...
Intersection -> Vermont
Node 5: Vermont's capital -> Montpelier
Node 6: Montpelier charter year -> 1781
```

Passing cleaned plan:

```text
1. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2020.
2. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2021.
3. Identify U.S. states with between 150 and 300 VA pension recipients in FY 2023.
4. Determine which states are in New England.
5. Find the capital of the state that remains after intersecting the qualifying sets.
6. Return the year in which that capital city was chartered.
```

Why it passes:
- keeps the original narrowing path
- does not leak `Vermont`, `Montpelier`, or `1781`
- does not let the agent skip the capital lookup

## Failing Example: Intermediate Leak

```text
1. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2020.
2. Identify U.S. states with between 200 and 400 VA pension recipients in FY 2021.
3. Identify U.S. states with between 150 and 300 VA pension recipients in FY 2023.
4. Determine which states are in New England.
5. Find the capital of Vermont.
6. Return the year Montpelier was chartered.
```

Why it fails:
- leaks the intermediate surviving state
- leaks the downstream lookup target
- makes steps 1-4 partly optional because the plan already reveals the result

## Failing Example: Step Skipping

Original chain requires:
- top-20 agencies by fines for each year
- intersection of agencies
- moving-violation comparison across the surviving agencies
- lookup of the federal agency operating the winner

Bad cleaned plan:

```text
1. Identify the federal law-enforcement agency with the highest average January moving violations across 2019-2021.
2. Return the federal agency that operates it.
```

Why it fails:
- collapses multiple retrieval steps
- removes the parking-fines intersection stage
- makes the task much easier than the original reasoning chain
