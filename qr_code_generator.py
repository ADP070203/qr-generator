import os
import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


ERROR_LEVELS = {
    "L (7%)": ERROR_CORRECT_L,
    "M (15%)": ERROR_CORRECT_M,
    "Q (25%)": ERROR_CORRECT_Q,
    "H (30%)": ERROR_CORRECT_H,
}


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_location_var.set(folder)


def generate_qr():
    text = text_input.get("1.0", tk.END).strip()
    save_location = save_location_var.get().strip()
    file_name = file_name_var.get().strip()
    version_text = version_var.get().strip()
    box_size_text = box_size_var.get().strip()
    border_text = border_var.get().strip()
    error_level_text = error_level_var.get().strip()

    if not text:
        messagebox.showerror("Missing text", "Please enter text or a URL.")
        return

    if not save_location:
        messagebox.showerror("Missing folder", "Please choose where to save the QR code.")
        return

    if not os.path.isdir(save_location):
        messagebox.showerror("Invalid folder", "The save folder does not exist.")
        return

    if not file_name:
        messagebox.showerror("Missing file name", "Please enter a file name.")
        return

    # Remove .png if the user typed it
    if file_name.lower().endswith(".png"):
        file_name = file_name[:-4]

    try:
        version = int(version_text)
        if version < 1 or version > 40:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid version", "Version must be a whole number from 1 to 40.")
        return

    try:
        box_size = int(box_size_text)
        if box_size < 1:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid box size", "Box size must be a whole number greater than 0.")
        return

    try:
        border = int(border_text)
        if border < 4:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid border", "Border must be a whole number of at least 4.")
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

        messagebox.showinfo("Success", f"QR code saved successfully:\n{full_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate QR code.\n\n{e}")


# Main window
root = tk.Tk()
root.title("C-biotech QR Code Generator")
root.geometry("700x620")
root.resizable(False, False)
root.configure(bg="#74C365")

title_label = tk.Label(
    root,
    text="C-biotech QR Code Generator",
    font=("Arial", 22, "bold"),
    bg="#74C365",
    fg="#1b4332"
)
title_label.pack(pady=15)

# Text / URL
text_frame = tk.Frame(root, bg="#74C365")
text_frame.pack(fill="x", padx=20, pady=8)

tk.Label(
    text_frame,
    text="Enter text or URL:",
    font=("Arial", 12, "bold"),
    bg="#74C365"
).pack(anchor="w")

text_input = tk.Text(text_frame, height=5, font=("Arial", 11))
text_input.pack(fill="x", pady=5)

# Save location
location_frame = tk.Frame(root, bg="#74C365")
location_frame.pack(fill="x", padx=20, pady=8)

tk.Label(
    location_frame,
    text="Choose folder to save the QR code:",
    font=("Arial", 12, "bold"),
    bg="#74C365"
).grid(row=0, column=0, sticky="w", columnspan=2)

save_location_var = tk.StringVar()

location_entry = tk.Entry(location_frame, textvariable=save_location_var, font=("Arial", 11), width=60)
location_entry.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")

browse_button = tk.Button(
    location_frame,
    text="Browse",
    font=("Arial", 11),
    command=browse_folder
)
browse_button.grid(row=1, column=1, pady=5)

# File name
name_frame = tk.Frame(root, bg="#74C365")
name_frame.pack(fill="x", padx=20, pady=8)

tk.Label(
    name_frame,
    text="File name:",
    font=("Arial", 12, "bold"),
    bg="#74C365"
).pack(anchor="w")

file_name_var = tk.StringVar(value="my_qr_code")
file_name_entry = tk.Entry(name_frame, textvariable=file_name_var, font=("Arial", 11))
file_name_entry.pack(fill="x", pady=5)

# Options
options_frame = tk.Frame(root, bg="#74C365")
options_frame.pack(fill="x", padx=20, pady=8)

# Version
tk.Label(options_frame, text="Version (1-40):", font=("Arial", 11, "bold"), bg="#74C365").grid(row=0, column=0, sticky="w", padx=5, pady=5)
version_var = tk.StringVar(value="1")
tk.Entry(options_frame, textvariable=version_var, font=("Arial", 11), width=10).grid(row=1, column=0, sticky="w", padx=5)

# Box size
tk.Label(options_frame, text="Box size:", font=("Arial", 11, "bold"), bg="#74C365").grid(row=0, column=1, sticky="w", padx=5, pady=5)
box_size_var = tk.StringVar(value="10")
tk.Entry(options_frame, textvariable=box_size_var, font=("Arial", 11), width=10).grid(row=1, column=1, sticky="w", padx=5)

# Border
tk.Label(options_frame, text="Border (min 4):", font=("Arial", 11, "bold"), bg="#74C365").grid(row=0, column=2, sticky="w", padx=5, pady=5)
border_var = tk.StringVar(value="4")
tk.Entry(options_frame, textvariable=border_var, font=("Arial", 11), width=10).grid(row=1, column=2, sticky="w", padx=5)

# Error correction
tk.Label(options_frame, text="Error correction:", font=("Arial", 11, "bold"), bg="#74C365").grid(row=0, column=3, sticky="w", padx=5, pady=5)
error_level_var = tk.StringVar(value="M (15%)")
error_menu = tk.OptionMenu(options_frame, error_level_var, *ERROR_LEVELS.keys())
error_menu.config(font=("Arial", 10), width=12)
error_menu.grid(row=1, column=3, sticky="w", padx=5)

# Generate button
generate_button = tk.Button(
    root,
    text="Generate QR Code",
    font=("Arial", 14, "bold"),
    bg="#2d6a4f",
    fg="white",
    padx=20,
    pady=10,
    command=generate_qr
)
generate_button.pack(pady=25)

# Help text
help_label = tk.Label(
    root,
    text=(
        "Tip: Version controls QR size/complexity (1 is smallest, 40 is largest).\n"
        "Use H for the strongest error correction."
    ),
    font=("Arial", 10),
    bg="#74C365",
    fg="#333333",
    justify="center"
)
help_label.pack(pady=5)

root.mainloop()
