"""
Home / Dashboard page displaying stats and activity.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from datetime import datetime
import logging

from core.models import get_volunteer_stats, get_recent_visits, get_upcoming_appointments
from config import Colors

logger = logging.getLogger(__name__)

class HomePage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()
        self.refresh_data()

    # -------- Build UI -------- #
    def _build(self):
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(2, weight=1)
        self._build_header()
        self._build_stats()
        self._build_activity()

    def _build_header(self):
        frame = ttk.Frame(self)
        frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,20))
        ttk.Label(
            frame,
            text="Welcome to EnergieFixers071",
            font=("Helvetica", 20, "bold"),
            foreground=Colors.PRIMARY_GREEN,
        ).pack(anchor="w")
        ttk.Label(
            frame,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Helvetica", 11),
            foreground=Colors.TEXT_SECONDARY,
        ).pack(anchor="w")

    def _build_stats(self):
        frame = ttk.LabelFrame(self, text="Statistics Overview", padding=15)
        frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        frame.columnconfigure((0,1,2,3), weight=1)
        self.cards = {}
        items = [
            ("volunteers", "👥 Volunteers", Colors.PRIMARY_GREEN),
            ("active_volunteers", "✅ Active", Colors.SUCCESS),
            ("visits", "🏡 Visits", Colors.INFO),
            ("visits_month", "📊 This Month", Colors.WARNING),
        ]
        for i,(key,label,color) in enumerate(items):
            card = ttk.Frame(frame, style="Card.TFrame")
            card.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            val_lbl = ttk.Label(card, text="0", font=("Helvetica",24,"bold"), foreground=color)
            val_lbl.pack(pady=(10,5))
            ttk.Label(card, text=label, font=("Helvetica",10), foreground=Colors.TEXT_SECONDARY).pack(pady=(0,10))
            self.cards[key]=val_lbl

    def _build_activity(self):
        visits = ttk.LabelFrame(self, text="Recent Visits", padding=10)
        visits.grid(row=2, column=0, sticky="nsew", padx=(0,10))
        visits.columnconfigure(0, weight=1)
        self.visit_list = tk.Listbox(visits, height=8)
        ttk.Scrollbar(visits, orient=VERTICAL, command=self.visit_list.yview).grid(row=0,column=1,sticky="ns")
        self.visit_list.grid(row=0,column=0,sticky="nsew")

        appts = ttk.LabelFrame(self, text="Upcoming Appointments", padding=10)
        appts.grid(row=2,column=1, sticky="nsew")
        appts.columnconfigure(0, weight=1)
        self.appt_list = tk.Listbox(appts, height=8)
        ttk.Scrollbar(appts, orient=VERTICAL, command=self.appt_list.yview).grid(row=0,column=1,sticky="ns")
        self.appt_list.grid(row=0,column=0,sticky="nsew")

    # -------- Data -------- #
    def refresh_data(self):
        stats = get_volunteer_stats()
        for k,v in stats.items():
            self.cards[k].config(text=str(v))
        # visits
        self.visit_list.delete(0, tk.END)
        for v in get_recent_visits():
            txt = f"{v.visit_date:%d/%m} - {v.address[:30]}" if v.address else str(v.visit_date)
            self.visit_list.insert(tk.END, txt)
        # appointments
        self.appt_list.delete(0, tk.END)
        for a in get_upcoming_appointments():
            txt = f"{a.start_time:%d/%m %H:%M} - {a.event_name}"
            self.appt_list.insert(tk.END, txt)