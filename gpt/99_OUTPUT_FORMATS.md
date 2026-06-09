# 99 Output Formats and Shared Schemas

## Purpose

This file defines shared JSON conventions for all skills.

Every skill should output valid JSON unless it is explicitly the report writer.

## Global Metadata

Every JSON output should include:

```json
{
  "status": "completed | needs_more_data | failed",
  "theme": "",
  "generated_at": "",
  "skill_name": "",
  "warnings": []
}
```

If the system cannot complete a stage:

```json
{
  "status": "needs_more_data",
  "theme": "",
  "skill_name": "",
  "missing_data": [],
  "recommended_next_actions": [],
  "partial_output": {}
}
```

## Evidence Object

Use this object whenever citing evidence.

```json
{
  "evidence_type": "hard | soft | inference",
  "source_type": "filing | earnings_call | investor_presentation | press_release | government_data | company_website | customer_disclosure | industry_report | news | financial_data_api | other | none",
  "source_title": "",
  "source_url": "",
  "source_date": "",
  "summary": "",
  "why_it_matters": "",
  "confidence": "low | medium | high"
}
```

## Company Object

```json
{
  "ticker": "",
  "company_name": "",
  "exchange": "",
  "market_cap": "unknown",
  "enterprise_value": "unknown",
  "segment_name": "",
  "exposure_category": "pure_play | high_exposure | partial_exposure | loose_exposure | not_relevant",
  "business_relevance_score": 0
}
```

## Segment Object

```json
{
  "segment_id": "",
  "segment_name": "",
  "value_chain_position": "upstream_materials | component | equipment | software | integration | service | customer | other",
  "role_in_theme": "",
  "demand_driver": "",
  "supply_constraint": "",
  "chokepoint_score": 0
}
```

## Commercial Validation Object

```json
{
  "commercial_validation_level": 0,
  "commercial_validation_score": 0,
  "validation_stage_label": "No Evidence | Soft Evidence Only | Early Validation | Hard Evidence Emerging | Fully Repriced",
  "hard_evidence": [],
  "soft_evidence": [],
  "inferences": [],
  "missing_evidence": []
}
```

## Valuation and Crowding Object

```json
{
  "valuation_status": "undemanding | reasonable | stretched | very_stretched | unknown",
  "crowding_status": "low | medium | high | unknown",
  "repricing_status": "not_repriced | partially_repriced | mostly_repriced | unknown",
  "valuation_score": 0,
  "crowding_score": 0
}
```

## Final Ranking Object

```json
{
  "rank": 1,
  "ticker": "",
  "company_name": "",
  "final_score": 0,
  "classification": "High Priority Research | Watchlist | Wait for Pullback | Observe | Reject",
  "one_sentence_thesis": "",
  "key_evidence": [],
  "key_risks": [],
  "near_term_catalysts": [],
  "what_to_verify_next": []
}
```

## File Naming Convention

```text
outputs/01_theme_research.json
outputs/02_value_chain.json
outputs/03_chokepoint_scores.json
outputs/04_company_candidates.json
outputs/05_commercial_validation.json
outputs/06_valuation_crowding.json
outputs/07_bear_case.json
outputs/08_final_ranking.json
outputs/final_report.md
```

## Output Quality Rules

1. JSON must be parseable.
2. Do not include comments inside JSON.
3. Use `unknown` for missing data.
4. Do not hallucinate sources.
5. Do not use empty evidence to support high scores.
6. Every high-priority candidate must include both supporting evidence and bear-case risks.
7. Final outputs are research classifications, not buy/sell/hold instructions.
