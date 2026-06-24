from __future__ import annotations

from pathlib import Path
from typing import Any

from data_connectors.market_data_client import build_market_data_profile
from data_connectors.sec_client import fetch_companyfacts, fetch_company_submissions, normalize_cik
from data_connectors.yahoo_client import extract_quote_snapshot, fetch_chart


def build_company_profile(
    ticker: str,
    cik: str | None = None,
    data_cache_dir: str | Path = "data_cache",
) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    warnings: list[str] = []
    missing_fields: list[str] = []
    source_urls = [
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
    ]

    sec_summary: dict[str, Any] = {}
    key_metrics: dict[str, Any] = {}
    sec_data: dict[str, Any] = {}
    normalized_cik: str | None = None
    company_name: str | None = None

    if cik:
        try:
            normalized_cik = normalize_cik(cik)
            facts = fetch_companyfacts(normalized_cik, cache_dir=data_cache_dir)
            source_urls.append(
                f"https://data.sec.gov/api/xbrl/companyfacts/CIK{normalized_cik}.json"
            )
            sec_summary = _summarize_companyfacts(facts)
            key_metrics = _extract_key_financial_metrics(facts)
            sec_data = {
                "companyfacts_summary": sec_summary,
                "key_financial_metrics": key_metrics,
            }
            company_name = sec_summary.get("company_name")
            try:
                submissions = fetch_company_submissions(normalized_cik, cache_dir=data_cache_dir)
                source_urls.append(
                    f"https://data.sec.gov/submissions/CIK{normalized_cik}.json"
                )
                company_name = company_name or submissions.get("name")
                sec_summary["sic"] = submissions.get("sic")
                sec_summary["sic_description"] = submissions.get("sicDescription")
                sec_summary["fiscal_year_end"] = submissions.get("fiscalYearEnd")
                sec_data["submissions_summary"] = {
                    "name": submissions.get("name"),
                    "sic": submissions.get("sic"),
                    "sic_description": submissions.get("sicDescription"),
                    "fiscal_year_end": submissions.get("fiscalYearEnd"),
                }
            except Exception as exc:
                warnings.append(f"SEC submissions unavailable for {symbol}: {exc}")
        except Exception as exc:
            warnings.append(f"SEC companyfacts unavailable for {symbol}: {exc}")
    else:
        missing_fields.append("cik")
        warnings.append(f"No CIK supplied for {symbol}; SEC data was not fetched.")

    market_data_profile: dict[str, Any] = {}
    market_data: dict[str, Any] = {}
    financial_data: dict[str, Any] = {}
    try:
        market_data_profile = build_market_data_profile(symbol, cache_dir=data_cache_dir)
        market_data = market_data_profile.get("market_data") or {}
        financial_data = market_data_profile.get("financial_data") or {}
        source_urls.extend(market_data_profile.get("source_urls") or [])
        missing_fields.extend(
            f"market_data.{field}" for field in market_data_profile.get("missing_fields", [])
        )
        warnings.extend(market_data_profile.get("data_quality_warnings", []))
        warnings.extend(market_data_profile.get("endpoint_failures", []))
    except Exception as exc:
        warnings.append(f"Market data unavailable for {symbol}: {exc}")
        missing_fields.append("market_data")

    yahoo_snapshot: dict[str, Any] = {}
    try:
        yahoo_snapshot = extract_quote_snapshot(
            fetch_chart(symbol, range="1y", interval="1d", cache_dir=data_cache_dir)
        )
    except Exception as exc:
        warnings.append(f"Yahoo chart unavailable for {symbol}: {exc}")

    if not company_name:
        missing_fields.append("company_name")

    if not key_metrics:
        missing_fields.append("key_financial_metrics")

    return {
        "ticker": symbol,
        "cik": normalized_cik or cik,
        "company_name": company_name,
        "market_data": market_data,
        "financial_data": financial_data,
        "sec_data": sec_data,
        "source_urls": _dedupe(source_urls),
        "missing_fields": _dedupe(missing_fields),
        "data_quality_warnings": _dedupe(warnings),
        # Legacy fields retained for the first connector test and older run artifacts.
        "sec_companyfacts_summary": sec_summary,
        "yahoo_quote_snapshot": yahoo_snapshot,
        "key_financial_metrics": key_metrics,
    }


def _summarize_companyfacts(facts: dict[str, Any]) -> dict[str, Any]:
    fact_namespaces = facts.get("facts") or {}
    us_gaap = fact_namespaces.get("us-gaap") or {}
    return {
        "company_name": facts.get("entityName"),
        "cik": facts.get("cik"),
        "available_namespaces": list(fact_namespaces.keys()),
        "us_gaap_fact_count": len(us_gaap),
    }


def _extract_key_financial_metrics(facts: dict[str, Any]) -> dict[str, Any]:
    us_gaap = ((facts.get("facts") or {}).get("us-gaap") or {})
    concepts = {
        "revenue": [
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "Revenues",
            "SalesRevenueNet",
        ],
        "net_income_loss": ["NetIncomeLoss"],
        "operating_income_loss": ["OperatingIncomeLoss"],
        "assets": ["Assets"],
        "liabilities": ["Liabilities"],
        "stockholders_equity": ["StockholdersEquity"],
        "cash_and_equivalents": ["CashAndCashEquivalentsAtCarryingValue"],
        "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    }
    metrics: dict[str, Any] = {}
    for metric_name, candidate_tags in concepts.items():
        value = _latest_fact_value(us_gaap, candidate_tags)
        if value is not None:
            metrics[metric_name] = value
    return metrics


def _latest_fact_value(us_gaap: dict[str, Any], candidate_tags: list[str]) -> dict[str, Any] | None:
    for tag in candidate_tags:
        units = (us_gaap.get(tag) or {}).get("units") or {}
        for unit in ["USD", "shares", "USD/shares", "pure"]:
            values = [
                item
                for item in units.get(unit, [])
                if item.get("val") is not None and item.get("end")
            ]
            if not values:
                continue
            values.sort(key=lambda item: (item.get("end") or "", item.get("filed") or ""), reverse=True)
            latest = values[0]
            return {
                "concept": tag,
                "unit": unit,
                "value": latest.get("val"),
                "end": latest.get("end"),
                "filed": latest.get("filed"),
                "form": latest.get("form"),
                "fy": latest.get("fy"),
                "fp": latest.get("fp"),
            }
    return None


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result
