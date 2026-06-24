# 07 Financial Valuation and Crowding Skill

## Purpose

Determine whether a commercially validated company is still underappreciated, fairly priced, or already over-owned/repriced.

This skill separates three concepts:

1. Good company.
2. Good stock.
3. Good entry point for further research.

## When to Use

Run after `06_COMMERCIAL_VALIDATION.md`.

## Input

```json
{
  "theme": "",
  "validated_companies": []
}
```

## Process

For each company, evaluate:

1. Basic financial health.
2. Revenue growth and margin trend.
3. Valuation versus history and peers.
4. Stock price performance.
5. Whether the market has already repriced the thesis.
6. Whether institutional, analyst, media, and social attention is already high.
7. Whether the company has enough balance sheet strength to execute.
8. Whether dilution or debt could impair the thesis.

## Required Metrics

Use available public data. If unavailable, use `unknown`.

Recommended metrics:

- market cap;
- enterprise value;
- revenue growth;
- gross margin;
- operating margin;
- free cash flow;
- net debt;
- cash runway if relevant;
- EV/Sales;
- EV/EBITDA;
- P/E if profitable;
- price change 1 month;
- price change 3 months;
- price change 6 months;
- price change 12 months;
- distance from 52-week high;
- distance from 52-week low;
- analyst coverage count;
- institutional ownership;
- short interest if available;
- abnormal volume;
- recent news intensity.

## Valuation Status

Use one of:

- `undemanding`
- `reasonable`
- `stretched`
- `very_stretched`
- `unknown`

Valuation must be judged relative to:

- growth rate;
- margin profile;
- balance sheet;
- peer group;
- historical range;
- commercial validation stage.

## Crowding Status

Use one of:

- `low`
- `medium`
- `high`
- `unknown`

Crowding is likely high if:

- the stock has already risen dramatically;
- analyst coverage has increased sharply;
- the theme is widely discussed;
- valuation has expanded without matching earnings evidence;
- news/social attention is high;
- the company is repeatedly cited as a top beneficiary of the theme.

## Heuristic Downgrades

Downgrade or move to `Wait for Pullback` if:

- 6-month price change is greater than 100% without matching hard evidence.
- EV/Sales or EV/EBITDA is far above peer/history without a clear margin/growth explanation.
- Commercial validation is Level 1 or 2 but the stock already trades like Level 4.
- The company needs major financing to execute.
- Dilution risk is high.
- Debt maturity risk is high.

Do not automatically reject a strong company only because it has appreciated. Instead, classify it correctly as `Wait for Pullback` when the thesis is good but the entry risk is high.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "valuation_results": [
    {
      "ticker": "",
      "company_name": "",
      "market_cap": "unknown",
      "enterprise_value": "unknown",
      "revenue_growth": "unknown",
      "gross_margin": "unknown",
      "operating_margin": "unknown",
      "free_cash_flow": "unknown",
      "net_debt": "unknown",
      "ev_sales": "unknown",
      "ev_ebitda": "unknown",
      "pe_ratio": "unknown",
      "price_change_1m": "unknown",
      "price_change_3m": "unknown",
      "price_change_6m": "unknown",
      "price_change_12m": "unknown",
      "distance_from_52w_high": "unknown",
      "distance_from_52w_low": "unknown",
      "analyst_coverage": "unknown",
      "institutional_ownership": "unknown",
      "short_interest": "unknown",
      "valuation_status": "undemanding | reasonable | stretched | very_stretched | unknown",
      "crowding_status": "low | medium | high | unknown",
      "balance_sheet_risk": "low | medium | high | unknown",
      "repricing_status": "not_repriced | partially_repriced | mostly_repriced | unknown",
      "valuation_score": 0,
      "crowding_score": 0,
      "summary": "",
      "rating_after_valuation": "High Priority Research | Watchlist | Wait for Pullback | Observe | Reject",
      "evidence": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ]
    }
  ],
  "summary": ""
}
```

## Scoring Rules

### Valuation Score

Score from 0 to 100.

- 80–100: valuation appears undemanding relative to growth and validation.
- 60–79: valuation is reasonable.
- 40–59: valuation is stretched.
- 0–39: valuation is very stretched or unsupported.

### Crowding Score

Score from 0 to 100, where higher means less crowded.

- 80–100: low attention, limited repricing.
- 60–79: some attention, not fully repriced.
- 40–59: moderately crowded.
- 0–39: highly crowded or already repriced.

## Next Step

Pass all companies except clear rejects to `08_BEAR_CASE.md`.
