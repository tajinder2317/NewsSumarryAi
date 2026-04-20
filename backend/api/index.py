#!/usr/bin/env python3
"""
Vercel serverless function entry point for News Analyzer AI backend
"""
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
current_dir = Path(__file__).parent
backend_dir = current_dir.parent
sys.path.insert(0, str(backend_dir))

# Set environment variables for serverless deployment
os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DATABASE_URL", "sqlite:///./database.db")

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

# Import and configure the FastAPI app
try:
    from app.main import app
    handler = app
    logging.info("FastAPI app imported successfully")
except Exception as e:
    logging.error(f"Error importing FastAPI app: {e}")
    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI(title="News Analyzer API - Fallback")
    
    @app.get("/")
    async def root():
        return {"message": "News Analyzer API - Fallback Mode", "error": str(e)}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "mode": "fallback"}
    
    handler = app
    logging.info("Fallback FastAPI app created")
