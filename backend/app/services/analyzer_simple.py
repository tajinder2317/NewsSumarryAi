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
            
            # Convert polarity to label.
            # Lower thresholds help avoid everything being classified as neutral for concise headlines.
            if polarity > 0.03:
                label = "positive"
            elif polarity < -0.03:
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
        """Extract topics using improved keyword clustering"""
        try:
            # Combine all texts for analysis
            combined_text = ' '.join(texts)
            
            # Extract keywords with higher frequency threshold
            all_keywords = self._extract_keywords(combined_text, 50)
            
            # Group related keywords into topics
            topic_groups = self._group_keywords_into_topics(all_keywords, num_topics)
            
            topics = []
            for i, (topic_words, topic_label) in enumerate(topic_groups):
                # Calculate weights based on word frequency in the original text
                weights = []
                for word in topic_words:
                    weight = combined_text.lower().count(word.lower())
                    weights.append(weight)
                
                topics.append({
                    "topic_id": i,
                    "words": topic_words,
                    "weights": weights,
                    "label": topic_label
                })
            
            return topics[:num_topics]
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []

    def _group_keywords_into_topics(self, keywords: List[str], num_topics: int) -> List[tuple]:
        """Group related keywords into coherent topics"""
        try:
            # Simple topic grouping based on semantic categories
            topic_categories = {
                'Politics & Government': ['government', 'policy', 'political', 'election', 'president', 'congress', 'senate', 'law', 'legal', 'court', 'judge', 'minister'],
                'Technology & Science': ['technology', 'tech', 'software', 'computer', 'internet', 'digital', 'ai', 'artificial', 'intelligence', 'data', 'science', 'research', 'study'],
                'Business & Economy': ['business', 'economy', 'market', 'financial', 'company', 'corporate', 'stock', 'trade', 'economic', 'revenue', 'profit', 'investment'],
                'Health & Medicine': ['health', 'medical', 'hospital', 'disease', 'treatment', 'doctor', 'patient', 'medicine', 'clinical', 'drug', 'pharmaceutical', 'therapy'],
                'Social Issues': ['social', 'society', 'community', 'people', 'public', 'rights', 'justice', 'equality', 'diversity', 'inclusion', 'welfare'],
                'International Affairs': ['international', 'global', 'world', 'foreign', 'diplomatic', 'country', 'nation', 'border', 'immigration', 'refugee', 'asylum'],
                'Media & Communication': ['media', 'news', 'report', 'journalist', 'broadcast', 'publication', 'article', 'story', 'information', 'communication'],
                'Crime & Legal': ['crime', 'criminal', 'legal', 'law', 'court', 'police', 'investigation', 'arrest', 'trial', 'justice', 'case']
            }
            
            # Categorize keywords
            categorized_topics = {}
            uncategorized_keywords = []
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                assigned = False
                
                for category, category_words in topic_categories.items():
                    if keyword_lower in category_words:
                        if category not in categorized_topics:
                            categorized_topics[category] = []
                        categorized_topics[category].append(keyword)
                        assigned = True
                        break
                
                if not assigned:
                    uncategorized_keywords.append(keyword)
            
            # Build topic list
            topic_groups = []
            
            # Add categorized topics first
            for category, words in list(categorized_topics.items())[:num_topics-1]:
                if words:
                    topic_groups.append((words[:3], category))
            
            # Add remaining uncategorized keywords as a general topic
            if uncategorized_keywords and len(topic_groups) < num_topics:
                topic_groups.append((uncategorized_keywords[:3], "General Topics"))
            
            # If no topics found, create simple frequency-based topics
            if not topic_groups and keywords:
                for i in range(0, min(len(keywords), num_topics * 3), 3):
                    topic_words = keywords[i:i+3]
                    if topic_words:
                        topic_groups.append((topic_words, f"Topic {i//3 + 1}"))
            
            return topic_groups[:num_topics]
            
        except Exception as e:
            logger.error(f"Error grouping keywords into topics: {e}")
            # Fallback to simple grouping
            topic_groups = []
            for i in range(0, min(len(keywords), num_topics * 3), 3):
                topic_words = keywords[i:i+3]
                if topic_words:
                    topic_groups.append((topic_words, f"Topic {i//3 + 1}"))
            return topic_groups[:num_topics]

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
