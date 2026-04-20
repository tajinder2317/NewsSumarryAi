#!/usr/bin/env python3
"""
Backend entry point for Vercel experimental services
"""
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables for serverless deployment
os.environ.setdefault("VERCEL", "1")
os.environ.setdefault("DATABASE_URL", "sqlite:///./database.db")

# Configure logging for serverless
import logging
logging.basicConfig(level=logging.INFO)

# Import and configure the FastAPI app
try:
    from app.main import app
    # Export the app for Vercel experimental services
    handler = app
except Exception as e:
    logging.error(f"Error importing app: {e}")
    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI(title="News Analyzer API")
    
    @app.get("/")
    async def root():
        return {"message": "News Analyzer API - Basic Mode", "error": str(e)}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "mode": "basic"}
    
    handler = app
