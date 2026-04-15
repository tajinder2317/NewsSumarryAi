import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database.db")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # News API
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    NEWS_API_URL = os.getenv("NEWS_API_URL", "https://newsapi.org/v2")
    
    # RSS Feeds
    RSS_FEEDS = os.getenv("RSS_FEEDS", "").split(",") if os.getenv("RSS_FEEDS") else []
    
    # Analysis Configuration
    SENTIMENT_ANALYSIS_ENABLED = os.getenv("SENTIMENT_ANALYSIS_ENABLED", "True").lower() == "true"
    TOPIC_MODELING_ENABLED = os.getenv("TOPIC_MODELING_ENABLED", "True").lower() == "true"
    SUMMARIZATION_ENABLED = os.getenv("SUMMARIZATION_ENABLED", "True").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "./data/logs/app.log")

settings = Settings()
