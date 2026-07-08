from __future__ import annotations

from scoutos.cli import main
from scoutos.scouts.shopping import extract_fixture_items, search_shopping_fixture


def test_extract_fixture_items_matches_query() -> None:
    items = extract_fixture_items("frullatore")

    assert len(items) == 6
    assert all("frullatore" in item.title.casefold() for item in items)


def test_search_shopping_fixture_filters_over_max_price_and_ranks_top_three() -> None:
    results = search_shopping_fixture("frullatore", 60)

    assert [result.opportunity.source_id for result in results] == [
        "vinted-frullatore-001",
        "vinted-frullatore-002",
        "vinted-frullatore-003",
    ]
    assert all(result.opportunity.attributes["total_cost"] <= 60 for result in results)
    assert results[0].score.total > results[1].score.total > results[2].score.total


def test_cli_prints_ranked_candidates(capsys) -> None:
    exit_code = main(["shopping", "search", "--query", "frullatore", "--max-price", "60"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Shopping Scout dry run: query='frullatore' max_price=EUR 60.00" in output
    assert "1. Nutribullet 600 frullatore compatto" in output
    assert "Score:" in output
    assert "Reasons:" in output
