# Vercel Deployment Fix

## Issues Fixed

1. **Removed conflicting vercel.json** from backend directory
2. **Switched from experimental services to standard configuration**
3. **Fixed backend entry point** for serverless functions
4. **Updated routing configuration** for proper API access

## Updated Configuration

### vercel.json (Root)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    },
    {
      "src": "backend/api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/backend/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ],
  "env": {
    "PYTHON_VERSION": "3.14"
  }
}
```

### Backend API Entry Point
- **File**: `backend/api/index.py`
- **Purpose**: Serverless function entry point
- **Exports**: FastAPI app as `handler`

## Deployment Steps

### 1. Push Changes to GitHub
```bash
git add .
git commit -m "Fix Vercel deployment configuration"
git push origin main
```

### 2. Redeploy to Vercel
```bash
vercel --prod
```

### 3. Set Environment Variables
In Vercel dashboard, set:
```
DATABASE_URL=sqlite:///./database.db
NEWS_API_KEY=your_news_api_key_here
RSS_FEEDS=http://feeds.bbci.co.uk/news/rss.xml,https://rss.cnn.com/rss/edition.rss
DEBUG=False
```

## URL Structure After Fix

```
https://your-domain.vercel.app/          -> Frontend (React)
https://your-domain.vercel.app/api/      -> Backend (FastAPI)
https://your-domain.vercel.app/api/v1/news/ -> News API
https://your-domain.vercel.app/api/docs  -> API Documentation
```

## Why This Fix Works

1. **Standard Configuration**: Uses proven Vercel setup instead of experimental features
2. **Proper Routing**: Clear API routing to backend functions
3. **Serverless Compatible**: Backend entry point optimized for serverless
4. **No Conflicts**: Single vercel.json prevents configuration conflicts

## Testing the Deployment

After deployment, test:
1. Frontend loads at root URL
2. API endpoints accessible at `/api/v1/`
3. Health check at `/api/health`
4. API docs at `/api/docs`

## Troubleshooting

If deployment still fails:
1. Check Vercel build logs
2. Verify all dependencies in requirements.txt
3. Test locally with `vercel dev`
4. Contact Vercel support if needed
