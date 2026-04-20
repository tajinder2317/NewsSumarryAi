# Vercel Deployment Guide

This guide explains how to deploy the News Analyzer AI application to Vercel with both frontend and backend.

## Architecture Overview

- **Frontend**: React app deployed as static site
- **Backend**: FastAPI deployed as serverless functions
- **Database**: SQLite (file-based) for simplicity

## Prerequisites

1. Vercel account ([vercel.com](https://vercel.com))
2. GitHub account (recommended)
3. Node.js 18+ installed locally

## Deployment Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Configure Environment Variables

In your Vercel dashboard, set these environment variables:

#### Backend Environment Variables
```
DATABASE_URL=sqlite:///./database.db
NEWS_API_KEY=your_news_api_key_here
NEWS_API_URL=https://newsapi.org/v2
RSS_FEEDS=http://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss,https://feeds.reuters.com/reuters/topNews,https://feeds.apnews.com/apnews/topnews
DEBUG=False
LOG_LEVEL=INFO
```

#### Frontend Environment Variables
```
REACT_APP_API_URL=/api
```

### 4. Deploy to Vercel

From the project root directory:

```bash
# Deploy to production
vercel --prod

# Or deploy to preview first
vercel
```

### 5. Configure Custom Domain (Optional)

In Vercel dashboard:
1. Go to Project Settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## File Structure for Vercel

```
NewsSumarryAi/
|-- vercel.json              # Vercel configuration
|-- frontend/
|   |-- .env.production      # Production env vars
|   |-- package.json
|   |-- build/               # Built React app
|-- backend/
|   |-- api/
|   |   |-- index.py         # Serverless entry point
|   |-- requirements-vercel.txt
|-- .vercel/                 # Vercel deployment files
```

## Configuration Files

### vercel.json
- Routes `/api/*` to backend serverless functions
- Routes everything else to frontend
- Configures Python 3.14 runtime

### backend/api/index.py
- Entry point for serverless functions
- Imports and exports FastAPI app

### frontend/.env.production
- Sets API URL to relative path for production

## Database Considerations

For production, consider upgrading from SQLite to:
- **Vercel Postgres** (recommended)
- **PlanetScale** (MySQL)
- **Supabase** (PostgreSQL)

To upgrade database:
1. Update `DATABASE_URL` environment variable
2. Modify SQLAlchemy connection string
3. Run database migrations

## Performance Optimization

### Backend
- Enable response caching
- Use connection pooling for database
- Implement rate limiting

### Frontend
- Enable static asset optimization
- Configure CDN caching
- Use Vercel Analytics

## Monitoring

Set up these monitoring tools:
- **Vercel Analytics** - Performance and usage
- **Vercel Logs** - Error tracking
- **Custom health checks** - API monitoring

## Troubleshooting

### Common Issues

1. **Serverless Function Timeout**
   - Increase timeout in vercel.json
   - Optimize long-running operations

2. **Database Connection Issues**
   - Check DATABASE_URL format
   - Ensure database file is accessible

3. **CORS Errors**
   - Verify API endpoints are properly routed
   - Check frontend API URL configuration

### Debug Commands

```bash
# Check deployment logs
vercel logs

# View function metrics
vercel env ls

# Test locally
vercel dev
```

## Scaling Considerations

For high-traffic deployments:
1. **Database**: Move to managed database service
2. **Caching**: Add Redis for session/data caching
3. **CDN**: Use Vercel Edge Network
4. **Monitoring**: Set up comprehensive alerting

## Security Best Practices

1. **Environment Variables**: Never commit secrets
2. **API Keys**: Rotate regularly
3. **Database**: Use connection strings with SSL
4. **Rate Limiting**: Implement API rate limiting
5. **HTTPS**: Enforce HTTPS (automatic on Vercel)

## Cost Optimization

- **Free Tier**: Vercel Hobby plan includes:
  - 100GB bandwidth/month
  - Serverless functions
  - Static hosting
  
- **Optimization Tips**:
  - Optimize images and assets
  - Implement response caching
  - Monitor function execution time

## Support

For deployment issues:
1. Check [Vercel Documentation](https://vercel.com/docs)
2. Review deployment logs
3. Test locally with `vercel dev`
4. Contact Vercel support if needed
