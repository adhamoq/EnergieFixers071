# Improved root.py with better UI design and wider sidebar

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from config import Config, Colors
from ui.pages.home_page import HomePage
from ui.pages.volunteer_page import VolunteerPage
from ui.pages.appointments_page import AppointmentsPage
from ui.pages.visits_page import VisitsPage
from ui.pages.links_page import LinksPage
from ui.pages.settings_page import SettingsPage
import logging

logger = logging.getLogger(__name__)

class MainApplication:
    """Main application window with improved navigation and styling"""
    
    def __init__(self):
        # Create main window with modern theme
        self.root = ttk.Window(
            title=Config.WINDOW_TITLE,
            themename="flatly",  # Using flatly theme for better contrast
            size=tuple(map(int, Config.WINDOW_GEOMETRY.split('x'))),
            minsize=Config.MIN_WINDOW_SIZE
        )
        
        # Configure window
        self.root.iconify()  # Start minimized to avoid flashing
        
        # Initialize variables
        self.current_page = None
        self.pages = {}
        
        # Setup UI
        self.setup_ui()
        self.setup_styles()
        
        # Show home page by default
        self.show_page("home")
        
        # Center window and show
        self.center_window()
        self.root.deiconify()
        
        logger.info("Main application window initialized")
    
    def setup_ui(self):
        """Setup the main UI layout with improved design"""
        # Configure main grid - sidebar takes more space now
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create wider sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_content_area()
    
    def create_sidebar(self):
        """Create improved navigation sidebar - wider and more attractive"""
        # Sidebar frame - much wider now (300px instead of 200px)
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=300)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.sidebar.grid_propagate(False)
        
        # Logo/Header section with better spacing
        header_frame = ttk.Frame(self.sidebar, style="SidebarHeader.TFrame")
        header_frame.pack(fill=X, padx=20, pady=30)
        
        # Application title with larger font and better color
        title_label = ttk.Label(
            header_frame,
            text="EnergieFixers071",
            font=("Helvetica", 18, "bold"),
            foreground=Colors.PRIMARY_GREEN,
            background=Colors.SIDEBAR_BG,
            style="SidebarTitle.TLabel"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Volunteer Management System",
            font=("Helvetica", 11),
            foreground=Colors.TEXT_SECONDARY,
            background=Colors.SIDEBAR_BG,
            style="SidebarSubtitle.TLabel"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Divider line
        divider = ttk.Frame(header_frame, height=2, style="SidebarDivider.TFrame")
        divider.pack(fill=X, pady=20)
        
        # Navigation buttons with better spacing and icons
        nav_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        nav_frame.pack(fill=BOTH, expand=True, padx=20)
        
        # Navigation items with better icons and descriptions
        self.nav_items = [
            ("home", "🏠", "Dashboard", "Overview and statistics", HomePage),
            ("volunteers", "👥", "Volunteers", "Manage volunteer profiles", VolunteerPage),
            ("appointments", "📅", "Appointments", "Scheduled appointments", AppointmentsPage),
            ("visits", "🏡", "Visits", "Energy assessment visits", VisitsPage),
            ("links", "🔗", "Link Generator", "Create pre-filled forms", LinksPage),
            ("settings", "⚙️", "Settings", "Application settings", SettingsPage)
        ]
        
        self.nav_buttons = {}
        for page_id, icon, label, description, page_class in self.nav_items:
            # Button container with padding
            btn_container = ttk.Frame(nav_frame, style="Sidebar.TFrame")
            btn_container.pack(fill=X, pady=3)
            
            # Main navigation button - much wider
            btn = ttk.Button(
                btn_container,
                text=f"{icon}  {label}",
                command=lambda p=page_id: self.show_page(p),
                style="SidebarNav.TButton",
                width=25  # Increased width
            )
            btn.pack(fill=X)
            
            # Description text
            desc_label = ttk.Label(
                btn_container,
                text=description,
                font=("Helvetica", 8),
                foreground=Colors.TEXT_MUTED,
                background=Colors.SIDEBAR_BG,
                style="SidebarDesc.TLabel"
            )
            desc_label.pack(pady=(2, 8))
            
            self.nav_buttons[page_id] = btn
        
        # Footer section with better spacing
        footer_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        footer_frame.pack(side=BOTTOM, fill=X, padx=20, pady=20)
        
        # Status indicator
        status_frame = ttk.Frame(footer_frame, style="Sidebar.TFrame")
        status_frame.pack(fill=X, pady=(0, 10))
        
        status_dot = ttk.Label(
            status_frame,
            text="●",
            font=("Helvetica", 12),
            foreground=Colors.SUCCESS,
            background=Colors.SIDEBAR_BG
        )
        status_dot.pack(side=LEFT)
        
        status_label = ttk.Label(
            status_frame,
            text="System Online",
            font=("Helvetica", 9),
            foreground=Colors.TEXT_SECONDARY,
            background=Colors.SIDEBAR_BG
        )
        status_label.pack(side=LEFT, padx=(5, 0))
        
        # Version info
        version_label = ttk.Label(
            footer_frame,
            text=f"Version {Config.APP_VERSION}",
            font=("Helvetica", 8),
            foreground=Colors.TEXT_MUTED,
            background=Colors.SIDEBAR_BG,
            style="SidebarVersion.TLabel"
        )
        version_label.pack()
    
    def create_content_area(self):
        """Create main content area with better styling"""
        # Content frame with padding and background
        self.content_frame = ttk.Frame(self.root, style="Content.TFrame")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def setup_styles(self):
        """Setup custom styles with improved colors and contrast"""
        style = ttk.Style()
        
        # Sidebar styles with better colors
        style.configure(
            "Sidebar.TFrame",
            background=Colors.SIDEBAR_BG,
            relief="flat",
            borderwidth=0
        )
        
        style.configure(
            "SidebarHeader.TFrame",
            background=Colors.SIDEBAR_BG,
            relief="flat"
        )
        
        style.configure(
            "SidebarDivider.TFrame",
            background=Colors.PRIMARY_GREEN
        )
        
        # Navigation button styles
        style.configure(
            "SidebarNav.TButton",
            background=Colors.SIDEBAR_BG,
            foreground=Colors.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor="none",
            font=("Helvetica", 11, "normal"),
            padding=(15, 12),
            anchor="w"
        )
        
        style.map(
            "SidebarNav.TButton",
            background=[
                ("active", Colors.PRIMARY_GREEN_LIGHT),
                ("pressed", Colors.PRIMARY_GREEN)
            ],
            foreground=[
                ("active", Colors.TEXT_PRIMARY),
                ("pressed", "white")
            ]
        )
        
        # Active navigation button style
        style.configure(
            "SidebarNavActive.TButton",
            background=Colors.PRIMARY_GREEN,
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            font=("Helvetica", 11, "bold"),
            padding=(15, 12),
            anchor="w"
        )
        
        # Text label styles
        style.configure(
            "SidebarTitle.TLabel",
            background=Colors.SIDEBAR_BG,
            foreground=Colors.PRIMARY_GREEN,
            font=("Helvetica", 18, "bold")
        )
        
        style.configure(
            "SidebarSubtitle.TLabel",
            background=Colors.SIDEBAR_BG,
            foreground=Colors.TEXT_SECONDARY,
            font=("Helvetica", 11)
        )
        
        style.configure(
            "SidebarDesc.TLabel",
            background=Colors.SIDEBAR_BG,
            foreground=Colors.TEXT_MUTED,
            font=("Helvetica", 8)
        )
        
        style.configure(
            "SidebarVersion.TLabel",
            background=Colors.SIDEBAR_BG,
            foreground=Colors.TEXT_MUTED,
            font=("Helvetica", 8)
        )
        
        # Content area style
        style.configure(
            "Content.TFrame",
            background=Colors.BACKGROUND,
            relief="flat"
        )
    
    def show_page(self, page_id):
        """Show a specific page"""
        try:
            # Hide current page
            if self.current_page:
                self.current_page.pack_forget()
            
            # Get or create page
            if page_id not in self.pages:
                page_class = next(
                    (pc for pid, _, _, _, pc in self.nav_items if pid == page_id), 
                    None
                )
                if page_class:
                    self.pages[page_id] = page_class(self.content_frame, self)
                else:
                    logger.error(f"Unknown page: {page_id}")
                    return
            
            # Show page
            page = self.pages[page_id]
            page.pack(fill=BOTH, expand=True)
            self.current_page = page
            
            # Update navigation button styles
            self.update_nav_buttons(page_id)
            
            # Refresh page data if needed
            if hasattr(page, 'refresh_data'):
                page.refresh_data()
            
            logger.info(f"Switched to page: {page_id}")
            
        except Exception as e:
            logger.error(f"Failed to show page {page_id}: {e}")
            messagebox.showerror("Error", f"Failed to load page: {e}")
    
    def update_nav_buttons(self, active_page):
        """Update navigation button styles"""
        for page_id, button in self.nav_buttons.items():
            if page_id == active_page:
                button.configure(style="SidebarNavActive.TButton")
            else:
                button.configure(style="SidebarNav.TButton")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        
        # Get window size
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window position
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def run(self):
        """Run the application"""
        try:
            # Handle window close event
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Application runtime error: {e}")
            raise
    
    def on_closing(self):
        """Handle application closing"""
        try:
            # Ask for confirmation
            if messagebox.askokcancel(
                "Quit", 
                "Do you want to quit EnergieFixers071?"
            ):
                logger.info("Application closing...")
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            logger.error(f"Error during application closing: {e}")
            self.root.quit()
    
    def refresh_all_pages(self):
        """Refresh all loaded pages"""
        for page in self.pages.values():
            if hasattr(page, 'refresh_data'):
                try:
                    page.refresh_data()
                except Exception as e:
                    logger.error(f"Failed to refresh page: {e}")