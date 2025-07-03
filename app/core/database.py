"""
Database initialization and management for EnergieFixers071.
"""
import logging
from pathlib import Path
from peewee import SqliteDatabase, DatabaseProxy

logger = logging.getLogger(__name__)

# Global database proxy - initialized once
db = DatabaseProxy()

def initialize_database():
    """Initialize the SQLite database with proper error handling"""
    try:
        # Import config after module initialization to avoid circular imports
        from config import Config
        
        # Ensure data directory exists
        Config.ensure_directories()
        
        # Create the actual database connection
        sqlite_db = SqliteDatabase(
            str(Config.DATABASE_PATH),
            pragmas={
                'journal_mode': 'wal',
                'cache_size': -1024 * 64,  # 64MB cache
                'foreign_keys': 1,
                'ignore_check_constraints': 0,
                'synchronous': 0
            }
        )
        
        # Initialize the proxy with the actual database
        db.initialize(sqlite_db)
        
        # Test the connection
        db.connect()
        logger.info("Database connection established successfully")
        
        # Import models only after database is initialized
        from core.models import create_tables
        
        # Create tables
        create_tables()
        
        logger.info(f"Database initialized successfully at {Config.DATABASE_PATH}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return False

def close_database():
    """Close database connection safely"""
    try:
        if hasattr(db, 'obj') and db.obj and not db.obj.is_closed():
            db.close()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")

def get_database():
    """Get the database instance"""
    return db
