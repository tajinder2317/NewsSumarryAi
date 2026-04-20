"""
Real news collector that fetches from RSS feeds for serverless deployment
"""
import feedparser
import requests
from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup

from .article_store import article_store

logger = logging.getLogger(__name__)

class RealNewsCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NewsAnalyzerAI/1.0 (News Aggregator Bot)'
        })
        
        # Reliable RSS feeds that work well in serverless environment
        self.rss_feeds = [
            {
                'name': 'BBC News',
                'url': 'http://feeds.bbci.co.uk/news/rss.xml',
                'category': 'General'
            },
            {
                'name': 'Reuters',
                'url': 'https://feeds.reuters.com/reuters/topNews',
                'category': 'General'
            },
            {
                'name': 'CNN',
                'url': 'https://rss.cnn.com/rss/edition.rss',
                'category': 'General'
            },
            {
                'name': 'TechCrunch',
                'url': 'https://feeds.feedburner.com/techcrunch',
                'category': 'Technology'
            },
            {
                'name': 'BBC Technology',
                'url': 'http://feeds.bbci.co.uk/news/technology/rss.xml',
                'category': 'Technology'
            }
        ]
    
    def clean_html(self, html_content: str) -> str:
        """Remove HTML tags and clean text"""
        if not html_content:
            return ""
        
        # Remove HTML tags
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Limit length for storage
        if len(text) > 2000:
            text = text[:2000] + "..."
        
        return text
    
    def extract_summary(self, content: str, max_length: int = 200) -> str:
        """Extract a summary from content"""
        if not content:
            return ""
        
        # Try to find first sentence
        sentences = re.split(r'[.!?]+', content)
        if sentences:
            first_sentence = sentences[0].strip()
            if len(first_sentence) <= max_length:
                return first_sentence
            else:
                return first_sentence[:max_length] + "..."
        
        return content[:max_length] + "..." if len(content) > max_length else content
    
    def fetch_feed_articles(self, feed_info: Dict[str, Any], max_articles: int = 5) -> List[Dict[str, Any]]:
        """Fetch articles from a single RSS feed"""
        articles = []
        
        try:
            logger.info(f"Fetching from {feed_info['name']}")
            
            # Fetch RSS feed with timeout
            response = self.session.get(feed_info['url'], timeout=10)
            response.raise_for_status()
            
            # Parse RSS feed
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                logger.warning(f"Feed parsing warning for {feed_info['name']}: {feed.bozo_exception}")
            
            # Process entries
            for entry in feed.entries[:max_articles]:
                try:
                    # Extract basic info
                    title = entry.get('title', '').strip()
                    link = entry.get('link', '')
                    description = entry.get('description', '')
                    content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else description
                    
                    # Skip if missing essential info
                    if not title or not link:
                        continue
                    
                    # Parse publication date
                    pub_date = datetime.utcnow()
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        try:
                            pub_date = datetime(*entry.published_parsed[:6])
                        except (ValueError, TypeError):
                            pass
                    
                    # Clean content
                    clean_content = self.clean_html(content)
                    summary = self.extract_summary(clean_content)
                    
                    # Create article dict
                    article = {
                        'title': title,
                        'content': clean_content,
                        'summary': summary,
                        'url': link,
                        'source': feed_info['name'],
                        'author': entry.get('author', 'Unknown'),
                        'published_date': pub_date,
                        'collected_date': datetime.utcnow(),
                        'category': feed_info['category'],
                        'sentiment_score': 0.0,  # Will be analyzed later
                        'sentiment_label': 'neutral',
                        'topics': '[]'  # JSON string, will be analyzed later
                    }
                    
                    articles.append(article)
                    logger.info(f"Added article: {title[:50]}...")
                    
                except Exception as e:
                    logger.error(f"Error processing article from {feed_info['name']}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(articles)} articles from {feed_info['name']}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching {feed_info['name']}: {e}")
        except Exception as e:
            logger.error(f"Error processing {feed_info['name']}: {e}")
        
        return articles
    
    def collect_all_sources(self, timeout: int = 30) -> int:
        """Collect news from all RSS feeds"""
        all_articles = []
        
        logger.info(f"Starting news collection from {len(self.rss_feeds)} sources")
        
        for feed_info in self.rss_feeds:
            try:
                articles = self.fetch_feed_articles(feed_info, max_articles=3)  # Limit per feed for speed
                all_articles.extend(articles)
                
            except Exception as e:
                logger.error(f"Failed to collect from {feed_info['name']}: {e}")
                continue
        
        # Store articles in the article store
        new_articles_count = article_store.store_articles(all_articles)
        
        logger.info(f"Collection completed. Total articles stored: {len(article_store.articles)}, New articles: {new_articles_count}")
        return new_articles_count
    
    def get_sample_articles(self) -> List[Dict[str, Any]]:
        """Get sample articles for demonstration when real collection fails"""
        return [
            {
                'id': 1,
                'title': 'Breaking: Major Tech Company Announces AI Breakthrough',
                'content': 'A leading technology company has announced a significant breakthrough in artificial intelligence research, promising to revolutionize how we interact with machines...',
                'summary': 'Tech company announces major AI breakthrough with potential widespread applications.',
                'url': 'https://example.com/tech-ai-breakthrough',
                'source': 'Tech News Daily',
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
                'content': 'World leaders have reached a historic agreement on climate action at the global summit, committing to ambitious new targets for carbon reduction...',
                'summary': 'Historic climate agreement reached with new carbon reduction targets.',
                'url': 'https://example.com/climate-summit-agreement',
                'source': 'Environmental News',
                'author': 'Jane Smith',
                'published_date': datetime.utcnow() - timedelta(hours=4),
                'collected_date': datetime.utcnow() - timedelta(hours=3),
                'sentiment_score': 0.6,
                'sentiment_label': 'positive',
                'topics': '["climate", "environment", "policy"]',
                'category': 'Environment'
            }
        ]
