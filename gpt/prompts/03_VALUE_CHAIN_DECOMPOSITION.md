# 03 Value Chain Decomposition Skill

## Purpose

Break the approved theme into a detailed value chain so that chokepoint segments can be identified before any company is selected.

## When to Use

Run after `02_THEME_RESEARCH.md` returns `continue_to_value_chain = true`.

## Input

```json
{
  "theme_research_output": {},
  "theme": "",
  "market": "US stocks"
}
```

## Process

Decompose the theme into value-chain segments. Use the most relevant categories for the theme.

Typical categories:

- Upstream materials
- Specialized components
- Core equipment
- Manufacturing tools
- Software/control systems
- Integration/EPC
- Distribution/channel
- Maintenance/services
- End customers
- Terminal applications

For each segment, identify:

1. What the segment does.
2. Why it matters to the theme.
3. What drives demand.
4. What constrains supply.
5. Whether customers can easily substitute suppliers.
6. Whether margins could expand when demand rises.
7. Representative public companies or private leaders.
8. Evidence quality.

## Key Questions

- What must exist for the theme to scale?
- Which physical, software, regulatory, or operational inputs are required?
- Which segments have the longest lead times?
- Which segments have the fewest qualified suppliers?
- Which segments have customer qualification or certification barriers?
- Which segments are likely to capture incremental economics?
- Which segments are commoditized and should be avoided?

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "value_chain_summary": "",
  "segments": [
    {
      "segment_id": "S1",
      "segment_name": "",
      "value_chain_position": "upstream_materials | component | equipment | software | integration | service | customer | other",
      "role_in_theme": "",
      "demand_driver": "",
      "supply_constraint": "",
      "customer_switching_cost": "low | medium | high | unknown",
      "substitution_risk": "low | medium | high | unknown",
      "margin_expansion_potential": "low | medium | high | unknown",
      "representative_companies": [],
      "evidence": [
        {
          "evidence_type": "hard | soft | inference",
          "summary": "",
          "source": ""
        }
      ],
      "initial_attractiveness": "low | medium | high"
    }
  ],
  "segments_to_score_next": [],
  "major_unknowns": []
}
```

## Scoring Rules

This skill does not assign final chokepoint scores. It should assign only `initial_attractiveness`.

Use:

- `high` if the segment appears required, constrained, and not obviously crowded.
- `medium` if the segment is important but constraints are uncertain.
- `low` if the segment is commoditized, crowded, easily substituted, or weakly connected.

## Reject Rules

Mark a segment as low priority if:

1. It is a commodity input with many suppliers.
2. It has little pricing power.
3. It is only indirectly related to the theme.
4. Customers can easily switch suppliers.
5. The segment is already dominated by mega-cap companies with little hidden opportunity.

## Next Step

Pass all `high` and selected `medium` segments to `04_CHOKEPOINT_SCORING.md`.
