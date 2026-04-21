from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from datetime import datetime
import os
from ..config import settings

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False, index=True)  # Add index for source filtering
    author = Column(String)
    published_date = Column(DateTime, index=True)  # Add index for date ordering
    collected_date = Column(DateTime, default=datetime.utcnow)
    region = Column(String, index=True)
    
    # Analysis fields
    sentiment_score = Column(Float)
    sentiment_label = Column(String, index=True)  # Add index for sentiment filtering
    topics = Column(Text)  # JSON string of topics
    category = Column(String, index=True)  # Add index for category filtering
    
    def __repr__(self):
        return f"<NewsArticle(id={self.id}, title='{self.title[:50]}...', source='{self.source}')>"

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_type = Column(String, nullable=False)  # sentiment, topics, trends
    result_data = Column(Text, nullable=False)  # JSON string
    created_date = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnalysisResult(id={self.id}, type='{self.analysis_type}')>"

# Database setup - handle serverless environment
try:
    url = make_url(settings.DATABASE_URL)

    connect_args = {}
    if url.drivername.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Database setup failed: {e}")
    # Fallback to in-memory database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global variable to track if tables are created
_tables_created = False

def get_db():
    global _tables_created
    try:
        # Create tables on first database access in serverless
        if not _tables_created:
            create_tables()
            _tables_created = True
        
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        # If database fails, return None and let the endpoint handle it
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database error: {e}")
        yield None

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)

        # Lightweight schema patching for existing databases (no Alembic in this repo).
        # Add `region` column if the table already exists without it.
        try:
            with engine.begin() as conn:
                if engine.dialect.name == "sqlite":
                    conn.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                else:
                    conn.execute(text("ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS region VARCHAR"))
        except Exception:
            # Column already exists or dialect doesn't support IF NOT EXISTS.
            pass
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not create tables: {e}")
        # Don't raise error, just log it
