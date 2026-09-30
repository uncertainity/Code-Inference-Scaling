# Stage 2: Fair data

The fair-data stage creates the matched task population used by generation and
analysis. A task is retained only when both of the following are available:

1. at least one non-empty reference solution; and
2. a corresponding complexity trace containing `AST_Length`.

This prevents model/configuration comparisons from being driven by different
task sets.

## Build

```bash
python fair_data/build.py
```

`build.py` joins normalized rows from `data_collection/normalized/` with traces
from `complexity_metrics/traces/`. It writes generation-ready records to
`data_jsonl/` and aligned metrics to `complexity_metrics/fair_traces/`.

The current fair set contains:

| Dataset | Tasks |
|---|---:|
| MBPP | 500 |
| HumanEval | 164 |
| APPS | 3,927 |
| LiveCodeBench | 400 |

`subsets/` contains compact checked-in samples for development. The full
`data_jsonl/` files are large derived artifacts and are excluded from Git.

