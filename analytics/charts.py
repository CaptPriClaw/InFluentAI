import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

def display_trend_chart(df, influencer_name=None):
    """
    Generates a line chart showing sentiment scores over time.
    If influencer_name is provided, filters the data accordingly.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    if influencer_name:
        df = df[df['influencer'] == influencer_name]
        title = f"Sentiment Trend for {influencer_name}"
    else:
        title = "Overall Sentiment Trend"

    if df.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.text(0.5, 0.5, 'No data available.', horizontalalignment='center', verticalalignment='center')
        return fig

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x='timestamp', y='sentiment_score', marker='o', ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Sentiment Score")
    ax.grid(True)

    return fig

def generate_platform_distribution(df):
    """
    Pie chart showing the distribution of content across platforms.
    """
    platform_counts = df['platform'].value_counts()
    fig = px.pie(values=platform_counts.values, names=platform_counts.index, title="Platform Distribution of Posts")
    return fig

def generate_trend_frequency_chart(df, top_n=10):
    """
    Bar chart for most frequent keywords/topics used.
    """
    topic_counts = df['predicted_topic'].value_counts().nlargest(top_n)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=topic_counts.values, y=topic_counts.index, palette="viridis", ax=ax)
    ax.set_title("Top Trending Topics")
    ax.set_xlabel("Frequency")
    return fig

def fig_to_base64(fig):
    """
    Converts a Matplotlib figure to a base64-encoded PNG for embedding in web apps.
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image_base64
