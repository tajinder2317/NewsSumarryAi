import React from 'react';
import { useQuery, useMutation } from 'react-query';
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
  Fade,
  Slide,
  Avatar,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  Article,
  Analytics,
  Refresh,
  AutoGraph,
  Psychology,
  Summarize,
  Search,
  RocketLaunch,
} from '@mui/icons-material';

import { newsService, trendsService } from '../services/newsService';

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
  } = useQuery('trendsSummary', () => trendsService.getTrendingTopics(24), {
    staleTime: 10 * 60 * 1000, // 10 minutes
  });

  const {
    mutate: collectNews,
    isLoading: collecting,
  } = useMutation(newsService.collectNews);

  const handleCollectNews = () => {
    collectNews(undefined, {
      onSuccess: (data) => {
        refetchStats();
        // Some deployments previously returned mock arrays here; guard to avoid "undefined" alerts.
        if (!data || Array.isArray(data)) {
          alert('News collection requested. Refresh in a moment to see updated articles.');
          return;
        }

        if (data.timeout) {
          alert(`Collection timed out. You can try again with a longer timeout or check your internet connection.\n\n${data.message}`);
        } else {
          alert(data.message || 'News collected successfully.');
        }
      },
      onError: (error) => {
        const message = error?.message ? String(error.message) : String(error);
        if (message.includes('timeout')) {
          alert(`Request timed out. Please check your internet connection and try again.`);
        } else {
          alert(`Error collecting news: ${message}`);
        }
      },
    });
  };

  const features = [
    {
      title: 'Real-time Collection',
      description: 'Automatically collect news from multiple sources including RSS feeds and news APIs in real-time.',
      icon: <RocketLaunch />,
      color: 'primary',
    },
    {
      title: 'AI-Powered Analysis',
      description: 'Advanced sentiment analysis, topic extraction, and automatic categorization using machine learning.',
      icon: <Psychology />,
      color: 'secondary',
    },
    {
      title: 'Trend Detection',
      description: 'Identify trending topics and breaking news as they happen with intelligent algorithms.',
      icon: <AutoGraph />,
      color: 'success',
    },
    {
      title: 'Smart Summarization',
      description: 'Get concise summaries of articles and topic clusters powered by natural language processing.',
      icon: <Summarize />,
      color: 'warning',
    },
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 0, minHeight: '100vh' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: { xs: 5, md: 8 },
          mb: { xs: 4, md: 6 },
          borderRadius: 0,
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0,0,0,0.1)',
            zIndex: 1,
          },
          '& > *': {
            position: 'relative',
            zIndex: 2,
          }
        }}
      >
        <Container maxWidth="lg">
          <Fade in timeout={800}>
            <Box textAlign="center">
              <Typography
                variant="h2"
                component="h1"
                gutterBottom
                sx={{
                  fontWeight: 700,
                  mb: 2,
                  textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
                  fontSize: { xs: '2rem', sm: '2.8rem', md: '3.75rem' },
                }}
              >
                News Analyzer AI
              </Typography>
              <Typography
                variant="h5"
                sx={{
                  mb: 4,
                  opacity: 0.9,
                  maxWidth: 600,
                  mx: 'auto',
                  lineHeight: 1.6,
                  fontSize: { xs: '1rem', sm: '1.25rem' },
                }}
              >
                AI-powered news analysis and summarization platform that helps you stay informed with intelligent insights
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap', flexDirection: { xs: 'column', sm: 'row' } }}>
                <Button
                  variant="contained"
                  size="large"
                  startIcon={<Search />}
                  onClick={() => window.location.href = '/news'}
                  sx={{
                    bgcolor: 'white',
                    color: 'primary.main',
                    px: 4,
                    py: 1.5,
                    fontWeight: 600,
                    width: { xs: '100%', sm: 'auto' },
                    '&:hover': {
                      bgcolor: 'grey.100',
                      transform: 'translateY(-2px)',
                      boxShadow: 4
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  Explore News
                </Button>
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<Analytics />}
                  onClick={() => window.location.href = '/dashboard'}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    px: 4,
                    py: 1.5,
                    fontWeight: 600,
                    width: { xs: '100%', sm: 'auto' },
                    '&:hover': {
                      borderColor: 'white',
                      bgcolor: 'rgba(255,255,255,0.1)',
                      transform: 'translateY(-2px)',
                      boxShadow: 4
                    },
                    transition: 'all 0.3s ease'
                  }}
                >
                  View Dashboard
                </Button>
              </Box>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Stats Overview */}
      <Container maxWidth="lg" sx={{ mb: 6 }}>
        {(statsError || trendsError) && (
          <Alert severity="error" sx={{ mb: 3 }}>
            Error loading data. Please try refreshing the page.
          </Alert>
        )}

        {stats && (
          <Slide in timeout={600} direction="up">
            <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    textAlign: 'center',
                    p: { xs: 1.5, sm: 2, md: 3 },
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 8
                    },
                    cursor: 'pointer'
                  }}
                >
                  <CardContent>
                    <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mb: 2, mx: 'auto', width: 56, height: 56 }}>
                      <Article sx={{ fontSize: 28 }} />
                    </Avatar>
                    <Typography variant="h4" fontWeight="bold" sx={{ mb: 1, fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
                      {statsLoading ? '...' : (stats?.total_articles?.toLocaleString() || '0')}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Total Articles
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    textAlign: 'center',
                    p: { xs: 1.5, sm: 2, md: 3 },
                    background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                    color: 'white',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 8
                    },
                    cursor: 'pointer'
                  }}
                >
                  <CardContent>
                    <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mb: 2, mx: 'auto', width: 56, height: 56 }}>
                      <TrendingUp sx={{ fontSize: 28 }} />
                    </Avatar>
                    <Typography variant="h4" fontWeight="bold" sx={{ mb: 1, fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
                      {statsLoading ? '...' : (stats?.recent_articles_24h || '0')}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Last 24 Hours
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    textAlign: 'center',
                    p: { xs: 1.5, sm: 2, md: 3 },
                    background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                    color: 'white',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 8
                    },
                    cursor: 'pointer'
                  }}
                >
                  <CardContent>
                    <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mb: 2, mx: 'auto', width: 56, height: 56 }}>
                      <Analytics sx={{ fontSize: 28 }} />
                    </Avatar>
                    <Typography variant="h4" fontWeight="bold" sx={{ mb: 1, fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
                      {statsLoading ? '...' : (stats?.sources?.length || 0)}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      News Sources
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card
                  sx={{
                    textAlign: 'center',
                    p: { xs: 1.5, sm: 2, md: 3 },
                    background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                    color: 'white',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 8
                    },
                    cursor: 'pointer'
                  }}
                >
                  <CardContent>
                    <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', mb: 2, mx: 'auto', width: 56, height: 56 }}>
                      <Search sx={{ fontSize: 28 }} />
                    </Avatar>
                    <Typography variant="h4" fontWeight="bold" sx={{ mb: 1, fontSize: { xs: '1.8rem', md: '2.125rem' } }}>
                      {trendsLoading ? '...' : (trends?.trending_topics?.length || 0)}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9 }}>
                      Trending Topics
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Slide>
        )}
      </Container>

      {/* Action Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mb: 6, px: { xs: 1, sm: 0 } }}>
        <Button
          variant="contained"
          size="large"
          startIcon={collecting ? <CircularProgress size={20} /> : <Refresh />}
          onClick={handleCollectNews}
          disabled={collecting}
          sx={{
            px: 4,
            py: 2,
            fontWeight: 600,
            width: { xs: '100%', sm: 'auto' },
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)',
              transform: 'translateY(-2px)',
              boxShadow: 4
            },
            transition: 'all 0.3s ease'
          }}
        >
          {collecting ? 'Collecting...' : 'Collect News'}
        </Button>
      </Box>

      {/* Features Grid */}
      <Slide in timeout={800} direction="up">
        <Box sx={{ mb: 6 }}>
          <Typography
            variant="h4"
            gutterBottom
            align="center"
            sx={{
              mb: 4,
              fontWeight: 600,
              color: 'text.primary',
              fontSize: { xs: '1.7rem', md: '2.125rem' },
            }}
          >
            Powerful Features
          </Typography>
          <Grid container spacing={{ xs: 2, md: 4 }}>
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Fade in timeout={1000 + index * 200}>
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: 8,
                        '& .feature-icon': {
                          transform: 'scale(1.1)',
                          bgcolor: `${feature.color}.main`,
                          color: 'white'
                        }
                      },
                      cursor: 'pointer',
                      border: '1px solid rgba(0,0,0,0.08)'
                    }}
                  >
                    <CardContent sx={{ flexGrow: 1, textAlign: 'center', p: { xs: 2, md: 3 } }}>
                      <Avatar
                        className="feature-icon"
                        sx={{
                          mb: 3,
                          mx: 'auto',
                          width: 64,
                          height: 64,
                          bgcolor: `${feature.color}.main`,
                          color: 'white',
                          transition: 'all 0.3s ease'
                        }}
                      >
                        {React.cloneElement(feature.icon, { sx: { fontSize: 32 } })}
                      </Avatar>
                      <Typography
                        variant="h6"
                        component="h3"
                        gutterBottom
                        sx={{
                          fontWeight: 600,
                          mb: 2,
                          color: 'text.primary'
                        }}
                      >
                        {feature.title}
                      </Typography>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                          lineHeight: 1.6,
                          mb: 2
                        }}
                      >
                        {feature.description}
                      </Typography>
                      <Chip
                        label="Learn More"
                        size="small"
                        variant="outlined"
                        color={feature.color}
                        sx={{
                          '&:hover': {
                            bgcolor: `${feature.color}.main`,
                            color: 'white'
                          },
                          transition: 'all 0.2s ease'
                        }}
                      />
                    </CardContent>
                  </Card>
                </Fade>
              </Grid>
            ))}
          </Grid>
        </Box>
      </Slide>

      {/* Recent Trending Topics */}
      {trends?.trending_topics && trends.trending_topics.length > 0 && (
        <Slide in timeout={1000} direction="up">
          <Box sx={{ mb: 6 }}>
            <Typography
              variant="h4"
              gutterBottom
              sx={{
                fontWeight: 600,
                mb: 3,
                color: 'text.primary',
                fontSize: { xs: '1.6rem', md: '2.125rem' },
              }}
            >
              Trending Topics
            </Typography>
            <Grid container spacing={{ xs: 2, md: 3 }}>
              {trends.trending_topics.slice(0, 6).map((topic, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Fade in timeout={1200 + index * 100}>
                    <Card
                      sx={{
                        height: '100%',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateY(-4px)',
                          boxShadow: 6
                        },
                        cursor: 'pointer',
                        border: '1px solid rgba(0,0,0,0.08)'
                      }}
                    >
                      <CardContent sx={{ p: { xs: 2, md: 3 } }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                          <Avatar
                            sx={{
                              bgcolor: 'primary.main',
                              mr: 2,
                              width: 32,
                              height: 32,
                              fontSize: '0.875rem'
                            }}
                          >
                            {index + 1}
                          </Avatar>
                          <Typography
                            variant="h6"
                            component="h3"
                            sx={{
                              fontWeight: 600,
                              color: 'text.primary',
                              lineHeight: 1.3
                            }}
                          >
                            {topic.topic_name}
                          </Typography>
                        </Box>
                        <Typography
                          variant="body2"
                          color="text.secondary"
                          sx={{ mb: 2 }}
                        >
                          {topic.article_count} articles
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                          {topic.top_terms?.slice(0, 3).map((term, termIndex) => (
                            <Chip
                              key={termIndex}
                              label={term}
                              size="small"
                              variant="filled"
                              sx={{
                                bgcolor: 'primary.50',
                                color: 'primary.main',
                                fontSize: '0.75rem',
                                fontWeight: 500,
                                '&:hover': {
                                  bgcolor: 'primary.100'
                                }
                              }}
                            />
                          ))}
                        </Box>
                      </CardContent>
                    </Card>
                  </Fade>
                </Grid>
              ))}
            </Grid>
          </Box>
        </Slide>
      )}
    </Container>
  );
};

export default Home;
