#!/usr/bin/env python3
"""
Vercel serverless function entry point for News Analyzer AI backend
"""
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the FastAPI app
from app.main import app

# Export the app for Vercel
handler = app
