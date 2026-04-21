import sys
import os
import json
from urllib.parse import parse_qs

# Simple API endpoints for Vercel deployment
def handler(environ, start_response):
    """
    Simple Vercel serverless handler for News API
    """
    try:
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        query_string = environ.get('QUERY_STRING', '')
        
        # Parse query parameters
        query_params = {}
        if query_string:
            query_params = parse_qs(query_string)
            # Convert lists to single values
            query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        # Get request body
        body = b''
        content_length = environ.get('CONTENT_LENGTH')
        if method in ['POST', 'PUT', 'PATCH'] and content_length:
            wsgi_input = environ.get('wsgi.input')
            if wsgi_input:
                body = wsgi_input.read(int(content_length))
        
        # Simple routing with mock data
        if path == '/api/health':
            response_data = {'status': 'healthy', 'message': 'News API is running'}
        elif path == '/api/v1/news/':
            # Mock news articles for News page
            response_data = [
                {
                    'id': 1,
                    'title': 'Breaking News: AI Technology Advances',
                    'content': 'Latest developments in artificial intelligence technology are transforming industries worldwide.',
                    'url': 'https://example.com/news/1',
                    'source': 'Tech News',
                    'author': 'AI Reporter',
                    'published_date': '2026-04-21T10:00:00Z',
                    'summary': 'AI technology continues to advance rapidly.',
                    'sentiment_score': 0.5,
                    'sentiment_label': 'neutral',
                    'category': 'Technology'
                },
                {
                    'id': 2,
                    'title': 'Global Climate Summit Results',
                    'content': 'World leaders agree on new climate action plans to address environmental challenges.',
                    'url': 'https://example.com/news/2',
                    'source': 'World News',
                    'author': 'Climate Reporter',
                    'published_date': '2026-04-21T09:30:00Z',
                    'summary': 'New climate agreements reached at global summit.',
                    'sentiment_score': 0.7,
                    'sentiment_label': 'positive',
                    'category': 'Environment'
                },
                {
                    'id': 3,
                    'title': 'Economic Markets Update',
                    'content': 'Stock markets show positive trends as economic indicators improve.',
                    'url': 'https://example.com/news/3',
                    'source': 'Financial News',
                    'author': 'Economy Reporter',
                    'published_date': '2026-04-21T08:45:00Z',
                    'summary': 'Markets respond positively to economic data.',
                    'sentiment_score': 0.6,
                    'sentiment_label': 'positive',
                    'category': 'Business'
                }
            ]
        elif path == '/api/v1/news/stats/summary':
            # Mock stats for Dashboard
            response_data = {
                'total_articles': 156,
                'recent_articles_24h': 23,
                'sources': [
                    {'source': 'Tech News', 'count': 45},
                    {'source': 'World News', 'count': 38},
                    {'source': 'Financial News', 'count': 32},
                    {'source': 'Sports News', 'count': 28},
                    {'source': 'Health News', 'count': 13}
                ],
                'sentiment_distribution': [
                    {'sentiment': 'positive', 'count': 78},
                    {'sentiment': 'neutral', 'count': 56},
                    {'sentiment': 'negative', 'count': 22}
                ]
            }
        elif path == '/api/v1/trends/summary':
            # Mock trends for Home page
            response_data = {
                'summary': {
                    'trending_topics': [
                        {
                            'topic_id': 1,
                            'topic_name': 'Artificial Intelligence',
                            'article_count': 15,
                            'top_terms': ['AI', 'machine learning', 'automation'],
                            'trend_score': 0.85
                        },
                        {
                            'topic_id': 2,
                            'topic_name': 'Climate Change',
                            'article_count': 12,
                            'top_terms': ['climate', 'environment', 'sustainability'],
                            'trend_score': 0.72
                        },
                        {
                            'topic_id': 3,
                            'topic_name': 'Economy',
                            'article_count': 10,
                            'top_terms': ['markets', 'finance', 'business'],
                            'trend_score': 0.68
                        }
                    ]
                }
            }
        elif path == '/api/v1/analysis/sentiment':
            # Mock sentiment analysis
            response_data = {
                'positive': 0.65,
                'negative': 0.15,
                'neutral': 0.20,
                'label': 'positive'
            }
        elif path == '/api/v1/analysis/topics':
            # Mock topic analysis
            response_data = {
                'topics': [
                    {'topic_id': 1, 'words': ['technology', 'innovation'], 'weights': [0.8, 0.7], 'label': 'Technology'},
                    {'topic_id': 2, 'words': ['business', 'finance'], 'weights': [0.9, 0.8], 'label': 'Business'},
                    {'topic_id': 3, 'words': ['health', 'medicine'], 'weights': [0.7, 0.6], 'label': 'Health'}
                ],
                'dominant_topic': 'Technology'
            }
        elif path == '/api/v1/analysis/summarize':
            # Mock summarization
            response_data = {
                'article_id': 1,
                'summary': 'This article discusses the latest developments in artificial intelligence technology and its impact on various industries.',
                'key_points': [
                    'AI technology is advancing rapidly',
                    'Multiple industries are being transformed',
                    'Future implications are significant'
                ]
            }
        elif path == '/api/v1/analysis/keywords':
            # Mock keyword extraction
            response_data = {
                'keywords': [
                    {'keyword': 'artificial intelligence', 'score': 0.9},
                    {'keyword': 'technology', 'score': 0.8},
                    {'keyword': 'innovation', 'score': 0.7},
                    {'keyword': 'industry', 'score': 0.6},
                    {'keyword': 'development', 'score': 0.5}
                ]
            }
        else:
            response_data = {'message': 'API endpoint not found', 'path': path}
        
        # Convert to JSON
        response_body = json.dumps(response_data).encode('utf-8')
        
        # Start response
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body))),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ])
        
        return [response_body]
        
    except Exception as e:
        # Error response
        error_body = json.dumps({'error': str(e)}).encode('utf-8')
        start_response('500 Internal Server Error', [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(error_body))),
            ('Access-Control-Allow-Origin', '*'),
        ])
        return [error_body]
