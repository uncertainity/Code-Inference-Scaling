import html
import json
import os
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "https://atcoder.jp"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_COLLECTION_DIR = PROJECT_ROOT / "data_collection"
CSV_PATH = DATA_COLLECTION_DIR / "metadata" / "platform_info.csv"

OUT_DIR = DATA_COLLECTION_DIR / "reference_solutions" / "scraped" / "atcoder"
META_PATH = (
    DATA_COLLECTION_DIR
    / "reference_solutions"
    / "scraped"
    / "atcoder_metadata.jsonl"
)

REQUEST_DELAY_SECONDS = 1.0
MAX_RETRIES = 3
FALLBACK_PAGES = 5
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}
PYTHON_LANGUAGE_KEYWORDS = ("Python", "PyPy")

OUT_DIR.mkdir(parents=True, exist_ok=True)
META_PATH.parent.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; atcode_solutions.py)",
})

atcoder_cookie = os.environ.get("ATCODER_COOKIE")
revel_session = os.environ.get("ATCODER_REVEL_SESSION")
if atcoder_cookie:
    SESSION.headers["Cookie"] = atcoder_cookie
elif revel_session:
    SESSION.headers["Cookie"] = f"REVEL_SESSION={revel_session}"


def get_soup(url, **kwargs):
    response = None
    for attempt in range(MAX_RETRIES):
        response = SESSION.get(url, timeout=20, **kwargs)

        if response.status_code in TRANSIENT_STATUS_CODES and attempt + 1 < MAX_RETRIES:
            time.sleep(2 ** attempt)
            continue

        break

    if "/login" in response.url:
        if atcoder_cookie:
            cookie_status = "ATCODER_COOKIE is set, but AtCoder rejected it"
        elif revel_session:
            cookie_status = "ATCODER_REVEL_SESSION is set, but AtCoder rejected it"
        else:
            cookie_status = "neither ATCODER_COOKIE nor ATCODER_REVEL_SESSION is set in this process"
        raise RuntimeError(
            "AtCoder redirected this request to the login page. "
            f"{cookie_status}. "
            f"Requested URL: {response.request.url}"
        )

    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def find_python_detail_url(soup, require_ac):
    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")
        if len(cells) < 7:
            continue

        status = cells[6].get_text(" ", strip=True)
        if require_ac and status != "AC":
            continue

        language = cells[3].get_text(" ", strip=True)
        if not any(keyword in language for keyword in PYTHON_LANGUAGE_KEYWORDS):
            continue

        detail_link = row.find("a", string="Detail")
        if detail_link is not None:
            return urljoin(BASE, detail_link["href"])

    return None


def find_python_ac_submission(contest_id, task_id):
    url = f"{BASE}/contests/{contest_id}/submissions"

    try:
        soup = get_soup(url, params={"f.Task": task_id, "f.Status": "AC"})
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code not in TRANSIENT_STATUS_CODES:
            raise
    else:
        detail_url = find_python_detail_url(soup, require_ac=False)
        if detail_url is not None:
            return detail_url

    for page in range(1, FALLBACK_PAGES + 1):
        soup = get_soup(url, params={"f.Task": task_id, "page": page})
        detail_url = find_python_detail_url(soup, require_ac=True)
        if detail_url is not None:
            return detail_url
        time.sleep(REQUEST_DELAY_SECONDS)

    return None


def fetch_submission_code(detail_url):
    soup = get_soup(detail_url)
    code_block = soup.select_one("pre#submission-code")
    if code_block is None:
        return None
    return html.unescape(code_block.get_text())


def main():
    df = pd.read_csv(CSV_PATH)
    atcoder_df = df[df["platform"] == "atcoder"].copy()

    missing = []
    copied = 0

    with META_PATH.open("w", encoding="utf-8") as meta_f:
        for _, row in atcoder_df.iterrows():
            question_id = str(row["question_id"])
            contest_id = str(row["contest_id"])

            try:
                detail_url = find_python_ac_submission(contest_id, question_id)
            except requests.HTTPError as exc:
                missing.append(question_id)
                print(f"HTTP error for {question_id}: {exc}")
                continue

            if detail_url is None:
                missing.append(question_id)
                continue

            try:
                code = fetch_submission_code(detail_url)
            except requests.HTTPError as exc:
                missing.append(question_id)
                print(f"HTTP error for {question_id} detail page: {exc}")
                continue

            if code is None:
                missing.append(question_id)
                continue

            dst = OUT_DIR / f"{question_id}.py"
            dst.write_text(code, encoding="utf-8")

            meta = {
                "platform": "atcoder",
                "question_id": question_id,
                "contest_id": contest_id,
                "source_site": "atcoder",
                "source_url": detail_url,
                "local_path": str(dst),
            }
            meta_f.write(json.dumps(meta) + "\n")
            copied += 1

            time.sleep(REQUEST_DELAY_SECONDS)

    print(f"Copied: {copied}")
    print(f"Missing: {len(missing)}")
    print("Missing IDs:", missing[:50])


if __name__ == "__main__":
    main()
