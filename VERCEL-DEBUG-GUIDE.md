# Vercel Debugging Guide for White Screen Issue

## Problem
White screen on News and Analytics pages after Vercel deployment.

## Debugging Steps

### 1. Check Browser Console
Open browser developer tools and check:
- Network tab for failed API calls
- Console tab for JavaScript errors
- Any 404 or 500 errors

### 2. Test API Endpoints Directly
Test these URLs in browser:
- `https://your-app.vercel.app/api/health`
- `https://your-app.vercel.app/api/v1/news/`
- `https://your-app.vercel.app/api/v1/trends/summary`

### 3. Common Issues & Solutions

#### Issue: API Handler Not Working
**Symptoms**: White screen, no data loading
**Solution**: Check if `vercel_handler.py` is being used correctly

#### Issue: CORS Problems
**Symptoms**: Network errors in console
**Solution**: Ensure CORS headers are properly set

#### Issue: Frontend API URL
**Symptoms**: Requests going to wrong URL
**Solution**: Check `REACT_APP_API_URL` environment variable

### 4. Quick Fix Test

Replace the API handler with a minimal version:

```python
# backend/api/vercel_handler.py
def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"status": "API is working"}'
    }
```

### 5. Deployment Checklist

- [ ] `vercel.json` routes to correct handler
- [ ] Frontend uses `/api` as base URL
- [ ] CORS headers included in responses
- [ ] No JavaScript errors in console
- [ ] API endpoints return 200 status

### 6. Alternative Solutions

#### Option A: Use Vercel Functions
Create separate function files for each endpoint.

#### Option B: Static Mock Data
Serve static JSON files instead of serverless functions.

#### Option C: External API
Deploy backend separately and use external API URL.

### 7. Files to Check

- `backend/api/vercel_handler.py` - Main API handler
- `vercel.json` - Vercel configuration
- `frontend/src/services/api.js` - Frontend API calls
- Browser console - Error messages

## Next Steps

1. Deploy the updated `vercel_handler.py`
2. Check browser console for specific errors
3. Test API endpoints manually
4. Verify Vercel deployment logs
5. If still broken, try minimal static approach
