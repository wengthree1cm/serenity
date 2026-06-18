# Serenity Scanner Report: Commercial Space and Defense Satellite Infrastructure Supply Chain

## Executive Summary

This Codex-agent run treats the space sector as a value chain, not a single basket of space stocks. The strongest chokepoint hypotheses are secure defense electronics and RF payloads, satellite ground infrastructure and mission software, spacecraft components and integration, and defense ISR/geospatial data infrastructure.

The top research candidates are KTOS, RDW, MRCY, IRDM, and RKLB. No company is classified as High Priority Research in this first run because market cap, enterprise value, valuation multiples, backlog, and named customer evidence are missing from the connector layer. This report is a research watchlist only and does not provide investment advice or trading instructions.

## Theme Assessment

The theme is structurally interesting because defense satellite infrastructure and commercial constellation growth can create bottlenecks in qualified hardware, RF systems, ground infrastructure, mission software, and spacecraft components. Evidence quality is mixed: company-level SEC/Yahoo profile data is hard evidence for financial and price fields, while many customer-demand and chokepoint claims remain inference until filings, earnings calls, backlog, and contract disclosures are reviewed.

Major limitation: Yahoo chart data did not provide market cap for any ticker, so market-cap and valuation claims are marked missing rather than inferred.

## Value Chain Map

| Segment | Role | Chokepoint View |
|---|---|---|
| Secure defense electronics and RF payloads | Mission-critical electronics and RF subsystems | High |
| Satellite ground infrastructure and mission software | Ground stations, command/control, signal processing | High |
| Spacecraft components, power, thermal, and integration | Flight hardware and integrated subsystems | High |
| Defense ISR and geospatial data infrastructure | Imagery, analytics, and tasking workflows | Medium-high |
| Launch cadence and integrated space systems | Launch and mission deployment | Medium |
| Satellite network operators and connectivity capacity | Operational satellite communications capacity | Medium |

## Chokepoint Analysis

The highest-ranked segments are qualification-heavy and hard to substitute quickly. Secure electronics, RF payloads, and ground systems are more attractive than generic thematic exposure because defense and mission-critical customers usually require reliability, security, and integration. This is an inference in this run and must be verified with customer, contract, and backlog evidence.

## Candidate Company Table

| Rank | Ticker | Company | Segment | Validation Level | Valuation Status | Crowding | Classification |
|---:|---|---|---|---:|---|---|---|
| 1 | KTOS | Kratos Defense & Security Solutions, Inc. | Satellite ground infrastructure and mission software | 3 | unknown | medium | Watchlist |
| 2 | RDW | Redwire Corp | Spacecraft components, power, thermal, and integration | 2 | unknown | medium | Watchlist |
| 3 | MRCY | MERCURY SYSTEMS, INC. | Secure defense electronics and RF payloads | 2 | unknown | high | Watchlist |
| 4 | IRDM | Iridium Communications Inc. | Satellite network operators and connectivity capacity | 3 | unknown | medium | Watchlist |
| 5 | RKLB | Rocket Lab Corp | Spacecraft components, power, thermal, and integration | 3 | unknown | high | Wait for Pullback |
| 6 | BKSY | BlackSky Technology Inc. | Defense ISR and geospatial data infrastructure | 2 | unknown | high | Wait for Pullback |
| 7 | PL | Planet Labs PBC | Defense ISR and geospatial data infrastructure | 2 | unknown | high | Wait for Pullback |
| 8 | VSAT | VIASAT INC | Satellite ground infrastructure and mission software | 3 | unknown | high | Observe |


## High Priority Research Candidates

None in this first Codex-agent run. The main reason is data integrity: market cap, EV, valuation multiples, backlog, segment revenue, and customer-contract evidence are missing. Assigning High Priority Research without those fields would overstate the evidence.

## Watchlist / Wait for Pullback

### Watchlist

- KTOS: strongest first-pass rank due to satellite ground and defense systems relevance plus grounded SEC financial fields. Still needs segment revenue, backlog, and contract verification.
- RDW: direct spacecraft infrastructure exposure, but profitability and cash-flow metrics are weak in the profile.
- MRCY: secure defense electronics maps well to a chokepoint, but earnings metrics and repricing risk keep it below high priority.
- IRDM: operational satellite communications profile with positive income and operating cash flow, but it may be less of an underappreciated supply-chain chokepoint.

### Wait for Pullback

- RKLB: direct launch and space-systems exposure, but the Yahoo snapshot shows price_change_12m=3.029516, so repricing risk is high and valuation fields are missing.
- BKSY: relevant geospatial/ISR exposure, but revenue scale, profitability, and price repricing require caution.
- PL: relevant Earth observation exposure, but the Yahoo snapshot shows price_change_12m=4.800745 and SEC-derived net income is negative.

### Observe

- VSAT: relevant satellite communications infrastructure, but the profile shows high liabilities relative to cash and strong 12-month repricing. Market cap and EV are missing.

## Rejects / Avoid List

No final-ranked company was classified Reject. LUNR, ASTS, GSAT, SPIR, and SATS were excluded from the capped top-8 candidate pool in this run, mainly because this pass prioritized direct supply-chain chokepoints and penalized concept-stage exposure, narrower network-operator exposure, or heavily repriced connectivity names.

## Evidence Quality

Hard evidence used in this run comes from `company_profiles.json`: SEC-derived revenue, net income/loss, operating income/loss, assets, liabilities, stockholders' equity, cash and equivalents, operating cash flow, and Yahoo-derived current price and price-change fields.

Soft evidence comes from the seed universe segment hints and company inclusion rationale.

Inference is used for value-chain chokepoint logic, segment attractiveness, and the mapping from broad space infrastructure demand to possible company benefit.

Missing evidence includes market cap for all tickers, enterprise value, valuation multiples, gross margin, free cash flow, net debt, backlog, named customer contracts, segment revenue, analyst coverage, institutional ownership, and short interest.

## Next Research Checklist

1. Add a market-data connector that returns market cap, EV, shares, and valuation multiples.
2. Read each candidate's latest 10-K and 10-Q.
3. Read the last two earnings calls for KTOS, RDW, MRCY, IRDM, and RKLB.
4. Verify backlog, bookings, customer concentration, and segment revenue for each candidate.
5. Separate defense satellite revenue from broader defense, communications, or aerospace exposure.
6. Compare peer valuation after market cap and EV data are available.
7. Monitor whether high price-change names have business evidence catching up to the stock move.

## Important Note

This report is for research purposes only. It is not investment advice or a trading instruction.
