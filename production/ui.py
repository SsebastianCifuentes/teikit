# ui.py
import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from gpio_controller import open_locker_gpio, open_all_lockers_gpio, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open

def start_ui():
    def open_locker_ui(locker_number):
        Thread(target=lambda: (
            open_locker_gpio(locker_number),
            notify_external_api(locker_number)
        )).start()

    def open_all_lockers_ui():
        Thread(target=lambda: (
            open_all_lockers_gpio(),
            notify_all_lockers_open()
        )).start()

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")

    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana a la resolución de la pantalla
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Configurar la ventana para que sea borderless
    root.overrideredirect(True)  # Elimina el borde de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un botón de "Cerrar" que estará en la parte superior de la ventana
    close_button = tk.Button(
        root,
        text="Cerrar",
        font=("Helvetica", 20),
        command=on_closing
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  # Se coloca en la esquina superior izquierda

    # Crear un botón para abrir todos los casilleros
    open_all_button = tk.Button(
        root,
        text="Abrir Todos los Casilleros",
        font=("Helvetica", 20),
        command=open_all_lockers_ui
    )
    open_all_button.grid(row=0, column=1, padx=10, pady=10)

    # Configurar la cuadrícula para los botones de los casilleros
    for i in range(TOTAL_LOCKERS // 4 + 1):  # Configurar filas
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):  # Máximo 4 columnas
        root.grid_columnconfigure(j, weight=1)

    # Crear botones para cada casillero
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        row, col = (i - 1) // 4, (i - 1) % 4
        button = tk.Button(
            root,
            text=f"Casillero {locker_number}",
            font=("Helvetica", 20),
            command=lambda ln=locker_number: open_locker_ui(ln)
        )
        button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")  # Desplazar las filas para dejar espacio al botón de cerrar

    root.mainloop()
