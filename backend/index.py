#!/usr/bin/env python3
"""
Backend entry point for Vercel serverless deployment
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

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)

# Import the simple API handler
from api.simple_handler import handler as api_handler

# Export the handler for Vercel
handler = api_handler
