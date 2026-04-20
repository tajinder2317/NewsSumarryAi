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
  Fade,
  Avatar,
} from '@mui/material';
import {
  OpenInNew,
  Share,
  Bookmark,
  BookmarkBorder,
  TrendingUp,
  TrendingDown,
  Remove,
  Schedule,
  Person,
  Tag,
} from '@mui/icons-material';
import moment from 'moment';

const NewsCard = ({ article, onAnalyze, onDelete, showActions = true }) => {
  const [isBookmarked, setIsBookmarked] = React.useState(false);
  const [isHovered, setIsHovered] = React.useState(false);

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

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
    // Here you would typically save to backend/localStorage
  };

  const formatDate = (dateString) => {
    return moment(dateString).fromNow();
  };

  const getSourceInitials = (source) => {
    return source?.slice(0, 2).toUpperCase() || 'NN';
  };

  return (
    <Fade in timeout={300}>
      <Card
        className="news-card"
        sx={{
          mb: 3,
          position: 'relative',
          transition: 'all 0.3s ease-in-out',
          transform: isHovered ? 'translateY(-4px)' : 'translateY(0)',
          boxShadow: isHovered ? '0 12px 24px rgba(0,0,0,0.15)' : '0 4px 12px rgba(0,0,0,0.08)',
          border: '1px solid rgba(0,0,0,0.08)',
          borderRadius: 2,
          overflow: 'visible',
          cursor: 'pointer',
          '&:hover': {
            '& .news-card-title': {
              color: 'primary.main',
            }
          }
        }}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
      >
        <CardContent sx={{ pb: 2 }}>
          {/* Header with source avatar and date */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar
              sx={{
                width: 32,
                height: 32,
                mr: 2,
                bgcolor: 'primary.main',
                fontSize: '0.875rem',
                fontWeight: 'bold'
              }}
            >
              {getSourceInitials(article.source)}
            </Avatar>
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 600, color: 'text.primary' }}>
                {article.source}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Schedule sx={{ fontSize: 14, color: 'text.secondary' }} />
                <Typography variant="caption" color="text.secondary">
                  {article.published_date ? formatDate(article.published_date) : 'Unknown date'}
                </Typography>
              </Box>
            </Box>

            {article.sentiment_label && (
              <Chip
                icon={getSentimentIcon(article.sentiment_label)}
                label={article.sentiment_label}
                size="small"
                color={getSentimentColor(article.sentiment_label)}
                variant="filled"
                sx={{
                  fontWeight: 500,
                  '& .MuiChip-icon': {
                    fontSize: 16
                  }
                }}
              />
            )}
          </Box>

          {/* Title */}
          <Typography
            variant="h6"
            component="h3"
            className="news-card-title"
            gutterBottom
            sx={{
              fontWeight: 600,
              lineHeight: 1.3,
              mb: 2,
              transition: 'color 0.2s ease',
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden'
            }}
          >
            {article.title}
          </Typography>

          {/* Summary/Content preview */}
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              mb: 2,
              lineHeight: 1.5,
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical',
              overflow: 'hidden'
            }}
          >
            {article.summary || article.content?.substring(0, 200) + '...'}
          </Typography>

          {/* Tags and metadata */}
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
            {article.category && (
              <Chip
                icon={<Tag sx={{ fontSize: 14 }} />}
                label={article.category}
                size="small"
                variant="outlined"
                color="primary"
                sx={{
                  height: 24,
                  '& .MuiChip-icon': {
                    fontSize: 14
                  }
                }}
              />
            )}

            {article.author && (
              <Chip
                icon={<Person sx={{ fontSize: 14 }} />}
                label={article.author}
                size="small"
                variant="outlined"
                sx={{
                  height: 24,
                  '& .MuiChip-icon': {
                    fontSize: 14
                  }
                }}
              />
            )}
          </Box>

          {/* Topics if available */}
          {article.topics && Array.isArray(JSON.parse(article.topics || '[]')) && JSON.parse(article.topics || '[]').length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="caption" color="text.secondary" sx={{ mr: 1, fontWeight: 500 }}>
                Topics:
              </Typography>
              {JSON.parse(article.topics || '[]').slice(0, 3).map((topic, index) => (
                <Chip
                  key={index}
                  label={topic}
                  size="small"
                  variant="filled"
                  sx={{
                    mr: 0.5,
                    mb: 0.5,
                    bgcolor: 'grey.100',
                    color: 'text.secondary',
                    fontSize: '0.7rem',
                    height: 20
                  }}
                />
              ))}
            </Box>
          )}
        </CardContent>

        {showActions && (
          <CardActions sx={{
            justifyContent: 'space-between',
            px: 2,
            pb: 2,
            pt: 0,
            borderTop: '1px solid rgba(0,0,0,0.06)'
          }}>
            <Box>
              <Button
                size="small"
                startIcon={<OpenInNew />}
                onClick={() => window.open(article.url, '_blank')}
                sx={{
                  textTransform: 'none',
                  fontWeight: 500
                }}
              >
                Read More
              </Button>

              {onAnalyze && (
                <Button
                  size="small"
                  variant="outlined"
                  onClick={() => onAnalyze(article.id)}
                  sx={{
                    ml: 1,
                    textTransform: 'none',
                    fontWeight: 500
                  }}
                >
                  Analyze
                </Button>
              )}
            </Box>

            <Box sx={{ display: 'flex', gap: 0.5 }}>
              <Tooltip title="Share">
                <IconButton
                  size="small"
                  onClick={handleShare}
                  sx={{
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      bgcolor: 'primary.main',
                      color: 'primary.contrastText'
                    }
                  }}
                >
                  <Share />
                </IconButton>
              </Tooltip>

              <Tooltip title={isBookmarked ? "Remove from saved" : "Save article"}>
                <IconButton
                  size="small"
                  onClick={handleBookmark}
                  sx={{
                    transition: 'all 0.2s ease',
                    color: isBookmarked ? 'primary.main' : 'inherit',
                    '&:hover': {
                      bgcolor: isBookmarked ? 'primary.main' : 'action.hover',
                      color: isBookmarked ? 'primary.contrastText' : 'inherit'
                    }
                  }}
                >
                  {isBookmarked ? <Bookmark /> : <BookmarkBorder />}
                </IconButton>
              </Tooltip>

              {onDelete && (
                <Tooltip title="Delete">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(article.id)}
                    sx={{
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        bgcolor: 'error.main',
                        color: 'error.contrastText'
                      }
                    }}
                  >
                    <Remove />
                  </IconButton>
                </Tooltip>
              )}
            </Box>
          </CardActions>
        )}
      </Card>
    </Fade>
  );
};

export default NewsCard;
