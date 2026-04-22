"""
Real news collector that fetches from RSS feeds for serverless deployment
"""
import feedparser
import requests
from datetime import datetime, timedelta
import calendar
import logging
from typing import List, Dict, Any
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

from .article_store import article_store
from .analyzer_simple import TextAnalyzer

logger = logging.getLogger(__name__)

class RealNewsCollector:
    def __init__(self):
        self.request_headers = {
            'User-Agent': 'NewsAnalyzerAI/1.0 (News Aggregator Bot)'
        }
        self.analyzer = TextAnalyzer()
        
        # Broad global feed coverage across Asia, Europe, Americas, Middle East, and Africa.
        self.rss_feeds = [
            # Global wires / international
            {'name': 'Reuters', 'url': 'https://feeds.reuters.com/reuters/topNews', 'category': 'General', 'region': 'Global'},
            {'name': 'BBC World', 'url': 'http://feeds.bbci.co.uk/news/world/rss.xml', 'category': 'General', 'region': 'Europe'},
            {'name': 'Al Jazeera', 'url': 'https://www.aljazeera.com/xml/rss/all.xml', 'category': 'General', 'region': 'Middle East'},
            {'name': 'DW', 'url': 'https://rss.dw.com/xml/rss-en-all', 'category': 'General', 'region': 'Europe'},

            # Americas
            {'name': 'CNN', 'url': 'https://rss.cnn.com/rss/edition.rss', 'category': 'General', 'region': 'Americas'},
            {'name': 'AP Top News', 'url': 'https://feeds.apnews.com/apnews/topnews', 'category': 'General', 'region': 'Americas'},
            {'name': 'NYT Home', 'url': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', 'category': 'General', 'region': 'Americas'},
            {'name': 'Washington Post', 'url': 'https://feeds.washingtonpost.com/rss/world', 'category': 'General', 'region': 'Americas'},

            # Europe
            {'name': 'The Guardian World', 'url': 'https://www.theguardian.com/world/rss', 'category': 'General', 'region': 'Europe'},
            {'name': 'France24', 'url': 'https://www.france24.com/en/rss', 'category': 'General', 'region': 'Europe'},
            {'name': 'Euronews', 'url': 'https://www.euronews.com/rss?format=mrss', 'category': 'General', 'region': 'Europe'},

            # Asia
            {'name': 'The Hindu', 'url': 'https://www.thehindu.com/news/feeder/default.rss', 'category': 'General', 'region': 'Asia'},
            {'name': 'Times of India', 'url': 'https://timesofindia.indiatimes.com/rssfeedsdefault.cms', 'category': 'General', 'region': 'Asia'},
            {'name': 'Indian Express', 'url': 'https://indianexpress.com/section/india/feed/', 'category': 'General', 'region': 'Asia'},
            {'name': 'NDTV', 'url': 'https://feeds.feedburner.com/ndtvnews-latest', 'category': 'General', 'region': 'Asia'},
            {'name': 'Channel NewsAsia', 'url': 'https://www.channelnewsasia.com/rssfeeds/8395986', 'category': 'General', 'region': 'Asia'},
            {'name': 'Nikkei Asia', 'url': 'https://asia.nikkei.com/rss/feed/nar', 'category': 'Business', 'region': 'Asia'},
            {'name': 'SCMP', 'url': 'https://www.scmp.com/rss/91/feed', 'category': 'General', 'region': 'Asia'},

            # Middle East
            {'name': 'Arab News', 'url': 'https://www.arabnews.com/rss.xml', 'category': 'General', 'region': 'Middle East'},
            {'name': 'Jerusalem Post', 'url': 'https://www.jpost.com/rss/rssfeedsheadlines.aspx', 'category': 'General', 'region': 'Middle East'},

            # Africa
            {'name': 'AllAfrica', 'url': 'https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf', 'category': 'General', 'region': 'Africa'},
            {'name': 'News24 Africa', 'url': 'https://feeds.24.com/articles/news24/Africa/rss', 'category': 'General', 'region': 'Africa'},

            # Technology / business cross-region
            {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'category': 'Technology', 'region': 'Global'},
            {'name': 'Ars Technica', 'url': 'https://feeds.arstechnica.com/arstechnica/index', 'category': 'Technology', 'region': 'Global'},
            {'name': 'Bloomberg Markets', 'url': 'https://feeds.bloomberg.com/markets/news.rss', 'category': 'Business', 'region': 'Global'},
        ]

    def collect_articles(self, timeout: int = 30, max_articles_per_feed: int = 3) -> List[Dict[str, Any]]:
        """Collect articles from all configured RSS feeds and return raw article dicts."""
        all_articles: List[Dict[str, Any]] = []

        logger.info(f"Starting news collection from {len(self.rss_feeds)} sources")

        max_workers = min(10, max(4, len(self.rss_feeds)))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    self.fetch_feed_articles,
                    feed_info,
                    max_articles_per_feed,
                    timeout,
                )
                for feed_info in self.rss_feeds
            ]
            for future in as_completed(futures):
                try:
                    all_articles.extend(future.result())
                except Exception as e:
                    logger.error(f"Feed collection worker failed: {e}")
                    continue

        # Keep only the latest unique article per URL, and return newest-first.
        unique_by_url = {}
        for article in all_articles:
            url = article.get("url")
            if not url:
                continue
            existing = unique_by_url.get(url)
            if existing is None or article.get("published_date", datetime.min) > existing.get("published_date", datetime.min):
                unique_by_url[url] = article

        all_articles = sorted(
            unique_by_url.values(),
            key=lambda a: a.get("published_date", datetime.min),
            reverse=True,
        )

        logger.info(f"Collected {len(all_articles)} articles total")
        return all_articles
    
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
    
    def fetch_feed_articles(
        self,
        feed_info: Dict[str, Any],
        max_articles: int = 5,
        request_timeout: int = 10,
    ) -> List[Dict[str, Any]]:
        """Fetch articles from a single RSS feed"""
        articles = []
        
        try:
            logger.info(f"Fetching from {feed_info['name']}")
            
            # Fetch RSS feed with timeout
            response = requests.get(feed_info['url'], headers=self.request_headers, timeout=request_timeout)
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
                    parsed = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        parsed = entry.published_parsed
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        parsed = entry.updated_parsed

                    if parsed:
                        try:
                            # feedparser returns a time.struct_time in UTC for typical RSS/Atom feeds.
                            # Convert to a UTC timestamp and then to a naive UTC datetime for storage.
                            pub_date = datetime.utcfromtimestamp(calendar.timegm(parsed))
                        except (ValueError, TypeError, OverflowError):
                            pass
                    
                    # Clean content
                    clean_content = self.clean_html(content)
                    summary = self.extract_summary(clean_content)
                    sentiment = self.analyzer.analyze_sentiment(f"{title}. {clean_content}")
                    
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
                        'region': feed_info.get('region', 'Global'),
                        'sentiment_score': sentiment.get('polarity', 0.0),
                        'sentiment_label': sentiment.get('label', 'neutral'),
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
        """Collect news from all RSS feeds and store in the in-memory article store."""
        all_articles = self.collect_articles(timeout=timeout, max_articles_per_feed=3)
        new_articles_count = article_store.store_articles(all_articles)

        logger.info(
            f"Collection completed. Total articles stored: {len(article_store.articles)}, New articles: {new_articles_count}"
        )
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
                'content': 'World leaders have reached a historic agreement on climate action at the global Summit, committing to ambitious new targets for carbon reduction...',
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
            }
        ]
