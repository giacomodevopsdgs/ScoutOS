from __future__ import annotations

from scoutos.evaluation import EvaluationAction, default_decision_profile, evaluate
from scoutos.models import Opportunity, OpportunityKind


def test_evaluate_reflects_default_decision_profile_preferences() -> None:
    opportunity = Opportunity(
        kind=OpportunityKind.SHOPPING_DEAL,
        source="vinted_fixture",
        source_id="good-running-earbuds",
        title="Jabra Elite 4 Active wireless earbuds",
        url="https://example.test/listing",
        price=28.0,
        currency="EUR",
        location="Milano",
        description="Complete sport earbuds with charging case and spare ear tips.",
        attributes={
            "brand": "Jabra",
            "model": "Elite 4 Active",
            "condition": "good",
            "total_cost": 32.0,
            "estimated_market_value": 48.0,
            "seller_rating": 4.9,
            "seller_reviews": 84,
            "accessories": ["charging case", "ear tips", "usb-c cable"],
            "water_resistant": True,
            "water_resistance": "IP57",
            "sport_features": ["secure fit", "running"],
            "replacement_parts_available": True,
            "local_pickup": True,
        },
    )

    evaluation = evaluate(opportunity, default_decision_profile(), context={"max_price": 40})

    assert evaluation.score >= 80
    assert evaluation.action == EvaluationAction.BUY
    assert not evaluation.risks
    assert "Brand matches the durability preference." in evaluation.reasons
    assert "Sport-oriented design fits running use." in evaluation.reasons
    assert "Complete durable item supports the minimalism preference." in evaluation.reasons


def test_evaluate_surfaces_missing_charging_case_risk() -> None:
    opportunity = Opportunity(
        kind=OpportunityKind.SHOPPING_DEAL,
        source="vinted_fixture",
        source_id="incomplete-earbuds",
        title="Jabra Elite 3 wireless earbuds",
        url="https://example.test/listing",
        price=24.0,
        currency="EUR",
        location="Bologna",
        description="Earbuds only, missing the charging case.",
        attributes={
            "brand": "Jabra",
            "model": "Elite 3",
            "condition": "fair",
            "total_cost": 28.0,
            "estimated_market_value": 38.0,
            "seller_rating": 4.5,
            "seller_reviews": 18,
            "accessories": ["ear tips"],
            "water_resistant": True,
            "water_resistance": "IP55",
            "sport_features": ["compact fit"],
        },
    )

    evaluation = evaluate(opportunity, default_decision_profile(), context={"max_price": 40})

    assert evaluation.risks == ["Missing required accessory verification: charging case."]
    assert evaluation.action == EvaluationAction.INSPECT


def test_evaluate_penalizes_suspicious_unknown_brand() -> None:
    opportunity = Opportunity(
        kind=OpportunityKind.SHOPPING_DEAL,
        source="vinted_fixture",
        source_id="unknown-earbuds",
        title="Generic wireless running earbuds",
        url="https://example.test/listing",
        price=5.0,
        currency="EUR",
        location="Bari",
        description="Unknown-brand running wireless earbuds.",
        attributes={
            "brand": "Generic",
            "condition": "new sealed",
            "total_cost": 7.0,
            "estimated_market_value": 30.0,
            "seller_rating": 4.0,
            "seller_reviews": 3,
            "accessories": ["charging case", "ear tips"],
            "water_resistant": True,
            "sport_features": ["running"],
        },
    )

    evaluation = evaluate(opportunity, default_decision_profile(), context={"max_price": 40})

    assert evaluation.action == EvaluationAction.REJECT
    assert "Price is suspiciously low versus the estimated used-market value." in evaluation.risks
    assert "Unknown brand reduces durability and support confidence." in evaluation.risks
