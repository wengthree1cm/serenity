# Run Sector Analysis

Use this prompt to run a full Serenity sector analysis in Codex-agent mode.

## Parameters

Fill in or infer from the user request:

```json
{
  "theme": "",
  "market": "US stocks",
  "market_cap_min": null,
  "market_cap_max": null,
  "max_companies": 10,
  "seed_universe": null,
  "use_live_data": true
}
```

## Execution Mode

Use Codex-agent reasoning, not the OpenAI API runner.

Do not:

- Call `scripts/run_serenity_workflow.py` if it requires `OPENAI_API_KEY`.
- Use the OpenAI API runner.
- Ask for `OPENAI_API_KEY`.
- Modify the `gpt/` markdown investment logic.
- Build the web app.
- Add trading, brokerage, portfolio, auto-buy, or order execution features.
- Output `Buy`, `Sell`, or `Hold`.
- Invent missing data.

## Required Local Inputs

Read the local skill files in this order when present:

1. `gpt/00_SYSTEM_PRINCIPLES.md`
2. `gpt/02_THEME_RESEARCH.md`
3. `gpt/03_VALUE_CHAIN_DECOMPOSITION.md`
4. `gpt/03A_LEADER_BUSINESS_ANATOMY.md`
5. `gpt/03B_LEADER_FUTURE_OPTIONALITY.md`
6. `gpt/04_CHOKEPOINT_SCORING.md`
7. `gpt/05_COMPANY_DISCOVERY.md`
8. `gpt/06_COMMERCIAL_VALIDATION.md`
9. `gpt/07_FINANCIAL_VALUATION_CROWDING.md`
10. `gpt/08_BEAR_CASE.md`
11. `gpt/09_FINAL_RANKING.md`
12. `gpt/10_REPORT_WRITER.md`
13. `gpt/99_OUTPUT_FORMATS.md`

Use local connectors where available:

- `data_connectors/company_profile_builder.py`
- `data_connectors/market_data_client.py`
- `data_connectors/sec_client.py`
- `data_connectors/yahoo_client.py`
- `data_connectors/filing_text_client.py`
- `data_connectors/commercial_validation_client.py`

Use cached source documents where available under `data_cache/`.

## Output Folder

Create a timestamped output folder:

```text
outputs/codex_agent_[short_theme_slug]_YYYYMMDD_HHMM/
```

Inside it, create:

```text
data/
```

Save live and enriched data:

```text
data/company_profiles.json
data/data_quality_report.json
```

If commercial validation connector outputs are produced, save them under:

```text
data/commercial_validation_[scope].json
data/commercial_validation_[scope].md
```

## Workflow Outputs

Write both raw markdown and JSON outputs when applicable:

```text
01_theme_research.raw.md
01_theme_research.json
02_value_chain.raw.md
02_value_chain.json
03A_leader_business_anatomy.raw.md
03A_leader_business_anatomy.json
03B_leader_future_optionality.raw.md
03B_leader_future_optionality.json
03_chokepoint_scores.raw.md
03_chokepoint_scores.json
04_company_discovery.raw.md
04_company_discovery.json
05_commercial_validation.raw.md
05_commercial_validation.json
06_valuation_crowding.raw.md
06_valuation_crowding.json
07_bear_case.raw.md
07_bear_case.json
08_final_ranking.raw.md
08_final_ranking.json
quality_gate_audit.md
quality_gate_audit.json
final_report.md
run_metadata.json
```

## Evidence Rules

Separate evidence into:

- `hard_evidence`
- `soft_evidence`
- `inference`
- `missing_evidence`

Any claim about price, market cap, enterprise value, revenue, cash, debt, free cash flow, valuation, backlog, contracts, segment revenue, customer concentration, ownership, short interest, or price performance must be grounded in local company profiles, connector outputs, cached filings, or cited source evidence.

If data is unavailable, mark it missing. Do not infer:

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

## Future Optionality Rules

Use `03B_LEADER_FUTURE_OPTIONALITY.md` only for scenario analysis.

Future optionality must never be treated as current commercial validation.

Only `F3` or `F4` future scenarios may pass into main chokepoint scoring. `F0`, `F1`, and `F2` scenarios belong in a scenario watchlist and cannot support a `High Priority Research` classification by themselves.

## Allowed Final Categories

Use only:

- `High Priority Research`
- `Watchlist`
- `Wait for Pullback`
- `Observe`
- `Reject`

Do not output `Buy`, `Sell`, or `Hold`.

## Quality Gate

Create a quality gate output after final ranking:

```text
quality_gate_audit.md
quality_gate_audit.json
```

For each final company, score:

- evidence_strength_score
- data_completeness_score
- valuation_confidence_score
- commercial_validation_confidence_score
- crowding_confidence_score
- should_keep_rating
- suggested_rating_change
- reason

The quality gate should identify:

- companies rated too generously
- companies with missing critical evidence
- claims supported by live or cached data
- claims that are only inference
- files that need improvement before investment-grade use

## Final Response

After the run finishes, summarize:

- output folder path
- whether all expected files were created
- top chokepoint segments
- top candidate companies
- final category distribution
- tickers with missing live data
- invalid JSON repairs or errors
- whether future optionality was kept separate from current validation
- biggest remaining data gap
