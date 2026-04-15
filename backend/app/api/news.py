from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..models import (
    get_db, NewsArticle, NewsArticleResponse, SearchRequest
)
from ..services import NewsCollector

router = APIRouter()

@router.get("/", response_model=List[NewsArticleResponse])
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get news articles with optional filtering"""
    query = db.query(NewsArticle)
    
    if source:
        query = query.filter(NewsArticle.source.ilike(f"%{source}%"))
    
    if category:
        query = query.filter(NewsArticle.category == category)
    
    articles = query.order_by(NewsArticle.published_date.desc()).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=NewsArticleResponse)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific news article by ID"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/collect")
async def collect_news(db: Session = Depends(get_db)):
    """Trigger news collection from all sources"""
    try:
        collector = NewsCollector()
        collected_count = collector.collect_all_sources()
        
        return {
            "message": f"Successfully collected {collected_count} new articles",
            "collected_count": collected_count
        }
    except Exception as e:
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
    sources = db.query(NewsArticle.source).distinct().all()
    return {"sources": [source[0] for source in sources]}

@router.get("/categories/list")
async def get_news_categories(db: Session = Depends(get_db)):
    """Get list of all news categories"""
    categories = db.query(NewsArticle.category).distinct().filter(NewsArticle.category.isnot(None)).all()
    return {"categories": [category[0] for category in categories]}

@router.get("/stats/summary")
async def get_news_stats(db: Session = Depends(get_db)):
    """Get news statistics summary"""
    total_articles = db.query(NewsArticle).count()
    
    # Articles in last 24 hours
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_articles = db.query(NewsArticle).filter(NewsArticle.published_date >= yesterday).count()
    
    # Articles by source
    source_counts = db.query(NewsArticle.source, db.func.count(NewsArticle.id)).group_by(NewsArticle.source).all()
    
    # Sentiment distribution
    sentiment_counts = db.query(NewsArticle.sentiment_label, db.func.count(NewsArticle.id)).group_by(NewsArticle.sentiment_label).all()
    
    return {
        "total_articles": total_articles,
        "recent_articles_24h": recent_articles,
        "sources": [{"source": source, "count": count} for source, count in source_counts],
        "sentiment_distribution": [{"sentiment": sentiment, "count": count} for sentiment, count in sentiment_counts]
    }

@router.delete("/{article_id}")
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete a news article"""
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    
    return {"message": "Article deleted successfully"}
