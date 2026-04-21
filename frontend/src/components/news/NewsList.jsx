import React from 'react';
import {
  Box,
  Typography,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Button,
  Alert,
} from '@mui/material';
import { Refresh } from '@mui/icons-material';
import NewsCard from './NewsCard';
import Loading from '../common/Loading';

const NewsList = ({
  articles = [],
  loading,
  error,
  onArticleAnalyze,
  onArticleDelete,
  onRefresh,
  pagination,
  onPageChange,
  filters,
  onFilterChange,
  totalCount,
  regions,
}) => {
  const handleFilterChange = (filterType, value) => {
    if (onFilterChange) {
      onFilterChange(filterType, value);
    }
  };

  // Error boundary fallback
  if (error && !loading) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error || 'Error loading articles'}
        </Alert>
        <Button variant="outlined" onClick={onRefresh} startIcon={<Refresh />}>
          Try Again
        </Button>
      </Box>
    );
  }

  const clearFilters = () => {
    if (onFilterChange) {
      onFilterChange('clear', null);
    }
  };

  const hasActiveFilters = filters && (
    filters.source ||
    filters.category ||
    filters.sentiment ||
    filters.region
  );

  if (loading && articles.length === 0) {
    return <Loading message="Loading articles..." />;
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!articles || articles.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          No articles found
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {hasActiveFilters
            ? 'Try adjusting your filters or search terms.'
            : 'Try collecting some news first.'}
        </Typography>
        {onRefresh && (
          <Button
            variant="contained"
            startIcon={<Refresh />}
            onClick={onRefresh}
            sx={{ mr: 2 }}
          >
            Refresh
          </Button>
        )}
        {hasActiveFilters && (
          <Button variant="outlined" onClick={clearFilters}>
            Clear Filters
          </Button>
        )}
      </Box>
    );
  }

  return (
    <Box>
      {/* Filters Section */}
      {filters && (
        <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
          <Typography variant="h6" gutterBottom>
            Filters
          </Typography>

          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Source</InputLabel>
              <Select
                value={filters.source || ''}
                label="Source"
                onChange={(e) => handleFilterChange('source', e.target.value || null)}
              >
                <MenuItem value="">All Sources</MenuItem>
                {filters.availableSources && filters.availableSources.map((source) => (
                  <MenuItem key={source} value={source}>
                    {source}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Region</InputLabel>
              <Select
                value={filters.region || ''}
                label="Region"
                onChange={(e) => handleFilterChange('region', e.target.value || null)}
              >
                <MenuItem value="">All Regions</MenuItem>
                <MenuItem value="Global">Global</MenuItem>
                <MenuItem value="India">India</MenuItem>
                <MenuItem value="US">United States</MenuItem>
                <MenuItem value="UK">United Kingdom</MenuItem>
              </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Category</InputLabel>
              <Select
                value={filters.category || ''}
                label="Category"
                onChange={(e) => handleFilterChange('category', e.target.value || null)}
              >
                <MenuItem value="">All Categories</MenuItem>
                {filters.availableCategories && filters.availableCategories.map((category) => (
                  <MenuItem key={category} value={category}>
                    {category}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Sentiment</InputLabel>
              <Select
                value={filters.sentiment || ''}
                label="Sentiment"
                onChange={(e) => handleFilterChange('sentiment', e.target.value || null)}
              >
                <MenuItem value="">All Sentiments</MenuItem>
                <MenuItem value="positive">Positive</MenuItem>
                <MenuItem value="negative">Negative</MenuItem>
                <MenuItem value="neutral">Neutral</MenuItem>
              </Select>
            </FormControl>

            {hasActiveFilters && (
              <Button variant="outlined" size="small" onClick={clearFilters}>
                Clear Filters
              </Button>
            )}
          </Box>

          {/* Active filter chips */}
          {hasActiveFilters && (
            <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {filters.query && (
                <Chip
                  label={`Search: ${filters.query}`}
                  onDelete={() => handleFilterChange('query', null)}
                  size="small"
                />
              )}
              {filters.source && (
                <Chip
                  label={`Source: ${filters.source}`}
                  onDelete={() => handleFilterChange('source', null)}
                  size="small"
                />
              )}
              {filters.category && (
                <Chip
                  label={`Category: ${filters.category}`}
                  onDelete={() => handleFilterChange('category', null)}
                  size="small"
                />
              )}
              {filters.sentiment && (
                <Chip
                  label={`Sentiment: ${filters.sentiment}`}
                  onDelete={() => handleFilterChange('sentiment', null)}
                  size="small"
                />
              )}
            </Box>
          )}
        </Box>
      )}

      {/* Results count and refresh */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          {totalCount !== undefined
            ? `Showing ${articles.length} of ${totalCount} articles`
            : `${articles.length} articles`}
        </Typography>

        {onRefresh && (
          <Button
            variant="outlined"
            size="small"
            startIcon={<Refresh />}
            onClick={onRefresh}
            disabled={loading}
          >
            Refresh
          </Button>
        )}
      </Box>

      {/* Articles List */}
      <Box>
        {articles.map((article) => (
          <NewsCard
            key={article.id}
            article={article}
            onAnalyze={onArticleAnalyze}
            onDelete={onArticleDelete}
          />
        ))}
      </Box>

      {/* Pagination */}
      {pagination && totalCount > pagination.limit && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
          <Pagination
            count={Math.ceil(totalCount / pagination.limit)}
            page={pagination.page}
            onChange={onPageChange}
            color="primary"
            showFirstButton
            showLastButton
          />
        </Box>
      )}

      {/* Loading indicator for pagination */}
      {loading && articles.length > 0 && (
        <Box sx={{ textAlign: 'center', py: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Loading more articles...
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default NewsList;
