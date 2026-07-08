# Architecture

ScoutOS is organized as a small pipeline:

1. **Discovery** finds candidate pages, searches, feeds, or alerts.
2. **Extraction** turns raw web data into normalized opportunity records.
3. **Evaluation** scores records against user intent, constraints, and history.
4. **Ranking** sorts candidates for review or action.
5. **Monitoring** stores snapshots and detects changes over time.

## Core Concepts

- `Opportunity` is the normalized item ScoutOS evaluates, regardless of source.
- `ExtractedItem` is raw structured data emitted by an extractor before normalization.
- `ScoreBreakdown` captures transparent scoring components and reasons.
- `Extractor` is a source-specific adapter that can later use Playwright, HTTP, feeds, or APIs.

## Playwright-Ready Extraction

Extractors expose async methods so browser-backed implementations can reuse Playwright without changing the calling model. Browser session state should live outside git, for example in `.auth/` or `browser-state/`, and should be loaded at runtime.

Expected future flow:

```text
Browser context -> source extractor -> extracted items -> opportunity model -> scoring -> SQLite
```

## SQLite-Ready Persistence

The first scaffold keeps models in Python dataclasses. A future persistence layer should use SQLite for:

- opportunity snapshots
- source runs and run metadata
- score history
- watchlists and saved queries
- alerts and notification state

SQLite files belong in `data/` or another local path ignored by git.

## Source Modules

Each extractor should keep source-specific parsing isolated. Shared behavior belongs in `src/scoutos/extractors/base.py` or future service modules.

Initial source target:

- `vinted.py` for marketplace deal discovery and price monitoring
