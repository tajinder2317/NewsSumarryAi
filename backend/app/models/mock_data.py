"""
Mock data for serverless deployment when database is not available
"""
from datetime import datetime, timedelta
import random

# Sample news articles for demonstration
MOCK_ARTICLES = [
    {
        "id": 1,
        "title": "Breaking: Major Tech Company Announces AI Breakthrough",
        "content": "A leading technology company has announced a significant breakthrough in artificial intelligence research, promising to revolutionize how we interact with machines...",
        "summary": "Tech company announces major AI breakthrough with potential widespread applications.",
        "url": "https://example.com/tech-ai-breakthrough",
        "source": "Tech News Daily",
        "author": "John Doe",
        "published_date": datetime.utcnow() - timedelta(hours=2),
        "collected_date": datetime.utcnow() - timedelta(hours=1),
        "sentiment_score": 0.7,
        "sentiment_label": "positive",
        "topics": '["AI", "technology", "innovation"]',
        "category": "Technology"
    },
    {
        "id": 2,
        "title": "Global Climate Summit Reaches Historic Agreement",
        "content": "World leaders have reached a historic agreement on climate action at the global summit, committing to ambitious new targets for carbon reduction...",
        "summary": "Historic climate agreement reached with new carbon reduction targets.",
        "url": "https://example.com/climate-summit-agreement",
        "source": "Environmental News",
        "author": "Jane Smith",
        "published_date": datetime.utcnow() - timedelta(hours=4),
        "collected_date": datetime.utcnow() - timedelta(hours=3),
        "sentiment_score": 0.6,
        "sentiment_label": "positive",
        "topics": '["climate", "environment", "policy"]',
        "category": "Environment"
    },
    {
        "id": 3,
        "title": "Stock Markets Show Mixed Performance Amid Economic Uncertainty",
        "content": "Global stock markets displayed mixed performance today as investors grapple with ongoing economic uncertainty and changing interest rate expectations...",
        "summary": "Stock markets show mixed performance amid economic uncertainty.",
        "url": "https://example.com/stock-markets-mixed",
        "source": "Financial Times",
        "author": "Mike Johnson",
        "published_date": datetime.utcnow() - timedelta(hours=6),
        "collected_date": datetime.utcnow() - timedelta(hours=5),
        "sentiment_score": -0.1,
        "sentiment_label": "neutral",
        "topics": '["stocks", "economy", "finance"]',
        "category": "Business"
    },
    {
        "id": 4,
        "title": "New Medical Study Reveals Promising Treatment Results",
        "content": "A groundbreaking medical study has revealed promising results for a new treatment approach that could help millions of patients worldwide...",
        "summary": "New medical study shows promising treatment results for widespread conditions.",
        "url": "https://example.com/medical-study-results",
        "source": "Health News Network",
        "author": "Dr. Sarah Wilson",
        "published_date": datetime.utcnow() - timedelta(hours=8),
        "collected_date": datetime.utcnow() - timedelta(hours=7),
        "sentiment_score": 0.8,
        "sentiment_label": "positive",
        "topics": '["health", "medicine", "research"]',
        "category": "Health"
    },
    {
        "id": 5,
        "title": "Sports Team Wins Championship in Thrilling Final Match",
        "content": "In an exciting championship final, the home team secured victory with a last-minute goal, ending their decades-long championship drought...",
        "summary": "Sports team wins championship in dramatic final match.",
        "url": "https://example.com/sports-championship",
        "source": "Sports Central",
        "author": "Tom Davis",
        "published_date": datetime.utcnow() - timedelta(hours=10),
        "collected_date": datetime.utcnow() - timedelta(hours=9),
        "sentiment_score": 0.9,
        "sentiment_label": "positive",
        "topics": '["sports", "championship", "competition"]',
        "category": "Sports"
    }
]

def get_mock_articles(limit=10, source=None, category=None):
    """Get mock articles with optional filtering"""
    articles = MOCK_ARTICLES.copy()
    
    # Apply filters
    if source:
        articles = [a for a in articles if source.lower() in a["source"].lower()]
    
    if category:
        articles = [a for a in articles if a["category"] == category]
    
    # Sort by published date (newest first) and limit
    articles.sort(key=lambda x: x["published_date"], reverse=True)
    return articles[:limit]

def get_mock_article_by_id(article_id):
    """Get a specific mock article by ID"""
    for article in MOCK_ARTICLES:
        if article["id"] == article_id:
            return article
    return None

def get_mock_sources():
    """Get list of mock sources"""
    return list(set(article["source"] for article in MOCK_ARTICLES))

def get_mock_categories():
    """Get list of mock categories"""
    return list(set(article["category"] for article in MOCK_ARTICLES))

def get_mock_stats():
    """Get mock statistics"""
    total_articles = len(MOCK_ARTICLES)
    recent_articles = len([a for a in MOCK_ARTICLES if a["published_date"] > datetime.utcnow() - timedelta(days=1)])
    
    source_counts = {}
    sentiment_counts = {}
    
    for article in MOCK_ARTICLES:
        source = article["source"]
        sentiment = article["sentiment_label"]
        
        source_counts[source] = source_counts.get(source, 0) + 1
        sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
    
    return {
        "total_articles": total_articles,
        "recent_articles_24h": recent_articles,
        "sources": [{"source": source, "count": count} for source, count in source_counts.items()],
        "sentiment_distribution": [{"sentiment": sentiment, "count": count} for sentiment, count in sentiment_counts.items()]
    }
