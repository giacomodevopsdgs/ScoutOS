"""Deterministic scoring primitives for ScoutOS opportunities."""

from __future__ import annotations

from scoutos.models import Opportunity, ScoreBreakdown


def score_opportunity(
    opportunity: Opportunity,
    *,
    target_price: float | None = None,
    preferred_locations: set[str] | None = None,
    required_terms: set[str] | None = None,
) -> ScoreBreakdown:
    """Score an opportunity with simple transparent rules."""

    components: dict[str, float] = {
        "base": 50.0,
        "price": _score_price(opportunity.price, target_price),
        "location": _score_location(opportunity.location, preferred_locations),
        "terms": _score_terms(opportunity, required_terms),
        "completeness": _score_completeness(opportunity),
    }
    total = max(0.0, min(100.0, sum(components.values())))
    reasons = _reasons(opportunity, components)
    return ScoreBreakdown(total=round(total, 2), components=components, reasons=reasons)


def _score_price(price: float | None, target_price: float | None) -> float:
    if price is None or target_price is None or target_price <= 0:
        return 0.0
    if price <= target_price:
        return 20.0
    overage = (price - target_price) / target_price
    return max(-20.0, -40.0 * overage)


def _score_location(location: str | None, preferred_locations: set[str] | None) -> float:
    if not preferred_locations:
        return 0.0
    if not location:
        return -5.0
    normalized = location.casefold()
    if any(place.casefold() in normalized for place in preferred_locations):
        return 10.0
    return -5.0


def _score_terms(opportunity: Opportunity, required_terms: set[str] | None) -> float:
    if not required_terms:
        return 0.0
    haystack = " ".join(
        value
        for value in [opportunity.title, opportunity.description or ""]
        if value
    ).casefold()
    missing = [term for term in required_terms if term.casefold() not in haystack]
    return 10.0 if not missing else -5.0 * len(missing)


def _score_completeness(opportunity: Opportunity) -> float:
    fields = [
        opportunity.title,
        opportunity.url,
        opportunity.price,
        opportunity.location,
        opportunity.description,
    ]
    present = sum(value is not None and value != "" for value in fields)
    return present * 2.0


def _reasons(opportunity: Opportunity, components: dict[str, float]) -> list[str]:
    reasons = [f"{opportunity.source} item scored as {opportunity.kind.value}."]
    if components["price"] > 0:
        reasons.append("Price is at or below the configured target.")
    elif components["price"] < 0:
        reasons.append("Price is above the configured target.")
    if components["location"] > 0:
        reasons.append("Location matches a preferred area.")
    if components["terms"] < 0:
        reasons.append("Required terms are missing from the title or description.")
    return reasons
