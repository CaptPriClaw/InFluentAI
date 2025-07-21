import sqlite3
from datetime import datetime

DB_NAME = "influentsight.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Posts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            influencer TEXT,
            platform TEXT,
            content TEXT,
            timestamp TEXT,
            url TEXT
        )
    ''')

    # Summaries table
    c.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            post_id INTEGER,
            summary TEXT,
            sentiment TEXT,
            topic TEXT,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    ''')

    # Trend history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS trend_forecast (
            date TEXT,
            topic TEXT,
            predicted_count INTEGER
        )
    ''')

    conn.commit()
    conn.close()


def insert_post(influencer, platform, content, timestamp, url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO posts (influencer, platform, content, timestamp, url)
        VALUES (?, ?, ?, ?, ?)
    ''', (influencer, platform, content, timestamp, url))
    post_id = c.lastrowid
    conn.commit()
    conn.close()
    return post_id


def insert_summary(post_id, summary, sentiment, topic):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO summaries (post_id, summary, sentiment, topic)
        VALUES (?, ?, ?, ?)
    ''', (post_id, summary, sentiment, topic))
    conn.commit()
    conn.close()


def insert_trend_forecast(date, topic, predicted_count):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO trend_forecast (date, topic, predicted_count)
        VALUES (?, ?, ?)
    ''', (date, topic, predicted_count))
    conn.commit()
    conn.close()


def get_recent_posts(limit=100):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT posts.id, influencer, platform, content, timestamp, url, summary, sentiment, topic
        FROM posts
        LEFT JOIN summaries ON posts.id = summaries.post_id
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_trend_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM trend_forecast ORDER BY date
    ''')
    rows = c.fetchall()
    conn.close()
    return rows
