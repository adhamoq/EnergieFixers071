"""
Simple theme manager for switching between flatly and darkly themes.
"""
import ttkbootstrap as ttk
import logging
from config import Config, Colors

logger = logging.getLogger(__name__)

class SimpleThemeManager:
    """Simple theme manager for flatly and darkly themes"""
    
    def __init__(self, root_window):
        self.root = root_window
        self.current_theme = Config.DEFAULT_THEME
        self.available_themes = {
            "flatly": "Light Mode",
            "darkly": "Dark Mode"
        }
    
    def get_available_themes(self):
        """Get available theme names"""
        return self.available_themes
    
    def apply_theme(self, theme_name):
        """Apply a theme"""
        try:
            if theme_name in self.available_themes:
                self.root.style.theme_use(theme_name)
                self.current_theme = theme_name
                logger.info(f"Applied theme: {theme_name}")
                return True
            else:
                logger.error(f"Unknown theme: {theme_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_name}: {e}")
            return False
    
    def get_current_theme(self):
        """Get current theme name"""
        return self.current_theme
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "flatly":
            return self.apply_theme("darkly")
        else:
            return self.apply_theme("flatly")