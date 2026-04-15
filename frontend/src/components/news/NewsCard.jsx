import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Box,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  OpenInNew,
  Share,
  Bookmark,
  TrendingUp,
  TrendingDown,
  Remove,
} from '@mui/icons-material';
import moment from 'moment';

const NewsCard = ({ article, onAnalyze, onDelete, showActions = true }) => {
  const getSentimentIcon = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return <TrendingUp color="success" />;
      case 'negative':
        return <TrendingDown color="error" />;
      default:
        return <Remove color="action" />;
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'error';
      default:
        return 'default';
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: article.title,
        text: article.summary || article.content?.substring(0, 200),
        url: article.url,
      });
    } else {
      navigator.clipboard.writeText(article.url);
      alert('Link copied to clipboard!');
    }
  };

  const formatDate = (dateString) => {
    return moment(dateString).format('MMM DD, YYYY · h:mm A');
  };

  return (
    <Card className="news-card" sx={{ mb: 2, position: 'relative' }}>
      <CardContent>
        {/* Header with source and date */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="caption" color="text.secondary">
            {article.source}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {article.published_date ? formatDate(article.published_date) : 'Unknown date'}
          </Typography>
        </Box>

        {/* Title */}
        <Typography variant="h6" component="h3" gutterBottom sx={{ fontWeight: 600 }}>
          {article.title}
        </Typography>

        {/* Summary/Content preview */}
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {article.summary || article.content?.substring(0, 200) + '...'}
        </Typography>

        {/* Tags and metadata */}
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          {article.category && (
            <Chip
              label={article.category}
              size="small"
              variant="outlined"
              color="primary"
            />
          )}
          
          {article.sentiment_label && (
            <Chip
              icon={getSentimentIcon(article.sentiment_label)}
              label={article.sentiment_label}
              size="small"
              color={getSentimentColor(article.sentiment_label)}
              variant="outlined"
            />
          )}

          {article.author && (
            <Chip
              label={`By: ${article.author}`}
              size="small"
              variant="outlined"
            />
          )}
        </Box>

        {/* Topics if available */}
        {article.topics && (
          <Box sx={{ mb: 2 }}>
            <Typography variant="caption" color="text.secondary" sx={{ mr: 1 }}>
              Topics:
            </Typography>
            {JSON.parse(article.topics || '[]').slice(0, 3).map((topic, index) => (
              <Chip
                key={index}
                label={topic}
                size="small"
                variant="filled"
                sx={{ mr: 0.5, mb: 0.5 }}
              />
            ))}
          </Box>
        )}
      </CardContent>

      {showActions && (
        <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
          <Box>
            <Button
              size="small"
              startIcon={<OpenInNew />}
              onClick={() => window.open(article.url, '_blank')}
            >
              Read More
            </Button>
            
            {onAnalyze && (
              <Button
                size="small"
                variant="outlined"
                onClick={() => onAnalyze(article.id)}
                sx={{ ml: 1 }}
              >
                Analyze
              </Button>
            )}
          </Box>

          <Box>
            <Tooltip title="Share">
              <IconButton size="small" onClick={handleShare}>
                <Share />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Save">
              <IconButton size="small">
                <Bookmark />
              </IconButton>
            </Tooltip>

            {onDelete && (
              <Tooltip title="Delete">
                <IconButton
                  size="small"
                  color="error"
                  onClick={() => onDelete(article.id)}
                >
                  <Remove />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </CardActions>
      )}
    </Card>
  );
};

export default NewsCard;
