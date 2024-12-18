import RPi.GPIO as GPIO
import tkinter as tk

GPIO.setmode(GPIO.BOARD)
relay_pins = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

# Función para alternar el estado de un relé
def toggle_relay(relay_pin, status_label):
    GPIO.output(relay_pin, not GPIO.input(relay_pin))
    update_status(relay_pin, status_label)

# Configuración inicial de los pines GPIO
def setup_gpio():
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Función para crear un botón con comportamiento adaptable
def create_button(relay_pin, root, status_label):
    button = tk.Button(root, text=f"Relé {relay_pin + 1}", font=("Helvetica", 30), command=lambda p=relay_pin: toggle_relay(relay_pins[p], status_label))
    row, col = relay_pin // 4, relay_pin % 4
    button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")  # Configura sticky para que el botón se expanda

# Función para actualizar el estado del relé
def update_status(relay_pin, status_label):
    status = "ACTIVADO" if GPIO.input(relay_pin) == GPIO.HIGH else "DESACTIVADO"
    status_label.config(text=f"Relé {relay_pins.index(relay_pin) + 1}: {status}")

# Función para liberar los recursos al cerrar la ventana
def on_closing():
    GPIO.cleanup()
    root.destroy()

# Configuración principal
def main():
    try:
        global root
        root = tk.Tk()
        root.title("Relay UI - Teikit")
        root.geometry("900x500")
        root.protocol("WM_DELETE_WINDOW", on_closing)

        root.bind("<Escape>", lambda event: on_closing())
        setup_gpio()

        # Configura pesos de las filas y columnas
        for i in range(len(relay_pins) // 4 + 2):  # +2 para incluir la fila de la etiqueta de estado
            root.grid_rowconfigure(i, weight=1)
        for j in range(4):  # Máximo 4 columnas
            root.grid_columnconfigure(j, weight=1)

        # Etiqueta de estado en la primera fila
        status_label = tk.Label(root, text="", font=("Helvetica", 30))
        status_label.grid(row=0, columnspan=4, sticky="ew")

        # Crea botones para cada relé, empezando desde la segunda fila
        for i in range(len(relay_pins)):
            row, col = (i // 4) + 1, i % 4  # +1 para dejar espacio para la etiqueta de estado
            button = tk.Button(root, text=f"Relay {i + 1}", font=("Helvetica", 30), command=lambda p=i: toggle_relay(relay_pins[p], status_label))
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            update_status(relay_pins[i], status_label)

        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
