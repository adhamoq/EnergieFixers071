import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import logging
from config import Colors

logger = logging.getLogger(__name__)

class AppointmentsPage(ttk.Frame):
    """Simple appointments page for testing"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        """Setup basic appointments page UI"""
        # Header
        header_label = ttk.Label(
            self,
            text="Appointments Management",
            font=("Segoe UI", 20, "bold"),
            foreground=Colors.PRIMARY_GREEN
        )
        header_label.pack(pady=20)
        
        # Placeholder content
        content_frame = ttk.LabelFrame(self, text="Appointments", padding=20)
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(
            content_frame,
            text="Appointment management and Calendly integration will be available here.",
            font=("Segoe UI", 12),
            foreground=Colors.TEXT_SECONDARY
        ).pack(pady=20)
        
        # Add test button
        ttk.Button(
            content_frame,
            text="📅 Sync Appointments (Demo)",
            command=self.demo_sync_appointments,
            bootstyle=INFO,
            padding=(15, 10)
        ).pack(pady=10)
    
    def demo_sync_appointments(self):
        """Demo sync appointments functionality"""
        messagebox.showinfo(
            "Demo", 
            "This will sync appointments from Calendly.\n\nFull functionality coming soon!"
        )
    
    def refresh_data(self):
        """Refresh page data"""
        pass

