"""
Enhanced volunteers management page with improved selection and visit statistics.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from core.models import Volunteer, Visit, search_volunteers
from config import Colors, Theme
import logging

logger = logging.getLogger(__name__)

class VolunteerPage(ttk.Frame):
    """Enhanced volunteers management page with proper visit statistics"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_volunteer = None
        self.colors = Colors(getattr(app, 'current_theme', 'flatly'))
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Setup the enhanced volunteers page UI"""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Header with search and actions
        self.create_header()
        
        # Main content area
        self.create_main_content()
    
    def create_header(self):
        """Create enhanced page header with search and actions"""
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Page title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="👥 Volunteer Management",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADER, "bold"),
            foreground=self.colors.PRIMARY_GREEN
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Manage your volunteer team and track their contributions",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            foreground=self.colors.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor="w")
        
        # Search frame
        search_frame = ttk.LabelFrame(header_frame, text="🔍 Search Volunteers", padding=10)
        search_frame.grid(row=0, column=1, sticky="ew", padx=(0, 20))
        search_frame.columnconfigure(0, weight=1)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_changed)
        
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            width=30
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.insert(0, "Search by name, email, or phone...")
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        
        ttk.Button(
            search_frame,
            text="✕",
            command=self.clear_search,
            width=3
        ).grid(row=0, column=1)
        
        # Action buttons (simplified - removed export and edit)
        actions_frame = ttk.Frame(header_frame)
        actions_frame.grid(row=0, column=2, sticky="e")
        
        ttk.Button(
            actions_frame,
            text="➕ Add Volunteer",
            command=self.add_volunteer,
            bootstyle=SUCCESS,
            width=15
        ).pack(pady=2)
        
        ttk.Button(
            actions_frame,
            text="🗑️ Delete",
            command=self.delete_volunteer,
            bootstyle=DANGER,
            width=15
        ).pack(pady=2)
    
    def create_main_content(self):
        """Create main content area"""
        # Left panel - Volunteer list
        self.create_volunteer_list()
        
        # Right panel - Details and statistics
        self.create_details_panel()
    
    def create_volunteer_list(self):
        """Create volunteer list with enhanced selection visibility"""
        list_frame = ttk.LabelFrame(self, text="📋 Volunteer Directory", padding=15)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Summary info
        self.summary_label = ttk.Label(
            list_frame,
            text="Loading volunteers...",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        )
        self.summary_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Scrollable frame for volunteer cards
        self.create_scrollable_volunteer_list(list_frame)
    
    def create_scrollable_volunteer_list(self, parent):
        """Create scrollable list of volunteer cards"""
        canvas_frame = ttk.Frame(parent)
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            highlightthickness=0,
            bg=self.colors.SURFACE
        )
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        self.volunteer_cards = {}
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_volunteer_card(self, volunteer):
        """Create volunteer card with enhanced selection visibility"""
        card_frame = ttk.Frame(self.scrollable_frame, relief="solid", borderwidth=2)
        card_frame.pack(fill=X, padx=5, pady=5)
        card_frame.columnconfigure(1, weight=1)
        
        # Default styling
        card_frame.configure(style="Card.TFrame")
        
        # Status indicator
        status_color = self.colors.SUCCESS if volunteer.is_active else self.colors.TEXT_MUTED
        status_canvas = tk.Canvas(card_frame, width=20, height=20, highlightthickness=0)
        status_canvas.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="n")
        status_canvas.create_oval(5, 5, 15, 15, fill=status_color, outline=status_color)
        
        # Content area
        content_frame = ttk.Frame(card_frame)
        content_frame.grid(row=0, column=1, sticky="ew", padx=(5, 10), pady=10)
        content_frame.columnconfigure(1, weight=1)
        
        # Name and status
        name_frame = ttk.Frame(content_frame)
        name_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        name_label = ttk.Label(
            name_frame,
            text=volunteer.name,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
            foreground=self.colors.TEXT_PRIMARY
        )
        name_label.pack(side=LEFT)
        
        status_label = ttk.Label(
            name_frame,
            text="🟢 Active" if volunteer.is_active else "⚪ Inactive",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=status_color
        )
        status_label.pack(side=RIGHT)
        
        # Contact info
        if volunteer.email:
            ttk.Label(
                content_frame,
                text=f"📧 {volunteer.email}",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
                foreground=self.colors.TEXT_SECONDARY
            ).grid(row=1, column=0, sticky="w")
        
        if volunteer.phone:
            ttk.Label(
                content_frame,
                text=f"📱 {volunteer.phone}",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
                foreground=self.colors.TEXT_SECONDARY
            ).grid(row=1, column=1, sticky="w")
        
        # Visit statistics (basic preview)
        visits_count = self.get_volunteer_visit_count(volunteer)
        visits_label = ttk.Label(
            content_frame,
            text=f"🏠 {visits_count} visits",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.INFO
        )
        visits_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        
        last_visit = self.get_volunteer_last_visit(volunteer)
        last_visit_text = last_visit.strftime("%d/%m/%Y") if last_visit else "Never"
        ttk.Label(
            content_frame,
            text=f"📅 Last: {last_visit_text}",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        ).grid(row=2, column=1, sticky="w", pady=(5, 0))
        
        # Bind click events
        self.bind_card_events(card_frame, volunteer)
        
        return card_frame
    
    def bind_card_events(self, card_frame, volunteer):
        """Bind click events to card with enhanced visual feedback"""
        def on_click(event):
            self.select_volunteer_card(card_frame, volunteer)
        
        def on_enter(event):
            if card_frame != getattr(self, 'selected_card', None):
                card_frame.configure(bg=self.colors.BACKGROUND)
        
        def on_leave(event):
            if card_frame != getattr(self, 'selected_card', None):
                card_frame.configure(bg=self.colors.SURFACE)
        
        # Bind events to card and all children recursively
        self.bind_events_recursive(card_frame, on_click, on_enter, on_leave)
    
    def bind_events_recursive(self, widget, on_click, on_enter, on_leave):
        """Recursively bind events to widget and all children"""
        widget.bind("<Button-1>", on_click)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
        
        for child in widget.winfo_children():
            self.bind_events_recursive(child, on_click, on_enter, on_leave)
    
    def select_volunteer_card(self, card_frame, volunteer):
        """Select volunteer card with clear visual feedback"""
        # Deselect previous card
        if hasattr(self, 'selected_card') and self.selected_card:
            self.selected_card.configure(bg=self.colors.SURFACE)
        
        # Select new card with prominent green background
        card_frame.configure(bg=self.colors.PRIMARY_GREEN)
        self.selected_card = card_frame
        self.selected_volunteer = volunteer
        
        # Update details panel
        self.populate_details(volunteer)
        
        logger.info(f"Selected volunteer: {volunteer.name}")
    
    def create_details_panel(self):
        """Create details and statistics panel"""
        details_frame = ttk.Frame(self)
        details_frame.grid(row=1, column=1, sticky="nsew")
        details_frame.rowconfigure(2, weight=1)
        
        # Enhanced statistics section
        self.create_enhanced_statistics(details_frame)
        
        # Month selector for specific month visits
        self.create_month_selector(details_frame)
        
        # Volunteer details form
        self.create_volunteer_form(details_frame)
    
    def create_enhanced_statistics(self, parent):
        """Create 5 specific statistics as requested"""
        stats_frame = ttk.LabelFrame(parent, text="📊 Volunteer Statistics", padding=15)
        stats_frame.pack(fill=X, pady=(0, 10))
        stats_frame.columnconfigure((0, 1, 2), weight=1)
        
        # Row 1: Total Visits, Last Visit, Experience
        self.total_visits_card = self.create_stat_card(stats_frame, "🏠", "Total Visits", "0", self.colors.INFO, 0, 0)
        self.last_visit_card = self.create_stat_card(stats_frame, "📅", "Last Visit", "Never", self.colors.WARNING, 0, 1)
        self.experience_card = self.create_stat_card(stats_frame, "🎯", "Experience", "Beginner", self.colors.SUCCESS, 0, 2)
        
        # Row 2: Monthly average and specific month (wider)
        self.avg_month_card = self.create_stat_card(stats_frame, "📊", "Avg Per Month", "0", self.colors.SECONDARY, 1, 0)
        self.specific_month_card = self.create_wide_stat_card(stats_frame, "📋", "Selected Month", "0", self.colors.PRIMARY, 1, 1, 2)
    
    def create_stat_card(self, parent, icon, title, value, color, row, col):
        """Create individual statistic card"""
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        ttk.Label(card, text=icon, font=(Theme.FONT_FAMILY, 20)).pack(pady=(10, 5))
        
        value_label = ttk.Label(
            card,
            text=value,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
            foreground=color
        )
        value_label.pack()
        
        ttk.Label(
            card,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        ).pack(pady=(0, 10))
        
        card.value_label = value_label
        return card
    
    def create_wide_stat_card(self, parent, icon, title, value, color, row, col, colspan):
        """Create wider statistic card for specific month"""
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        card.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="ew")
        
        ttk.Label(card, text=icon, font=(Theme.FONT_FAMILY, 20)).pack(pady=(10, 5))
        
        value_label = ttk.Label(
            card,
            text=value,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
            foreground=color
        )
        value_label.pack()
        
        ttk.Label(
            card,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        ).pack(pady=(0, 10))
        
        card.value_label = value_label
        return card
    
    def create_month_selector(self, parent):
        """Create month and year selector for specific month statistics"""
        selector_frame = ttk.LabelFrame(parent, text="📅 Select Month for Statistics", padding=10)
        selector_frame.pack(fill=X, pady=(0, 10))
        selector_frame.columnconfigure(2, weight=1)
        
        # Month selector
        ttk.Label(selector_frame, text="Month:").grid(row=0, column=0, padx=(0, 5))
        self.month_var = tk.StringVar(value=str(datetime.now().month))
        month_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.month_var,
            values=[str(i) for i in range(1, 13)],
            width=8,
            state="readonly"
        )
        month_combo.grid(row=0, column=1, padx=(0, 15))
        
        # Year selector
        ttk.Label(selector_frame, text="Year:").grid(row=0, column=2, padx=(0, 5))
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.year_var,
            values=[str(year) for year in range(2024, 2027)],
            width=8,
            state="readonly"
        )
        year_combo.grid(row=0, column=3, padx=(0, 15))
        
        # Update button
        ttk.Button(
            selector_frame,
            text="🔄 Update",
            command=self.update_monthly_stats,
            bootstyle=INFO,
            width=10
        ).grid(row=0, column=4)
        
        # Bind change events
        month_combo.bind('<<ComboboxSelected>>', lambda e: self.update_monthly_stats())
        year_combo.bind('<<ComboboxSelected>>', lambda e: self.update_monthly_stats())
    
    def create_volunteer_form(self, parent):
        """Create volunteer details form with visits section"""
        form_frame = ttk.LabelFrame(parent, text="👤 Volunteer Details", padding=15)
        form_frame.pack(fill=BOTH, expand=True)
        form_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Name field
        ttk.Label(form_frame, text="Full Name *:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
            row=row, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=1, sticky="ew", pady=8
        )
        row += 1
        
        # Email field
        ttk.Label(form_frame, text="Email:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=1, sticky="ew", pady=8
        )
        row += 1
        
        # Phone field
        ttk.Label(form_frame, text="Phone:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=1, sticky="ew", pady=8
        )
        row += 1
        
        # Skills field
        ttk.Label(form_frame, text="Skills:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=0, sticky="w", pady=8, padx=(0, 10)
        )
        self.skills_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.skills_var, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
            row=row, column=1, sticky="ew", pady=8
        )
        row += 1
        
        # Active status
        self.active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            form_frame,
            text="✅ Active Volunteer",
            variable=self.active_var,
            bootstyle="success"
        ).grid(row=row, column=1, sticky="w", pady=10)
        row += 1
        
        # Visits section
        ttk.Label(form_frame, text="Visits:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
            row=row, column=0, sticky="nw", pady=8, padx=(0, 10)
        )
        
        visits_frame = ttk.Frame(form_frame)
        visits_frame.grid(row=row, column=1, sticky="ew", pady=8)
        visits_frame.columnconfigure(0, weight=1)
        
        self.visits_label = ttk.Label(
            visits_frame,
            text="No volunteer selected",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            foreground=self.colors.TEXT_SECONDARY
        )
        self.visits_label.grid(row=0, column=0, sticky="w")
        
        self.view_visits_button = ttk.Button(
            visits_frame,
            text="👁️ View Visits",
            command=self.view_volunteer_visits,
            bootstyle=INFO,
            width=15,
            state="disabled"
        )
        self.view_visits_button.grid(row=0, column=1, padx=(10, 0))
        row += 1
        
        # Action buttons
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        self.save_button = ttk.Button(
            buttons_frame,
            text="💾 Save Volunteer",
            command=self.save_volunteer,
            bootstyle=SUCCESS,
            width=20
        )
        self.save_button.pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            bootstyle=SECONDARY,
            width=15
        ).pack(side=LEFT, padx=5)
    
    def get_volunteer_visit_count(self, volunteer):
        """Get total visit count for volunteer (uitvoerder 1 or 2)"""
        try:
            count = Visit.select().where(
                (Visit.volunteer == volunteer) | 
                (Visit.volunteer_2 == volunteer)
            ).count()
            return count
        except Exception as e:
            logger.error(f"Failed to get visit count for {volunteer.name}: {e}")
            return 0
    
    def get_volunteer_last_visit(self, volunteer):
        """Get last visit date for volunteer"""
        try:
            last_visit = Visit.select().where(
                (Visit.volunteer == volunteer) | 
                (Visit.volunteer_2 == volunteer)
            ).order_by(Visit.visit_date.desc()).first()
            return last_visit.visit_date if last_visit else None
        except Exception as e:
            logger.error(f"Failed to get last visit for {volunteer.name}: {e}")
            return None
    
    def get_volunteer_monthly_average(self, volunteer):
        """Calculate monthly average visits for volunteer"""
        try:
            visits = list(Visit.select().where(
                (Visit.volunteer == volunteer) | 
                (Visit.volunteer_2 == volunteer)
            ))
            
            if not visits:
                return 0
            
            # Calculate months between first and last visit
            first_visit = min(visit.visit_date for visit in visits)
            last_visit = max(visit.visit_date for visit in visits)
            
            months_diff = ((last_visit.year - first_visit.year) * 12 + 
                          last_visit.month - first_visit.month) + 1
            
            return round(len(visits) / max(months_diff, 1), 1)
        except Exception as e:
            logger.error(f"Failed to calculate monthly average for {volunteer.name}: {e}")
            return 0
    
    def get_volunteer_experience_level(self, visit_count):
        """Calculate experience level based on visit count"""
        if visit_count >= 15:
            return "Experienced"
        elif visit_count >= 5:
            return "Intermediate"
        else:
            return "Beginner"
    
    def get_volunteer_monthly_visits(self, volunteer, month, year):
        """Get visits for specific month and year"""
        try:
            count = Visit.select().where(
                ((Visit.volunteer == volunteer) | (Visit.volunteer_2 == volunteer)) &
                (Visit.visit_date.month == month) &
                (Visit.visit_date.year == year)
            ).count()
            return count
        except Exception as e:
            logger.error(f"Failed to get monthly visits for {volunteer.name}: {e}")
            return 0
    
    def populate_details(self, volunteer):
        """Populate details panel with volunteer information"""
        try:
            # Clear form
            self.clear_form()
            
            # Set form values
            self.name_var.set(volunteer.name)
            self.email_var.set(volunteer.email or "")
            self.phone_var.set(volunteer.phone or "")
            self.skills_var.set(volunteer.skills or "")
            self.active_var.set(volunteer.is_active)
            
            # Update statistics
            self.update_volunteer_statistics(volunteer)
            
            # Update visits section
            visit_count = self.get_volunteer_visit_count(volunteer)
            self.visits_label.config(text=f"This volunteer has participated in {visit_count} visits")
            self.view_visits_button.config(state="normal")
            
            # Update save button
            self.save_button.config(text="💾 Update Volunteer")
            
        except Exception as e:
            logger.error(f"Failed to populate volunteer details: {e}")
    
    def update_volunteer_statistics(self, volunteer):
        """Update the 5 specific statistics"""
        try:
            # Total visits
            total_visits = self.get_volunteer_visit_count(volunteer)
            self.total_visits_card.value_label.config(text=str(total_visits))
            
            # Last visit
            last_visit = self.get_volunteer_last_visit(volunteer)
            last_visit_str = last_visit.strftime("%d/%m/%Y") if last_visit else "Never"
            self.last_visit_card.value_label.config(text=last_visit_str)
            
            # Experience level
            experience = self.get_volunteer_experience_level(total_visits)
            self.experience_card.value_label.config(text=experience)
            
            # Monthly average
            avg_monthly = self.get_volunteer_monthly_average(volunteer)
            self.avg_month_card.value_label.config(text=str(avg_monthly))
            
            # Update monthly stats
            self.update_monthly_stats()
            
        except Exception as e:
            logger.error(f"Failed to update statistics: {e}")
    
    def update_monthly_stats(self):
        """Update specific month statistics"""
        if not self.selected_volunteer:
            self.specific_month_card.value_label.config(text="0")
            return
        
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
            monthly_visits = self.get_volunteer_monthly_visits(self.selected_volunteer, month, year)
            self.specific_month_card.value_label.config(text=str(monthly_visits))
        except Exception as e:
            logger.error(f"Failed to update monthly stats: {e}")
            self.specific_month_card.value_label.config(text="0")
    
    def clear_form(self):
        """Clear the volunteer form"""
        self.selected_volunteer = None
        
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.skills_var.set("")
        self.active_var.set(True)
        
        # Reset statistics
        if hasattr(self, 'total_visits_card'):
            self.total_visits_card.value_label.config(text="0")
            self.last_visit_card.value_label.config(text="Never")
            self.experience_card.value_label.config(text="Beginner")
            self.avg_month_card.value_label.config(text="0")
            self.specific_month_card.value_label.config(text="0")
        
        # Reset visits section
        self.visits_label.config(text="No volunteer selected")
        self.view_visits_button.config(state="disabled")
        
        self.save_button.config(text="💾 Save Volunteer")
        
        # Clear selection
        if hasattr(self, 'selected_card') and self.selected_card:
            self.selected_card.configure(bg=self.colors.SURFACE)
            self.selected_card = None
    
    def save_volunteer(self):
        """Save volunteer data"""
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Name is required.")
            return
        
        try:
            volunteer_data = {
                'name': self.name_var.get().strip(),
                'email': self.email_var.get().strip() or None,
                'phone': self.phone_var.get().strip() or None,
                'skills': self.skills_var.get().strip() or None,
                'is_active': self.active_var.get()
            }
            
            if self.selected_volunteer:
                # Update existing
                for key, value in volunteer_data.items():
                    setattr(self.selected_volunteer, key, value)
                self.selected_volunteer.save()
                logger.info(f"Updated volunteer: {self.selected_volunteer.name}")
                messagebox.showinfo("Success", "Volunteer updated successfully!")
            else:
                # Create new
                volunteer = Volunteer.create(**volunteer_data)
                self.selected_volunteer = volunteer
                logger.info(f"Created new volunteer: {volunteer.name}")
                messagebox.showinfo("Success", "Volunteer created successfully!")
            
            self.refresh_data()
            
        except Exception as e:
            logger.error(f"Failed to save volunteer: {e}")
            messagebox.showerror("Error", f"Failed to save volunteer: {e}")
    
    def add_volunteer(self):
        """Add new volunteer"""
        self.clear_form()
    
    def delete_volunteer(self):
        """Delete selected volunteer with proper error handling"""
        if not self.selected_volunteer:
            messagebox.showwarning("No Selection", "Please select a volunteer to delete.")
            return
        
        # Check if volunteer has visits
        visit_count = self.get_volunteer_visit_count(self.selected_volunteer)
        if visit_count > 0:
            if not messagebox.askyesno(
                "Confirm Delete", 
                f"Volunteer '{self.selected_volunteer.name}' has {visit_count} associated visits.\n\nDeleting the volunteer will remove all visit associations. Continue?"
            ):
                return
        
        if messagebox.askyesno("Confirm Delete", f"Delete volunteer '{self.selected_volunteer.name}'?\n\nThis cannot be undone."):
            try:
                name = self.selected_volunteer.name
                
                # Remove volunteer associations from visits
                Visit.update(volunteer=None).where(Visit.volunteer == self.selected_volunteer).execute()
                Visit.update(volunteer_2=None).where(Visit.volunteer_2 == self.selected_volunteer).execute()
                
                # Delete volunteer
                self.selected_volunteer.delete_instance()
                
                logger.info(f"Deleted volunteer: {name}")
                messagebox.showinfo("Success", f"Volunteer '{name}' deleted successfully.")
                self.clear_form()
                self.refresh_data()
                
            except Exception as e:
                logger.error(f"Failed to delete volunteer: {e}")
                messagebox.showerror("Error", f"Failed to delete volunteer: {e}")
    
    def view_volunteer_visits(self):
        """Show popup with volunteer's visits"""
        if not self.selected_volunteer:
            return
        
        try:
            # Get all visits for this volunteer
            visits = list(Visit.select().where(
                (Visit.volunteer == self.selected_volunteer) | 
                (Visit.volunteer_2 == self.selected_volunteer)
            ).order_by(Visit.visit_date.desc()))
            
            if not visits:
                messagebox.showinfo("No Visits", f"{self.selected_volunteer.name} has no recorded visits.")
                return
            
            # Create popup window
            popup = tk.Toplevel(self)
            popup.title(f"Visits by {self.selected_volunteer.name}")
            popup.geometry("800x600")
            popup.transient(self)
            popup.grab_set()
            
            # Center popup
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() - popup.winfo_width()) // 2
            y = (popup.winfo_screenheight() - popup.winfo_height()) // 2
            popup.geometry(f"+{x}+{y}")
            
            # Header
            header_frame = ttk.Frame(popup)
            header_frame.pack(fill=X, padx=20, pady=20)
            
            ttk.Label(
                header_frame,
                text=f"Visits by {self.selected_volunteer.name}",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
                foreground=self.colors.PRIMARY_GREEN
            ).pack()
            
            ttk.Label(
                header_frame,
                text=f"Total: {len(visits)} visits",
                font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
                foreground=self.colors.TEXT_SECONDARY
            ).pack()
            
            # Visits list
            list_frame = ttk.Frame(popup)
            list_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
            
            # Create treeview for visits
            columns = ("Date", "Address", "Role", "Residents", "Status")
            tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)
            
            # Scrollbar
            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            tree.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)
            
            # Populate visits
            for visit in visits:
                role = "Primary" if visit.volunteer == self.selected_volunteer else "Secondary"
                tree.insert("", "end", values=(
                    visit.visit_date.strftime("%d/%m/%Y"),
                    visit.address[:40] + "..." if len(visit.address) > 40 else visit.address,
                    role,
                    visit.residents_count,
                    visit.status.title()
                ))
            
            # Close button
            ttk.Button(
                popup,
                text="Close",
                command=popup.destroy,
                bootstyle=SECONDARY,
                width=15
            ).pack(pady=(0, 20))
            
        except Exception as e:
            logger.error(f"Failed to show volunteer visits: {e}")
            messagebox.showerror("Error", f"Failed to load visits: {e}")
    
    def refresh_data(self):
        """Refresh volunteer list"""
        try:
            # Clear existing cards
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self.volunteer_cards.clear()
            
            # Load volunteers
            volunteers = list(Volunteer.select().order_by(Volunteer.name))
            
            # Update summary
            active_count = sum(1 for v in volunteers if v.is_active)
            self.summary_label.config(
                text=f"📊 {len(volunteers)} total volunteers • {active_count} active • {len(volunteers) - active_count} inactive"
            )
            
            # Create volunteer cards
            for volunteer in volunteers:
                card = self.create_volunteer_card(volunteer)
                self.volunteer_cards[volunteer.id] = card
            
            # Update canvas
            self.scrollable_frame.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            logger.info(f"Loaded {len(volunteers)} volunteers")
            
        except Exception as e:
            logger.error(f"Failed to refresh volunteer data: {e}")
            messagebox.showerror("Error", f"Failed to load volunteers: {e}")
    
    def on_search_changed(self, *args):
        """Handle search input changes"""
        query = self.search_var.get().strip()
        
        if not query or query == "Search by name, email, or phone...":
            self.refresh_data()
            return
        
        try:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            volunteers = search_volunteers(query)
            self.summary_label.config(text=f"🔍 Found {len(volunteers)} volunteers matching '{query}'")
            
            for volunteer in volunteers:
                self.create_volunteer_card(volunteer)
                
        except Exception as e:
            logger.error(f"Search failed: {e}")
    
    def on_search_focus_in(self, event):
        """Handle search field focus in"""
        if event.widget.get() == "Search by name, email, or phone...":
            event.widget.delete(0, tk.END)
    
    def on_search_focus_out(self, event):
        """Handle search field focus out"""
        if not event.widget.get().strip():
            event.widget.insert(0, "Search by name, email, or phone...")
    
    def clear_search(self):
        """Clear search and refresh"""
        self.search_var.set("")
        self.refresh_data()
    
    def refresh_styling(self):
        """Refresh styling when theme changes"""
        self.colors = Colors(getattr(self.app, 'current_theme', 'flatly'))
        self.refresh_data()
