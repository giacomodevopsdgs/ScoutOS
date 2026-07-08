from __future__ import annotations

from scoutos.cli import main
from scoutos.scouts.shopping import extract_fixture_items, search_shopping_fixture


def test_extract_fixture_items_matches_query() -> None:
    items = extract_fixture_items("running wireless earbuds")

    assert len(items) == 10
    assert all("running" in item.raw["category"] for item in items)


def test_search_shopping_fixture_filters_over_max_price_and_uses_evaluation() -> None:
    results = search_shopping_fixture("running wireless earbuds", 40)

    assert [result.opportunity.source_id for result in results] == [
        "earbuds-001",
        "earbuds-003",
        "earbuds-002",
    ]
    assert all(result.opportunity.attributes["total_cost"] <= 40 for result in results)
    assert results[0].evaluation.score > results[1].evaluation.score > results[2].evaluation.score
    assert results[0].evaluation.reasons[0] == "Evaluated with the default decision profile."


def test_cli_prints_ranked_candidates_with_evaluation(capsys) -> None:
    exit_code = main(
        ["shopping", "search", "--query", "running wireless earbuds", "--max-price", "40"]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Shopping Scout dry run: query='running wireless earbuds' max_price=EUR 40.00" in output
    assert "1. Jabra Elite 4 Active wireless earbuds" in output
    assert "Score:" in output
    assert "Action:" in output
    assert "Confidence:" in output
    assert "Reasons:" in output
    assert "Risks:" in output
