"""
Enhanced main application window for EnergieFixers071
with custom theme support (flatly_enhanced and darkly_enhanced),
sidebar improvements, and robust error handling.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import logging
from core.theme_manager import ThemeManager

logger = logging.getLogger(__name__)

class MainApplication:
    """Main application window with custom theming and improved sidebar."""

    def __init__(self):
        try:
            # Initialize theme manager and register themes
            self.theme_manager = ThemeManager()
            if not self.theme_manager.initialize_themes():
                raise Exception("Failed to initialize themes")

            # Create main window with enhanced theme
            self.create_window()
            self.setup_variables()
            self.setup_ui()
            self.show_page("home")
            self.center_window()

            logger.info("Main application initialized with enhanced themes")

        except Exception as e:
            logger.error(f"Failed to initialize main application: {e}")
            self.show_startup_error(e)

    def create_window(self):
        """Create main window with enhanced theme."""
        from config import Config

        self.root = ttk.Window(
            title=Config.WINDOW_TITLE,
            themename=self.theme_manager.current_theme,
            size=tuple(map(int, Config.WINDOW_GEOMETRY.split('x'))),
            minsize=Config.MIN_WINDOW_SIZE
        )

        # Update style reference
        self.theme_manager.style = self.root.style
        self.root.iconify()

    def setup_variables(self):
        self.current_page = None
        self.pages = {}
        self.nav_buttons = {}

    def setup_ui(self):
        """Setup the main UI layout with enhanced styling."""
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.create_sidebar()
        self.create_content_area()

    def create_sidebar(self):
        """Create enhanced sidebar with theme toggle."""
        from config import Config

        self.sidebar = ttk.Frame(
            self.root,
            style="Sidebar.TFrame",
            width=Config.SIDEBAR_WIDTH
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 1))
        self.sidebar.grid_propagate(False)

        self.create_sidebar_header()
        self.create_theme_toggle()
        self.create_navigation()
        self.create_sidebar_footer()

    def create_sidebar_header(self):
        """Sidebar header with logo/title."""
        from config import Theme

        header_frame = ttk.Frame(self.sidebar)
        header_frame.pack(fill=X, padx=15, pady=20)

        title_label = ttk.Label(
            header_frame,
            text="EnergieFixers071",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
            foreground=self.theme_manager.colors.PRIMARY
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Volunteer Management",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.theme_manager.colors.TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 5))

        status_label = ttk.Label(
            header_frame,
            text="● Online",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.theme_manager.colors.SUCCESS
        )
        status_label.pack()

    def create_theme_toggle(self):
        """Theme toggle section for switching between flatly and darkly."""
        theme_frame = ttk.Frame(self.sidebar)
        theme_frame.pack(fill=X, padx=15, pady=10)

        ttk.Label(
            theme_frame,
            text="Theme:",
            font=("Segoe UI", 10, "bold"),
            foreground=self.theme_manager.colors.TEXT_PRIMARY
        ).pack(anchor="w")

        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        theme_names = self.theme_manager.get_theme_display_names()

        for theme_id, display_name in theme_names.items():
            ttk.Radiobutton(
                theme_frame,
                text=display_name,
                variable=self.theme_var,
                value=theme_id,
                command=self.change_theme
            ).pack(anchor="w", pady=2)

    def change_theme(self):
        """Handle theme change."""
        new_theme = self.theme_var.get()
        if new_theme != self.theme_manager.current_theme:
            if self.theme_manager.apply_theme(new_theme):
                self.refresh_ui_styling()
                messagebox.showinfo("Theme Changed", f"Theme changed to {self.theme_manager.get_theme_display_names()[new_theme]}")
            else:
                messagebox.showerror("Theme Error", "Failed to change theme")
                self.theme_var.set(self.theme_manager.current_theme)

    def refresh_ui_styling(self):
        """Refresh UI styling after theme change."""
        try:
            for page in getattr(self, 'pages', {}).values():
                if hasattr(page, 'refresh_styling'):
                    page.refresh_styling()
        except Exception as e:
            logger.error(f"Failed to refresh UI styling: {e}")

    def create_navigation(self):
        """Create navigation menu with improved layout."""
        nav_frame = ttk.Frame(self.sidebar)
        nav_frame.pack(fill=BOTH, expand=True, padx=15)

        self.nav_items = [
            ("home", "🏠 Dashboard", "Overview & Statistics", self.load_home_page),
            ("volunteers", "👥 Volunteers", "Manage Volunteer Data", self.load_volunteer_page),
            ("appointments", "📅 Appointments", "Calendar & Scheduling", self.load_appointments_page),
            ("visits", "🏡 Visits", "Energy Assessment Records", self.load_visits_page),
            ("links", "🔗 Link Generator", "Create Pre-filled Forms", self.load_links_page),
            ("settings", "⚙️ Settings", "App Configuration", self.load_settings_page)
        ]

        for page_id, label, description, loader_func in self.nav_items:
            self.create_nav_button(nav_frame, page_id, label, description, loader_func)

    def create_nav_button(self, parent, page_id, label, description, loader_func):
        """Create individual navigation button."""
        from config import Theme

        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=X, pady=2)

        btn = ttk.Button(
            button_frame,
            text=label,
            command=lambda: self.show_page(page_id),
            style="Sidebar.TButton",
            width=25
        )
        btn.pack(fill=X)

        desc_label = ttk.Label(
            button_frame,
            text=description,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL - 1),
            foreground=self.theme_manager.colors.TEXT_MUTED
        )
        desc_label.pack(fill=X, padx=(10, 0))

        self.nav_buttons[page_id] = btn

    def create_sidebar_footer(self):
        """Sidebar footer with version and status."""
        from config import Config, Theme

        footer_frame = ttk.Frame(self.sidebar)
        footer_frame.pack(side=BOTTOM, fill=X, padx=15, pady=15)

        version_label = ttk.Label(
            footer_frame,
            text=f"v{Config.APP_VERSION}",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.theme_manager.colors.TEXT_MUTED
        )
        version_label.pack()

        status_label = ttk.Label(
            footer_frame,
            text="Ready",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.theme_manager.colors.SUCCESS
        )
        status_label.pack()

    def create_content_area(self):
        """Create main content area."""
        from config import Theme

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
        """Show a specific page with enhanced error handling."""
        try:
            if self.current_page:
                self.current_page.pack_forget()

            if page_id not in self.pages:
                page_class = self.get_page_class(page_id)
                if page_class:
                    self.pages[page_id] = page_class(self.content_frame, self)
                else:
                    logger.error(f"Unknown page: {page_id}")
                    self.show_error_page(f"Page '{page_id}' not found")
                    return

            page = self.pages[page_id]
            page.pack(fill=BOTH, expand=True)
            self.current_page = page

            self.update_nav_buttons(page_id)

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
        """Get page class with safe imports."""
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
        except Exception as e:
            logger.error(f"Failed to load page class {page_id}: {e}")
            return None

    def show_error_page(self, error_message):
        """Show error page."""
        try:
            if hasattr(self, 'current_page') and self.current_page:
                self.current_page.pack_forget()

            error_frame = ttk.Frame(self.content_frame)
            error_frame.pack(fill=BOTH, expand=True)

            ttk.Label(
                error_frame,
                text="⚠️ Error",
                font=("Segoe UI", 18, "bold"),
                foreground=self.theme_manager.colors.DANGER
            ).pack(pady=50)

            ttk.Label(
                error_frame,
                text=str(error_message),
                font=("Segoe UI", 11)
            ).pack()

            self.current_page = error_frame

        except Exception as e:
            logger.error(f"Failed to show error page: {e}")

    def update_nav_buttons(self, active_page):
        """Update navigation button styles safely."""
        try:
            for page_id, button in self.nav_buttons.items():
                if page_id == active_page:
                    button.configure(style="SidebarActive.TButton")
                else:
                    button.configure(style="Sidebar.TButton")
        except Exception as e:
            logger.error(f"Failed to update nav buttons: {e}")

    def center_window(self):
        """Center the window on screen."""
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
        """Show startup error dialog."""
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
        """Run the application with error handling."""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.deiconify()
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application runtime error: {e}")
            raise

    def on_closing(self):
        """Handle application closing."""
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
        """Refresh all loaded pages safely."""
        for page_id, page in self.pages.items():
            if hasattr(page, 'refresh_data'):
                try:
                    page.refresh_data()
                except Exception as e:
                    logger.error(f"Failed to refresh page {page_id}: {e}")
