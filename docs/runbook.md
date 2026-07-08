# Runbook

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,browser]"
python -m playwright install
```

## Runtime State

Keep private files local:

- `.env` for API keys and local settings
- `.auth/` or `browser-state/` for Playwright storage state
- `data/` for SQLite databases and run outputs
- `logs/` for runtime logs

These paths are ignored by git.

## Adding a New Extractor

1. Create a module under `src/scoutos/extractors/`.
2. Subclass `Extractor`.
3. Implement `extract`.
4. Return `ExtractedItem` records with stable source IDs when possible.
5. Add normalization rules that map source fields into `Opportunity`.

## Scoring Changes

Use `src/scoutos/scoring.py` for deterministic scoring components. Keep LLM ranking prompts in `prompts/` and preserve structured output expectations.

## Operational Checks

- Confirm cookies and storage state are not staged before committing.
- Keep database files out of git.
- Review extractor selectors whenever a source page changes.
- Re-run source-specific smoke checks after changing extraction code.
