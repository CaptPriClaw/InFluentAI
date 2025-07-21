# agents/trend_predictor.py

import re
from collections import Counter
from datetime import datetime, timedelta

def extract_hashtags_and_keywords(text: str) -> list:
    """
    Extracts hashtags and potential trend keywords from a piece of text.

    Args:
        text (str): Input social media content.

    Returns:
        list: List of lowercase hashtags and keywords (excluding common stopwords).
    """
    hashtags = re.findall(r"#\w+", text)
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())  # words with 4+ chars
    common_stopwords = set([
        "this", "that", "with", "from", "about", "have", "just", "your", "they",
        "what", "when", "where", "which", "their", "will", "there", "some", "like"
    ])
    filtered_keywords = [w for w in words if w not in common_stopwords]
    return [*hashtags, *filtered_keywords]


def predict_trends(contents: list[str], timeframe_hours: int = 48) -> list[tuple[str, int]]:
    """
    Predicts trending hashtags or keywords based on frequency.

    Args:
        contents (list[str]): List of social post contents.
        timeframe_hours (int): Time window to consider for trends (default: 48 hours).

    Returns:
        list[tuple[str, int]]: List of top keywords/hashtags with counts.
    """
    keyword_counter = Counter()

    for content in contents:
        keywords = extract_hashtags_and_keywords(content)
        keyword_counter.update(keywords)

    top_keywords = keyword_counter.most_common(10)
    return top_keywords
