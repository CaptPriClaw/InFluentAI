import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

def prepare_trend_data(df, topic_column='predicted_topic', date_column='timestamp'):
    """
    Prepares a time series dataset of topic frequencies over time.
    Returns a pivot table with dates as index and topics as columns.
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df['date'] = df[date_column].dt.date
    trend_data = df.groupby(['date', topic_column]).size().unstack(fill_value=0)
    return trend_data


def forecast_topic_trend(trend_df, forecast_days=7):
    """
    Forecasts the frequency of each topic over the next N days using linear regression.
    Returns a DataFrame with predicted values.
    """
    future_forecasts = pd.DataFrame()
    for topic in trend_df.columns:
        topic_series = trend_df[topic].values
        X = np.arange(len(topic_series)).reshape(-1, 1)
        y = topic_series

        model = LinearRegression()
        model.fit(X, y)

        future_X = np.arange(len(topic_series), len(topic_series) + forecast_days).reshape(-1, 1)
        y_pred = model.predict(future_X)
        y_pred = np.clip(y_pred, 0, None).astype(int)  # ensure no negative values

        forecast_dates = [trend_df.index[-1] + timedelta(days=i+1) for i in range(forecast_days)]
        future_forecasts[topic] = pd.Series(y_pred, index=forecast_dates)

    return future_forecasts


def get_top_rising_trends(forecast_df, top_n=5):
    """
    Identifies the top N rising trends based on predicted growth rate.
    """
    growth = forecast_df.iloc[-1] - forecast_df.iloc[0]
    top_trends = growth.sort_values(ascending=False).head(top_n)
    return top_trends.reset_index().rename(columns={0: 'predicted_increase', 'index': 'topic'})
