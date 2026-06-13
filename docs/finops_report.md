# Token FinOps Report — Graph-Nav vs. Naive Ingestion

## Executive Summary

| Metric | Value |
|--------|-------|
| Queries benchmarked | 3 |
| Average token savings | **98.9%** |
| Target savings | ≥ 70% (aim 95%) |
| Status | ✅ TARGET MET |

## Query Results

| ID | Question | Naive Tokens | Nav Tokens | Savings |
|----|----------|-------------|------------|---------|
| q1 | What is the main execution flow when a Crew is kicke… | 51,428 | 420 | **99.2%** |
| q2 | How does Task output propagate between agents in a s… | 35,822 | 485 | **98.6%** |
| q3 | What memory retention patterns does the Agent use fo… | 37,412 | 406 | **98.9%** |

## Methodology

- **Naive**: full source files concatenated for the query.
- **Graph-nav**: node metadata + 1-hop edges from `vault/graph.json`.
- **Token estimate**: `floor(char_count / 4)` (Anthropic standard).

## Per-Query Detail

### q1: What is the main execution flow when a Crew is kicked off?

- Naive: 205,714 chars → **51,428 tokens**
- Graph-nav: 1,680 chars → **420 tokens**
- Saved: 51,008 tokens (**99.2%**)

### q2: How does Task output propagate between agents in a sequential process?

- Naive: 143,288 chars → **35,822 tokens**
- Graph-nav: 1,940 chars → **485 tokens**
- Saved: 35,337 tokens (**98.6%**)

### q3: What memory retention patterns does the Agent use for context?

- Naive: 149,650 chars → **37,412 tokens**
- Graph-nav: 1,624 chars → **406 tokens**
- Saved: 37,006 tokens (**98.9%**)
