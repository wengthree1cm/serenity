# 01 Workflow Router Skill

## Purpose

This skill controls the end-to-end research workflow. It determines which skill should run next, what inputs each skill needs, and when the workflow should stop or ask for more data.

## When to Use

Use this skill at the beginning of every run and between major workflow stages.

## Input

```json
{
  "user_theme": "",
  "market": "US stocks",
  "market_cap_min": 300000000,
  "market_cap_max": 20000000000,
  "exclude": ["OTC", "SPAC", "pre-revenue biotech"],
  "previous_outputs": {}
}
```

## Workflow Order

Run the workflow in this order:

1. `00_SYSTEM_PRINCIPLES.md`
2. `02_THEME_RESEARCH.md`
3. `03_VALUE_CHAIN_DECOMPOSITION.md`
4. `04_CHOKEPOINT_SCORING.md`
5. `05_COMPANY_DISCOVERY.md`
6. `06_COMMERCIAL_VALIDATION.md`
7. `07_FINANCIAL_VALUATION_CROWDING.md`
8. `08_BEAR_CASE.md`
9. `09_FINAL_RANKING.md`
10. `10_REPORT_WRITER.md`
11. `99_OUTPUT_FORMATS.md` for validation

## Execution Rules

### Rule 1: Do not skip the value-chain steps

The system must not move directly from theme to stock picks. It must first identify value-chain segments and chokepoints.

### Rule 2: Persist every step

Each step should be saved to disk.

Recommended file names:

```text
outputs/01_theme_research.json
outputs/02_value_chain.json
outputs/03_chokepoint_scores.json
outputs/04_company_candidates.json
outputs/05_commercial_validation.json
outputs/06_valuation_crowding.json
outputs/07_bear_case.json
outputs/08_final_ranking.json
outputs/final_report.md
```

### Rule 3: Use previous outputs as inputs

Each stage should receive:

- the global system principles;
- the current skill instruction;
- the original user theme;
- the previous step output;
- any relevant stored data.

### Rule 4: Validate JSON

Every output should be valid JSON unless the skill is explicitly a report writer.

If JSON fails validation, call the same skill again with a repair instruction:

```text
Your previous output was not valid JSON. Return only valid JSON matching the required schema. Do not add commentary.
```

### Rule 5: Stop early when appropriate

The system may stop early if:

- the theme is not structurally attractive;
- the value chain has no clear chokepoint;
- no companies meet minimum liquidity, relevance, and data availability standards;
- the only candidates are pure concept stocks;
- valuation/crowding shows that the theme is already fully repriced.

In that case, still produce a short report explaining why the workflow stopped.

## Stage Gate Rules

### After Theme Research

Continue only if:

- `theme_score >= 60`, or
- the user explicitly asks to continue despite a low score.

### After Chokepoint Scoring

Continue only with segments where:

- `chokepoint_score >= 70`, or
- the segment has an unusually strong underpricing signal.

### After Company Discovery

Continue only with companies where:

- `business_relevance_score >= 60`;
- ticker is valid;
- company is publicly traded;
- market cap and liquidity are within scope unless user overrides.

### After Commercial Validation

High-priority candidates should generally require:

- `commercial_validation_level >= 2`, and
- either at least one hard evidence item or several strong soft evidence items.

### After Valuation/Crowding

Companies with strong fundamentals but very stretched valuation should be moved to `Wait for Pullback` instead of `High Priority Research`.

## Required Output

```json
{
  "workflow_status": "running | stopped | completed | needs_more_data",
  "current_stage": "",
  "next_stage": "",
  "inputs_for_next_stage": {},
  "stage_gate_result": "pass | fail | conditional",
  "reason": "",
  "files_to_read": [],
  "files_to_write": [],
  "warnings": []
}
```

## Next Step

The next step is determined by the `next_stage` field.
