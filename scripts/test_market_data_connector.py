#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data_connectors.company_profile_builder import build_company_profile


TEST_COMPANIES = {
    "RKLB": "0001819994",
    "KTOS": "0001069258",
    "RDW": "0001819810",
    "MRCY": "0001049521",
    "IRDM": "0001418819",
}


def main() -> int:
    rows: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    for ticker, cik in TEST_COMPANIES.items():
        profile = build_company_profile(ticker, cik, data_cache_dir=ROOT / "data_cache")
        profiles.append(profile)
        market_data = profile.get("market_data") or {}
        rows.append(
            {
                "ticker": ticker,
                "current_price": _value(market_data, "current_price"),
                "market_cap": _value(market_data, "market_cap"),
                "enterprise_value": _value(market_data, "enterprise_value"),
                "shares_outstanding": _value(market_data, "shares_outstanding"),
                "price_change_6m": _value(market_data, "price_change_6m"),
                "price_change_12m": _value(market_data, "price_change_12m"),
                "ev_to_sales": _value(market_data, "ev_to_sales"),
                "price_to_sales": _value(market_data, "price_to_sales"),
                "missing_fields_count": len(profile.get("missing_fields") or []),
                "missing_fields": profile.get("missing_fields") or [],
                "data_quality_warnings": profile.get("data_quality_warnings") or [],
            }
        )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tickers": list(TEST_COMPANIES.keys()),
        "rows": rows,
        "profiles": profiles,
    }

    outputs_dir = ROOT / "outputs"
    outputs_dir.mkdir(exist_ok=True)
    (outputs_dir / "market_data_connector_test.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (outputs_dir / "market_data_connector_test.md").write_text(_markdown_table(rows), encoding="utf-8")
    print(_plain_table(rows))
    return 0


def _value(market_data: dict[str, Any], field: str) -> Any:
    payload = market_data.get(field) or {}
    return payload.get("value")


def _plain_table(rows: list[dict[str, Any]]) -> str:
    columns = [
        "ticker",
        "current_price",
        "market_cap",
        "enterprise_value",
        "shares_outstanding",
        "price_change_6m",
        "price_change_12m",
        "ev_to_sales",
        "price_to_sales",
        "missing_fields_count",
    ]
    widths = {
        column: max(len(column), *(len(_fmt(row[column])) for row in rows))
        for column in columns
    }
    lines = ["  ".join(column.ljust(widths[column]) for column in columns)]
    lines.append("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        lines.append("  ".join(_fmt(row[column]).ljust(widths[column]) for column in columns))
    return "\n".join(lines)


def _markdown_table(rows: list[dict[str, Any]]) -> str:
    columns = [
        "ticker",
        "current_price",
        "market_cap",
        "enterprise_value",
        "shares_outstanding",
        "price_change_6m",
        "price_change_12m",
        "ev_to_sales",
        "price_to_sales",
        "missing_fields_count",
    ]
    lines = ["# Market Data Connector Test\n", "| " + " | ".join(columns) + " |"]
    lines.append("|" + "|".join(["---"] * len(columns)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(_fmt(row[column]) for column in columns) + " |")
    lines.append("")
    lines.append("## Missing Fields")
    for row in rows:
        missing = row.get("missing_fields") or []
        lines.append(f"- `{row['ticker']}`: {', '.join(missing) if missing else 'none'}")
    lines.append("")
    lines.append("## Warnings")
    for row in rows:
        warnings = row.get("data_quality_warnings") or []
        lines.append(f"- `{row['ticker']}`: {', '.join(warnings) if warnings else 'none'}")
    lines.append("")
    return "\n".join(lines)


def _fmt(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


if __name__ == "__main__":
    raise SystemExit(main())
