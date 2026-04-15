from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from ..models import (
    get_db, NewsArticle, AnalysisRequest, AnalysisResponse, 
    SentimentAnalysis, TopicAnalysis
)
from ..services.analyzer_simple import TextAnalyzer
from ..services.summarizer import TextSummarizer

router = APIRouter()

@router.post("/sentiment", response_model=SentimentAnalysis)
async def analyze_sentiment(
    article_ids: List[int],
    db: Session = Depends(get_db)
):
    """Analyze sentiment for specified articles"""
    try:
        # Get articles
        articles = db.query(NewsArticle).filter(NewsArticle.id.in_(article_ids)).all()
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        analyzer = TextAnalyzer()
        sentiments = {"positive": 0, "negative": 0, "neutral": 0}
        
        for article in articles:
            # Analyze title and content
            text = f"{article.title} {article.content}"
            sentiment_result = analyzer.analyze_sentiment(text)
            
            # Update article with sentiment analysis
            article.sentiment_score = sentiment_result["polarity"]
            article.sentiment_label = sentiment_result["label"]
            
            # Count sentiments
            sentiments[sentiment_result["label"]] += 1
        
        # Calculate percentages
        total = sum(sentiments.values())
        for key in sentiments:
            sentiments[key] = sentiments[key] / total if total > 0 else 0
        
        # Determine overall label
        overall_label = max(sentiments, key=sentiments.get)
        
        # Save changes
        db.commit()
        
        return SentimentAnalysis(
            positive=sentiments["positive"],
            negative=sentiments["negative"],
            neutral=sentiments["neutral"],
            label=overall_label
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")

@router.post("/topics", response_model=TopicAnalysis)
async def analyze_topics(
    article_ids: List[int],
    db: Session = Depends(get_db)
):
    """Extract topics from specified articles"""
    try:
        # Get articles
        articles = db.query(NewsArticle).filter(NewsArticle.id.in_(article_ids)).all()
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        analyzer = TextAnalyzer()
        texts = [f"{article.title} {article.content}" for article in articles]
        
        # Extract topics
        topics = analyzer.extract_topics(texts, num_topics=5)
        
        # Update articles with topic information
        topic_dict = {topic["topic_id"]: topic for topic in topics}
        
        for i, article in enumerate(articles):
            if i < len(topics):
                # Assign dominant topic to article
                article.topics = json.dumps(topics[i])
                article.category = analyzer.categorize_text(texts[i])
        
        # Save changes
        db.commit()
        
        # Find dominant topic
        dominant_topic = topics[0]["label"] if topics else "Unknown"
        
        return TopicAnalysis(
            topics=topics,
            dominant_topic=dominant_topic
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing topics: {str(e)}")

@router.post("/summarize")
async def summarize_articles(
    article_ids: List[int],
    max_sentences: int = 3,
    db: Session = Depends(get_db)
):
    """Summarize specified articles"""
    try:
        # Get articles
        articles = db.query(NewsArticle).filter(NewsArticle.id.in_(article_ids)).all()
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        summarizer = TextSummarizer()
        
        if len(articles) == 1:
            # Summarize single article
            article = articles[0]
            summary = summarizer.summarize_article(article.content, max_sentences)
            
            # Update article with summary
            article.summary = summary
            db.commit()
            
            return {
                "article_id": article.id,
                "summary": summary,
                "key_points": summarizer.extract_key_points(article.content)
            }
        else:
            # Summarize multiple articles
            article_dicts = [
                {
                    "title": article.title,
                    "content": article.content
                }
                for article in articles
            ]
            
            summary = summarizer.summarize_multiple_articles(article_dicts, max_sentences)
            
            return {
                "summary": summary,
                "article_count": len(articles),
                "key_points": summarizer.extract_key_points(
                    " ".join([article.content for article in articles])
                )
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing articles: {str(e)}")

@router.post("/keywords")
async def extract_keywords(
    article_ids: List[int],
    num_keywords: int = 10,
    db: Session = Depends(get_db)
):
    """Extract keywords from specified articles"""
    try:
        # Get articles
        articles = db.query(NewsArticle).filter(NewsArticle.id.in_(article_ids)).all()
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        analyzer = TextAnalyzer()
        all_keywords = []
        
        for article in articles:
            text = f"{article.title} {article.content}"
            keywords = analyzer.extract_keywords(text, num_keywords)
            all_keywords.extend(keywords)
        
        # Count keyword frequency
        from collections import Counter
        keyword_counts = Counter(all_keywords)
        
        return {
            "keywords": dict(keyword_counts.most_common(num_keywords)),
            "total_keywords": len(keyword_counts),
            "articles_analyzed": len(articles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting keywords: {str(e)}")

@router.post("/categorize")
async def categorize_articles(
    article_ids: List[int],
    db: Session = Depends(get_db)
):
    """Categorize specified articles"""
    try:
        # Get articles
        articles = db.query(NewsArticle).filter(NewsArticle.id.in_(article_ids)).all()
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        analyzer = TextAnalyzer()
        categories = {}
        
        for article in articles:
            text = f"{article.title} {article.content}"
            category = analyzer.categorize_text(text)
            
            # Update article category
            article.category = category
            categories[article.id] = category
        
        # Save changes
        db.commit()
        
        return {
            "categories": categories,
            "articles_updated": len(articles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error categorizing articles: {str(e)}")

@router.get("/statistics")
async def get_analysis_statistics(db: Session = Depends(get_db)):
    """Get analysis statistics"""
    try:
        total_articles = db.query(NewsArticle).count()
        
        # Sentiment distribution
        sentiment_counts = db.query(
            NewsArticle.sentiment_label, 
            db.func.count(NewsArticle.id)
        ).group_by(NewsArticle.sentiment_label).all()
        
        # Category distribution
        category_counts = db.query(
            NewsArticle.category,
            db.func.count(NewsArticle.id)
        ).group_by(NewsArticle.category).all()
        
        # Articles with analysis
        analyzed_articles = db.query(NewsArticle).filter(
            NewsArticle.sentiment_label.isnot(None)
        ).count()
        
        return {
            "total_articles": total_articles,
            "analyzed_articles": analyzed_articles,
            "analysis_coverage": analyzed_articles / total_articles if total_articles > 0 else 0,
            "sentiment_distribution": [
                {"sentiment": sentiment, "count": count} 
                for sentiment, count in sentiment_counts
            ],
            "category_distribution": [
                {"category": category, "count": count} 
                for category, count in category_counts
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")
