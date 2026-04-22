from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..models import get_db, NewsArticle
from ..services.trend_detector_simple import TrendDetector

router = APIRouter()

@router.get("/topics")
async def get_trending_topics(
    hours: int = Query(24, ge=1, le=168),  # 1 hour to 1 week
    db: Session = Depends(get_db)
):
    """Get trending topics from recent articles"""
    try:
        # Get recent articles
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time
        ).all()
        
        if not articles:
            return {"trending_topics": [], "message": "No recent articles found"}
        
        # Convert to dict format
        article_dicts = []
        for article in articles:
            article_dicts.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'published_date': article.published_date,
                'sentiment_label': article.sentiment_label
            })
        
        # Detect trending topics
        detector = TrendDetector()
        trending_topics = detector.detect_trending_topics(article_dicts, hours)
        
        return {
            "trending_topics": trending_topics,
            "time_window_hours": hours,
            "articles_analyzed": len(article_dicts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting trends: {str(e)}")

@router.get("/analysis")
async def get_topic_trends(
    days: int = Query(7, ge=1, le=30),  # 1 day to 1 month
    db: Session = Depends(get_db)
):
    """Analyze topic trends over time"""
    try:
        # Get articles for the specified period
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time
        ).all()
        
        if not articles:
            return {"topic_trends": {}, "message": "No articles found in the specified period"}
        
        # Convert to dict format
        article_dicts = []
        for article in articles:
            article_dicts.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'published_date': article.published_date
            })
        
        # Analyze topic trends
        detector = TrendDetector()
        topic_trends = detector.analyze_topic_trends(article_dicts, days)
        
        return {
            "topic_trends": topic_trends,
            "analysis_period_days": days,
            "articles_analyzed": len(article_dicts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing topic trends: {str(e)}")

@router.get("/breaking")
async def get_breaking_news(
    minutes: int = Query(60, ge=15, le=1440),  # 15 minutes to 24 hours
    db: Session = Depends(get_db)
):
    """Get breaking news alerts"""
    try:
        # Get recent articles
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time
        ).all()
        
        if not articles:
            return {"breaking_news": [], "message": "No recent articles found"}
        
        # Convert to dict format
        article_dicts = []
        for article in articles:
            article_dicts.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'published_date': article.published_date,
                'source': article.source
            })
        
        # Detect breaking news
        detector = TrendDetector()
        breaking_news = detector.detect_breaking_news(article_dicts, minutes)
        
        return {
            "breaking_news": breaking_news,
            "time_window_minutes": minutes,
            "articles_analyzed": len(article_dicts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting breaking news: {str(e)}")

@router.get("/sentiment-trends")
async def get_sentiment_trends(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get sentiment trends over time"""
    try:
        # Get articles for the specified period
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time,
            NewsArticle.sentiment_label.isnot(None)
        ).all()
        
        if not articles:
            return {"sentiment_trends": {}, "message": "No analyzed articles found"}
        
        # Group by day and sentiment
        daily_sentiments = {}
        for article in articles:
            day = article.published_date.strftime('%Y-%m-%d')
            if day not in daily_sentiments:
                daily_sentiments[day] = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            if article.sentiment_label in daily_sentiments[day]:
                daily_sentiments[day][article.sentiment_label] += 1
        
        # Calculate trends
        sentiment_trends = {}
        for sentiment in ['positive', 'negative', 'neutral']:
            values = []
            for day in sorted(daily_sentiments.keys()):
                total = sum(daily_sentiments[day].values())
                if total > 0:
                    percentage = daily_sentiments[day][sentiment] / total * 100
                    values.append(percentage)
                else:
                    values.append(0)
            
            # Calculate trend direction
            if len(values) >= 2:
                recent_avg = sum(values[-3:]) / min(3, len(values))
                earlier_avg = sum(values[:-3]) / max(1, len(values) - 3)
                
                if recent_avg > earlier_avg * 1.1:
                    trend = "increasing"
                elif recent_avg < earlier_avg * 0.9:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            sentiment_trends[sentiment] = {
                "daily_values": dict(zip(sorted(daily_sentiments.keys()), values)),
                "trend_direction": trend,
                "current_percentage": values[-1] if values else 0
            }
        
        return {
            "sentiment_trends": sentiment_trends,
            "analysis_period_days": days,
            "articles_analyzed": len(articles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment trends: {str(e)}")

@router.get("/source-trends")
async def get_source_trends(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get trends by news source"""
    try:
        # Get articles for the specified period
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time
        ).all()
        
        if not articles:
            return {"source_trends": {}, "message": "No articles found"}
        
        # Group by source and day
        source_trends = {}
        for article in articles:
            source = article.source
            day = article.published_date.strftime('%Y-%m-%d')
            
            if source not in source_trends:
                source_trends[source] = {}
            
            if day not in source_trends[source]:
                source_trends[source][day] = 0
            
            source_trends[source][day] += 1
        
        # Calculate trend metrics for each source
        source_metrics = {}
        for source, daily_counts in source_trends.items():
            total_articles = sum(daily_counts.values())
            avg_daily = total_articles / len(daily_counts)
            
            # Calculate trend
            days_sorted = sorted(daily_counts.keys())
            if len(days_sorted) >= 2:
                recent_avg = sum(daily_counts[day] for day in days_sorted[-3:]) / min(3, len(days_sorted))
                earlier_avg = sum(daily_counts[day] for day in days_sorted[:-3]) / max(1, len(days_sorted) - 3)
                
                if recent_avg > earlier_avg * 1.2:
                    trend = "increasing"
                elif recent_avg < earlier_avg * 0.8:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "insufficient_data"
            
            source_metrics[source] = {
                "total_articles": total_articles,
                "average_daily": avg_daily,
                "trend_direction": trend,
                "daily_counts": daily_counts
            }
        
        return {
            "source_trends": source_metrics,
            "analysis_period_days": days,
            "articles_analyzed": len(articles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing source trends: {str(e)}")

@router.get("/summary")
async def get_trends_summary(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Get a comprehensive trends summary"""
    try:
        # Get recent articles
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        articles = db.query(NewsArticle).filter(
            NewsArticle.published_date >= cutoff_time
        ).all()
        
        if not articles:
            return {"summary": {}, "message": "No recent articles found"}
        
        # Basic statistics
        total_articles = len(articles)
        
        # Source distribution
        source_counts = {}
        for article in articles:
            source = article.source
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Sentiment distribution
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        for article in articles:
            if article.sentiment_label:
                sentiment_counts[article.sentiment_label] += 1
        
        # Category distribution
        category_counts = {}
        for article in articles:
            if article.category:
                category_counts[article.category] = category_counts.get(article.category, 0) + 1
        
        # Get trending topics
        article_dicts = []
        for article in articles:
            article_dicts.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'published_date': article.published_date
            })
        
        detector = TrendDetector()
        trending_topics = detector.detect_trending_topics(article_dicts, hours)
        
        return {
            "summary": {
                "total_articles": total_articles,
                "time_window_hours": hours,
                "top_sources": sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                "sentiment_distribution": sentiment_counts,
                "top_categories": sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                "trending_topics": trending_topics[:5] if trending_topics else []
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating trends summary: {str(e)}")
