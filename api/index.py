#!/usr/bin/env python3
"""
Vercel serverless function for backend API with full news collection functionality
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import feedparser
import requests
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="News Analyzer AI API",
    description="AI-powered news analysis and summarization platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class NewsArticle(BaseModel):
    title: str
    content: str
    url: str
    source: str
    published_date: Optional[str] = None

class CollectResponse(BaseModel):
    message: str
    collected_count: int
    total_articles: int
    articles_processed: int
    timeout: bool
    articles: List[NewsArticle] = []

# RSS Feeds
RSS_FEEDS = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.reuters.com/reuters/topNews",
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
]

def collect_from_rss(rss_url: str, max_articles: int = 3) -> List[NewsArticle]:
    """Collect news from RSS feed"""
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        
        for entry in feed.entries[:max_articles]:
            article = NewsArticle(
                title=entry.get('title', ''),
                content=entry.get('summary', entry.get('description', '')),
                url=entry.get('link', ''),
                source=feed.feed.get('title', 'Unknown'),
                published_date=entry.get('published', '')
            )
            articles.append(article)
        
        logger.info(f"Collected {len(articles)} articles from {rss_url}")
        return articles
    except Exception as e:
        logger.error(f"Error collecting from {rss_url}: {e}")
        return []

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "News Analyzer AI API",
        "version": "1.0.0",
        "status": "running",
        "environment": "vercel"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}

@app.get("/api/v1/news/", response_model=List[NewsArticle])
async def get_news(skip: int = 0, limit: int = 10):
    """Get news articles"""
    try:
        all_articles = []
        for feed_url in RSS_FEEDS[:2]:  # Limit to 2 feeds for performance
            articles = collect_from_rss(feed_url, max_articles=2)
            all_articles.extend(articles)
        
        return all_articles[skip:skip+limit]
    except Exception as e:
        logger.error(f"Error getting news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")

@app.post("/api/v1/news/collect", response_model=CollectResponse)
async def collect_news():
    """Collect news from sources"""
    try:
        logger.info("Starting news collection")
        all_articles = []
        collected_count = 0
        
        for i, feed_url in enumerate(RSS_FEEDS[:3]):  # Limit to 3 feeds
            try:
                articles = collect_from_rss(feed_url, max_articles=2)
                all_articles.extend(articles)
                collected_count += len(articles)
                logger.info(f"Feed {i+1}: Collected {len(articles)} articles")
            except Exception as e:
                logger.error(f"Error with feed {i+1}: {e}")
                continue
        
        logger.info(f"Collection complete: {collected_count} total articles")
        
        return CollectResponse(
            message=f"Successfully collected {collected_count} articles from {len(RSS_FEEDS)} feeds",
            collected_count=collected_count,
            total_articles=len(all_articles),
            articles_processed=len(RSS_FEEDS),
            timeout=False,
            articles=all_articles
        )
    except Exception as e:
        logger.error(f"Error in news collection: {e}")
        raise HTTPException(status_code=500, detail="Failed to collect news")

# Export for Vercel
handler = app
