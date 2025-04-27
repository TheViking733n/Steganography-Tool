from tkinter import filedialog
import customtkinter
from steganography_cli import hide, unhide


# Configuration
RES_X, RES_Y = 1000, 700

# UI Setup
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.title("🕵️‍♂️ Steganography Tool 🧾")
app.geometry(f"{RES_X}x{RES_Y}")

# Variables (Use StringVars instead of globals)
input_img = customtkinter.StringVar()
input_text = customtkinter.StringVar()
output_img = customtkinter.StringVar(value="secret_image.png")
password_hide = customtkinter.StringVar()
password_unhide = customtkinter.StringVar()

# Functions
def hide_button():
    print("Hiding...")
    hide(input_img.get(), input_text.get(), output_img.get(), password_hide.get())
    print("Done Hiding")

def unhide_button():
    print("Unhiding...")
    unhide(output_img.get(), "extracted_text.txt", password_unhide.get())
    print("Done Unhiding")

def browse_file(var, filetypes):
    file = filedialog.askopenfile(mode="r", filetypes=filetypes)
    if file:
        print(f"Selected file: {file.name}")
        var.set(file.name)



# Fonts
header_font = customtkinter.CTkFont(size=32, weight="bold")
label_font = customtkinter.CTkFont(size=18)
button_font = customtkinter.CTkFont(size=18, weight="bold")

# Header
header = customtkinter.CTkLabel(app, text="🔐 Steganography: Hide & Reveal Text 🔍", font=header_font, justify="center")
header.pack(pady=10)

# Subheading
subheading_font = customtkinter.CTkFont(size=20, weight="normal")
subheading = customtkinter.CTkLabel(app, text="CS558: Cybersecurity Essentials - Course Project", font=subheading_font, justify="center")
subheading.pack()

# Frame Setup
main_frame = customtkinter.CTkFrame(app)
main_frame.pack(expand=True, fill="both", padx=40, pady=20)
main_frame.grid_columnconfigure((0, 1), weight=1)

# Description (animated)
description_font = customtkinter.CTkFont(size=16)
description_text = (
    "Steganography hides text inside images.\n"
    "Use this app to securely embed or extract text from images.\n"
    "To hide your secret text, select an image (jpg or png) and a text file, and then click on Hide.\n"
    "To get your text back, select the output image file and click on Unhide.\n"
    "You must provide a password while hiding or unhiding.\n"
    "Happy Hiding!"
)
description = customtkinter.CTkLabel(main_frame, text="", font=description_font, justify="center")
description.grid(row=0, column=0, columnspan=2, pady=(15, 20))

def typewriter(index=0):
    if index <= len(description_text):
        description.configure(text=description_text[:index])
        app.after(30, lambda: typewriter(index + 1))
    else:
        toggle_lock_icon()

app.after(500, typewriter)

lock_emojis = ["🔒", "🔓"]

def toggle_lock_icon():
    current_icon = lock_emojis[toggle_lock_icon.state % 2]
    toggle_lock_icon.state += 1
    description.configure(text=description_text + " " + current_icon)
    app.after(800, toggle_lock_icon)
toggle_lock_icon.state = 0

# Browse for Input Image
img_label = customtkinter.CTkLabel(main_frame, text="🖼️ Select Image File:", font=label_font, anchor="center")
img_label.grid(row=1, column=0, pady=10, sticky="e")
img_button = customtkinter.CTkButton(main_frame, text="📂 Browse Image", command=lambda: browse_file(input_img, [("PNG", "*.png"), ("JPG", "*.jpg")]), font=button_font)
img_button.grid(row=1, column=1, padx=20, sticky="w")

# Browse for Text File
text_label = customtkinter.CTkLabel(main_frame, text="📝 Select Text File:", font=label_font, anchor="center")
text_label.grid(row=2, column=0, pady=10, sticky="e")
text_button = customtkinter.CTkButton(main_frame, text="📂 Browse Text", command=lambda: browse_file(input_text, [("Text", "*.txt")]), font=button_font)
text_button.grid(row=2, column=1, padx=20, sticky="w")

# Password Entry for Hiding
password_label_hide = customtkinter.CTkLabel(main_frame, text="🔑 Enter Password (for Hiding):", font=label_font, anchor="center")
password_label_hide.grid(row=3, column=0, pady=10, sticky="e")
password_entry_hide = customtkinter.CTkEntry(main_frame, show="*", font=label_font, textvariable=password_hide)
password_entry_hide.grid(row=3, column=1, padx=20, sticky="w")

# Hide Button
hide_btn = customtkinter.CTkButton(main_frame, text="🔒 HIDE TEXT", command=hide_button, font=button_font, height=50, corner_radius=12)
hide_btn.grid(row=4, column=0, columnspan=2, pady=20)

# Browse for Output Image
out_img_label = customtkinter.CTkLabel(main_frame, text="🖼️ Select Encoded Image:", font=label_font, anchor="center")
out_img_label.grid(row=5, column=0, pady=10, sticky="e")
out_img_button = customtkinter.CTkButton(main_frame, text="📂 Browse Image", command=lambda: browse_file(output_img, [("PNG", "*.png"), ("JPG", "*.jpg")]), font=button_font)
out_img_button.grid(row=5, column=1, padx=20, sticky="w")

# Password Entry for Unhiding
password_label_unhide = customtkinter.CTkLabel(main_frame, text="🔑 Enter Password (for Unhiding):", font=label_font, anchor="center")
password_label_unhide.grid(row=6, column=0, pady=10, sticky="e")
password_entry_unhide = customtkinter.CTkEntry(main_frame, show="*", font=label_font, textvariable=password_unhide)
password_entry_unhide.grid(row=6, column=1, padx=20, sticky="w")

# Unhide Button
unhide_btn = customtkinter.CTkButton(main_frame, text="🔓 UNHIDE TEXT", command=unhide_button, font=button_font, height=50, corner_radius=12)
unhide_btn.grid(row=7, column=0, columnspan=2, pady=20)

# Footer
footer = customtkinter.CTkLabel(app, text="👨‍💻 Made with ❤️ by Group 16", font=label_font, justify="center")
footer.pack(pady=10)

app.mainloop()
