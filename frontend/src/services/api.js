import axios from 'axios';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add auth token here if needed
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data);
    
    // Log specific errors for debugging
    if (error.response?.status === 404) {
      console.error('API Endpoint Not Found:', error.config?.url);
    } else if (error.response?.status >= 500) {
      console.error('Server Error:', error.response?.data);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request Timeout:', error.message);
    }
    
    // Handle common error cases
    if (error.response?.status === 404) {
      throw new Error('Resource not found');
    } else if (error.response?.status === 500) {
      throw new Error('Server error. Please try again later.');
    } else if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please check your connection.');
    }
    
    throw error;
  }
);

// News API endpoints
export const newsAPI = {
  // Get all news with optional filters
  getNews: (params = {}) => {
    return api.get('/api/v1/news/', { params });
  },
  
  // Get specific article by ID
  getArticle: (id) => {
    return api.get(`/api/v1/news/${id}`);
  },
  
  // Search news articles
  searchNews: (searchData) => {
    return api.post('/api/v1/news/search', searchData);
  },
  
  // Collect news from sources
  collectNews: () => {
    return api.post('/api/v1/news/collect');
  },
  
  // Get news sources
  getSources: () => {
    return api.get('/api/v1/news/sources/list');
  },
  
  // Get news categories
  getCategories: () => {
    return api.get('/api/v1/news/categories');
  },
  
  // Get news statistics
  getStats: () => {
    return api.get('/api/v1/news/stats/summary');
  },
  
  // Delete article
  deleteArticle: (id) => {
    return api.delete(`/api/v1/news/${id}`);
  },
};

// Analysis API endpoints
export const analysisAPI = {
  // Analyze sentiment
  analyzeSentiment: (articleIds) => {
    return api.post('/api/v1/analysis/sentiment', { article_ids: articleIds });
  },
  
  // Extract topics
  analyzeTopics: (articleIds) => {
    return api.post('/api/v1/analysis/topics', { article_ids: articleIds });
  },
  
  // Summarize articles
  summarizeArticles: (articleIds, maxSentences = 3) => {
    return api.post('/api/v1/analysis/summarize', { article_ids: articleIds, max_sentences: maxSentences });
  },
  
  // Extract keywords
  extractKeywords: (articleIds, numKeywords = 10) => {
    return api.post('/api/v1/analysis/keywords', { article_ids: articleIds, num_keywords: numKeywords });
  },
  
  // Categorize articles
  categorizeArticles: (articleIds) => {
    return api.post('/api/v1/analysis/categorize', { article_ids: articleIds });
  },
  
  // Get analysis statistics
  getStats: () => {
    return api.get('/api/v1/analysis/statistics');
  },
};

// Trends API endpoints
export const trendsAPI = {
  // Get trending topics
  getTrendingTopics: (hours = 24) => {
    return api.get('/api/v1/trends/topics', { params: { hours } });
  },
  
  // Get topic trends analysis
  getTopicTrends: (days = 7) => {
    return api.get('/api/v1/trends/analysis', { params: { days } });
  },
  
  // Get breaking news
  getBreakingNews: (minutes = 60) => {
    return api.get('/api/v1/trends/breaking', { params: { minutes } });
  },
  
  // Get sentiment trends
  getSentimentTrends: (days = 7) => {
    return api.get('/api/v1/trends/sentiment-trends', { params: { days } });
  },
  
  // Get source trends
  getSourceTrends: (days = 7) => {
    return api.get('/api/v1/trends/source-trends', { params: { days } });
  },
  
  // Get trends summary
  getTrendsSummary: (hours = 24) => {
    return api.get('/api/v1/trends/summary', { params: { hours } });
  },
};

// Health check
export const healthAPI = {
  check: () => {
    return api.get('/health');
  },
};

export default api;
