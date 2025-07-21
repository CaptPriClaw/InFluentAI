import time
import schedule
from agents.handle_scraper import scrape_all_influencers
from agents.content_summarizer import summarize_post
from agents.sentiment_analyzer import analyze_sentiment
from agents.trend_predictor import predict_trends
from backend.db import (
    insert_post, insert_summary, insert_trend_forecast, init_db
)

# Optional: Email notification
from notifications.send_email import send_summary_email


def pipeline_run():
    print("[INFO] Starting scheduled pipeline...")

    # Step 1: Scrape posts
    all_posts = scrape_all_influencers()
    print(f"[INFO] Scraped {len(all_posts)} posts.")

    for post in all_posts:
        influencer = post['influencer']
        platform = post['platform']
        content = post['content']
        timestamp = post['timestamp']

        # Step 2: Store post in DB
        post_id = insert_post(influencer, platform, content, timestamp)

        # Step 3: Summarize content
        summary = summarize_post(content)

        # Step 4: Analyze sentiment and extract topic
        sentiment, topic = analyze_sentiment(content)

        # Step 5: Save summary & sentiment
        insert_summary(post_id, summary, sentiment, topic)

    # Step 6: Trend prediction based on latest data
    forecast = predict_trends()
    insert_trend_forecast(forecast)
    print("[INFO] Forecast saved.")

    # Step 7: Notify via email (optional)
    send_summary_email(forecast)

    print("[INFO] Pipeline completed.\n")


def schedule_pipeline():
    init_db()  # Ensure tables exist
    pipeline_run()  # Run immediately on start

    # Schedule every 48 hours
    schedule.every(48).hours.do(pipeline_run)

    print("[INFO] Scheduler is running every 48 hours.")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    schedule_pipeline()
