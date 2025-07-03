"""
Enhanced configuration with custom flatly and darkly themes.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Enhanced application configuration"""
    
    # Application Information
    APP_NAME = "EnergieFixers071"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Window Configuration
    WINDOW_TITLE = f"{APP_NAME} - Volunteer Management"
    WINDOW_GEOMETRY = os.getenv('WINDOW_GEOMETRY', '1400x900')
    MIN_WINDOW_SIZE = (1000, 700)
    
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
    DEFAULT_THEME = "flatly_enhanced"
    AVAILABLE_THEMES = ["flatly_enhanced", "darkly_enhanced"]
    
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

# Enhanced Theme Definitions
ENHANCED_THEMES = {
    "flatly_enhanced": {
        "type": "light",
        "colors": {
            "primary": "#2c3e50",
            "secondary": "#95a5a6",
            "success": "#18bc9c",
            "info": "#3498db",
            "warning": "#f39c12",
            "danger": "#e74c3c",
            "light": "#e9ecef",
            "dark": "#6c757d",
            "bg": "#f8f9fa",
            "fg": "#212529",
            "selectbg": "#dee2e6",
            "selectfg": "#212529",
            "border": "#ced4da",
            "inputfg": "#495057",
            "inputbg": "#ffffff",
            "active": "#1abc9c"
        }
    },
    "darkly_enhanced": {
        "type": "dark",
        "colors": {
            "primary": "#2c3e50",
            "secondary": "#6c757d",
            "success": "#18bc9c",
            "info": "#3498db",
            "warning": "#f39c12",
            "danger": "#e74c3c",
            "light": "#6c757d",
            "dark": "#343a40",
            "bg": "#212529",
            "fg": "#ffffff",
            "selectbg": "#495057",
            "selectfg": "#ffffff",
            "border": "#495057",
            "inputfg": "#ffffff",
            "inputbg": "#343a40",
            "active": "#1abc9c"
        }
    }
}


class Colors:
    """Enhanced color palette with theme-aware properties"""
    
    def __init__(self, theme_name="flatly_enhanced"):
        self.theme_name = theme_name
        self.theme_colors = ENHANCED_THEMES.get(theme_name, ENHANCED_THEMES["flatly_enhanced"])["colors"]
        
        # Set all colors based on current theme
        self.PRIMARY = self.theme_colors["primary"]
        self.SECONDARY = self.theme_colors["secondary"]
        self.SUCCESS = self.theme_colors["success"]
        self.INFO = self.theme_colors["info"]
        self.WARNING = self.theme_colors["warning"]
        self.DANGER = self.theme_colors["danger"]
        
        # Background colors
        self.BACKGROUND = self.theme_colors["bg"]
        self.SURFACE = self.theme_colors["bg"]
        self.SIDEBAR_BG = self.theme_colors["light"]
        
        # Text colors
        self.TEXT_PRIMARY = self.theme_colors["fg"]
        self.TEXT_SECONDARY = self.theme_colors["secondary"]
        self.TEXT_MUTED = self.theme_colors["secondary"]
        
        # Interface colors
        self.BORDER = self.theme_colors["border"]
        self.INPUT_BG = self.theme_colors["inputbg"]
        self.INPUT_FG = self.theme_colors["inputfg"]
        
        # Additional UI colors
        self.ACTIVE = self.PRIMARY
        self.HOVER = self._darken_color(self.PRIMARY, 0.1)
    
    def _darken_color(self, hex_color, factor):
        """Darken a hex color by a factor"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(c * (1 - factor))) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

# Initialize directories
Config.ensure_directories()
