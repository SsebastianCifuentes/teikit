import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from gpio_controller import open_locker_gpio, open_all_lockers_gpio, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open
from PIL import Image, ImageTk  # Importar Pillow para manejar imágenes

locker_states = {locker: "cerrado" for locker in relay_pins}

def start_ui():
    def open_locker_ui(locker_number):
        def task():
            open_locker_gpio(locker_number)
            locker_states[locker_number] = "abierto"
            notify_external_api(locker_number)
        
        thread = Thread(target=task)
        thread.start()

    def open_all_lockers_ui():
        def task():
            open_all_lockers_gpio()
            locker_states.update({locker: "abierto" for locker in relay_pins})
            notify_all_lockers_open()
        
        thread = Thread(target=task)
        thread.start()

    def update_button_states():
        for button, locker_number in button_map.items():
            state = locker_states[locker_number]
            button.config(bg="white", fg="#f54c09")  # Color blanco con texto naranja
        root.after(1000, update_button_states)  # Actualizar cada 1 segundo

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")

    # Configurar el fondo naranja
    root.configure(bg='#f54c09')  # Fondo naranja

    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un botón de "Cerrar" que estará en la parte superior de la ventana
    close_button = tk.Button(
        root, text="Cerrar", font=("Arial", 18, "bold"), command=on_closing,
        bg="white", fg="#f54c09", relief="flat", width=10, height=2
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Crear un botón para abrir todos los casilleros con texto más corto
    open_all_button = tk.Button(
        root, text="Apertura Total", font=("Arial", 20, "bold"), command=open_all_lockers_ui,
        bg="white", fg="#f54c09", relief="flat", width=12, height=2
    )
    open_all_button.grid(row=0, column=1, padx=10, pady=10)

    # Cargar el logo
    logo = Image.open("teikit_banner.png")  
    logo = logo.resize((372, 125), Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)

    # Colocar el logo en el lado derecho
    logo_label = tk.Label(root, image=logo, bg='#f54c09')  # Usar el mismo color de fondo
    logo_label.grid(row=0, column=3, padx=10, pady=10, sticky="ne")

    # Configurar la cuadrícula para los botones de los casilleros
    for i in range(TOTAL_LOCKERS // 4 + 1):
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):
        root.grid_columnconfigure(j, weight=1)

    # Diccionario para mapear los botones con sus números de casillero
    button_map = {}

    # Crear botones para cada casillero con colores personalizados
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        row, col = (i - 1) // 4, (i - 1) % 4
        button = tk.Button(
            root, text=f"Casillero {locker_number}", font=("Arial", 20, "bold"),
            command=lambda ln=locker_number: open_locker_ui(ln),
            bg="white", fg="#f54c09", relief="flat", width=12, height=2
        )
        button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")
        
        # Guardar el botón en el diccionario
        button_map[button] = locker_number

    update_button_states()  # Iniciar actualización periódica de los botones
    root.mainloop()
