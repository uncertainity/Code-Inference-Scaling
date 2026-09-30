# Task: Generate the missing reference solutions

## Input
`data_collection/reference_solutions/missing/`

## Description 
The missing-solutions directory contains two JSONL files:

- `data_collection/reference_solutions/missing/missing_apps.jsonl`
- `data_collection/reference_solutions/missing/missing_lcb.jsonl`

Each row/line corresponds to a coding question from LCB or APPS whose reference solution was unparsable or not found.

## Output
- `data_collection/reference_solutions/codex/apps_test/`
- `data_collection/reference_solutions/codex/lcb_test/`


## Description

For every JSONL row, generate one `.py` file named with the numeric part of
its `task_id`. For example:

- `apps/4532` -> `data_collection/reference_solutions/codex/apps_test/4532.py`
- `lcb/4532` -> `data_collection/reference_solutions/codex/lcb_test/4532.py`

Each file must contain a general solution that satisfies the test cases in the
corresponding JSON row.

## Additional Information

Keep the code concise and valid for the AST and Radon metrics implemented in
`complexity_metrics/ast_metrics.py`. Existing solutions and traces can be used
as format references.

## Helper Files

- `data_collection/normalized/`: normalized APPS and LCB records.
- `complexity_metrics/traces/`: existing complexity traces.
- `complexity_metrics/ast_metrics.py`: complexity-metric implementation.

## IMPORTANT

Do not write lookup tables containing test cases. Implement the general
algorithm.
