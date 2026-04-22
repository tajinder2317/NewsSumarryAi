import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_PRISMA_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("POSTGRES_URL_NON_POOLING")
        or os.getenv("NEON_DATABASE_URL")
        or os.getenv("SUPABASE_URL")
        or os.getenv("NILE_DATABASE_URL")
        or "sqlite:///./data/database.db"
    )
    
    # Handle Supabase connection string format
    if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_PASSWORD"):
        supabase_db_url = f"{os.getenv('SUPABASE_URL')}/postgres?password={os.getenv('SUPABASE_PASSWORD')}"
        DATABASE_URL = supabase_db_url
    
    # In Vercel serverless, SQLite is non-persistent. Keep app booting so `/healthz` can report config issues.
    DB_CONFIG_WARNING = None
    if os.getenv("VERCEL") and DATABASE_URL.startswith("sqlite"):
        DB_CONFIG_WARNING = (
            "Missing external database configuration for Vercel. "
            "Set DATABASE_URL or POSTGRES_PRISMA_URL in backend project environment variables."
        )
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # News API
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
    NEWS_API_URL = os.getenv("NEWS_API_URL", "https://newsapi.org/v2")
    
    # RSS Feeds
    RSS_FEEDS = os.getenv("RSS_FEEDS", "").split(",") if os.getenv("RSS_FEEDS") else [
        # International News
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss",
        "https://feeds.reuters.com/reuters/topNews",
        "https://feeds.apnews.com/apnews/topnews",
        
        # US News
        "https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "https://feeds.washingtonpost.com/rss/politics",
        "https://feeds.nbcnews.com/nbcnews/public/news",
        
        # Business News
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.finance.yahoo.com/rss/2.0/headline",
        "https://feeds.marketwatch.com/marketwatch/topstories",
        
        # Tech News
        "https://feeds.feedburner.com/techcrunch",
        "https://feeds.wired.com/wired/index",
        "https://feeds.arstechnica.com/arstechnica/index",
        
        # International Perspectives
        "https://feeds.feedburner.com/TheGuardian-World-News",
        "https://feeds.aljazeera.com/xml/rss/all",
        "https://feeds.dw.com/xml/rss/all",
        
        # Asian News
        "https://feeds.channelnewsasia.com/cna/topstories.rss",
        "https://feeds.bbc.co.uk/news/world/asia/rss.xml"
    ]
    
    # Analysis Configuration
    SENTIMENT_ANALYSIS_ENABLED = os.getenv("SENTIMENT_ANALYSIS_ENABLED", "True").lower() == "true"
    TOPIC_MODELING_ENABLED = os.getenv("TOPIC_MODELING_ENABLED", "True").lower() == "true"
    SUMMARIZATION_ENABLED = os.getenv("SUMMARIZATION_ENABLED", "True").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "./data/logs/app.log")

settings = Settings()
