# 11 Independent Valuation and Entry Readiness Skill

## Purpose

Run an independent valuation and entry-readiness check after a single-company deep dive.

This module determines whether a company is attractive for manual investment review at the current price using grounded evidence, scenario valuation, margin-of-safety analysis, and explicit evidence gating.

This is not a trading recommendation engine. Do not output `Buy`, `Sell`, or `Hold`.

## When to Use

Run after a company deep dive has been completed.

Recommended sequence:

1. Sector workflow.
2. Company deep dive.
3. Independent valuation and entry-readiness check.

## Input

```json
{
  "ticker": "",
  "company_name": "",
  "theme": "",
  "company_deep_dive": {},
  "final_ranking_output": {},
  "company_profile": {},
  "market_data": {},
  "commercial_validation_evidence": {},
  "valuation_crowding_output": {},
  "bear_case_output": {},
  "quality_gate_output": {},
  "cached_source_files": []
}
```

## Prior Research Integration

This module must not produce generic valuation commentary. It must explicitly connect valuation assumptions to prior Serenity research conclusions.

Read and use:

- company deep dive output;
- final ranking output;
- quality gate output;
- commercial validation evidence;
- market data v2;
- bear case output;
- cached SEC and filing evidence where available.

Explain how prior conclusions affect valuation assumptions.

Examples:

- Strong backlog evidence may support a higher revenue CAGR assumption.
- Weak segment revenue evidence should reduce confidence or lower the valuation multiple.
- Negative or unstable free cash flow should reduce valuation attractiveness.
- Stretched EV/Sales or EV/EBITDA should reduce margin of safety.
- Weak commercial validation should prevent aggressive bull-case assumptions.
- A strong bear case should widen downside assumptions and lower scenario confidence.

Required output:

- identify the previous research conclusions that most affected the valuation;
- map each key scenario assumption to the prior output or source evidence that supports, weakens, or limits it;
- clearly label where a scenario uses analyst judgment rather than hard evidence.

## Evidence Rules

Use only grounded data from:

- company deep dive markdown or JSON;
- company profile and market data connector output;
- commercial validation evidence;
- valuation and crowding output;
- bear case output;
- quality gate output;
- cached SEC filings and source evidence files.

Do not invent missing data.

Any claim about price, market cap, enterprise value, revenue, cash, debt, net debt, free cash flow, valuation multiples, shares outstanding, stock performance, backlog, contracts, customer concentration, segment revenue, ownership, short interest, or analyst coverage must be grounded in the provided sources or marked as missing.

Classify evidence as:

- `hard_evidence`
- `soft_evidence`
- `inference`
- `missing_evidence`
- `assumption`

## Allowed Final Entry Categories

Use only:

- `Attractive for Manual Review`
- `Watch for Better Entry`
- `Too Expensive`
- `Insufficient Evidence`
- `Avoid`

Do not output `Buy`, `Sell`, or `Hold`.

## Required Analysis

### 1. Current Market Snapshot

Use only grounded data. Include available values and mark unavailable values as `unknown` or `null`.

Required fields:

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

### 2. Business Quality Underwriting

Assess:

- revenue quality;
- margin quality;
- free cash flow quality;
- balance sheet quality;
- customer concentration risk;
- cyclicality;
- capital intensity;
- evidence quality.

Separate proven evidence from assumptions.

### 3. Scenario Assumptions

Create three scenarios:

- Bear Case;
- Base Case;
- Bull Case.

For each scenario, define:

- revenue CAGR assumption;
- terminal revenue estimate;
- EBITDA margin assumption;
- FCF margin assumption;
- appropriate valuation multiple;
- net debt adjustment;
- fair enterprise value;
- fair equity value;
- fair value per share;
- upside or downside versus current price;
- key thesis assumptions;
- key evidence supporting the scenario;
- key evidence weakening the scenario;
- confidence level.

If an assumption is not directly supported by evidence, label it as an assumption. Do not treat scenario assumptions as facts.

### 4. Assumption Evidence Table

Every key valuation assumption must include:

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

The assumption evidence table must include, when applicable:

- revenue CAGR;
- terminal revenue;
- EBITDA margin;
- FCF margin;
- valuation multiple;
- net debt adjustment;
- shares outstanding;
- normalized free cash flow;
- business quality adjustment;
- margin of safety adjustment.

### 4. Valuation Methods

Use at least two valuation approaches where possible:

- EV/Sales scenario valuation;
- EV/EBITDA scenario valuation;
- FCF yield or simplified FCF valuation if free cash flow is meaningful;
- DCF only if assumptions are sufficiently grounded.

If free cash flow is negative, unstable, or not representative, do not force a DCF. Explain why DCF is unreliable.

### 5. Valuation Method Selection Rules

Choose valuation methods based on business type and data quality.

- Use EV/Sales when revenue growth is meaningful but EBITDA or free cash flow is unstable.
- Use EV/EBITDA when EBITDA is positive and meaningful.
- Use FCF yield or simplified FCF valuation when free cash flow is positive and durable.
- Use P/E only when earnings are positive and meaningful.
- Use DCF only when free cash flow assumptions are sufficiently grounded.
- Do not force DCF for companies with negative or unstable free cash flow.
- If the company is a contractor or services firm, consider EV/EBITDA, FCF yield, backlog quality, and normalized margin.
- If the company is a hardware or high-growth supplier, consider EV/Sales, gross margin, revenue growth, and cash burn.

Explain which method is most appropriate and why. Also explain which methods were rejected and why.

### 6. Explicit Formulas

Show formulas in the Markdown output and preserve formula strings in JSON.

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

Only compute values when the required source fields are available. If required source fields are missing, mark the affected result as `unknown`.

### 7. Fair Value Range

Estimate:

- bear case fair value per share;
- base case fair value per share;
- bull case fair value per share;
- current price;
- implied upside or downside to base case;
- implied upside or downside to bull case;
- implied downside to bear case.

Use transparent formulas.

If shares outstanding, enterprise value bridge, cash, debt, or free cash flow are missing, mark affected outputs as `unknown` and explain the missing fields.

### 8. Margin of Safety

Assess:

- whether current price offers margin of safety;
- what entry price would be more attractive for manual review;
- what valuation multiple would be acceptable;
- what evidence would justify paying the current valuation.

Do not present the entry price as a trading instruction. Treat it as a research threshold.

### 9. Valuation Discipline Rules

Do not use aggressive bull-case assumptions unless all are true:

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

### 10. Entry Readiness Gate

Score each category from 0 to 100:

- thesis quality score;
- evidence quality score;
- valuation attractiveness score;
- margin of safety score;
- downside risk score;
- timing score;
- final entry readiness score.

Higher scores mean better research readiness and more attractive current evidence/valuation balance.

### 11. Final Entry Category

Classify using only the allowed final entry categories.

Category guidance:

- `Attractive for Manual Review`: Strong thesis, strong evidence, reasonable valuation, and adequate margin of safety.
- `Watch for Better Entry`: Good or improving thesis, but valuation, crowding, timing, or missing evidence prevents current attractiveness.
- `Too Expensive`: Business may be strong, but current valuation leaves poor margin of safety.
- `Insufficient Evidence`: Key data is missing or too much of the thesis depends on inference.
- `Avoid`: Evidence, quality, valuation, balance sheet, or downside risk is unfavorable enough that further research is low priority.

## Required Direct Answers

Answer directly:

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

## Output Format

Return Markdown and JSON.

### Markdown Structure

```markdown
# Independent Valuation Check: [TICKER]

## Summary

...

## Current Market Snapshot

...

## Business Quality Underwriting

...

## Scenario Assumptions

...

## Assumption Evidence Table

...

## Valuation Methods

...

## Fair Value Range

...

## Margin of Safety

...

## Entry Readiness Gate

...

## Final Entry Category

...

## Direct Answers

...

## Evidence Quality and Missing Data

...

## Important Note

This is for research purposes only. It is not a buy, sell, or hold recommendation.
```

### JSON Structure

```json
{
  "ticker": "",
  "company_name": "",
  "theme": "",
  "prior_research_integration": {
    "company_deep_dive_conclusions_used": [],
    "final_ranking_conclusions_used": [],
    "quality_gate_conclusions_used": [],
    "commercial_validation_conclusions_used": [],
    "market_data_conclusions_used": [],
    "bear_case_conclusions_used": [],
    "cached_filing_evidence_used": [],
    "valuation_assumption_impacts": []
  },
  "current_market_snapshot": {
    "current_price": null,
    "market_cap": null,
    "enterprise_value": null,
    "shares_outstanding": null,
    "cash": null,
    "debt": null,
    "net_debt": null,
    "revenue_ttm": null,
    "gross_margin": null,
    "free_cash_flow": null,
    "ev_to_sales": null,
    "price_to_sales": null,
    "ev_to_ebitda": null,
    "price_change_1m": null,
    "price_change_3m": null,
    "price_change_6m": null,
    "price_change_12m": null,
    "distance_from_52w_high": null,
    "distance_from_52w_low": null
  },
  "business_quality_underwriting": {
    "revenue_quality": "",
    "margin_quality": "",
    "free_cash_flow_quality": "",
    "balance_sheet_quality": "",
    "customer_concentration_risk": "",
    "cyclicality": "",
    "capital_intensity": "",
    "evidence_quality": ""
  },
  "assumption_evidence_table": [
    {
      "assumption_name": "",
      "assumption_value": "",
      "source_from_prior_research": "",
      "evidence_type": "hard_evidence | soft_evidence | inference | assumption",
      "confidence": "high | medium | low",
      "reason": ""
    }
  ],
  "scenarios": [
    {
      "name": "Bear Case",
      "revenue_cagr_assumption": "",
      "terminal_revenue_estimate": null,
      "ebitda_margin_assumption": "",
      "fcf_margin_assumption": "",
      "valuation_multiple": "",
      "net_debt_adjustment": null,
      "fair_enterprise_value": null,
      "fair_equity_value": null,
      "fair_value_per_share": null,
      "upside_downside_vs_current_price": null,
      "key_thesis_assumptions": [],
      "supporting_evidence": [],
      "weakening_evidence": [],
      "confidence_level": "high | medium | low",
      "assumption_quality": "high | medium | low"
    }
  ],
  "valuation_method_selection": {
    "business_type": "",
    "selected_methods": [],
    "rejected_methods": [
      {
        "method": "",
        "reason": ""
      }
    ],
    "most_appropriate_method": "",
    "reason": ""
  },
  "formulas": {
    "revenue_n": "Revenue_N = Revenue_TTM * (1 + revenue_CAGR)^N",
    "fair_ev_from_sales": "Fair_EV_from_sales = Revenue_N * target_EV_Sales_multiple",
    "ebitda_n": "EBITDA_N = Revenue_N * EBITDA_margin",
    "fair_ev_from_ebitda": "Fair_EV_from_EBITDA = EBITDA_N * target_EV_EBITDA_multiple",
    "equity_value": "Equity_Value = Fair_EV - Net_Debt",
    "fair_value_per_share": "Fair_Value_Per_Share = Equity_Value / Shares_Outstanding",
    "upside_downside": "Upside_Downside = Fair_Value_Per_Share / Current_Price - 1",
    "fair_equity_value_from_fcf_yield": "Fair_Equity_Value = Normalized_FCF / Target_FCF_Yield"
  },
  "valuation_methods": {
    "ev_sales_scenario_valuation": {},
    "ev_ebitda_scenario_valuation": {},
    "fcf_yield_valuation": {},
    "dcf": {
      "used": false,
      "reason": ""
    }
  },
  "fair_value_range": {
    "bear_case_fair_value_per_share": null,
    "base_case_fair_value_per_share": null,
    "bull_case_fair_value_per_share": null,
    "current_price": null,
    "implied_upside_downside_to_base": null,
    "implied_upside_downside_to_bull": null,
    "implied_downside_to_bear": null
  },
  "margin_of_safety": {
    "current_price_margin_of_safety": "",
    "more_attractive_manual_review_price": null,
    "acceptable_valuation_multiple": "",
    "evidence_needed_to_justify_current_valuation": []
  },
  "entry_readiness_gate": {
    "thesis_quality_score": 0,
    "evidence_quality_score": 0,
    "valuation_attractiveness_score": 0,
    "margin_of_safety_score": 0,
    "downside_risk_score": 0,
    "timing_score": 0,
    "final_entry_readiness_score": 0
  },
  "final_entry_category": "Attractive for Manual Review | Watch for Better Entry | Too Expensive | Insufficient Evidence | Avoid",
  "direct_answers": {
    "previous_research_conclusions_most_affected_valuation": [],
    "hard_evidence_based_assumptions": [],
    "inferred_assumptions": [],
    "most_appropriate_valuation_method": "",
    "base_case_fair_value_range": "",
    "bull_case_fair_value_range": "",
    "bear_case_downside": "",
    "current_price_attractive_enough_for_manual_review": "",
    "fundamentally_attractive": "",
    "current_valuation_reasonable": "",
    "enough_margin_of_safety": "",
    "more_attractive_price_or_valuation": "",
    "evidence_to_upgrade_entry_category": [],
    "evidence_to_force_downgrade": [],
    "research_posture": "consider now | wait | avoid for now"
  },
  "evidence_quality": {
    "hard_evidence": [],
    "soft_evidence": [],
    "inference": [],
    "missing_evidence": []
  },
  "source_files": []
}
```

## Reject Rules

Do not provide trading instructions.

Do not use `Buy`, `Sell`, or `Hold`.

Do not treat a valuation scenario as a price target unless the valuation method, assumptions, and evidence limits are explicit.

Do not upgrade a company based only on speculative future optionality.

Do not hide missing market data, contracts, backlog, segment revenue, customer concentration, ownership, short interest, or valuation fields.

## Next Step

Save outputs as:

```text
outputs/[run_folder]/[TICKER]_valuation_check_v1.md
outputs/[run_folder]/[TICKER]_valuation_check_v1.json
```
