import json

def handler(request):
    """
    Simple Vercel serverless handler for News API
    """
    try:
        # Get the request path
        path = request.url if hasattr(request, 'url') else str(request)
        
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
        
        # Return JSON response with CORS headers
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        # Error response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
