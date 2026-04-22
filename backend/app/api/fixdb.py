"""
API endpoint to fix database connection and schema
"""
from fastapi import APIRouter
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/fixdb")
async def fix_database():
    """Force database connection and schema fix"""
    try:
        # Force PostgreSQL connection
        database_url = "postgres://83cd09c60c797f96246190cdd9cd172ba0dc3db40bff1e6d010d540a7734f840:sk_E0Jb06_KVQ-L1XJlGzXYr@db.prisma.io:5432/postgres?sslmode=require"
        
        # Create engine
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Create tables if they don't exist
            from ..models.database import Base
            Base.metadata.create_all(bind=engine)
            
            # Check if region column exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name = 'region'
            """))
            
            region_exists = result.fetchone() is not None
            
            if not region_exists:
                conn.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                conn.commit()
                logger.info("Successfully added 'region' column")
                
                return {"success": True, "message": "Database fixed - added region column"}
            else:
                return {"success": True, "message": "Database schema already correct"}
                
    except Exception as e:
        logger.error(f"Database fix failed: {e}")
        return {"error": str(e)}
