"""
Simplified main application window for EnergieFixers071
with basic theming and error-free imports.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)

class MainApplication:
    """Main application window with improved navigation and styling"""
    
    def __init__(self):
        try:
            # Import configuration safely
            from config import Config, Colors, Theme
            self.config = Config
            self.colors = Colors
            self.theme = Theme
            
            # Create main window
            self.create_window()
            self.setup_variables()
            self.setup_ui()
            self.setup_styles()
            self.show_page("home")
            self.center_window()
            
            logger.info("Main application window initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize main application: {e}")
            self.show_startup_error(e)
    
    def create_window(self):
        """Create main window"""
        self.root = ttk.Window(
            title=self.config.WINDOW_TITLE,
            themename=self.config.DEFAULT_THEME,
            size=tuple(map(int, self.config.WINDOW_GEOMETRY.split('x'))),
            minsize=self.config.MIN_WINDOW_SIZE
        )
        
        # Configure window
        self.root.iconify()  # Start minimized to avoid flashing
    
    def setup_variables(self):
        """Initialize application variables"""
        self.current_page = None
        self.pages = {}
        self.nav_buttons = {}
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Configure main grid
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create UI components
        self.create_sidebar()
        self.create_content_area()
    
    def create_sidebar(self):
        """Create enhanced navigation sidebar"""
        # Sidebar frame - wider and more attractive
        self.sidebar = ttk.Frame(
            self.root, 
            style="Sidebar.TFrame", 
            width=self.config.SIDEBAR_WIDTH
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
        self.sidebar.grid_propagate(False)
        
        # Header section
        self.create_sidebar_header()
        
        # Navigation section
        self.create_navigation()
        
        # Footer section
        self.create_sidebar_footer()
    
    def create_sidebar_header(self):
        """Create sidebar header with logo/title"""
        header_frame = ttk.Frame(self.sidebar, style="SidebarHeader.TFrame")
        header_frame.pack(fill=X, padx=20, pady=30)
        
        # Application title
        title_label = ttk.Label(
            header_frame,
            text="EnergieFixers071",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_HEADER, "bold"),
            foreground=self.colors.PRIMARY_GREEN,
            background=self.colors.SIDEBAR_BG,
            style="SidebarTitle.TLabel"
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Volunteer Management System",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_NORMAL),
            foreground=self.colors.TEXT_SECONDARY,
            background=self.colors.SIDEBAR_BG,
            style="SidebarSubtitle.TLabel"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Divider line
        divider = ttk.Frame(header_frame, height=2, style="SidebarDivider.TFrame")
        divider.pack(fill=X, pady=20)
    
    def create_navigation(self):
        """Create navigation menu"""
        nav_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        nav_frame.pack(fill=BOTH, expand=True, padx=20)
        
        # Navigation items with descriptions
        self.nav_items = [
            ("home", "🏠", "Dashboard", "Overview and statistics"),
            ("volunteers", "👥", "Volunteers", "Manage volunteer profiles"),
            ("appointments", "📅", "Appointments", "Scheduled appointments"),
            ("visits", "🏡", "Visits", "Energy assessment visits"),
            ("links", "🔗", "Link Generator", "Create pre-filled forms"),
            ("settings", "⚙️", "Settings", "Application settings")
        ]
        
        # Create navigation buttons
        for page_id, icon, label, description in self.nav_items:
            self.create_nav_button(nav_frame, page_id, icon, label, description)
    
    def create_nav_button(self, parent, page_id, icon, label, description):
        """Create individual navigation button"""
        # Button container with padding
        btn_container = ttk.Frame(parent, style="Sidebar.TFrame")
        btn_container.pack(fill=X, pady=3)
        
        # Main navigation button
        btn = ttk.Button(
            btn_container,
            text=f"{icon} {label}",
            command=lambda: self.show_page(page_id),
            style="SidebarNav.TButton",
            width=25
        )
        btn.pack(fill=X)
        
        # Description text
        desc_label = ttk.Label(
            btn_container,
            text=description,
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_MUTED,
            background=self.colors.SIDEBAR_BG,
            style="SidebarDesc.TLabel"
        )
        desc_label.pack(pady=(2, 8))
        
        self.nav_buttons[page_id] = btn
    
    def create_sidebar_footer(self):
        """Create sidebar footer"""
        footer_frame = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        footer_frame.pack(side=BOTTOM, fill=X, padx=20, pady=20)
        
        # Status indicator
        status_frame = ttk.Frame(footer_frame, style="Sidebar.TFrame")
        status_frame.pack(fill=X, pady=(0, 10))
        
        status_dot = ttk.Label(
            status_frame,
            text="●",
            font=(self.theme.FONT_FAMILY, 12),
            foreground=self.colors.SUCCESS,
            background=self.colors.SIDEBAR_BG
        )
        status_dot.pack(side=LEFT)
        
        status_label = ttk.Label(
            status_frame,
            text="System Online",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY,
            background=self.colors.SIDEBAR_BG
        )
        status_label.pack(side=LEFT, padx=(5, 0))
        
        # Version info
        version_label = ttk.Label(
            footer_frame,
            text=f"Version {self.config.APP_VERSION}",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_MUTED,
            background=self.colors.SIDEBAR_BG,
            style="SidebarVersion.TLabel"
        )
        version_label.pack()
    
    def create_content_area(self):
        """Create main content area"""
        self.content_frame = ttk.Frame(self.root, style="Content.TFrame")
        self.content_frame.grid(
            row=0, column=1, 
            sticky="nsew", 
            padx=self.theme.SPACING_LARGE, 
            pady=self.theme.SPACING_LARGE
        )
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def setup_styles(self):
        """Setup custom styles"""
        try:
            style = ttk.Style()
            
            # Sidebar styles
            style.configure(
                "Sidebar.TFrame",
                background=self.colors.SIDEBAR_BG,
                relief="flat",
                borderwidth=0
            )
            
            style.configure(
                "SidebarHeader.TFrame",
                background=self.colors.SIDEBAR_BG,
                relief="flat"
            )
            
            style.configure(
                "SidebarDivider.TFrame",
                background=self.colors.PRIMARY_GREEN
            )
            
            # Navigation button styles
            style.configure(
                "SidebarNav.TButton",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_PRIMARY,
                borderwidth=0,
                focuscolor="none",
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_NORMAL, "normal"),
                padding=(15, 12),
                anchor="w"
            )
            
            style.map(
                "SidebarNav.TButton",
                background=[
                    ("active", self.colors.PRIMARY_GREEN_LIGHT),
                    ("pressed", self.colors.PRIMARY_GREEN)
                ],
                foreground=[
                    ("active", self.colors.TEXT_PRIMARY),
                    ("pressed", "white")
                ]
            )
            
            # Active navigation button style
            style.configure(
                "SidebarNavActive.TButton",
                background=self.colors.PRIMARY_GREEN,
                foreground="white",
                borderwidth=0,
                focuscolor="none",
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_NORMAL, "bold"),
                padding=(15, 12),
                anchor="w"
            )
            
            # Text label styles
            style.configure(
                "SidebarTitle.TLabel",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.PRIMARY_GREEN,
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_HEADER, "bold")
            )
            
            style.configure(
                "SidebarSubtitle.TLabel",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_SECONDARY,
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_NORMAL)
            )
            
            style.configure(
                "SidebarDesc.TLabel",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_MUTED,
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL)
            )
            
            style.configure(
                "SidebarVersion.TLabel",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_MUTED,
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL)
            )
            
            # Content area style
            style.configure(
                "Content.TFrame",
                background=self.colors.BACKGROUND,
                relief="flat"
            )
            
        except Exception as e:
            logger.error(f"Failed to setup styles: {e}")
            # Continue without custom styling
    
    def show_page(self, page_id):
        """Show a specific page with enhanced error handling"""
        try:
            # Hide current page
            if self.current_page:
                self.current_page.pack_forget()
            
            # Get or create page
            if page_id not in self.pages:
                page_class = self.get_page_class(page_id)
                if page_class:
                    self.pages[page_id] = page_class(self.content_frame, self)
                else:
                    logger.error(f"Unknown page: {page_id}")
                    self.show_error_page(f"Page '{page_id}' not found")
                    return
            
            # Show page
            page = self.pages[page_id]
            page.pack(fill=BOTH, expand=True)
            self.current_page = page
            
            # Update navigation button styles
            self.update_nav_buttons(page_id)
            
            # Refresh page data if needed
            if hasattr(page, 'refresh_data'):
                try:
                    page.refresh_data()
                except Exception as e:
                    logger.error(f"Failed to refresh page data: {e}")
            
            logger.info(f"Successfully showed page: {page_id}")
            
        except Exception as e:
            logger.error(f"Failed to show page {page_id}: {e}")
            self.show_error_page(f"Error loading page: {e}")
    
    def get_page_class(self, page_id):
        """Get page class with safe imports"""
        try:
            if page_id == "home":
                from ui.pages.home_page import HomePage
                return HomePage
            elif page_id == "volunteers":
                from ui.pages.volunteer_page import VolunteerPage
                return VolunteerPage
            elif page_id == "appointments":
                from ui.pages.appointments_page import AppointmentsPage
                return AppointmentsPage
            elif page_id == "visits":
                from ui.pages.visits_page import VisitsPage
                return VisitsPage
            elif page_id == "links":
                from ui.pages.links_page import LinksPage
                return LinksPage
            elif page_id == "settings":
                from ui.pages.settings_page import SettingsPage
                return SettingsPage
            else:
                return None
        except ImportError as e:
            logger.error(f"Failed to import page class {page_id}: {e}")
            return self.create_placeholder_page_class(page_id.title(), f"{page_id.title()} page coming soon...")
    
    def create_placeholder_page_class(self, title, message):
        """Create placeholder page class for missing pages"""
        class PlaceholderPage(ttk.Frame):
            def __init__(self, parent, app):
                super().__init__(parent)
                ttk.Label(
                    self, 
                    text=title, 
                    font=("Arial", 18, "bold")
                ).pack(pady=50)
                ttk.Label(
                    self, 
                    text=message, 
                    font=("Arial", 12)
                ).pack()
            
            def refresh_data(self):
                pass
        
        return PlaceholderPage
    
    def show_error_page(self, error_message):
        """Show error page"""
        try:
            if hasattr(self, 'current_page') and self.current_page:
                self.current_page.pack_forget()
            
            error_frame = ttk.Frame(self.content_frame)
            error_frame.pack(fill=BOTH, expand=True)
            
            ttk.Label(
                error_frame,
                text="⚠️ Error",
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_HEADER, "bold"),
                foreground=self.colors.DANGER
            ).pack(pady=50)
            
            ttk.Label(
                error_frame,
                text=str(error_message),
                font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_NORMAL)
            ).pack()
            
            self.current_page = error_frame
            
        except Exception as e:
            logger.error(f"Failed to show error page: {e}")
    
    def update_nav_buttons(self, active_page):
        """Update navigation button styles safely"""
        try:
            for page_id, button in self.nav_buttons.items():
                if page_id == active_page:
                    button.configure(style="SidebarNavActive.TButton")
                else:
                    button.configure(style="SidebarNav.TButton")
        except Exception as e:
            logger.error(f"Failed to update nav buttons: {e}")
    
    def center_window(self):
        """Center the window on screen"""
        try:
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
            
        except Exception as e:
            logger.error(f"Failed to center window: {e}")
    
    def show_startup_error(self, error):
        """Show startup error dialog"""
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            
            messagebox.showerror(
                "EnergieFixers071 - Startup Error",
                f"Failed to start application:\n\n{error}\n\nCheck logs for details."
            )
            
            root.destroy()
            
        except Exception:
            print(f"CRITICAL ERROR: Failed to start EnergieFixers071: {error}")
    
    def run(self):
        """Run the application with error handling"""
        try:
            # Handle window close event
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # Show window
            self.root.deiconify()
            
            # Start main loop
            self.root.mainloop()
            
        except Exception as e:
            logger.error(f"Application runtime error: {e}")
            raise
    
    def on_closing(self):
        """Handle application closing"""
        try:
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
        """Refresh all loaded pages safely"""
        for page_id, page in self.pages.items():
            if hasattr(page, 'refresh_data'):
                try:
                    page.refresh_data()
                except Exception as e:
                    logger.error(f"Failed to refresh page {page_id}: {e}")