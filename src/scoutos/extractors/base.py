"""Base extractor contracts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from scoutos.models import ExtractedItem


@dataclass(frozen=True)
class ExtractorContext:
    """Runtime context passed to extractors."""

    query: str
    options: dict[str, Any] = field(default_factory=dict)


class Extractor(ABC):
    """Async extraction interface for HTTP, feed, API, or Playwright sources."""

    source_name: str

    @abstractmethod
    async def extract(self, context: ExtractorContext) -> AsyncIterator[ExtractedItem]:
        """Yield extracted source items."""
