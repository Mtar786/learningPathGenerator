"""YouTube Data API client helper.

This module handles querying the YouTube Data API v3 for videos related to a
particular skill. It searches for videos using the `search.list` endpoint with
the `q` query, restricts results to videos, and retrieves additional details
such as duration via the `videos.list` endpoint.

To use this module you need a valid API key with the YouTube Data API enabled.
See the project README for instructions.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import googleapiclient.discovery
import googleapiclient.errors
import isodate


def search_videos(
    api_key: str,
    query: str,
    max_results: int = 10,
    order: str = "relevance",
) -> List[Dict[str, str]]:
    """Search for videos matching the query term.

    Parameters
    ----------
    api_key: str
        YouTube Data API key (not OAuth). The API key must be enabled for
        the YouTube Data API in your Google Cloud project.
    query: str
        Search term. The API’s `q` parameter specifies the query term【674794175442299†L360-L370】.
        You can use Boolean operators (e.g. "React tutorial|guide -redux").
    max_results: int, optional
        Number of search results to return. The API supports 0–50; default 10【674794175442299†L315-L318】.
    order: str, optional
        Ordering of results. Acceptable values include 'date', 'rating',
        'relevance' (default), 'title', 'viewCount'【674794175442299†L331-L344】.

    Returns
    -------
    list of dict
        Each dictionary contains keys: 'title', 'channel', 'video_id', 'url',
        'published_at', and 'duration' (ISO 8601 duration).
    """
    # Build YouTube service using the API key (no OAuth required)
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key, cache_discovery=False
    )
    try:
        # Search for videos
        search_response = (
            youtube.search()
            .list(
                part="snippet",
                q=query,
                type="video",  # restrict results to videos【674794175442299†L478-L488】
                maxResults=max_results,
                order=order,
            )
            .execute()
        )
    except googleapiclient.errors.HttpError as exc:
        print(f"YouTube API error: {exc}")
        return []

    items = search_response.get("items", [])
    if not items:
        return []
    # Collect video IDs
    video_ids = [item["id"]["videoId"] for item in items]
    # Fetch durations
    durations: Dict[str, str] = {}
    try:
        video_response = (
            youtube.videos()
            .list(part="contentDetails", id=",".join(video_ids))
            .execute()
        )
        for vid in video_response.get("items", []):
            vid_id = vid["id"]
            duration = vid["contentDetails"]["duration"]  # ISO 8601
            durations[vid_id] = duration
    except googleapiclient.errors.HttpError:
        # If this call fails, we still return videos without durations
        pass

    results: List[Dict[str, str]] = []
    for item in items:
        vid_id = item["id"]["videoId"]
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        channel = snippet.get("channelTitle", "")
        published_at = snippet.get("publishedAt", "")
        url = f"https://www.youtube.com/watch?v={vid_id}"
        duration_iso = durations.get(vid_id)
        # Convert duration to human‑readable minutes
        duration_str = ""
        if duration_iso:
            try:
                duration_td = isodate.parse_duration(duration_iso)
                minutes = int(duration_td.total_seconds() // 60)
                seconds = int(duration_td.total_seconds() % 60)
                duration_str = f"{minutes}:{seconds:02d}"
            except (ValueError, TypeError):
                duration_str = duration_iso
        results.append(
            {
                "title": title,
                "channel": channel,
                "video_id": vid_id,
                "url": url,
                "published_at": published_at,
                "duration": duration_str,
            }
        )
    return results
