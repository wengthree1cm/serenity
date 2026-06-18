# Quality Gate Audit v2

Generated: 2026-06-12T22:47:24.248809+00:00

## Overall Gate

**closer_but_not_investment_grade**. Market Data Connector v2 fixes the prior market-cap, EV, multiples, and price-performance blocker. The biggest remaining blocker is commercial validation: backlog, named customer contracts, segment revenue, and customer concentration remain missing.

## Company Scores

| Ticker | Rating | Evidence | Completeness | Valuation Confidence | Commercial Confidence | Crowding Confidence | Keep? | Suggested Change | Reason |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| KTOS | Watchlist | 72 | 72 | 70 | 55 | 62 | true | Keep Watchlist | KTOS still deserves provisional Watchlist. V2 fixes valuation data and shows net cash and moderate momentum, but valuation is stretched and customer/backlog/segment revenue evidence is still missing. |
| IRDM | Watchlist | 70 | 74 | 68 | 50 | 52 | true | Upgrade from Observe audit view to Watchlist | IRDM can return to provisional Watchlist because v2 shows market cap, EV, P/E, EV/EBITDA, positive free cash flow, and gross margin. Chokepoint purity and high net debt still cap the rating. |
| RDW | Observe | 58 | 68 | 45 | 42 | 38 | true | Keep Observe | RDW should remain downgraded to Observe because v2 confirms demanding EV/Sales, negative free cash flow, negative EV/EBITDA, P/E not meaningful, and strong 6-month momentum without backlog/customer proof. |
| MRCY | Observe | 58 | 69 | 45 | 40 | 32 | true | Keep Observe | MRCY should remain downgraded to Observe. V2 shows positive free cash flow, but valuation and momentum are stretched and space/satellite revenue, backlog, and customer evidence are missing. |
| RKLB | Wait for Pullback | 68 | 70 | 18 | 56 | 15 | true | Keep Wait for Pullback | RKLB remains Wait for Pullback rather than Observe because direct business relevance is strong, but v2 shows extreme EV/Sales, P/S, negative free cash flow, negative EV/EBITDA, and very high 12-month price change. |
| VSAT | Observe | 55 | 72 | 60 | 38 | 12 | true | Keep Observe | VSAT has less extreme valuation multiples but high net debt, very high price momentum, and mixed chokepoint purity. Observe remains appropriate. |
| BKSY | Observe | 48 | 66 | 28 | 35 | 20 | true | Keep Observe | BKSY is too weakly validated and too expensive for Wait for Pullback. V2 shows demanding EV/Sales/P/S, negative free cash flow, negative EV/EBITDA, and high price momentum. |
| PL | Observe | 50 | 68 | 22 | 36 | 10 | true | Keep Observe | PL appears too hype-driven/expensive for a stronger rating. V2 shows positive free cash flow and net cash, but EV/Sales and P/S are very high and 12-month price change is extreme. |

## Direct Answers

- **KTOS**: Still deserves provisional Watchlist, not High Priority Research.
- **RDW_MRCY_IRDM**: IRDM can return to provisional Watchlist; RDW and MRCY should remain Observe.
- **RKLB**: Remains Wait for Pullback based on extreme valuation and price momentum, not downgraded to Observe because direct business relevance remains strong.
- **BKSY_PL**: Both are too expensive/momentum-driven and too weakly validated for Wait for Pullback; both should be Observe.
- **High Priority Research**: No company is close enough for High Priority Research until backlog/customer/segment-revenue evidence improves.

## Category Distribution

- watchlist: KTOS, IRDM
- wait_for_pullback: RKLB
- observe: RDW, MRCY, VSAT, BKSY, PL
- reject: none

## Biggest Remaining Data Gaps

- Backlog by relevant segment
- Named customer contracts and awards
- Segment revenue materiality
- Customer concentration
- Ownership, analyst coverage, and short interest
- Peer valuation context and historical valuation ranges

## Connector Status

Market Data Connector v2 is good enough to rerun Module 07 Valuation & Crowding. It is not enough to make the run investment-grade because the commercial evidence layer is still incomplete.
