import requests
import feedparser
import instaloader
from datetime import datetime, timedelta


# --------------------- YOUTUBE SCRAPER ---------------------

def fetch_youtube_posts(channel_id, max_results=5):
    """
    Fetch recent videos from a YouTube channel via RSS feed.
    """
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    videos = []

    for entry in feed.entries[:max_results]:
        videos.append({
            "platform": "YouTube",
            "title": entry.title,
            "published": entry.published,
            "link": entry.link,
            "description": entry.get("media_description", "No description available")
        })

    return videos


# --------------------- INSTAGRAM SCRAPER ---------------------

def fetch_instagram_posts(username, max_posts=5):
    """
    Fetch recent posts from an Instagram account using instaloader.
    Requires login and stored session.
    """
    L = instaloader.Instaloader()

    try:
        L.load_session_from_file("your_username")  # Must run once with manual login to save session

        profile = instaloader.Profile.from_username(L.context, username)
        posts = []

        for post in profile.get_posts():
            posts.append({
                "platform": "Instagram",
                "caption": post.caption,
                "posted_at": post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "url": post.url,
            })
            if len(posts) >= max_posts:
                break

        return posts

    except Exception as e:
        print(f"[Instagram Error] {e}")
        return []


# --------------------- LINKEDIN SCRAPER (Simulated) ---------------------

def fetch_linkedin_posts(profile_url):
    """
    Placeholder: LinkedIn scraping is restricted. Replace with real API or third-party tool.
    """
    return [{
        "platform": "LinkedIn",
        "title": "New hiring update from competitor",
        "published": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": "We’re expanding our data science team to Pune.",
        "link": profile_url
    }]


# --------------------- COMBINED FETCH FUNCTION ---------------------

def fetch_all_posts(sources):
    """
    Accepts a dict with keys: 'youtube', 'instagram', 'linkedin'
    Each maps to a list of handles/channel_ids/profile_urls
    Returns a unified list of scraped posts.
    """
    all_posts = []

    for yt_id in sources.get("youtube", []):
        all_posts.extend(fetch_youtube_posts(yt_id))

    for ig_user in sources.get("instagram", []):
        all_posts.extend(fetch_instagram_posts(ig_user))

    for li_profile in sources.get("linkedin", []):
        all_posts.extend(fetch_linkedin_posts(li_profile))

    return all_posts

def scrape_content(name: str, platform: str) -> list:
    """
    Wrapper to fetch posts based on platform.
    """
    if platform.lower() == "youtube":
        return fetch_youtube_posts(name)
    elif platform.lower() == "instagram":
        return fetch_instagram_posts(name)
    elif platform.lower() == "linkedin":
        return fetch_linkedin_posts(name)
    else:
        print(f"[ERROR] Unknown platform: {platform}")
        return []