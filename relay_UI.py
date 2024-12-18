import RPi.GPIO as GPIO
import tkinter as tk

GPIO.setmode(GPIO.BOARD)
relay_pins = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

# Función para alternar el estado de un relé
def toggle_relay(relay_pin, button, status_label):
    GPIO.output(relay_pin, not GPIO.input(relay_pin))
    update_status(relay_pin, status_label)
    update_button_color(relay_pin, button)

# Función para actualizar el color del botón según el estado del relé
def update_button_color(relay_pin, button):
    if GPIO.input(relay_pin) == GPIO.HIGH:
        button.config(bg="green")  # Verde cuando está activado
    else:
        button.config(bg="gray")  # Gris cuando está desactivado

# Configuración inicial de los pines GPIO
def setup_gpio():
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Función para crear un botón con comportamiento adaptable
def create_button(relay_pin, root, status_label):
    # Crear el botón
    button = tk.Button(root, text=f"Relé {relay_pin + 1}", font=("Helvetica", 30), command=lambda p=relay_pin, b=None: toggle_relay(relay_pins[p], b, status_label))
    
    # Configurar la fila y la columna
    row, col = relay_pin // 4, relay_pin % 4
    button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")  # +1 para dejar espacio para la etiqueta de estado
    
    # Actualizar el color del botón en función del estado inicial del relé
    update_button_color(relay_pin, button)

    return button

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
        root.title("Relé UI - Teikit")  # Cambié el título
        root.geometry("1000x600")
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

        # Crear botones para cada relé
        buttons = []
        for i in range(len(relay_pins)):
            button = create_button(i, root, status_label)
            buttons.append(button)

        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
