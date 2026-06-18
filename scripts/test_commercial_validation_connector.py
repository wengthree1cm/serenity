#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data_connectors.commercial_validation_client import build_commercial_validation_evidence


TARGETS = {
    "KTOS": "0001069258",
    "IRDM": "0001418819",
}
RUN_DIR = ROOT / "outputs" / "codex_agent_space_20260612_1523"


def main() -> int:
    results = []
    for ticker, cik in TARGETS.items():
        results.append(build_commercial_validation_evidence(ticker, cik, cache_dir=ROOT / "data_cache"))

    data_dir = RUN_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    json_path = data_dir / "commercial_validation_KTOS_IRDM.json"
    md_path = data_dir / "commercial_validation_KTOS_IRDM.md"
    payload = {"targets": list(TARGETS), "results": results}
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(_render_markdown(results), encoding="utf-8")

    print(_compact_summary(results))
    return 0


def _compact_summary(results: list[dict]) -> str:
    lines = ["ticker  filings  hard  backlog  contract_award  segment_revenue  customer_concentration  warnings"]
    lines.append("------  -------  ----  -------  --------------  ---------------  ----------------------  --------")
    for item in results:
        lines.append(
            f"{item['ticker']}  {len(item['filings_checked'])}  {len(item['hard_evidence'])}  "
            f"{len(item['backlog_evidence'])}  {len(item['contract_award_evidence'])}  "
            f"{len(item['segment_revenue_evidence'])}  {len(item['customer_concentration_evidence'])}  "
            f"{len(item['data_quality_warnings'])}"
        )
    return "\n".join(lines)


def _render_markdown(results: list[dict]) -> str:
    lines = ["# Commercial Validation Evidence: KTOS and IRDM", ""]
    for item in results:
        lines.append(f"## {item['ticker']}")
        lines.append("")
        lines.append("### Filings Checked")
        for filing in item["filings_checked"]:
            lines.append(
                f"- {filing['form']} filed {filing['filing_date']} "
                f"({filing['accession_number']})"
            )
        lines.append("")
        for label, key in [
            ("Backlog Evidence", "backlog_evidence"),
            ("Contract / Award Evidence", "contract_award_evidence"),
            ("Segment Revenue Evidence", "segment_revenue_evidence"),
            ("Customer Concentration Evidence", "customer_concentration_evidence"),
            ("Management Commentary Evidence", "management_commentary_evidence"),
            ("Risk Evidence", "risk_evidence"),
        ]:
            lines.append(f"### {label}")
            evidence = item.get(key) or []
            if not evidence:
                lines.append("- Missing in retrieved filings.")
            for ev in evidence[:6]:
                excerpt = ev.get("exact_excerpt") or ev.get("concise_paraphrase") or ""
                lines.append(
                    f"- **{ev.get('source_type')} {ev.get('source_date')}** "
                    f"[{ev.get('evidence_strength')}, relevance {ev.get('relevance_to_space_theme')}]: "
                    f"{excerpt}"
                )
            lines.append("")
        lines.append("### Missing Evidence")
        for missing in item.get("missing_evidence") or []:
            lines.append(f"- {missing}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
