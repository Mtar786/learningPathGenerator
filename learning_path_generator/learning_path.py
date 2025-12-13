"""Learning path generation logic.

This module defines a function to assemble a multi‑week learning plan by
combining resources retrieved from YouTube and Medium. The plan divides the
content into equal weekly segments and assigns generic themes and suggested
activities.
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from . import youtube_client, medium_client


def generate_learning_path(
    skill: str,
    youtube_api_key: str,
    weeks: int = 4,
    videos_per_week: int = 2,
    articles_per_week: int = 2,
    search_order: str = "relevance",
) -> List[Dict[str, object]]:
    """Generate a structured learning plan for the given skill.

    Parameters
    ----------
    skill: str
        The topic or technology to learn, e.g. "React" or "Cryptography".
    youtube_api_key: str
        API key for the YouTube Data API.
    weeks: int, optional
        Number of weeks in the plan. Default is 4.
    videos_per_week: int, optional
        Number of video recommendations per week. Default is 2.
    articles_per_week: int, optional
        Number of article recommendations per week. Default is 2.
    search_order: str, optional
        Ordering of YouTube search results. See the YouTube API docs for
        acceptable values (e.g. 'relevance', 'viewCount', 'date').

    Returns
    -------
    list of dict
        A list where each element corresponds to a week and contains keys:
        'week', 'theme', 'videos', 'articles', 'activities'.
    """
    # Total resources to fetch
    total_videos = weeks * videos_per_week
    total_articles = weeks * articles_per_week
    # Search for videos on YouTube
    # Add the keyword 'tutorial' to the query to improve relevance
    video_query = f"{skill} tutorial"
    videos = youtube_client.search_videos(
        api_key=youtube_api_key,
        query=video_query,
        max_results=total_videos,
        order=search_order,
    )
    # Fetch Medium articles
    # Convert spaces to hyphens and lowercase for tag slug
    tag_slug = re.sub(r"\s+", "-", skill.strip().lower())
    articles = medium_client.get_articles_for_tag(tag_slug, max_articles=total_articles)
    # Fill lists to required length (repeat if necessary)
    if not videos:
        videos = []
    if not articles:
        articles = []
    # Repeat resources if there are not enough items
    while len(videos) < total_videos and videos:
        videos.extend(videos)
    while len(articles) < total_articles and articles:
        articles.extend(articles)
    videos = videos[:total_videos]
    articles = articles[:total_articles]
    # Generic themes for weeks (can be customised)
    default_themes = [
        "Foundations",
        "Core Concepts",
        "Advanced Topics",
        "Project & Practice",
    ]
    # Build plan
    plan: List[Dict[str, object]] = []
    for week_num in range(weeks):
        week_videos = videos[week_num * videos_per_week : (week_num + 1) * videos_per_week]
        week_articles = articles[week_num * articles_per_week : (week_num + 1) * articles_per_week]
        theme = default_themes[week_num] if week_num < len(default_themes) else f"Week {week_num + 1}"
        activities = _suggest_activities(week_num, skill)
        plan.append(
            {
                "week": week_num + 1,
                "theme": theme,
                "videos": week_videos,
                "articles": week_articles,
                "activities": activities,
            }
        )
    return plan


def _suggest_activities(week_index: int, skill: str) -> str:
    """Return suggested practice activities for a given week index."""
    if week_index == 0:
        return (
            f"Set up your environment for {skill}. Work through basic examples "
            "covered in the videos and summarise the key concepts in your own words."
        )
    elif week_index == 1:
        return (
            f"Experiment with building small components or programs using {skill}. "
            "Complete exercises from articles and implement variations."
        )
    elif week_index == 2:
        return (
            f"Apply what you’ve learned to a mini‑project. Focus on more advanced features "
            "and read deeper resources."
        )
    else:
        return (
            f"Develop a capstone project incorporating multiple concepts of {skill}. "
            "Write a blog post or create a video summarising your project and share it."
        )
