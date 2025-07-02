"""
Database configuration and connection setup using Peewee ORM.
"""
import sqlite3
from pathlib import Path
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database connection
database_path = Config.DATABASE_PATH
db = SqliteExtDatabase(database_path, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64,  # 64MB cache
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})

class BaseModel(Model):
    """Base model class that all models should inherit from"""

    class Meta:
        database = db

def initialize_database():
    """Initialize the database and create tables"""
    try:
        # Ensure database directory exists
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        db.connect()

        # Import all models here to ensure they're registered
        from core.models import Volunteer, Visit, Appointment, Setting

        # Create tables if they don't exist
        db.create_tables([Volunteer, Visit, Appointment, Setting], safe=True)

        logger.info(f"Database initialized at: {database_path}")

        # Create default settings if they don't exist
        create_default_settings()

        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def create_default_settings():
    """Create default application settings"""
    from core.models import Setting

    default_settings = [
        ('theme', 'flatly'),
        ('auto_sync', 'true'),
        ('sync_interval', '300'),  # 5 minutes
        ('backup_enabled', 'true'),
        ('last_sync', ''),
        ('app_version', Config.APP_VERSION)
    ]

    for key, value in default_settings:
        Setting.get_or_create(key=key, defaults={'value': value})

def close_database():
    """Close database connection"""
    if not db.is_closed():
        db.close()
        logger.info("Database connection closed")

def backup_database(backup_path=None):
    """Create a backup of the database"""
    if backup_path is None:
        backup_dir = Path(database_path).parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"energiefixers_backup_{timestamp}.db"

    try:
        # Simple file copy for SQLite
        import shutil
        shutil.copy2(database_path, backup_path)
        logger.info(f"Database backed up to: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Database backup failed: {e}")
        return None

# Database context manager
class DatabaseManager:
    """Context manager for database connections"""

    def __enter__(self):
        if db.is_closed():
            db.connect()
        return db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not db.is_closed():
            db.close()
