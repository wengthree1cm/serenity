# Run Company Deep Dive

Use this prompt to run a single-company Serenity deep dive in Codex-agent mode.

## Parameters

Fill in or infer from the user request:

```json
{
  "ticker": "",
  "company_name": "",
  "sector_output_folder": "",
  "theme": "",
  "use_cached_sources": true,
  "use_live_connectors_if_needed": true
}
```

## Execution Mode

Use Codex-agent reasoning and local connector outputs.

Do not:

- Rerun the full sector workflow.
- Call the OpenAI API runner.
- Ask for `OPENAI_API_KEY`.
- Modify the `gpt/` markdown investment logic.
- Build the web app.
- Add trading, brokerage, portfolio, auto-buy, or order execution features.
- Output `Buy`, `Sell`, or `Hold`.
- Invent missing contract, backlog, revenue, valuation, or market data.

## Required Inputs

Use the existing sector output folder and local cached evidence.

Prioritize these files when available:

```text
[sector_output_folder]/data/company_profiles.json
[sector_output_folder]/data/company_profiles_v2.json
[sector_output_folder]/data/data_quality_report.json
[sector_output_folder]/data/data_quality_report_v2.json
[sector_output_folder]/data/commercial_validation_*.json
[sector_output_folder]/05_commercial_validation*.json
[sector_output_folder]/06_valuation_crowding*.json
[sector_output_folder]/07_bear_case*.json
[sector_output_folder]/08_final_ranking*.json
[sector_output_folder]/quality_gate_audit*.json
data_cache/
```

Read relevant local skill files:

1. `gpt/00_SYSTEM_PRINCIPLES.md`
2. `gpt/06_COMMERCIAL_VALIDATION.md`
3. `gpt/07_FINANCIAL_VALUATION_CROWDING.md`
4. `gpt/08_BEAR_CASE.md`
5. `gpt/09_FINAL_RANKING.md`
6. `gpt/99_OUTPUT_FORMATS.md`

Use local connectors only when needed to refresh missing data:

- `data_connectors/company_profile_builder.py`
- `data_connectors/market_data_client.py`
- `data_connectors/filing_text_client.py`
- `data_connectors/commercial_validation_client.py`

## Required Analysis

Evaluate:

1. Business description
2. Role in the sector value chain
3. Chokepoint role
4. What is proven vs inferred
5. Commercial validation
6. Market data and valuation
7. Cash flow, debt, dilution, and balance sheet quality
8. Customer, backlog, contract, and segment revenue evidence
9. Management commentary and program-level evidence
10. Future optionality, clearly separated from current validation
11. Bear case
12. Upgrade triggers
13. Downgrade triggers
14. Final rating

## Evidence Rules

Classify evidence as:

- `hard_evidence`
- `soft_evidence`
- `inference`
- `missing_evidence`

Any claim about price, market cap, enterprise value, revenue, cash, debt, free cash flow, valuation, backlog, contracts, segment revenue, customer concentration, ownership, short interest, or price performance must be grounded in local company profiles, connector outputs, cached filings, or cited source evidence.

If data is unavailable, mark it missing.

Do not infer:

- market data
- contract values
- backlog
- segment revenue
- customer concentration
- ownership
- short interest
- valuation multiples
- cash
- debt
- free cash flow

## Allowed Final Categories

Use only:

- `High Priority Research`
- `Watchlist`
- `Wait for Pullback`
- `Observe`
- `Reject`

Do not output `Buy`, `Sell`, or `Hold`.

## Output Files

Save outputs in the sector output folder:

```text
[sector_output_folder]/[TICKER]_deep_dive.md
[sector_output_folder]/[TICKER]_deep_dive.json
```

If versioning is needed because files already exist, append a version suffix:

```text
[sector_output_folder]/[TICKER]_deep_dive_v2.md
[sector_output_folder]/[TICKER]_deep_dive_v2.json
```

## Required JSON Sections

The JSON should include:

```json
{
  "ticker": "",
  "company_name": "",
  "theme": "",
  "final_classification": "",
  "business_description": {},
  "chokepoint_thesis": {},
  "commercial_validation": {
    "hard_evidence": [],
    "soft_evidence": [],
    "inference": [],
    "missing_evidence": []
  },
  "valuation_and_crowding": {},
  "future_optionality": {},
  "bear_case": {},
  "investment_grade_gate": {
    "trend_fit_score": 0,
    "chokepoint_score": 0,
    "commercial_validation_score": 0,
    "valuation_attractiveness_score": 0,
    "crowding_risk_score": 0,
    "evidence_quality_score": 0,
    "downside_risk_score": 0,
    "final_research_score": 0
  },
  "upgrade_triggers": [],
  "downgrade_triggers": [],
  "source_files": []
}
```

## Final Response

After completion, summarize:

- output files created
- final rating
- whether the company is close to `High Priority Research`
- top evidence points
- top missing evidence items
- top risks
- exact evidence needed to upgrade
- exact evidence that would cause downgrade
