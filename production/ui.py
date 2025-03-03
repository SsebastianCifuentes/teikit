import tkinter as tk
import RPi.GPIO as GPIO  # Importar GPIO aquí
from threading import Thread
from gpio_controller import turn_on_locker, turn_off_locker, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open
from PIL import Image, ImageTk
import time

# Variables globales
button_map = {}

# Funciones de apertura de casilleros (ámbito global)
def open_locker_ui(locker_number, button=None):
    def task():
        if button:
            button.config(bg="green", fg="white")
        turn_on_locker(locker_number)
        time.sleep(2)
        turn_off_locker(locker_number)
        if button:
            button.config(bg="white", fg="#000000")
        notify_external_api(locker_number)
        
    thread = Thread(target=task, daemon=True)
    thread.start()

def open_all_lockers_ui():
    def open_locker_with_delay(locker_number, button, delay):
        def task():
            button.config(bg="green", fg="white")
            turn_on_locker(locker_number)
            time.sleep(2)
            turn_off_locker(locker_number)
            button.config(bg="white", fg="#000000")
            notify_external_api(locker_number)
        thread = Thread(target=task, daemon=True)
        thread.start()
        time.sleep(delay)

    def task():
        delay = 0.5
        for locker_number in relay_pins.keys():
            button = button_map[locker_number]
            open_locker_with_delay(locker_number, button, delay) 

        notify_all_lockers_open()

    thread = Thread(target=task, daemon=True)
    thread.start()

def start_ui():
    def on_closing():
        root.destroy()  # Cierra la ventana
        GPIO.cleanup()  # Limpia GPIO
        print("UI cerrada correctamente")

    root = tk.Tk()
    root.title("Relé UI - Teikit")
    root.configure(bg='#f54c09')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    top_frame = tk.Frame(root, bg='#f54c09')
    top_frame.pack(side="top", fill="x", pady=10)

    bottom_frame = tk.Frame(root, bg='#f54c09')
    bottom_frame.pack(expand=True, fill="both", pady=10)

    button_width = 14
    button_height = 3
    button_font = ("Arial", 18, "bold")
    small_button_width = 10
    small_button_height = 2
    small_button_font = ("Arial", 14, "bold")

    button_style = {
        "relief": "flat",
        "borderwidth": 0,
        "width": button_width,
        "height": button_height,
        "font": button_font,
        "bg": "white",
        "fg": "#000000"
    }

    close_button = tk.Button(
        top_frame, text="Cerrar", font=small_button_font, command=on_closing,
        bg="#ff4d4d", fg="white", relief="flat",
        width=small_button_width, height=small_button_height,
        borderwidth=2, highlightbackground="#b30000", highlightthickness=2
    )
    close_button.pack(side="left", padx=20)

    open_all_button = tk.Button(
        top_frame, text="Apertura Total", font=small_button_font, command=open_all_lockers_ui,
        bg="#4caf50", fg="white", relief="flat",
        width=small_button_width, height=small_button_height,
        borderwidth=2, highlightbackground="#2e7d32", highlightthickness=2
    )
    open_all_button.pack(side="left", padx=20)

    logo = Image.open("teikit_banner.png")
    width, height = logo.size
    new_size = (int(width * 0.7), int(height * 0.7))
    logo = logo.resize(new_size, Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)

    logo_label = tk.Label(top_frame, image=logo, bg='#f54c09')
    logo_label.pack(side="right", padx=20)

    # Crear botones para cada casillero
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        button = tk.Button(
            bottom_frame, text=f"Casillero {locker_number}", **button_style
        )
        button.config(command=lambda ln=locker_number, btn=button: open_locker_ui(ln, btn))
        button.grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=10, pady=10, sticky="nsew")
        button_map[locker_number] = button  # Actualiza el diccionario global

    for i in range((TOTAL_LOCKERS // 4) + 1):
        bottom_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        bottom_frame.grid_columnconfigure(j, weight=1)

    root.mainloop()

if __name__ == "__main__":
    start_ui()