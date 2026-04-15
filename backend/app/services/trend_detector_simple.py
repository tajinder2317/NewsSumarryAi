from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
import json
import re

logger = logging.getLogger(__name__)

class TrendDetector:
    def __init__(self):
        pass
    
    def detect_trending_topics(self, articles: List[Dict], time_window_hours: int = 24) -> List[Dict]:
        """Detect trending topics from recent articles using simple keyword analysis"""
        try:
            if not articles:
                return []
            
            # Filter articles by time window
            recent_articles = self._filter_by_time_window(articles, time_window_hours)
            
            if len(recent_articles) < 2:
                return []
            
            # Extract all keywords from recent articles
            all_keywords = []
            for article in recent_articles:
                text = self._extract_text_content(article)
                keywords = self._extract_keywords(text, 10)
                all_keywords.extend(keywords)
            
            # Count keyword frequency
            keyword_counts = Counter(all_keywords)
            
            # Create trending topics from most common keywords
            trending_topics = []
            for keyword, count in keyword_counts.most_common(10):
                if count >= 2:  # Only include keywords that appear in at least 2 articles
                    # Find articles related to this keyword
                    related_articles = []
                    for article in recent_articles:
                        text = self._extract_text_content(article).lower()
                        if keyword.lower() in text:
                            related_articles.append(article)
                    
                    if len(related_articles) >= 2:
                        trending_topics.append({
                            'topic_id': len(trending_topics),
                            'topic_name': keyword.title(),
                            'article_count': len(related_articles),
                            'top_terms': [keyword],
                            'articles': related_articles[:5],
                            'sentiment_distribution': self._calculate_simple_sentiment_dist(related_articles),
                            'trend_score': self._calculate_simple_trend_score(related_articles, time_window_hours)
                        })
            
            # Sort by trend score
            trending_topics.sort(key=lambda x: x['trend_score'], reverse=True)
            return trending_topics[:5]
            
        except Exception as e:
            logger.error(f"Error detecting trending topics: {e}")
            return []
    
    def analyze_topic_trends(self, articles: List[Dict], days_back: int = 7) -> Dict[str, Dict]:
        """Analyze how topics trend over time using simple analysis"""
        try:
            if not articles:
                return {}
            
            # Group articles by day
            daily_articles = self._group_by_day(articles, days_back)
            
            # Track topic frequency over time
            topic_trends = defaultdict(lambda: defaultdict(int))
            
            for day, day_articles in daily_articles.items():
                day_keywords = []
                for article in day_articles:
                    text = self._extract_text_content(article)
                    keywords = self._extract_keywords(text, 5)
                    day_keywords.extend(keywords)
                
                keyword_counts = Counter(day_keywords)
                for keyword, count in keyword_counts.items():
                    if count >= 2:  # Only include keywords that appear multiple times
                        topic_trends[keyword][day] = count
            
            # Calculate trend directions
            trends = {}
            for topic, daily_freq in topic_trends.items():
                trend_direction = self._calculate_simple_trend_direction(daily_freq)
                total_frequency = sum(daily_freq.values())
                
                trends[topic] = {
                    'frequency': total_frequency,
                    'trend_direction': trend_direction,
                    'daily_frequency': dict(daily_freq),
                    'peak_day': max(daily_freq.items(), key=lambda x: x[1])[0] if daily_freq else None
                }
            
            return dict(trends)
            
        except Exception as e:
            logger.error(f"Error analyzing topic trends: {e}")
            return {}
    
    def detect_breaking_news(self, articles: List[Dict], threshold_minutes: int = 60) -> List[Dict]:
        """Detect breaking news based on sudden increase in similar articles"""
        try:
            if not articles:
                return []
            
            # Group recent articles
            recent_time = datetime.utcnow() - timedelta(minutes=threshold_minutes)
            recent_articles = [
                article for article in articles
                if article.get('published_date') and article['published_date'] >= recent_time
            ]
            
            if len(recent_articles) < 3:
                return []
            
            # Find clusters of similar articles using keyword overlap
            breaking_clusters = self._find_keyword_clusters(recent_articles)
            
            # Format breaking news alerts
            breaking_news = []
            for cluster in breaking_clusters:
                if len(cluster) >= 3:  # Threshold for breaking news
                    breaking_news.append({
                        'topic': self._extract_cluster_topic(cluster),
                        'article_count': len(cluster),
                        'articles': cluster[:5],
                        'detected_time': datetime.utcnow().isoformat(),
                        'urgency': self._calculate_urgency(cluster)
                    })
            
            return breaking_news
            
        except Exception as e:
            logger.error(f"Error detecting breaking news: {e}")
            return []
    
    def _filter_by_time_window(self, articles: List[Dict], hours: int) -> List[Dict]:
        """Filter articles within specified time window"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return [
            article for article in articles
            if article.get('published_date') and article['published_date'] >= cutoff_time
        ]
    
    def _extract_text_content(self, article: Dict) -> str:
        """Extract combined text content from article"""
        title = article.get('title', '')
        content = article.get('content', '')
        summary = article.get('summary', '')
        
        return f"{title} {summary} {content}"
    
    def _extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extract keywords from text using simple frequency analysis"""
        try:
            # Convert to lowercase and remove punctuation
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            
            # Split into words
            words = text.split()
            
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just'}
            
            # Filter words
            filtered_words = [word for word in words if len(word) > 2 and word not in stop_words]
            
            # Count frequency
            word_counts = Counter(filtered_words)
            
            # Return most common words
            return [word for word, count in word_counts.most_common(num_keywords)]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def _calculate_simple_sentiment_dist(self, articles: List[Dict]) -> Dict[str, float]:
        """Calculate sentiment distribution for a cluster"""
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for article in articles:
            sentiment = article.get('sentiment_label', 'neutral')
            if sentiment in sentiments:
                sentiments[sentiment] += 1
        
        total = sum(sentiments.values())
        if total > 0:
            for key in sentiments:
                sentiments[key] = sentiments[key] / total
        
        return sentiments
    
    def _calculate_simple_trend_score(self, articles: List[Dict], hours: int) -> float:
        """Calculate trend score for a cluster"""
        if not articles:
            return 0.0
        
        # Simple scoring based on recency and article count
        now = datetime.utcnow()
        recency_score = sum(
            max(0, 1 - (now - article['published_date']).total_seconds() / 3600)
            for article in articles
            if article.get('published_date')
        ) / len(articles)
        
        count_score = min(1.0, len(articles) / 10.0)
        
        return (recency_score * 0.7 + count_score * 0.3)
    
    def _group_by_day(self, articles: List[Dict], days_back: int) -> Dict[str, List[Dict]]:
        """Group articles by day"""
        daily_articles = defaultdict(list)
        
        for article in articles:
            if article.get('published_date'):
                day_key = article['published_date'].strftime('%Y-%m-%d')
                daily_articles[day_key].append(article)
        
        return dict(daily_articles)
    
    def _calculate_simple_trend_direction(self, daily_freq: Dict[str, int]) -> str:
        """Calculate trend direction based on daily frequency"""
        if len(daily_freq) < 2:
            return "stable"
        
        days = sorted(daily_freq.keys())
        recent_avg = sum(daily_freq[day] for day in days[-3:]) / min(3, len(days))
        earlier_avg = sum(daily_freq[day] for day in days[:-3]) / max(1, len(days) - 3)
        
        if recent_avg > earlier_avg * 1.5:
            return "rising"
        elif recent_avg < earlier_avg * 0.7:
            return "falling"
        else:
            return "stable"
    
    def _find_keyword_clusters(self, articles: List[Dict]) -> List[List[Dict]]:
        """Find clusters of similar articles using keyword overlap"""
        clusters = []
        used_articles = set()
        
        for i, article1 in enumerate(articles):
            if article1['id'] in used_articles:
                continue
                
            cluster = [article1]
            keywords1 = set(self._extract_keywords(self._extract_text_content(article1), 10))
            
            for j, article2 in enumerate(articles[i+1:], i+1):
                if article2['id'] in used_articles:
                    continue
                    
                keywords2 = set(self._extract_keywords(self._extract_text_content(article2), 10))
                
                # Calculate keyword overlap
                overlap = len(keywords1.intersection(keywords2))
                total_keywords = len(keywords1.union(keywords2))
                
                if total_keywords > 0 and overlap / total_keywords > 0.3:  # 30% overlap threshold
                    cluster.append(article2)
                    used_articles.add(article2['id'])
            
            if len(cluster) >= 2:
                clusters.append(cluster)
                used_articles.add(article1['id'])
        
        return clusters
    
    def _extract_cluster_topic(self, cluster: List[Dict]) -> str:
        """Extract main topic from article cluster"""
        all_keywords = []
        for article in cluster:
            text = self._extract_text_content(article)
            keywords = self._extract_keywords(text, 5)
            all_keywords.extend(keywords)
        
        keyword_counts = Counter(all_keywords)
        
        if keyword_counts:
            return keyword_counts.most_common(1)[0][0].title()
        return "Unknown Topic"
    
    def _calculate_urgency(self, cluster: List[Dict]) -> str:
        """Calculate urgency level for breaking news"""
        if len(cluster) >= 10:
            return "high"
        elif len(cluster) >= 5:
            return "medium"
        else:
            return "low"
