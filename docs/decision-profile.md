# ScoutOS Decision Profile

## Purpose

The Decision Profile represents **how a person makes decisions**.

While the Opportunity model describes **what exists in the world**, the Decision Profile describes **how those opportunities should be evaluated**.

The final recommendation is produced by evaluating an Opportunity against a Decision Profile.

```text
Decision Profile
        │
        ▼
Opportunity
        │
        ▼
Evaluation
        │
        ▼
Recommendation
```

---

# Stable Components

These rarely change.

## Values

Core principles.

Examples:

- sustainability
- long-term thinking
- quality over quantity
- transparency
- learning
- minimalism
- privacy

---

Taste

Taste reflects aesthetic, cultural, and emotional preferences. It influences recommendations but should never override core values or practical constraints.

Examples:

- Linux, Python, open source, transparency, and community-driven ecosystems.
- Objects with identity, history, or craftsmanship rather than anonymous, generic products.
- Logos and brands are appreciated when they represent tradition, heritage, engineering excellence, or a meaningful story—not - as status symbols.
- Preference for second-hand marketplaces and the culture of repair, reuse, and circular economy.
- Essentiality: removing the unnecessary while preserving quality and purpose.
- Appreciation for independent thinkers, niche communities, and subcultures that challenge conventional thinking.
- Preference for authentic experiences over mainstream trends.
- Attraction to elegant, timeless design rather than short-lived fashion.
- Preference for tools that empower autonomy rather than dependence.
---

## Decision Rules

Rules that guide evaluation.

Examples:

- prefer used before buying new
- avoid vendor lock-in
- buy once, buy well
- explain every recommendation
- never optimize only for price

---

# Semi-Stable Components

These evolve over months.

## Goals

Examples:

- improve AI engineering skills
- reduce waste
- optimize spending
- increase minimalismn
- save time, save monay in the long term

---

## Constraints

Current limits.

Examples:

- budget
- available time
- location
- transportation
- family commitments

Constraints are temporary and should never be confused with values.

---

# Dynamic Components

These change continuously.

## Context

Current situation.

Examples:

- already owns an immersion blender
- travelling next month
- currently looking for DevSecOps roles
- working from home

---

## Feedback

Records previous decisions.

Examples:

- accepted recommendation
- rejected recommendation
- ignored recommendation

Feedback should help improve future scoring.

---

## Learned Preferences

Patterns inferred from repeated decisions.

Examples:

- consistently prefers Bosch over Philips
- rarely buys new electronics
- usually accepts local pickup
- values repairability

Learned preferences should always be explainable and overridable.

---

# Domain-Specific Extensions

Shopping

- preferred brands
- preferred marketplaces
- acceptable wear level

Jobs

- preferred countries
- salary expectations
- remote preference

Travel

- preferred airlines
- stopover tolerance
- luggage preferences

Real Estate

- commuting time
- minimum size
- energy efficiency

---

# Design Principles

The Decision Profile should:

- remain explainable
- separate facts from preferences
- distinguish stable values from temporary constraints
- evolve through explicit feedback and observed decisions
- never silently override user intent

---

# Long-Term Vision

The Decision Profile should become ScoutOS's personal reasoning model.

Rather than asking:

> "What is the best opportunity?"

ScoutOS should answer:

> "What is the best opportunity for this person, given their values, goals, constraints, and current context?"