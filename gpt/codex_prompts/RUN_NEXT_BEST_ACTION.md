# Run Next Best Action

Use this prompt to decide the next best action after a completed Serenity sector analysis.

## Parameters

Fill in from the user request:

```json
{
  "existing_run_folder": ""
}
```

## Execution Mode

Use Codex-agent reasoning and existing local outputs.

Do not:

- Rerun the sector workflow.
- Run a company deep dive.
- Run a two-company comparison.
- Run sector closeout.
- Call the OpenAI API runner.
- Ask for `OPENAI_API_KEY`.
- Modify the `gpt/` markdown investment logic.
- Build the web app.
- Add trading, brokerage, portfolio, auto-buy, or order execution features.
- Output `Buy`, `Sell`, or `Hold`.

This prompt only decides what should happen next and writes a short next-action recommendation.

## Required Inputs

Inspect these files in `existing_run_folder`:

```text
final_report.md
08_final_ranking.json
quality_gate_audit.json
data/company_profiles.json
data/commercial_validation*.json
```

If a file is missing, continue with available files and record the missing file in the output.

## Allowed Recommendations

Recommend exactly one of:

1. `Run company deep dive`
2. `Run two-company comparison`
3. `Run sector closeout`
4. `Improve data connectors before deeper research`
5. `Stop because evidence quality is too weak`

## Decision Rules

Use these rules in order:

1. If market data or commercial validation is too incomplete for most candidates, recommend `Improve data connectors before deeper research`.
2. If all candidates are `Observe` or `Reject`, do not recommend a deep dive. Recommend `Stop because evidence quality is too weak` unless sector closeout is clearly useful.
3. If there is one clear `Watchlist` candidate with materially stronger evidence than the rest, recommend `Run company deep dive`.
4. If there are two close `Watchlist` candidates, recommend individual deep dives first unless both already have deep dives. If both already have deep dives, recommend `Run two-company comparison`.
5. If the sector analysis already has enough company-level work and the main remaining task is synthesis, recommend `Run sector closeout`.
6. If a candidate is classified `Wait for Pullback`, do not automatically prioritize it over a `Watchlist` candidate unless the evidence quality is clearly stronger and the next question is valuation/crowding.
7. Never recommend deeper research solely because a company has strong price momentum.
8. Do not use future optionality as current commercial validation.

## Ranking Signals

When selecting a target ticker, consider:

- final classification
- final score
- evidence strength
- data completeness
- commercial validation confidence
- valuation confidence
- missing evidence severity
- whether the next research question is answerable with local filings or connector improvements

Prefer a `Watchlist` candidate with:

- populated market data
- at least moderate commercial validation
- a clear chokepoint segment
- valuation not already too stretched
- specific missing evidence that can be resolved through a deep dive

## Output Files

Create these files inside `existing_run_folder`:

```text
next_best_action.md
next_best_action.json
```

If those files already exist, create versioned files:

```text
next_best_action_v2.md
next_best_action_v2.json
```

## Required JSON Shape

```json
{
  "existing_run_folder": "",
  "recommended_action": "Run company deep dive | Run two-company comparison | Run sector closeout | Improve data connectors before deeper research | Stop because evidence quality is too weak",
  "target_ticker": null,
  "second_ticker": null,
  "reason": "",
  "required_prompt_file": "",
  "exact_short_command": "",
  "inputs_inspected": [],
  "missing_inputs": [],
  "decision_factors": {
    "category_distribution": {},
    "watchlist_candidates": [],
    "wait_for_pullback_candidates": [],
    "observe_or_reject_candidates": [],
    "market_data_completeness": "",
    "commercial_validation_completeness": "",
    "quality_gate_status": "",
    "top_missing_evidence": []
  },
  "alternatives_considered": []
}
```

## Command Formats

For company deep dive:

```text
Run codex_prompts/RUN_COMPANY_DEEP_DIVE.md

existing_run_folder = outputs/...
ticker = MYRG
```

For two-company comparison:

```text
Run a two-company comparison using existing run folder outputs/...

first_ticker = MYRG
second_ticker = POWL
```

For sector closeout:

```text
Run codex_prompts/RUN_CLOSEOUT.md

sector_output_folder = outputs/...
```

For connector improvement:

```text
Improve the Serenity data connectors before deeper research.

existing_run_folder = outputs/...
missing_fields = [field list]
```

For stop:

```text
Stop deeper Serenity research for this run because evidence quality is too weak.

existing_run_folder = outputs/...
```

## Markdown Output

The markdown file should include:

1. Recommended next action
2. Target ticker, if applicable
3. Second ticker, if applicable
4. Reason
5. Evidence quality summary
6. Missing evidence or connector gaps
7. Exact short command to copy into Codex
8. Alternatives considered

## Final Response

After creating the files, summarize:

- output files created
- recommended action
- target ticker, if applicable
- exact short command
