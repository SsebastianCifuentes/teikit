import tkinter as tk
from threading import Thread
from gpio_controller import turn_on_locker, turn_off_locker, relay_pins, TOTAL_LOCKERS, open_all_lockers
from PIL import Image, ImageTk
import time

button_map = {}

def update_button_ui(root, locker_number, state):
    button = button_map[locker_number]
    color = "green" if state else "white"
    fg_color = "white" if state else "#000000"
    button.config(bg=color, fg=fg_color)
    root.update_idletasks()

def open_locker_ui(locker_number, button):
    def task():
        button.config(bg="green", fg="white")
        turn_on_locker(locker_number)
        time.sleep(2)
        turn_off_locker(locker_number)
        button.config(bg="white", fg="#000000")
    Thread(target=task, daemon=True).start()

def open_all_lockers_ui(root):
    def task():
        try:
            # Apertura secuencial
            for locker in relay_pins.keys():
                turn_on_locker(locker)
                update_button_ui(root, locker, True)
                time.sleep(0.5)
            
            time.sleep(2)  # Tiempo de apertura total
            
            # Cierre secuencial
            for locker in relay_pins.keys():
                turn_off_locker(locker)
                update_button_ui(root, locker, False)
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error en apertura total: {e}")
    Thread(target=task, daemon=True).start()

def start_ui():
    root = tk.Tk()
    root.title("Control de Casilleros - Teikit")
    root.configure(bg='#f54c09')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.overrideredirect(True)

    # Frame superior
    top_frame = tk.Frame(root, bg='#f54c09')
    top_frame.pack(side="top", fill="x", pady=10)

    # Botón de cierre
    close_button = tk.Button(
        top_frame, 
        text="Cerrar", 
        command=lambda: [root.destroy(), GPIO.cleanup()],
        bg="#ff4d4d", 
        fg="white",
        width=10,
        height=2,
        font=("Arial", 14, "bold")
    )
    close_button.pack(side="left", padx=20)

    # Botón de apertura total
    open_all_button = tk.Button(
        top_frame,
        text="Apertura Total",
        command=lambda: open_all_lockers_ui(root),
        bg="#4caf50",
        fg="white",
        width=10,
        height=2,
        font=("Arial", 14, "bold")
    )
    open_all_button.pack(side="left", padx=20)

    # Logo (sección corregida)
    try:
        logo = Image.open("teikit_banner.png")
        new_width = int(logo.width * 0.7)
        new_height = int(logo.height * 0.7)
        logo = logo.resize((new_width, new_height), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(top_frame, image=logo, bg='#f54c09')
        logo_label.image = logo  # Mantener referencia
        logo_label.pack(side="right", padx=20)
    except Exception as e:
        print(f"Error cargando logo: {e}")

    # Botones de casilleros
    bottom_frame = tk.Frame(root, bg='#f54c09')
    bottom_frame.pack(expand=True, fill="both", pady=10)
    
    button_style = {
        "relief": "flat",
        "borderwidth": 0,
        "width": 14,
        "height": 3,
        "font": ("Arial", 18, "bold"),
        "bg": "white",
        "fg": "#000000"
    }

    for i, locker in enumerate(relay_pins.keys(), 1):
        btn = tk.Button(
            bottom_frame,
            text=f"Casillero {locker}",
            command=lambda ln=locker: open_locker_ui(ln, button_map[ln]),
            **button_style
        )
        btn.grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
        button_map[locker] = btn

    # Configurar grid
    for i in range((TOTAL_LOCKERS // 4) + 1):
        bottom_frame.grid_rowconfigure(i, weight=1)
    for j in range(4):
        bottom_frame.grid_columnconfigure(j, weight=1)

    root.protocol("WM_DELETE_WINDOW", lambda: [GPIO.cleanup(), root.destroy()])
    root.mainloop()

if __name__ == "__main__":
    start_ui()