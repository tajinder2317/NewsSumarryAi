from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class NewsArticleBase(BaseModel):
    title: str
    content: str
    url: HttpUrl
    source: str
    author: Optional[str] = None
    published_date: Optional[datetime] = None

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticleResponse(NewsArticleBase):
    id: int
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    topics: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    collected_date: datetime
    
    class Config:
        from_attributes = True

class NewsArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    topics: Optional[str] = None
    category: Optional[str] = None

class AnalysisRequest(BaseModel):
    article_ids: List[int]
    analysis_types: List[str]  # ["sentiment", "topics", "trends"]

class AnalysisResponse(BaseModel):
    analysis_type: str
    results: dict
    created_date: datetime

class TrendAnalysis(BaseModel):
    topic: str
    frequency: int
    sentiment_distribution: dict
    trend_direction: str  # "up", "down", "stable"

class SearchRequest(BaseModel):
    query: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    sentiment: Optional[str] = None
    limit: int = 20
    offset: int = 0

class SentimentAnalysis(BaseModel):
    positive: float
    negative: float
    neutral: float
    label: str

class TopicAnalysis(BaseModel):
    topics: List[dict]
    dominant_topic: str
