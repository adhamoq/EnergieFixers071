"""
Enhanced configuration settings for EnergieFixers071 application.
Complete fix for all missing attributes and classes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Enhanced application configuration with all required attributes"""
    
    # Application Information
    APP_NAME = "EnergieFixers071"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Window Configuration
    WINDOW_TITLE = f"{APP_NAME} - Volunteer Management"
    WINDOW_GEOMETRY = os.getenv('WINDOW_GEOMETRY', '1400x900')
    MIN_WINDOW_SIZE = (1000, 700)
    
    # UI Configuration - ADDED MISSING ATTRIBUTES
    SIDEBAR_WIDTH = 300
    CONTENT_PADDING = 20
    BUTTON_WIDTH = 150
    
    # Directory Paths
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
    
    # API Configuration
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
    
    # Theme Configuration
    PRIMARY_COLOR = "#1D8420"  # EnergieFixers071 green
    SECONDARY_COLOR = "#F9C440"  # Yellow accent
    DEFAULT_THEME = "flatly"
    AVAILABLE_THEMES = ["flatly", "darkly"]
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        try:
            directories = [cls.DATA_DIR, cls.LOG_DIR, cls.BACKUP_DIR, cls.ASSETS_DIR]
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Warning: Could not create directories: {e}")
            return False

class Colors:
    """Complete color palette with ALL required attributes"""
    
    # Primary Brand Colors
    PRIMARY = "#1D8420"           # EnergieFixers071 Green
    PRIMARY_GREEN = "#1D8420"     # Alias for compatibility
    PRIMARY_GREEN_LIGHT = "#28A745"  # Light green variant - ADDED MISSING
    PRIMARY_DARK = "#0F5132"      # Dark green variant
    
    SECONDARY = "#F9C440"         # EnergieFixers071 Yellow
    SECONDARY_YELLOW = "#F9C440"  # Alias for compatibility
    SECONDARY_GREEN = "#0F5132"   # Darker green variant
    ACCENT = "#F9C440"            # Accent color
    
    # Background Colors
    BACKGROUND = "#F8F9FA"        # Main background (less white)
    SURFACE = "#F2F2F2"           # Surface background
    SIDEBAR_BG = "#F8F9FA"        # Sidebar background
    CONTENT_BG = "#F2F2F2"        # Content area background
    
    # Text Colors - ADDED ALL MISSING VARIANTS
    TEXT_PRIMARY = "#212529"      # Primary text (dark)
    TEXT_SECONDARY = "#6C757D"    # Secondary text (medium)
    TEXT_MUTED = "#ADB5BD"        # Muted text (light) - ADDED MISSING
    TEXT_LIGHT = "#E9ECEF"        # Very light text
    TEXT_WHITE = "#FFFFFF"        # White text
    TEXT_DARK = "#212529"         # Dark text
    
    # Status Colors
    SUCCESS = "#28A745"           # Success green
    WARNING = "#FFC107"           # Warning yellow
    DANGER = "#DC3545"            # Danger red
    INFO = "#17A2B8"              # Info blue
    
    # Interactive Elements
    BUTTON_PRIMARY = PRIMARY_GREEN
    BUTTON_SECONDARY = "#6C757D"
    BUTTON_SUCCESS = SUCCESS
    BUTTON_WARNING = WARNING
    BUTTON_DANGER = DANGER
    BUTTON_INFO = INFO
    
    # Border and Outline Colors
    BORDER = "#DEE2E6"            # Standard border
    HIGHLIGHT = "#E9ECEF"         # Light highlight
    
    # State Colors
    ACTIVE = PRIMARY              # Active state
    HOVER = "#157347"             # Hover state
    
    @classmethod
    def get_all_colors(cls):
        """Get all color attributes as dictionary"""
        return {k: v for k, v in cls.__dict__.items() 
                if not k.startswith('_') and isinstance(v, str) and v.startswith('#')}

class Theme:
    """Theme configuration class - ADDED MISSING CLASS"""
    
    # Font Configuration
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_LARGE = 14
    FONT_SIZE_HEADER = 18
    FONT_SIZE_TITLE = 24
    
    # Spacing Configuration
    SPACING_SMALL = 5
    SPACING_MEDIUM = 10
    SPACING_LARGE = 20
    SPACING_XLARGE = 30
    
    # UI Configuration
    SIDEBAR_WIDTH = Config.SIDEBAR_WIDTH
    CONTENT_PADDING = Config.CONTENT_PADDING
    BUTTON_WIDTH = Config.BUTTON_WIDTH
    
    # Border Configuration
    BORDER_RADIUS = 4
    BORDER_WIDTH = 1

# Initialize directories on module import
Config.ensure_directories()