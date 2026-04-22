# Vercel Deployment Setup Guide

## Database Setup Options

### Option 1: Prisma PostgreSQL (Recommended)

1. **Create Prisma PostgreSQL Database**

   ```bash
   # In your Vercel project dashboard:
   # 1. Go to Storage tab
   # 2. Click "Create Database"
   # 3. Select "Prisma PostgreSQL"
   # 4. Choose region (closest to your users)
   # 5. Click "Create"
   ```

2. **Get Database Connection String**
   - After creation, go to Storage > Your Database > ".env.local" tab
   - Copy the `POSTGRES_PRISMA_URL` environment variable

3. **Add Environment Variables to Vercel**
   ```bash
   # In Vercel project dashboard > Settings > Environment Variables:
   POSTGRES_PRISMA_URL=your_prisma_postgres_connection_string
   VERCEL=true
   ```

### Option 2: Neon (PostgreSQL)

1. **Create Neon Database**

   ```bash
   # In your Vercel project dashboard:
   # 1. Go to Storage tab
   # 2. Click "Create Database"
   # 3. Select "Neon"
   # 4. Follow Neon setup process
   ```

2. **Add Environment Variables to Vercel**
   ```bash
   NEON_DATABASE_URL=postgresql://[user]:[password]@[neon-hostname]/[dbname]?sslmode=require
   ```

### Option 3: Supabase (PostgreSQL)

1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create new project
   - Get project URL and database password

2. **Add Environment Variables to Vercel**
   ```bash
   SUPABASE_URL=https://[project-id].supabase.co
   SUPABASE_PASSWORD=your_database_password
   ```

### Option 4: Nile (PostgreSQL)

1. **Create Nile Database**

   ```bash
   # In your Vercel project dashboard:
   # 1. Go to Storage tab
   # 2. Click "Create Database"
   # 3. Select "Nile"
   # 4. Follow Nile setup process
   ```

2. **Add Environment Variables to Vercel**
   ```bash
   NILE_DATABASE_URL=postgresql://[user]:[password]@[nile-hostname]/[dbname]?sslmode=require
   ```

### Option 5: Vercel Blob (For File Storage Only)

- Note: Blob storage is for files, not relational data
- Use this for storing images, documents, etc.
- Not suitable for news article database

## Frontend Configuration

### Environment Variables for Frontend

Create `.env.production` in `frontend/` directory:

```env
# Set backend URL for separate deployment
REACT_APP_API_URL=https://your-backend-domain.vercel.app
```

### Environment Variables for Backend

Add these to your Vercel project:

```env
NEWS_API_KEY=your_news_api_key  # Optional, from newsapi.org
RSS_FEEDS=https://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss
SENTIMENT_ANALYSIS_ENABLED=true
TOPIC_MODELING_ENABLED=true
SUMMARIZATION_ENABLED=true
LOG_LEVEL=INFO
```

## Deployment Steps

### For Separate Frontend/Backend Deployment

1. **Deploy Backend First**

   ```bash
   cd backend
   vercel --prod
   # Note the backend URL (e.g., https://your-backend-abc123.vercel.app)
   ```

2. **Update Frontend Configuration**
   - Edit `frontend/.env.production`
   - Set `REACT_APP_API_URL=https://your-backend-abc123.vercel.app`

3. **Deploy Frontend**
   ```bash
   cd frontend
   vercel --prod
   ```

### For Combined Deployment (Single Project)

1. **Install Vercel CLI**

   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**

   ```bash
   vercel login
   ```

3. **Deploy Project**
   ```bash
   # From project root directory
   vercel --prod
   ```

## Troubleshooting

### Issue: News not persisting

**Cause**: Using SQLite on serverless functions
**Solution**: Use external database (Vercel Postgres recommended)

### Issue: Frontend can't reach backend

**Cause**: API routing configuration
**Solution**: Check `vercel.json` routes configuration

### Issue: Database connection errors

**Cause**: Missing environment variables or incorrect connection string
**Solution**: Verify DATABASE_URL or POSTGRES_URL in Vercel dashboard

### Issue: CORS errors

**Cause**: Frontend and backend deployed separately
**Solution**: Set REACT_APP_API_URL to backend domain

## Testing Deployment

1. **Health Check**

   ```bash
   curl https://your-app.vercel.app/health
   ```

2. **API Documentation**

   ```bash
   # Visit in browser:
   https://your-app.vercel.app/docs
   ```

3. **Test News Collection**
   ```bash
   curl -X POST https://your-app.vercel.app/api/v1/news/collect
   ```

## Monitoring

- Check Vercel Logs for any errors
- Monitor database usage in Vercel Storage tab
- Test API endpoints regularly

## Cost Considerations

- **Vercel Postgres**: Free tier available (500MB storage, 60 hours compute/month)
- **PlanetScale**: Free tier available
- **Supabase**: Free tier available
- **Neon**: Free tier available

Choose based on your expected traffic and requirements.
