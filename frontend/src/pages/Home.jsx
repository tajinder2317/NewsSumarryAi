import React from 'react';
import { useQuery } from 'react-query';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Box,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  TrendingUp,
  Article,
  Analytics,
  Refresh,
} from '@mui/icons-material';

import { newsService } from '../services/newsService';
import Loading from '../components/common/Loading';

const Home = () => {
  const {
    data: stats,
    isLoading: statsLoading,
    error: statsError,
    refetch: refetchStats,
  } = useQuery('newsStats', newsService.getStats, {
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const {
    data: trends,
    isLoading: trendsLoading,
    error: trendsError,
  } = useQuery('trendsSummary', () => newsService.getTrendingTopics(24), {
    staleTime: 10 * 60 * 1000, // 10 minutes
  });

  const {
    mutate: collectNews,
    isLoading: collecting,
  } = newsService.collectNews;

  const handleCollectNews = () => {
    collectNews(undefined, {
      onSuccess: (data) => {
        refetchStats();
        alert(`Successfully collected ${data.collected_count} new articles!`);
      },
      onError: (error) => {
        alert(`Error collecting news: ${error.message}`);
      },
    });
  };

  const features = [
    {
      title: 'Real-time News Collection',
      description: 'Automatically collect news from multiple sources including RSS feeds and news APIs.',
      icon: <Refresh fontSize="large" color="primary" />,
    },
    {
      title: 'AI-Powered Analysis',
      description: 'Advanced sentiment analysis, topic extraction, and automatic categorization.',
      icon: <Analytics fontSize="large" color="primary" />,
    },
    {
      title: 'Trend Detection',
      description: 'Identify trending topics and breaking news as they happen.',
      icon: <TrendingUp fontSize="large" color="primary" />,
    },
    {
      title: 'Smart Summarization',
      description: 'Get concise summaries of articles and topic clusters.',
      icon: <Article fontSize="large" color="primary" />,
    },
  ];

  if (statsLoading || trendsLoading) {
    return <Loading message="Loading dashboard..." />;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        News Analyzer AI
      </Typography>
      <Typography variant="h6" color="text.secondary" align="center" sx={{ mb: 4 }}>
        AI-powered news analysis and summarization platform
      </Typography>

      {/* Stats Overview */}
      {(statsError || trendsError) && (
        <Alert severity="error" sx={{ mb: 3 }}>
          Error loading data. Please try refreshing the page.
        </Alert>
      )}

      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center', p: 2 }}>
              <CardContent>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {stats.total_articles}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Articles
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center', p: 2 }}>
              <CardContent>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {stats.recent_articles_24h}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Last 24 Hours
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center', p: 2 }}>
              <CardContent>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {stats.sources?.length || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  News Sources
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card sx={{ textAlign: 'center', p: 2 }}>
              <CardContent>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {trends?.trending_topics?.length || 0}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Trending Topics
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={collecting ? <CircularProgress size={20} /> : <Refresh />}
          onClick={handleCollectNews}
          disabled={collecting}
        >
          {collecting ? 'Collecting...' : 'Collect News'}
        </Button>
      </Box>

      {/* Features Grid */}
      <Typography variant="h4" gutterBottom align="center" sx={{ mb: 3 }}>
        Features
      </Typography>
      <Grid container spacing={3}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h3" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Trending Topics */}
      {trends?.trending_topics && trends.trending_topics.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h4" gutterBottom>
            Trending Topics
          </Typography>
          <Grid container spacing={2}>
            {trends.trending_topics.slice(0, 6).map((topic, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" component="h3" gutterBottom>
                      {topic.topic_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {topic.article_count} articles
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      {topic.top_terms?.slice(0, 3).map((term, termIndex) => (
                        <span
                          key={termIndex}
                          style={{
                            display: 'inline-block',
                            backgroundColor: '#e3f2fd',
                            color: '#1976d2',
                            padding: '2px 8px',
                            margin: '2px',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                          }}
                        >
                          {term}
                        </span>
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );
};

export default Home;
