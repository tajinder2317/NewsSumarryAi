import React, { useState } from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  Article,
  SentimentSatisfied,
  Source,
  Refresh,
} from '@mui/icons-material';

import { newsService, trendsService, analysisService } from '../services/newsService';
import Loading from '../components/common/Loading';
import SentimentChart from '../components/analysis/SentimentChart';
import TrendChart from '../components/analysis/TrendChart';

const Dashboard = () => {
  const [timeRange, setTimeRange] = useState(24);

  const {
    data: stats,
    isLoading: statsLoading,
    error: statsError,
    refetch: refetchStats,
  } = useQuery('newsStats', newsService.getStats, {
    staleTime: 5 * 60 * 1000,
  });

  const {
    data: trends,
    isLoading: trendsLoading,
    error: trendsError,
  } = useQuery(['trendsSummary', timeRange], () => trendsService.getTrendsSummary(timeRange), {
    staleTime: 10 * 60 * 1000,
  });

  const {
    data: sentimentTrends,
    isLoading: sentimentLoading,
  } = useQuery(['sentimentTrends', 7], () => trendsService.getSentimentTrends(7), {
    staleTime: 15 * 60 * 1000,
  });

  const {
    data: sourceTrends,
    isLoading: sourceLoading,
  } = useQuery(['sourceTrends', 7], () => trendsService.getSourceTrends(7), {
    staleTime: 15 * 60 * 1000,
  });

  const {
    data: analysisStats,
  } = useQuery('analysisStats', analysisService.getAnalysisStats, {
    staleTime: 10 * 60 * 1000,
  });

  const handleRefresh = () => {
    refetchStats();
  };

  if (statsLoading || trendsLoading) {
    return <Loading message="Loading dashboard..." />;
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1">
          Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value={1}>Last Hour</MenuItem>
              <MenuItem value={6}>Last 6 Hours</MenuItem>
              <MenuItem value={24}>Last 24 Hours</MenuItem>
              <MenuItem value={168}>Last Week</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRefresh}
            disabled={statsLoading}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {(statsError || trendsError) && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading dashboard data. Please try refreshing.
        </Alert>
      )}

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2, height: '100%' }}>
            <CardContent>
              <Article color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="primary" fontWeight="bold">
                {stats?.total_articles || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Articles
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2, height: '100%' }}>
            <CardContent>
              <TrendingUp color="success" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="success" fontWeight="bold">
                {stats?.recent_articles_24h || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Last 24 Hours
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2, height: '100%' }}>
            <CardContent>
              <Source color="info" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="info" fontWeight="bold">
                {stats?.sources?.length || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                News Sources
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ textAlign: 'center', p: 2, height: '100%' }}>
            <CardContent>
              <SentimentSatisfied color="warning" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" color="warning" fontWeight="bold">
                {analysisStats?.analysis_coverage ? 
                  `${Math.round(analysisStats.analysis_coverage * 100)}%` : '0%'}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Analyzed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Sentiment Distribution */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Sentiment Distribution
              </Typography>
              {sentimentLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <SentimentChart data={sentimentTrends?.sentiment_trends} />
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Source Trends */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: 400 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top News Sources
              </Typography>
              {sourceLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <TrendChart 
                  data={Object.entries(sourceTrends?.source_trends || {})
                    .slice(0, 5)
                    .map(([source, data]) => ({ name: source, value: data.total_articles }))}
                  type="bar"
                />
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Trending Topics */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Trending Topics (Last {timeRange} Hours)
              </Typography>
              {trends?.summary?.trending_topics?.length > 0 ? (
                <Grid container spacing={2}>
                  {trends.summary.trending_topics.slice(0, 6).map((topic, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Card variant="outlined" sx={{ p: 2, height: '100%' }}>
                        <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                          {topic.topic_name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {topic.article_count} articles
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {topic.top_terms?.slice(0, 3).map((term, termIndex) => (
                            <span
                              key={termIndex}
                              style={{
                                backgroundColor: '#e3f2fd',
                                color: '#1976d2',
                                padding: '2px 8px',
                                borderRadius: '12px',
                                fontSize: '0.75rem',
                              }}
                            >
                              {term}
                            </span>
                          ))}
                        </Box>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              ) : (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body2" color="text.secondary">
                    No trending topics found in the selected time range.
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
