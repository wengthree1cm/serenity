# Serenity Scanner GPT Skills

This folder contains a modular LLM research workflow for Serenity-style investment research.

The system is designed to move from:

`Theme → Value Chain → Leader Anatomy → Leader Future Optionality → Chokepoint Segment → Company Discovery → Commercial Validation → Valuation & Crowding → Bear Case → Final Ranking → Report`

It is not a stock picker and does not produce automatic buy/sell instructions. It produces structured research outputs, evidence levels, risk flags, and a watchlist for further human review.

## Recommended Execution Order

1. `00_SYSTEM_PRINCIPLES.md`
2. `01_WORKFLOW_ROUTER.md`
3. `02_THEME_RESEARCH.md`
4. `03_VALUE_CHAIN_DECOMPOSITION.md`
5. `03A_LEADER_BUSINESS_ANATOMY.md`
6. `03B_LEADER_FUTURE_OPTIONALITY.md`
7. `04_CHOKEPOINT_SCORING.md`
8. `05_COMPANY_DISCOVERY.md`
9. `06_COMMERCIAL_VALIDATION.md`
10. `07_FINANCIAL_VALUATION_CROWDING.md`
11. `08_BEAR_CASE.md`
12. `09_FINAL_RANKING.md`
13. `10_REPORT_WRITER.md`
14. `99_OUTPUT_FORMATS.md`

## Engineering Note

Each `.md` file is a skill instruction. The runner should load the relevant skill file, combine it with the previous step output, call the LLM, validate JSON, and save the output.

The runner should not rely on a single giant prompt. Each stage should be executed separately and persisted to disk.
