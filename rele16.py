import RPi.GPIO as GPIO
import time

# Configuración de la biblioteca RPi.GPIO
GPIO.setmode(GPIO.BOARD)

# Lista de pines GPIO conectados a los relés
pines_relays = [3, 16, 5, 12, 7, 11, 8, 10, 15, 18, 19, 21, 22, 24, 26, 32]

try:
    # Configuración de los pines GPIO como salidas
    for pin in pines_relays:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    while True:
        print("Seleccione un relé (1-16) o presione 'q' para salir:")
        seleccion = input()

        if seleccion.lower() == 'q':
            break

        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= 16:
                # Activar el relé seleccionado
                GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
                print(f"Relé {seleccion} activado.")
                
                # Esperar un momento (puedes ajustar según sea necesario)
                time.sleep(3)
                
                # Desactivar el relé
                GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
                print(f"Relé {seleccion} desactivado.")
            else:
                print("Seleccione un número entre 1 y 16.")
        except ValueError:
            print("Entrada no válida. Introduzca un número entre 1 y 16.")
except KeyboardInterrupt:
    pass
finally:
    # Limpiar la configuración de los pines GPIO al salir
    GPIO.cleanup()
