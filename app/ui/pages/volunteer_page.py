"""
Volunteers management page for CRUD operations on volunteer data.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from datetime import date
from core.models import Volunteer, search_volunteers
from config import Colors
import logging

logger = logging.getLogger(__name__)

class VolunteerPage(ttk.Frame):
    """Volunteers management page"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_volunteer = None
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Setup the volunteers page UI"""
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        
        # Header with search and actions
        self.create_header()
        
        # Left panel - Volunteer list
        self.create_volunteer_list()
        
        # Right panel - Volunteer details/form
        self.create_volunteer_form()
    
    def create_header(self):
        """Create page header with search and actions"""
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Page title
        title_label = ttk.Label(
            header_frame,
            text="Volunteer Management",
            font=("Helvetica", 18, "bold"),
            foreground=Colors.PRIMARY_GREEN
        )
        title_label.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Search frame
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=0, column=1, sticky="ew", padx=(0, 20))
        search_frame.columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_changed)
        
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Helvetica", 11),
            width=30
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        search_entry.insert(0, "Search volunteers...")
        search_entry.bind("<FocusIn>", self.on_search_focus_in)
        search_entry.bind("<FocusOut>", self.on_search_focus_out)
        
        # Action buttons
        actions_frame = ttk.Frame(header_frame)
        actions_frame.grid(row=0, column=2, sticky="e")
        
        ttk.Button(
            actions_frame,
            text="➕ Add Volunteer",
            command=self.add_volunteer,
            bootstyle=SUCCESS,
            width=15
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            actions_frame,
            text="✏️ Edit",
            command=self.edit_volunteer,
            bootstyle=PRIMARY,
            width=10
        ).pack(side=LEFT, padx=2)
        
        ttk.Button(
            actions_frame,
            text="🗑️ Delete",
            command=self.delete_volunteer,
            bootstyle=DANGER,
            width=10
        ).pack(side=LEFT, padx=2)
    
    def create_volunteer_list(self):
        """Create volunteer list panel"""
        # Left panel frame
        list_frame = ttk.LabelFrame(self, text="Volunteers", padding=10)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview for volunteer list
        columns = ("Name", "Phone", "Email", "Visits", "Last Visit")
        self.volunteer_tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Configure columns
        column_widths = {"Name": 120, "Phone": 100, "Email": 150, "Visits": 60, "Last Visit": 100}
        for col in columns:
            self.volunteer_tree.heading(col, text=col)
            self.volunteer_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.volunteer_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=HORIZONTAL, command=self.volunteer_tree.xview)
        
        self.volunteer_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.volunteer_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind selection event
        self.volunteer_tree.bind("<<TreeviewSelect>>", self.on_volunteer_select)
    
    def create_volunteer_form(self):
        """Create volunteer details/form panel"""
        # Right panel frame
        form_frame = ttk.LabelFrame(self, text="Volunteer Details", padding=15)
        form_frame.grid(row=1, column=1, sticky="nsew")
        form_frame.columnconfigure(1, weight=1)
        
        # Form fields
        row = 0
        
        # Name
        ttk.Label(form_frame, text="Name *:").grid(row=row, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.name_var, width=30).grid(
            row=row, column=1, sticky="ew", padx=(10, 0), pady=5
        )
        row += 1
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=row, column=0, sticky="w", pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.phone_var, width=30).grid(
            row=row, column=1, sticky="ew", padx=(10, 0), pady=5
        )
        row += 1
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=row, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).grid(
            row=row, column=1, sticky="ew", padx=(10, 0), pady=5
        )
        row += 1
        
        # Address
        ttk.Label(form_frame, text="Address:").grid(row=row, column=0, sticky="nw", pady=5)
        self.address_text = tk.Text(form_frame, height=3, width=30, font=("Helvetica", 10))
        self.address_text.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
        row += 1
        
        # Skills
        ttk.Label(form_frame, text="Skills:").grid(row=row, column=0, sticky="w", pady=5)
        self.skills_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.skills_var, width=30).grid(
            row=row, column=1, sticky="ew", padx=(10, 0), pady=5
        )
        # Skills help text
        help_label = ttk.Label(
            form_frame, 
            text="(Comma-separated: plumbing, electrical, insulation)",
            font=("Helvetica", 8),
            foreground=Colors.TEXT_SECONDARY
        )
        help_label.grid(row=row+1, column=1, sticky="w", padx=(10, 0))
        row += 2
        
        # Active status
        self.active_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            form_frame,
            text="Active volunteer",
            variable=self.active_var
        ).grid(row=row, column=1, sticky="w", padx=(10, 0), pady=5)
        row += 1
        
        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=row, column=0, sticky="nw", pady=5)
        self.notes_text = tk.Text(form_frame, height=4, width=30, font=("Helvetica", 10))
        self.notes_text.grid(row=row, column=1, sticky="ew", padx=(10, 0), pady=5)
        row += 1
        
        # Buttons frame
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        self.save_button = ttk.Button(
            buttons_frame,
            text="💾 Save Volunteer",
            command=self.save_volunteer,
            bootstyle=SUCCESS,
            width=15
        )
        self.save_button.pack(side=LEFT, padx=5)
        
        ttk.Button(
            buttons_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            bootstyle=SECONDARY,
            width=15
        ).pack(side=LEFT, padx=5)
        
        # Statistics section
        stats_frame = ttk.LabelFrame(form_frame, text="Statistics", padding=10)
        stats_frame.grid(row=row+1, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        stats_frame.columnconfigure((0, 1), weight=1)
        
        # Stats labels
        self.stats_visits_label = ttk.Label(stats_frame, text="Total Visits: 0", font=("Helvetica", 10, "bold"))
        self.stats_visits_label.grid(row=0, column=0, sticky="w")
        
        self.stats_last_visit_label = ttk.Label(stats_frame, text="Last Visit: Never", font=("Helvetica", 10))
        self.stats_last_visit_label.grid(row=0, column=1, sticky="w")
        
        self.stats_joined_label = ttk.Label(stats_frame, text="Joined: ", font=("Helvetica", 10))
        self.stats_joined_label.grid(row=1, column=0, columnspan=2, sticky="w")
    
    def refresh_data(self):
        """Refresh volunteer list"""
        try:
            # Clear existing items
            for item in self.volunteer_tree.get_children():
                self.volunteer_tree.delete(item)
            
            # Load volunteers
            volunteers = Volunteer.select().order_by(Volunteer.name)
            
            for volunteer in volunteers:
                last_visit = volunteer.last_visit_date
                last_visit_str = last_visit.strftime("%m/%d/%Y") if last_visit else "Never"
                
                self.volunteer_tree.insert("", "end", values=(
                    volunteer.name,
                    volunteer.phone or "",
                    volunteer.email or "",
                    volunteer.visit_count,
                    last_visit_str
                ))
            
            logger.info(f"Loaded {len(list(volunteers))} volunteers")
            
        except Exception as e:
            logger.error(f"Failed to refresh volunteer data: {e}")
            messagebox.showerror("Error", f"Failed to load volunteers: {e}")
    
    def on_search_changed(self, *args):
        """Handle search input changes"""
        query = self.search_var.get().strip()
        
        if not query or query == "Search volunteers...":
            self.refresh_data()
            return
        
        try:
            # Clear existing items
            for item in self.volunteer_tree.get_children():
                self.volunteer_tree.delete(item)
            
            # Search volunteers
            volunteers = search_volunteers(query)
            
            for volunteer in volunteers:
                last_visit = volunteer.last_visit_date
                last_visit_str = last_visit.strftime("%m/%d/%Y") if last_visit else "Never"
                
                self.volunteer_tree.insert("", "end", values=(
                    volunteer.name,
                    volunteer.phone or "",
                    volunteer.email or "",
                    volunteer.visit_count,
                    last_visit_str
                ))
                
        except Exception as e:
            logger.error(f"Search failed: {e}")
    
    def on_search_focus_in(self, event):
        """Handle search field focus in"""
        if event.widget.get() == "Search volunteers...":
            event.widget.delete(0, tk.END)
    
    def on_search_focus_out(self, event):
        """Handle search field focus out"""
        if not event.widget.get().strip():
            event.widget.insert(0, "Search volunteers...")
    
    def on_volunteer_select(self, event):
        """Handle volunteer selection"""
        selection = self.volunteer_tree.selection()
        if not selection:
            return
        
        # Get selected volunteer data
        item = self.volunteer_tree.item(selection[0])
        volunteer_name = item['values'][0]
        
        try:
            # Find volunteer by name
            volunteer = Volunteer.get(Volunteer.name == volunteer_name)
            self.selected_volunteer = volunteer
            
            # Update form with volunteer data
            self.populate_form(volunteer)
            
        except Volunteer.DoesNotExist:
            logger.error(f"Volunteer not found: {volunteer_name}")
        except Exception as e:
            logger.error(f"Failed to load volunteer details: {e}")
    
    def populate_form(self, volunteer):
        """Populate form with volunteer data"""
        # Clear form first
        self.clear_form()
        
        # Set form values
        self.name_var.set(volunteer.name)
        self.phone_var.set(volunteer.phone or "")
        self.email_var.set(volunteer.email or "")
        self.skills_var.set(volunteer.skills or "")
        self.active_var.set(volunteer.is_active)
        
        # Set text fields
        if volunteer.address:
            self.address_text.insert("1.0", volunteer.address)
        
        if volunteer.notes:
            self.notes_text.insert("1.0", volunteer.notes)
        
        # Update statistics
        self.stats_visits_label.config(text=f"Total Visits: {volunteer.visit_count}")
        
        last_visit = volunteer.last_visit_date
        last_visit_str = last_visit.strftime("%B %d, %Y") if last_visit else "Never"
        self.stats_last_visit_label.config(text=f"Last Visit: {last_visit_str}")
        
        joined_str = volunteer.date_joined.strftime("%B %d, %Y")
        self.stats_joined_label.config(text=f"Joined: {joined_str}")
        
        # Update save button text
        self.save_button.config(text="💾 Update Volunteer")
    
    def clear_form(self):
        """Clear the volunteer form"""
        self.selected_volunteer = None
        
        # Clear string variables
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.skills_var.set("")
        self.active_var.set(True)
        
        # Clear text widgets
        self.address_text.delete("1.0", tk.END)
        self.notes_text.delete("1.0", tk.END)
        
        # Reset statistics
        self.stats_visits_label.config(text="Total Visits: 0")
        self.stats_last_visit_label.config(text="Last Visit: Never")
        self.stats_joined_label.config(text="Joined: ")
        
        # Reset save button text
        self.save_button.config(text="💾 Save Volunteer")
        
        # Clear tree selection
        self.volunteer_tree.selection_remove(self.volunteer_tree.selection())
    
    def add_volunteer(self):
        """Add new volunteer"""
        self.clear_form()
        self.name_var.set("")  # Focus on name field
    
    def edit_volunteer(self):
        """Edit selected volunteer"""
        if not self.selected_volunteer:
            messagebox.showwarning("No Selection", "Please select a volunteer to edit.")
            return
        
        # Form is already populated, user can make changes and save
        messagebox.showinfo("Edit Mode", "Make your changes and click 'Update Volunteer' to save.")
    
    def delete_volunteer(self):
        """Delete selected volunteer"""
        if not self.selected_volunteer:
            messagebox.showwarning("No Selection", "Please select a volunteer to delete.")
            return
        
        # Confirm deletion
        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete volunteer '{self.selected_volunteer.name}'?\n\nThis action cannot be undone."
        ):
            try:
                volunteer_name = self.selected_volunteer.name
                self.selected_volunteer.delete_instance()
                
                logger.info(f"Deleted volunteer: {volunteer_name}")
                messagebox.showinfo("Success", f"Volunteer '{volunteer_name}' has been deleted.")
                
                self.clear_form()
                self.refresh_data()
                
            except Exception as e:
                logger.error(f"Failed to delete volunteer: {e}")
                messagebox.showerror("Error", f"Failed to delete volunteer: {e}")
    
    def save_volunteer(self):
        """Save volunteer data"""
        # Validate required fields
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Name is required.")
            return
        
        try:
            # Get form data
            volunteer_data = {
                'name': self.name_var.get().strip(),
                'phone': self.phone_var.get().strip() or None,
                'email': self.email_var.get().strip() or None,
                'address': self.address_text.get("1.0", tk.END).strip() or None,
                'skills': self.skills_var.get().strip() or None,
                'notes': self.notes_text.get("1.0", tk.END).strip() or None,
                'is_active': self.active_var.get()
            }
            
            if self.selected_volunteer:
                # Update existing volunteer
                for key, value in volunteer_data.items():
                    setattr(self.selected_volunteer, key, value)
                self.selected_volunteer.save()
                
                logger.info(f"Updated volunteer: {self.selected_volunteer.name}")
                messagebox.showinfo("Success", "Volunteer updated successfully!")
                
            else:
                # Create new volunteer
                volunteer = Volunteer.create(**volunteer_data)
                self.selected_volunteer = volunteer
                
                logger.info(f"Created new volunteer: {volunteer.name}")
                messagebox.showinfo("Success", "Volunteer created successfully!")
            
            # Refresh data and update form
            self.refresh_data()
            self.populate_form(self.selected_volunteer)
            
        except Exception as e:
            logger.error(f"Failed to save volunteer: {e}")
            messagebox.showerror("Error", f"Failed to save volunteer: {e}")
