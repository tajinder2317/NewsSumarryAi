from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
import time
import logging

logger = logging.getLogger(__name__)

from ..models import (
    get_db, NewsArticle, NewsArticleResponse, SearchRequest
)

router = APIRouter()
_NEWS_STATS_CACHE = {"ts": 0.0, "data": None}
_NEWS_STATS_CACHE_TTL_SECONDS = 60

@router.get("/", response_model=List[NewsArticleResponse])
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),  # Reduced default limit for faster loading
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    minutes: Optional[int] = Query(None, ge=1, le=7 * 24 * 60, description="Only return articles published in the last N minutes"),
    db: Session = Depends(get_db)
):
    """Get news articles with optional filtering"""
    try:
        # Use a more efficient query with indexes
        query = db.query(NewsArticle)
        
        if source:
            query = query.filter(NewsArticle.source.ilike(f"%{source}%"))
        
        if category:
            query = query.filter(NewsArticle.category == category)

        if region:
            query = query.filter(NewsArticle.region == region)

        if minutes:
            cutoff = datetime.utcnow() - timedelta(minutes=minutes)
            query = query.filter(NewsArticle.published_date >= cutoff)
        
        # Order and limit for better performance
        articles = query.order_by(NewsArticle.published_date.desc()).offset(skip).limit(limit).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@router.get("/latest", response_model=List[NewsArticleResponse])
async def get_latest_news(
    minutes: int = Query(5, ge=1, le=24 * 60, description="Freshness window in minutes"),
    limit: int = Query(20, ge=1, le=50),
    refresh: bool = Query(True, description="Try to collect fresh news before returning results"),
    timeout: int = Query(6, ge=2, le=12, description="Timeout in seconds for RSS feed collection"),
    max_per_source: int = Query(3, ge=1, le=10, description="Max latest articles to fetch per RSS source"),
    db: Session = Depends(get_db),
):
    """
    Return the freshest news (default: last 5 minutes).

    On serverless deployments, we don't have a background scheduler by default,
    so this endpoint can optionally trigger a small collection pass first.
    """
    if refresh:
        from ..services.real_news_collector import RealNewsCollector

        try:
            collector = RealNewsCollector()
            articles = collector.collect_articles(timeout=timeout, max_articles_per_feed=max_per_source)

            urls = [a.get("url") for a in articles if a.get("url")]
            existing_urls = set()
            if urls:
                existing_rows = db.query(NewsArticle).filter(NewsArticle.url.in_(urls)).all()
                existing_urls = {row.url for row in existing_rows}

            for a in articles:
                url = a.get("url")
                if not url or url in existing_urls:
                    continue

                db.add(
                    NewsArticle(
                        title=a.get("title") or "Untitled",
                        content=a.get("content") or "",
                        summary=a.get("summary"),
                        url=url,
                        source=a.get("source") or "Unknown",
                        author=a.get("author"),
                        published_date=a.get("published_date"),
                        collected_date=a.get("collected_date"),
                        category=a.get("category"),
                        region=a.get("region"),
                        sentiment_score=a.get("sentiment_score"),
                        sentiment_label=a.get("sentiment_label"),
                        topics=a.get("topics"),
                    )
                )

            db.commit()
        except Exception as e:
            logger.warning(f"Latest refresh collection failed: {e}")
            try:
                db.rollback()
            except Exception:
                pass

    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    return (
        db.query(NewsArticle)
        .filter(NewsArticle.published_date >= cutoff)
        .order_by(NewsArticle.published_date.desc())
        .limit(limit)
        .all()
    )

@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific news article by ID"""
    try:
        article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching article: {str(e)}")

@router.post("/collect")
async def collect_news(
    timeout: int = Query(6, ge=2, le=12, description="Timeout in seconds for RSS feed collection"),
    max_per_source: int = Query(3, ge=1, le=10, description="Max latest articles to fetch per RSS source"),
    db: Session = Depends(get_db)
):
    """Trigger news collection from all sources"""
    from ..services.real_news_collector import RealNewsCollector

    try:
        collector = RealNewsCollector()
        articles = collector.collect_articles(timeout=timeout, max_articles_per_feed=max_per_source)

        total_before = db.query(NewsArticle).count()

        urls = [a.get("url") for a in articles if a.get("url")]
        existing_urls = set()
        existing_by_url = {}
        if urls:
            existing_rows = db.query(NewsArticle).filter(NewsArticle.url.in_(urls)).all()
            existing_by_url = {row.url: row for row in existing_rows}
            existing_urls = set(existing_by_url.keys())

        new_count = 0
        for a in articles:
            url = a.get("url")
            if not url or url in existing_urls:
                # Improve existing rows that were previously neutral/unscored.
                if url and url in existing_by_url:
                    existing = existing_by_url[url]
                    if (existing.sentiment_label in (None, "neutral")) and (existing.sentiment_score is None or abs(existing.sentiment_score) < 0.001):
                        existing.sentiment_score = a.get("sentiment_score")
                        existing.sentiment_label = a.get("sentiment_label")
                    if not existing.region and a.get("region"):
                        existing.region = a.get("region")
                    if not existing.category and a.get("category"):
                        existing.category = a.get("category")
                continue

            article = NewsArticle(
                title=a.get("title") or "Untitled",
                content=a.get("content") or "",
                summary=a.get("summary"),
                url=url,
                source=a.get("source") or "Unknown",
                author=a.get("author"),
                published_date=a.get("published_date"),
                collected_date=a.get("collected_date"),
                category=a.get("category"),
                region=a.get("region"),
                sentiment_score=a.get("sentiment_score"),
                sentiment_label=a.get("sentiment_label"),
                topics=a.get("topics"),
            )
            db.add(article)
            new_count += 1

        db.commit()

        total_after = db.query(NewsArticle).count()
        _NEWS_STATS_CACHE["ts"] = 0.0
        _NEWS_STATS_CACHE["data"] = None
        return {
            "message": f"Collected {new_count} new articles (processed {len(articles)}).",
            "collected_count": new_count,
            "total_articles": total_after,
            "articles_processed": len(articles),
            "timeout": False,
            "storage": "database"
        }
    except Exception as e:
        logger.error(f"Error in collect_news: {e}")
        raise HTTPException(status_code=500, detail=f"News collection failed: {str(e)}")

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
    try:
        sources = db.query(NewsArticle.source).distinct().all()
        return {"sources": [source[0] for source in sources]}
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching sources: {str(e)}")

@router.get("/categories/list")
async def get_news_categories(db: Session = Depends(get_db)):
    """Get list of all news categories"""
    try:
        categories = db.query(NewsArticle.category).distinct().filter(NewsArticle.category.isnot(None)).all()
        return {"categories": [category[0] for category in categories]}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")

@router.get("/stats/summary")
async def get_news_stats(db: Session = Depends(get_db)):
    """Get news statistics summary"""
    now = time.time()
    if _NEWS_STATS_CACHE["data"] is not None and (now - _NEWS_STATS_CACHE["ts"] < _NEWS_STATS_CACHE_TTL_SECONDS):
        return _NEWS_STATS_CACHE["data"]

    try:
        total_articles = db.query(NewsArticle).count()
        
        # Articles in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_articles = db.query(NewsArticle).filter(NewsArticle.published_date >= yesterday).count()
        
        # Articles by source
        source_counts = db.query(NewsArticle.source, func.count(NewsArticle.id)).group_by(NewsArticle.source).all()
        
        # Sentiment distribution
        sentiment_counts = db.query(NewsArticle.sentiment_label, func.count(NewsArticle.id)).group_by(NewsArticle.sentiment_label).all()
        
        result = {
            "total_articles": total_articles,
            "recent_articles_24h": recent_articles,
            "sources": [{"source": source, "count": count} for source, count in source_counts],
            "sentiment_distribution": [{"sentiment": sentiment, "count": count} for sentiment, count in sentiment_counts]
        }
        _NEWS_STATS_CACHE["ts"] = now
        _NEWS_STATS_CACHE["data"] = result
        return result
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete a news article"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    _NEWS_STATS_CACHE["ts"] = 0.0
    _NEWS_STATS_CACHE["data"] = None
    
    return {"message": "Article deleted successfully"}
