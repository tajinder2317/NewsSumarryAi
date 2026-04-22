#!/usr/bin/env python3
"""
Database migration script to add missing columns to PostgreSQL database
"""
import os
import sys
from sqlalchemy import create_engine, text

def migrate_database():
    """Add missing columns to the database"""
    try:
        # Use the PostgreSQL connection string directly
        database_url = "postgres://83cd09c60c797f96246190cdd9cd172ba0dc3db40bff1e6d010d540a7734f840:sk_E0Jb06_KVQ-L1XJlGzXYr@db.prisma.io:5432/postgres?sslmode=require"
        
        # Create engine with PostgreSQL settings
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if region column exists (PostgreSQL syntax)
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news_articles' 
                AND column_name = 'region'
            """))
            
            region_exists = result.fetchone() is not None
            
            if not region_exists:
                print("Adding 'region' column to news_articles table...")
                conn.execute(text("ALTER TABLE news_articles ADD COLUMN region VARCHAR"))
                conn.commit()
                print("Successfully added 'region' column")
            else:
                print("'region' column already exists")
            
            # Verify table structure
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'news_articles'
                ORDER BY ordinal_position
            """))
            
            columns = [row[0] for row in result.fetchall()]
            print(f"Current columns in news_articles: {columns}")
            
            return True
            
    except Exception as e:
        print(f"Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
