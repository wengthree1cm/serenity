# 10 Report Writer Skill

## Purpose

Convert the full workflow output into a clear, readable research report for a human investor.

The report should explain the reasoning chain, evidence quality, top candidates, and next research tasks.

## When to Use

Run after `09_FINAL_RANKING.md`.

## Input

```json
{
  "theme": "",
  "all_previous_outputs": {},
  "final_rankings": {}
}
```

## Report Requirements

The report must be written in clear language and organized around the Serenity-style research logic:

1. Theme
2. Value chain
3. Chokepoints
4. Companies
5. Commercial validation
6. Valuation/crowding
7. Bear case
8. Final watchlist
9. Next research actions

## Tone

Use a research analyst tone.

Avoid promotional language.

Do not say the user should buy or sell. Use research classifications only.

## Required Sections

### 1. Executive Summary

Summarize:

- the theme;
- whether it is worth researching;
- the strongest chokepoint segments;
- the best company candidates;
- the biggest risks.

### 2. Theme Assessment

Explain why the theme is or is not structurally attractive.

### 3. Value Chain Map

Show the value chain and identify where economic bottlenecks may appear.

### 4. Chokepoint Analysis

List the top segments and why they scored highly.

### 5. Candidate Company Table

Include:

- ticker;
- company;
- segment;
- business relevance;
- commercial validation level;
- valuation status;
- crowding status;
- final classification.

### 6. High Priority Research Candidates

For each candidate:

- thesis;
- evidence;
- valuation/crowding view;
- bear case;
- catalysts;
- what to verify next.

### 7. Watchlist and Wait-for-Pullback Candidates

Explain why they are not ranked higher.

### 8. Rejects / Avoid List

Explain why rejected companies failed.

### 9. Evidence Quality and Missing Data

Separate:

- hard evidence;
- soft evidence;
- inference;
- missing data.

### 10. Next Research Checklist

Provide actionable next research tasks, such as:

- read latest 10-K/10-Q;
- read last two earnings calls;
- verify backlog trend;
- compare peer valuation;
- monitor next earnings date;
- verify customer concentration;
- track capex announcements;
- watch for guidance changes.

## Output Format

Return Markdown.

```markdown
# Serenity Scanner Report: [Theme]

## Executive Summary

...

## Theme Assessment

...

## Value Chain Map

...

## Chokepoint Analysis

...

## Candidate Company Table

...

## High Priority Research Candidates

...

## Watchlist / Wait for Pullback

...

## Rejects / Avoid List

...

## Evidence Quality

...

## Next Research Checklist

...

## Important Note

This report is for research purposes only. It is not a buy, sell, or hold recommendation.
```

## Reject Rules

Do not include unsupported promotional claims.

Do not hide missing data.

Do not treat inference as fact.

Do not give price targets unless a separate valuation model has been explicitly run.

## Next Step

Save the report as:

```text
outputs/final_report.md
```
