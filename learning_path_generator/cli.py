"""Command-line interface for the Learning Path Generator.

This script parses command-line arguments, retrieves resources using the YouTube
and Medium clients, constructs a learning plan, and prints it in a human-
readable format. You can run it as a module:

```bash
python -m learning_path_generator.cli --skill "React" --youtube-api-key YOUR_KEY
```
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

try:
    from tabulate import tabulate  # type: ignore
except ImportError:
    tabulate = None  # type: ignore

from .learning_path import generate_learning_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a personalised multi-week learning path using YouTube and Medium resources.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--skill",
        required=True,
        help="Skill or topic to learn (e.g. 'React', 'Cryptography').",
    )
    parser.add_argument(
        "--youtube-api-key",
        default=os.environ.get("YOUTUBE_API_KEY", ""),
        help="YouTube Data API key. You can also set the YOUTUBE_API_KEY environment variable.",
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=4,
        help="Number of weeks in the learning plan.",
    )
    parser.add_argument(
        "--videos-per-week",
        type=int,
        default=2,
        help="Number of videos to recommend each week.",
    )
    parser.add_argument(
        "--articles-per-week",
        type=int,
        default=2,
        help="Number of Medium articles to recommend each week.",
    )
    parser.add_argument(
        "--search-order",
        type=str,
        default="relevance",
        help="Ordering for YouTube search results (date, rating, relevance, title, viewCount).",
    )
    parser.add_argument(
        "--no-table",
        action="store_true",
        help="Disable tabular formatting even if the tabulate package is installed.",
    )
    args = parser.parse_args()

    if not args.youtube_api_key:
        parser.error(
            "You must provide a YouTube API key via --youtube-api-key or set the YOUTUBE_API_KEY environment variable."
        )

    # Generate the learning plan
    plan = generate_learning_path(
        skill=args.skill,
        youtube_api_key=args.youtube_api_key,
        weeks=args.weeks,
        videos_per_week=args.videos_per_week,
        articles_per_week=args.articles_per_week,
        search_order=args.search_order,
    )

    # Print the plan
    print_learning_plan(plan, use_table=not args.no_table)


def print_learning_plan(plan: List[dict], use_table: bool = True) -> None:
    """Pretty-print the learning plan to stdout."""
    for week in plan:
        week_num = week["week"]
        theme = week["theme"]
        videos = week["videos"]
        articles = week["articles"]
        activities = week["activities"]
        print(f"\nWeek {week_num}: {theme}")
        # Videos
        if videos:
            print("  Videos:")
            rows = []
            for idx, vid in enumerate(videos, start=1):
                title = vid["title"]
                url = vid["url"]
                duration = vid["duration"] or "--"
                rows.append([str(idx), title, duration, url])
            if tabulate and use_table:
                print(
                    tabulate(
                        rows,
                        headers=["#", "Title", "Duration", "URL"],
                        tablefmt="github",
                    )
                )
            else:
                for row in rows:
                    print(f"    {row[0]}. {row[1]} ({row[2]}) – {row[3]}")
        else:
            print("  Videos: None")
        # Articles
        if articles:
            print("  Articles:")
            rows = []
            for idx, art in enumerate(articles, start=1):
                title = art["title"]
                url = art["url"]
                rows.append([str(idx), title, url])
            if tabulate and use_table:
                print(
                    tabulate(
                        rows,
                        headers=["#", "Title", "URL"],
                        tablefmt="github",
                    )
                )
            else:
                for row in rows:
                    print(f"    {row[0]}. {row[1]} – {row[2]}")
        else:
            print("  Articles: None")
        # Activities
        print("  Suggested activities:")
        print(f"    {activities}")


if __name__ == "__main__":
    main()