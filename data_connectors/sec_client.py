from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


SEC_USER_AGENT = "RichardFuSerenityResearch/0.1 contact: a2843668904@gmail.com"
SEC_BASE_URL = "https://data.sec.gov"
DEFAULT_CACHE_DIR = Path("data_cache")


def normalize_cik(cik: str) -> str:
    digits = "".join(ch for ch in str(cik) if ch.isdigit())
    if not digits:
        raise ValueError("CIK must contain at least one digit.")
    if len(digits) > 10:
        raise ValueError("CIK must not exceed 10 digits.")
    return digits.zfill(10)


def fetch_companyfacts(cik: str, cache_dir: str | Path = DEFAULT_CACHE_DIR) -> dict[str, Any]:
    normalized = normalize_cik(cik)
    url = f"{SEC_BASE_URL}/api/xbrl/companyfacts/CIK{normalized}.json"
    return _fetch_sec_json(url, cache_dir, normalized, "companyfacts")


def fetch_company_submissions(cik: str, cache_dir: str | Path = DEFAULT_CACHE_DIR) -> dict[str, Any]:
    normalized = normalize_cik(cik)
    url = f"{SEC_BASE_URL}/submissions/CIK{normalized}.json"
    return _fetch_sec_json(url, cache_dir, normalized, "submissions")


def _fetch_sec_json(
    url: str,
    cache_dir: str | Path,
    ticker_or_cik: str,
    stem: str,
    timeout: int = 20,
    max_retries: int = 2,
) -> dict[str, Any]:
    headers = {
        "User-Agent": SEC_USER_AGENT,
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code in {429, 500, 502, 503, 504} and attempt < max_retries:
                time.sleep(1.0 + attempt)
                continue
            response.raise_for_status()
            data = response.json()
            _save_raw_response(cache_dir, "sec", ticker_or_cik, stem, url, data)
            time.sleep(0.2)
            return data
        except requests.RequestException as exc:
            last_error = exc
            if attempt < max_retries:
                time.sleep(1.0 + attempt)
                continue
            raise
    if last_error:
        raise last_error
    raise RuntimeError(f"SEC request failed for {url}")


def _save_raw_response(
    cache_dir: str | Path,
    source: str,
    key: str,
    stem: str,
    url: str,
    data: dict[str, Any],
) -> None:
    folder = Path(cache_dir) / source / key.upper()
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = folder / f"{timestamp}_{stem}.json"
    payload = {
        "source_url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
