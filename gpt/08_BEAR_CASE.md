# 08 Bear Case Skill

## Purpose

Stress-test each candidate by attacking the investment thesis.

This skill exists to prevent attractive narratives from entering the final watchlist without sufficient skepticism.

## When to Use

Run after `07_FINANCIAL_VALUATION_CROWDING.md`.

## Input

```json
{
  "theme": "",
  "valuation_results": [],
  "commercial_validation_results": [],
  "chokepoint_results": []
}
```

## Process

For each company, write the strongest realistic bear case.

The bear case should test:

1. Whether the segment is actually a chokepoint.
2. Whether the company truly benefits from the segment.
3. Whether commercial evidence is strong enough.
4. Whether valuation already prices the upside.
5. Whether there are execution, margin, customer, debt, dilution, or cyclical risks.
6. Whether competitors could capture the economics instead.
7. Whether the market already understands the story.

## Bear Case Categories

Evaluate each company across these categories:

- Chokepoint risk
- Business relevance risk
- Commercial validation risk
- Customer concentration risk
- Competition/substitution risk
- Margin risk
- Execution/capacity risk
- Balance sheet/dilution risk
- Valuation risk
- Crowding/repricing risk
- Cyclical or macro risk
- Management credibility risk

## Thesis Kill Conditions

Identify conditions that would invalidate the thesis.

Examples:

- Backlog does not convert to revenue.
- Growth is driven by one-time orders.
- Customer capex slows.
- Margins decline despite demand growth.
- A larger competitor takes share.
- The company must dilute shareholders.
- The relevant segment is too small to affect valuation.
- The stock already prices in unrealistic growth.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "bear_cases": [
    {
      "ticker": "",
      "company_name": "",
      "core_bull_thesis": "",
      "strongest_bear_case": "",
      "risk_breakdown": {
        "chokepoint_risk": "low | medium | high | unknown",
        "business_relevance_risk": "low | medium | high | unknown",
        "commercial_validation_risk": "low | medium | high | unknown",
        "competition_substitution_risk": "low | medium | high | unknown",
        "margin_risk": "low | medium | high | unknown",
        "execution_capacity_risk": "low | medium | high | unknown",
        "balance_sheet_dilution_risk": "low | medium | high | unknown",
        "valuation_risk": "low | medium | high | unknown",
        "crowding_risk": "low | medium | high | unknown",
        "cyclical_macro_risk": "low | medium | high | unknown"
      },
      "thesis_kill_conditions": [],
      "evidence_against_thesis": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ],
      "bear_case_severity": "low | medium | high",
      "recommended_adjustment": "upgrade | keep | downgrade | reject | wait_for_pullback",
      "summary": ""
    }
  ],
  "summary": ""
}
```

## Scoring Rules

- `low` bear severity: risks exist but do not currently break the thesis.
- `medium` bear severity: risks are meaningful and require monitoring.
- `high` bear severity: risks may invalidate the thesis or make valuation unattractive.

## Reject Rules

Recommend `reject` if:

1. The company is not truly exposed to the chokepoint.
2. Commercial validation is mostly narrative.
3. Valuation already assumes aggressive success.
4. Debt/dilution risk can destroy upside.
5. A major risk is already visible but not reflected in the bull case.

## Next Step

Pass bear-case adjusted results to `09_FINAL_RANKING.md`.
