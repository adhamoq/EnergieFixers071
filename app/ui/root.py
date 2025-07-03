"""
Main application window for EnergieFixers071
Supports only flatly and darkly themes with consistent layout
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import logging
from config import Config, Colors, Theme

logger = logging.getLogger(__name__)

class MainApplication:
    """Main application with flatly and darkly theme support"""
    
    def __init__(self):
        try:
            # Start with default theme
            self.current_theme = Config.DEFAULT_THEME
            self.colors = Colors(self.current_theme)
            
            self.create_window()
            self.setup_variables()
            self.setup_ui()
            self.apply_custom_styles()
            self.show_page("home")
            self.center_window()
            
            logger.info(f"Application initialized with {self.current_theme} theme")
            
        except Exception as e:
            logger.error(f"Failed to initialize application: {e}")
            self.show_startup_error(e)
    
    def create_window(self):
        """Create main window with current theme"""
        self.root = ttk.Window(
            title=Config.WINDOW_TITLE,
            themename=self.current_theme,
            size=tuple(map(int, Config.WINDOW_GEOMETRY.split('x'))),
            minsize=Config.MIN_WINDOW_SIZE
        )
        self.root.iconify()
    
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
        """Create sidebar with theme toggle"""
        # Sidebar frame with fixed width
        self.sidebar = ttk.Frame(
            self.root,
            width=Theme.SIDEBAR_WIDTH
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar.grid_propagate(False)
        
        # Header section
        self.create_sidebar_header()
        
        # Theme toggle section
        self.create_theme_toggle()
        
        # Navigation section
        self.create_navigation()
        
        # Footer section
        self.create_sidebar_footer()
    
    def create_sidebar(self):
        """Create sidebar without theme toggle"""
        # Sidebar frame with fixed width
        self.sidebar = ttk.Frame(
            self.root,
            width=Theme.SIDEBAR_WIDTH
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar.grid_propagate(False)
        
        # Header section
        self.create_sidebar_header()
        
        # Navigation section (NO theme toggle)
        self.create_navigation()
        
        # Footer section
        self.create_sidebar_footer()

    
    def create_sidebar_header(self):
        """Create sidebar header"""
        header_frame = ttk.Frame(self.sidebar)
        header_frame.pack(fill=X, padx=15, pady=20)
        
        # Application title
        title_label = ttk.Label(
            header_frame,
            text="EnergieFixers071",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
            foreground=self.colors.PRIMARY_GREEN
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Volunteer Management",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 5))
    
    def change_theme(self):
        """Change between flatly and darkly themes"""
        new_theme = self.theme_var.get()
        
        if new_theme != self.current_theme and new_theme in Config.AVAILABLE_THEMES:
            try:
                # Update theme
                self.current_theme = new_theme
                self.colors = Colors(new_theme)
                
                # Apply new theme to window
                self.root.style.theme_use(new_theme)
                
                # Reapply custom styles
                self.apply_custom_styles()
                
                # Refresh all pages
                self.refresh_all_pages()
                
                logger.info(f"Changed theme to: {new_theme}")
                
            except Exception as e:
                logger.error(f"Failed to change theme: {e}")
                # Reset to previous theme
                self.theme_var.set(self.current_theme)
    
    def apply_custom_styles(self):
        """Apply custom styles for current theme"""
        try:
            style = self.root.style
            
            # Sidebar styling
            style.configure(
                "Sidebar.TFrame",
                background=self.colors.SIDEBAR_BG
            )
            
            # Sidebar buttons
            style.configure(
                "Sidebar.TButton",
                background=self.colors.SIDEBAR_BG,
                foreground=self.colors.TEXT_PRIMARY,
                borderwidth=0,
                focuscolor="none",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
                padding=(15, 10)
            )
            
            style.map(
                "Sidebar.TButton",
                background=[
                    ("active", self.colors.PRIMARY),
                    ("pressed", self.colors.HOVER)
                ],
                foreground=[
                    ("active", "white" if self.current_theme == "flatly" else "white"),
                    ("pressed", "white")
                ]
            )
            
            # Active sidebar button
            style.configure(
                "SidebarActive.TButton",
                background=self.colors.PRIMARY,
                foreground="white",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")
            )
            
            # Content area
            style.configure(
                "Content.TFrame",
                background=self.colors.CONTENT_BG
            )
            
        except Exception as e:
            logger.error(f"Failed to apply custom styles: {e}")
    
    def create_navigation(self):
        """Create navigation menu"""
        nav_frame = ttk.Frame(self.sidebar)
        nav_frame.pack(fill=BOTH, expand=True, padx=15)
        
        # Navigation items
        self.nav_items = [
            ("home", "🏠 Dashboard", "Overview & Statistics"),
            ("volunteers", "👥 Volunteers", "Manage Volunteer Data"),
            ("appointments", "📅 Appointments", "Calendar & Scheduling"),
            ("visits", "🏡 Visits", "Energy Assessment Records"),
            ("links", "🔗 Link Generator", "Create Pre-filled Forms"),
            ("settings", "⚙️ Settings", "App Configuration")
        ]
        
        # Create navigation buttons
        for page_id, label, description in self.nav_items:
            self.create_nav_button(nav_frame, page_id, label, description)
    
    def create_nav_button(self, parent, page_id, label, description):
        """Create individual navigation button"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=X, pady=3)
        
        # Main button
        btn = ttk.Button(
            button_frame,
            text=label,
            command=lambda: self.show_page(page_id),
            style="Sidebar.TButton",
            width=25
        )
        btn.pack(fill=X)
        
        # Description label
        desc_label = ttk.Label(
            button_frame,
            text=description,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL - 1),
            foreground=self.colors.TEXT_MUTED
        )
        desc_label.pack(fill=X, padx=(10, 0))
        
        self.nav_buttons[page_id] = btn
    
    def create_sidebar_footer(self):
        """Create sidebar footer"""
        footer_frame = ttk.Frame(self.sidebar)
        footer_frame.pack(side=BOTTOM, fill=X, padx=15, pady=15)
        
        # Version info
        version_label = ttk.Label(
            footer_frame,
            text=f"v{Config.APP_VERSION}",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_MUTED
        )
        version_label.pack()
        
        # Current theme info
        theme_label = ttk.Label(
            footer_frame,
            text=f"Theme: {self.current_theme.title()}",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.SUCCESS
        )
        theme_label.pack()
    
    def create_content_area(self):
        """Create main content area"""
        self.content_frame = ttk.Frame(self.root, style="Content.TFrame")
        self.content_frame.grid(
            row=0, column=1,
            sticky="nsew",
            padx=Theme.SPACING_LARGE,
            pady=Theme.SPACING_LARGE
        )
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def show_page(self, page_id):
        """Show a specific page"""
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
                    self.show_error_page(f"Page '{page_id}' not found")
                    return
            
            # Show page
            page = self.pages[page_id]
            page.pack(fill=BOTH, expand=True)
            self.current_page = page
            
            # Update navigation
            self.update_nav_buttons(page_id)
            
            # Refresh page data
            if hasattr(page, 'refresh_data'):
                page.refresh_data()
            
        except Exception as e:
            logger.error(f"Failed to show page {page_id}: {e}")
            self.show_error_page(f"Error loading page: {e}")
    
    def get_page_class(self, page_id):
        """Get page class with safe imports"""
        try:
            page_map = {
                "home": lambda: __import__('ui.pages.home_page', fromlist=['HomePage']).HomePage,
                "volunteers": lambda: __import__('ui.pages.volunteer_page', fromlist=['VolunteerPage']).VolunteerPage,
                "appointments": lambda: __import__('ui.pages.appointments_page', fromlist=['AppointmentsPage']).AppointmentsPage,
                "visits": lambda: __import__('ui.pages.visits_page', fromlist=['VisitsPage']).VisitsPage,
                "links": lambda: __import__('ui.pages.links_page', fromlist=['LinksPage']).LinksPage,
                "settings": lambda: __import__('ui.pages.settings_page', fromlist=['SettingsPage']).SettingsPage
            }
            
            if page_id in page_map:
                return page_map[page_id]()
            return None
            
        except ImportError:
            return self.create_placeholder_page(page_id)
        except Exception as e:
            logger.error(f"Failed to load page {page_id}: {e}")
            return None
    
    def create_placeholder_page(self, page_id):
        """Create placeholder page for missing pages"""
        class PlaceholderPage(ttk.Frame):
            def __init__(self, parent, app):
                super().__init__(parent)
                ttk.Label(
                    self,
                    text=f"{page_id.title()} Page",
                    font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADER, "bold")
                ).pack(pady=50)
                ttk.Label(
                    self,
                    text="This page is under development",
                    font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)
                ).pack()
            
            def refresh_data(self):
                pass
        
        return PlaceholderPage
    
    def show_error_page(self, error_message):
        """Show error page"""
        try:
            if self.current_page:
                self.current_page.pack_forget()
            
            error_frame = ttk.Frame(self.content_frame)
            error_frame.pack(fill=BOTH, expand=True)
            
            ttk.Label(
                error_frame,
                text="⚠️ Error",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADER, "bold"),
                foreground=self.colors.DANGER
            ).pack(pady=50)
            
            ttk.Label(
                error_frame,
                text=str(error_message),
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)
            ).pack()
            
            self.current_page = error_frame
            
        except Exception as e:
            logger.error(f"Failed to show error page: {e}")
    
    def update_nav_buttons(self, active_page):
        """Update navigation button styles"""
        for page_id, button in self.nav_buttons.items():
            if page_id == active_page:
                button.configure(style="SidebarActive.TButton")
            else:
                button.configure(style="Sidebar.TButton")
    
    def center_window(self):
        """Center window on screen"""
        try:
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self.root.geometry(f"{width}x{height}+{x}+{y}")
        except Exception as e:
            logger.error(f"Failed to center window: {e}")
    
    def show_startup_error(self, error):
        """Show startup error"""
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "EnergieFixers071 - Error",
                f"Failed to start:\n\n{error}"
            )
            root.destroy()
        except Exception:
            print(f"CRITICAL ERROR: {error}")
    
    def run(self):
        """Run the application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.deiconify()
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Runtime error: {e}")
            raise
    
    def on_closing(self):
        """Handle application closing"""
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit EnergieFixers071?"):
                self.root.quit()
                self.root.destroy()
        except Exception as e:
            logger.error(f"Error during closing: {e}")
            self.root.quit()
    
    def refresh_all_pages(self):
        """Refresh all loaded pages after theme change"""
        for page_id, page in self.pages.items():
            if hasattr(page, 'refresh_styling'):
                try:
                    page.refresh_styling()
                except Exception as e:
                    logger.error(f"Failed to refresh styling for {page_id}: {e}")
