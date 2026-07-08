"""Minimal deterministic evaluation layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from scoutos.models import Opportunity


class EvaluationAction(StrEnum):
    """Recommended next action for an evaluated opportunity."""

    BUY = "buy"
    INSPECT = "inspect"
    NEGOTIATE = "negotiate"
    WAIT = "wait"
    REJECT = "reject"


@dataclass(frozen=True)
class DecisionProfile:
    """Small explainable profile for deterministic opportunity evaluation."""

    name: str = "default"
    sustainability_weight: float = 8.0
    used_market_preference: float = 8.0
    durability_weight: float = 16.0
    repairability_weight: float = 6.0
    sport_fit_weight: float = 8.0
    minimalism_weight: float = 8.0
    completeness_weight: float = 14.0
    condition_weight: float = 10.0
    seller_reliability_weight: float = 12.0
    local_pickup_weight: float = 4.0
    preferred_brands: frozenset[str] = frozenset(
        {"jabra", "sony", "soundcore", "jbl", "beats", "tozo"}
    )
    durable_brands: frozenset[str] = frozenset(
        {"jabra", "sony", "soundcore", "jbl", "beats"}
    )
    repairable_brands: frozenset[str] = frozenset({"jabra", "sony", "soundcore"})
    sport_oriented_terms: frozenset[str] = frozenset(
        {"active", "sport", "endurance", "running", "wing", "ear hook", "ip57", "ipx7"}
    )
    required_accessories: frozenset[str] = frozenset({"charging case", "ear tips"})
    minimum_seller_rating: float = 4.5
    suspicious_price_ratio: float = 0.35


@dataclass(frozen=True)
class Evaluation:
    """Evaluation result for an opportunity against a decision profile."""

    score: float
    action: EvaluationAction
    reasons: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    confidence: float = 0.0
    components: dict[str, float] = field(default_factory=dict)


def default_decision_profile() -> DecisionProfile:
    """Return the single default profile used by the first vertical slices."""

    return DecisionProfile()


def evaluate(
    opportunity: Opportunity,
    decision_profile: DecisionProfile,
    context: dict[str, Any] | None = None,
) -> Evaluation:
    """Evaluate an opportunity with deterministic profile-aware rules."""

    context = context or {}
    max_price = _optional_float(context.get("max_price"))
    components = {
        "budget_value": _score_budget_value(opportunity, max_price),
        "sustainability": _score_sustainability(opportunity, decision_profile),
        "durability": _score_durability(opportunity, decision_profile),
        "repairability": _score_repairability(opportunity, decision_profile),
        "sport_fit": _score_sport_fit(opportunity, decision_profile),
        "minimalism": _score_minimalism(opportunity, decision_profile),
        "completeness": _score_completeness(opportunity, decision_profile),
        "condition": _score_condition(opportunity, decision_profile),
        "seller_reliability": _score_seller_reliability(opportunity, decision_profile),
        "local_pickup": _score_local_pickup(opportunity, decision_profile),
        "risk_penalty": _score_risk_penalty(opportunity, decision_profile, max_price),
    }
    score = round(max(0.0, min(100.0, sum(components.values()))), 2)
    risks = _risks(opportunity, decision_profile, max_price)
    action = _action_for(score, risks)
    return Evaluation(
        score=score,
        action=action,
        reasons=_reasons(opportunity, decision_profile, components),
        risks=risks,
        confidence=_confidence(opportunity),
        components=components,
    )


def _score_budget_value(opportunity: Opportunity, max_price: float | None) -> float:
    total_cost = _total_cost(opportunity)
    if total_cost is None:
        return 0.0
    if max_price is None or max_price <= 0:
        return 20.0
    if total_cost > max_price:
        overage_ratio = (total_cost - max_price) / max_price
        return max(0.0, 16.0 - (overage_ratio * 40.0))
    headroom_ratio = (max_price - total_cost) / max_price
    return round(22.0 + (headroom_ratio * 18.0), 2)


def _score_sustainability(opportunity: Opportunity, profile: DecisionProfile) -> float:
    source = opportunity.source.casefold()
    condition = str(opportunity.attributes.get("condition", "")).casefold()
    if "fixture" in source or "vinted" in source:
        return profile.used_market_preference
    if "nuovo" not in condition:
        return profile.sustainability_weight
    return profile.sustainability_weight / 2


def _score_durability(opportunity: Opportunity, profile: DecisionProfile) -> float:
    brand = str(opportunity.attributes.get("brand", "")).casefold()
    if brand in profile.durable_brands:
        return profile.durability_weight
    if brand in profile.preferred_brands:
        return profile.durability_weight * 0.6
    return 0.0


def _score_repairability(opportunity: Opportunity, profile: DecisionProfile) -> float:
    brand = str(opportunity.attributes.get("brand", "")).casefold()
    if bool(opportunity.attributes.get("replacement_parts_available")):
        return profile.repairability_weight
    if brand in profile.repairable_brands:
        return profile.repairability_weight * 0.75
    return 0.0


def _score_sport_fit(opportunity: Opportunity, profile: DecisionProfile) -> float:
    haystack = _haystack(opportunity)
    if any(term in haystack for term in profile.sport_oriented_terms):
        return profile.sport_fit_weight
    if bool(opportunity.attributes.get("water_resistant")):
        return profile.sport_fit_weight * 0.5
    return 0.0


def _score_minimalism(opportunity: Opportunity, profile: DecisionProfile) -> float:
    brand = str(opportunity.attributes.get("brand", "")).casefold()
    accessories = _accessories(opportunity)
    required_accessories = _required_accessories(opportunity, profile)
    if brand in profile.durable_brands and required_accessories <= accessories:
        return profile.minimalism_weight
    if brand in profile.preferred_brands:
        return profile.minimalism_weight * 0.6
    return 0.0


def _score_completeness(opportunity: Opportunity, profile: DecisionProfile) -> float:
    missing = _required_accessories(opportunity, profile) - _accessories(opportunity)
    if not missing:
        return profile.completeness_weight
    return max(0.0, profile.completeness_weight - (6.0 * len(missing)))


def _score_condition(opportunity: Opportunity, profile: DecisionProfile) -> float:
    condition = str(opportunity.attributes.get("condition", "")).casefold()
    condition_scores = {
        "new sealed": profile.condition_weight,
        "like new": profile.condition_weight,
        "excellent": profile.condition_weight * 0.9,
        "good": profile.condition_weight * 0.7,
        "fair": profile.condition_weight * 0.4,
        "poor": 0.0,
    }
    return condition_scores.get(condition, profile.condition_weight * 0.5)


def _score_seller_reliability(opportunity: Opportunity, profile: DecisionProfile) -> float:
    rating = _optional_float(opportunity.attributes.get("seller_rating")) or 0.0
    reviews = int(opportunity.attributes.get("seller_reviews", 0))
    rating_score = min(8.0, max(0.0, (rating - 4.0) * 8.0))
    review_score = 4.0 if reviews >= 50 else 2.0 if reviews >= 15 else 0.0
    score = rating_score + review_score
    if rating < profile.minimum_seller_rating:
        score -= 2.0
    return round(max(0.0, min(profile.seller_reliability_weight, score)), 2)


def _score_local_pickup(opportunity: Opportunity, profile: DecisionProfile) -> float:
    if bool(opportunity.attributes.get("local_pickup")):
        return profile.local_pickup_weight
    return 0.0


def _score_risk_penalty(
    opportunity: Opportunity,
    profile: DecisionProfile,
    max_price: float | None,
) -> float:
    penalty = 0.0
    if _is_suspiciously_cheap(opportunity, profile):
        penalty -= 18.0
    if _is_unknown_brand(opportunity, profile):
        penalty -= 12.0
    if _is_poor_condition(opportunity):
        penalty -= 15.0
    total_cost = _total_cost(opportunity)
    if max_price is not None and total_cost is not None and total_cost > max_price:
        penalty -= 12.0
    return penalty


def _reasons(
    opportunity: Opportunity,
    profile: DecisionProfile,
    components: dict[str, float],
) -> list[str]:
    reasons = [f"Evaluated with the {profile.name} decision profile."]
    total_cost = _total_cost(opportunity)
    if total_cost is not None:
        reasons.append(f"Total estimated cost is {opportunity.currency} {total_cost:.2f}.")
    if components["sustainability"] >= profile.used_market_preference:
        reasons.append("Used-market listing fits the sustainability preference.")
    if components["durability"] >= profile.durability_weight:
        reasons.append("Brand matches the durability preference.")
    if components["repairability"] > 0:
        reasons.append("Replacement parts or brand support improve repairability.")
    if components["sport_fit"] >= profile.sport_fit_weight:
        reasons.append("Sport-oriented design fits running use.")
    if components["minimalism"] >= profile.minimalism_weight:
        reasons.append("Complete durable item supports the minimalism preference.")
    if components["completeness"] >= profile.completeness_weight:
        reasons.append("Includes the required accessories to verify.")
    if components["local_pickup"] > 0:
        reasons.append("Local pickup reduces shipping uncertainty and impact.")
    if components["seller_reliability"] >= profile.seller_reliability_weight * 0.75:
        reasons.append("Seller signals are strong enough for a used purchase.")
    return reasons


def _risks(
    opportunity: Opportunity,
    profile: DecisionProfile,
    max_price: float | None,
) -> list[str]:
    risks: list[str] = []
    total_cost = _total_cost(opportunity)
    if max_price is not None and total_cost is not None and total_cost > max_price:
        risks.append("Total cost is above the configured budget.")
    missing_accessories = _required_accessories(opportunity, profile) - _accessories(opportunity)
    if missing_accessories:
        missing = ", ".join(sorted(missing_accessories))
        risks.append(f"Missing required accessory verification: {missing}.")
    if _is_suspiciously_cheap(opportunity, profile):
        risks.append("Price is suspiciously low versus the estimated used-market value.")
    if _is_unknown_brand(opportunity, profile):
        risks.append("Unknown brand reduces durability and support confidence.")
    if _is_poor_condition(opportunity):
        risks.append("Poor condition creates hygiene, battery, or reliability risk.")
    rating = _optional_float(opportunity.attributes.get("seller_rating"))
    if rating is None or rating < profile.minimum_seller_rating:
        risks.append("Seller rating is below the default confidence threshold.")
    if not opportunity.description:
        risks.append("Description is missing, so condition confidence is lower.")
    return risks


def _action_for(score: float, risks: list[str]) -> EvaluationAction:
    if any("Unknown brand" in risk or "Poor condition" in risk for risk in risks):
        return EvaluationAction.REJECT if score < 55 else EvaluationAction.WAIT
    if any("suspiciously low" in risk for risk in risks):
        return EvaluationAction.INSPECT if score >= 55 else EvaluationAction.REJECT
    if score < 40:
        return EvaluationAction.REJECT
    if score < 55:
        return EvaluationAction.WAIT
    if any("Missing required accessory" in risk for risk in risks):
        return EvaluationAction.INSPECT if score >= 65 else EvaluationAction.NEGOTIATE
    if score >= 82:
        return EvaluationAction.BUY
    if score >= 68:
        return EvaluationAction.INSPECT
    return EvaluationAction.NEGOTIATE


def _confidence(opportunity: Opportunity) -> float:
    fields = [
        opportunity.title,
        opportunity.url,
        opportunity.price,
        opportunity.location,
        opportunity.description,
        opportunity.attributes.get("condition"),
        opportunity.attributes.get("seller_rating"),
        opportunity.attributes.get("accessories"),
        opportunity.attributes.get("condition"),
        opportunity.attributes.get("estimated_market_value"),
    ]
    present = sum(value is not None and value != "" and value != [] for value in fields)
    return round(min(0.95, 0.35 + (present / len(fields) * 0.6)), 2)


def _total_cost(opportunity: Opportunity) -> float | None:
    total_cost = opportunity.attributes.get("total_cost", opportunity.price)
    return _optional_float(total_cost)


def _accessories(opportunity: Opportunity) -> set[str]:
    return {
        str(accessory).casefold()
        for accessory in opportunity.attributes.get("accessories", [])
    }


def _required_accessories(opportunity: Opportunity, profile: DecisionProfile) -> frozenset[str]:
    if opportunity.attributes.get("form_factor") == "neckband":
        return frozenset({"charging cable", "ear tips"})
    return profile.required_accessories


def _haystack(opportunity: Opportunity) -> str:
    values = [
        opportunity.title,
        str(opportunity.attributes.get("model", "")),
        str(opportunity.attributes.get("sport_features", "")),
        str(opportunity.attributes.get("water_resistance", "")),
    ]
    return " ".join(values).casefold()


def _is_suspiciously_cheap(opportunity: Opportunity, profile: DecisionProfile) -> bool:
    total_cost = _total_cost(opportunity)
    market_value = _optional_float(opportunity.attributes.get("estimated_market_value"))
    if total_cost is None or market_value is None or market_value <= 0:
        return False
    return total_cost < market_value * profile.suspicious_price_ratio


def _is_unknown_brand(opportunity: Opportunity, profile: DecisionProfile) -> bool:
    brand = str(opportunity.attributes.get("brand", "")).casefold()
    return brand not in profile.preferred_brands


def _is_poor_condition(opportunity: Opportunity) -> bool:
    return str(opportunity.attributes.get("condition", "")).casefold() == "poor"


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
