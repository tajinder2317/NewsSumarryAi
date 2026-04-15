from textblob import TextBlob
from typing import List, Dict
import logging
import re
import json

logger = logging.getLogger(__name__)

class TextAnalyzer:
    def __init__(self):
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
        except Exception as e:
            logger.warning(f"Error downloading NLTK data: {e}")

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Convert polarity to label
            if polarity > 0.1:
                label = "positive"
            elif polarity < -0.1:
                label = "negative"
            else:
                label = "neutral"
            
            return {
                "polarity": polarity,
                "subjectivity": blob.sentiment.subjectivity,
                "label": label,
                "confidence": abs(polarity)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"polarity": 0.0, "subjectivity": 0.0, "label": "neutral", "confidence": 0.0}

    def extract_topics(self, texts: List[str], num_topics: int = 5) -> List[Dict]:
        """Extract topics using simple keyword extraction"""
        try:
            # Simple keyword-based topic extraction
            all_words = []
            for text in texts:
                words = self._extract_keywords(text, 20)
                all_words.extend(words)
            
            # Count word frequency
            from collections import Counter
            word_counts = Counter(all_words)
            
            # Create topics from most common words
            topics = []
            common_words = word_counts.most_common(num_topics * 3)
            
            for i in range(0, min(len(common_words), num_topics * 3), 3):
                topic_words = common_words[i:i+3]
                if topic_words:
                    topics.append({
                        "topic_id": i // 3,
                        "words": [word for word, count in topic_words],
                        "weights": [count for word, count in topic_words],
                        "label": self._generate_topic_label([word for word, count in topic_words])
                    })
            
            return topics[:num_topics]
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []

    def categorize_text(self, text: str) -> str:
        """Categorize text into predefined categories"""
        categories = {
            'politics': ['government', 'election', 'president', 'congress', 'senate', 'policy', 'political'],
            'technology': ['technology', 'tech', 'software', 'computer', 'internet', 'digital', 'ai', 'artificial intelligence'],
            'sports': ['sport', 'game', 'team', 'player', 'match', 'championship', 'league'],
            'business': ['business', 'economy', 'market', 'financial', 'company', 'corporate', 'stock'],
            'health': ['health', 'medical', 'hospital', 'disease', 'treatment', 'doctor', 'patient'],
            'entertainment': ['movie', 'music', 'celebrity', 'film', 'actor', 'singer', 'show'],
            'science': ['science', 'research', 'study', 'university', 'scientist', 'discovery'],
            'world': ['international', 'global', 'country', 'nation', 'foreign', 'diplomatic']
        }
        
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        if max(scores.values()) == 0:
            return 'general'
        
        return max(scores, key=scores.get)

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
            from collections import Counter
            word_counts = Counter(filtered_words)
            
            # Return most common words
            return [word for word, count in word_counts.most_common(num_keywords)]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

    def _generate_topic_label(self, words: List[str]) -> str:
        """Generate a label for topic based on top words"""
        if not words:
            return "Unknown"
        
        # Simple heuristic: use first 2-3 words
        return ' '.join(words[:3]).title()

    def get_text_statistics(self, text: str) -> Dict:
        """Get basic text statistics"""
        try:
            words = text.split()
            sentences = text.split('.')
            
            return {
                "word_count": len(words),
                "sentence_count": len([s for s in sentences if s.strip()]),
                "avg_words_per_sentence": len(words) / max(1, len(sentences)),
                "char_count": len(text),
                "char_count_no_spaces": len(text.replace(' ', ''))
            }
        except Exception as e:
            logger.error(f"Error calculating text statistics: {e}")
            return {}
