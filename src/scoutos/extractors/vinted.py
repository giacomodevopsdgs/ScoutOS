"""Vinted extraction scaffold."""

from __future__ import annotations

from collections.abc import AsyncIterator
from urllib.parse import urlencode

from scoutos.extractors.base import Extractor, ExtractorContext
from scoutos.models import ExtractedItem, Opportunity, OpportunityKind


class VintedExtractor(Extractor):
    """Playwright-ready scaffold for Vinted search extraction."""

    source_name = "vinted"

    async def extract(self, context: ExtractorContext) -> AsyncIterator[ExtractedItem]:
        """Yield Vinted items.

        A future implementation should accept a Playwright page or browser context
        through `context.options` and parse listing cards from the search page.
        """

        if False:
            yield _placeholder_item(context.query)
        return


def build_search_url(query: str) -> str:
    """Build a Vinted catalog search URL."""

    params = urlencode({"search_text": query})
    return f"https://www.vinted.com/catalog?{params}"


def normalize_vinted_item(item: ExtractedItem) -> Opportunity:
    """Convert a raw Vinted item into a ScoutOS opportunity."""

    price = item.raw.get("price")
    return Opportunity(
        kind=OpportunityKind.SHOPPING_DEAL,
        source=item.source,
        source_id=item.source_id,
        title=item.title,
        url=item.url,
        price=float(price) if price is not None else None,
        currency=item.raw.get("currency"),
        location=item.raw.get("location"),
        description=item.raw.get("description"),
        attributes=item.raw,
        observed_at=item.extracted_at,
    )


def _placeholder_item(query: str) -> ExtractedItem:
    return ExtractedItem(
        source=VintedExtractor.source_name,
        source_id="placeholder",
        url=build_search_url(query),
        title=query,
    )
