# ScoutOS Agent Instructions

ScoutOS is a personal web intelligence platform for discovering, evaluating, ranking, and monitoring opportunities across the web.

## Source of Truth

The GitHub repository is the canonical source of truth for code, documentation, architecture, and roadmap.

ChatGPT is used for reasoning and planning. Codex is used for implementation.

## Engineering Principles

- Prefer modular, reusable, maintainable components.
- Keep the architecture simple until real use cases justify more complexity.
- Favor deterministic extraction and scoring before LLM reasoning.
- Minimize token usage by passing structured data to AI components.
- Keep documentation aligned with implementation.
- Do not commit secrets, cookies, browser sessions, tokens, or API keys.

## Before Coding

Check the relevant docs under `docs/`, especially:

- `docs/vision.md`
- `docs/personal-philosophy.md`
- `docs/architecture.md`
- `docs/roadmap.md`

When architectural decisions change, update the docs in the same pull request or commit.
