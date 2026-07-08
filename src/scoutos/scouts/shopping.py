"""Fixture-backed Shopping Scout dry-run pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any

from scoutos.evaluation import (
    DecisionProfile,
    Evaluation,
    default_decision_profile,
    evaluate,
)
from scoutos.models import ExtractedItem, Opportunity, OpportunityKind

FIXTURE_NAME = "running_wireless_earbuds.json"


@dataclass(frozen=True)
class RankedOpportunity:
    """Opportunity paired with profile-aware evaluation details."""

    opportunity: Opportunity
    evaluation: Evaluation


def search_shopping_fixture(
    query: str,
    max_price: float,
    *,
    limit: int = 3,
    decision_profile: DecisionProfile | None = None,
) -> list[RankedOpportunity]:
    """Run the Shopping Scout fixture pipeline."""

    profile = decision_profile or default_decision_profile()
    extracted = extract_fixture_items(query)
    opportunities = [normalize_shopping_item(item) for item in extracted]
    in_budget = [
        opportunity
        for opportunity in opportunities
        if _total_cost(opportunity) is not None and _total_cost(opportunity) <= max_price
    ]
    ranked = [
        RankedOpportunity(
            opportunity=opportunity,
            evaluation=evaluate(
                opportunity,
                profile,
                context={"query": query, "max_price": max_price},
            ),
        )
        for opportunity in in_budget
    ]
    ranked.sort(
        key=lambda item: (
            item.evaluation.score,
            -float(item.opportunity.attributes.get("total_cost", 0)),
            item.opportunity.title.casefold(),
        ),
        reverse=True,
    )
    return ranked[:limit]


def extract_fixture_items(query: str) -> list[ExtractedItem]:
    """Load fake Vinted-like listings that match the query."""

    query_terms = _query_terms(query)
    return [
        _fixture_record_to_item(record)
        for record in _load_fixture()
        if _matches_query(record, query_terms)
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


def _query_terms(query: str) -> set[str]:
    stopwords = {"for", "the", "a", "an"}
    return {
        term
        for term in query.casefold().replace("-", " ").split()
        if term and term not in stopwords
    }


def _matches_query(record: dict[str, Any], query_terms: set[str]) -> bool:
    haystack = " ".join(
        [
            record["title"],
            record.get("description", ""),
            record.get("category", ""),
            record.get("use_case", ""),
            " ".join(record.get("tags", [])),
        ]
    ).casefold()
    return all(term in haystack for term in query_terms)
