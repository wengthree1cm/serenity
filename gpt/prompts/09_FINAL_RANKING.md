# 09 Final Ranking Skill

## Purpose

Combine all prior outputs into a final research ranking.

This skill creates a prioritized watchlist, but it must not produce buy/sell recommendations.

## When to Use

Run after `08_BEAR_CASE.md`.

## Input

```json
{
  "theme": "",
  "theme_research": {},
  "chokepoint_scores": {},
  "company_discovery": {},
  "commercial_validation": {},
  "valuation_crowding": {},
  "bear_case": {}
}
```

## Final Score

Score each company from 0 to 100.

| Factor | Weight |
|---|---:|
| Theme strength | 15 |
| Value-chain importance | 15 |
| Chokepoint strength | 20 |
| Business relevance | 10 |
| Commercial validation | 15 |
| Valuation discipline | 10 |
| Low crowding / underappreciation | 5 |
| Catalyst clarity | 5 |
| Risk control after bear case | 5 |

## Classification Rules

### High Priority Research

Use this classification when:

- final score >= 82;
- commercial validation level is 2 or 3;
- valuation is not very stretched;
- crowding is not high;
- bear case severity is not high;
- at least one meaningful catalyst exists.

### Watchlist

Use this classification when:

- final score is 70–81; or
- thesis is attractive but needs more evidence; or
- commercial validation is Level 2 but not enough hard evidence yet.

### Wait for Pullback

Use this classification when:

- company quality and commercial validation are strong;
- valuation or crowding is the main problem;
- the market has already substantially repriced the thesis.

### Observe

Use this classification when:

- the theme is relevant;
- company exposure is plausible;
- but evidence is too early, weak, or incomplete.

### Reject

Use this classification when:

- business relevance is weak;
- commercial validation is absent;
- the bear case is thesis-breaking;
- valuation is extreme without evidence;
- the company is mostly a concept stock.

## Catalyst Assessment

Identify possible 6–24 month catalysts:

- next earnings report;
- backlog conversion;
- customer award;
- guidance raise;
- margin expansion;
- capacity ramp;
- regulatory approval;
- customer capex cycle;
- industry shortage becoming visible;
- analyst coverage initiation;
- balance sheet improvement.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "final_rankings": [
    {
      "rank": 1,
      "ticker": "",
      "company_name": "",
      "segment_name": "",
      "final_score": 0,
      "classification": "High Priority Research | Watchlist | Wait for Pullback | Observe | Reject",
      "score_breakdown": {
        "theme_strength": 0,
        "value_chain_importance": 0,
        "chokepoint_strength": 0,
        "business_relevance": 0,
        "commercial_validation": 0,
        "valuation_discipline": 0,
        "low_crowding_underappreciation": 0,
        "catalyst_clarity": 0,
        "risk_control": 0
      },
      "one_sentence_thesis": "",
      "key_evidence": [],
      "key_risks": [],
      "near_term_catalysts": [],
      "what_to_verify_next": [],
      "why_not_higher": "",
      "why_not_reject": ""
    }
  ],
  "classification_summary": {
    "high_priority_research": [],
    "watchlist": [],
    "wait_for_pullback": [],
    "observe": [],
    "reject": []
  },
  "portfolio_research_notes": "",
  "summary": ""
}
```

## Tie-Breaking Rules

If two companies have similar scores, rank higher the company with:

1. Stronger commercial validation.
2. Lower crowding.
3. More direct chokepoint exposure.
4. Cleaner balance sheet.
5. Clearer catalysts.
6. More attractive risk/reward after bear-case adjustment.

## Next Step

Pass final rankings to `10_REPORT_WRITER.md`.
