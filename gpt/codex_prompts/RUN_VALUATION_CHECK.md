# Run Valuation Check

Use this prompt to run an independent Serenity valuation and entry-readiness check in Codex-agent mode after a company deep dive.

## Parameters

Fill in or infer from the user request:

```json
{
  "existing_run_folder": "",
  "ticker": "",
  "company_name": "",
  "theme": ""
}
```

## Execution Mode

Use Codex-agent reasoning and local files.

Do not:

- Rerun the full sector workflow.
- Call the OpenAI API runner.
- Ask for `OPENAI_API_KEY`.
- Modify the `gpt/` markdown investment logic.
- Build the web app.
- Add trading, brokerage, portfolio, auto-buy, or order execution features.
- Output `Buy`, `Sell`, or `Hold`.
- Invent missing market, valuation, contract, backlog, revenue, customer, or ownership data.

## Required Skill File

Read:

```text
gpt/11_INDEPENDENT_VALUATION.md
```

Also read supporting files if needed:

```text
gpt/00_SYSTEM_PRINCIPLES.md
gpt/07_FINANCIAL_VALUATION_CROWDING.md
gpt/08_BEAR_CASE.md
gpt/09_FINAL_RANKING.md
gpt/99_OUTPUT_FORMATS.md
```

## Required Inputs

Use the existing run folder and local cached evidence.

Prioritize these files when available:

```text
[existing_run_folder]/[TICKER]_deep_dive.md
[existing_run_folder]/[TICKER]_deep_dive.json
[existing_run_folder]/data/company_profiles.json
[existing_run_folder]/data/company_profiles_v2.json
[existing_run_folder]/data/data_quality_report.json
[existing_run_folder]/data/data_quality_report_v2.json
[existing_run_folder]/data/commercial_validation*.json
[existing_run_folder]/05_commercial_validation*.json
[existing_run_folder]/06_valuation_crowding*.json
[existing_run_folder]/07_bear_case*.json
[existing_run_folder]/08_final_ranking*.json
[existing_run_folder]/quality_gate_audit*.json
data_cache/
```

If multiple versions exist, prefer the latest version by suffix or timestamp, unless the user specifies otherwise.

## Prior Research Integration

The valuation check must explicitly use prior research conclusions. It must not produce generic valuation commentary.

Read and connect assumptions to:

- company deep dive output;
- final ranking output;
- quality gate output;
- commercial validation evidence;
- market data v2;
- bear case output;
- cached SEC and filing evidence where available.

Explain how prior conclusions affect valuation assumptions.

Examples:

- Strong backlog evidence may support a higher revenue CAGR.
- Weak segment revenue evidence should reduce confidence or lower the valuation multiple.
- Negative or unstable free cash flow should reduce valuation attractiveness.
- Stretched EV/Sales or EV/EBITDA should reduce margin of safety.
- Weak commercial validation should prevent aggressive bull-case assumptions.
- A strong bear case should widen downside assumptions.

## Required Analysis

Produce an independent valuation framework and entry-readiness assessment.

Required sections:

1. Current market snapshot.
2. Business quality underwriting.
3. Bear, base, and bull scenario assumptions.
4. Assumption evidence table.
5. Valuation method selection.
6. Explicit formulas.
7. Valuation methods.
8. Fair value range.
9. Margin of safety.
10. Entry readiness gate.
11. Final entry category.
12. Required direct answers.
13. Evidence quality and missing data.

## Grounded Data Rules

Use only grounded data for:

- current price;
- market cap;
- enterprise value;
- shares outstanding;
- cash;
- debt;
- net debt;
- revenue TTM;
- gross margin;
- free cash flow;
- EV/Sales;
- Price/Sales;
- EV/EBITDA;
- price change 1 month;
- price change 3 months;
- price change 6 months;
- price change 12 months;
- distance from 52-week high;
- distance from 52-week low.

If a field is missing, keep it missing.

Do not infer:

- market cap;
- enterprise value;
- shares outstanding;
- cash;
- debt;
- net debt;
- revenue;
- free cash flow;
- valuation multiples;
- backlog;
- contract values;
- customer concentration;
- ownership;
- short interest.

Only compute values when the source fields are present and the formula is explicit. Record the formula.

## Evidence Classification

Classify evidence as:

- `hard_evidence`
- `soft_evidence`
- `inference`
- `missing_evidence`

Scenario assumptions must be labeled as assumptions unless directly supported by hard evidence.

Future optionality may be included only as scenario analysis. Do not treat speculative optionality as current commercial validation.

## Assumption Evidence Table

Every key assumption must include:

```json
{
  "assumption_name": "",
  "assumption_value": "",
  "source_from_prior_research": "",
  "evidence_type": "hard_evidence | soft_evidence | inference | assumption",
  "confidence": "high | medium | low",
  "reason": ""
}
```

Include assumptions for revenue CAGR, terminal revenue, EBITDA margin, FCF margin, valuation multiple, net debt adjustment, shares outstanding, normalized free cash flow, business quality adjustment, and margin of safety adjustment where applicable.

## Valuation Methods

Use at least two methods where possible:

- EV/Sales scenario valuation;
- EV/EBITDA scenario valuation;
- FCF yield or simplified FCF valuation if free cash flow is meaningful;
- DCF only if assumptions are sufficiently grounded.

If free cash flow is negative, unstable, or not representative, do not force a DCF. Explain why DCF is unreliable.

## Valuation Method Selection Rules

Choose valuation methods based on business type and data quality:

- Use EV/Sales when revenue growth is meaningful but EBITDA or free cash flow is unstable.
- Use EV/EBITDA when EBITDA is positive and meaningful.
- Use FCF yield or simplified FCF valuation when free cash flow is positive and durable.
- Use P/E only when earnings are positive and meaningful.
- Use DCF only when free cash flow assumptions are sufficiently grounded.
- Do not force DCF for companies with negative or unstable free cash flow.
- If the company is a contractor or services firm, consider EV/EBITDA, FCF yield, backlog quality, and normalized margin.
- If the company is a hardware or high-growth supplier, consider EV/Sales, gross margin, revenue growth, and cash burn.

Explain which method is most appropriate and why. Also explain which methods were rejected and why.

## Explicit Formulas

Show formulas in Markdown and preserve formula strings in JSON.

Required formulas:

```text
Revenue_N = Revenue_TTM * (1 + revenue_CAGR)^N

Fair_EV_from_sales = Revenue_N * target_EV_Sales_multiple

EBITDA_N = Revenue_N * EBITDA_margin

Fair_EV_from_EBITDA = EBITDA_N * target_EV_EBITDA_multiple

Equity_Value = Fair_EV - Net_Debt

Fair_Value_Per_Share = Equity_Value / Shares_Outstanding

Upside_Downside = Fair_Value_Per_Share / Current_Price - 1
```

If using FCF yield:

```text
Fair_Equity_Value = Normalized_FCF / Target_FCF_Yield

Fair_Value_Per_Share = Fair_Equity_Value / Shares_Outstanding
```

Only compute values when required source fields are available. If required source fields are missing, mark the affected result as `unknown`.

## Scenario Requirements

Create Bear, Base, and Bull cases.

For each scenario, provide:

- revenue CAGR;
- terminal revenue;
- EBITDA margin if applicable;
- FCF margin if applicable;
- valuation multiple;
- net debt adjustment;
- fair enterprise value;
- fair equity value;
- fair value per share;
- upside or downside versus current price;
- key evidence supporting the scenario;
- key evidence weakening the scenario;
- confidence level.

## Valuation Discipline Rules

Do not use aggressive bull-case assumptions unless:

- commercial validation is strong;
- relevant segment revenue is material or likely material;
- valuation is not already excessive;
- free cash flow or path to free cash flow is credible;
- bear case risks are survivable.

If segment revenue, backlog, contracts, or customer evidence are missing:

- lower confidence;
- avoid aggressive multiples;
- mark the valuation as evidence-gated;
- avoid classifying the company as `Attractive for Manual Review` unless the margin of safety is very large.

## Allowed Final Entry Categories

Use only:

- `Attractive for Manual Review`
- `Watch for Better Entry`
- `Too Expensive`
- `Insufficient Evidence`
- `Avoid`

Do not output `Buy`, `Sell`, or `Hold`.

## Required Scores

Score from 0 to 100:

- thesis_quality_score;
- evidence_quality_score;
- valuation_attractiveness_score;
- margin_of_safety_score;
- downside_risk_score;
- timing_score;
- final_entry_readiness_score.

## Required Direct Answers

Specifically answer:

- Which previous research conclusions most affected the valuation?
- Which assumptions are hard-evidence-based?
- Which assumptions are only inferred?
- Which valuation method is most appropriate and why?
- What is the base-case fair value range?
- What is the bull-case fair value range?
- What is the bear-case downside?
- Is the current price attractive enough for manual review?
- Is the company fundamentally attractive?
- Is the current valuation reasonable?
- Is there enough margin of safety?
- What price or valuation level would make it more attractive?
- What evidence would justify upgrading the entry category?
- What evidence would force a downgrade?
- Is this a `consider now`, `wait`, or `avoid for now` situation?

Use research language, not trading instructions.

## Output Files

Save:

```text
[existing_run_folder]/[TICKER]_valuation_check_v1.md
[existing_run_folder]/[TICKER]_valuation_check_v1.json
```

If versioning is needed because files already exist, append the next version suffix:

```text
[existing_run_folder]/[TICKER]_valuation_check_v2.md
[existing_run_folder]/[TICKER]_valuation_check_v2.json
```

## Required JSON Structure

Use the JSON schema from `gpt/11_INDEPENDENT_VALUATION.md`.

## Final Response

After completion, summarize:

- output files created;
- final entry category;
- previous research conclusions that most affected valuation;
- most appropriate valuation method;
- base-case fair value range;
- bull-case fair value range;
- bear-case downside;
- whether the company is fundamentally attractive;
- whether current valuation is reasonable;
- whether margin of safety is adequate;
- more attractive manual-review price or valuation level;
- evidence needed to upgrade;
- evidence that would force downgrade;
- key missing evidence fields.
