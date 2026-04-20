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
    try:
        # Always ensure we have sample articles in serverless environment
        if os.getenv("VERCEL"):
            # Clear and reinitialize for fresh data
            article_store.articles.clear()
            print("Cleared article store for serverless reinitialization")
        
        if len(article_store.articles) == 0:
            # Import sample articles directly to avoid circular import
            from datetime import datetime, timedelta
            
            sample_articles = [
                {
                    'id': 1,
                    'title': 'Breaking: Major Tech Company Announces AI Breakthrough',
                    'content': 'A leading technology company has announced a significant breakthrough in artificial intelligence research, promising to revolutionize how we interact with machines. The new AI system demonstrates unprecedented capabilities in natural language understanding and problem-solving.',
                    'summary': 'Tech company announces major AI breakthrough with potential widespread applications.',
                    'url': 'https://example.com/tech-ai-breakthrough',
                    'source': 'Tech News Daily',
                    'region': 'Global',
                    'author': 'John Doe',
                    'published_date': datetime.utcnow() - timedelta(hours=2),
                    'collected_date': datetime.utcnow() - timedelta(hours=1),
                    'sentiment_score': 0.7,
                    'sentiment_label': 'positive',
                    'topics': '["AI", "technology", "innovation"]',
                    'category': 'Technology'
                },
                {
                    'id': 2,
                    'title': 'Global Climate Summit Reaches Historic Agreement',
                    'content': 'World leaders have reached a historic agreement on climate action at the global Summit, committing to ambitious new targets for carbon reduction. The agreement includes binding commitments from major economies.',
                    'summary': 'Historic climate agreement reached with new carbon reduction targets.',
                    'url': 'https://example.com/climate-summit-agreement',
                    'source': 'Environmental News',
                    'region': 'Global',
                    'author': 'Jane Smith',
                    'published_date': datetime.utcnow() - timedelta(hours=4),
                    'collected_date': datetime.utcnow() - timedelta(hours=3),
                    'sentiment_score': 0.6,
                    'sentiment_label': 'positive',
                    'topics': '["climate", "environment", "policy"]',
                    'category': 'Environment'
                },
                {
                    'id': 3,
                    'title': 'Indian Stock Market Hits Record High Amid Economic Growth',
                    'content': 'The Indian stock market reached an all-time high today as investors showed confidence in the country\'s economic growth prospects. Major indices surged to unprecedented levels.',
                    'summary': 'Indian stock market achieves record high amid positive economic indicators.',
                    'url': 'https://example.com/indian-stock-market-record',
                    'source': 'Financial Express',
                    'region': 'India',
                    'author': 'Raj Kumar',
                    'published_date': datetime.utcnow() - timedelta(hours=3),
                    'collected_date': datetime.utcnow() - timedelta(hours=2),
                    'sentiment_score': 0.8,
                    'sentiment_label': 'positive',
                    'topics': '["economy", "stocks", "India", "finance"]',
                    'category': 'Business'
                },
                {
                    'id': 4,
                    'title': 'New Health Breakthrough in Cancer Research',
                    'content': 'Medical researchers have discovered a promising new treatment approach for certain types of cancer, showing remarkable results in early clinical trials. The breakthrough could save millions of lives.',
                    'summary': 'Revolutionary cancer treatment shows promising results in clinical trials.',
                    'url': 'https://example.com/cancer-research-breakthrough',
                    'source': 'Health News Today',
                    'region': 'Global',
                    'author': 'Dr. Sarah Johnson',
                    'published_date': datetime.utcnow() - timedelta(hours=5),
                    'collected_date': datetime.utcnow() - timedelta(hours=4),
                    'sentiment_score': 0.9,
                    'sentiment_label': 'positive',
                    'topics': '["health", "medicine", "cancer", "research"]',
                    'category': 'Health'
                },
                {
                    'id': 5,
                    'title': 'Tech Giants Face New Regulatory Challenges in Europe',
                    'content': 'Major technology companies are facing increased regulatory scrutiny in Europe as new rules come into effect. The regulations aim to protect user privacy and promote fair competition.',
                    'summary': 'European regulators implement new rules for tech companies.',
                    'url': 'https://example.com/tech-regulation-europe',
                    'source': 'BBC News',
                    'region': 'UK',
                    'author': 'Michael Brown',
                    'published_date': datetime.utcnow() - timedelta(hours=6),
                    'collected_date': datetime.utcnow() - timedelta(hours=5),
                    'sentiment_score': 0.3,
                    'sentiment_label': 'negative',
                    'topics': '["technology", "regulation", "Europe", "privacy"]',
                    'category': 'Technology'
                }
            ]
            
            # Add unique timestamps to make articles appear fresh
            current_time = datetime.utcnow()
            for i, article in enumerate(sample_articles):
                article['published_date'] = current_time - timedelta(hours=i+1)
                article['collected_date'] = current_time - timedelta(minutes=i*10)
                article['id'] = i + 1  # Ensure unique IDs
            
            article_store.store_articles(sample_articles)
            print(f"Article store initialized with {len(sample_articles)} fresh sample articles")
            
            # Try to collect real news in background
            try:
                from .real_news_collector import RealNewsCollector
                collector = RealNewsCollector()
                # Quick collection with short timeout
                collector.collect_all_sources(timeout=3)
                print("Attempted real news collection in background")
            except Exception as e:
                print(f"Background news collection failed: {e}")
    except Exception as e:
        print(f"Error initializing article store: {e}")
        # Don't fail startup, just log the error

# Initialize on import
initialize_article_store()
