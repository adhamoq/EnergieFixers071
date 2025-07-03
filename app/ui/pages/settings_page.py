"""
Settings page for EnergieFixers071 with theme switching and fixed color access.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv, set_key
from config import Config, Colors, Theme

class SettingsPage(ttk.Frame):
    """Settings page with theme switching and API configuration"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.env_path = os.path.abspath('.env')
        load_dotenv(self.env_path)
        self.setup_ui()

    def setup_ui(self):
        """Setup the settings page UI"""
        
        # Title - FIXED: Now uses guaranteed Colors.PRIMARY_GREEN
        ttk.Label(
            self, 
            text="Settings",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADER, "bold"),
            foreground=Colors.PRIMARY_GREEN  # This is now guaranteed to exist
        ).pack(anchor="w", pady=(10, 20), padx=15)

        # Theme Section - MOVED from sidebar to here
        self.create_theme_section()
        
        # API Tokens Section
        self.create_api_section()
        
        # Application Info Section
        self.create_info_section()

    def create_theme_section(self):
        """Create theme selection section - ONLY flatly and darkly"""
        theme_frame = ttk.LabelFrame(self, text="Appearance", padding=15)
        theme_frame.pack(fill=X, padx=20, pady=10)
        theme_frame.columnconfigure(1, weight=1)

        # Current theme detection
        try:
            current_theme = self.app.current_theme if hasattr(self.app, 'current_theme') else Config.DEFAULT_THEME
        except:
            current_theme = Config.DEFAULT_THEME

        # Theme description
        ttk.Label(
            theme_frame, 
            text="Choose your preferred theme:",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Theme selection - ONLY flatly and darkly
        self.theme_var = tk.StringVar(value=current_theme)
        
        # Light theme option
        light_frame = ttk.Frame(theme_frame)
        light_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Radiobutton(
            light_frame,
            text="☀️ Light Mode (Flatly)",
            variable=self.theme_var,
            value="flatly",
            command=self.on_theme_change
        ).pack(side=LEFT)
        
        ttk.Label(
            light_frame,
            text="Clean light interface with improved contrast",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=Colors.TEXT_SECONDARY
        ).pack(side=LEFT, padx=(10, 0))

        # Dark theme option  
        dark_frame = ttk.Frame(theme_frame)
        dark_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        
        ttk.Radiobutton(
            dark_frame,
            text="🌙 Dark Mode (Darkly)",
            variable=self.theme_var,
            value="darkly", 
            command=self.on_theme_change
        ).pack(side=LEFT)
        
        ttk.Label(
            dark_frame,
            text="Easy on the eyes dark interface",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=Colors.TEXT_SECONDARY
        ).pack(side=LEFT, padx=(10, 0))

    def create_api_section(self):
        """Create API tokens configuration section"""
        api_frame = ttk.LabelFrame(self, text="API Configuration", padding=15)
        api_frame.pack(fill=X, padx=20, pady=10)
        api_frame.columnconfigure(1, weight=1)

        # KoboToolbox Token
        ttk.Label(
            api_frame, 
            text="KoboToolbox API Token:", 
            width=25
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.kobo_token_var = tk.StringVar(value=os.getenv("KOBO_API_TOKEN", ""))
        ttk.Entry(
            api_frame, 
            textvariable=self.kobo_token_var, 
            width=50, 
            show="*"
        ).grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Calendly Token
        ttk.Label(
            api_frame, 
            text="Calendly API Token:", 
            width=25
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.calendly_token_var = tk.StringVar(value=os.getenv("CALENDLY_API_TOKEN", ""))
        ttk.Entry(
            api_frame, 
            textvariable=self.calendly_token_var, 
            width=50, 
            show="*"
        ).grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Save button
        ttk.Button(
            api_frame, 
            text="💾 Save API Tokens", 
            command=self.save_tokens, 
            bootstyle=SUCCESS
        ).grid(row=2, column=0, columnspan=2, pady=15)

    def create_info_section(self):
        """Create application information section"""
        info_frame = ttk.LabelFrame(self, text="Application Information", padding=15)
        info_frame.pack(fill=X, padx=20, pady=10)

        # App details
        info_items = [
            ("Application:", Config.APP_NAME),
            ("Version:", Config.APP_VERSION), 
            ("Author:", "EnergieFixers071 Team"),
            ("Support:", "info@energiefixers071.nl")
        ]

        for i, (label, value) in enumerate(info_items):
            ttk.Label(
                info_frame, 
                text=f"{label} {value}",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)
            ).pack(anchor="w", pady=2)

    def on_theme_change(self):
        """Handle theme change"""
        new_theme = self.theme_var.get()
        
        if hasattr(self.app, 'change_theme'):
            try:
                # Use the app's theme change method if available
                self.app.change_theme(new_theme)
               
            except Exception as e:
                messagebox.showerror("Theme Error", f"Failed to change theme: {e}")
                # Reset to previous theme
                current_theme = getattr(self.app, 'current_theme', Config.DEFAULT_THEME)
                self.theme_var.set(current_theme)
        else:
            # Fallback: direct theme application
            try:
                self.app.root.style.theme_use(new_theme)
                
            except Exception as e:
                messagebox.showerror("Theme Error", f"Could not apply theme: {e}")

    def save_tokens(self):
        """Save API tokens to .env file"""
        try:
            set_key(self.env_path, "KOBO_API_TOKEN", self.kobo_token_var.get())
            set_key(self.env_path, "CALENDLY_API_TOKEN", self.calendly_token_var.get())
            messagebox.showinfo(
                "Settings Saved", 
                "API tokens saved successfully!\n\nRestart the application to apply changes."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tokens: {e}")

    def refresh_data(self):
        """Refresh settings data"""
        try:
            # Update theme selection to match current theme
            if hasattr(self.app, 'current_theme'):
                self.theme_var.set(self.app.current_theme)
        except Exception:
            pass
