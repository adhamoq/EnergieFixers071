"""
Configuration settings for EnergieFixers071 application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class with all required attributes"""
    
    # Application Information
    APP_NAME = "EnergieFixers071"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Window Configuration
    WINDOW_TITLE = f"{APP_NAME} - Volunteer Management"
    WINDOW_GEOMETRY = os.getenv('WINDOW_GEOMETRY', '1200x800')
    MIN_WINDOW_SIZE = (800, 600)
    
    # Directory Paths - CRITICAL: These were missing and causing the error
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"
    ASSETS_DIR = BASE_DIR / "assets"
    
    # Database Configuration
    DATABASE_PATH = DATA_DIR / "energiefixers.db"
    BACKUP_DIR = DATA_DIR / "backups"
    
    # Logging Configuration
    LOG_FILE = LOG_DIR / "energiefixers.log"
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # API Configuration (optional - can be empty)
    KOBO_BASE_URL = os.getenv('KOBO_BASE_URL', 'https://kf.kobotoolbox.org')
    KOBO_API_TOKEN = os.getenv('KOBO_API_TOKEN', '')
    KOBO_FORM_ID = os.getenv('KOBO_FORM_ID', '')
    
    CALENDLY_API_TOKEN = os.getenv('CALENDLY_API_TOKEN', '')
    CALENDLY_USER_URI = os.getenv('CALENDLY_USER_URI', '')
    
    # Link Generator Configuration
    DEFAULT_KOBO_FORM_URL = os.getenv(
        'DEFAULT_KOBO_FORM_URL', 
        'https://ee-eu.kobotoolbox.org/x/Evnz0R4w'
    )
    
    # UI Theme and Colors
    PRIMARY_COLOR = "#1D8420"  # EnergieFixers071 green
    SECONDARY_COLOR = "#F9C440"  # Yellow accent
    THEME_NAME = "flatly"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [cls.DATA_DIR, cls.LOG_DIR, cls.BACKUP_DIR, cls.ASSETS_DIR]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        return True

class Colors:
    """Complete color constants for the application"""
    # Primary brand colors
    PRIMARY_GREEN = Config.PRIMARY_COLOR
    SECONDARY_YELLOW = Config.SECONDARY_COLOR
    SECONDARY_GREEN = "#0F5132"  # Darker green variant
    
    # UI Background colors
    SIDEBAR_BG = "#F8F9FA"        # Light gray sidebar background
    SURFACE = "#FFFFFF"           # White surface
    BACKGROUND = "#F5F5F5"        # Light background
    
    # Text colors
    TEXT_PRIMARY = "#212529"      # Dark gray text
    TEXT_SECONDARY = "#6C757D"    # Medium gray text
    TEXT_LIGHT = "#ADB5BD"        # Light gray text
    
    # Status colors
    SUCCESS = "#28A745"           # Green success
    WARNING = "#FFC107"           # Yellow warning
    DANGER = "#DC3545"            # Red danger/error
    INFO = "#17A2B8"              # Blue info
    
    # Interactive elements
    BUTTON_PRIMARY = PRIMARY_GREEN
    BUTTON_SECONDARY = "#6C757D"
    BUTTON_SUCCESS = SUCCESS
    BUTTON_WARNING = WARNING
    BUTTON_DANGER = DANGER
    BUTTON_INFO = INFO
    
    # Border and accent colors
    BORDER = "#DEE2E6"            # Light border
    ACCENT = SECONDARY_YELLOW     # Yellow accent
    HIGHLIGHT = "#E9ECEF"         # Light highlight
    
    # Active/hover states
    ACTIVE = PRIMARY_GREEN
    HOVER = "#157347"             # Darker green for hover

