# Next Best Action

Existing run folder: `outputs/codex_agent_ai_power_20260613_1843`

## Recommendation

Run company deep dive

Target ticker: `MYRG`

Second ticker: none

## Reason

Recommend a company deep dive on MYRG. The run has several Watchlist names, but MYRG is the clear first-ranked Watchlist candidate: it ranked #1 overall with a 78 final score, has populated market data, positive free cash flow in company_profiles.json, and sits in the electrical contracting/substation/grid-interconnection segment. The quality gate is evidence-gated rather than connector-blocked, so the next useful action is to resolve MYRG-specific missing evidence such as data-center backlog, customer/contracts, segment exposure, margins, and customer concentration.

## Evidence Quality Summary

Quality gate status: `evidence_gated_not_investment_grade`. Market data is sufficiently complete; commercial validation remains evidence-gated and needs company-specific manual review.

## Missing Evidence / Connector Gaps

- data-center-specific backlog
- named customer/contracts
- segment revenue by data center/power infrastructure exposure
- segment margins
- customer concentration
- ownership and short interest
- lead times/order visibility
- peer/historical valuation context

## Exact Short Command

```text
Run codex_prompts/RUN_COMPANY_DEEP_DIVE.md

existing_run_folder = outputs/codex_agent_ai_power_20260613_1843
ticker = MYRG
```

## Alternatives Considered

- Run two-company comparison: defer. Comparison is premature because MYRG does not yet have a single-company deep dive, and the closest alternatives are either Wait for Pullback names with valuation/crowding issues or lower-ranked Watchlist names.
- Run sector closeout: defer. The run is not ready for closeout because the recommended manual research priority from final_report.md has not been executed.
- Improve data connectors before deeper research: defer. Market data is populated for nearly all required fields. Commercial validation gaps are better addressed first through a MYRG filing/customer deep dive rather than connector work.
- Stop because evidence quality is too weak: reject. The run has multiple Watchlist candidates and populated market data, so evidence quality is not too weak to continue.
