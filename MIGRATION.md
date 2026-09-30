# Repository layout migration

No experiment data was deleted during the reorganization. Active components
were moved into one of the six pipeline stages, while superseded material was
moved under `legacy/`.

| Previous path | Current path |
|---|---|
| `data/` | `data_collection/raw/` |
| `data_json/` | `data_collection/normalized/` |
| `codex_solutions/` | `data_collection/reference_solutions/codex/` |
| `missing_solutions/` | `data_collection/reference_solutions/missing/` |
| `scraped_solutions/` | `data_collection/reference_solutions/scraped/` |
| `LCB_HF/` and `LeetCode-Solutions/` | `data_collection/reference_solutions/vendor/` |
| `traces/` | `complexity_metrics/traces/` |
| `fair_data/traces/` | `complexity_metrics/fair_traces/` |
| `fair_data/trace_metric_plots/` | `complexity_metrics/outputs/` |
| `configs/` | `generation/configs/` |
| `params_models/` | `generation/models/` |
| `inference/vllm/` | `generation/vllm/` |
| `runs/vllm/scaling_law_001/` | `generation/runs/vllm/scaling_law_001/` |
| exploratory/obsolete root scripts | `legacy/prototypes/` or `legacy/judges/` |
| superseded run directories | `legacy/runs/vllm/` |

All active Python, YAML, shell, harness, and analysis references were updated
to the current paths. External notebooks or commands using the previous paths
must be adjusted according to this table.

