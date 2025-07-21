import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import json
import pandas as pd
from analytics.charts import display_trend_chart
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="InFluentAI", layout="wide")

st.title("📲 InFluentAI")
st.markdown("Track influencer content, summarize it, and stay ahead of trends — every 48 hours.")

# Load influencer list
with open("data/influencers_list.json") as f:
    influencers = json.load(f)

with open("data/platform_map.json") as f:
    platforms = json.load(f)

col1, col2 = st.columns(2)

with col1:
    influencer_names = [inf["name"] for inf in influencers]
    selected_name = st.selectbox("Select Influencer", influencer_names)

with col2:
    selected_platform = st.selectbox("Select Platform", platforms)

# Trigger backend API
if st.button("🚀 Analyze Now"):
    with st.spinner("Running full analysis..."):
        try:
            res = requests.post("http://localhost:8000/process/", json={
                "name": selected_name,
                "platform": selected_platform
            })
            if res.status_code == 200:
                st.success(f"✅ Analysis started for {selected_name} on {selected_platform}. Refresh in a while.")
            else:
                st.error("❌ Something went wrong with the backend.")
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend server not running at http://localhost:8000")

st.markdown("---")
st.subheader("🔍 Last Analysis Results")

sample_results = {
    "summary": "The influencer discussed AI in daily productivity apps, hinting at a new tool launch.",
    "sentiment": {
        "overall_sentiment": "Positive",
        "score": 0.82
    },
    "predicted_trend": [
        "AI Personal Assistants",
        "No-Code Automation",
        "Creator Tools"
    ],
    "forecast": {
        "AI Personal Assistants": "Upward",
        "No-Code Automation": "Stable",
        "Creator Tools": "Upward"
    }
}

with st.expander("🧾 Summary"):
    st.write(sample_results["summary"])

with st.expander("📊 Sentiment Analysis"):
    sentiment = sample_results["sentiment"]
    st.metric(label="Overall Sentiment", value=sentiment["overall_sentiment"])
    st.metric(label="Confidence Score", value=round(sentiment["score"] * 100, 2))

with st.expander("📈 Predicted Trends"):
    for trend in sample_results["predicted_trend"]:
        st.markdown(f"- {trend}")

with st.expander("🔮 Trend Forecast"):
    for topic, direction in sample_results["forecast"].items():
        emoji = "📈" if direction == "Upward" else "➡️" if direction == "Stable" else "📉"
        st.write(f"{emoji} **{topic}** → {direction}")

st.markdown("---")
st.subheader("📉 Visual Forecast")

# 👇 Mock Data for Chart (until real results are loaded from DB)
mock_df = pd.DataFrame({
    "influencer": [selected_name] * 5,
    "timestamp": pd.date_range(end=pd.Timestamp.today(), periods=5).tolist(),
    "sentiment_score": [0.7, 0.65, 0.8, 0.75, 0.82]
})

# Correctly pass influencer_name and df
fig = display_trend_chart(mock_df, selected_name)
st.pyplot(fig)
