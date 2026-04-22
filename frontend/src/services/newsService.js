import { newsAPI, analysisAPI, trendsAPI } from "./api";

const normalizeArticles = (data) => {
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.articles)) return data.articles;
  return [];
};

const normalizePage = (data) => {
  if (!data || typeof data !== 'object') return { items: [], total: 0, page: 1, page_size: 50 };
  const items = Array.isArray(data.items) ? data.items : normalizeArticles(data);
  const total = typeof data.total === 'number' ? data.total : items.length;
  const page = typeof data.page === 'number' ? data.page : 1;
  const page_size = typeof data.page_size === 'number' ? data.page_size : 50;
  return { items, total, page, page_size };
};

const normalizeStringList = (data) => {
  if (Array.isArray(data)) return data;
  return [];
};

// News service functions
export const newsService = {
  // Fetch news articles
  fetchNews: async (params = {}) => {
    try {
      const response = await newsAPI.getNews(params);
      console.log("News API response:", response);

      return normalizeArticles(response?.data);
    } catch (error) {
      console.error("News API error:", error);
      throw new Error(`Failed to fetch news: ${error.message}`);
    }
  },

  // Fetch the freshest news (default: last 5 minutes)
  fetchLatest: async (params = {}) => {
    try {
      const response = await newsAPI.getLatest(params);
      return normalizeArticles(response?.data);
    } catch (error) {
      throw new Error(`Failed to fetch latest news: ${error.message}`);
    }
  },

  // Fetch paged news with totals (for proper pagination UI)
  fetchNewsPaged: async (params = {}) => {
    try {
      const response = await newsAPI.getNewsPaged(params);
      return normalizePage(response?.data);
    } catch (error) {
      throw new Error(`Failed to fetch news: ${error.message}`);
    }
  },

  // Fetch single article
  fetchArticle: async (id) => {
    try {
      const response = await newsAPI.getArticle(id);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch article: ${error.message}`);
    }
  },

  // Search news articles
  searchNews: async (searchData) => {
    try {
      const response = await newsAPI.searchNews(searchData);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to search news: ${error.message}`);
    }
  },

  // Collect news from sources
  collectNews: async () => {
    try {
      const response = await newsAPI.collectNews();
      return response.data;
    } catch (error) {
      throw new Error(`Failed to collect news: ${error.message}`);
    }
  },

  // Get news sources
  getSources: async () => {
    try {
      const response = await newsAPI.getSources();
      const data = response?.data;
      if (data && Array.isArray(data.sources)) return data;
      return { sources: normalizeStringList(data) };
    } catch (error) {
      throw new Error(`Failed to fetch sources: ${error.message}`);
    }
  },

  // Get news categories
  getCategories: async () => {
    try {
      const response = await newsAPI.getCategories();
      const data = response?.data;
      if (data && Array.isArray(data.categories)) return data;
      return { categories: normalizeStringList(data) };
    } catch (error) {
      throw new Error(`Failed to fetch categories: ${error.message}`);
    }
  },

  // Get news statistics
  getStats: async () => {
    try {
      const response = await newsAPI.getStats();
      return response?.data;
    } catch (error) {
      throw new Error(`Failed to fetch stats: ${error.message}`);
    }
  },

  // Delete article
  deleteArticle: async (id) => {
    try {
      await newsAPI.deleteArticle(id);
      return true;
    } catch (error) {
      throw new Error(`Failed to delete article: ${error.message}`);
    }
  },
};

// Analysis service functions
export const analysisService = {
  // Analyze sentiment
  analyzeSentiment: async (articleIds) => {
    try {
      const ids = Array.isArray(articleIds)
        ? articleIds
        : (articleIds && Array.isArray(articleIds.articleIds) ? articleIds.articleIds : []);

      const response = await analysisAPI.analyzeSentiment(ids);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to analyze sentiment: ${error.message}`);
    }
  },

  // Extract topics
  analyzeTopics: async (articleIds) => {
    try {
      const ids = Array.isArray(articleIds)
        ? articleIds
        : (articleIds && Array.isArray(articleIds.articleIds) ? articleIds.articleIds : []);

      const response = await analysisAPI.analyzeTopics(ids);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to analyze topics: ${error.message}`);
    }
  },

  // Summarize articles
  summarizeArticles: async (variables) => {
    try {
      const articleIds = Array.isArray(variables) ? variables : variables?.articleIds;
      const maxSentences = variables?.maxSentences ?? 3;

      const response = await analysisAPI.summarizeArticles(articleIds || [], maxSentences);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to summarize articles: ${error.message}`);
    }
  },

  // Extract keywords
  extractKeywords: async (variables) => {
    try {
      const articleIds = Array.isArray(variables) ? variables : variables?.articleIds;
      const numKeywords = variables?.numKeywords ?? 10;

      const response = await analysisAPI.extractKeywords(articleIds || [], numKeywords);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to extract keywords: ${error.message}`);
    }
  },

  // Categorize articles
  categorizeArticles: async (articleIds) => {
    try {
      const response = await analysisAPI.categorizeArticles(articleIds);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to categorize articles: ${error.message}`);
    }
  },

  // Get analysis statistics
  getAnalysisStats: async () => {
    try {
      const response = await analysisAPI.getStats();
      return response?.data;
    } catch (error) {
      throw new Error(`Failed to fetch analysis stats: ${error.message}`);
    }
  },
};

// Trends service functions
export const trendsService = {
  // Get trending topics
  getTrendingTopics: async (hours = 24) => {
    try {
      const response = await trendsAPI.getTrendingTopics(hours);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch trending topics: ${error.message}`);
    }
  },

  // Get topic trends analysis
  getTopicTrends: async (days = 7) => {
    try {
      const response = await trendsAPI.getTopicTrends(days);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch topic trends: ${error.message}`);
    }
  },

  // Get breaking news
  getBreakingNews: async (minutes = 60) => {
    try {
      const response = await trendsAPI.getBreakingNews(minutes);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch breaking news: ${error.message}`);
    }
  },

  // Get sentiment trends
  getSentimentTrends: async (days = 7) => {
    try {
      const response = await trendsAPI.getSentimentTrends(days);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch sentiment trends: ${error.message}`);
    }
  },

  // Get source trends
  getSourceTrends: async (days = 7) => {
    try {
      const response = await trendsAPI.getSourceTrends(days);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch source trends: ${error.message}`);
    }
  },

  // Get trends summary
  getTrendsSummary: async (hours = 24) => {
    try {
      const response = await trendsAPI.getTrendsSummary(hours);
      return response?.data;
    } catch (error) {
      throw new Error(`Failed to fetch trends summary: ${error.message}`);
    }
  },
};
