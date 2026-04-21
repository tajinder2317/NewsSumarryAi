import { newsAPI, analysisAPI, trendsAPI } from "./api";

// News service functions
export const newsService = {
  // Fetch news articles
  fetchNews: async (params = {}) => {
    try {
      const response = await newsAPI.getNews(params);
      console.log("News API response:", response);

      // Simple response handling - just return what we get
      if (response && response.data) {
        return { articles: response.data };
      } else if (response && Array.isArray(response)) {
        return { articles: response };
      } else if (response && response.articles) {
        return { articles: response.articles };
      } else {
        console.warn("Unexpected response format:", response);
        return { articles: [] };
      }
    } catch (error) {
      console.error("News API error:", error);
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
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch sources: ${error.message}`);
    }
  },

  // Get news categories
  getCategories: async () => {
    try {
      const response = await newsAPI.getCategories();
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch categories: ${error.message}`);
    }
  },

  // Get news statistics
  getStats: async () => {
    try {
      const response = await newsAPI.getStats();
      // Handle different response formats
      if (response && typeof response === "object") {
        // If response has data property, use that
        if (response.data) {
          return response.data;
        }
        // Otherwise, return the response directly
        return response;
      }
      return response;
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
      const response = await analysisAPI.analyzeSentiment(articleIds);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to analyze sentiment: ${error.message}`);
    }
  },

  // Extract topics
  analyzeTopics: async (articleIds) => {
    try {
      const response = await analysisAPI.analyzeTopics(articleIds);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to analyze topics: ${error.message}`);
    }
  },

  // Summarize articles
  summarizeArticles: async (articleIds, maxSentences = 3) => {
    try {
      const response = await analysisAPI.summarizeArticles(
        articleIds,
        maxSentences,
      );
      return response.data;
    } catch (error) {
      throw new Error(`Failed to summarize articles: ${error.message}`);
    }
  },

  // Extract keywords
  extractKeywords: async (articleIds, numKeywords = 10) => {
    try {
      const response = await analysisAPI.extractKeywords(
        articleIds,
        numKeywords,
      );
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
      // Handle different response formats
      if (response && typeof response === "object") {
        // If response has data property, use that
        if (response.data) {
          return response.data;
        }
        // Otherwise, return the response directly
        return response;
      }
      return response;
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
      // Handle different response formats
      if (response && typeof response === "object") {
        // If response has data property, use that
        if (response.data) {
          return response.data;
        }
        // Otherwise, return the response directly
        return response;
      }
      return response;
    } catch (error) {
      throw new Error(`Failed to fetch trends summary: ${error.message}`);
    }
  },
};
