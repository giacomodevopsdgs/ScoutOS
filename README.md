# ScoutOS

ScoutOS is a personal web intelligence agent for discovering, evaluating, ranking, and monitoring opportunities across shopping deals, job openings, flights and travel, real estate, events, and price tracking.

The project is designed around a small Python core with source-specific extractors, normalized opportunity models, reusable scoring, and future-ready persistence for SQLite.

## Goals

- Discover opportunities from web pages, feeds, saved searches, and alerts.
- Extract structured candidates with Playwright-ready browser automation.
- Rank candidates using transparent scoring rules and LLM-assisted judgment.
- Monitor changes over time, including price drops, new listings, and stale results.
- Keep credentials, cookies, browser profiles, and local databases out of git.

## Project Layout

```text
docs/                       Architecture, runbook, and use cases
prompts/                    Ranking prompt templates
src/scoutos/                Python package
src/scoutos/extractors/     Source-specific extraction modules
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,browser]"
python -m playwright install
```

ScoutOS does not commit secrets, cookies, browser state, or SQLite database files. Use `.env`, local browser profiles, or a local `data/` directory for private runtime state.

## Status

Initial scaffold.
