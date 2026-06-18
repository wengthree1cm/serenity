# 03A Leader Business Anatomy Skill

## Purpose

Decompose a sector by studying anchor companies and industry leaders. Identify what leading companies actually build, buy, outsource, integrate, and depend on, then infer which upstream or adjacent segments may become chokepoints.

This skill uses leaders as dependency maps, not as automatic investment candidates.

## When to Use

Run after `03_VALUE_CHAIN_DECOMPOSITION.md` and before `04_CHOKEPOINT_SCORING.md`.

## Input

```json
{
  "theme": "",
  "market": "US stocks",
  "value_chain_decomposition_output": {},
  "anchor_companies": []
}
```

## Process

For each anchor company or industry leader, analyze:

1. What the company actually builds or operates.
2. What it integrates into final products, platforms, systems, or services.
3. What it likely buys from suppliers.
4. What it likely outsources or relies on partners to provide.
5. Which dependencies are scarce, technically difficult, certified, capacity constrained, or mission critical.
6. Which dependencies could become upstream or adjacent chokepoints if the theme scales.
7. Which claims are supported by hard evidence, soft evidence, or inference.

Use the leader analysis to improve the segment map before chokepoint scoring. Do not use leadership status alone as a reason to select a company for investment research.

## Key Questions

- Which inputs must leaders have for the theme to scale?
- Which capabilities do leaders keep internal because they are strategically critical?
- Which capabilities are likely supplier dependent?
- Which dependencies have long qualification cycles, certification barriers, or limited qualified capacity?
- Which suppliers, components, tools, subsystems, software layers, or services are repeatedly needed across multiple leaders?
- Which dependencies are merely generic inputs and should not be treated as chokepoints?
- What evidence is still needed before a supplier or segment claim can be scored?

## Evidence Rules

Every dependency or supplier claim must be classified as one of:

- `hard`: directly supported by filings, customer disclosures, contract awards, supply agreements, technical documentation, or other primary-source evidence.
- `soft`: supported by credible but indirect evidence such as industry reports, management commentary, job postings, product documentation, or repeated market references.
- `inference`: logically inferred from the product architecture or operating model, but not yet directly verified.

Do not infer a named supplier relationship unless evidence exists. If evidence is missing, describe the needed evidence instead of filling the gap.

## Output Format

Return only JSON.

```json
{
  "theme": "",
  "anchor_companies": [
    {
      "company_name": "",
      "ticker": "",
      "role_in_sector": "",
      "core_business_lines": [],
      "critical_dependencies": [
        {
          "dependency": "",
          "why_it_matters": "",
          "internal_or_external": "internal | external | mixed | unknown",
          "evidence_type": "hard | soft | inference",
          "evidence_summary": "",
          "source": ""
        }
      ],
      "likely_outsourced_or_supplier_dependent_areas": [
        {
          "area": "",
          "supplier_dependency_rationale": "",
          "evidence_type": "hard | soft | inference",
          "evidence_summary": "",
          "source": "",
          "named_suppliers": []
        }
      ],
      "potential_chokepoint_implications": [
        {
          "segment": "",
          "implication": "",
          "evidence_type": "hard | soft | inference",
          "evidence_summary": "",
          "source": ""
        }
      ],
      "evidence_needed": []
    }
  ],
  "leader_derived_chokepoint_candidates": [
    {
      "segment": "",
      "why_leaders_depend_on_it": "",
      "supply_constraint": "",
      "public_company_candidates": [],
      "evidence_strength": "high | medium | low",
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
  "segments_to_pass_to_chokepoint_scoring": [],
  "major_unknowns": []
}
```

## Rules

1. Do not treat leader companies themselves as automatic investment candidates.
2. Use leaders mainly to infer dependency chains.
3. Distinguish between what leaders do internally and what they likely need from suppliers.
4. Do not infer supplier relationships unless evidence exists.
5. Any supplier or dependency claim must be marked as `hard`, `soft`, or `inference`.
6. Do not overstate supplier concentration when only product architecture is known.
7. Do not promote a leader-derived segment unless the dependency is important to the theme and has at least plausible supply constraints.
8. Mark generic, commoditized, or easily substituted inputs as low-priority dependencies.

## Chokepoint Candidate Rules

Promote a segment into `leader_derived_chokepoint_candidates` only if at least one of the following is true:

1. Multiple leaders appear to depend on the same scarce input or capability.
2. The input has technical, certification, regulatory, or qualification barriers.
3. Capacity expansion appears slow or capital intensive.
4. The input is mission critical and difficult to substitute.
5. The dependency appears adjacent to the theme but may capture economics before the final-product leaders do.

## Reject Rules

Do not pass a leader-derived segment to scoring if:

1. The dependency is generic and widely available.
2. The relationship is purely speculative with no clear evidence path.
3. The segment is already captured adequately in the prior value-chain decomposition and adds no new insight.
4. The only reason for inclusion is that a famous leader operates in the theme.

## Next Step

Pass `leader_derived_chokepoint_candidates` and `segments_to_pass_to_chokepoint_scoring` into `04_CHOKEPOINT_SCORING.md` along with the original high and selected medium segments from `03_VALUE_CHAIN_DECOMPOSITION.md`.
