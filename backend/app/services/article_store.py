"""
In-memory article store for serverless deployment
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ArticleStore:
    def __init__(self):
        # In-memory storage for collected articles
        self.articles: List[Dict[str, Any]] = []
        self.last_collection: Optional[datetime] = None
    
    def store_articles(self, articles: List[Dict[str, Any]]) -> int:
        """Store articles and return count of new articles"""
        new_count = 0
        
        for article in articles:
            # Check if article already exists (by URL)
            existing_urls = [a.get('url') for a in self.articles]
            if article.get('url') not in existing_urls:
                # Add ID if not present
                if 'id' not in article:
                    article['id'] = len(self.articles) + new_count + 1
                
                self.articles.append(article)
                new_count += 1
                logger.info(f"Stored new article: {article.get('title', 'Unknown')[:50]}...")
        
        self.last_collection = datetime.utcnow()
        logger.info(f"Stored {new_count} new articles. Total: {len(self.articles)}")
        return new_count
    
    def get_articles(self, limit: int = 10, skip: int = 0, source: Optional[str] = None, category: Optional[str] = None, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve articles with optional filtering"""
        filtered_articles = self.articles.copy()
        
        # Apply filters
        if source:
            filtered_articles = [a for a in filtered_articles if source.lower() in a.get('source', '').lower()]
        
        if category:
            filtered_articles = [a for a in filtered_articles if a.get('category') == category]
        
        if region:
            filtered_articles = [a for a in filtered_articles if a.get('region', '').lower() == region.lower()]
        
        # Sort by published date (newest first)
        filtered_articles.sort(key=lambda x: x.get('published_date', datetime.utcnow()), reverse=True)
        
        # Apply pagination
        return filtered_articles[skip:skip+limit]
    
    def get_article_by_id(self, article_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific article by ID"""
        for article in self.articles:
            if article.get('id') == article_id:
                return article
        return None
    
    def get_sources(self) -> List[str]:
        """Get list of unique sources"""
        sources = list(set(article.get('source', 'Unknown') for article in self.articles))
        return sorted(sources)
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        categories = list(set(article.get('category', 'Unknown') for article in self.articles if article.get('category')))
        return sorted(categories)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored articles"""
        total_articles = len(self.articles)
        
        # Articles in last 24 hours
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_articles = len([a for a in self.articles if a.get('published_date', datetime.utcnow()) > yesterday])
        
        # Source distribution
        source_counts = {}
        for article in self.articles:
            source = article.get('source', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Sentiment distribution
        sentiment_counts = {}
        for article in self.articles:
            sentiment = article.get('sentiment_label', 'neutral')
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        return {
            "total_articles": total_articles,
            "recent_articles_24h": recent_articles,
            "sources": [{"source": source, "count": count} for source, count in source_counts.items()],
            "sentiment_distribution": [{"sentiment": sentiment, "count": count} for sentiment, count in sentiment_counts.items()]
        }
    
    def clear_old_articles(self, days: int = 7) -> int:
        """Remove articles older than specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        initial_count = len(self.articles)
        
        self.articles = [a for a in self.articles if a.get('published_date', datetime.utcnow()) > cutoff_date]
        
        removed_count = initial_count - len(self.articles)
        logger.info(f"Removed {removed_count} old articles. Remaining: {len(self.articles)}")
        return removed_count

# Global instance for serverless deployment
article_store = ArticleStore()

# Initialize with sample articles if store is empty
def initialize_article_store():
    """Initialize the article store with sample articles if empty"""
    if len(article_store.articles) == 0:
        from .real_news_collector import RealNewsCollector
        collector = RealNewsCollector()
        sample_articles = collector.get_sample_articles()
        article_store.store_articles(sample_articles)
        print("Article store initialized with sample articles")

# Initialize on import
initialize_article_store()
