"""Download the four source datasets into ``data_collection/raw``."""

from __future__ import annotations

import argparse
from pathlib import Path

from datasets import load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data_collection" / "raw"
DATASETS = {
    "mbpp": ("google-research-datasets/mbpp", None),
    "humaneval": ("openai/openai_humaneval", None),
    "apps": ("codeparrot/apps", "test"),
    "lcb": ("livecodebench/code_generation", "test"),
}


def download(name: str, output_dir: Path) -> Path:
    repository, split = DATASETS[name]
    destination = output_dir / name
    if destination.exists():
        raise FileExistsError(
            f"Refusing to overwrite {destination}; move it aside before downloading"
        )
    dataset = load_dataset(repository, split=split) if split else load_dataset(repository)
    dataset.save_to_disk(destination)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "datasets",
        nargs="*",
        choices=sorted(DATASETS),
        default=list(DATASETS),
        help="Datasets to download; defaults to all four.",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name in args.datasets:
        print(f"Downloaded {name} to {download(name, args.output_dir)}")


if __name__ == "__main__":
    main()
