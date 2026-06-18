# Quality Gate Audit: Codex-Agent Serenity Space Run
Audit generated: 2026-06-12T22:32:55.720226+00:00
Audited folder: `outputs/codex_agent_space_20260612_1523`
## Overall Gate
**Result:** `not_investment_grade`

The run is useful as a first research map, but not investment-grade because valuation and commercial validation are materially incomplete.
## Evidence Map
**Supported by live data:** current price, 1m/3m/6m/12m price changes, revenue, net income/loss, operating income/loss, assets, liabilities, stockholders equity, cash and equivalents, operating cash flow.

**Inference only:** chokepoint ranking, company exposure materiality, supplier scarcity, customer switching cost, commercial validation level, catalyst quality, crowding beyond price changes.

**Requires missing data:** market_cap, enterprise_value, valuation multiples, backlog, named customer contracts, segment revenue, customer concentration, gross margin, free cash flow, net debt, analyst coverage, institutional ownership, short interest.
## Company Rating Audit
| Ticker | Current Rating | Evidence | Completeness | Valuation Confidence | Commercial Confidence | Keep? | Suggested Change | Reason |
|---|---|---:|---:|---:|---:|---|---|---|
| KTOS | Watchlist | 58 | 45 | 20 | 45 | true | Keep Watchlist, but mark as provisional / evidence-gated | KTOS has live-data support for current price, price changes, revenue, cash, assets, liabilities, and income fields. The Watchlist label is acceptable only as a research queue item because segment revenue, backlog, contracts, customer concentration, market cap, EV, and multiples are missing. |
| RDW | Watchlist | 50 | 42 | 18 | 38 | false | Downgrade from Watchlist to Observe | RDW has direct thematic exposure and live financial fields, but the run lacks backlog, customer contracts, segment revenue validation, market cap, EV, and valuation multiples. Negative net income, operating income, and operating cash flow in company_profiles.json make Watchlist too generous without stronger commercial evidence. |
| MRCY | Watchlist | 48 | 42 | 18 | 35 | false | Downgrade from Watchlist to Observe | The secure defense electronics chokepoint is plausible, but company-specific space/satellite revenue, backlog, and customer evidence are missing. The live profile shows negative net income and operating income, and price-change data indicates repricing risk, so Watchlist is not sufficiently supported. |
| IRDM | Watchlist | 55 | 44 | 20 | 40 | false | Downgrade from Watchlist to Observe | IRDM has live support for revenue, profitability, operating cash flow, current price, and price changes. The problem is thesis fit: satellite network operation is less clearly a hidden supply-chain chokepoint, and the run lacks defense-satellite backlog, segment-specific contracts, market cap, EV, and multiples. |
| RKLB | Wait for Pullback | 57 | 44 | 15 | 42 | false | Downgrade from Wait for Pullback to Observe | Wait for Pullback implies quality and valuation context are established. The live profile supports revenue, cash, liabilities, current price, and a very large 12-month price change, but market cap, EV, multiples, backlog, contracts, and segment revenue are missing. Without valuation data, pullback language is not investment-grade. |
| BKSY | Wait for Pullback | 43 | 40 | 15 | 32 | false | Downgrade from Wait for Pullback to Observe | BKSY has thematic geospatial/ISR relevance and live basic financial/price fields, but revenue scale is small, net income and operating income are negative, and the run lacks backlog, customer contracts, market cap, EV, and valuation multiples. Wait for Pullback is too generous. |
| PL | Wait for Pullback | 45 | 41 | 15 | 34 | false | Downgrade from Wait for Pullback to Observe | PL has live support for revenue, cash, liabilities, operating cash flow, and large price appreciation. The run lacks market cap, EV, valuation multiples, backlog, customer contracts, and segment revenue proof; net income is negative. Wait for Pullback overstates the evidence. |
| VSAT | Observe | 48 | 43 | 16 | 34 | true | Keep Observe | Observe is appropriately cautious. VSAT has live financial and price fields, but the run lacks market cap, EV, multiples, segment-specific space/defense evidence, backlog, contracts, and customer concentration. Large liabilities relative to cash and high price-change data argue against a stronger rating. |

## Ratings Too Generous
- RDW Watchlist
- MRCY Watchlist
- IRDM Watchlist
- RKLB Wait for Pullback
- BKSY Wait for Pullback
- PL Wait for Pullback

## Files Needing Improvement
- `data/company_profiles.json`: Add market cap, EV, shares outstanding, debt breakdown, gross margin, free cash flow, and net debt.
- `data/data_quality_report.json`: Track missing fields by severity and distinguish valuation-critical fields from optional fields.
- `05_commercial_validation.json`: Replace seed-universe inference with primary-source backlog, contract, customer, and segment revenue evidence.
- `06_valuation_crowding.json`: Do not assign high valuation scores when valuation_status is unknown; add market cap, EV, multiples, peer comparisons, ownership, and short interest.
- `08_final_ranking.json`: Lower ratings where commercial and valuation evidence is missing; separate provisional research queue from validated Watchlist.
- `final_report.md`: Add a visible quality-gate section stating the run is not investment-grade and explaining downgraded ratings.

## Connector Improvements Needed
- Market data connector for market cap, shares outstanding, EV, and valuation multiples.
- SEC filing parser for 10-K/10-Q segment revenue, backlog, customer concentration, debt, and liquidity notes.
- Press release and 8-K connector for named contracts, awards, and customer disclosures.
- Earnings transcript connector for management commentary and guidance changes.
- Ownership/short-interest connector for crowding checks.
- News/source citation connector with date, URL, and evidence type.

## Bottom Line
The run is useful as a first screening and workflow demonstration. It should not be treated as investment-grade research until valuation data, market cap, EV, multiples, backlog, customer contracts, and segment-level revenue evidence are added and the provisional ratings are downgraded or revalidated.
