#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data_connectors.company_profile_builder import build_company_profile
from data_connectors.sec_client import fetch_companyfacts
from data_connectors.yahoo_client import extract_quote_snapshot, fetch_chart


def main() -> int:
    cache_dir = Path("data_cache")
    results: dict[str, object] = {}

    sec_json = fetch_companyfacts("0001819994", cache_dir=cache_dir)
    results["sec_test_passed"] = sec_json.get("entityName") == "Rocket Lab Corp"

    chart_json = fetch_chart("RKLB", cache_dir=cache_dir)
    snapshot = extract_quote_snapshot(chart_json)
    results["yahoo_test_passed"] = snapshot.get("ticker") == "RKLB" and snapshot.get("current_price") is not None

    profile = build_company_profile("RKLB", "0001819994", data_cache_dir=cache_dir)
    results["profile_test_passed"] = profile.get("ticker") == "RKLB" and bool(profile.get("yahoo_quote_snapshot"))
    results["sample_profile_fields"] = {
        "ticker": profile.get("ticker"),
        "cik": profile.get("cik"),
        "company_name": profile.get("company_name"),
        "current_price": (profile.get("yahoo_quote_snapshot") or {}).get("current_price"),
        "market_cap": (profile.get("yahoo_quote_snapshot") or {}).get("market_cap"),
        "key_financial_metric_names": list((profile.get("key_financial_metrics") or {}).keys()),
    }
    results["data_quality_warnings"] = profile.get("data_quality_warnings")
    results["missing_fields"] = profile.get("missing_fields")

    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0 if all(results[key] for key in ["sec_test_passed", "yahoo_test_passed", "profile_test_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
