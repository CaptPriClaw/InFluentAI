# agents/sentiment_analyzer.py

from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    """
    Analyzes the sentiment of the given text.

    Args:
        text (str): Input text to analyze.

    Returns:
        dict: A dictionary with polarity score, sentiment label.
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {
            "polarity": polarity,
            "sentiment": sentiment
        }
    except Exception as e:
        print(f"[ERROR] Sentiment analysis failed: {e}")
        return {
            "polarity": 0.0,
            "sentiment": "Unknown"
        }
