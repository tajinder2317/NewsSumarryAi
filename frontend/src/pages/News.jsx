import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
} from '@mui/material';
import { Refresh } from '@mui/icons-material';

import { newsService } from '../services/newsService';
import NewsList from '../components/news/NewsList';

const NewsPage = () => {
  const [filters, setFilters] = useState({
    source: '',
    category: '',
    sentiment: '',
    region: '',
  });
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 20;

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
    refetch();
  };

  return (
    <Container maxWidth="lg" sx={{ py: { xs: 2, md: 4 } }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: { xs: 'stretch', sm: 'center' }, mb: 4, gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
        <Typography variant="h4" component="h1" sx={{ fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
          Latest News
        </Typography>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleRefresh}
          disabled={isLoading}
          sx={{ width: { xs: '100%', sm: 'auto' } }}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading news: {error.message}
        </Alert>
      )}

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
