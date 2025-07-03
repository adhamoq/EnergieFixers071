"""
Configuration settings for EnergieFixers071 application.
Only flatly and darkly themes with proper contrast and consistency.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration with only flatly and darkly themes"""
    
    # Application Information
    APP_NAME = "EnergieFixers071"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Window Configuration
    WINDOW_TITLE = f"{APP_NAME} - Volunteer Management"
    WINDOW_GEOMETRY = os.getenv('WINDOW_GEOMETRY', '1400x900')
    MIN_WINDOW_SIZE = (1000, 700)
    
    # UI Configuration
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
    
    # Theme Configuration - ONLY flatly and darkly
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
    # ─── Brand constants (always available) ────────────────────────
    PRIMARY_GREEN     = "#1D8420"
    SECONDARY_YELLOW  = "#F9C440"

    # ─── Global fall-backs so class access never crashes ───────────
    PRIMARY           = "#2c3e50"
    SECONDARY         = "#95a5a6"
    SUCCESS           = "#18bc9c"
    INFO              = "#3498db"
    WARNING           = "#f39c12"
    DANGER            = "#e74c3c"
    TEXT_PRIMARY      = "#212529"
    TEXT_SECONDARY    = "#6c757d"
    TEXT_MUTED        = "#adb5bd"
    BORDER            = "#dee2e6"
    INPUT_BG          = "#ffffff"
    INPUT_FG          = "#495057"
    BACKGROUND        = "#f8f9fa"
    SIDEBAR_BG        = "#e9ecef"
    SURFACE           = "#f1f3f4"
    CONTENT_BG        = "#f8f9fa"

    # ─── Theme-specific overrides ──────────────────────────────────
    def __init__(self, theme_name: str = "flatly"):
        self.theme_name = theme_name

        if theme_name == "flatly":
            self.PRIMARY   = "#2c3e50"
            self.SECONDARY = "#95a5a6"
            self.SUCCESS   = "#19fccf"
            self.INFO      = "#3498db"
            self.WARNING   = "#f39c12"
            self.DANGER    = "#e74c3c"
            self.BACKGROUND = "#f8f9fa"
            self.SURFACE    = "#f1f3f4"
            self.SIDEBAR_BG = "#e9ecef"
            self.CONTENT_BG = "#f8f9fa"
            self.TEXT_PRIMARY   = "#212529"
            self.TEXT_SECONDARY = "#6c757d"
            self.TEXT_MUTED     = "#adb5bd"
            self.BORDER   = "#dee2e6"
            self.INPUT_BG = "#ffffff"
            self.INPUT_FG = "#495057"

        else:  # darkly
            self.PRIMARY   = "#375a7f"
            self.SECONDARY = "#444444"
            self.SUCCESS   = "#00bc8c"
            self.INFO      = "#3498db"
            self.WARNING   = "#f39c12"
            self.DANGER    = "#e74c3c"
            self.BACKGROUND = "#222222"
            self.SURFACE    = "#303030"
            self.SIDEBAR_BG = "#2b2b2b"
            self.CONTENT_BG = "#222222"
            self.TEXT_PRIMARY   = "#ffffff"
            self.TEXT_SECONDARY = "#adb5bd"
            self.TEXT_MUTED     = "#6c757d"
            self.BORDER   = "#444444"
            self.INPUT_BG = "#495057"
            self.INPUT_FG = "#ffffff"

        # Common dynamic colours
        self.ACTIVE = self.PRIMARY
        self.HOVER  = self._tint(self.PRIMARY, 0.1)

    def _tint(self, hex_color: str, amt: float) -> str:
        """Lighten for dark theme or darken for light."""
        hex_color = hex_color.lstrip('#')
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        if self.theme_name == "darkly":
            r, g, b = (min(255, int(c + (255 - c) * amt)) for c in (r, g, b))
        else:
            r, g, b = (max(0, int(c * (1 - amt))) for c in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"


class Theme:
    """Consistent theme configuration for both flatly and darkly"""
    
    # Font Configuration - IDENTICAL for both themes
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_LARGE = 14
    FONT_SIZE_HEADER = 18
    FONT_SIZE_TITLE = 24
    
    # Spacing Configuration - IDENTICAL for both themes
    SPACING_SMALL = 5
    SPACING_MEDIUM = 10
    SPACING_LARGE = 20
    SPACING_XLARGE = 30
    
    # Layout Configuration - IDENTICAL for both themes
    SIDEBAR_WIDTH = Config.SIDEBAR_WIDTH
    CONTENT_PADDING = Config.CONTENT_PADDING
    BUTTON_WIDTH = Config.BUTTON_WIDTH
    
    # Border Configuration - IDENTICAL for both themes
    BORDER_RADIUS = 4
    BORDER_WIDTH = 1

# Initialize directories
Config.ensure_directories()
