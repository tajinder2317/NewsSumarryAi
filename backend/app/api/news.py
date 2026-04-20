from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

from ..models import (
    get_db, NewsArticle, NewsArticleResponse, SearchRequest
)
from ..models.mock_data import (
    get_mock_articles, get_mock_article_by_id, get_mock_sources, 
    get_mock_categories, get_mock_stats
)
from ..services import NewsCollector
from ..config import settings
import os

router = APIRouter()

@router.get("/", response_model=List[NewsArticleResponse])
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),  # Reduced default limit for faster loading
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get news articles with optional filtering"""
    # Use mock data in serverless environment or when database fails
    if os.getenv("VERCEL") or db is None:
        logger.info("Using mock data for serverless deployment")
        mock_articles = get_mock_articles(limit=limit, source=source, category=category)
        # Apply skip for pagination
        return mock_articles[skip:skip+limit]
    
    try:
        # Use a more efficient query with indexes
        query = db.query(NewsArticle)
        
        if source:
            query = query.filter(NewsArticle.source.ilike(f"%{source}%"))
        
        if category:
            query = query.filter(NewsArticle.category == category)
        
        # Order and limit for better performance
        articles = query.order_by(NewsArticle.published_date.desc()).offset(skip).limit(limit).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        # Fallback to mock data
        mock_articles = get_mock_articles(limit=limit, source=source, category=category)
        return mock_articles[skip:skip+limit]

@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific news article by ID"""
    # Use mock data in serverless environment or when database fails
    if os.getenv("VERCEL") or db is None:
        logger.info("Using mock data for article retrieval")
        article = get_mock_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    
    try:
        article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except Exception as e:
        logger.error(f"Error fetching article: {e}")
        # Fallback to mock data
        article = get_mock_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

@router.post("/collect")
async def collect_news(
    timeout: int = Query(5, ge=3, le=15, description="Timeout in seconds for RSS feed collection"),
    db: Session = Depends(get_db)
):
    """Trigger news collection from all sources"""
    # Handle database errors gracefully
    if db is None:
        logger.error("Database connection failed for news collection")
        return {
            "message": "Database connection failed. Please try again later.",
            "collected_count": 0,
            "total_articles": 0,
            "articles_processed": 0,
            "timeout": False,
            "error": "database_error"
        }
    
    try:
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        collector = NewsCollector()
        
        # Get total articles before collection
        try:
            total_before = db.query(NewsArticle).count()
        except Exception as e:
            logger.error(f"Error counting articles before collection: {e}")
            total_before = 0
        
        # Run collection in a separate thread with timeout
        loop = asyncio.get_event_loop()
        
        def collect_with_timeout():
            return collector.collect_all_sources(timeout=timeout)
        
        try:
            collected_count = await asyncio.wait_for(
                loop.run_in_executor(ThreadPoolExecutor(max_workers=1), collect_with_timeout),
                timeout=timeout + 2  # Small buffer for API processing
            )
        except asyncio.TimeoutError:
            logger.error(f"News collection timed out after {timeout + 2} seconds")
            return {
                "message": f"News collection timed out after {timeout} seconds. Please try again with a longer timeout or check your internet connection.",
                "collected_count": 0,
                "total_articles": total_before,
                "articles_processed": 0,
                "timeout": True
            }
        
        # Get total articles after collection
        total_after = db.query(NewsArticle).count()
        articles_processed = total_after - total_before
        
        if collected_count == 0 and articles_processed > 0:
            message = f"Processed {articles_processed} articles from RSS feeds, but all were already in database"
        elif collected_count > 0:
            message = f"Successfully collected {collected_count} new articles (processed {articles_processed} total)"
        else:
            message = f"No new articles found. {total_after} articles already in database"
        
        return {
            "message": message,
            "collected_count": collected_count,
            "total_articles": total_after,
            "articles_processed": articles_processed,
            "timeout": False
        }
    except Exception as e:
        logger.error(f"Error in collect_news: {e}")
        raise HTTPException(status_code=500, detail=f"Error collecting news: {str(e)}")

@router.post("/search", response_model=List[NewsArticleResponse])
async def search_news(
    search_request: SearchRequest,
    db: Session = Depends(get_db)
):
    """Search news articles with various filters"""
    query = db.query(NewsArticle)
    
    # Text search
    if search_request.query:
        query = query.filter(
            NewsArticle.title.ilike(f"%{search_request.query}%") |
            NewsArticle.content.ilike(f"%{search_request.query}%")
        )
    
    # Source filter
    if search_request.source:
        query = query.filter(NewsArticle.source.ilike(f"%{search_request.source}%"))
    
    # Category filter
    if search_request.category:
        query = query.filter(NewsArticle.category == search_request.category)
    
    # Date range filter
    if search_request.date_from:
        query = query.filter(NewsArticle.published_date >= search_request.date_from)
    
    if search_request.date_to:
        query = query.filter(NewsArticle.published_date <= search_request.date_to)
    
    # Sentiment filter
    if search_request.sentiment:
        query = query.filter(NewsArticle.sentiment_label == search_request.sentiment)
    
    # Apply pagination
    articles = query.order_by(NewsArticle.published_date.desc()).offset(search_request.offset).limit(search_request.limit).all()
    
    return articles

@router.get("/sources/list")
async def get_news_sources(db: Session = Depends(get_db)):
    """Get list of all news sources"""
    # Use mock data in serverless environment or when database fails
    if os.getenv("VERCEL") or db is None:
        logger.info("Using mock data for sources")
        return {"sources": get_mock_sources()}
    
    try:
        sources = db.query(NewsArticle.source).distinct().all()
        return {"sources": [source[0] for source in sources]}
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        # Fallback to mock data
        return {"sources": get_mock_sources()}

@router.get("/categories/list")
async def get_news_categories(db: Session = Depends(get_db)):
    """Get list of all news categories"""
    # Use mock data in serverless environment or when database fails
    if os.getenv("VERCEL") or db is None:
        logger.info("Using mock data for categories")
        return {"categories": get_mock_categories()}
    
    try:
        categories = db.query(NewsArticle.category).distinct().filter(NewsArticle.category.isnot(None)).all()
        return {"categories": [category[0] for category in categories]}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        # Fallback to mock data
        return {"categories": get_mock_categories()}

@router.get("/stats/summary")
async def get_news_stats(db: Session = Depends(get_db)):
    """Get news statistics summary"""
    # Use mock data in serverless environment or when database fails
    if os.getenv("VERCEL") or db is None:
        logger.info("Using mock data for stats")
        return get_mock_stats()
    
    try:
        total_articles = db.query(NewsArticle).count()
        
        # Articles in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_articles = db.query(NewsArticle).filter(NewsArticle.published_date >= yesterday).count()
        
        # Articles by source
        source_counts = db.query(NewsArticle.source, func.count(NewsArticle.id)).group_by(NewsArticle.source).all()
        
        # Sentiment distribution
        sentiment_counts = db.query(NewsArticle.sentiment_label, func.count(NewsArticle.id)).group_by(NewsArticle.sentiment_label).all()
        
        return {
            "total_articles": total_articles,
            "recent_articles_24h": recent_articles,
            "sources": [{"source": source, "count": count} for source, count in source_counts],
            "sentiment_distribution": [{"sentiment": sentiment, "count": count} for sentiment, count in sentiment_counts]
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        # Fallback to mock data
        return get_mock_stats()

@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete a news article"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    
    return {"message": "Article deleted successfully"}
