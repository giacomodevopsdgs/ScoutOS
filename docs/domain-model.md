# ScoutOS Domain Model

This document defines the initial shared vocabulary for ScoutOS.

It is intentionally lightweight. The model should evolve only when real Scouts expose concrete needs.

## Core Question

What is an Opportunity?

In ScoutOS, an **Opportunity** is any candidate worth evaluating against a user's intent, constraints, preferences, and personal philosophy.

An Opportunity can represent many things:

- a product listing
- a job opening
- a flight option
- a house or rental listing
- an event
- a course
- an investment idea

The purpose of the domain model is to let all Scouts speak the same language while still allowing each domain to keep source-specific details.

## Universal Concepts

### Opportunity

The canonical object evaluated by ScoutOS.

Universal fields should include:

- `id`: stable internal identifier
- `title`: human-readable name
- `summary`: short description when available
- `source`: where the opportunity came from
- `url`: original URL when available
- `category`: shopping, job, travel, real_estate, event, learning, etc.
- `location`: physical or remote location when relevant
- `price`: cost, salary, rent, fare, or economic value when relevant
- `evidence`: facts used to evaluate the opportunity
- `score`: structured score and reasoning
- `metadata`: timestamps and source-specific technical information

### Source

Represents where the opportunity was discovered.

Examples:

- Vinted
- eBay
- LinkedIn
- company career page
- Google Flights
- Immobiliare.it

Suggested fields:

- `name`
- `type`
- `url`
- `retrieved_at`

### Price

Represents economic information.

For shopping this may be item price plus shipping.
For jobs this may be salary or compensation range.
For real estate this may be rent, sale price, condominium fees, or tax assumptions.
For travel this may be fare plus baggage and transfer costs.

Suggested fields:

- `amount`
- `currency`
- `shipping_cost`
- `fees`
- `total_estimated_cost`
- `period` when relevant, such as monthly or yearly
- `confidence`

### Location

Represents where the opportunity is physically or logically located.

Suggested fields:

- `city`
- `region`
- `country`
- `remote`
- `distance_km`

### Evidence

Evidence is the structured set of facts used to support a score or recommendation.

Examples:

- product condition
- seller reliability signals
- salary range
- commute distance
- flight duration
- real estate square meters
- listing age
- historical price comparison

Evidence should remain factual. Interpretation belongs in scoring or recommendation.

### ScoreBreakdown

A transparent explanation of how an opportunity was evaluated.

Suggested fields:

- `overall_score`
- `components`
- `reasons`
- `risks`
- `confidence`

Scores should be explainable. ScoutOS should avoid opaque recommendations.

### Recommendation

A human-facing evaluation of what to do next.

Possible recommendation actions:

- buy
- apply
- inspect
- negotiate
- monitor
- wait
- reject

Suggested fields:

- `action`
- `summary`
- `pros`
- `cons`
- `next_steps`
- `confidence`

## Universal vs Source-Specific Fields

Universal fields belong directly on `Opportunity`.

Source-specific details should live under a separate structure, such as `attributes` or `domain_data`.

Example:

```text
Opportunity
  title
  source
  url
  price
  location
  score
  attributes
```

For a shopping listing, `attributes` may include:

- brand
- model
- condition
- accessories included
- seller rating

For a job opening, `attributes` may include:

- company
- role level
- contract type
- required skills
- salary range

For travel, `attributes` may include:

- airline
- departure airport
- arrival airport
- duration
- baggage policy

For real estate, `attributes` may include:

- square meters
- rooms
- energy class
- floor
- condominium fees

## Domain Examples

### Shopping

A blender listing on Vinted is an Opportunity.

Universal fields:

- title
- price
- source
- URL
- location
- score

Source-specific fields:

- condition
- seller signals
- accessories
- brand
- model

### Jobs

A DevSecOps job opening in Lugano is an Opportunity.

Universal fields:

- title
- source
- location
- price as salary or compensation range
- evidence
- score

Source-specific fields:

- company
- required skills
- remote policy
- contract type
- seniority

### Travel

A flight to Japan in October is an Opportunity.

Universal fields:

- title
- source
- price
- location
- evidence
- score

Source-specific fields:

- airline
- departure airport
- arrival airport
- stops
- baggage
- duration

### Real Estate

A rental or property listing is an Opportunity.

Universal fields:

- title
- source
- price
- location
- evidence
- score

Source-specific fields:

- square meters
- rooms
- floor
- energy class
- monthly fees
- ownership or rental constraints

## Initial Design Principle

Start with a small model and extend only through real cases.

ScoutOS should not try to model every domain perfectly from day one. The first implementation should support the Shopping Scout while keeping enough abstraction to avoid blocking future Scouts.
