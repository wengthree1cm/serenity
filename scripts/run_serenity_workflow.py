#!/usr/bin/env python3
"""Local CLI runner for the Serenity markdown skill workflow."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GPT_DIR = ROOT / "gpt"
OUTPUTS_DIR = ROOT / "outputs"


@dataclass(frozen=True)
class WorkflowStep:
    skill_file: str
    output_stem: str
    requires_json: bool = True

    @property
    def raw_name(self) -> str:
        return f"{self.output_stem}.raw.md"

    @property
    def json_name(self) -> str:
        return f"{self.output_stem}.json"


WORKFLOW: list[WorkflowStep] = [
    WorkflowStep("02_THEME_RESEARCH.md", "01_theme_research"),
    WorkflowStep("03_VALUE_CHAIN_DECOMPOSITION.md", "02_value_chain"),
    WorkflowStep("04_CHOKEPOINT_SCORING.md", "03_chokepoint_scores"),
    WorkflowStep("05_COMPANY_DISCOVERY.md", "04_company_discovery"),
    WorkflowStep("06_COMMERCIAL_VALIDATION.md", "05_commercial_validation"),
    WorkflowStep("07_FINANCIAL_VALUATION_CROWDING.md", "06_valuation_crowding"),
    WorkflowStep("08_BEAR_CASE.md", "07_bear_case"),
    WorkflowStep("09_FINAL_RANKING.md", "08_final_ranking"),
    WorkflowStep("10_REPORT_WRITER.md", "final_report", requires_json=False),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Serenity-style investment research markdown workflow."
    )
    parser.add_argument("--theme", required=True, help="Research theme to evaluate.")
    parser.add_argument("--market", default="US stocks", help="Market universe.")
    parser.add_argument("--market-cap-min", type=int, default=300_000_000)
    parser.add_argument("--market-cap-max", type=int, default=20_000_000_000)
    parser.add_argument("--max-companies", type=int, default=30)
    parser.add_argument("--model", default="gpt-4.1", help="OpenAI model name.")
    parser.add_argument(
        "--session-dir",
        type=Path,
        help="Existing or desired output session folder. Use this to resume a run.",
    )
    parser.add_argument("--force", action="store_true", help="Rerun all steps.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned workflow and paths without calling the LLM.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "research_theme"


def make_session_dir(theme: str, requested: Path | None) -> Path:
    if requested is not None:
        return requested if requested.is_absolute() else ROOT / requested

    date_prefix = datetime.now().strftime("%Y-%m-%d")
    base = OUTPUTS_DIR / f"{date_prefix}_{slugify(theme)}"
    if not base.exists():
        return base

    suffix = datetime.now().strftime("%H%M%S")
    return OUTPUTS_DIR / f"{date_prefix}_{slugify(theme)}_{suffix}"


def read_skill(name: str) -> str:
    path = GPT_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required skill file: {path}")
    return path.read_text(encoding="utf-8")


def user_input_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "theme": args.theme,
        "market": args.market,
        "market_cap_min": args.market_cap_min,
        "market_cap_max": args.market_cap_max,
        "max_companies": args.max_companies,
    }


def build_prompt(
    system_principles: str,
    output_formats: str,
    skill_name: str,
    skill_markdown: str,
    payload: dict[str, Any],
    previous_output: Any,
    requires_json: bool,
) -> list[dict[str, str]]:
    output_instruction = (
        "Return only valid JSON. Do not wrap the JSON in markdown fences."
        if requires_json
        else "Return Markdown only. Do not provide trading instructions or buy/sell/hold recommendations."
    )

    user_content = f"""
You are executing one step of the Serenity-style investment research workflow.

Follow the current skill markdown exactly. Use the global principles as binding context.
Frame all outputs as research, watchlist, validation, and risk analysis only. Do not make
investment recommendations and do not add trading, brokerage, portfolio management, or
auto-buy functionality.

Current skill file: {skill_name}

Original user input:
{json.dumps(payload, indent=2)}

Previous step output:
{json.dumps(previous_output, indent=2, ensure_ascii=False) if previous_output is not None else "null"}

Current skill markdown:
---
{skill_markdown}
---

Shared output formats:
---
{output_formats}
---

Required response discipline:
{output_instruction}
"""
    return [
        {"role": "system", "content": system_principles},
        {"role": "user", "content": user_content},
    ]


def call_openai(model: str, messages: list[dict[str, str]]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required unless --dry-run is used.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "The openai package is not installed. Install dependencies with: pip install -r requirements.txt"
        ) from exc

    client = OpenAI(api_key=api_key)
    response = client.responses.create(model=model, input=messages)
    text = getattr(response, "output_text", None)
    if text:
        return text

    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            value = getattr(content, "text", None)
            if value:
                chunks.append(value)
    return "\n".join(chunks).strip()


def extract_json(raw: str) -> Any:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    starts = [idx for idx, ch in enumerate(text) if ch in "[{"]
    for start in starts:
        try:
            parsed, _ = decoder.raw_decode(text[start:])
            return parsed
        except json.JSONDecodeError:
            continue
    raise ValueError("No valid JSON object or array found.")


def repair_json(
    model: str,
    raw_output: str,
    skill_markdown: str,
    payload: dict[str, Any],
    previous_output: Any,
) -> tuple[str, Any | None]:
    repair_messages = [
        {
            "role": "system",
            "content": "Convert the provided output into valid JSON only. Do not add commentary.",
        },
        {
            "role": "user",
            "content": f"""
The previous response was not valid JSON. Return only valid JSON matching the required schema.

Original user input:
{json.dumps(payload, indent=2)}

Previous step output:
{json.dumps(previous_output, indent=2, ensure_ascii=False) if previous_output is not None else "null"}

Skill markdown:
---
{skill_markdown}
---

Invalid output to repair:
---
{raw_output}
---
""",
        },
    ]
    repaired_raw = call_openai(model, repair_messages)
    try:
        return repaired_raw, extract_json(repaired_raw)
    except ValueError:
        return repaired_raw, None


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def existing_step_output(session_dir: Path, step: WorkflowStep) -> Any:
    if step.requires_json:
        json_path = session_dir / step.json_name
        if json_path.exists():
            return json.loads(json_path.read_text(encoding="utf-8"))
        raw_path = session_dir / step.raw_name
        if raw_path.exists():
            return raw_path.read_text(encoding="utf-8")
        return None

    report_path = session_dir / "final_report.md"
    if report_path.exists():
        return report_path.read_text(encoding="utf-8")
    return None


def output_paths(session_dir: Path, step: WorkflowStep) -> tuple[Path, Path | None]:
    if step.requires_json:
        return session_dir / step.raw_name, session_dir / step.json_name
    return session_dir / "final_report.md", None


def print_dry_run(session_dir: Path, payload: dict[str, Any]) -> None:
    print("Dry run: no LLM calls will be made.")
    print(f"Session folder: {session_dir}")
    print("Input:")
    print(json.dumps(payload, indent=2))
    print("Workflow:")
    print(f"  global: {GPT_DIR / '00_SYSTEM_PRINCIPLES.md'}")
    for step in WORKFLOW:
        raw_path, json_path = output_paths(session_dir, step)
        print(f"  - {step.skill_file}")
        print(f"    raw: {raw_path}")
        if json_path:
            print(f"    json: {json_path}")


def main() -> int:
    args = parse_args()
    payload = user_input_payload(args)
    session_dir = make_session_dir(args.theme, args.session_dir)

    if args.dry_run:
        print_dry_run(session_dir, payload)
        return 0

    session_dir.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(exist_ok=True)

    system_principles = read_skill("00_SYSTEM_PRINCIPLES.md")
    output_formats = read_skill("99_OUTPUT_FORMATS.md")

    metadata: dict[str, Any] = {
        "theme": args.theme,
        "market": args.market,
        "market_cap_min": args.market_cap_min,
        "market_cap_max": args.market_cap_max,
        "max_companies": args.max_companies,
        "model": args.model,
        "session_dir": str(session_dir),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "force": args.force,
        "steps": [],
        "note": "Research workflow only. No trading, brokerage, portfolio management, or auto-buy functionality.",
    }

    previous_output: Any = None
    all_outputs: dict[str, Any] = {}

    for step in WORKFLOW:
        raw_path, json_path = output_paths(session_dir, step)
        skill_markdown = read_skill(step.skill_file)
        step_meta: dict[str, Any] = {
            "skill_file": step.skill_file,
            "raw_path": str(raw_path),
            "json_path": str(json_path) if json_path else None,
            "status": "pending",
        }

        if not args.force and raw_path.exists():
            skipped_output = existing_step_output(session_dir, step)
            if skipped_output is not None:
                previous_output = skipped_output
                all_outputs[step.output_stem] = skipped_output
                step_meta["status"] = "skipped_existing"
                metadata["steps"].append(step_meta)
                print(f"Skipping existing step: {step.skill_file}")
                continue

        prompt_previous_output = (
            {"all_previous_outputs": all_outputs, "previous_step_output": previous_output}
            if not step.requires_json
            else previous_output
        )
        messages = build_prompt(
            system_principles=system_principles,
            output_formats=output_formats,
            skill_name=step.skill_file,
            skill_markdown=skill_markdown,
            payload=payload,
            previous_output=prompt_previous_output,
            requires_json=step.requires_json,
        )

        print(f"Running step: {step.skill_file}")
        raw_response = call_openai(args.model, messages)
        raw_path.write_text(raw_response, encoding="utf-8")

        if step.requires_json and json_path is not None:
            try:
                parsed = extract_json(raw_response)
                save_json(json_path, parsed)
                previous_output = parsed
                all_outputs[step.output_stem] = parsed
                step_meta["status"] = "completed"
            except ValueError as exc:
                step_meta["json_parse_error"] = str(exc)
                repair_raw_path = session_dir / f"{step.output_stem}.repair.raw.md"
                print(f"Repairing invalid JSON for: {step.skill_file}")
                repaired_raw, repaired_json = repair_json(
                    args.model,
                    raw_response,
                    skill_markdown,
                    payload,
                    previous_output,
                )
                repair_raw_path.write_text(repaired_raw, encoding="utf-8")
                step_meta["repair_raw_path"] = str(repair_raw_path)
                if repaired_json is not None:
                    save_json(json_path, repaired_json)
                    previous_output = repaired_json
                    all_outputs[step.output_stem] = repaired_json
                    step_meta["status"] = "completed_after_repair"
                else:
                    previous_output = raw_response
                    all_outputs[step.output_stem] = raw_response
                    step_meta["status"] = "raw_saved_json_failed"
        else:
            previous_output = raw_response
            all_outputs[step.output_stem] = raw_response
            step_meta["status"] = "completed"

        metadata["steps"].append(step_meta)
        metadata["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_json(session_dir / "run_metadata.json", metadata)

    metadata["completed_at"] = datetime.now(timezone.utc).isoformat()
    save_json(session_dir / "run_metadata.json", metadata)
    print(f"Done. Outputs saved to: {session_dir}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
