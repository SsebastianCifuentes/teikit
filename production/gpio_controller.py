import RPi.GPIO as GPIO

# Configuración centralizada de GPIO (solo ejecutar una vez)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  # Desactivar advertencias

relay_pins = {
    1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26,
    9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40
}

# Inicializar pines solo si no están configurados
for pin in relay_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

TOTAL_LOCKERS = len(relay_pins)

def turn_on_locker(locker_number):
    pin = relay_pins.get(locker_number)
    if pin:
        GPIO.output(pin, GPIO.HIGH)

def turn_off_locker(locker_number):
    pin = relay_pins.get(locker_number)
    if pin:
        GPIO.output(pin, GPIO.LOW)