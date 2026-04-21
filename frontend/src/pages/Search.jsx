import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
} from '@mui/material';
import { Search, Clear, FilterList } from '@mui/icons-material';
import moment from 'moment';

import { newsService } from '../services/newsService';
import NewsList from '../components/news/NewsList';

const SearchPage = () => {
  const [searchParams, setSearchParams] = useState({
    query: '',
    source: '',
    category: '',
    sentiment: '',
    date_from: null,
    date_to: null,
    limit: 20,
    offset: 0,
  });

  const [currentPage, setCurrentPage] = useState(1);

  const {
    data: searchResults,
    isLoading,
    error,
    refetch,
  } = useQuery(
    ['searchNews', searchParams],
    () => newsService.searchNews(searchParams),
    {
      enabled: false, // Don't search on mount, only on button click
    }
  );

  const {
    data: sources,
  } = useQuery('newsSources', newsService.getSources, {
    staleTime: 30 * 60 * 1000, // 30 minutes
  });

  const {
    data: categories,
  } = useQuery('newsCategories', newsService.getCategories, {
    staleTime: 30 * 60 * 1000,
  });

  const handleSearch = () => {
    setCurrentPage(1);
    setSearchParams(prev => ({ ...prev, offset: 0 }));
    refetch();
  };

  const handleClear = () => {
    setSearchParams({
      query: '',
      source: '',
      category: '',
      sentiment: '',
      date_from: null,
      date_to: null,
      limit: 20,
      offset: 0,
    });
    setCurrentPage(1);
  };

  const handleFilterChange = (field, value) => {
    setSearchParams(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePageChange = (event, page) => {
    const newOffset = (page - 1) * searchParams.limit;
    setSearchParams(prev => ({ ...prev, offset: newOffset }));
    setCurrentPage(page);
  };

  const hasSearchCriteria = searchParams.query || 
                           searchParams.source || 
                           searchParams.category || 
                           searchParams.sentiment ||
                           searchParams.date_from ||
                           searchParams.date_to;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Search News
      </Typography>

      {/* Search Form */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Search Criteria
          </Typography>
          
          <Grid container spacing={2}>
            {/* Search Query */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Search Query"
                value={searchParams.query}
                onChange={(e) => handleFilterChange('query', e.target.value)}
                placeholder="Enter keywords to search in article titles and content..."
                variant="outlined"
              />
            </Grid>

            {/* Source Filter */}
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Source</InputLabel>
                <Select
                  value={searchParams.source}
                  label="Source"
                  onChange={(e) => handleFilterChange('source', e.target.value)}
                >
                  <MenuItem value="">All Sources</MenuItem>
                  {sources?.sources?.map((source) => (
                    <MenuItem key={source} value={source}>
                      {source}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* Category Filter */}
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Category</InputLabel>
                <Select
                  value={searchParams.category}
                  label="Category"
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                >
                  <MenuItem value="">All Categories</MenuItem>
                  {categories?.categories?.map((category) => (
                    <MenuItem key={category} value={category}>
                      {category}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* Sentiment Filter */}
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Sentiment</InputLabel>
                <Select
                  value={searchParams.sentiment}
                  label="Sentiment"
                  onChange={(e) => handleFilterChange('sentiment', e.target.value)}
                >
                  <MenuItem value="">All Sentiments</MenuItem>
                  <MenuItem value="positive">Positive</MenuItem>
                  <MenuItem value="negative">Negative</MenuItem>
                  <MenuItem value="neutral">Neutral</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Results per page */}
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth>
                <InputLabel>Results per page</InputLabel>
                <Select
                  value={searchParams.limit}
                  label="Results per page"
                  onChange={(e) => handleFilterChange('limit', e.target.value)}
                >
                  <MenuItem value={10}>10</MenuItem>
                  <MenuItem value={20}>20</MenuItem>
                  <MenuItem value={50}>50</MenuItem>
                  <MenuItem value={100}>100</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Date Range */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="From Date"
                type="date"
                value={searchParams.date_from ? moment(searchParams.date_from).format('YYYY-MM-DD') : ''}
                onChange={(e) => handleFilterChange('date_from', e.target.value ? new Date(e.target.value) : null)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="To Date"
                type="date"
                value={searchParams.date_to ? moment(searchParams.date_to).format('YYYY-MM-DD') : ''}
                onChange={(e) => handleFilterChange('date_to', e.target.value ? new Date(e.target.value) : null)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            {/* Action Buttons */}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-start' }}>
                <Button
                  variant="contained"
                  startIcon={<Search />}
                  onClick={handleSearch}
                  disabled={!hasSearchCriteria || isLoading}
                >
                  {isLoading ? 'Searching...' : 'Search'}
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Clear />}
                  onClick={handleClear}
                >
                  Clear
                </Button>
              </Box>
            </Grid>
          </Grid>

          {/* Active Filters Display */}
          {hasSearchCriteria && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Active Filters:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {searchParams.query && (
                  <Chip
                    label={`Query: ${searchParams.query}`}
                    onDelete={() => handleFilterChange('query', '')}
                    size="small"
                  />
                )}
                {searchParams.source && (
                  <Chip
                    label={`Source: ${searchParams.source}`}
                    onDelete={() => handleFilterChange('source', '')}
                    size="small"
                  />
                )}
                {searchParams.category && (
                  <Chip
                    label={`Category: ${searchParams.category}`}
                    onDelete={() => handleFilterChange('category', '')}
                    size="small"
                  />
                )}
                {searchParams.sentiment && (
                  <Chip
                    label={`Sentiment: ${searchParams.sentiment}`}
                    onDelete={() => handleFilterChange('sentiment', '')}
                    size="small"
                  />
                )}
                {searchParams.date_from && (
                  <Chip
                    label={`From: ${moment(searchParams.date_from).format('MMM DD, YYYY')}`}
                    onDelete={() => handleFilterChange('date_from', null)}
                    size="small"
                  />
                )}
                {searchParams.date_to && (
                  <Chip
                    label={`To: ${moment(searchParams.date_to).format('MMM DD, YYYY')}`}
                    onDelete={() => handleFilterChange('date_to', null)}
                    size="small"
                  />
                )}
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Search Results */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Error searching articles: {error.message}
        </Alert>
      )}

      {searchResults && (
        <NewsList
          articles={searchResults}
          loading={isLoading}
          error={error}
          pagination={{
            page: currentPage,
            limit: searchParams.limit,
          }}
          onPageChange={handlePageChange}
          totalCount={searchResults.length >= searchParams.limit ? undefined : searchResults.length}
          filters={{
            availableSources: sources?.sources,
            availableCategories: categories?.categories,
          }}
        />
      )}

      {/* Initial state */}
      {!searchResults && !isLoading && (
        <Card sx={{ textAlign: 'center', py: 4 }}>
          <CardContent>
            <FilterList sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary" gutterBottom>
              Start Your Search
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Use the search form above to find specific news articles. You can search by keywords,
              filter by source, category, sentiment, and date range.
            </Typography>
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default SearchPage;
