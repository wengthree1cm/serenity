# 06 Commercial Validation Skill

## Purpose

Evaluate whether each company has real commercial validation for the theme.

The goal is not to require that the company has already fully monetized the trend. The goal is to determine whether there is enough evidence that future revenue growth is more than speculation.

## Core Question

Is the company already showing evidence that it can benefit from the theme, or is the investment case only based on prediction?

## When to Use

Run after `05_COMPANY_DISCOVERY.md` creates a list of candidate companies.

## Input

```json
{
  "theme": "",
  "candidate_companies": [],
  "chokepoint_segments": []
}
```

## Validation Levels

### Level 0: No Evidence

The company is only thematically related. There is no customer evidence, order evidence, backlog evidence, revenue evidence, or management commentary.

Default rating: `Reject` or low-priority `Observe`.

### Level 1: Soft Evidence Only

The company has some soft indicators, such as:

- management commentary about demand;
- general industry tailwinds;
- product relevance;
- capacity preparation;
- early customer discussions without disclosed names or measurable impact.

Default rating: `Observe`.

### Level 2: Strong Soft Evidence + Early Company-Level Validation

The company has stronger indicators, such as:

- design win;
- customer qualification;
- pilot project;
- supplier approval;
- small initial orders;
- specific product demand mentioned in earnings calls;
- capacity expansion tied to customer demand;
- customer capex strongly aligned with the company's offering.

Default rating: `Watchlist` candidate.

### Level 3: Hard Evidence Emerging

The company has clear hard evidence, such as:

- backlog growth;
- disclosed orders;
- revenue acceleration in the relevant segment;
- gross margin improvement;
- guidance raise;
- long-term supply agreement;
- customer contract;
- 8-K or press release confirming material demand.

Default rating: `High Priority Research`, if valuation is not stretched.

### Level 4: Fully Repriced

The commercial evidence is already obvious to the market. Revenue has accelerated, analysts have revised estimates upward, and the stock has already been significantly repriced.

Default rating: `Wait for Pullback` or `Good company, valuation discipline required`.

## Commercial Validation Score

Assign a score from 0 to 100.

| Factor | Weight |
|---|---:|
| Disclosed orders or backlog growth | 25 |
| Customer qualification, certification, or design win | 20 |
| Management commentary with specific demand evidence | 15 |
| Revenue already tied to the theme | 15 |
| Capacity expansion tied to demand | 10 |
| Customer capex or industry demand support | 10 |
| Third-party validation | 5 |

## Evidence Rules

Separate evidence into:

- `hard_evidence`
- `soft_evidence`
- `inferences`
- `missing_evidence`

A company with only vague management language should not be scored above Level 1.

A company with no direct company-level evidence should not enter `High Priority Research`.

The most attractive stage is usually Level 2 moving toward Level 3: enough evidence to reduce speculation, but not so much that the market has fully repriced the company.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "validated_companies": [
    {
      "ticker": "",
      "company_name": "",
      "segment_name": "",
      "commercial_validation_level": 0,
      "commercial_validation_score": 0,
      "validation_stage_label": "No Evidence | Soft Evidence Only | Early Validation | Hard Evidence Emerging | Fully Repriced",
      "hard_evidence": [
        {
          "evidence": "",
          "source": "",
          "why_it_matters": ""
        }
      ],
      "soft_evidence": [
        {
          "evidence": "",
          "source": "",
          "why_it_matters": ""
        }
      ],
      "inferences": [
        {
          "inference": "",
          "supporting_evidence": [],
          "confidence": "low | medium | high"
        }
      ],
      "missing_evidence": [],
      "validation_summary": "",
      "rating_before_valuation": "Reject | Observe | Watchlist | High Priority | Wait for Pullback",
      "continue_to_valuation": true
    }
  ],
  "summary": ""
}
```

## Reject or Downgrade Rules

Reject or downgrade the company if:

1. The company is only loosely related to the theme.
2. There is no evidence beyond narrative.
3. Management uses vague language without financial or customer support.
4. The stock has already risen significantly without matching business evidence.
5. The company depends on future orders that are not supported by any customer, capacity, product, or industry evidence.
6. The relevant product is not material enough to move company-level revenue or valuation.

## Next Step

Pass companies with Level 2 or Level 3 validation to `07_FINANCIAL_VALUATION_CROWDING.md`.

Pass Level 4 companies too, but mark them as possible `Wait for Pullback` candidates.

Do not pass Level 0 companies unless the user explicitly wants speculative observations.
