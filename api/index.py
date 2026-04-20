#!/usr/bin/env python3
"""
Minimal Vercel serverless function for backend API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="News Analyzer AI API",
    description="AI-powered news analysis and summarization platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "News Analyzer AI API",
        "version": "1.0.0",
        "status": "running",
        "environment": "vercel"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}

@app.get("/api/v1/news/")
async def get_news():
    """Get news articles"""
    return {
        "articles": [],
        "message": "News collection endpoint - backend is working"
    }

@app.post("/api/v1/news/collect")
async def collect_news():
    """Collect news from sources"""
    return {
        "message": "News collection endpoint - backend is working",
        "collected_count": 0,
        "total_articles": 0,
        "articles_processed": 0,
        "timeout": False
    }

# Export for Vercel
handler = app
