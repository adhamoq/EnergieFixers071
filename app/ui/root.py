"""
Main application window with navigation and page management.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from config import Config, Colors
from ui.pages.home import HomePage
from ui.pages.volunteer import VolunteerPage
from ui.pages.appointments import AppointmentsPage
from ui.pages.visits import VisitsPage
from ui.pages.links import LinksPage
from ui.pages.settings import SettingsPage
import logging

logger = logging.getLogger(__name__)

class MainApplication:
    """Main application window with navigation"""
    
    def __init__(self):
        # Create main window
        self.root = ttk.Window(
            title=Config.WINDOW_TITLE,
            themename="flatly",
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
        """Setup the main UI layout"""
        # Configure main grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_content_area()
    
    def create_sidebar(self):
        """Create navigation sidebar"""
        # Sidebar frame
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar.grid_propagate(False)
        
        # Logo/Header section
        header_frame = ttk.Frame(self.sidebar)
        header_frame.pack(fill=X, padx=10, pady=20)
        
        # Application title
        title_label = ttk.Label(
            header_frame,
            text="EnergieFixers071",
            font=("Helvetica", 14, "bold"),
            foreground=Colors.PRIMARY_GREEN
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Volunteer Management",
            font=("Helvetica", 9),
            foreground=Colors.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Navigation buttons
        nav_frame = ttk.Frame(self.sidebar)
        nav_frame.pack(fill=BOTH, expand=True, padx=10)
        
        # Navigation items
        self.nav_items = [
            ("home", "🏠 Dashboard", HomePage),
            ("volunteers", "👥 Volunteers", VolunteerPage),
            ("appointments", "📅 Appointments", AppointmentsPage),
            ("visits", "🏡 Visits", VisitsPage),
            ("links", "🔗 Link Generator", LinksPage),
            ("settings", "⚙️ Settings", SettingsPage)
        ]
        
        self.nav_buttons = {}
        for page_id, label, page_class in self.nav_items:
            btn = ttk.Button(
                nav_frame,
                text=label,
                command=lambda p=page_id: self.show_page(p),
                style="Sidebar.TButton",
                width=20
            )
            btn.pack(fill=X, pady=2)
            self.nav_buttons[page_id] = btn
        
        # Footer section
        footer_frame = ttk.Frame(self.sidebar)
        footer_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10)
        
        version_label = ttk.Label(
            footer_frame,
            text=f"v{Config.APP_VERSION}",
            font=("Helvetica", 8),
            foreground=Colors.TEXT_SECONDARY
        )
        version_label.pack()
    
    def create_content_area(self):
        """Create main content area"""
        # Content frame
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        
        # Sidebar styles
        style.configure(
            "Sidebar.TFrame",
            background=Colors.SURFACE,
            relief="flat"
        )
        
        style.configure(
            "Sidebar.TButton",
            background=Colors.SURFACE,
            foreground=Colors.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor="none",
            font=("Helvetica", 10)
        )
        
        style.map(
            "Sidebar.TButton",
            background=[
                ("active", Colors.PRIMARY_GREEN),
                ("pressed", Colors.SECONDARY_GREEN)
            ],
            foreground=[
                ("active", "white"),
                ("pressed", "white")
            ]
        )
        
        # Active navigation button style
        style.configure(
            "SidebarActive.TButton",
            background=Colors.PRIMARY_GREEN,
            foreground="white",
            borderwidth=0,
            focuscolor="none",
            font=("Helvetica", 10, "bold")
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
                    (pc for pid, _, pc in self.nav_items if pid == page_id), 
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
                button.configure(style="SidebarActive.TButton")
            else:
                button.configure(style="Sidebar.TButton")
    
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
