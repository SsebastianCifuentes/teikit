import RPi.GPIO as GPIO
import tkinter as tk

GPIO.setmode(GPIO.BOARD)
# Lista de pines GPIO para los relés, en el orden que corresponden a los números de relé (1-16)
relay_pins = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

# Función para alternar el estado de un relé
def toggle_relay(relay_index, button):
    relay_pin = relay_pins[relay_index]
    GPIO.output(relay_pin, not GPIO.input(relay_pin))  # Cambiar el estado del pin
    update_button_color(relay_index, button)  # Actualizar color del botón
    print(f"Relay {relay_index + 1} toggled.")  # Mostrar el número de relé (1-16)

# Función para configurar los pines GPIO como salidas
def setup_gpio():
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)  # Inicializar todos los relés apagados

# Función para crear un botón en la interfaz gráfica para cada relé
def create_button(relay_index, root):
    button = tk.Button(
        root,
        text=f"Relay {relay_index + 1}",  # Mostrar número de relé (1-16)
        command=lambda i=relay_index, b=button: toggle_relay(i, b),  # Pasar índice del relé
        width=10,
        height=2,
    )
    button.grid(row=relay_index // 4, column=relay_index % 4, padx=10, pady=10)
    update_button_color(relay_index, button)  # Actualizar color del botón al crearlo
    return button

# Función para actualizar el color del botón según el estado del relé
def update_button_color(relay_index, button):
    relay_pin = relay_pins[relay_index]
    if GPIO.input(relay_pin) == GPIO.HIGH:
        button.config(bg="grey")  # Relé apagado (HIGH)
    else:
        button.config(bg="green")  # Relé encendido (LOW)

# Función para limpiar los recursos al cerrar la ventana
def on_closing():
    GPIO.cleanup()
    root.destroy()

# Función principal que configura la interfaz y controla los relés
def main():
    try:
        global root
        # Crear la ventana principal de la interfaz gráfica con un tamaño adecuado
        root = tk.Tk()
        root.title("Relay UI - Teikit")
        root.geometry("400x400")  # Tamaño ajustado de la ventana
        root.protocol("WM_DELETE_WINDOW", on_closing)

        setup_gpio()

        # Crear los botones para cada relé
        for i in range(len(relay_pins)):
            create_button(i, root)

        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
