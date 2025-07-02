"""
Link Generator UI page for EnergieFixers071.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import webbrowser

from core.services.link_generator_service import LinkGeneratorService
from config import Colors

class LinksPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.svc = LinkGeneratorService()
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        ttk.Label(
            self,
            text="KoboToolbox Link Generator",
            font=("Helvetica",16,"bold"),
            foreground=Colors.PRIMARY_GREEN,
        ).grid(row=0,column=0,sticky="w", pady=(0,10))

        # Form URL
        urlfrm = ttk.Frame(self)
        urlfrm.grid(row=1,column=0,sticky="ew", pady=5)
        urlfrm.columnconfigure(0, weight=1)
        ttk.Label(urlfrm,text="Form URL:").grid(row=0,column=0,sticky="w")
        self.url = tk.StringVar(value=self.svc.default_form_url)
        ttk.Entry(urlfrm,textvariable=self.url).grid(row=1,column=0,sticky="ew")

        # Fields
        fieldfrm = ttk.LabelFrame(self, text="Pre-fill Fields")
        fieldfrm.grid(row=2,column=0,sticky="ew", pady=10)
        self.vars = {k: tk.StringVar() for k in self.svc.default_fields()}
        row=0
        for key,label in [("adres","Address"),("afspraakTijd","Appointment Time"),("uitvoerders","Volunteers")]:
            ttk.Label(fieldfrm,text=label+":").grid(row=row,column=0,sticky="w", padx=5, pady=4)
            ttk.Entry(fieldfrm,textvariable=self.vars[key]).grid(row=row,column=1,sticky="ew", padx=5, pady=4)
            fieldfrm.columnconfigure(1, weight=1)
            row+=1

        # Result
        resfrm = ttk.Frame(self)
        resfrm.grid(row=3,column=0,sticky="ew", pady=10)
        resfrm.columnconfigure(0,weight=1)
        ttk.Label(resfrm,text="Generated Link:").grid(row=0,column=0,sticky="w")
        self.result = tk.StringVar()
        ttk.Entry(resfrm,textvariable=self.result,state="readonly").grid(row=1,column=0,sticky="ew")

        btnfrm = ttk.Frame(self)
        btnfrm.grid(row=4,column=0,pady=10)
        ttk.Button(btnfrm,text="Generate",bootstyle=PRIMARY,command=self._generate).pack(side=LEFT,padx=5)
        ttk.Button(btnfrm,text="Copy",bootstyle=SUCCESS,command=self._copy).pack(side=LEFT,padx=5)
        ttk.Button(btnfrm,text="Open",bootstyle=INFO,command=self._open).pack(side=LEFT,padx=5)

    def _generate(self):
        if not self.svc.validate_url(self.url.get()):
            messagebox.showwarning("URL","Invalid KoboToolbox URL")
            return
        fields = {k:v.get().strip() for k,v in self.vars.items() if v.get().strip()}
        link = self.svc.generate_link(self.url.get().strip(), fields)
        self.result.set(link)

    def _copy(self):
        if self.result.get():
            self.clipboard_clear()
            self.clipboard_append(self.result.get())
            messagebox.showinfo("Copied","Link copied to clipboard")

    def _open(self):
        if self.result.get():
            webbrowser.open(self.result.get())