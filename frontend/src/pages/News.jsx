import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
  Divider,
} from '@mui/material';
import { Refresh } from '@mui/icons-material';

import { newsService } from '../services/newsService';
import NewsList from '../components/news/NewsList';
import NewsCard from '../components/news/NewsCard';

const NewsPage = () => {
  const FRESH_MINUTES = 5;
  const [filters, setFilters] = useState({
    source: '',
    category: '',
    sentiment: '',
    region: '',
  });
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 20;

  const {
    data: latestArticles = [],
    isLoading: latestLoading,
    error: latestError,
    refetch: refetchLatest,
  } = useQuery(
    ['latestNews', { minutes: FRESH_MINUTES, ...filters }],
    () => newsService.fetchLatest({
      minutes: FRESH_MINUTES,
      limit: 20,
      refresh: true,
      // Keep latest view consistent with filters when they’re applied.
      source: filters.source || undefined,
      category: filters.category || undefined,
      region: filters.region || undefined,
    }),
    {
      retry: 1,
      staleTime: 30 * 1000,
      refetchInterval: 120 * 1000,
      keepPreviousData: true,
      onError: (error) => {
        console.error('Latest news fetch error:', error);
      },
    }
  );

  // Fetch news articles
  const {
    data: articles = [],
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['news', { page: currentPage, limit, ...filters }],
    () => newsService.fetchNews({
      skip: (currentPage - 1) * limit,
      limit,
      source: filters.source || undefined,
      category: filters.category || undefined,
      region: filters.region || undefined,
    }),
    {
      keepPreviousData: true,
      retry: 2,
      onError: (error) => {
        console.error('News fetch error:', error);
      },
    }
  );

  // Fetch sources and categories for filters
  const {
    data: sources,
  } = useQuery('newsSources', newsService.getSources, {
    staleTime: 30 * 60 * 1000,
  });

  const {
    data: categories,
  } = useQuery('newsCategories', newsService.getCategories, {
    staleTime: 30 * 60 * 1000,
  });

  const handleFilterChange = (filterType, value) => {
    if (filterType === 'clear') {
      setFilters({
        source: '',
        category: '',
        sentiment: '',
        region: '',
      });
      setCurrentPage(1);
      return;
    }

    setFilters(prev => ({
      ...prev,
      [filterType]: value,
    }));
    setCurrentPage(1); // Reset to first page when filter changes
  };

  const handlePageChange = (event, page) => {
    setCurrentPage(page);
  };

  const handleRefresh = () => {
    refetchLatest();
    refetch();
  };

  return (
    <Container maxWidth="lg" sx={{ py: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: { xs: 'stretch', sm: 'center' }, mb: 4, gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
        <Typography variant="h4" component="h1" sx={{ fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
          Latest News (updates every 2 min)
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          disabled={isLoading || latestLoading}
          sx={{ width: { xs: '100%', sm: 'auto' } }}
        >
          Refresh
        </Button>
      </Box>

      {(error || latestError) && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading news: {(latestError || error).message}
        </Alert>
      )}

      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 1 }}>
          Fresh (last {FRESH_MINUTES} minutes)
        </Typography>
        {!latestLoading && (latestArticles || []).length === 0 && (
          <Alert severity="info" sx={{ mb: 2 }}>
            No articles were published in the last {FRESH_MINUTES} minutes from the current sources. Showing the most recent articles below.
          </Alert>
        )}
        {(latestArticles || []).map((article) => (
          <NewsCard key={article.url || article.id} article={article} />
        ))}
      </Box>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" sx={{ mb: 1 }}>
        All News
      </Typography>

      <NewsList
        articles={articles || []}
        loading={isLoading}
        error={error?.message}
        onRefresh={handleRefresh}
        pagination={{
          page: currentPage,
          limit,
        }}
        onPageChange={handlePageChange}
        totalCount={articles?.length >= limit ? undefined : articles?.length}
        filters={{
          ...filters,
          availableSources: sources?.sources || [],
          availableCategories: categories?.categories || [],
          regions: ['Global', 'India', 'US', 'UK'],
        }}
        onFilterChange={handleFilterChange}
      />
    </Container>
  );
};

export default NewsPage;
