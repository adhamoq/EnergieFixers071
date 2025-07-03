"""
Link Generator page - integrates your existing AutoEnergie.py functionality
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class LinksPage(ttk.Frame):
    """Link Generator page - preserving original AutoEnergie functionality"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Initialize variables exactly like original
        self.link_var = tk.StringVar()
        
        # Fields to be filled (exactly like original)
        self.fields = {
            "adres": "",
            "afspraakTijd": "",
            "uitvoerders": ""
        }
        self.value_entry = {}
        
        # Setup UI exactly like original
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI exactly like the original AutoEnergie.py"""
        # Make the frame fill and be responsive like original
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        main_frame.columnconfigure(0, weight=1)
        
        # Load and display the logo (exactly like original)
        self.create_logo_section(main_frame)
        
        # Base URL Input (exactly like original)
        self.create_base_url_section(main_frame)
        
        # Create input fields dynamically (exactly like original)
        self.create_fields_section(main_frame)
        
        # Generate Link Button (exactly like original)
        self.create_generate_button(main_frame)
        
        # Link Display (exactly like original)
        self.create_link_display(main_frame)
        
        # Copy Button (exactly like original)
        self.create_copy_button(main_frame)
    
    def create_logo_section(self, parent):
        """Load and display the logo exactly like original"""
        logo_path = "Logo-Energiefixers071.png"  # Same path as original
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((350, 175), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_label = ttk.Label(parent, image=self.logo_photo)
            logo_label.pack(pady=20)  # Same padding as original
        except Exception as e:
            logger.warning(f"Unable to load logo: {e}")
            # Fallback text if logo not found
            title_label = ttk.Label(
                parent,
                text="AutoEnergie",
                font=("Helvetica", 20, "bold")
            )
            title_label.pack(pady=20)
    
    def create_base_url_section(self, parent):
        """Create base URL section exactly like original"""
        base_url_frame = ttk.Frame(parent, padding=10)
        base_url_frame.pack(pady=5, fill=tk.X, padx=20)
        ttk.Label(
            base_url_frame, 
            text="Enter KoboToolbox Form URL:", 
            font=("Helvetica", 12)
        ).pack(side=tk.LEFT, padx=5)

        # Default value set in the Entry field (exactly like original)
        self.base_url_entry = ttk.Entry(base_url_frame, width=50, font=("Helvetica", 12))
        self.base_url_entry.insert(0, "https://ee-eu.kobotoolbox.org/x/Evnz0R4w")  # Your default link
        self.base_url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def create_fields_section(self, parent):
        """Create input fields dynamically exactly like original"""
        fields_frame = ttk.Frame(parent, padding=10)
        fields_frame.pack(pady=10, fill=tk.X, padx=20)
        ttk.Label(
            fields_frame, 
            text="Enter field values:", 
            font=("Helvetica", 14, "bold")
        ).pack(pady=5)
        
        # Create fields exactly like original
        for key in self.fields:
            frame = ttk.Frame(fields_frame, padding=5)
            frame.pack(pady=5, fill=tk.X)
            ttk.Label(
                frame, 
                text=f"{key}:", 
                font=("Helvetica", 12), 
                width=20
            ).pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=50, font=("Helvetica", 12))
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
            self.value_entry[key] = entry
    
    def create_generate_button(self, parent):
        """Create Generate Link Button exactly like original"""
        generate_button = ttk.Button(
            parent, 
            text="Generate Link", 
            command=self.generate_link, 
            bootstyle=SUCCESS
        )
        generate_button.pack(pady=10, fill=tk.X, padx=50)
    
    def create_link_display(self, parent):
        """Create Link Display exactly like original"""
        self.link_entry = ttk.Entry(
            parent, 
            textvariable=self.link_var, 
            width=80, 
            font=("Helvetica", 12), 
            state="readonly"
        )
        self.link_entry.pack(pady=5, fill=tk.X, padx=50)
    
    def create_copy_button(self, parent):
        """Create Copy Button exactly like original"""
        copy_button = ttk.Button(
            parent, 
            text="Copy Link", 
            command=self.copy_to_clipboard, 
            bootstyle=INFO
        )
        copy_button.pack(pady=10, fill=tk.X, padx=50)
    
    def generate_link(self):
        """Generate the KoboToolbox link - EXACTLY like your original function"""
        base_url = self.base_url_entry.get().strip()
        if not base_url:
            messagebox.showwarning("Warning", "Please enter a valid BASE_URL")
            return

        # Define the group and fields inside the group (exactly like original)
        group = "introductie"
        
        # Build the query parameters with the group prefix (exactly like original)
        params = "&".join([
            f"d[{group}/{key}]={self.value_entry[key].get().strip()}" 
            for key in self.fields 
            if self.value_entry[key].get().strip()
        ])
        final_link = f"{base_url}?{params}" if params else base_url
        self.link_var.set(final_link)

    def copy_to_clipboard(self):
        """Copy the generated link to the clipboard - EXACTLY like your original function"""
        self.clipboard_clear()
        self.clipboard_append(self.link_var.get())
        self.update()
    
    def refresh_data(self):
        """Required method for page framework - no action needed"""
        pass