# serenity

## Serenity Research Workflow Runner

This project includes a local CLI runner for the Serenity-style investment research pipeline. It executes the markdown skills in `gpt/` step by step and saves each raw model response plus parsed JSON when JSON is required.

Run a dry run first:

```bash
python scripts/run_serenity_workflow.py --theme "AI data center power infrastructure" --dry-run
```

Run the workflow:

```bash
export OPENAI_API_KEY="your_api_key"
python scripts/run_serenity_workflow.py --theme "AI data center power infrastructure"
```

Optional inputs:

```bash
python scripts/run_serenity_workflow.py \
  --theme "AI data center power infrastructure" \
  --market "US stocks" \
  --market-cap-min 300000000 \
  --market-cap-max 20000000000 \
  --max-companies 30
```

Resume an existing session:

```bash
python scripts/run_serenity_workflow.py \
  --theme "AI data center power infrastructure" \
  --session-dir outputs/2026-06-08_ai_data_center_power_infrastructure
```

Rerun all steps in a session:

```bash
python scripts/run_serenity_workflow.py \
  --theme "AI data center power infrastructure" \
  --session-dir outputs/2026-06-08_ai_data_center_power_infrastructure \
  --force
```

The runner creates timestamped folders under `outputs/`. It is a research workflow only: it does not add trading, brokerage, portfolio management, auto-buy functionality, or investment recommendations.
