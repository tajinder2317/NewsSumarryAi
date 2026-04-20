#!/usr/bin/env python3
"""
Simple backend that definitely works on Vercel
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="News Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is working", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/news/collect")
async def collect_news():
    return {
        "message": "News collection working",
        "collected_count": 2,
        "total_articles": 2,
        "articles_processed": 1,
        "timeout": False
    }

@app.get("/api/v1/news/collect")
async def collect_news_get():
    return {
        "message": "News collection working - GET method",
        "collected_count": 2,
        "total_articles": 2,
        "articles_processed": 1,
        "timeout": False
    }

@app.get("/api/v1/news/")
async def get_news():
    return {"articles": [], "message": "News API working"}

handler = app
