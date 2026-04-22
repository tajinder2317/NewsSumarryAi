"""
API endpoint for database migration
"""
from fastapi import APIRouter
from sqlalchemy import text
from ..models import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/migrate")
async def migrate_database():
    """Run database migration to add missing columns"""
    try:
        # Get database connection
        db_gen = get_db()
        db = next(db_gen)
        
        if db is None:
            return {"error": "Database connection failed"}
        
        try:
            # Check if region column exists (PostgreSQL syntax)
            result = db.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name = 'region'
            """))
            
            region_exists = result.fetchone() is not None
            
            if not region_exists:
                # Add region column
                db.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                db.commit()
                logger.info("Successfully added 'region' column")
                
                return {"success": True, "message": "Added 'region' column successfully"}
            else:
                return {"success": True, "message": "'region' column already exists"}
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return {"error": str(e)}
