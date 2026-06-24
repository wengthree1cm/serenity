# 04 Chokepoint Scoring Skill

## Purpose

Score each value-chain segment to determine which segments are true chokepoints and deserve company-level research.

## When to Use

Run after `03_VALUE_CHAIN_DECOMPOSITION.md`.

## Input

```json
{
  "theme": "",
  "segments": []
}
```

## Process

For each segment, evaluate whether it is a true chokepoint or merely thematically related.

A true chokepoint should have multiple reinforcing traits:

1. Downstream customers must use it.
2. There are few qualified suppliers.
3. Customers cannot switch easily.
4. Capacity expansion is slow.
5. Technical, engineering, regulatory, or certification barriers exist.
6. Demand acceleration can create pricing power, margin expansion, or backlog growth.
7. The market may not fully appreciate the segment.

## Chokepoint Score

Assign a score from 0 to 100.

| Factor | Weight |
|---|---:|
| Downstream necessity | 20 |
| Supplier scarcity | 15 |
| Customer switching cost | 15 |
| Capacity expansion difficulty | 15 |
| Technical/certification barrier | 15 |
| Margin or pricing power potential | 10 |
| Market underappreciation potential | 10 |

## Evidence Requirements

For every score above 80, provide at least one strong evidence item or clearly state that the score is inference-based and requires verification.

Do not over-score a segment simply because the theme is popular.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "scored_segments": [
    {
      "segment_id": "",
      "segment_name": "",
      "chokepoint_score": 0,
      "score_breakdown": {
        "downstream_necessity": 0,
        "supplier_scarcity": 0,
        "customer_switching_cost": 0,
        "capacity_expansion_difficulty": 0,
        "technical_certification_barrier": 0,
        "margin_pricing_power_potential": 0,
        "market_underappreciation_potential": 0
      },
      "why_it_may_be_a_chokepoint": "",
      "why_it_may_not_be_a_chokepoint": "",
      "evidence": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ],
      "recommended_action": "continue | observe | reject"
    }
  ],
  "top_chokepoint_segments": [],
  "segments_rejected": [],
  "summary": ""
}
```

## Recommended Action Rules

- `continue`: chokepoint score >= 70 and sufficient evidence quality.
- `observe`: score 55–69 or evidence is interesting but incomplete.
- `reject`: score below 55 or segment is commoditized/weakly connected.

## Red Flags

Downgrade a segment if:

1. The segment has many interchangeable suppliers.
2. Capacity can be added quickly.
3. Customers buy mostly on price.
4. The segment has no clear margin expansion path.
5. The segment is already broadly recognized and richly valued.

## Next Step

Pass `continue` segments to `05_COMPANY_DISCOVERY.md`.
