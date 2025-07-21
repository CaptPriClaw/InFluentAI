from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("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")

llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)

# Custom prompt to focus on influencer marketing and trends
SUMMARY_PROMPT = PromptTemplate.from_template("""
You are a brand strategist. Summarize the key ideas, themes, and marketing angles in the following content.
Focus on:
- Campaign messaging
- Audience reaction
- Any emerging trends or viral elements

Content:
{text}

Summary:
""")

def build_summary_chain():
    """
    Returns a chain for summarizing influencer content using LangChain's map-reduce approach.
    """
    return load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=SUMMARY_PROMPT,
        combine_prompt=SUMMARY_PROMPT
    )

import asyncio

async def summarize_content(raw_text: str) -> str:
    """
    Async wrapper to summarize influencer content using LangChain.

    Args:
        raw_text (str): The influencer post, transcript, or caption.

    Returns:
        str: A summarized version with trends and highlights.
    """
    try:
        chain = build_summary_chain()
        docs = [Document(page_content=raw_text)]

        # Run the chain in a background thread (safe for blocking code in async app)
        summary = await asyncio.to_thread(chain.run, docs)
        return summary.strip()
    except Exception as e:
        print(f"[ERROR] LangChain summarization failed: {e}")
        return "Summary unavailable due to an error."

def get_summary_chain():
    return build_summary_chain()

