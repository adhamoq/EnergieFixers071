"""
Enhanced home page with comprehensive error handling and statistics.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HomePage(ttk.Frame):
    """Enhanced home page with robust error handling"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        try:
            from config import Colors, Theme
            self.colors = Colors
            self.theme = Theme
            
            self.setup_ui()
            self.refresh_data()
            
        except Exception as e:
            logger.error(f"Failed to initialize home page: {e}")
            self.create_error_display(e)
    
    def setup_ui(self):
        """Setup the home page UI with error handling"""
        try:
            # Configure grid
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(1, weight=1)
            
            # Create UI sections
            self.create_header()
            self.create_stats_section()
            self.create_activity_section()
            self.create_action_buttons()
            
        except Exception as e:
            logger.error(f"Failed to setup home page UI: {e}")
            self.create_simple_fallback()
    
    def create_header(self):
        """Create page header"""
        try:
            header_frame = ttk.Frame(self)
            header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
            
            # Welcome message
            welcome_label = ttk.Label(
                header_frame,
                text="Welcome to EnergieFixers071",
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 20, "bold"),
                foreground=getattr(self.colors, 'PRIMARY', '#1D8420')
            )
            welcome_label.pack(anchor="w")
            
            # Current date
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            date_label = ttk.Label(
                header_frame,
                text=current_date,
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 12),
                foreground=getattr(self.colors, 'TEXT_SECONDARY', '#6C757D')
            )
            date_label.pack(anchor="w")
            
        except Exception as e:
            logger.error(f"Failed to create header: {e}")
    
    def create_stats_section(self):
        """Create statistics cards section"""
        try:
            stats_frame = ttk.LabelFrame(self, text="Statistics Overview", padding=15)
            stats_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
            stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
            
            # Initialize stat cards
            self.stat_cards = {}
            
            # Define statistics to show
            stats_config = [
                ("volunteers", "👥 Total Volunteers", "0", getattr(self.colors, 'PRIMARY', '#1D8420')),
                ("active_volunteers", "✅ Active Volunteers", "0", getattr(self.colors, 'SUCCESS', '#28A745')),
                ("visits", "🏡 Total Visits", "0", getattr(self.colors, 'INFO', '#17A2B8')),
                ("visits_month", "📊 This Month", "0", getattr(self.colors, 'WARNING', '#FFC107'))
            ]
            
            for i, (key, title, value, color) in enumerate(stats_config):
                card = self.create_stat_card(stats_frame, title, value, color)
                card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
                self.stat_cards[key] = card
                
        except Exception as e:
            logger.error(f"Failed to create stats section: {e}")
    
    def create_stat_card(self, parent, title, value, color):
        """Create a single statistics card"""
        try:
            # Card frame
            card = ttk.Frame(parent)
            
            # Value label (large number)
            value_label = ttk.Label(
                card,
                text=value,
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 24, "bold"),
                foreground=color
            )
            value_label.pack(pady=(10, 5))
            
            # Title label
            title_label = ttk.Label(
                card,
                text=title,
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 10),
                foreground=getattr(self.colors, 'TEXT_SECONDARY', '#6C757D')
            )
            title_label.pack(pady=(0, 10))
            
            # Store reference to value label for updates
            card.value_label = value_label
            
            return card
            
        except Exception as e:
            logger.error(f"Failed to create stat card: {e}")
            return ttk.Frame(parent)  # Return empty frame as fallback
    
    def create_activity_section(self):
        """Create recent activity section"""
        try:
            # Left column - Recent Visits
            visits_frame = ttk.LabelFrame(self, text="Recent Visits", padding=10)
            visits_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
            
            # Visits listbox with scrollbar
            visits_list_frame = ttk.Frame(visits_frame)
            visits_list_frame.pack(fill=BOTH, expand=True)
            
            self.visits_listbox = tk.Listbox(
                visits_list_frame,
                height=8,
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 10),
                selectmode=tk.SINGLE
            )
            visits_scrollbar = ttk.Scrollbar(visits_list_frame, orient=VERTICAL)
            
            self.visits_listbox.config(yscrollcommand=visits_scrollbar.set)
            visits_scrollbar.config(command=self.visits_listbox.yview)
            
            self.visits_listbox.pack(side=LEFT, fill=BOTH, expand=True)
            visits_scrollbar.pack(side=RIGHT, fill=Y)
            
            # Right column - Upcoming Appointments
            appointments_frame = ttk.LabelFrame(self, text="Upcoming Appointments", padding=10)
            appointments_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0))
            
            # Appointments listbox with scrollbar
            appointments_list_frame = ttk.Frame(appointments_frame)
            appointments_list_frame.pack(fill=BOTH, expand=True)
            
            self.appointments_listbox = tk.Listbox(
                appointments_list_frame,
                height=8,
                font=(getattr(self.theme, 'FONT_FAMILY', 'Arial'), 10),
                selectmode=tk.SINGLE
            )
            appointments_scrollbar = ttk.Scrollbar(appointments_list_frame, orient=VERTICAL)
            
            self.appointments_listbox.config(yscrollcommand=appointments_scrollbar.set)
            appointments_scrollbar.config(command=self.appointments_listbox.yview)
            
            self.appointments_listbox.pack(side=LEFT, fill=BOTH, expand=True)
            appointments_scrollbar.pack(side=RIGHT, fill=Y)
            
        except Exception as e:
            logger.error(f"Failed to create activity section: {e}")
    
    def create_action_buttons(self):
        """Create quick action buttons"""
        try:
            actions_frame = ttk.Frame(self)
            actions_frame.grid(row=3, column=0, columnspan=2, pady=20)
            
            # Quick action buttons
            buttons_config = [
                ("➕ Add Volunteer", lambda: self.safe_show_page("volunteers"), SUCCESS),
                ("🔗 Generate Link", lambda: self.safe_show_page("links"), PRIMARY),
                ("📊 View Reports", self.show_reports, INFO),
                ("🔄 Sync Data", self.sync_data, WARNING)
            ]
            
            for text, command, style in buttons_config:
                ttk.Button(
                    actions_frame,
                    text=text,
                    command=command,
                    bootstyle=style,
                    width=15
                ).pack(side=LEFT, padx=5)
                
        except Exception as e:
            logger.error(f"Failed to create action buttons: {e}")
    
    def refresh_data(self):
        """Refresh dashboard data with comprehensive error handling"""
        try:
            # Get statistics with fallback
            stats = self.get_safe_stats()
            
            # Update statistics cards
            if hasattr(self, 'stat_cards'):
                for key, value in stats.items():
                    if key in self.stat_cards and hasattr(self.stat_cards[key], 'value_label'):
                        try:
                            self.stat_cards[key].value_label.config(text=str(value))
                        except Exception as e:
                            logger.error(f"Failed to update stat card {key}: {e}")
            
            # Update recent visits
            self.update_visits_list()
            
            # Update appointments
            self.update_appointments_list()
            
            logger.info("Dashboard data refreshed successfully")
            
        except Exception as e:
            logger.error(f"Failed to refresh dashboard data: {e}")
    
    def get_safe_stats(self):
        """Get statistics with safe error handling"""
        try:
            from core.models import get_volunteer_stats
            return get_volunteer_stats()
        except Exception as e:
            logger.error(f"Failed to get volunteer stats: {e}")
            return {
                "total_volunteers": 0,
                "active_volunteers": 0,
                "total_visits": 0,
                "visits_this_month": 0
            }
    
    def update_visits_list(self):
        """Update recent visits list"""
        try:
            if hasattr(self, 'visits_listbox'):
                self.visits_listbox.delete(0, tk.END)
                
                from core.models import get_recent_visits
                recent_visits = get_recent_visits(10)
                
                for visit in recent_visits:
                    try:
                        volunteer_name = visit.volunteer.name if visit.volunteer else "Unknown"
                        date_str = visit.visit_date.strftime("%m/%d") if hasattr(visit, 'visit_date') else "N/A"
                        address = getattr(visit, 'address', 'Unknown address')[:30]
                        display_text = f"{date_str} - {volunteer_name} - {address}..."
                        self.visits_listbox.insert(tk.END, display_text)
                    except Exception as e:
                        logger.error(f"Failed to format visit entry: {e}")
                        self.visits_listbox.insert(tk.END, "Visit entry error")
                        
        except Exception as e:
            logger.error(f"Failed to update visits list: {e}")
    
    def update_appointments_list(self):
        """Update upcoming appointments list"""
        try:
            if hasattr(self, 'appointments_listbox'):
                self.appointments_listbox.delete(0, tk.END)
                
                from core.models import get_upcoming_appointments
                upcoming_appointments = get_upcoming_appointments(10)
                
                for appointment in upcoming_appointments:
                    try:
                        date_str = appointment.start_time.strftime("%m/%d %H:%M") if hasattr(appointment, 'start_time') else "N/A"
                        invitee_name = getattr(appointment, 'invitee_name', 'Unknown')
                        event_name = getattr(appointment, 'event_name', 'Appointment')
                        display_text = f"{date_str} - {invitee_name} - {event_name}"
                        self.appointments_listbox.insert(tk.END, display_text)
                    except Exception as e:
                        logger.error(f"Failed to format appointment entry: {e}")
                        self.appointments_listbox.insert(tk.END, "Appointment entry error")
                        
        except Exception as e:
            logger.error(f"Failed to update appointments list: {e}")
    
    def safe_show_page(self, page_name):
        """Safely show a page"""
        try:
            if hasattr(self.app, 'show_page'):
                self.app.show_page(page_name)
            else:
                logger.error(f"Cannot navigate to {page_name}: app.show_page not available")
        except Exception as e:
            logger.error(f"Failed to show page {page_name}: {e}")
    
    def show_reports(self):
        """Show reports dialog"""
        try:
            tk.messagebox.showinfo(
                "Reports",
                "Reports feature coming soon!\n\nThis will include:\n• Energy savings summary\n• Volunteer performance\n• Monthly statistics\n• Export capabilities"
            )
        except Exception as e:
            logger.error(f"Failed to show reports dialog: {e}")
    
    def sync_data(self):
        """Trigger data synchronization"""
        try:
            tk.messagebox.showinfo(
                "Sync Data",
                "Data synchronization feature coming soon!\n\nThis will sync:\n• KoboToolbox form submissions\n• Calendly appointments\n• Volunteer information"
            )
        except Exception as e:
            logger.error(f"Failed to show sync dialog: {e}")
    
    def create_error_display(self, error):
        """Create error display for initialization failures"""
        try:
            error_label = ttk.Label(
                self,
                text=f"⚠️ Home Page Error\n\n{str(error)}",
                font=("Arial", 12),
                foreground="#DC3545"
            )
            error_label.pack(expand=True)
        except Exception:
            pass  # If even this fails, the frame will just be empty
    
    def create_simple_fallback(self):
        """Create simple fallback UI"""
        try:
            ttk.Label(
                self,
                text="EnergieFixers071 Dashboard",
                font=("Arial", 16, "bold")
            ).pack(pady=50)
            
            ttk.Label(
                self,
                text="Loading dashboard components...",
                font=("Arial", 12)
            ).pack()
        except Exception:
            pass  # If even this fails, the frame will just be empty
