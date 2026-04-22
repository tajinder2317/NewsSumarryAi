from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url
from datetime import datetime
from fastapi import HTTPException, status
import os
from ..config import settings

Base = declarative_base()
DB_INIT_ERROR = None

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

# Database setup - keep app bootable even if DB init fails.
try:
    url = make_url(settings.DATABASE_URL)

    connect_args = {}
    engine_kwargs = {"pool_pre_ping": True}
    
    if url.drivername.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    elif url.drivername.startswith("postgresql"):
        # PostgreSQL specific settings for Vercel
        engine_kwargs.update({
            "pool_size": 1,
            "max_overflow": 0,
            "pool_timeout": 30,
            "pool_recycle": 300,
        })
        # SSL configuration for Vercel Postgres
        if os.getenv("VERCEL"):
            connect_args = {"sslmode": "require"}

    engine = create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        **engine_kwargs
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Database setup failed: {e}")
    DB_INIT_ERROR = str(e)
    engine = None
    SessionLocal = None

# Global variable to track if tables are created
_tables_created = False

def _ensure_news_articles_schema(db):
    """
    Best-effort schema fixups for existing databases.

    This repo doesn't use Alembic migrations, but the deployed DB may already exist
    (e.g., SQLite file) with an older schema. Ensure required columns exist so ORM
    queries don't crash at runtime.
    """
    try:
        bind = db.get_bind()
        dialect = getattr(bind, "dialect", None)
        dialect_name = getattr(dialect, "name", "")

        if dialect_name == "sqlite":
            cols = db.execute(text("PRAGMA table_info(news_articles)")).fetchall()
            col_names = {c[1] for c in cols}  # (cid, name, type, notnull, dflt_value, pk)
            if "region" not in col_names:
                db.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                db.commit()
        elif dialect_name == "postgresql":
            # Check if column exists first for PostgreSQL
            try:
                result = db.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'news_articles' 
                    AND column_name = 'region'
                """))
                region_exists = result.fetchone() is not None
                
                if not region_exists:
                    db.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                    db.commit()
            except Exception:
                # Fallback: Try adding column directly
                try:
                    db.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                    db.commit()
                except Exception:
                    pass
        else:
            # Postgres supports IF NOT EXISTS; MySQL may not in all versions.
            db.execute(text("ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS region VARCHAR"))
            db.commit()
    except Exception:
        # Ignore any failure (already exists, permissions, unsupported SQL, race, etc.).
        try:
            db.rollback()
        except Exception:
            pass

def get_db():
    global _tables_created
    if SessionLocal is None:
        detail = "Database unavailable. Check backend DATABASE_URL/POSTGRES_PRISMA_URL configuration."
        if settings.DB_CONFIG_WARNING:
            detail = settings.DB_CONFIG_WARNING
        elif DB_INIT_ERROR:
            detail = f"Database initialization failed: {DB_INIT_ERROR}"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )

    # Create tables on first database access
    if not _tables_created:
        try:
            create_tables()
        finally:
            _tables_created = True

    try:
        db = SessionLocal()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Database connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable. Check backend DATABASE_URL/POSTGRES_PRISMA_URL configuration."
        )

    try:
        _ensure_news_articles_schema(db)
        yield db
    finally:
        db.close()

def create_tables():
    if engine is None:
        return

    try:
        Base.metadata.create_all(bind=engine)

        # Lightweight schema patching for existing databases (no Alembic in this repo).
        # Ensure `region` exists even if the DB was created before this column was added.
        with engine.connect() as conn:
            try:
                if engine.dialect.name == "sqlite":
                    cols = conn.execute(text("PRAGMA table_info(news_articles)")).fetchall()
                    col_names = {c[1] for c in cols}  # (cid, name, type, notnull, dflt_value, pk)
                    if "region" not in col_names:
                        conn.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                        conn.commit()
                else:
                    conn.execute(text("ALTER TABLE news_articles ADD COLUMN IF NOT EXISTS region VARCHAR"))
                    conn.commit()
            except Exception:
                # Best-effort migration: ignore if it fails (e.g., already exists, permissions).
                pass
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not create tables: {e}")
        # Don't raise error, just log it

def get_db_diagnostic():
    """Lightweight DB diagnostic for health endpoints."""
    if settings.DB_CONFIG_WARNING:
        return {
            "status": "warning",
            "ready": False,
            "detail": settings.DB_CONFIG_WARNING,
            "driver": None,
        }

    if SessionLocal is None or engine is None:
        return {
            "status": "error",
            "ready": False,
            "detail": f"Database not initialized: {DB_INIT_ERROR or 'unknown error'}",
            "driver": None,
        }

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "ready": True,
            "detail": "Database connection successful",
            "driver": engine.dialect.name if engine.dialect else None,
        }
    except Exception as e:
        return {
            "status": "error",
            "ready": False,
            "detail": f"Database connectivity failed: {str(e)}",
            "driver": engine.dialect.name if engine and engine.dialect else None,
        }
