"""
Vercel serverless entry for the FastAPI app.

This replaces the previous mock WSGI handler so the deployed API serves real data.
"""
import sys
from pathlib import Path

# Ensure `backend/` is on sys.path so `app.*` imports work.
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from app.main import app  # noqa: E402

