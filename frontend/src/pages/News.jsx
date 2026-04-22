import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Box,
  Button,
  Alert,
  Divider,
  ToggleButton,
  ToggleButtonGroup,
} from '@mui/material';
import { Refresh } from '@mui/icons-material';

import { newsService } from '../services/newsService';
import NewsList from '../components/news/NewsList';
import NewsCard from '../components/news/NewsCard';

const startOfLocalDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0, 0, 0, 0);
const endOfLocalDay = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), 23, 59, 59, 999);
const startOfLocalMonth = (d) => new Date(d.getFullYear(), d.getMonth(), 1, 0, 0, 0, 0);
const startOfLocalYear = (d) => new Date(d.getFullYear(), 0, 1, 0, 0, 0, 0);
const startOfLocalWeekMonday = (d) => {
  const day = d.getDay(); // 0=Sun .. 6=Sat
  const diff = day === 0 ? 6 : day - 1; // days since Monday
  const monday = new Date(d);
  monday.setDate(d.getDate() - diff);
  return startOfLocalDay(monday);
};

const NewsPage = () => {
  const FRESH_MINUTES = 5;
  const PAGE_SIZE = 50;
  const [timeRange, setTimeRange] = useState('today');
  const [filters, setFilters] = useState({
    source: '',
    category: '',
    sentiment: '',
    region: '',
  });
  const [currentPage, setCurrentPage] = useState(1);

  const getDateRangeParams = () => {
    const now = new Date();
    if (timeRange === 'all') return {};

    if (timeRange === 'today') {
      return { date_from: startOfLocalDay(now).toISOString(), date_to: now.toISOString() };
    }

    if (timeRange === 'yesterday') {
      const y = new Date(now);
      y.setDate(now.getDate() - 1);
      return { date_from: startOfLocalDay(y).toISOString(), date_to: endOfLocalDay(y).toISOString() };
    }

    if (timeRange === 'week') {
      return { date_from: startOfLocalWeekMonday(now).toISOString(), date_to: now.toISOString() };
    }

    if (timeRange === 'month') {
      return { date_from: startOfLocalMonth(now).toISOString(), date_to: now.toISOString() };
    }

    if (timeRange === 'year') {
      return { date_from: startOfLocalYear(now).toISOString(), date_to: now.toISOString() };
    }

    return {};
  };

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
    data: pageData,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['newsPaged', { page: currentPage, page_size: PAGE_SIZE, timeRange, ...filters }],
    () => newsService.fetchNewsPaged({
      page: currentPage,
      page_size: PAGE_SIZE,
      ...getDateRangeParams(),
      source: filters.source || undefined,
      category: filters.category || undefined,
      region: filters.region || undefined,
      sentiment: filters.sentiment || undefined,
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

  const articles = pageData?.items || [];
  const totalCount = typeof pageData?.total === 'number' ? pageData.total : undefined;

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
          disabled={isLoading || latestLoading}
          sx={{ width: { xs: '100%', sm: 'auto' } }}
        >
          Refresh
        </Button>
      </Box>

      <Box sx={{ mb: 3, display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 1.5, alignItems: { xs: 'stretch', sm: 'center' }, justifyContent: 'space-between' }}>
        <ToggleButtonGroup
          value={timeRange}
          exclusive
          onChange={(e, next) => {
            if (!next) return;
            setTimeRange(next);
            setCurrentPage(1);
          }}
          size="small"
          sx={{
            flexWrap: 'wrap',
            '& .MuiToggleButton-root': {
              textTransform: 'none',
              px: 1.5,
              borderColor: 'rgba(15, 23, 42, 0.18)',
            },
          }}
        >
          <ToggleButton value="today">Today</ToggleButton>
          <ToggleButton value="yesterday">Yesterday</ToggleButton>
          <ToggleButton value="week">This Week</ToggleButton>
          <ToggleButton value="month">This Month</ToggleButton>
          <ToggleButton value="year">This Year</ToggleButton>
          <ToggleButton value="all">All Time</ToggleButton>
        </ToggleButtonGroup>

        <Typography variant="body2" color="text.secondary" sx={{ textAlign: { xs: 'left', sm: 'right' } }}>
          {totalCount !== undefined ? `${totalCount.toLocaleString()} articles` : `${articles.length} articles`}
          {' · '}
          {PAGE_SIZE} per page
        </Typography>
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
          limit: PAGE_SIZE,
        }}
        onPageChange={handlePageChange}
        totalCount={totalCount}
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
