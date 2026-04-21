import json
from urllib.parse import parse_qs

# This is the top-level handler function that Vercel expects
def handler(environ, start_response):
    """
    Vercel serverless handler for News API
    """
    try:
        # Get request method and path
        method = environ.get('REQUEST_METHOD', 'GET')
        path = environ.get('PATH_INFO', '/')
        query_string = environ.get('QUERY_STRING', '')
        
        # Parse query parameters
        query_params = {}
        if query_string:
            query_params = parse_qs(query_string)
            # Convert lists to single values
            query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        # Get request body for POST requests
        content_length = environ.get('CONTENT_LENGTH')
        body = b''
        if method in ['POST', 'PUT', 'PATCH'] and content_length:
            wsgi_input = environ.get('wsgi.input')
            if wsgi_input:
                body = wsgi_input.read(int(content_length))
        
        # Simple routing with mock data
        if '/api/health' in path:
            response_data = {'status': 'healthy', 'message': 'News API is running'}
        elif '/api/v1/news/' in path and 'sources' not in path and 'categories' not in path and 'stats' not in path:
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
                }
            ]
        elif '/api/v1/news/sources' in path:
            response_data = ['BBC News', 'CNN', 'Reuters', 'TechCrunch', 'The Guardian']
        elif '/api/v1/news/categories' in path:
            response_data = ['Technology', 'Business', 'Sports', 'Health', 'Entertainment', 'Science', 'Politics']
        elif '/api/v1/news/stats/summary' in path:
            response_data = {
                'total_articles': 156,
                'recent_articles_24h': 23,
                'sources': [
                    {'source': 'Tech News', 'count': 45},
                    {'source': 'World News', 'count': 38}
                ],
                'sentiment_distribution': [
                    {'sentiment': 'positive', 'count': 78},
                    {'sentiment': 'neutral', 'count': 56}
                ]
            }
        elif '/api/v1/trends/summary' in path:
            response_data = {
                'summary': {
                    'trending_topics': [
                        {
                            'topic_name': 'Artificial Intelligence',
                            'article_count': 15,
                            'trend_score': 0.85
                        },
                        {
                            'topic_name': 'Climate Change',
                            'article_count': 12,
                            'trend_score': 0.72
                        }
                    ]
                }
            }
        elif '/api/v1/analysis/' in path:
            response_data = {
                'message': 'Analysis endpoint - mock data',
                'sentiment': {'positive': 0.65, 'negative': 0.15, 'neutral': 0.20, 'label': 'positive'},
                'topics': [
                    {'topic_id': 1, 'words': ['technology', 'innovation'], 'label': 'Technology'}
                ],
                'summary': 'This article discusses AI technology developments.',
                'keywords': [
                    {'keyword': 'artificial intelligence', 'score': 0.9},
                    {'keyword': 'technology', 'score': 0.8}
                ]
            }
        else:
            response_data = {'message': 'API endpoint not found', 'path': path}
        
        # Convert to JSON
        response_body = json.dumps(response_data).encode('utf-8')
        
        # Start response with WSGI interface
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

# Also provide alternative names that Vercel might look for
app = handler
application = handler
