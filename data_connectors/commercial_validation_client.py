from __future__ import annotations

from pathlib import Path
from typing import Any

from data_connectors.filing_text_client import fetch_filing_text, get_latest_filings, search_filing_text


SEARCH_TERMS = [
    "backlog",
    "contract",
    "award",
    "customer",
    "concentration",
    "revenue by segment",
    "segment revenue",
    "government",
    "defense",
    "satellite",
    "space",
    "communications",
    "ground system",
    "mission",
    "guidance",
    "liquidity",
    "debt",
    "cash flow",
    "risk factors",
]


def build_commercial_validation_evidence(
    ticker: str,
    cik: str,
    cache_dir: str | Path = "data_cache",
) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    warnings: list[str] = []
    filings_checked: list[dict[str, Any]] = []
    evidence_by_category = {
        "backlog_evidence": [],
        "contract_award_evidence": [],
        "segment_revenue_evidence": [],
        "customer_concentration_evidence": [],
        "management_commentary_evidence": [],
        "risk_evidence": [],
    }
    all_hard: list[dict[str, Any]] = []
    all_soft: list[dict[str, Any]] = []

    filings = get_latest_filings(symbol, cik, cache_dir=cache_dir)
    for filing in filings:
        try:
            fetched = fetch_filing_text(symbol, filing, cache_dir=cache_dir)
        except Exception as exc:
            warnings.append(f"Could not fetch {filing.get('form')} {filing.get('filingDate')}: {exc}")
            continue
        filing_meta = {
            "form": filing.get("form"),
            "filing_date": filing.get("filingDate"),
            "report_date": filing.get("reportDate"),
            "accession_number": filing.get("accessionNumber"),
            "source_url": filing.get("source_url"),
            "cached_file_path": fetched.get("cached_file_path"),
        }
        filings_checked.append(filing_meta)
        hits = search_filing_text(fetched["plain_text"], SEARCH_TERMS)
        _collect_evidence(symbol, filing_meta, hits, evidence_by_category, all_hard, all_soft)

    missing_evidence = []
    for category, label in [
        ("backlog_evidence", "backlog"),
        ("contract_award_evidence", "contracts or awards"),
        ("segment_revenue_evidence", "segment revenue"),
        ("customer_concentration_evidence", "customer concentration"),
        ("management_commentary_evidence", "management commentary or guidance"),
        ("risk_evidence", "risk factors"),
    ]:
        if not evidence_by_category[category]:
            missing_evidence.append(f"No {label} evidence found in retrieved filings.")

    inferences = [
        {
            "source_type": "other",
            "source_date": None,
            "source_url": None,
            "cached_file_path": None,
            "exact_excerpt": None,
            "concise_paraphrase": "Commercial validation should remain provisional until extracted filing evidence is tied to the specific space/defense satellite thesis.",
            "evidence_strength": "medium",
            "relevance_to_space_theme": "medium",
        }
    ]

    return {
        "ticker": symbol,
        "filings_checked": filings_checked,
        "hard_evidence": all_hard,
        "soft_evidence": all_soft,
        "inferences": inferences,
        "missing_evidence": missing_evidence,
        "backlog_evidence": evidence_by_category["backlog_evidence"],
        "contract_award_evidence": evidence_by_category["contract_award_evidence"],
        "segment_revenue_evidence": evidence_by_category["segment_revenue_evidence"],
        "customer_concentration_evidence": evidence_by_category["customer_concentration_evidence"],
        "management_commentary_evidence": evidence_by_category["management_commentary_evidence"],
        "risk_evidence": evidence_by_category["risk_evidence"],
        "data_quality_warnings": warnings,
    }


def _collect_evidence(
    ticker: str,
    filing_meta: dict[str, Any],
    hits: dict[str, list[dict[str, Any]]],
    evidence_by_category: dict[str, list[dict[str, Any]]],
    all_hard: list[dict[str, Any]],
    all_soft: list[dict[str, Any]],
) -> None:
    term_categories = {
        "backlog": ["backlog_evidence"],
        "contract": ["contract_award_evidence"],
        "award": ["contract_award_evidence"],
        "customer": ["customer_concentration_evidence", "management_commentary_evidence"],
        "concentration": ["customer_concentration_evidence"],
        "revenue by segment": ["segment_revenue_evidence"],
        "segment revenue": ["segment_revenue_evidence"],
        "government": ["management_commentary_evidence"],
        "defense": ["management_commentary_evidence"],
        "satellite": ["management_commentary_evidence"],
        "space": ["management_commentary_evidence"],
        "communications": ["management_commentary_evidence"],
        "ground system": ["management_commentary_evidence"],
        "mission": ["management_commentary_evidence"],
        "guidance": ["management_commentary_evidence"],
        "liquidity": ["risk_evidence"],
        "debt": ["risk_evidence"],
        "cash flow": ["risk_evidence"],
        "risk factors": ["risk_evidence"],
    }
    for term, term_hits in hits.items():
        for hit in term_hits[:3]:
            item = _evidence_item(term, hit["excerpt"], filing_meta)
            for category in term_categories.get(term, []):
                if not _has_similar_excerpt(evidence_by_category[category], item["exact_excerpt"]):
                    evidence_by_category[category].append(item)
            target = all_hard if item["evidence_strength"] in {"high", "medium"} else all_soft
            if not _has_similar_excerpt(target, item["exact_excerpt"]):
                target.append(item)


def _evidence_item(term: str, excerpt: str, filing_meta: dict[str, Any]) -> dict[str, Any]:
    relevance = "high" if term in {"backlog", "contract", "award", "defense", "satellite", "space", "ground system"} else "medium"
    strength = "high" if term in {"backlog", "contract", "award", "customer", "concentration"} else "medium"
    if filing_meta.get("form") == "8-K":
        strength = "medium"
    return {
        "source_type": filing_meta.get("form") or "other",
        "source_date": filing_meta.get("filing_date"),
        "source_url": filing_meta.get("source_url"),
        "cached_file_path": filing_meta.get("cached_file_path"),
        "exact_excerpt": excerpt,
        "concise_paraphrase": f"Retrieved filing text contains the term '{term}' in a potentially relevant passage.",
        "evidence_strength": strength,
        "relevance_to_space_theme": relevance,
    }


def _has_similar_excerpt(items: list[dict[str, Any]], excerpt: str) -> bool:
    excerpt_prefix = excerpt[:80]
    return any((item.get("exact_excerpt") or "")[:80] == excerpt_prefix for item in items)
