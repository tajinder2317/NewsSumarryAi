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

# Import and configure the FastAPI app
from app.main import app

# Vercel will automatically handle the FastAPI app
# No custom handler needed - Vercel Python runtime handles FastAPI natively
