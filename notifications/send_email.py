import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVERS", "").split(",")  # comma-separated list


def send_summary_email(forecast_data):
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_RECEIVERS:
        print("[WARN] Email credentials or recipients not set. Skipping email.")
        return

    subject = "📊 InFluentAI: New Trend Forecast Update"
    body = "<h2>Here are the latest influencer trend insights:</h2><ul>"

    for topic, score in forecast_data.items():
        body += f"<li><strong>{topic}:</strong> Trending Score - {score}</li>"
    body += "</ul><p>— InFluentAI Bot</p>"

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = ", ".join(EMAIL_RECEIVERS)
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECEIVERS, msg.as_string())

        print("[INFO] Email sent successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
