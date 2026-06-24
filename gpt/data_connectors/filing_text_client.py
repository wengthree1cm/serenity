from __future__ import annotations

import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from data_connectors.sec_client import SEC_USER_AGENT, fetch_company_submissions, normalize_cik


SEC_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"
DEFAULT_CACHE_DIR = Path("data_cache")


def get_latest_filings(
    ticker: str,
    cik: str,
    forms: list[str] | None = None,
    count_per_form: int = 1,
    include_recent_8k: int = 3,
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
) -> list[dict[str, Any]]:
    forms = forms or ["10-K", "10-Q"]
    submissions = fetch_company_submissions(cik, cache_dir=cache_dir)
    recent = (submissions.get("filings") or {}).get("recent") or {}
    rows = _recent_rows(recent)
    selected: list[dict[str, Any]] = []
    for form in forms:
        matching = [row for row in rows if row.get("form") == form]
        selected.extend(matching[:count_per_form])
    if include_recent_8k:
        selected.extend([row for row in rows if row.get("form") == "8-K"][:include_recent_8k])
    for row in selected:
        row["ticker"] = ticker.upper()
        row["cik"] = normalize_cik(cik)
        row["source_url"] = filing_document_url(row["cik"], row["accessionNumber"], row["primaryDocument"])
    return selected


def fetch_filing_text(
    ticker: str,
    filing: dict[str, Any],
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
) -> dict[str, Any]:
    url = filing["source_url"]
    response = requests.get(
        url,
        headers={"User-Agent": SEC_USER_AGENT, "Accept-Encoding": "gzip, deflate"},
        timeout=30,
    )
    response.raise_for_status()
    raw_text = response.text
    cache_path = _cache_filing(ticker, filing, raw_text, cache_dir)
    return {
        "filing": filing,
        "source_url": url,
        "cached_file_path": str(cache_path),
        "raw_text": raw_text,
        "plain_text": html_to_text(raw_text),
    }


def filing_document_url(cik: str, accession_number: str, primary_document: str) -> str:
    cik_int = str(int(normalize_cik(cik)))
    accession = accession_number.replace("-", "")
    return f"{SEC_ARCHIVES_BASE}/{cik_int}/{accession}/{primary_document}"


def html_to_text(raw_text: str) -> str:
    text = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", raw_text)
    text = re.sub(r"(?is)<ix:hidden.*?</ix:hidden>", " ", text)
    text = re.sub(r"(?is)<ix:header.*?</ix:header>", " ", text)
    text = re.sub(r"(?is)<xbrli:context.*?</xbrli:context>", " ", text)
    text = re.sub(r"(?is)<xbrli:unit.*?</xbrli:unit>", " ", text)
    text = re.sub(r"(?is)<link:schemaRef.*?</link:schemaRef>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def search_filing_text(
    plain_text: str,
    terms: list[str],
    context_chars: int = 450,
    max_hits_per_term: int = 4,
) -> dict[str, list[dict[str, Any]]]:
    results: dict[str, list[dict[str, Any]]] = {}
    lower_text = plain_text.lower()
    for term in terms:
        hits: list[dict[str, Any]] = []
        start = 0
        needle = term.lower()
        while len(hits) < max_hits_per_term:
            idx = lower_text.find(needle, start)
            if idx < 0:
                break
            snippet_start = max(0, idx - context_chars)
            snippet_end = min(len(plain_text), idx + len(term) + context_chars)
            snippet = plain_text[snippet_start:snippet_end].strip()
            hits.append(
                {
                    "term": term,
                    "start": idx,
                    "excerpt": _shorten_excerpt(snippet),
                }
            )
            start = idx + len(term)
        results[term] = hits
    return results


def _recent_rows(recent: dict[str, list[Any]]) -> list[dict[str, Any]]:
    keys = list(recent.keys())
    if not keys:
        return []
    row_count = len(recent.get(keys[0]) or [])
    rows: list[dict[str, Any]] = []
    for idx in range(row_count):
        rows.append({key: (recent.get(key) or [None] * row_count)[idx] for key in keys})
    return rows


def _cache_filing(
    ticker: str,
    filing: dict[str, Any],
    raw_text: str,
    cache_dir: str | Path,
) -> Path:
    folder = Path(cache_dir) / "sec_filings" / ticker.upper()
    folder.mkdir(parents=True, exist_ok=True)
    accession = filing["accessionNumber"].replace("-", "")
    document = re.sub(r"[^A-Za-z0-9_.-]+", "_", filing["primaryDocument"])
    path = folder / f"{filing['form']}_{filing['filingDate']}_{accession}_{document}"
    path.write_text(raw_text, encoding="utf-8", errors="replace")
    metadata_path = folder / f"{filing['form']}_{filing['filingDate']}_{accession}.metadata.json"
    metadata = {
        "cached_at": datetime.now(timezone.utc).isoformat(),
        "filing": filing,
        "source_url": filing.get("source_url"),
        "cached_file_path": str(path),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def _shorten_excerpt(text: str, max_words: int = 60) -> str:
    words = text.split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]) + " ..."
