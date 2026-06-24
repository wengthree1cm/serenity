# 05 Company Discovery Skill

## Purpose

Identify publicly traded companies connected to the highest-scoring chokepoint segments.

This skill creates the candidate company pool. It does not make final judgments.

## When to Use

Run after `04_CHOKEPOINT_SCORING.md` identifies segments with `recommended_action = continue`.

## Input

```json
{
  "theme": "",
  "top_chokepoint_segments": [],
  "market": "US stocks",
  "market_cap_min": 300000000,
  "market_cap_max": 20000000000,
  "exclude": ["OTC", "SPAC", "pre-revenue biotech"]
}
```

## Process

For each chokepoint segment:

1. Identify public companies with direct exposure.
2. Separate direct exposure from indirect or loose thematic exposure.
3. Prefer companies where the relevant segment is material enough to affect valuation.
4. Identify whether the company is pure-play, partial exposure, or conglomerate exposure.
5. Apply basic investability filters.
6. Create a candidate pool for commercial validation.

## Investability Filters

Default filters:

- Publicly traded company.
- Valid ticker.
- Prefer US-listed stocks unless user specifies otherwise.
- Market cap between user-specified range.
- Sufficient liquidity.
- Exclude OTC unless user explicitly allows.
- Exclude SPACs unless de-SPACed and operating company has sufficient filings.
- Exclude companies with no operating revenue unless the user explicitly wants speculative research.

## Business Relevance Score

Score each company from 0 to 100.

| Factor | Weight |
|---|---:|
| Direct exposure to chokepoint segment | 30 |
| Materiality of segment to company revenue/profit | 25 |
| Competitive position in segment | 20 |
| Ability to benefit from demand acceleration | 15 |
| Public data availability | 10 |

## Exposure Categories

Use one of:

- `pure_play`: majority of business tied to target segment.
- `high_exposure`: meaningful segment exposure that can drive valuation.
- `partial_exposure`: relevant but not enough alone to drive thesis.
- `loose_exposure`: thematically related but weak.
- `not_relevant`: reject.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "candidate_companies": [
    {
      "ticker": "",
      "company_name": "",
      "exchange": "",
      "market_cap": "unknown",
      "segment_id": "",
      "segment_name": "",
      "exposure_category": "pure_play | high_exposure | partial_exposure | loose_exposure | not_relevant",
      "business_relevance_score": 0,
      "business_description": "",
      "why_relevant": "",
      "why_may_be_irrelevant": "",
      "known_customers_or_end_markets": [],
      "data_sources_to_check_next": [],
      "evidence": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ],
      "continue_to_commercial_validation": true
    }
  ],
  "rejected_companies": [],
  "summary": ""
}
```

## Reject Rules

Reject or downgrade companies if:

1. They are only loosely related to the theme.
2. The relevant segment is too small to affect valuation.
3. There is no public information to verify the exposure.
4. The company is pre-revenue or purely promotional.
5. The company is too illiquid for the user's scope.
6. The company is already a mega-cap where hidden discovery is unlikely, unless it is included only as a benchmark.

## Next Step

Pass companies with `continue_to_commercial_validation = true` to `06_COMMERCIAL_VALIDATION.md`.
