# agents/content_summarizer.py

import os
from summarizer.langchain_chain import get_summary_chain
from dotenv import load_dotenv

load_dotenv()

def summarize_content(content: str, platform: str, creator_handle: str) -> str:
    """
    Summarizes raw content using LangChain LLM pipeline.

    Args:
        content (str): Full text content scraped from influencer/competitor posts.
        platform (str): Platform name (e.g., 'YouTube', 'Instagram', 'LinkedIn').
        creator_handle (str): Username/handle of the creator.

    Returns:
        str: Clean summarized output ready for insights pipeline.
    """
    try:
        summary_chain = get_summary_chain(platform)
        result = summary_chain.run({
            "content": content,
            "creator_handle": creator_handle,
            "platform": platform
        })
        return result.strip()
    except Exception as e:
        print(f"[ERROR] Summarization failed for {creator_handle} on {platform}: {e}")
        return "Summarization Failed"

