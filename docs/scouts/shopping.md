# Shopping Scout

The Shopping Scout is the first practical ScoutOS study case.

Its goal is to help evaluate marketplace and e-commerce opportunities using structured extraction, scoring, and transparent recommendations.

## Initial Sources

- Vinted
- eBay
- Subito
- Amazon, later and only where appropriate

## Current Study Case

Find the best running wireless earbuds under a EUR 40 target budget.

This use case is useful because it exercises:

- fixture-based listing extraction
- price comparison
- condition assessment
- missing charging case and accessory detection
- sport-fit assessment
- sustainability and minimalism principles
- recommendation explanation

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

## Current Dry Run

The current local command uses running-earbuds fixture data and the default Decision Profile:

```bash
scout shopping search --query "running wireless earbuds" --max-price 40
```

Pipeline:

```text
Search fixture -> Extract -> Normalize -> Evaluate -> Rank -> Print recommendations
```

Evaluation is deterministic and considers listing facts together with profile preferences such as
sustainability, used-market preference, durability, minimalism, and accessory completeness. It does
not use Playwright, live scraping, SQLite, notifications, or LLM calls.

## Recommendation Style

Recommendations should explain:

- why it is a good or bad deal
- what to verify before buying
- likely negotiation target
- alternatives worth considering
- whether waiting is better than acting
