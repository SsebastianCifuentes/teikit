import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from gpio_controller import open_locker_gpio, open_all_lockers_gpio, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open
from PIL import Image, ImageTk, ImageDraw

locker_states = {locker: "cerrado" for locker in relay_pins}

def create_rounded_button(canvas, text, command, x, y, width, height, bg_color, text_color):
    """
    Crea un botón redondeado usando Canvas.
    """
    radius = 25  # Radio de las esquinas redondeadas
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Dibujar un rectángulo con bordes redondeados
    draw.rounded_rectangle((0, 0, width, height), radius, fill=bg_color)
    
    # Convertir la imagen a formato Tkinter
    img_tk = ImageTk.PhotoImage(img)
    
    # Crear botón en Canvas
    button_id = canvas.create_image(x, y, anchor="nw", image=img_tk)
    text_id = canvas.create_text(x + width // 2, y + height // 2, text=text, font=("Arial", 14, "bold"), fill=text_color)

    def on_click(event):
        command()

    # Asociar la acción al botón
    canvas.tag_bind(button_id, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)

    # Mantener referencia a la imagen para evitar que se borre
    canvas.image_refs.append(img_tk)

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

    # Crear un Canvas en lugar de un Frame
    top_canvas = tk.Canvas(root, bg='#f54c09', highlightthickness=0)
    top_canvas.pack(side="top", fill="x", pady=10)
    top_canvas.image_refs = []  # Para evitar que las imágenes se borren

    # Crear un Frame para los botones de los casilleros
    bottom_frame = tk.Frame(root, bg='#f54c09')
    bottom_frame.pack(expand=True, fill="both", pady=10)

    # Tamaño estándar para los botones de los casilleros
    button_width = 14
    button_height = 3
    button_font = ("Arial", 18, "bold")

    # Tamaño más pequeño para "Cerrar" y "Apertura Total"
    small_button_width = 150
    small_button_height = 50

    # Crear botones redondeados
    create_rounded_button(top_canvas, "Cerrar", on_closing, 20, 10, small_button_width, small_button_height, "#ff4d4d", "white")
    create_rounded_button(top_canvas, "Apertura Total", open_all_lockers_ui, 200, 10, small_button_width, small_button_height, "#4caf50", "white")

    # Cargar y escalar el logo al 70%
    logo = Image.open("teikit_banner.png")
    width, height = logo.size
    new_size = (int(width * 0.7), int(height * 0.7))
    logo = logo.resize(new_size, Image.Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo)

    # Colocar el logo en la parte derecha del `top_canvas`
    logo_label = tk.Label(root, image=logo, bg='#f54c09')
    logo_label.place(x=screen_width - new_size[0] - 20, y=10)

    # Diccionario para mapear botones con casilleros
    button_map = {}

    # Estilo de los botones de los casilleros
    button_style = {
        "relief": "flat",
        "borderwidth": 0,
        "width": button_width,
        "height": button_height,
        "font": button_font,
        "bg": "white",
        "fg": "#000000"
    }

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
