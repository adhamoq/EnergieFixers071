"""
Visits management page with detailed popups and comprehensive visit data display.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from core.models import Visit, Volunteer
from config import Colors, Theme
import logging

logger = logging.getLogger(__name__)

class VisitsPage(ttk.Frame):
    """Comprehensive visits management page with detailed popups"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_visit = None
        self.colors = Colors(getattr(app, 'current_theme', 'flatly'))
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Setup the visits page UI"""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Header with filters and actions
        self.create_header()
        
        # Main visits table
        self.create_visits_table()
    
    def create_header(self):
        """Create page header with filters and statistics"""
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # Page title
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="🏠 Energy Visits Management",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_HEADER, "bold"),
            foreground=self.colors.PRIMARY_GREEN
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Track and manage energy assessment visits",
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            foreground=self.colors.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor="w")
        
        # Statistics cards
        stats_frame = ttk.Frame(header_frame)
        stats_frame.grid(row=0, column=1, sticky="ew")
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        # Get visit statistics
        total_visits = Visit.select().count()
        this_month_visits = Visit.select().where(
            (Visit.visit_date.month == datetime.now().month) &
            (Visit.visit_date.year == datetime.now().year)
        ).count()
        visits_with_issues = Visit.select().where(
            (Visit.mold_issues == True) | 
            (Visit.moisture_issues == True) | 
            (Visit.draft_issues == True)
        ).count()
        avg_residents = Visit.select().avg(Visit.residents_count) or 0
        
        self.create_stat_card(stats_frame, "🏠", "Total Visits", str(total_visits), self.colors.INFO, 0)
        self.create_stat_card(stats_frame, "📅", "This Month", str(this_month_visits), self.colors.SUCCESS, 1)
        self.create_stat_card(stats_frame, "⚠️", "With Issues", str(visits_with_issues), self.colors.WARNING, 2)
        self.create_stat_card(stats_frame, "👥", "Avg Residents", f"{avg_residents:.1f}", self.colors.SECONDARY, 3)
        
        # Filters
        self.create_filters(header_frame)
    
    def create_stat_card(self, parent, icon, title, value, color, col):
        """Create statistic card"""
        card = ttk.Frame(parent, relief="solid", borderwidth=1)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        
        ttk.Label(card, text=icon, font=(Theme.FONT_FAMILY, 16)).pack(pady=(5, 0))
        ttk.Label(
            card,
            text=value,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
            foreground=color
        ).pack()
        ttk.Label(
            card,
            text=title,
            font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
            foreground=self.colors.TEXT_SECONDARY
        ).pack(pady=(0, 5))
    
    def create_filters(self, parent):
        """Create filter controls"""
        filters_frame = ttk.LabelFrame(parent, text="🔍 Filters", padding=10)
        filters_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        filters_frame.columnconfigure((1, 3, 5), weight=1)
        
        # Date range filter
        ttk.Label(filters_frame, text="From Date:").grid(row=0, column=0, padx=(0, 5))
        self.from_date_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.from_date_var, width=12).grid(row=0, column=1, padx=(0, 15))
        
        ttk.Label(filters_frame, text="To Date:").grid(row=0, column=2, padx=(0, 5))
        self.to_date_var = tk.StringVar()
        ttk.Entry(filters_frame, textvariable=self.to_date_var, width=12).grid(row=0, column=3, padx=(0, 15))
        
        # Volunteer filter
        ttk.Label(filters_frame, text="Volunteer:").grid(row=0, column=4, padx=(0, 5))
        self.volunteer_var = tk.StringVar()
        volunteer_combo = ttk.Combobox(filters_frame, textvariable=self.volunteer_var, width=20)
        volunteer_combo.grid(row=0, column=5, padx=(0, 15))
        
        # Populate volunteer filter
        volunteers = list(Volunteer.select().order_by(Volunteer.name))
        volunteer_names = ["All Volunteers"] + [v.name for v in volunteers]
        volunteer_combo['values'] = volunteer_names
        volunteer_combo.set("All Volunteers")
        
        # Filter buttons
        ttk.Button(
            filters_frame,
            text="🔍 Apply Filter",
            command=self.apply_filters,
            bootstyle=INFO,
            width=12
        ).grid(row=0, column=6, padx=5)
        
        ttk.Button(
            filters_frame,
            text="🔄 Clear",
            command=self.clear_filters,
            bootstyle=SECONDARY,
            width=10
        ).grid(row=0, column=7, padx=5)
    
    def create_visits_table(self):
        """Create the main visits table"""
        table_frame = ttk.LabelFrame(self, text="📋 Visit Records", padding=15)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ("Date", "Address", "Primary Volunteer", "Secondary Volunteer", "Residents", "Issues", "Status")
        self.visits_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        column_widths = {"Date": 100, "Address": 200, "Primary Volunteer": 150, "Secondary Volunteer": 150, 
                        "Residents": 80, "Issues": 100, "Status": 100}
        
        for col in columns:
            self.visits_tree.heading(col, text=col)
            self.visits_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.visits_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.visits_tree.xview)
        self.visits_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.visits_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind double-click event
        self.visits_tree.bind("<Double-1>", self.on_visit_double_click)
        
        # Action buttons
        actions_frame = ttk.Frame(table_frame)
        actions_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(
            actions_frame,
            text="👁️ View Details",
            command=self.view_visit_details,
            bootstyle=INFO,
            width=15
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            actions_frame,
            text="📊 Export",
            command=self.export_visits,
            bootstyle=SUCCESS,
            width=15
        ).pack(side=LEFT, padx=5)
    
    def refresh_data(self):
        """Refresh visits table data"""
        try:
            # Clear existing items
            for item in self.visits_tree.get_children():
                self.visits_tree.delete(item)
            
            # Load visits
            visits = list(Visit.select().order_by(Visit.visit_date.desc()))
            
            # Populate table
            for visit in visits:
                primary_volunteer = visit.volunteer.name if visit.volunteer else "Unknown"
                secondary_volunteer = visit.volunteer_2.name if visit.volunteer_2 else "None"
                
                # Determine issues
                issues = []
                if visit.mold_issues:
                    issues.append("Mold")
                if visit.moisture_issues:
                    issues.append("Moisture")
                if visit.draft_issues:
                    issues.append("Draft")
                issues_text = ", ".join(issues) if issues else "None"
                
                self.visits_tree.insert("", "end", iid=visit.id, values=(
                    visit.visit_date.strftime("%d/%m/%Y"),
                    visit.address[:35] + "..." if len(visit.address) > 35 else visit.address,
                    primary_volunteer,
                    secondary_volunteer,
                    visit.residents_count,
                    issues_text,
                    visit.status.title()
                ))
            
            logger.info(f"Loaded {len(visits)} visits")
            
        except Exception as e:
            logger.error(f"Failed to refresh visits data: {e}")
            messagebox.showerror("Error", f"Failed to load visits: {e}")
    
    def on_visit_double_click(self, event):
        """Handle double-click on visit"""
        self.view_visit_details()
    
    def view_visit_details(self):
        """Show detailed visit popup"""
        selection = self.visits_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a visit to view details.")
            return
        
        visit_id = selection[0]
        try:
            visit = Visit.get_by_id(visit_id)
            self.show_visit_detail_popup(visit)
        except Exception as e:
            logger.error(f"Failed to load visit details: {e}")
            messagebox.showerror("Error", f"Failed to load visit details: {e}")
    
    def show_visit_detail_popup(self, visit):
        """Show comprehensive visit details in popup"""
        popup = tk.Toplevel(self)
        popup.title(f"Visit Details - {visit.address}")
        popup.geometry("900x700")
        popup.transient(self)
        popup.grab_set()
        
        # Center popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() - popup.winfo_width()) // 2
        y = (popup.winfo_screenheight() - popup.winfo_height()) // 2
        popup.geometry(f"+{x}+{y}")
        
        # Create notebook for organized sections
        notebook = ttk.Notebook(popup)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Basic Information Tab
        self.create_basic_info_tab(notebook, visit)
        
        # Energy Assessment Tab
        self.create_energy_tab(notebook, visit)
        
        # Materials & Interventions Tab
        self.create_materials_tab(notebook, visit)
        
        # Problems & Issues Tab
        self.create_problems_tab(notebook, visit)
        
        # Community Building Tab
        self.create_community_tab(notebook, visit)
        
        # Close button
        ttk.Button(
            popup,
            text="Close",
            command=popup.destroy,
            bootstyle=SECONDARY,
            width=15
        ).pack(pady=(0, 20))
    
    def create_basic_info_tab(self, notebook, visit):
        """Create basic information tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📋 Basic Info")
        
        # Create scrollable frame
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Basic information
        info_frame = ttk.LabelFrame(scrollable_frame, text="Visit Information", padding=15)
        info_frame.pack(fill=X, padx=10, pady=10)
        
        basic_info = [
            ("Visit Date:", visit.visit_date.strftime("%d/%m/%Y")),
            ("Address:", visit.address),
            ("Appointment Time:", visit.appointment_time or "Not specified"),
            ("Primary Volunteer:", visit.volunteer.name if visit.volunteer else "Not assigned"),
            ("Secondary Volunteer:", visit.volunteer_2.name if visit.volunteer_2 else "None"),
            ("Number of Residents:", str(visit.residents_count)),
            ("Status:", visit.status.title()),
        ]
        
        for i, (label, value) in enumerate(basic_info):
            ttk.Label(info_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=5, padx=(0, 10)
            )
            ttk.Label(info_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=5
            )
        
        # Contact information
        if visit.resident_email:
            contact_frame = ttk.LabelFrame(scrollable_frame, text="Contact Information", padding=15)
            contact_frame.pack(fill=X, padx=10, pady=10)
            
            ttk.Label(contact_frame, text="Resident Email:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=0, column=0, sticky="w", pady=5, padx=(0, 10)
            )
            ttk.Label(contact_frame, text=visit.resident_email, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=0, column=1, sticky="w", pady=5
            )
        
        # Notes
        if visit.other_remarks:
            notes_frame = ttk.LabelFrame(scrollable_frame, text="Additional Remarks", padding=15)
            notes_frame.pack(fill=X, padx=10, pady=10)
            
            text_widget = tk.Text(notes_frame, height=4, wrap=tk.WORD, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL))
            text_widget.pack(fill=X)
            text_widget.insert("1.0", visit.other_remarks)
            text_widget.config(state="disabled")
    
    def create_energy_tab(self, notebook, visit):
        """Create energy assessment tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚡ Energy Assessment")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Energy measures taken
        measures_frame = ttk.LabelFrame(scrollable_frame, text="Existing Energy Measures", padding=15)
        measures_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(measures_frame, text="Energy measures already taken:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).pack(anchor="w")
        ttk.Label(measures_frame, text="Yes" if visit.energy_measures_taken else "No", 
                 foreground=self.colors.SUCCESS if visit.energy_measures_taken else self.colors.DANGER).pack(anchor="w", pady=(0, 5))
        
        if visit.which_measures:
            ttk.Label(measures_frame, text="Which measures:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).pack(anchor="w")
            ttk.Label(measures_frame, text=visit.which_measures).pack(anchor="w")
        
        # Energy contract information
        contract_frame = ttk.LabelFrame(scrollable_frame, text="Energy Contract", padding=15)
        contract_frame.pack(fill=X, padx=10, pady=10)
        
        contract_info = [
            ("Contract Duration:", visit.contract_duration or "Not specified"),
            ("Electricity Consumption (kWh/year):", str(visit.electricity_consumption) if visit.electricity_consumption else "Not recorded"),
            ("Gas Consumption (m³/year):", str(visit.gas_consumption) if visit.gas_consumption else "Not recorded"),
            ("Monthly Amount (€):", f"€{visit.monthly_amount}" if visit.monthly_amount else "Not recorded"),
            ("Energy Bill Concerns:", "Yes" if visit.energy_bill_concerns else "No"),
        ]
        
        for i, (label, value) in enumerate(contract_info):
            ttk.Label(contract_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(contract_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
        
        # Heating system
        heating_frame = ttk.LabelFrame(scrollable_frame, text="Heating System (CV)", padding=15)
        heating_frame.pack(fill=X, padx=10, pady=10)
        
        heating_info = [
            ("Current CV Temperature:", f"{visit.current_cv_temperature}°C" if visit.current_cv_temperature else "Not recorded"),
            ("Lowered to:", f"{visit.cv_temperature_lowered_to}°C" if visit.cv_temperature_lowered_to else "Not changed"),
            ("Water Pressure Under 1 Bar:", "Yes" if visit.cv_water_pressure_under_1_bar else "No"),
            ("Tap Comfort Off:", "Yes" if visit.tap_comfort_off else "No"),
        ]
        
        for i, (label, value) in enumerate(heating_info):
            ttk.Label(heating_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(heating_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
    
    def create_materials_tab(self, notebook, visit):
        """Create materials and interventions tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🔧 Materials & Work")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Insulation materials
        insulation_frame = ttk.LabelFrame(scrollable_frame, text="Insulation & Draft Sealing", padding=15)
        insulation_frame.pack(fill=X, padx=10, pady=10)
        
        insulation_info = [
            ("Radiator Foil (meters):", str(visit.radiator_foil_meters) if visit.radiator_foil_meters else "0"),
            ("Radiator Fan Needed:", "Yes" if visit.radiator_fan_needed else "No"),
            ("Draft Strip (meters):", str(visit.draft_strip_meters) if visit.draft_strip_meters else "0"),
            ("Door Draft Band:", "Yes" if visit.door_draft_band else "No"),
            ("Door Closers:", "Yes" if visit.door_closers else "No"),
            ("Door Closer Spring:", "Yes" if visit.door_closer_spring else "No"),
        ]
        
        for i, (label, value) in enumerate(insulation_info):
            ttk.Label(insulation_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(insulation_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
        
        # Lighting and electrical
        electrical_frame = ttk.LabelFrame(scrollable_frame, text="Lighting & Electrical", padding=15)
        electrical_frame.pack(fill=X, padx=10, pady=10)
        
        electrical_info = [
            ("LED Lamps Needed:", "Yes" if visit.led_lamps_needed else "No"),
            ("E14 LEDs Count:", str(visit.e14_leds_count) if visit.e14_leds_count else "0"),
            ("E27 LEDs Count:", str(visit.e27_leds_count) if visit.e27_leds_count else "0"),
            ("Small Power Strip Needed:", "Yes" if visit.small_power_strip_needed else "No"),
            ("Large Power Strip Needed:", "Yes" if visit.large_power_strip_needed else "No"),
        ]
        
        for i, (label, value) in enumerate(electrical_info):
            ttk.Label(electrical_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(electrical_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
        
        # Bathroom equipment
        bathroom_frame = ttk.LabelFrame(scrollable_frame, text="Bathroom Equipment", padding=15)
        bathroom_frame.pack(fill=X, padx=10, pady=10)
        
        bathroom_info = [
            ("Shower Timer:", "Yes" if visit.shower_timer else "No"),
            ("Shower Head:", "Yes" if visit.shower_head else "No"),
        ]
        
        for i, (label, value) in enumerate(bathroom_info):
            ttk.Label(bathroom_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(bathroom_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
    
    def create_problems_tab(self, notebook, visit):
        """Create problems and issues tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚠️ Issues & Problems")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Problems identified
        problems_frame = ttk.LabelFrame(scrollable_frame, text="Problems Identified", padding=15)
        problems_frame.pack(fill=X, padx=10, pady=10)
        
        issues = []
        if visit.mold_issues:
            issues.append("🟢 Mold Issues")
        if visit.moisture_issues:
            issues.append("🟢 Moisture Issues")
        if visit.draft_issues:
            issues.append("🟢 Draft Issues")
        
        if issues:
            for issue in issues:
                ttk.Label(problems_frame, text=issue, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).pack(anchor="w", pady=2)
        else:
            ttk.Label(problems_frame, text="No specific issues identified", 
                     foreground=self.colors.SUCCESS, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).pack(anchor="w")
        
        if visit.problem_rooms_description:
            ttk.Label(problems_frame, text="Affected Rooms:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).pack(anchor="w", pady=(10, 0))
            ttk.Label(problems_frame, text=visit.problem_rooms_description, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).pack(anchor="w")
        
        if visit.problems_with:
            ttk.Label(problems_frame, text="Additional Problems:", font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).pack(anchor="w", pady=(10, 0))
            ttk.Label(problems_frame, text=visit.problems_with, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).pack(anchor="w")
        
        # Equipment needed
        equipment_frame = ttk.LabelFrame(scrollable_frame, text="Additional Equipment Needed", padding=15)
        equipment_frame.pack(fill=X, padx=10, pady=10)
        
        equipment_info = [
            ("Hygrometer Needed:", "Yes" if visit.hygrometer_needed else "No"),
            ("Old Refrigerator Present:", "Yes" if visit.old_refrigerator else "No"),
        ]
        
        for i, (label, value) in enumerate(equipment_info):
            ttk.Label(equipment_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            ttk.Label(equipment_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL)).grid(
                row=i, column=1, sticky="w", pady=3
            )
    
    def create_community_tab(self, notebook, visit):
        """Create community building tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🤝 Community")
        
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Community engagement
        community_frame = ttk.LabelFrame(scrollable_frame, text="Community Engagement", padding=15)
        community_frame.pack(fill=X, padx=10, pady=10)
        
        community_info = [
            ("Knows Potential Fixers:", "Yes" if visit.knows_potential_fixers else "No"),
            ("Wants to Help:", "Yes" if visit.wants_to_help else "No"),
            ("Will Tell Neighbors:", "Yes" if visit.tell_neighbors else "No"),
        ]
        
        for i, (label, value) in enumerate(community_info):
            ttk.Label(community_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            color = self.colors.SUCCESS if "Yes" in value else self.colors.TEXT_SECONDARY
            ttk.Label(community_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL), foreground=color).grid(
                row=i, column=1, sticky="w", pady=3
            )
        
        # Information sharing
        sharing_frame = ttk.LabelFrame(scrollable_frame, text="Information Sharing", padding=15)
        sharing_frame.pack(fill=X, padx=10, pady=10)
        
        sharing_info = [
            ("Share with Housing Corp:", "Yes" if visit.share_info_with_housing_corp else "No"),
            ("Keep Updated on Results:", "Yes" if visit.keep_updated_on_results else "No"),
        ]
        
        for i, (label, value) in enumerate(sharing_info):
            ttk.Label(sharing_frame, text=label, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold")).grid(
                row=i, column=0, sticky="w", pady=3, padx=(0, 10)
            )
            color = self.colors.SUCCESS if "Yes" in value else self.colors.TEXT_SECONDARY
            ttk.Label(sharing_frame, text=value, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL), foreground=color).grid(
                row=i, column=1, sticky="w", pady=3
            )
        
        if visit.community_building:
            community_text_frame = ttk.LabelFrame(scrollable_frame, text="Community Building Notes", padding=15)
            community_text_frame.pack(fill=X, padx=10, pady=10)
            
            text_widget = tk.Text(community_text_frame, height=4, wrap=tk.WORD, font=(Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL))
            text_widget.pack(fill=X)
            text_widget.insert("1.0", visit.community_building)
            text_widget.config(state="disabled")
    
    def apply_filters(self):
        """Apply filters to visits table"""
        try:
            # Clear existing items
            for item in self.visits_tree.get_children():
                self.visits_tree.delete(item)
            
            # Build query with filters
            query = Visit.select()
            
            # Date range filter
            if self.from_date_var.get():
                try:
                    from_date = datetime.strptime(self.from_date_var.get(), "%Y-%m-%d").date()
                    query = query.where(Visit.visit_date >= from_date)
                except ValueError:
                    messagebox.showerror("Invalid Date", "From date format should be YYYY-MM-DD")
                    return
            
            if self.to_date_var.get():
                try:
                    to_date = datetime.strptime(self.to_date_var.get(), "%Y-%m-%d").date()
                    query = query.where(Visit.visit_date <= to_date)
                except ValueError:
                    messagebox.showerror("Invalid Date", "To date format should be YYYY-MM-DD")
                    return
            
            # Volunteer filter
            if self.volunteer_var.get() and self.volunteer_var.get() != "All Volunteers":
                volunteer_name = self.volunteer_var.get()
                volunteer = Volunteer.select().where(Volunteer.name == volunteer_name).first()
                if volunteer:
                    query = query.where(
                        (Visit.volunteer == volunteer) | 
                        (Visit.volunteer_2 == volunteer)
                    )
            
            # Execute query and populate table
            visits = list(query.order_by(Visit.visit_date.desc()))
            
            for visit in visits:
                primary_volunteer = visit.volunteer.name if visit.volunteer else "Unknown"
                secondary_volunteer = visit.volunteer_2.name if visit.volunteer_2 else "None"
                
                issues = []
                if visit.mold_issues:
                    issues.append("Mold")
                if visit.moisture_issues:
                    issues.append("Moisture")
                if visit.draft_issues:
                    issues.append("Draft")
                issues_text = ", ".join(issues) if issues else "None"
                
                self.visits_tree.insert("", "end", iid=visit.id, values=(
                    visit.visit_date.strftime("%d/%m/%Y"),
                    visit.address[:35] + "..." if len(visit.address) > 35 else visit.address,
                    primary_volunteer,
                    secondary_volunteer,
                    visit.residents_count,
                    issues_text,
                    visit.status.title()
                ))
            
            logger.info(f"Applied filters, showing {len(visits)} visits")
            
        except Exception as e:
            logger.error(f"Failed to apply filters: {e}")
            messagebox.showerror("Error", f"Failed to apply filters: {e}")
    
    def clear_filters(self):
        """Clear all filters and refresh data"""
        self.from_date_var.set("")
        self.to_date_var.set("")
        self.volunteer_var.set("All Volunteers")
        self.refresh_data()
    
    def export_visits(self):
        """Export visits to CSV (placeholder)"""
        messagebox.showinfo("Export", "Export functionality will be implemented soon!")
    
    def refresh_styling(self):
        """Refresh styling when theme changes"""
        self.colors = Colors(getattr(self.app, 'current_theme', 'flatly'))
        self.refresh_data()
