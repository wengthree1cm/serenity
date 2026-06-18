# Codex Prompt Templates

This folder contains reusable prompt templates for running Serenity analyses in Codex-agent mode.

Use these prompts when you want Codex to reason through the workflow directly, read the local `gpt/` skill files, use local data connectors and cached evidence, and write outputs into the repository without calling the OpenAI API runner.

## How to Use

After these files are available, you can give Codex a short command such as:

```text
Run codex_prompts/RUN_SECTOR_ANALYSIS.md with theme = commercial space and defense satellite infrastructure supply chain, market = US stocks, max_companies = 10.
```

For a company-level follow-up:

```text
Run codex_prompts/RUN_COMPANY_DEEP_DIVE.md with ticker = KTOS and sector_output_folder = outputs/codex_agent_space_20260612_1523.
```

For a sector closeout:

```text
Run codex_prompts/RUN_CLOSEOUT.md with sector_output_folder = outputs/codex_agent_space_20260612_1523.
```

To decide what to do next after a completed run:

```text
Run codex_prompts/RUN_NEXT_BEST_ACTION.md with existing_run_folder = outputs/codex_agent_ai_power_20260613_1843.
```

## Available Templates

- `RUN_SECTOR_ANALYSIS.md`: Run a full Codex-agent sector workflow using local skills and connectors.
- `RUN_COMPANY_DEEP_DIVE.md`: Run a single-company deep dive using an existing sector output folder and cached evidence.
- `RUN_CLOSEOUT.md`: Produce a sector closeout summary, final classifications, missing evidence list, and lessons learned.
- `RUN_NEXT_BEST_ACTION.md`: Inspect a completed sector run and recommend the next best follow-up action.

## Guardrails

These templates are for research workflow execution only.

They do not add trading, brokerage, portfolio, auto-buy, or order execution behavior. They also do not change the `gpt/` skill files unless the user explicitly asks for a separate prompt-editing task.
