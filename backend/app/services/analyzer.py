from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
from typing import List, Dict, Tuple
import logging
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

logger = logging.getLogger(__name__)

class TextAnalyzer:
    def __init__(self):
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('english'))
        
    def _download_nltk_data(self):
        """Download required NLTK data"""
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
        """Extract topics using LDA"""
        try:
            if len(texts) < num_topics:
                num_topics = max(1, len(texts))
            
            # Preprocess texts
            processed_texts = [self._preprocess_text(text) for text in texts]
            processed_texts = [text for text in processed_texts if text.strip()]
            
            if not processed_texts:
                return []
            
            # Create TF-IDF matrix
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2)
            )
            tfidf_matrix = vectorizer.fit_transform(processed_texts)
            
            # Apply LDA
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                random_state=42,
                max_iter=100
            )
            lda.fit(tfidf_matrix)
            
            # Extract topics
            feature_names = vectorizer.get_feature_names_out()
            topics = []
            
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[-10:][::-1]
                top_words = [feature_names[i] for i in top_words_idx]
                top_weights = [float(topic[i]) for i in top_words_idx]
                
                topics.append({
                    "topic_id": topic_idx,
                    "words": top_words,
                    "weights": top_weights,
                    "label": self._generate_topic_label(top_words[:3])
                })
            
            return topics
            
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

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)

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

    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """Extract keywords from text using TF-IDF"""
        try:
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            if not processed_text.strip():
                return []
            
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                max_features=num_keywords,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Fit and transform
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()[0]
            
            # Get top keywords
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores[:num_keywords]]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
