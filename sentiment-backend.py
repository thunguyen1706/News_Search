import os
import re
import logging
import requests
from dataclasses import dataclass
from typing import List, Dict, Any
from newspaper import Article
from dotenv import load_dotenv
from google import genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ------------------- Configuration -------------------

load_dotenv()  # Load from .env file

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BRAVE_API_KEY:
    raise ValueError("Missing BRAVE_API_KEY environment variable!")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable!")

logging.basicConfig(level=logging.INFO)

client = genai.Client(api_key=GEMINI_API_KEY)

# ------------------- Data Classes -------------------

@dataclass
class SentimentResult:
    title: str
    sentiment: str
    confidence: int
    summary: str
    insights: List[str]
    url: str

class TopicRequest(BaseModel):
    topic: str = "Finance"
    num_articles: int = 5

# ------------------- Brave Search -------------------

def get_news_articles(topic="Finance", num_articles=5):
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }

    params = {
        "q": topic,
        "count": num_articles,
        "result_filter": "news",
        "search_lang": "en"
    }

    response = requests.get(
        "https://api.search.brave.com/res/v1/news/search",
        headers=headers,
        params=params
    )
    response.raise_for_status()
    return response.json().get("results", [])

def get_article_content(url, fallback_title=""):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text or fallback_title
    except Exception as e:
        logging.warning(f"Could not parse article content from {url}: {e}")
        return fallback_title

# ------------------- Gemini Analysis -------------------

def analyze_with_gemini(title, description, url, article_content):
    prompt = f"""
You are a financial news sentiment analyst.

Given a news article with the following fields:
- Title: {title}
- Description: {description}
- URL: {url}
- Full Content: {article_content}

Please:
1. Summarize the main points of the article in 2–3 sentences.
2. Classify the sentiment as one of:
   - Very Bullish
   - Bullish
   - Neutral
   - Bearish
   - Very Bearish
3. Assign a confidence score from 0 to 10.
4. Extract 2–4 bullet-point key insights that explain the sentiment choice.
5. Return the information in this JSON format:

```json
{{
  "title": "{title}",
  "summary": "...",
  "sentiment": "...",
  "confidence": ...,
  "insights": ["...", "..."],
  "url": "{url}"
}}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}]
    )

    response_text = response.text

    # Extract JSON-like fields using regex
    sentiment = re.search(r'"sentiment"\s*:\s*"([^"]+)"', response_text)
    confidence = re.search(r'"confidence"\s*:\s*(\d+)', response_text)
    summary = re.search(r'"summary"\s*:\s*"([^"]+)"', response_text, re.DOTALL)
    insights_block = re.search(r'"insights"\s*:\s*\[(.*?)\]', response_text, re.DOTALL)
    insights = re.findall(r'"([^"]+)"', insights_block.group(1)) if insights_block else []

    return SentimentResult(
        title=title,
        sentiment=sentiment.group(1).strip() if sentiment else "Unknown",
        confidence=int(confidence.group(1)) if confidence else 0,
        summary=summary.group(1).strip() if summary else "No summary.",
        insights=insights,
        url=url
    )

# ------------------- API Setup -------------------

app = FastAPI(title="Sentiment Analysis API")

@app.post("/analyze")
async def analyze_sentiment(request: TopicRequest):
    try:
        articles = get_news_articles(request.topic, request.num_articles)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        results = []
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "")
            url = article.get("url", "")
            content = get_article_content(url, title)
            
            result = analyze_with_gemini(title, description, url, content)
            results.append({
                "title": result.title,
                "sentiment": result.sentiment,
                "confidence": result.confidence,
                "summary": result.summary,
                "insights": result.insights,
                "url": result.url
            })
        
        return {"results": results}
    
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
