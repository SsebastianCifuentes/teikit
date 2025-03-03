# ui.py
import tkinter as tk
import RPi.GPIO as GPIO
from threading import Thread
from gpio_controller import open_locker_gpio, open_all_lockers_gpio, relay_pins, TOTAL_LOCKERS
from api_communicator import notify_external_api, notify_all_lockers_open

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
        for i, locker_number in enumerate(relay_pins.keys(), start=1):
            button = root.grid_slaves(row=i // 4 + 1, column=i % 4)[0]
            state = locker_states[locker_number]
            button.config(text=f"Casillero {locker_number} ({state})", bg="green" if state == "abierto" else "red")
        root.after(1000, update_button_states)  # Actualizar cada 1 segundo

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")

    # Configurar el fondo
    root.configure(bg='#f0f0f0')  # Fondo gris claro de la ventana

    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un botón de "Cerrar" que estará en la parte superior de la ventana
    close_button = tk.Button(
        root, text="Cerrar", font=("Helvetica", 18, "bold"), command=on_closing,
        bg="#f54c09", fg="white", relief="flat", width=10, height=2
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Crear un botón para abrir todos los casilleros
    open_all_button = tk.Button(
        root, text="Abrir Todos los Casilleros", font=("Helvetica", 20), command=open_all_lockers_ui,
        bg="#808080", fg="white", relief="flat", width=20, height=2
    )
    open_all_button.grid(row=0, column=1, padx=10, pady=10)

    # Configurar la cuadrícula para los botones de los casilleros
    for i in range(TOTAL_LOCKERS // 4 + 1):
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):
        root.grid_columnconfigure(j, weight=1)

    # Crear botones para cada casillero con colores personalizados
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        row, col = (i - 1) // 4, (i - 1) % 4
        button = tk.Button(
            root, text=f"Casillero {locker_number}", font=("Helvetica", 20),
            command=lambda ln=locker_number: open_locker_ui(ln),
            bg="#808080", fg="white", relief="flat", width=12, height=2
        )
        button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")
        
        # Efectos hover
        def on_hover(event):
            event.widget.config(bg="#666666")

        def on_leave(event):
            event.widget.config(bg="#808080")

        button.bind("<Enter>", on_hover)
        button.bind("<Leave>", on_leave)

    update_button_states()  # Iniciar actualización periódica de los botones
    root.mainloop()
