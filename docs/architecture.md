# ScoutOS Architecture

This document describes the initial architecture of ScoutOS. It is intentionally lightweight and should evolve through real use cases.

## Mental Model

ScoutOS is built around independent Scouts.

A Scout is a domain-specific module that searches a source, extracts structured data, normalizes it, scores it, and returns recommendations.

Examples:

- Shopping Scout
- Job Scout
- Travel Scout
- Real Estate Scout
- Event Scout

## Standard Pipeline

```text
Search -> Extract -> Normalize -> Score -> Rank -> Notify
```

## Core Concepts

- `Opportunity` is the normalized item ScoutOS evaluates, regardless of source.
- `ExtractedItem` is raw structured data emitted by an extractor before normalization.
- `ScoreBreakdown` captures transparent scoring components and reasons.
- `Extractor` is a source-specific adapter that can later use Playwright, HTTP, feeds, or APIs.
- `Scout` is the domain-specific orchestrator that connects intent, source, extraction, scoring, ranking, and notification.

## Core Components

### Browser Layer

Uses Playwright to interact with web pages when no stable API is available.

Responsibilities:

- navigation
- login/session reuse when appropriate
- page interaction
- structured extraction

Browser session state should live outside git, for example in `.auth/` or `browser-state/`, and should be loaded at runtime.

### Extractors

Extractors convert source-specific pages, feeds, or APIs into structured records.

They should avoid returning raw HTML when possible.

### Models

Models define normalized data structures shared across Scouts.

Examples:

- Opportunity
- Source
- Price
- ScoreBreakdown
- Recommendation

### Scoring Engine

The scoring engine evaluates opportunities using deterministic rules first.

AI reasoning can be added later for explanation, summarization, ambiguity handling, and subjective trade-offs.

### Storage

SQLite is the default local storage for early development.

It can later be replaced or complemented by PostgreSQL if ScoutOS becomes service-oriented.

SQLite should support:

- opportunity snapshots
- source runs and run metadata
- score history
- watchlists and saved queries
- alerts and notification state

SQLite files belong in `data/` or another local path ignored by git.

### Notification Layer

Notifications should be optional and pluggable.

Potential channels:

- terminal output
- email
- Telegram
- Discord

## Design Rules

- Keep Scouts independent.
- Share common pipeline components.
- Prefer structured data over page screenshots or full HTML.
- Keep early implementations simple.
- Refactor only when repeated patterns appear.
- Update documentation when architectural decisions change.

## Initial Source Target

The first real study case should be a Shopping Scout using Vinted, because it provides immediate value and exercises the full pipeline: browser automation, extraction, scoring, ranking, and recommendation.
