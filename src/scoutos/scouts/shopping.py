"""Fixture-backed Shopping Scout dry-run pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any

from scoutos.models import ExtractedItem, Opportunity, OpportunityKind, ScoreBreakdown

FIXTURE_NAME = "vinted_frullatore.json"
REQUIRED_ACCESSORIES = frozenset({"lama", "coperchio"})
QUALITY_BRANDS = {
    "nutribullet": 16.0,
    "ninja": 16.0,
    "philips": 12.0,
    "kenwood": 12.0,
    "ariete": 8.0,
}
CONDITION_SCORES = {
    "come nuovo": 14.0,
    "nuovo senza etichetta": 12.0,
    "ottime condizioni": 12.0,
    "buone condizioni": 8.0,
    "discrete condizioni": 3.0,
}


@dataclass(frozen=True)
class RankedOpportunity:
    """Opportunity paired with deterministic scoring details."""

    opportunity: Opportunity
    score: ScoreBreakdown


def search_shopping_fixture(query: str, max_price: float, *, limit: int = 3) -> list[RankedOpportunity]:
    """Run the Sprint 1 Shopping Scout fixture pipeline."""

    extracted = extract_fixture_items(query)
    opportunities = [normalize_shopping_item(item) for item in extracted]
    in_budget = [
        opportunity
        for opportunity in opportunities
        if _total_cost(opportunity) is not None and _total_cost(opportunity) <= max_price
    ]
    ranked = [
        RankedOpportunity(opportunity=opportunity, score=score_shopping_opportunity(opportunity, max_price))
        for opportunity in in_budget
    ]
    ranked.sort(
        key=lambda item: (
            item.score.total,
            -float(item.opportunity.attributes.get("total_cost", 0)),
            item.opportunity.title.casefold(),
        ),
        reverse=True,
    )
    return ranked[:limit]


def extract_fixture_items(query: str) -> list[ExtractedItem]:
    """Load fake Vinted-like listings that match the query."""

    normalized_query = query.casefold().strip()
    return [
        _fixture_record_to_item(record)
        for record in _load_fixture()
        if normalized_query in record["title"].casefold()
        or normalized_query in record.get("description", "").casefold()
    ]


def normalize_shopping_item(item: ExtractedItem) -> Opportunity:
    """Convert a fixture listing into a normalized shopping opportunity."""

    price = float(item.raw["price"])
    shipping_cost = float(item.raw.get("shipping_cost", 0))
    attributes = {
        **item.raw,
        "shipping_cost": shipping_cost,
        "total_cost": round(price + shipping_cost, 2),
    }
    return Opportunity(
        kind=OpportunityKind.SHOPPING_DEAL,
        source=item.source,
        source_id=item.source_id,
        title=item.title,
        url=item.url,
        price=price,
        currency=item.raw.get("currency", "EUR"),
        location=item.raw.get("location"),
        description=item.raw.get("description"),
        attributes=attributes,
        observed_at=item.extracted_at,
    )


def score_shopping_opportunity(opportunity: Opportunity, max_price: float) -> ScoreBreakdown:
    """Score a shopping opportunity using deterministic marketplace rules."""

    components = {
        "budget_value": _score_budget_value(opportunity, max_price),
        "brand_quality": _score_brand(opportunity),
        "condition": _score_condition(opportunity),
        "accessories": _score_accessories(opportunity),
        "seller": _score_seller(opportunity),
        "used_sustainability": 8.0,
    }
    total = round(max(0.0, min(100.0, sum(components.values()))), 2)
    return ScoreBreakdown(total=total, components=components, reasons=_score_reasons(opportunity, components))


def _load_fixture() -> list[dict[str, Any]]:
    fixture = resources.files("scoutos.fixtures.shopping").joinpath(FIXTURE_NAME)
    return json.loads(fixture.read_text(encoding="utf-8"))


def _fixture_record_to_item(record: dict[str, Any]) -> ExtractedItem:
    return ExtractedItem(
        source=record["source"],
        source_id=record["source_id"],
        url=record["url"],
        title=record["title"],
        raw=record,
    )


def _total_cost(opportunity: Opportunity) -> float | None:
    total_cost = opportunity.attributes.get("total_cost")
    return float(total_cost) if total_cost is not None else None


def _score_budget_value(opportunity: Opportunity, max_price: float) -> float:
    total_cost = _total_cost(opportunity)
    if total_cost is None or max_price <= 0:
        return 0.0
    headroom_ratio = max(0.0, (max_price - total_cost) / max_price)
    return round(22.0 + (headroom_ratio * 18.0), 2)


def _score_brand(opportunity: Opportunity) -> float:
    brand = str(opportunity.attributes.get("brand", "")).casefold()
    return QUALITY_BRANDS.get(brand, 2.0)


def _score_condition(opportunity: Opportunity) -> float:
    condition = str(opportunity.attributes.get("condition", "")).casefold()
    return CONDITION_SCORES.get(condition, 5.0)


def _score_accessories(opportunity: Opportunity) -> float:
    accessories = {
        str(accessory).casefold()
        for accessory in opportunity.attributes.get("accessories", [])
    }
    missing = REQUIRED_ACCESSORIES - accessories
    if not missing:
        return 14.0
    return max(0.0, 8.0 - (4.0 * len(missing)))


def _score_seller(opportunity: Opportunity) -> float:
    rating = float(opportunity.attributes.get("seller_rating", 0))
    reviews = int(opportunity.attributes.get("seller_reviews", 0))
    rating_score = min(8.0, max(0.0, (rating - 4.0) * 8.0))
    review_score = 4.0 if reviews >= 50 else 2.0 if reviews >= 15 else 0.0
    return round(rating_score + review_score, 2)


def _score_reasons(opportunity: Opportunity, components: dict[str, float]) -> list[str]:
    total_cost = _total_cost(opportunity)
    reasons = [
        f"Total estimated cost is {opportunity.currency} {total_cost:.2f}.",
        f"Condition: {opportunity.attributes.get('condition', 'unknown')}.",
    ]
    if components["brand_quality"] >= 12.0:
        reasons.append("Known durable blender brand.")
    if components["accessories"] >= 14.0:
        reasons.append("Includes the key blade and lid accessories.")
    elif components["accessories"] < 8.0:
        reasons.append("Missing at least one key accessory to verify.")
    if components["seller"] >= 10.0:
        reasons.append("Seller signals are strong for a used purchase.")
    return reasons
