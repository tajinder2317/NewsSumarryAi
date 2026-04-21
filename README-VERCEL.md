# Vercel Multi-Service Deployment

This project is configured for Vercel deployment with both frontend and backend services.

## Quick Start

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

## Project Structure

```
NewsSumarryAi/
|-- vercel.json              # Multi-service configuration
|-- frontend/                # React frontend
|   |-- .env.production      # Production environment
|   |-- package.json
|   |-- build/               # Built app
|-- backend/                 # FastAPI backend
|   |-- api/
|   |   |-- index.py         # Serverless entry point
|   |-- requirements-vercel.txt
```

## Configuration Details

### vercel.json
- **Frontend**: Static build from `frontend/package.json`
- **Backend**: Serverless functions from `backend/api/index.py`
- **Routing**: `/api/*` routes to backend, everything else to frontend

### Environment Variables

Set these in your Vercel dashboard:

**Backend:**
```
DATABASE_URL=sqlite:///./database.db
NEWS_API_KEY=your_news_api_key_here
RSS_FEEDS=http://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss
DEBUG=False
```

**Frontend:**
```
REACT_APP_API_URL=/api
```

## Features

- **Automatic routing** between frontend and backend
- **Serverless functions** for API endpoints
- **Static site generation** for React app
- **Environment-specific configurations**
- **Zero-config deployment**

## API Endpoints

All backend endpoints are available under `/api/v1/`:

- `GET /api/v1/news/` - Get news articles
- `POST /api/v1/news/collect` - Collect news
- `GET /api/v1/analysis/statistics` - Analysis stats
- `GET /api/health` - Health check

## Troubleshooting

### Build Issues
- Check `vercel.json` syntax
- Verify all dependencies in `requirements-vercel.txt`
- Ensure frontend builds locally first

### Runtime Issues
- Check Vercel function logs
- Verify environment variables
- Test with `vercel dev` locally

### Database Issues
- SQLite database resets on each deployment
- Consider Vercel Postgres for production
- Check file permissions for database access

## Production Considerations

For production use:
1. **Database**: Upgrade to Vercel Postgres
2. **Caching**: Add Redis for performance
3. **Monitoring**: Set up Vercel Analytics
4. **Security**: Configure rate limiting
5. **Domain**: Add custom domain

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI on Vercel](https://vercel.com/guides/fastapi)
- [React on Vercel](https://vercel.com/guides/react)
