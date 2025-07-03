"""
Configuration settings for EnergieFixers071 desktop application.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Application info
    APP_NAME = "EnergieFixers071"
    APP_VERSION = "1.0.0"
    
    # Window settings
    WINDOW_TITLE = f"{APP_NAME} - Volunteer Management"
    WINDOW_GEOMETRY = "1200x800"
    MIN_WINDOW_SIZE = (800, 600)
    
    # Paths
    APP_DIR = Path(__file__).parent
    ROOT_DIR = APP_DIR.parent
    DATA_DIR = ROOT_DIR / "data"
    LOG_DIR = ROOT_DIR / "logs"
    
    # Ensure directories exist
    DATA_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    
    # Database settings
    DATABASE_PATH = DATA_DIR / "energiefixers.db"
    
    # API settings (optional - app works without them)
    KOBO_BASE_URL = os.getenv("KOBO_BASE_URL", "https://kf.kobotoolbox.org")
    KOBO_API_TOKEN = os.getenv("KOBO_API_TOKEN", "")
    KOBO_FORM_ID = os.getenv("KOBO_FORM_ID", "")
    
    CALENDLY_API_TOKEN = os.getenv("CALENDLY_API_TOKEN", "")
    CALENDLY_USER_URI = os.getenv("CALENDLY_USER_URI", "")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOG_DIR / "energiefixers.log"
    
    # Debug mode
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

class Colors:
    """Color scheme for EnergieFixers071 branding"""
    
    # Primary colors (EnergieFixers071 green)
    PRIMARY_GREEN = "#1D8420"
    SECONDARY_GREEN = "#15691A"
    
    # Accent colors (yellow)
    ACCENT_YELLOW = "#F9C440"
    LIGHT_YELLOW = "#FDE68A"
    
    # UI colors
    SURFACE = "#F8F9FA"
    BACKGROUND = "#FFFFFF"
    
    # Text colors
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    TEXT_MUTED = "#ADB5BD"
    
    # Status colors
    SUCCESS = "#28A745"
    INFO = "#17A2B8"
    WARNING = "#FFC107"
    DANGER = "#DC3545"

class Theme:
    """Theme configuration"""
    
    # ttkbootstrap theme
    THEME_NAME = "flatly"
    
    # Custom styles
    SIDEBAR_STYLE = {
        "background": Colors.SURFACE,
        "relief": "flat"
    }
    
    BUTTON_STYLE = {
        "background": Colors.PRIMARY_GREEN,
        "foreground": "white",
        "borderwidth": 0,
        "focuscolor": "none"
    }