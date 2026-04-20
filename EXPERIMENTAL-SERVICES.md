# Vercel Experimental Services Deployment

This project uses Vercel's experimental services feature for multi-service deployment with frontend and backend.

## Configuration Overview

### vercel.json
```json
{
  "version": 2,
  "experimentalServices": {
    "frontend": {
      "entrypoint": "frontend",
      "routePrefix": "/",
      "framework": "create-react-app"
    },
    "backend": {
      "entrypoint": "backend",
      "routePrefix": "/api"
    }
  },
  "env": {
    "PYTHON_VERSION": "3.14"
  }
}
```

## Service Architecture

### Frontend Service
- **Entrypoint**: `frontend/` directory
- **Route Prefix**: `/` (serves the root domain)
- **Framework**: Create React App
- **Build Output**: Static files in `frontend/build/`

### Backend Service
- **Entrypoint**: `backend/` directory
- **Route Prefix**: `/api` (all API endpoints)
- **Framework**: FastAPI
- **Runtime**: Python 3.14

## URL Structure

With experimental services, the URLs are structured as:

```
https://your-domain.vercel.app/          -> Frontend (React App)
https://your-domain.vercel.app/api/      -> Backend (FastAPI)
https://your-domain.vercel.app/api/v1/news/ -> News API endpoints
https://your-domain.vercel.app/api/docs  -> API Documentation
```

## Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
vercel --prod
```

## Environment Variables

### Backend Environment Variables
Set these in your Vercel dashboard:

```
DATABASE_URL=sqlite:///./database.db
NEWS_API_KEY=your_news_api_key_here
NEWS_API_URL=https://newsapi.org/v2
RSS_FEEDS=http://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss
DEBUG=False
LOG_LEVEL=INFO
```

### Frontend Environment Variables
Automatically configured via `.env.production`:
```
REACT_APP_API_URL=/api
```

## File Structure

```
NewsSumarryAi/
|-- vercel.json                    # Experimental services config
|-- frontend/
|   |-- .env.production           # Production env vars
|   |-- package.json
|   |-- src/
|   |-- build/                    # Built React app
|-- backend/
|   |-- vercel.json               # Backend-specific config
|   |-- app/
|   |   |-- main.py               # FastAPI app
|   |-- requirements-vercel.txt   # Python dependencies
```

## API Endpoints

All backend endpoints are available under `/api/` prefix:

### News Endpoints
- `GET /api/v1/news/` - Get news articles
- `POST /api/v1/news/collect` - Collect news from sources
- `GET /api/v1/news/sources/list` - List news sources
- `GET /api/v1/news/stats/summary` - News statistics

### Analysis Endpoints
- `GET /api/v1/analysis/statistics` - Analysis statistics
- `POST /api/v1/analysis/sentiment` - Sentiment analysis
- `POST /api/v1/analysis/topics` - Topic analysis
- `POST /api/v1/analysis/summarize` - Text summarization

### Trends Endpoints
- `GET /api/v1/trends/source-trends` - Source trends
- `GET /api/v1/trends/sentiment-trends` - Sentiment trends
- `GET /api/v1/trends/analysis` - Trend analysis

### Utility Endpoints
- `GET /api/health` - Health check
- `GET /api/docs` - API documentation
- `GET /api/` - Root endpoint

## Benefits of Experimental Services

1. **Isolated Services**: Frontend and backend run independently
2. **Automatic Routing**: No manual route configuration needed
3. **Framework Detection**: Automatic framework detection and optimization
4. **Shared Environment**: Services can share environment variables
5. **Simplified Deployment**: Single command deployment for both services

## Development vs Production

### Development (Local)
```bash
# Frontend
cd frontend && npm start

# Backend
cd backend && python run.py
```

### Production (Vercel)
```bash
vercel --prod
```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Backend CORS is configured to allow all origins
   - Check that frontend uses `/api` prefix for API calls

2. **Build Failures**
   - Ensure frontend builds locally: `cd frontend && npm run build`
   - Check backend dependencies in `requirements-vercel.txt`

3. **Database Issues**
   - SQLite database resets on each deployment
   - Consider upgrading to Vercel Postgres for production

4. **API Routes Not Found**
   - Verify backend service is accessible at `/api/`
   - Check Vercel function logs

### Debug Commands

```bash
# Check deployment status
vercel ls

# View function logs
vercel logs

# Test locally with experimental services
vercel dev
```

## Performance Considerations

### Frontend Optimization
- Static asset optimization by Vercel
- Automatic CDN distribution
- Edge caching for static files

### Backend Optimization
- Serverless functions scale automatically
- Cold start optimization
- Response caching for API endpoints

## Monitoring

Set up monitoring in Vercel dashboard:
- **Analytics**: Page views and performance
- **Function Logs**: API request logs
- **Error Tracking**: Automatic error reporting

## Production Upgrades

For production workloads:
1. **Database**: Upgrade to Vercel Postgres
2. **Caching**: Add Redis for session/data caching
3. **CDN**: Vercel Edge Network (automatic)
4. **Security**: Rate limiting and authentication
5. **Domain**: Custom domain configuration

## Support

- [Vercel Experimental Services](https://vercel.com/docs/concepts/projects/experimental-services)
- [FastAPI on Vercel](https://vercel.com/guides/fastapi)
- [React on Vercel](https://vercel.com/guides/react)
