# 02 Theme Research Skill

## Purpose

Evaluate whether the input theme represents a real structural trend worth researching.

This skill does not identify stocks. It determines whether the top-down theme is strong enough to justify deeper value-chain research.

## When to Use

Run this immediately after receiving a user-provided theme.

Example themes:

- AI data center power infrastructure
- Grid infrastructure
- Defense electronics
- Nuclear energy supply chain
- Industrial automation
- Water infrastructure
- Robotics components

## Input

```json
{
  "theme": "",
  "market": "US stocks",
  "time_horizon": "3-5 years",
  "user_constraints": {}
}
```

## Process

Analyze the theme through the following lenses:

1. Define the theme clearly.
2. Identify the structural demand drivers.
3. Identify the downstream spending sources.
4. Determine whether demand is cyclical, secular, policy-driven, or hype-driven.
5. Identify relevant capex, regulatory, technological, or customer adoption drivers.
6. Identify whether the theme has already become a crowded market narrative.
7. Determine whether there are likely value-chain bottlenecks worth investigating.
8. Separate hard evidence, soft evidence, and inference.

## Key Questions

- What real-world problem does this theme solve?
- Who is spending money because of this trend?
- Is spending already happening, or is it only forecasted?
- What part of the economy must expand for the theme to materialize?
- Does the theme depend on one uncertain event, or many independent drivers?
- Is this already a consensus market narrative?
- Are there supply constraints that could create pricing power?
- Is there a likely path to company-level revenue growth?

## Scoring Rules

Score the theme from 0 to 100.

| Factor | Weight |
|---|---:|
| Demand certainty | 20 |
| Multi-year durability | 15 |
| Evidence of real spending/capex | 20 |
| Value-chain bottleneck potential | 20 |
| Market underappreciation potential | 15 |
| Risk of hype or overpricing | 10 |

For `risk_of_hype_or_overpricing`, a lower hype risk should produce a higher score.

## Required Evidence

For each major claim, provide source-backed evidence if available.

Acceptable evidence types:

- filings;
- government data;
- company investor presentations;
- earnings calls;
- industry reports;
- customer capex disclosures;
- reputable news or trade publications.

If evidence is not available, mark the claim as an inference.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "theme_definition": "",
  "time_horizon": "3-5 years",
  "theme_score": 0,
  "theme_rating": "Strong | Moderate | Weak | Reject",
  "demand_drivers": [
    {
      "driver": "",
      "evidence_type": "hard | soft | inference",
      "evidence_summary": "",
      "source": ""
    }
  ],
  "spending_sources": [],
  "why_now": [],
  "bottleneck_hypotheses": [],
  "crowding_risk": "low | medium | high | unknown",
  "major_risks": [],
  "missing_data": [],
  "continue_to_value_chain": true,
  "summary": ""
}
```

## Reject Rules

Reject or downgrade the theme if:

1. Demand is mainly narrative-driven with little spending evidence.
2. The theme requires too many uncertain assumptions.
3. The value chain has no plausible bottleneck.
4. The entire theme is already extremely crowded and fully repriced.
5. Public companies exposed to the theme are too loosely connected.

## Next Step

If `continue_to_value_chain` is true, pass the output to `03_VALUE_CHAIN_DECOMPOSITION.md`.
