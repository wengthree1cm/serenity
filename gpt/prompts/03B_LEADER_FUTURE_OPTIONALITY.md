# 03B Leader Future Optionality Skill

## Purpose

Analyze future optionality from industry leaders. Identify potential future business lines that major anchor companies may pursue, decompose the new value chains those future businesses would create, and determine whether upstream or adjacent public companies could benefit if the scenario becomes real.

Future optionality must never be treated as current commercial validation. This skill separates current proven business from future scenario analysis.

## When to Use

Run after `03A_LEADER_BUSINESS_ANATOMY.md` and before `04_CHOKEPOINT_SCORING.md`.

## Input

```json
{
  "theme": "",
  "market": "US stocks",
  "value_chain_decomposition_output": {},
  "leader_business_anatomy_output": {},
  "anchor_companies": []
}
```

## Process

For each anchor company or industry leader:

1. Identify future business lines or strategic options that could matter to the theme.
2. Separate the company's current proven business from speculative future scenarios.
3. Assign a future business evidence level from `F0` to `F4`.
4. Identify required enablers for the scenario to become real.
5. Decompose the future value chain that would emerge if the scenario happens.
6. Identify upstream, supplier, infrastructure, software, component, manufacturing, regulatory, or services segments that could become chokepoints.
7. Determine whether each scenario is strong enough to enter main chokepoint scoring or should remain in a scenario watchlist.

## Future Business Evidence Levels

Use exactly one level for each future business line:

- `F0`: Rumor only. No reliable public source. Do not use in scoring except as a watch item.
- `F1`: Management or media discussion. Mentioned publicly but no product, capex, customer, contract, or revenue evidence. Treat as speculative optionality.
- `F2`: Technical roadmap or early preparation. Evidence of R&D, hiring, prototype, facility preparation, regulatory preparation, or early technical architecture. Can create a scenario watchlist, but cannot support High Priority Research.
- `F3`: Capital allocation or commercial preparation. Evidence of capex, supplier preparation, pilot customer, signed partnership, major procurement, or regulatory milestone. Can be passed into chokepoint scoring as an emerging scenario.
- `F4`: Commercial validation. Revenue, backlog, contract, customer commitment, guidance, or disclosed segment economics. Can be treated as part of the main thesis.

## Evidence Rules

Every claim must be classified as one of:

- `hard`: directly supported by filings, contracts, customer disclosures, regulatory filings, capex disclosures, procurement records, revenue, backlog, guidance, or other primary-source evidence.
- `soft`: supported by credible but indirect public evidence such as management commentary, investor presentations, media interviews, industry reports, technical roadmaps, hiring patterns, or product announcements.
- `inference`: logically inferred from the scenario architecture or leader strategy, but not directly verified.

If sources are missing or unreliable, mark the future business evidence level as `F0` or `F1`. Do not infer named supplier relationships without evidence.

## Key Questions

- What future business line could the leader plausibly pursue?
- Is the scenario backed by commercial evidence or only strategic discussion?
- Which new value-chain segments must exist if the future business scales?
- Which enablers are technically difficult, capacity constrained, regulated, or supplier dependent?
- Which public companies could benefit upstream or adjacent to the leader if the scenario becomes real?
- Which claims are current commercial facts and which are only optionality?
- Should the scenario affect main chokepoint scoring now, or stay in a scenario watchlist?

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "leader_future_optionality": [
    {
      "anchor_company": "",
      "ticker": "",
      "future_business_line": "",
      "evidence_level": "F0 | F1 | F2 | F3 | F4",
      "current_status": "",
      "why_it_could_matter": "",
      "required_enablers": [],
      "future_value_chain": [
        {
          "segment": "",
          "role": "",
          "why_it_becomes_important_if_scenario_happens": "",
          "supply_constraints": [],
          "possible_public_company_candidates": [],
          "evidence_strength": "high | medium | low",
          "current_commercial_validation": "none | weak | medium | strong",
          "evidence": [
            {
              "evidence_type": "hard | soft | inference",
              "summary": "",
              "source": ""
            }
          ],
          "missing_evidence": []
        }
      ],
      "scenario_probability": "low | medium | high",
      "time_horizon": "0-2 years | 2-5 years | 5+ years",
      "should_pass_to_chokepoint_scoring": true,
      "reason": ""
    }
  ],
  "scenario_chokepoint_candidates": [
    {
      "segment": "",
      "linked_future_business_lines": [],
      "evidence_level": "F0 | F1 | F2 | F3 | F4",
      "why_it_could_be_a_chokepoint": "",
      "public_company_candidates": [],
      "main_scoring_path": "pass_to_04 | scenario_watchlist_only | reject",
      "evidence": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ],
      "missing_evidence": []
    }
  ],
  "do_not_overweight_warnings": []
}
```

## Rules

1. Do not treat speculative future business as current revenue or backlog.
2. Do not upgrade a company to High Priority Research based only on `F0`, `F1`, or `F2` evidence.
3. Only `F3` or `F4` evidence can materially increase a company's chokepoint score.
4. If a future business is technically exciting but commercially unproven, classify it as optionality, not thesis.
5. Every claim must be marked as `hard`, `soft`, or `inference`.
6. If sources are missing or unreliable, mark the evidence level as `F0` or `F1`.
7. Pass only `F3` or `F4` scenario chokepoints into the main scoring path.
8. Put `F1` and `F2` scenarios into a separate scenario watchlist.
9. Do not infer a supplier, customer, backlog, contract, or revenue relationship unless evidence exists.
10. Do not double count a scenario as both current commercial validation and future optionality.

## Scenario Routing Rules

Use `main_scoring_path` as follows:

- `pass_to_04`: only for `F3` or `F4` scenarios with enough evidence to affect chokepoint scoring.
- `scenario_watchlist_only`: for `F1` or `F2` scenarios, and for `F3` scenarios with weak evidence or unclear supply-chain implications.
- `reject`: for `F0` scenarios, generic future ideas, or scenarios with no credible path to public-company beneficiaries.

Set `should_pass_to_chokepoint_scoring` to `true` only when:

1. The scenario evidence level is `F3` or `F4`.
2. The future value chain contains at least one plausible constrained segment.
3. The segment has identifiable evidence needs and a realistic public-company research path.

## Do-Not-Overweight Warnings

Add warnings when:

1. A scenario is based mainly on media speculation.
2. A leader's future business would mostly benefit the leader itself rather than suppliers.
3. The public-company candidate connection is only thematic.
4. The scenario is technically plausible but lacks customer, capex, procurement, regulatory, or revenue evidence.
5. The same optionality is already priced into highly crowded companies.

## Next Step

Pass only `scenario_chokepoint_candidates` marked `pass_to_04` into `04_CHOKEPOINT_SCORING.md`.

Keep `scenario_watchlist_only` candidates separate from the main scoring path so speculative optionality does not contaminate current commercial validation.
