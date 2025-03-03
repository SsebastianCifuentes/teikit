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
            button.config(bg="white", fg="#000000")  # Texto negro
        root.after(1000, update_button_states)

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")
    root.configure(bg='#f54c09')  # Fondo naranja

    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un Frame para la parte superior
    top_frame = tk.Frame(root, bg='#f54c09')
    top_frame.pack(side="top", fill="x", pady=10)

    # Crear un Frame para los botones de los casilleros
    bottom_frame = tk.Frame(root, bg='#f54c09')
    bottom_frame.pack(expand=True, fill="both", pady=10)

    # Tamaño estándar para los botones de los casilleros
    button_width = 14
    button_height = 3
    button_font = ("Arial", 18, "bold")

    # Tamaño más pequeño para "Cerrar" y "Apertura Total"
    small_button_width = 10
    small_button_height = 2
    small_button_font = ("Arial", 14, "bold")

    # Bordes redondeados → Simulación con padding y colores suaves
    button_style = {
        "relief": "flat",
        "borderwidth": 0,
        "width": button_width,
        "height": button_height,
        "font": button_font,
        "bg": "white",
        "fg": "#000000"
    }

    # Botón "Cerrar" con fondo rojo
    close_button = tk.Button(
        top_frame, text="Cerrar", font=small_button_font, command=on_closing,
        bg="#ff4d4d", fg="white", relief="flat",
        width=small_button_width, height=small_button_height,
        borderwidth=2, highlightbackground="#b30000", highlightthickness=2
    )
    close_button.pack(side="left", padx=20)

    # Botón "Apertura Total" con fondo verde
    open_all_button = tk.Button(
        top_frame, text="Apertura Total", font=small_button_font, command=open_all_lockers_ui,
        bg="#4caf50", fg="white", relief="flat",
        width=small_button_width, height=small_button_height,
        borderwidth=2, highlightbackground="#2e7d32", highlightthickness=2
    )
    open_all_button.pack(side="left", padx=20)

    # Cargar y escalar el logo al 70%
    logo = Image.open("teikit_banner.png")
    width, height = logo.size
    new_size = (int(width * 0.7), int(height * 0.7))
    logo = logo.resize(new_size, Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)

    # Colocar el logo en la parte derecha del `top_frame`
    logo_label = tk.Label(top_frame, image=logo, bg='#f54c09')
    logo_label.pack(side="right", padx=20)

    # Diccionario para mapear botones con casilleros
    button_map = {}

    # Crear botones para cada casillero dentro de `bottom_frame`
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        button = tk.Button(
            bottom_frame, text=f"Casillero {locker_number}", **button_style
        )
        button.config(command=lambda ln=locker_number: open_locker_ui(ln))
        button.grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=10, pady=10, sticky="nsew")
        button_map[button] = locker_number

    # Configurar distribución uniforme en la cuadrícula de `bottom_frame`
    for i in range((TOTAL_LOCKERS // 4) + 1):
        bottom_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        bottom_frame.grid_columnconfigure(j, weight=1)

    update_button_states()
    root.mainloop()
