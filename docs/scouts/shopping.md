# Shopping Scout

The Shopping Scout is the first practical ScoutOS study case.

Its goal is to help evaluate marketplace and e-commerce opportunities using structured extraction, scoring, and transparent recommendations.

## Initial Sources

- Vinted
- eBay
- Subito
- Amazon, later and only where appropriate

## Initial Use Case

Find the best personal blender under a target budget.

This use case is useful because it exercises:

- browser automation
- listing extraction
- price comparison
- condition assessment
- missing accessory detection
- sustainability and minimalism principles
- recommendation explanation

## Sprint 1 Dry Run

The first implemented vertical slice is intentionally fixture-based:

```bash
scout shopping search --query "frullatore" --max-price 60
```

Pipeline:

```text
Search fixture -> Extract -> Normalize -> Score -> Rank -> Print recommendations
```

This dry run does not use Playwright, live scraping, SQLite, notifications, or LLM calls.
It validates the pipeline shape with deterministic scoring before adding real marketplace
automation.

## Candidate Fields

A normalized shopping opportunity should ideally include:

- title
- brand
- model
- price
- shipping cost
- total estimated cost
- condition
- seller location
- seller reputation signals
- accessories included
- listing URL
- source
- extraction timestamp

## Scoring Dimensions

Possible scoring dimensions:

- price versus estimated market value
- product quality
- expected durability
- condition
- completeness of accessories
- seller reliability
- local pickup or reduced shipping impact
- resale value
- fit with personal philosophy

## Recommendation Style

Recommendations should explain:

- why it is a good or bad deal
- what to verify before buying
- likely negotiation target
- alternatives worth considering
- whether waiting is better than acting
