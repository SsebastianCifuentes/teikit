import RPi.GPIO as GPIO
import tkinter as tk

GPIO.setmode(GPIO.BOARD)
relay_pins = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

# Función para alternar el estado de un relé
def toggle_relay(relay_pin, status_label):
    GPIO.output(relay_pin, not GPIO.input(relay_pin))
    update_status(relay_pin, status_label)

# Función para configurar los pines GPIO como salidas
def setup_gpio():
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# Función para crear un botón en la interfaz gráfica para cada relé
def create_button(relay_pin, root, status_label, relay_index):
    button = tk.Button(
        root, 
        text=f"Relay {relay_index + 1}", 
        command=lambda p=relay_pin: toggle_relay(p, status_label)
    )
    button.grid(row=relay_index // 4, column=relay_index % 4, padx=10, pady=10)

# Función para actualizar el estado del relé en la interfaz gráfica
def update_status(relay_pin, status_label):
    status = "ON" if GPIO.input(relay_pin) == GPIO.HIGH else "OFF"
    status_label.config(text=f"Relay {relay_pins.index(relay_pin) + 1}: {status}")

# Función para limpiar los recursos al cerrar la ventana
def on_closing():
    GPIO.cleanup()
    root.destroy()

# Función principal que configura la interfaz y controla los relés
def main():
    try:
        global root
        # Crea la ventana principal de la interfaz gráfica
        root = tk.Tk()
        root.title("Relay UI - Teikit")
        root.geometry("1024x600")  
        root.protocol("WM_DELETE_WINDOW", on_closing)

        setup_gpio()

        # Crea una etiqueta para mostrar el estado de los relés
        status_label = tk.Label(root, text="", font=("Helvetica", 16))
        status_label.grid(row=len(relay_pins) // 4, columnspan=4)

        # Crea los botones para cada relé y actualiza su estado
        for i, relay_pin in enumerate(relay_pins):
            create_button(relay_pin, root, status_label, i)
            update_status(relay_pin, status_label)

        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
