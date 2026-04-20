import React, { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Chip,
  CircularProgress,
  Divider,
} from '@mui/material';
import {
  Analytics,
  Summarize,
  Topic,
  SentimentSatisfied,
  TrendingUp,
  PlayArrow,
} from '@mui/icons-material';

import { newsService, analysisService } from '../services/newsService';
import Loading from '../components/common/Loading';
import SentimentChart from '../components/analysis/SentimentChart';

const AnalysisPage = () => {
  const [selectedArticles, setSelectedArticles] = useState([]);
  const [analysisType, setAnalysisType] = useState('');
  const [analysisParams, setAnalysisParams] = useState({
    max_sentences: 3,
    num_keywords: 10,
  });

  const {
    data: articles,
    isLoading: articlesLoading,
  } = useQuery('recentNews', () => newsService.fetchNews({ limit: 50 }), {
    staleTime: 5 * 60 * 1000,
  });

  const {
    mutate: analyzeSentiment,
    isLoading: sentimentLoading,
    data: sentimentResult,
  } = useMutation(analysisService.analyzeSentiment);

  const {
    mutate: analyzeTopics,
    isLoading: topicsLoading,
    data: topicsResult,
  } = useMutation(analysisService.analyzeTopics);

  const {
    mutate: summarizeArticles,
    isLoading: summaryLoading,
    data: summaryResult,
  } = useMutation(analysisService.summarizeArticles);

  const {
    mutate: extractKeywords,
    isLoading: keywordsLoading,
    data: keywordsResult,
  } = useMutation(analysisService.extractKeywords);

  const handleArticleToggle = (articleId) => {
    setSelectedArticles(prev =>
      prev.includes(articleId)
        ? prev.filter(id => id !== articleId)
        : [...prev, articleId]
    );
  };

  const handleAnalyze = () => {
    if (selectedArticles.length === 0) {
      alert('Please select at least one article to analyze');
      return;
    }

    switch (analysisType) {
      case 'sentiment':
        analyzeSentiment(selectedArticles, {
          onSuccess: (data) => console.log('Sentiment analysis complete:', data),
          onError: (error) => alert(`Sentiment analysis failed: ${error.message}`),
        });
        break;
      case 'topics':
        analyzeTopics(selectedArticles, {
          onSuccess: (data) => console.log('Topic analysis complete:', data),
          onError: (error) => alert(`Topic analysis failed: ${error.message}`),
        });
        break;
      case 'summary':
        console.log('DEBUG: Calling summarizeArticles with:', selectedArticles, analysisParams.max_sentences);
        // Clear previous result to ensure fresh display
        if (summaryResult) {
          // Force re-render by setting result to null temporarily
          setTimeout(() => {
            summarizeArticles(selectedArticles, analysisParams.max_sentences, {
              onSuccess: (data) => {
                console.log('Summarization complete:', data);
                console.log('DEBUG: Summary length:', data.summary ? data.summary.length : 0);
                console.log('DEBUG: Max sentences requested:', analysisParams.max_sentences);
                console.log('DEBUG: Actual summary:', data.summary);
              },
              onError: (error) => alert(`Summarization failed: ${error.message}`),
            });
          }, 50);
        } else {
          summarizeArticles(selectedArticles, analysisParams.max_sentences, {
            onSuccess: (data) => {
              console.log('Summarization complete:', data);
              console.log('DEBUG: Summary length:', data.summary ? data.summary.length : 0);
              console.log('DEBUG: Max sentences requested:', analysisParams.max_sentences);
              console.log('DEBUG: Actual summary:', data.summary);
            },
            onError: (error) => alert(`Summarization failed: ${error.message}`),
          });
        }
        break;
      case 'keywords':
        extractKeywords(selectedArticles, analysisParams.num_keywords, {
          onSuccess: (data) => console.log('Keyword extraction complete:', data),
          onError: (error) => alert(`Keyword extraction failed: ${error.message}`),
        });
        break;
      default:
        alert('Please select an analysis type');
    }
  };

  const selectAllArticles = () => {
    if (articles) {
      setSelectedArticles(articles.map(article => article.id));
    }
  };

  const clearSelection = () => {
    setSelectedArticles([]);
  };

  const isAnalysisLoading = sentimentLoading || topicsLoading || summaryLoading || keywordsLoading;

  if (articlesLoading) {
    return <Loading message="Loading articles for analysis..." />;
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        News Analysis
      </Typography>

      <Grid container spacing={3}>
        {/* Article Selection */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Select Articles
              </Typography>

              <Box sx={{ mb: 2, display: 'flex', gap: 1 }}>
                <Button
                  size="small"
                  variant="outlined"
                  onClick={selectAllArticles}
                  disabled={!articles || articles.length === 0}
                >
                  Select All
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  onClick={clearSelection}
                  disabled={selectedArticles.length === 0}
                >
                  Clear
                </Button>
              </Box>

              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                {selectedArticles.length} of {articles?.length || 0} selected
              </Typography>

              <Box sx={{ maxHeight: 400, overflowY: 'auto' }}>
                {articles?.map((article) => (
                  <Card
                    key={article.id}
                    variant="outlined"
                    sx={{
                      mb: 1,
                      cursor: 'pointer',
                      border: selectedArticles.includes(article.id)
                        ? '2px solid primary.main'
                        : '1px solid grey.300',
                      '&:hover': {
                        backgroundColor: 'grey.50',
                      },
                    }}
                    onClick={() => handleArticleToggle(article.id)}
                  >
                    <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                        {article.title.substring(0, 60)}...
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {article.source} · {article.category || 'Uncategorized'}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Analysis Controls and Results */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analysis Configuration
              </Typography>

              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel>Analysis Type</InputLabel>
                    <Select
                      value={analysisType}
                      label="Analysis Type"
                      onChange={(e) => setAnalysisType(e.target.value)}
                    >
                      <MenuItem value="">
                        <em>Select analysis type</em>
                      </MenuItem>
                      <MenuItem value="sentiment">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <SentimentSatisfied fontSize="small" />
                          Sentiment Analysis
                        </Box>
                      </MenuItem>
                      <MenuItem value="topics">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Topic fontSize="small" />
                          Topic Extraction
                        </Box>
                      </MenuItem>
                      <MenuItem value="summary">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Summarize fontSize="small" />
                          Summarization
                        </Box>
                      </MenuItem>
                      <MenuItem value="keywords">
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <TrendingUp fontSize="small" />
                          Keyword Extraction
                        </Box>
                      </MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                {analysisType === 'summary' && (
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Max Sentences"
                      value={analysisParams.max_sentences}
                      onChange={(e) => setAnalysisParams(prev => ({
                        ...prev,
                        max_sentences: parseInt(e.target.value) || 3
                      }))}
                      inputProps={{ min: 1, max: 10 }}
                    />
                  </Grid>
                )}

                {analysisType === 'keywords' && (
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      type="number"
                      label="Number of Keywords"
                      value={analysisParams.num_keywords}
                      onChange={(e) => setAnalysisParams(prev => ({
                        ...prev,
                        num_keywords: parseInt(e.target.value) || 10
                      }))}
                      inputProps={{ min: 5, max: 50 }}
                    />
                  </Grid>
                )}
              </Grid>

              <Button
                variant="contained"
                startIcon={isAnalysisLoading ? <CircularProgress size={20} /> : <PlayArrow />}
                onClick={handleAnalyze}
                disabled={selectedArticles.length === 0 || isAnalysisLoading || !analysisType}
                fullWidth
                sx={{ mb: 3 }}
              >
                {isAnalysisLoading ? 'Analyzing...' : 'Start Analysis'}
              </Button>

              <Divider sx={{ mb: 3 }} />

              {/* Results */}
              <Typography variant="h6" gutterBottom>
                Analysis Results
              </Typography>

              {sentimentResult && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Sentiment Analysis
                  </Typography>
                  <SentimentChart data={{
                    positive: { current_percentage: sentimentResult.positive * 100 },
                    negative: { current_percentage: sentimentResult.negative * 100 },
                    neutral: { current_percentage: sentimentResult.neutral * 100 },
                  }} />
                  <Box sx={{ mt: 2 }}>
                    <Chip label={`Positive: ${(sentimentResult.positive * 100).toFixed(1)}%`} color="success" sx={{ mr: 1 }} />
                    <Chip label={`Negative: ${(sentimentResult.negative * 100).toFixed(1)}%`} color="error" sx={{ mr: 1 }} />
                    <Chip label={`Neutral: ${(sentimentResult.neutral * 100).toFixed(1)}%`} color="default" />
                  </Box>
                </Box>
              )}

              {topicsResult && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Topic Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Dominant Topic: <strong>{topicsResult.dominant_topic}</strong>
                  </Typography>
                  <Grid container spacing={2}>
                    {topicsResult.topics?.slice(0, 3).map((topic, index) => (
                      <Grid item xs={12} sm={4} key={index}>
                        <Card variant="outlined">
                          <CardContent>
                            <Typography variant="subtitle2" gutterBottom>
                              Topic {topic.topic_id + 1}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {topic.label}
                            </Typography>
                            <Box sx={{ mt: 1 }}>
                              {topic.words?.slice(0, 3).map((word, wordIndex) => (
                                <Chip
                                  key={wordIndex}
                                  label={word}
                                  size="small"
                                  variant="outlined"
                                  sx={{ mr: 0.5, mb: 0.5 }}
                                />
                              ))}
                            </Box>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}

              {summaryResult && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Article Summary
                  </Typography>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="body1">
                        {summaryResult.summary}
                      </Typography>
                      {summaryResult.key_points && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="subtitle2" gutterBottom>
                            Key Points:
                          </Typography>
                          <ul>
                            {summaryResult.key_points.map((point, index) => (
                              <li key={index}>
                                <Typography variant="body2">{point}</Typography>
                              </li>
                            ))}
                          </ul>
                        </Box>
                      )}
                    </CardContent>
                  </Card>
                </Box>
              )}

              {keywordsResult && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Keyword Extraction
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Found {keywordsResult.total_keywords} unique keywords from {keywordsResult.articles_analyzed} articles
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {Object.entries(keywordsResult.keywords || {}).map(([keyword, frequency]) => (
                      <Chip
                        key={keyword}
                        label={`${keyword} (${frequency})`}
                        variant="outlined"
                        size="small"
                      />
                    ))}
                  </Box>
                </Box>
              )}

              {!sentimentResult && !topicsResult && !summaryResult && !keywordsResult && !isAnalysisLoading && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Analytics sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    No Analysis Results Yet
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Select articles and choose an analysis type to get started.
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

export default AnalysisPage;
