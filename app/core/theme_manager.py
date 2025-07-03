"""
Theme manager for EnergieFixers071 application.
Handles registration and switching between enhanced themes.
"""
import ttkbootstrap as ttk
from ttkbootstrap.style import ThemeDefinition
import logging
from config import ENHANCED_THEMES, Colors

logger = logging.getLogger(__name__)

class ThemeManager:
    """Manages custom themes for the application"""
    
    def __init__(self):
        self.style = None
        self.current_theme = "flatly_enhanced"
        self.colors = Colors(self.current_theme)
        
    def initialize_themes(self):
        """Register custom themes with ttkbootstrap"""
        try:
            # Create style instance
            self.style = ttk.Style()
            
            # Register enhanced themes
            for theme_name, theme_data in ENHANCED_THEMES.items():
                theme_def = ThemeDefinition(
                    name=theme_name,
                    themetype=theme_data["type"],
                    colors=theme_data["colors"]
                )
                
                # Register the theme
                self.style.register_theme(theme_def)
                logger.info(f"Registered theme: {theme_name}")
            
            # Apply default theme
            self.apply_theme(self.current_theme)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize themes: {e}")
            return False
    
    def apply_theme(self, theme_name):
        """Apply a specific theme"""
        try:
            if theme_name in ENHANCED_THEMES:
                self.style.theme_use(theme_name)
                self.current_theme = theme_name
                self.colors = Colors(theme_name)
                
                # Apply additional customizations
                self._apply_custom_styles()
                
                logger.info(f"Applied theme: {theme_name}")
                return True
            else:
                logger.error(f"Unknown theme: {theme_name}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply theme {theme_name}: {e}")
            return False
    
    def _apply_custom_styles(self):
        """Apply additional custom styles for enhanced appearance"""
        try:
            # Enhanced sidebar styling
            self.style.configure(
                "Sidebar.TFrame",
                background=self.colors.SIDEBAR_BG,
                relief="flat"
            )
            
            # Enhanced button styling
            self.style.configure(
                "Sidebar.TButton",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_PRIMARY,
                borderwidth=0,
                focuscolor="none",
                font=("Segoe UI", 11),
                padding=(15, 10)
            )
            
            # Active button state
            self.style.map(
                "Sidebar.TButton",
                background=[
                    ("active", self.colors.PRIMARY),
                    ("pressed", self.colors.HOVER)
                ],
                foreground=[
                    ("active", "white"),
                    ("pressed", "white")
                ]
            )
            
            # Content area styling
            self.style.configure(
                "Content.TFrame",
                background=self.colors.BACKGROUND
            )
            
        except Exception as e:
            logger.error(f"Failed to apply custom styles: {e}")
    
    def get_available_themes(self):
        """Get list of available theme names"""
        return list(ENHANCED_THEMES.keys())
    
    def get_theme_display_names(self):
        """Get user-friendly theme names"""
        return {
            "flatly_enhanced": "Light Mode (Enhanced)",
            "darkly_enhanced": "Dark Mode (Enhanced)"
        }
    
    def is_dark_theme(self):
        """Check if current theme is dark"""
        return ENHANCED_THEMES[self.current_theme]["type"] == "dark"
