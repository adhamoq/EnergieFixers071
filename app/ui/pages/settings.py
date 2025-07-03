import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import os
from dotenv import load_dotenv, set_key
from config import Colors

class SettingsPage(ttk.Frame):
    """Settings page for EnergieFixers071"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.env_path = os.path.abspath('.env')
        load_dotenv(self.env_path)
        self.setup_ui()

    def setup_ui(self):
        # Title
        ttk.Label(
            self, text="Settings",
            font=("Helvetica", 18, "bold"),
            foreground=Colors.PRIMARY_GREEN
        ).pack(anchor="w", pady=(10, 20), padx=10)

        # API Tokens Section
        api_frame = ttk.LabelFrame(self, text="API Tokens", padding=15)
        api_frame.pack(fill=X, padx=20, pady=10)

        # KoboToolbox Token
        ttk.Label(api_frame, text="KoboToolbox API Token:", width=25).grid(row=0, column=0, sticky="w", pady=5)
        self.kobo_token_var = tk.StringVar(value=os.getenv("KOBO_API_TOKEN", ""))
        ttk.Entry(api_frame, textvariable=self.kobo_token_var, width=50, show="*").grid(row=0, column=1, sticky="ew", pady=5)

        # Calendly Token
        ttk.Label(api_frame, text="Calendly API Token:", width=25).grid(row=1, column=0, sticky="w", pady=5)
        self.calendly_token_var = tk.StringVar(value=os.getenv("CALENDLY_API_TOKEN", ""))
        ttk.Entry(api_frame, textvariable=self.calendly_token_var, width=50, show="*").grid(row=1, column=1, sticky="ew", pady=5)

        # Save API tokens button
        ttk.Button(api_frame, text="Save Tokens", command=self.save_tokens, bootstyle=SUCCESS).grid(row=2, column=0, columnspan=2, pady=10)

        # Theme Section
        theme_frame = ttk.LabelFrame(self, text="Theme", padding=15)
        theme_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(theme_frame, text="Select Theme:", width=25).grid(row=0, column=0, sticky="w", pady=5)
        self.theme_var = tk.StringVar(value=self.app.root.style.theme_use())
        themes = ["flatly", "superhero", "minty", "journal", "darkly", "cosmo", "pulse"]
        theme_menu = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=themes, width=20, state="readonly")
        theme_menu.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Button(theme_frame, text="Apply Theme", command=self.apply_theme, bootstyle=INFO).grid(row=1, column=0, columnspan=2, pady=10)

        # App Info Section
        info_frame = ttk.LabelFrame(self, text="Application Info", padding=15)
        info_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(info_frame, text="App Name: EnergieFixers071").pack(anchor="w")
        ttk.Label(info_frame, text="Version: 1.0.0").pack(anchor="w")
        ttk.Label(info_frame, text="Author: EnergieFixers071 Team").pack(anchor="w")
        ttk.Label(info_frame, text="For support, contact: info@energiefixers071.nl").pack(anchor="w")

    def save_tokens(self):
        """Save API tokens to .env file (overwrites existing keys)"""
        try:
            set_key(self.env_path, "KOBO_API_TOKEN", self.kobo_token_var.get())
            set_key(self.env_path, "CALENDLY_API_TOKEN", self.calendly_token_var.get())
            messagebox.showinfo("Settings", "API tokens saved!\nRestart the app to apply changes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tokens: {e}")

    def apply_theme(self):
        """Apply selected theme"""
        theme = self.theme_var.get()
        try:
            self.app.root.style.theme_use(theme)
            messagebox.showinfo("Theme Changed", f"Theme set to '{theme}'.")
        except Exception as e:
            messagebox.showerror("Theme Error", f"Could not apply theme: {e}")

    def refresh_data(self):
        """Reload settings if needed (optional for future use)"""
        pass
