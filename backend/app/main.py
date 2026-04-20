from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
import logging
import os

from .config import settings
from .models import get_db, create_tables
from .api import news, analysis, trends

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="News Analyzer AI",
    description="An AI-powered news analysis and summarization platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Vercel deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(news.router, prefix="/api/v1/news", tags=["news"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(trends.router, prefix="/api/v1/trends", tags=["trends"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and other startup tasks"""
    logger.info("Starting News Analyzer AI...")
    
    try:
        # For serverless deployment, handle database initialization differently
        if os.getenv("VERCEL"):
            # In serverless, create database on-demand
            logger.info("Serverless deployment detected - database will be created on demand")
        else:
            # Create data directory if it doesn't exist
            log_dir = os.path.dirname(settings.LOG_FILE)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            db_dir = os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", ""))
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            
            # Create database tables
            create_tables()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        # Don't fail startup, log the error and continue

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks"""
    logger.info("Shutting down News Analyzer AI...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "News Analyzer AI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Service is running"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
