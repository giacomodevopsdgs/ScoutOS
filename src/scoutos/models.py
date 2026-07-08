"""Shared data models for ScoutOS."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class OpportunityKind(StrEnum):
    """Supported opportunity domains."""

    SHOPPING_DEAL = "shopping_deal"
    JOB_OPENING = "job_opening"
    TRAVEL = "travel"
    REAL_ESTATE = "real_estate"
    EVENT = "event"
    PRICE_TRACKING = "price_tracking"


@dataclass(frozen=True)
class ExtractedItem:
    """Raw structured data emitted by a source extractor."""

    source: str
    source_id: str
    url: str
    title: str
    raw: dict[str, Any] = field(default_factory=dict)
    extracted_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class Opportunity:
    """Normalized candidate item ready for scoring and persistence."""

    kind: OpportunityKind
    source: str
    source_id: str
    title: str
    url: str
    price: float | None = None
    currency: str | None = None
    location: str | None = None
    description: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    observed_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class ScoreBreakdown:
    """Transparent scoring result for an opportunity."""

    total: float
    components: dict[str, float]
    reasons: list[str] = field(default_factory=list)
