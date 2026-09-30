import argparse
import json
from pathlib import Path
from pprint import pformat

import numpy as np
from datasets import DatasetDict, load_from_disk


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data_collection" / "raw"


def shorten(value, max_chars=800):
    if value is None:
        return "None"

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            value = parsed
        except json.JSONDecodeError:
            pass

    text = pformat(value, width=100, sort_dicts=False) if not isinstance(value, str) else value
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text


def inspect_data(
    dataset_folder,
    split_type=None,
    num_examples=5,
    seed=0,
    data_dir=DEFAULT_DATA_DIR,
):
    data_base = load_from_disk(Path(data_dir) / dataset_folder)

    if isinstance(data_base, DatasetDict):
        print(data_base)
        split_type = split_type or next(iter(data_base.keys()))
        dataset = data_base[split_type]
        print(f"\nDataset: {dataset_folder} split={split_type}")
    else:
        dataset = data_base
        print(f"\nDataset: {dataset_folder}")

    print(f"Total length: {len(dataset)}")
    print(f"Columns: {dataset.column_names}")

    rng = np.random.default_rng(seed)
    selected_idx = rng.choice(len(dataset), size=min(num_examples, len(dataset)), replace=False)

    for idx in selected_idx:
        print(f"\n========== row {idx} ==========")
        row = dataset[int(idx)]
        for key, value in row.items():
            print(f"\n[{key}]")
            print(shorten(value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["mbpp", "humaneval", "apps", "lcb"])
    parser.add_argument("--split", default=None)
    parser.add_argument("-n", "--num-examples", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args()

    inspect_data(
        args.dataset,
        args.split,
        args.num_examples,
        args.seed,
        args.data_dir,
    )


