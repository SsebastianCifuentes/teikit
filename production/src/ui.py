#ui.py
import tkinter as tk
import RPi.GPIO as GPIO
import time
from threading import Thread
from gpio_controller import turn_on_locker, turn_off_locker, relay_pins, TOTAL_LOCKERS
from cleanup import cleanup
from PIL import Image, ImageTk

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
        
    thread = Thread(target=task, daemon=True)
    thread.start()

def open_all_lockers_ui(root):
    def update_button(locker_number, state):
        button = button_map[locker_number]
        color = "green" if state else "white"
        button.config(bg=color, fg="#000000" if not state else "white")
        root.update_idletasks()

    def open_locker(locker_number, delay):
        """Abre un casillero después de un retraso."""
        root.after(int(delay), lambda: turn_on_locker(locker_number))
        root.after(int(delay), lambda: update_button(locker_number, True))

    def close_locker(locker_number, delay):
        """Cierra un casillero después de un retraso."""
        root.after(int(delay), lambda: turn_off_locker(locker_number))
        root.after(int(delay), lambda: update_button(locker_number, False))

    try:
        # Abrir casilleros con retrasos progresivos
        for locker_number, delay in zip(relay_pins.keys(), [i * 500 for i in range(TOTAL_LOCKERS)]):
            open_locker(locker_number, delay)

        # Cerrar casilleros con retrasos progresivos después de 2 segundos
        for locker_number, delay in zip(relay_pins.keys(), [i * 500 + 2000 for i in range(TOTAL_LOCKERS)]):
            close_locker(locker_number, delay)

    except Exception as e:
        print(f"Error en la tarea: {e}")
        for locker_number in relay_pins.keys():
            update_button(locker_number, False)

def on_closing():
    cleanup()  # Llama a la función cleanup desde cleanup.py
    root.destroy()
    print("UI cerrada correctamente.")

def start_ui():
    root = tk.Tk()
    root.title("Apertura manual de casilleros - Teikit")
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
        top_frame, text="Apertura Total", font=small_button_font, command=lambda: open_all_lockers_ui(root),
        bg="#4caf50", fg="white", relief="flat",
        width=small_button_width, height=small_button_height,
        borderwidth=2, highlightbackground="#2e7d32", highlightthickness=2
    )
    open_all_button.pack(side="left", padx=20)

    logo = Image.open("../assets/teikit_banner.png")
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