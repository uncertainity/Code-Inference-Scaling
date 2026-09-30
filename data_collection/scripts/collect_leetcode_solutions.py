import re
import json
import shutil
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_COLLECTION_DIR = PROJECT_ROOT / "data_collection"
KAMYU_ROOT = (
    DATA_COLLECTION_DIR / "reference_solutions" / "vendor" / "leetcode_solutions"
)
CSV_PATH = DATA_COLLECTION_DIR / "metadata" / "platform_info.csv"

OUT_DIR = DATA_COLLECTION_DIR / "reference_solutions" / "scraped" / "leetcode"
META_PATH = (
    DATA_COLLECTION_DIR
    / "reference_solutions"
    / "scraped"
    / "leetcode_metadata.jsonl"
)

OUT_DIR.mkdir(parents=True, exist_ok=True)
META_PATH.parent.mkdir(parents=True, exist_ok=True)

def build_kamyu_index(kamyu_root: Path):
    index = {}
    md_files = sorted(kamyu_root.glob("*.md"))
    count = 0
    for md_path in md_files:
        text = md_path.read_text(encoding = "utf-8", errors = "ignore")
        for line in text.splitlines():
            m_id = re.search(r"^\s*\|?\s*(\d+)\s*\|", line)
            if not m_id:
                continue

            qid_text = m_id.group(1).strip()
            if not qid_text:
                continue
            qid = int(qid_text)

            py_links = re.findall(r"\[Python(?:3)?\]\(([^)]+\.py)\)", line)
            if not py_links:
                continue

            rel_path = py_links[0].replace("%20", " ")
            rel_path = rel_path.split("#")[0]
            rel_path = rel_path.strip()
            if not rel_path:
                continue

            index[qid] = {
                "leetcode_id": qid,
                "md_file": str(md_path),
                "rel_path": rel_path,
                "abs_path": str(kamyu_root / rel_path),
            }

        #     print("inside the second loop")
        #     print("Line:",line)
        #     print(f"qid:{qid}") 
        #     print(f"relative path:{rel_path}")
        #     print(f"py links:{py_links}")
        #     print("--" * 10)
        #     count += 1
        #     if count == 10:
        #         break
        # if count == 10:
        #     break

    return index
              
          
        

def main():
    df = pd.read_csv(CSV_PATH)
    leetcode_df = df[df["platform"] == "leetcode"].copy()
    leetcode_df["question_id"] = leetcode_df["question_id"].astype(int)

    kamyu_index = build_kamyu_index(KAMYU_ROOT)

    missing = []
    copied = 0

    with META_PATH.open("w", encoding="utf-8") as meta_f:
        for _, row in leetcode_df.iterrows():
            qid = int(row["question_id"])

            item = kamyu_index.get(qid)
            if item is None:
                missing.append(qid)
                continue

            src = Path(item["abs_path"])
            if not src.exists():
                missing.append(qid)
                continue

            dst = OUT_DIR / f"{qid}.py"
            shutil.copyfile(src, dst)

            meta = {
                "platform": "leetcode",
                "question_id": qid,
                "contest_id": row.get("contest_id", None),
                "source_repo": "kamyu104/LeetCode-Solutions",
                "source_path": item["rel_path"],
                "local_path": str(dst),
            }
            meta_f.write(json.dumps(meta) + "\n")
            copied += 1

    print(f"Copied: {copied}")
    print(f"Missing: {len(missing)}")
    print("Missing IDs:", missing[:50])


if __name__ == "__main__":
    main()
