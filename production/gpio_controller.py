# gpio_controller.py
import RPi.GPIO as GPIO
import time
from threading import Lock

# Configuración de GPIO y casilleros
relay_pins = {
    1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26,
    9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40
}

TOTAL_LOCKERS = len(relay_pins)

gpio_lock = Lock()
GPIO.setmode(GPIO.BOARD)

def setup_gpio(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

setup_gpio(relay_pins.values())

# Abrir un casillero por 3 segundos
def open_locker_gpio(locker_number):
    with gpio_lock:
        pin = relay_pins[locker_number]
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(pin, GPIO.LOW)

def open_all_lockers_gpio():
    for locker_number in relay_pins.keys():
        open_locker_gpio(locker_number)
