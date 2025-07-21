import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from agents.handle_scraper import scrape_content
from agents.content_summarizer import generate_summary
from agents.sentiment_analyzer import analyze_sentiment
from agents.trend_predictor import predict_trends
from analytics.trend_forecaster import forecast_trend
from backend.db import save_to_db


app = FastAPI(
    title="InFluentAI Backend",
    description="API for influencer monitoring and trend summarization",
    version="1.0.0"
)

class InfluencerRequest(BaseModel):
    name: str
    platform: str

@app.post("/process/")
async def process_influencer(req: InfluencerRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to initiate full influencer processing.
    """
    background_tasks.add_task(full_pipeline, req.name, req.platform)
    return {"status": "Processing started", "influencer": req.name}

@app.get("/")
def read_root():
    return {"message": "Welcome to InFluentAI backend!"}

async def full_pipeline(name: str, platform: str):
    """
    Executes the full processing pipeline.
    """
    content = scrape_content(name, platform)
    if not content:
        print(f"[WARN] No content found for {name} on {platform}")
        return

    summary = generate_summary(content)
    sentiment = analyze_sentiment(content)
    predicted_trend = predict_trends(summary)
    forecast = forecast_trend(summary)

    save_to_db({
        "name": name,
        "platform": platform,
        "summary": summary,
        "sentiment": sentiment,
        "predicted_trend": predicted_trend,
        "forecast": forecast
    })

# ✅ RUN with this from terminal (not from here):
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
