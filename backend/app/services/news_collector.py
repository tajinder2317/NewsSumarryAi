import feedparser
import requests
from newspaper import Article
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from urllib.parse import urlparse
import time

from ..models import NewsArticle, get_db
from ..config import settings

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NewsAnalyzerAI/1.0 (Educational Purpose)'
        })

    def collect_from_rss(self, rss_url: str, max_articles: int = 20) -> List[dict]:
        """Collect news articles from RSS feed"""
        try:
            logger.info(f"Collecting news from RSS: {rss_url}")
            feed = feedparser.parse(rss_url)
            articles = []
            
            for entry in feed.entries[:max_articles]:
                try:
                    article_data = self._parse_rss_entry(entry)
                    if article_data:
                        articles.append(article_data)
                    time.sleep(0.1)  # Be respectful to servers
                except Exception as e:
                    logger.warning(f"Error parsing RSS entry: {e}")
                    continue
            
            logger.info(f"Collected {len(articles)} articles from {rss_url}")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from RSS {rss_url}: {e}")
            return []

    def collect_from_newsapi(self, category: str = "general", max_articles: int = 20) -> List[dict]:
        """Collect news from NewsAPI"""
        if not settings.NEWS_API_KEY:
            logger.warning("NewsAPI key not configured")
            return []
        
        try:
            url = f"{settings.NEWS_API_URL}/top-headlines"
            params = {
                'apiKey': settings.NEWS_API_KEY,
                'category': category,
                'pageSize': max_articles,
                'country': 'us'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            for article in data.get('articles', []):
                article_data = self._parse_newsapi_article(article)
                if article_data:
                    articles.append(article_data)
            
            logger.info(f"Collected {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from NewsAPI: {e}")
            return []

    def _parse_rss_entry(self, entry) -> Optional[dict]:
        """Parse RSS entry into article data"""
        try:
            url = entry.link
            title = entry.title
            
            # Extract full article content
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': title,
                'content': article.text,
                'url': url,
                'source': self._extract_source_from_url(url),
                'author': ', '.join(article.authors) if article.authors else None,
                'published_date': self._parse_date(entry.get('published')),
                'summary': article.summary
            }
            
        except Exception as e:
            logger.warning(f"Error parsing RSS entry {entry.get('link', 'unknown')}: {e}")
            return None

    def _parse_newsapi_article(self, article) -> Optional[dict]:
        """Parse NewsAPI article into article data"""
        try:
            return {
                'title': article['title'],
                'content': article.get('content', article.get('description', '')),
                'url': article['url'],
                'source': article['source']['name'],
                'author': article.get('author'),
                'published_date': self._parse_date(article.get('publishedAt')),
                'summary': article.get('description')
            }
            
        except Exception as e:
            logger.warning(f"Error parsing NewsAPI article: {e}")
            return None

    def _extract_source_from_url(self, url: str) -> str:
        """Extract source name from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            return domain.replace('www.', '').split('.')[0].title()
        except:
            return "Unknown"

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string into datetime object"""
        if not date_str:
            return None
        
        try:
            # Try common date formats
            formats = [
                '%Y-%m-%dT%H:%M:%S%z',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%d %H:%M:%S',
                '%a, %d %b %Y %H:%M:%S %z',
                '%a, %d %b %Y %H:%M:%S %Z'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            # Fallback to feedparser parsing
            import time
            timestamp = time.mktime(feedparser._parse_date(date_str))
            return datetime.fromtimestamp(timestamp)
            
        except Exception as e:
            logger.warning(f"Error parsing date '{date_str}': {e}")
            return None

    def save_articles(self, articles: List[dict]) -> int:
        """Save articles to database"""
        if not articles:
            return 0
        
        saved_count = 0
        
        try:
            db = next(get_db())
            for article_data in articles:
                # Check if article already exists
                existing = db.query(NewsArticle).filter(
                    NewsArticle.url == article_data['url']
                ).first()
                
                if not existing:
                    article = NewsArticle(**article_data)
                    db.add(article)
                    saved_count += 1
            
            db.commit()
            logger.info(f"Saved {saved_count} new articles to database")
            
        except Exception as e:
            if 'db' in locals():
                db.rollback()
            logger.error(f"Error saving articles: {e}")
        finally:
            if 'db' in locals():
                db.close()
        
        return saved_count

    def collect_all_sources(self) -> int:
        """Collect news from all configured sources"""
        total_articles = 0
        
        # Collect from RSS feeds
        for rss_url in settings.RSS_FEEDS:
            if rss_url.strip():
                articles = self.collect_from_rss(rss_url.strip())
                saved = self.save_articles(articles)
                total_articles += saved
        
        # Collect from NewsAPI
        if settings.NEWS_API_KEY:
            articles = self.collect_from_newsapi()
            saved = self.save_articles(articles)
            total_articles += saved
        
        return total_articles
