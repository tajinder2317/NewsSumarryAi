from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

logger = logging.getLogger(__name__)

class TrendDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
    
    def detect_trending_topics(self, articles: List[Dict], time_window_hours: int = 24) -> List[Dict]:
        """Detect trending topics from recent articles"""
        try:
            if not articles:
                return []
            
            # Filter articles by time window
            recent_articles = self._filter_by_time_window(articles, time_window_hours)
            
            if len(recent_articles) < 2:
                return []
            
            # Extract text content
            texts = [self._extract_text_content(article) for article in recent_articles]
            texts = [text for text in texts if text.strip()]
            
            if not texts:
                return []
            
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Apply clustering to identify topics
            num_clusters = min(10, len(texts) // 2)
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(tfidf_matrix)
            
            # Analyze clusters to identify trends
            trending_topics = self._analyze_clusters(
                texts, cluster_labels, recent_articles, kmeans.cluster_centers_
            )
            
            return trending_topics
            
        except Exception as e:
            logger.error(f"Error detecting trending topics: {e}")
            return []
    
    def analyze_topic_trends(self, articles: List[Dict], days_back: int = 7) -> Dict[str, Dict]:
        """Analyze how topics trend over time"""
        try:
            if not articles:
                return {}
            
            # Group articles by day
            daily_articles = self._group_by_day(articles, days_back)
            
            # Track topic frequency over time
            topic_trends = defaultdict(lambda: defaultdict(int))
            
            for day, day_articles in daily_articles.items():
                day_topics = self._extract_topics_from_articles(day_articles)
                
                for topic, frequency in day_topics.items():
                    topic_trends[topic][day] = frequency
            
            # Calculate trend directions
            trends = {}
            for topic, daily_freq in topic_trends.items():
                trend_direction = self._calculate_trend_direction(daily_freq)
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
            
            # Find clusters of similar articles
            breaking_clusters = self._find_similar_article_clusters(recent_articles)
            
            # Format breaking news alerts
            breaking_news = []
            for cluster in breaking_clusters:
                if len(cluster) >= 3:  # Threshold for breaking news
                    breaking_news.append({
                        'topic': self._extract_cluster_topic(cluster),
                        'article_count': len(cluster),
                        'articles': cluster[:5],  # Limit to top 5
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
    
    def _analyze_clusters(self, texts: List[str], labels: np.ndarray, articles: List[Dict], centers: np.ndarray) -> List[Dict]:
        """Analyze clusters to identify trending topics"""
        trending_topics = []
        
        for cluster_id in range(len(set(labels))):
            cluster_indices = np.where(labels == cluster_id)[0]
            
            if len(cluster_indices) < 2:
                continue
            
            # Extract articles in this cluster
            cluster_articles = [articles[i] for i in cluster_indices]
            cluster_texts = [texts[i] for i in cluster_indices]
            
            # Get top terms for this cluster
            top_terms = self._get_top_terms_for_cluster(centers[cluster_id])
            
            # Calculate cluster metrics
            trending_topics.append({
                'topic_id': cluster_id,
                'topic_name': self._generate_topic_name(top_terms),
                'article_count': len(cluster_articles),
                'top_terms': top_terms,
                'articles': cluster_articles[:5],  # Limit to top 5
                'sentiment_distribution': self._calculate_cluster_sentiment(cluster_articles),
                'trend_score': self._calculate_trend_score(cluster_articles)
            })
        
        # Sort by trend score
        trending_topics.sort(key=lambda x: x['trend_score'], reverse=True)
        return trending_topics[:10]  # Return top 10
    
    def _get_top_terms_for_cluster(self, center: np.ndarray, top_n: int = 5) -> List[str]:
        """Get top terms for a cluster center"""
        feature_names = self.vectorizer.get_feature_names_out()
        top_indices = center.argsort()[-top_n:][::-1]
        return [feature_names[i] for i in top_indices]
    
    def _generate_topic_name(self, terms: List[str]) -> str:
        """Generate a topic name from top terms"""
        if not terms:
            return "Unknown Topic"
        return ' '.join(terms[:3]).title()
    
    def _calculate_cluster_sentiment(self, articles: List[Dict]) -> Dict[str, float]:
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
    
    def _calculate_trend_score(self, articles: List[Dict]) -> float:
        """Calculate trend score for a cluster"""
        # Simple scoring based on recency and article count
        if not articles:
            return 0.0
        
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
    
    def _extract_topics_from_articles(self, articles: List[Dict]) -> Counter:
        """Extract topics from articles"""
        all_text = ' '.join([self._extract_text_content(article) for article in articles])
        words = re.findall(r'\b\w+\b', all_text.lower())
        
        # Simple keyword extraction
        common_words = Counter(word for word in words if len(word) > 3)
        return common_words.most_common(20)
    
    def _calculate_trend_direction(self, daily_freq: Dict[str, int]) -> str:
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
    
    def _find_similar_article_clusters(self, articles: List[Dict]) -> List[List[Dict]]:
        """Find clusters of similar articles"""
        texts = [self._extract_text_content(article) for article in articles]
        texts = [text for text in texts if text.strip()]
        
        if len(texts) < 3:
            return []
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        # Apply clustering
        num_clusters = min(5, len(texts) // 3)
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Group articles by cluster
        clusters = defaultdict(list)
        for i, label in enumerate(cluster_labels):
            clusters[label].append(articles[i])
        
        return list(clusters.values())
    
    def _extract_cluster_topic(self, cluster: List[Dict]) -> str:
        """Extract main topic from article cluster"""
        all_titles = ' '.join([article.get('title', '') for article in cluster])
        words = re.findall(r'\b\w+\b', all_titles.lower())
        common_words = Counter(word for word in words if len(word) > 4)
        
        if common_words:
            return common_words.most_common(1)[0][0].title()
        return "Unknown Topic"
    
    def _calculate_urgency(self, cluster: List[Dict]) -> str:
        """Calculate urgency level for breaking news"""
        if len(cluster) >= 10:
            return "high"
        elif len(cluster) >= 5:
            return "medium"
        else:
            return "low"
