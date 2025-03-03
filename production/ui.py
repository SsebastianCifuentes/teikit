# ui.py
import tkinter as tk
import time

def open_locker_ui(locker_number):
    print(f"Abriendo casillero {locker_number}...")  # Simulación de apertura
    time.sleep(3)
    print(f"Casillero {locker_number} abierto.")

def open_all_lockers_ui():
    print("Abriendo todos los casilleros...")
    for i in range(1, 17):
        open_locker_ui(i)

def start_ui():
    def on_closing():
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.overrideredirect(True)  # Ventana sin borde
    root.protocol("WM_DELETE_WINDOW", on_closing)

    close_button = tk.Button(
        root,
        text="Cerrar",
        font=("Helvetica", 20),
        command=on_closing
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    open_all_button = tk.Button(
        root,
        text="Abrir Todos los Casilleros",
        font=("Helvetica", 20),
        command=open_all_lockers_ui
    )
    open_all_button.grid(row=0, column=1, padx=10, pady=10)

    for i in range(1, 17):
        button = tk.Button(
            root,
            text=f"Casillero {i}",
            font=("Helvetica", 20),
            command=lambda ln=i: open_locker_ui(ln)
        )
        button.grid(row=(i-1)//4 + 1, column=(i-1)%4, padx=10, pady=10, sticky="nsew")

    root.mainloop()
