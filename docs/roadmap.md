# ScoutOS Roadmap

This roadmap is intentionally lightweight. It should be refined through real study cases.

## Phase 0 - Project Foundation

- Keep GitHub as the source of truth.
- Maintain core project documents.
- Define agent instructions for Codex.
- Keep secrets and browser sessions out of git.

## Phase 1 - First Study Case: Shopping Scout

Goal: use Vinted as the first practical source.

Initial capabilities:

- search for a product category
- extract title, price, condition, shipping, location, seller signals, and URL
- normalize listings into Opportunity records
- score candidates using deterministic rules
- explain recommendations using ScoutOS principles

Success criteria:

- ScoutOS can rank a small set of marketplace listings.
- The output is more useful than manual browsing.
- The code remains generic enough to support future sources.

## Phase 2 - Persistence

- Add SQLite persistence.
- Store search runs and opportunity snapshots.
- Track price changes over time.
- Detect new, changed, and removed listings.

## Phase 3 - Alerts

- Add watchlists.
- Add threshold-based alerts.
- Start with terminal or email notifications.
- Add Telegram or Discord later.

## Phase 4 - Additional Scouts

Potential next Scouts:

- Job Scout
- Travel Scout
- Real Estate Scout
- Event Scout

Each new Scout should reuse the same Search -> Extract -> Normalize -> Score -> Rank -> Notify pipeline.

## Phase 5 - AI-Assisted Ranking

Use AI only where it adds value:

- subjective trade-off analysis
- recommendation explanation
- negotiation messages
- uncertainty handling
- comparison summaries

Avoid sending large raw pages or unnecessary HTML to LLMs.
