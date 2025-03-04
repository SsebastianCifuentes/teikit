# gpio_controller
import RPi.GPIO as GPIO
import time

# Configuración única de GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

relay_pins = {
    1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26,
    9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40
}

TOTAL_LOCKERS = len(relay_pins)

# Inicializar pines solo una vez
for pin in relay_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def turn_on_locker(locker_number):
    pin = relay_pins.get(locker_number)
    if pin:
        GPIO.output(pin, GPIO.HIGH)

def turn_off_locker(locker_number):
    pin = relay_pins.get(locker_number)
    if pin:
        GPIO.output(pin, GPIO.LOW)

from threading import Thread
import time

def open_all_lockers_api():
    def open_and_close_locker(locker_number, delay):
        try:
            time.sleep(delay)
            turn_on_locker(locker_number)
            print(f"Casillero {locker_number} abierto a los {delay}s")
            time.sleep(2)
            turn_off_locker(locker_number)
            print(f"Casillero {locker_number} cerrado a los {delay + 2}s")
        
        except Exception as e:
            print(f"Error en el casillero {locker_number}: {e}")

    try:
        threads = []
        for locker_number, delay in zip(relay_pins.keys(), [i * 0.5 for i in range(TOTAL_LOCKERS)]):
            thread = Thread(target=open_and_close_locker, args=(locker_number, delay))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

    except Exception as e:
        print(f"Error al abrir todos los casilleros: {e}")