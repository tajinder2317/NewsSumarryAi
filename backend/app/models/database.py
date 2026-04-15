from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ..config import settings

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    author = Column(String)
    published_date = Column(DateTime)
    collected_date = Column(DateTime, default=datetime.utcnow)
    
    # Analysis fields
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    topics = Column(Text)  # JSON string of topics
    category = Column(String)
    
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

# Database setup
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
