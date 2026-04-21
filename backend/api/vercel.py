#!/usr/bin/env python3
"""
Vercel serverless function configuration
"""
import os
import sys

# Set environment variables for serverless deployment
os.environ.setdefault("DATABASE_URL", os.getenv("DATABASE_URL", "sqlite:///./data/database.db"))

# Add backend to path
sys.path.append(os.path.dirname(__file__))
