import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def generate_link():
    """Generate the KoboToolbox link with pre-filled fields inside the 'introductie' group."""
    base_url = base_url_entry.get().strip()
    if not base_url:
        messagebox.showwarning("Warning", "Please enter a valid BASE_URL")
        return

    # Define the group and fields inside the group
    group = "introductie"
    
    # Build the query parameters with the group prefix
    params = "&".join([f"d[{group}/{key}]={value_entry[key].get().strip()}" for key in fields if value_entry[key].get().strip()])
    final_link = f"{base_url}?{params}" if params else base_url
    link_var.set(final_link)


def copy_to_clipboard():
    """Copy the generated link to the clipboard."""
    root.clipboard_clear()
    root.clipboard_append(link_var.get())
    root.update()


# Tkinter UI Setup with ttkbootstrap
root = ttk.Window(themename="flatly")
root.title("AutoEnergie")
root.geometry("800x700")  # Increased window size for better layout
root.configure(bg="#f0f0f0")  # Slightly darker gray background

# Load and display the logo
logo_path = "Logo-Energiefixers071.png"  # Ensure the logo file is in the same directory
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((350, 175), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ttk.Label(root, image=logo_photo, background="#f0f0f0")
    logo_label.image = logo_photo
    logo_label.pack(pady=20)  # Increased padding for better spacing
except Exception as e:
    messagebox.showerror("Error", f"Unable to load logo: {e}")

# Base URL Input
base_url_frame = ttk.Frame(root, padding=10)
base_url_frame.pack(pady=5, fill=tk.X, padx=20)
ttk.Label(base_url_frame, text="Enter KoboToolbox Form URL:", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

# Default value set in the Entry field
base_url_entry = ttk.Entry(base_url_frame, width=50, font=("Helvetica", 12))
base_url_entry.insert(0, "https://ee-eu.kobotoolbox.org/x/Evnz0R4w")  # Default Link
base_url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)


# Fields to be filled
fields = {
    "adres": "",
    "afspraakTijd": "",
    "uitvoerders": ""
}

value_entry = {}

# Create input fields dynamically
fields_frame = ttk.Frame(root, padding=10)
fields_frame.pack(pady=10, fill=tk.X, padx=20)
ttk.Label(fields_frame, text="Enter field values:", font=("Helvetica", 14, "bold")).pack(pady=5)
for key in fields:
    frame = ttk.Frame(fields_frame, padding=5)
    frame.pack(pady=5, fill=tk.X)
    ttk.Label(frame, text=f"{key}:", font=("Helvetica", 12), width=20).pack(side=tk.LEFT, padx=5)
    entry = ttk.Entry(frame, width=50, font=("Helvetica", 12))
    entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    value_entry[key] = entry

# Generate Link Button
generate_button = ttk.Button(root, text="Generate Link", command=generate_link, bootstyle=SUCCESS)
generate_button.pack(pady=10, fill=tk.X, padx=50)

# Link Display
link_var = tk.StringVar()
link_entry = ttk.Entry(root, textvariable=link_var, width=80, font=("Helvetica", 12), state="readonly")
link_entry.pack(pady=5, fill=tk.X, padx=50)

# Copy Button
copy_button = ttk.Button(root, text="Copy Link", command=copy_to_clipboard, bootstyle=INFO)
copy_button.pack(pady=10, fill=tk.X, padx=50)

# Make UI Responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Run the Tkinter event loop
root.mainloop()
