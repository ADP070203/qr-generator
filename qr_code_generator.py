import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import qrcode
from qrcode.constants import (
    ERROR_CORRECT_H,
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
)


ERROR_LEVELS = {
    "L (7%)": ERROR_CORRECT_L,
    "M (15%)": ERROR_CORRECT_M,
    "Q (25%)": ERROR_CORRECT_Q,
    "H (30%)": ERROR_CORRECT_H,
}

TOKENS = {
    "bg": "#f4f1ea",
    "surface": "#ffffff",
    "surface_alt": "#f8f6f1",
    "border": "#ded9cf",
    "text": "#1f2933",
    "muted": "#667085",
    "accent": "#2f6f4f",
    "accent_hover": "#275c42",
    "accent_soft": "#e5f0e9",
    "focus": "#8bb89d",
}

FONTS = {
    "display": ("Avenir Next", 24, "bold"),
    "title": ("Avenir Next", 16, "bold"),
    "body": ("Avenir Next", 11),
    "body_bold": ("Avenir Next", 11, "bold"),
    "small": ("Avenir Next", 10),
}


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_location_var.set(folder)
        status_var.set(f"Save location set to {folder}")


def show_message(kind, title, message):
    if kind == "error":
        status_var.set(title)
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)


def generate_qr():
    text = text_input.get("1.0", tk.END).strip()
    save_location = save_location_var.get().strip()
    file_name = file_name_var.get().strip()
    version_text = version_var.get().strip()
    box_size_text = box_size_var.get().strip()
    border_text = border_var.get().strip()
    error_level_text = error_level_var.get().strip()

    if not text:
        show_message("error", "Missing text", "Please enter text or a URL.")
        return

    if not save_location:
        show_message("error", "Missing folder", "Please choose where to save the QR code.")
        return

    if not os.path.isdir(save_location):
        show_message("error", "Invalid folder", "The save folder does not exist.")
        return

    if not file_name:
        show_message("error", "Missing file name", "Please enter a file name.")
        return

    if file_name.lower().endswith(".png"):
        file_name = file_name[:-4]

    try:
        version = int(version_text)
        if version < 1 or version > 40:
            raise ValueError
    except ValueError:
        show_message("error", "Invalid version", "Version must be a whole number from 1 to 40.")
        return

    try:
        box_size = int(box_size_text)
        if box_size < 1:
            raise ValueError
    except ValueError:
        show_message("error", "Invalid box size", "Box size must be a whole number greater than 0.")
        return

    try:
        border = int(border_text)
        if border < 4:
            raise ValueError
    except ValueError:
        show_message("error", "Invalid border", "Border must be a whole number of at least 4.")
        return

    error_correction = ERROR_LEVELS.get(error_level_text, ERROR_CORRECT_M)

    try:
        qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        full_path = os.path.join(save_location, f"{file_name}.png")
        img.save(full_path)

        status_var.set(f"Saved to {full_path}")
        show_message("info", "Success", f"QR code saved successfully:\n{full_path}")
    except Exception as error:
        show_message("error", "Error", f"Could not generate QR code.\n\n{error}")


def create_card(parent):
    card = tk.Frame(
        parent,
        bg=TOKENS["surface"],
        highlightbackground=TOKENS["border"],
        highlightthickness=1,
        bd=0,
        padx=24,
        pady=22,
    )
    return card


def add_section_header(parent, title, subtitle):
    wrapper = tk.Frame(parent, bg=TOKENS["surface"])
    wrapper.pack(fill="x", pady=(0, 14))
    tk.Label(
        wrapper,
        text=title,
        font=FONTS["title"],
        bg=TOKENS["surface"],
        fg=TOKENS["text"],
    ).pack(anchor="w")
    tk.Label(
        wrapper,
        text=subtitle,
        font=FONTS["small"],
        bg=TOKENS["surface"],
        fg=TOKENS["muted"],
        wraplength=720,
        justify="left",
    ).pack(anchor="w", pady=(4, 0))


def add_field(parent, label, helper=None):
    wrapper = tk.Frame(parent, bg=TOKENS["surface"])
    tk.Label(
        wrapper,
        text=label,
        font=FONTS["body_bold"],
        bg=TOKENS["surface"],
        fg=TOKENS["text"],
    ).pack(anchor="w")
    if helper:
        tk.Label(
            wrapper,
            text=helper,
            font=FONTS["small"],
            bg=TOKENS["surface"],
            fg=TOKENS["muted"],
            wraplength=320,
            justify="left",
        ).pack(anchor="w", pady=(3, 8))
    else:
        wrapper.pack_propagate(False)
    return wrapper


def load_logo():
    logo_path = Path(__file__).with_name("logo-biotech.png")
    if not logo_path.exists():
        return None

    try:
        logo = tk.PhotoImage(file=str(logo_path))
    except tk.TclError:
        return None

    width = logo.width()
    target_width = 240
    scale = max(1, width // target_width)
    if scale > 1:
        logo = logo.subsample(scale, scale)
    return logo


def update_layout(event=None):
    width = root.winfo_width()
    if width < 920:
        main_card.grid_configure(row=0, column=0, padx=0, pady=(0, 16), sticky="nsew")
        sidebar_card.grid_configure(row=1, column=0, padx=0, pady=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=0)
    else:
        main_card.grid_configure(row=0, column=0, padx=(0, 16), pady=0, sticky="nsew")
        sidebar_card.grid_configure(row=0, column=1, padx=0, pady=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=3)
        content.grid_columnconfigure(1, weight=2)


root = tk.Tk()
root.title("C-biotech QR Code Generator")
root.geometry("980x760")
root.minsize(760, 680)
root.configure(bg=TOKENS["bg"])

style = ttk.Style()
style.theme_use("clam")

style.configure(
    ".",
    font=FONTS["body"],
)
style.configure(
    "Card.TFrame",
    background=TOKENS["surface"],
    borderwidth=0,
)
style.configure(
    "Modern.TEntry",
    fieldbackground=TOKENS["surface_alt"],
    background=TOKENS["surface_alt"],
    foreground=TOKENS["text"],
    bordercolor=TOKENS["border"],
    lightcolor=TOKENS["border"],
    darkcolor=TOKENS["border"],
    padding=10,
    relief="flat",
)
style.map(
    "Modern.TEntry",
    bordercolor=[("focus", TOKENS["focus"])],
    lightcolor=[("focus", TOKENS["focus"])],
    darkcolor=[("focus", TOKENS["focus"])],
)
style.configure(
    "Modern.TCombobox",
    fieldbackground=TOKENS["surface_alt"],
    background=TOKENS["surface_alt"],
    foreground=TOKENS["text"],
    bordercolor=TOKENS["border"],
    lightcolor=TOKENS["border"],
    darkcolor=TOKENS["border"],
    arrowsize=14,
    padding=8,
    relief="flat",
)
style.map(
    "Modern.TCombobox",
    bordercolor=[("focus", TOKENS["focus"])],
    lightcolor=[("focus", TOKENS["focus"])],
    darkcolor=[("focus", TOKENS["focus"])],
)
style.configure(
    "Primary.TButton",
    font=FONTS["body_bold"],
    foreground="#ffffff",
    background=TOKENS["accent"],
    borderwidth=0,
    padding=(18, 12),
)
style.map(
    "Primary.TButton",
    background=[("active", TOKENS["accent_hover"])],
)
style.configure(
    "Secondary.TButton",
    font=FONTS["body_bold"],
    foreground=TOKENS["text"],
    background=TOKENS["surface_alt"],
    borderwidth=0,
    padding=(14, 10),
)
style.map(
    "Secondary.TButton",
    background=[("active", "#ece7de")],
)

save_location_var = tk.StringVar()
file_name_var = tk.StringVar(value="my_qr_code")
version_var = tk.StringVar(value="1")
box_size_var = tk.StringVar(value="10")
border_var = tk.StringVar(value="4")
error_level_var = tk.StringVar(value="M (15%)")
status_var = tk.StringVar(value="Ready to generate a QR code.")

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

outer = tk.Frame(root, bg=TOKENS["bg"], padx=28, pady=28)
outer.grid(sticky="nsew")
outer.grid_columnconfigure(0, weight=1)
outer.grid_rowconfigure(1, weight=1)

hero = tk.Frame(outer, bg=TOKENS["surface"], padx=28, pady=26, highlightbackground=TOKENS["border"], highlightthickness=1)
hero.grid(row=0, column=0, sticky="ew", pady=(0, 20))
hero.grid_columnconfigure(0, weight=1)

logo_image = load_logo()
if logo_image:
    root.logo_image = logo_image
    tk.Label(hero, image=logo_image, bg=TOKENS["surface"]).grid(row=0, column=0, sticky="w", pady=(0, 14))

tk.Label(
    hero,
    text="C-biotech QR Code Generator",
    font=FONTS["display"],
    bg=TOKENS["surface"],
    fg=TOKENS["text"],
).grid(row=1, column=0, sticky="w")

tk.Label(
    hero,
    text="Generate production-ready QR codes with a cleaner workflow, clearer inputs and a calmer visual hierarchy.",
    font=FONTS["body"],
    bg=TOKENS["surface"],
    fg=TOKENS["muted"],
    wraplength=720,
    justify="left",
).grid(row=2, column=0, sticky="w", pady=(8, 18))

status_pill = tk.Label(
    hero,
    textvariable=status_var,
    font=FONTS["small"],
    bg=TOKENS["accent_soft"],
    fg=TOKENS["accent"],
    padx=12,
    pady=7,
)
status_pill.grid(row=3, column=0, sticky="w")

content = tk.Frame(outer, bg=TOKENS["bg"])
content.grid(row=1, column=0, sticky="nsew")
content.grid_columnconfigure(0, weight=3)
content.grid_columnconfigure(1, weight=2)
content.grid_rowconfigure(0, weight=1)
content.grid_rowconfigure(1, weight=1)

main_card = create_card(content)
main_card.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

sidebar_card = create_card(content)
sidebar_card.grid(row=0, column=1, sticky="nsew")

add_section_header(
    main_card,
    "Content",
    "Paste the URL, text or payload you want to encode. The content field remains fully multi-line.",
)

text_field = add_field(main_card, "Text or URL", "Anything entered here will be encoded into the QR code.")
text_field.pack(fill="x")

text_input = tk.Text(
    text_field,
    height=7,
    font=FONTS["body"],
    bg=TOKENS["surface_alt"],
    fg=TOKENS["text"],
    relief="flat",
    bd=0,
    padx=12,
    pady=12,
    insertbackground=TOKENS["text"],
    highlightthickness=2,
    highlightbackground=TOKENS["border"],
    highlightcolor=TOKENS["focus"],
    wrap="word",
)
text_input.pack(fill="x")

add_section_header(
    main_card,
    "Output",
    "Choose where the PNG should be saved and give it a clear file name.",
)

location_field = add_field(main_card, "Save folder")
location_field.pack(fill="x", pady=(0, 14))
location_row = tk.Frame(location_field, bg=TOKENS["surface"])
location_row.pack(fill="x")
location_row.grid_columnconfigure(0, weight=1)

location_entry = ttk.Entry(
    location_row,
    textvariable=save_location_var,
    style="Modern.TEntry",
)
location_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

browse_button = ttk.Button(
    location_row,
    text="Browse",
    command=browse_folder,
    style="Secondary.TButton",
)
browse_button.grid(row=0, column=1, sticky="ew")

name_field = add_field(main_card, "File name", "The file will always be saved as a PNG.")
name_field.pack(fill="x")

file_name_entry = ttk.Entry(
    name_field,
    textvariable=file_name_var,
    style="Modern.TEntry",
)
file_name_entry.pack(fill="x")

add_section_header(
    sidebar_card,
    "Settings",
    "Fine-tune the QR code size, density and resilience without changing the generation flow.",
)

settings_grid = tk.Frame(sidebar_card, bg=TOKENS["surface"])
settings_grid.pack(fill="x")
settings_grid.grid_columnconfigure(0, weight=1)
settings_grid.grid_columnconfigure(1, weight=1)

version_field = add_field(settings_grid, "Version", "1 is the smallest, 40 the largest.")
version_field.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(0, 14))
version_entry = ttk.Entry(version_field, textvariable=version_var, style="Modern.TEntry")
version_entry.pack(fill="x")

box_size_field = add_field(settings_grid, "Box size", "Controls pixel size for each QR square.")
box_size_field.grid(row=0, column=1, sticky="ew", padx=(8, 0), pady=(0, 14))
box_size_entry = ttk.Entry(box_size_field, textvariable=box_size_var, style="Modern.TEntry")
box_size_entry.pack(fill="x")

border_field = add_field(settings_grid, "Border", "Keep at least 4 for scanner compatibility.")
border_field.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(0, 14))
border_entry = ttk.Entry(border_field, textvariable=border_var, style="Modern.TEntry")
border_entry.pack(fill="x")

error_field = add_field(settings_grid, "Error correction", "Higher correction improves resilience but increases complexity.")
error_field.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(0, 14))
error_menu = ttk.Combobox(
    error_field,
    textvariable=error_level_var,
    values=list(ERROR_LEVELS.keys()),
    state="readonly",
    style="Modern.TCombobox",
)
error_menu.pack(fill="x")

tips_card = tk.Frame(
    sidebar_card,
    bg=TOKENS["surface_alt"],
    highlightbackground=TOKENS["border"],
    highlightthickness=1,
    bd=0,
    padx=16,
    pady=16,
)
tips_card.pack(fill="x", pady=(8, 20))

tk.Label(
    tips_card,
    text="Quick guidance",
    font=FONTS["body_bold"],
    bg=TOKENS["surface_alt"],
    fg=TOKENS["text"],
).pack(anchor="w")

tk.Label(
    tips_card,
    text=(
        "Use lower versions for short links.\n"
        "Choose H when physical damage or print quality may be an issue.\n"
        "Keep the file name short and descriptive for easier reuse."
    ),
    font=FONTS["small"],
    bg=TOKENS["surface_alt"],
    fg=TOKENS["muted"],
    justify="left",
    wraplength=280,
).pack(anchor="w", pady=(8, 0))

generate_button = ttk.Button(
    sidebar_card,
    text="Generate QR Code",
    command=generate_qr,
    style="Primary.TButton",
)
generate_button.pack(fill="x")

footer = tk.Label(
    outer,
    text="Designed for a calmer, clearer workflow without changing how QR generation works.",
    font=FONTS["small"],
    bg=TOKENS["bg"],
    fg=TOKENS["muted"],
)
footer.grid(row=2, column=0, sticky="w", pady=(16, 0))

text_input.focus_set()
root.bind("<Configure>", update_layout)
update_layout()

root.mainloop()
