"""Medium RSS feed client helper.

Medium doesn’t provide a public search API, but it exposes RSS feeds for tags,
users, and publications. This module fetches articles for a given tag from
Medium using the feed URL `https://medium.com/feed/tag/<tag-name>`【574958521376438†L27-L39】.

Note: Stories behind the Medium paywall are not available as full stories in
the RSS feed【574958521376438†L22-L24】.
"""

from __future__ import annotations

from typing import Dict, List

import feedparser


def get_articles_for_tag(tag: str, max_articles: int = 10) -> List[Dict[str, str]]:
    """Return a list of recent Medium articles for a specific tag.

    Parameters
    ----------
    tag: str
        The tag (without the '#' symbol). For example: 'react' or 'cryptography'.
    max_articles: int, optional
        Maximum number of articles to return. Default is 10.

    Returns
    -------
    list of dict
        Each dictionary contains keys: 'title', 'url', 'published', and
        'summary'. If fewer than ``max_articles`` are available, all entries
        are returned.
    """
    feed_url = f"https://medium.com/feed/tag/{tag}"
    parsed = feedparser.parse(feed_url)
    articles: List[Dict[str, str]] = []
    for entry in parsed.entries[:max_articles]:
        title = entry.get("title", "")
        url = entry.get("link", "")
        published = entry.get("published", "") or entry.get("updated", "")
        summary = entry.get("summary", "")
        articles.append(
            {
                "title": title,
                "url": url,
                "published": published,
                "summary": summary,
            }
        )
    return articles
