# ScoutOS

ScoutOS is a personal decision intelligence platform that discovers, evaluates, ranks, monitors, and helps act on opportunities across shopping, jobs, travel, real estate, events, learning, and other domains.

ScoutOS does not optimize for finding more opportunities. It optimizes for making better decisions.

The project is built around two core concepts:

- **Opportunity** — something worth evaluating.
- **Decision Profile** — how opportunities should be evaluated for a specific person.

The project is designed around a small Python core with source-specific extractors, normalized opportunity models, reusable scoring, and future-ready persistence for SQLite.

## Goals

- Discover opportunities from web pages, feeds, saved searches, and alerts.
- Extract structured candidates with Playwright-ready browser automation.
- Rank candidates using transparent scoring rules and AI-assisted reasoning where it adds value.
- Monitor changes over time, including price drops, new listings, and stale results.
- Help users make explainable, value-aligned decisions rather than simply presenting search results.
- Keep credentials, cookies, browser profiles, and local databases out of git.

## Project Layout

```text
docs/                       Architecture, runbook, and methodology
prompts/                    Ranking prompt templates
src/scoutos/                Python package
src/scoutos/extractors/     Source-specific extraction modules
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
scout shopping search --query "running wireless earbuds" --max-price 40
```

ScoutOS does not commit secrets, cookies, browser state, or SQLite database files. Use `.env`, local browser profiles, or a local `data/` directory for private runtime state.

Browser automation is intentionally not required for the current Shopping Scout dry run. Install
the optional browser extra only when working on future live extraction:

```bash
pip install -e ".[browser]"
python -m playwright install
```

## Status

Early-stage project developed incrementally through small, validated vertical slices. The current
Shopping Scout dry run uses running-earbuds fixture data, a default Decision Profile, and
deterministic evaluation.
