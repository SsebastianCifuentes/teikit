import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from gpio_controller import open_locker_gpio, open_all_lockers_gpio, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open
from PIL import Image, ImageTk

def create_rounded_button(parent, text, command, bg_color, text_color):
    """
    Crea un botón con bordes redondeados y animación al hacer clic.
    """
    def on_press(event):
        button.config(bg="#aaaaaa")  # Color temporal al presionar

    def on_release(event):
        button.config(bg=bg_color)
        command()

    button = tk.Button(
        parent, text=text, font=("Arial", 14, "bold"), bg=bg_color, fg=text_color,
        relief="ridge", width=12, height=2, borderwidth=5, highlightbackground="#000",
    )
    button.bind("<ButtonPress-1>", on_press)
    button.bind("<ButtonRelease-1>", on_release)
    return button

def start_ui():
    def open_locker_ui(locker_number):
        def task():
            open_locker_gpio(locker_number)
            notify_external_api(locker_number)
        
        thread = Thread(target=task)
        thread.start()

    def open_all_lockers_ui():
        def task():
            open_all_lockers_gpio()
            notify_all_lockers_open()
        
        thread = Thread(target=task)
        thread.start()

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")
    root.configure(bg='#f54c09')
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    top_frame = tk.Frame(root, bg='#f54c09')
    top_frame.pack(side="top", fill="x", pady=5)

    close_button = create_rounded_button(top_frame, "Cerrar", on_closing, "#ff4d4d", "white")
    close_button.pack(side="left", padx=10)

    open_all_button = create_rounded_button(top_frame, "Apertura Total", open_all_lockers_ui, "#4caf50", "white")
    open_all_button.pack(side="left", padx=10)

    logo = Image.open("teikit_banner.png")
    width, height = logo.size
    new_size = (int(width * 0.7), int(height * 0.7))
    logo = logo.resize(new_size, Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)

    logo_label = tk.Label(top_frame, image=logo, bg='#f54c09')
    logo_label.pack(side="right", padx=10)

    bottom_frame = tk.Frame(root, bg='#f54c09')
    bottom_frame.pack(expand=True, fill="both", pady=5)

    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        button = create_rounded_button(bottom_frame, f"Casillero {locker_number}", lambda ln=locker_number: open_locker_ui(ln), "white", "black")
        button.grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=8, pady=8, sticky="nsew")

    for i in range((TOTAL_LOCKERS // 4) + 1):
        bottom_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        bottom_frame.grid_columnconfigure(j, weight=1)

    root.mainloop()
