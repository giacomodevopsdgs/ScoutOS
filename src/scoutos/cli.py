"""Command-line interface for ScoutOS."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from scoutos.scouts.shopping import RankedOpportunity, search_shopping_fixture


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ScoutOS command-line interface."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "shopping" and args.shopping_command == "search":
        results = search_shopping_fixture(args.query, args.max_price, limit=args.limit)
        _print_shopping_results(args.query, args.max_price, results)
        return 0

    parser.print_help()
    return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="scout", description="ScoutOS local dry-run tools.")
    subparsers = parser.add_subparsers(dest="command")

    shopping_parser = subparsers.add_parser("shopping", help="Run Shopping Scout commands.")
    shopping_subparsers = shopping_parser.add_subparsers(dest="shopping_command")

    search_parser = shopping_subparsers.add_parser(
        "search",
        help="Rank fixture-backed shopping listings.",
    )
    search_parser.add_argument("--query", required=True, help="Search query to match in fixture data.")
    search_parser.add_argument(
        "--max-price",
        required=True,
        type=float,
        help="Maximum total price including shipping.",
    )
    search_parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum ranked candidates to print.",
    )
    return parser


def _print_shopping_results(query: str, max_price: float, results: list[RankedOpportunity]) -> None:
    print(f"Shopping Scout dry run: query='{query}' max_price=EUR {max_price:.2f}")
    print(f"Ranked candidates: {len(results)}")

    if not results:
        print("No fixture listings matched the query and budget.")
        return

    for index, ranked in enumerate(results, start=1):
        opportunity = ranked.opportunity
        total_cost = float(opportunity.attributes["total_cost"])
        shipping_cost = float(opportunity.attributes["shipping_cost"])
        print()
        print(f"{index}. {opportunity.title}")
        print(f"   Score: {ranked.score.total:.2f}/100")
        print(
            "   Price: "
            f"{opportunity.currency} {opportunity.price:.2f} "
            f"+ shipping {opportunity.currency} {shipping_cost:.2f} "
            f"= {opportunity.currency} {total_cost:.2f}"
        )
        print(
            "   Source: "
            f"{opportunity.source} | Location: {opportunity.location or 'unknown'} | "
            f"URL: {opportunity.url}"
        )
        print("   Reasons:")
        for reason in ranked.score.reasons:
            print(f"   - {reason}")


if __name__ == "__main__":
    raise SystemExit(main())
