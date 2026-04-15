from typing import List, Dict
import logging
from textblob import TextBlob
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self):
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('english'))
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            import nltk
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except Exception as e:
            logger.warning(f"Error downloading NLTK data: {e}")

    def summarize_article(self, text: str, max_sentences: int = 3) -> str:
        """Summarize article using extractive summarization"""
        try:
            if not text or len(text.strip()) < 50:
                return "Content too short to summarize."
            
            # Improved sentence tokenization - split on common sentence delimiters
            sentences = self._improved_sentence_tokenize(text)
            
            # Handle case where text has very few sentences
            if len(sentences) == 1:
                if max_sentences == 1:
                    return sentences[0]
                else:
                    return sentences[0] + f" [Single sentence content - requested {max_sentences} sentences, but only 1 available]"
            
            if len(sentences) <= max_sentences:
                return " ".join(sentences)
            
            # Calculate sentence scores
            sentence_scores = self._calculate_sentence_scores(sentences)
            
            # Get top sentences
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_sentences]
            top_sentences = sorted(top_sentences, key=lambda x: sentences.index(x[0]))
            
            summary = ' '.join([sentence for sentence, score in top_sentences])
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return text[:200] + "..." if len(text) > 200 else text

    def _improved_sentence_tokenize(self, text: str) -> List[str]:
        """Improved sentence tokenization that handles complex sentences"""
        try:
            # First try NLTK tokenizer
            sentences = sent_tokenize(text)
            
            # If NLTK doesn't split well, use custom splitting
            if len(sentences) == 1 and len(text) > 200:
                # Split on common sentence delimiters
                import re
                # Split on periods, question marks, exclamation marks, and semicolons
                custom_sentences = re.split(r'[.!?;]+', text)
                # Clean up and filter out empty strings
                custom_sentences = [s.strip() for s in custom_sentences if s.strip() and len(s.strip()) > 10]
                
                if len(custom_sentences) > 1:
                    return custom_sentences
            
            return sentences
            
        except Exception as e:
            logger.error(f"Error in sentence tokenization: {e}")
            # Fallback to simple splitting
            import re
            sentences = re.split(r'[.!?;]+', text)
            return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    def _calculate_sentence_scores(self, sentences: List[str]) -> Dict[str, float]:
        """Calculate importance scores for sentences"""
        try:
            # Build similarity matrix
            similarity_matrix = self._build_similarity_matrix(sentences)
            
            # Apply PageRank algorithm
            nx_graph = nx.from_numpy_array(similarity_matrix)
            scores = nx.pagerank(nx_graph)
            
            return {sentences[i]: scores[i] for i in range(len(sentences))}
            
        except Exception as e:
            logger.error(f"Error calculating sentence scores: {e}")
            return {sentence: 1.0 for sentence in sentences}

    def _build_similarity_matrix(self, sentences: List[str]) -> np.ndarray:
        """Build similarity matrix between sentences"""
        try:
            # Clean sentences
            clean_sentences = [self._clean_sentence(sentence) for sentence in sentences]
            
            # Create similarity matrix
            similarity_matrix = np.zeros((len(sentences), len(sentences)))
            
            for i in range(len(sentences)):
                for j in range(len(sentences)):
                    if i != j:
                        similarity_matrix[i][j] = self._sentence_similarity(
                            clean_sentences[i], clean_sentences[j]
                        )
            
            return similarity_matrix
            
        except Exception as e:
            logger.error(f"Error building similarity matrix: {e}")
            return np.eye(len(sentences))

    def _clean_sentence(self, sentence: str) -> str:
        """Clean and preprocess sentence"""
        # Convert to lowercase and remove special characters
        sentence = re.sub(r'[^a-zA-Z\s]', '', sentence.lower())
        
        # Remove stopwords
        words = sentence.split()
        words = [word for word in words if word not in self.stop_words]
        
        return ' '.join(words)

    def _sentence_similarity(self, sentence1: str, sentence2: str) -> float:
        """Calculate similarity between two sentences"""
        try:
            words1 = set(sentence1.split())
            words2 = set(sentence2.split())
            
            if not words1 or not words2:
                return 0.0
            
            # Jaccard similarity
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
            
        except Exception as e:
            logger.error(f"Error calculating sentence similarity: {e}")
            return 0.0

    def summarize_multiple_articles(self, articles: List[Dict], max_sentences: int = 5) -> str:
        """Summarize multiple articles into one summary"""
        try:
            if not articles:
                return ""
            
            # Extract titles and content
            texts = []
            for article in articles:
                title = article.get('title', '')
                content = article.get('content', '')
                if title:
                    texts.append(title)
                if content:
                    texts.append(content)
            
            # Combine all text
            combined_text = ' '.join(texts)
            
            # Summarize the combined text
            return self.summarize_article(combined_text, max_sentences)
            
        except Exception as e:
            logger.error(f"Error summarizing multiple articles: {e}")
            return ""

    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """Extract key points from text"""
        try:
            sentences = sent_tokenize(text)
            if len(sentences) <= num_points:
                return sentences
            
            # Calculate sentence scores
            sentence_scores = self._calculate_sentence_scores(sentences)
            
            # Get top sentences as key points
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_points]
            
            return [sentence for sentence, score in top_sentences]
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []

    def generate_headline(self, text: str) -> str:
        """Generate a headline for the text"""
        try:
            # Get first sentence or first 100 characters
            sentences = sent_tokenize(text)
            if sentences:
                headline = sentences[0]
            else:
                headline = text[:100]
            
            # Clean up headline
            headline = headline.strip()
            if len(headline) > 100:
                headline = headline[:97] + "..."
            
            return headline
            
        except Exception as e:
            logger.error(f"Error generating headline: {e}")
            return text[:50] + "..." if len(text) > 50 else text
