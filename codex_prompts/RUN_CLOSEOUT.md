# Run Sector Closeout

Use this prompt to close out a completed Serenity sector analysis in Codex-agent mode.

## Parameters

Fill in or infer from the user request:

```json
{
  "sector_output_folder": "",
  "theme": "",
  "include_company_deep_dives": true
}
```

## Execution Mode

Use Codex-agent reasoning and existing local outputs.

Do not:

- Rerun the full sector workflow.
- Call the OpenAI API runner.
- Ask for `OPENAI_API_KEY`.
- Modify the `gpt/` markdown investment logic.
- Build the web app.
- Add trading, brokerage, portfolio, auto-buy, or order execution features.
- Output `Buy`, `Sell`, or `Hold`.
- Add new investment conclusions that are not supported by existing evidence.

## Required Inputs

Use the existing sector output folder.

Read available files:

```text
[sector_output_folder]/final_report.md
[sector_output_folder]/08_final_ranking*.json
[sector_output_folder]/quality_gate_audit*.json
[sector_output_folder]/data/company_profiles*.json
[sector_output_folder]/data/data_quality_report*.json
[sector_output_folder]/data/commercial_validation_*.json
[sector_output_folder]/*_deep_dive*.json
[sector_output_folder]/*_comparison*.json
```

Use cached sources only to verify evidence already cited. Do not expand the analysis into a new workflow unless the user explicitly asks.

## Required Closeout Sections

Create:

```text
[sector_output_folder]/sector_closeout.md
[sector_output_folder]/sector_closeout.json
```

If versioning is needed because files already exist, append a version suffix:

```text
[sector_output_folder]/sector_closeout_v2.md
[sector_output_folder]/sector_closeout_v2.json
```

The closeout should include:

1. Final sector conclusion
2. Final company classifications
3. Trigger list
4. Missing evidence
5. Reusable lessons learned
6. High-priority gate checklist updates
7. Data connector improvement needs
8. Evidence quality assessment
9. What should be researched manually next

## Final Categories

Use only:

- `High Priority Research`
- `Watchlist`
- `Wait for Pullback`
- `Observe`
- `Reject`

Do not output `Buy`, `Sell`, or `Hold`.

## Evidence Rules

Classify evidence as:

- `hard_evidence`
- `soft_evidence`
- `inference`
- `missing_evidence`

Separate:

- current commercial validation
- future optionality
- valuation/crowding evidence
- missing evidence

Do not treat future optionality as current revenue, backlog, contracts, or segment economics.

## Trigger List

Create a trigger list grouped by:

- upgrade triggers
- downgrade triggers
- data refresh triggers
- commercial validation triggers
- valuation/crowding triggers
- future optionality triggers

Each trigger should include:

```json
{
  "ticker": "",
  "trigger": "",
  "why_it_matters": "",
  "evidence_needed": "",
  "expected_classification_impact": ""
}
```

## High-Priority Gate Checklist Updates

List reusable checklist items that should be applied before any company can move to `High Priority Research`.

Include checks for:

- market cap and enterprise value
- valuation multiples
- revenue and free cash flow
- cash, debt, and net debt
- backlog
- signed contracts or customer commitments
- segment revenue and segment margin
- customer concentration
- ownership and short interest
- commercial validation from primary sources
- whether future optionality is `F3` or `F4`, not merely `F0` to `F2`

## Required JSON Shape

```json
{
  "theme": "",
  "sector_output_folder": "",
  "final_sector_conclusion": "",
  "final_company_classifications": [],
  "category_distribution": {},
  "trigger_list": {
    "upgrade_triggers": [],
    "downgrade_triggers": [],
    "data_refresh_triggers": [],
    "commercial_validation_triggers": [],
    "valuation_crowding_triggers": [],
    "future_optionality_triggers": []
  },
  "missing_evidence": [],
  "reusable_lessons_learned": [],
  "high_priority_gate_checklist_updates": [],
  "connector_improvement_needs": [],
  "manual_research_priorities": [],
  "quality_gate_status": ""
}
```

## Final Response

After completion, summarize:

- output files created
- final sector conclusion
- final category distribution
- companies still closest to `High Priority Research`
- largest missing evidence blockers
- most important manual research priority
- reusable lessons learned
