from flask import Flask, request, jsonify, abort
import RPi.GPIO as GPIO
import time
import os
from dotenv import load_dotenv
from signal import signal, SIGINT

# Cargar configuración del token desde variables de entorno
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN no configurado en las variables de entorno")

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

# Diccionario que mapea números de casilleros a pines GPIO
relay_pins = {1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26, 
              9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40}

# Configurar los pines GPIO
def configure_gpio(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

configure_gpio(relay_pins.values())

# Middleware para verificar el token de autorización
@app.before_request
def verify_token():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        abort(401, description="Acceso no autorizado")

# Ruta principal con información sobre las rutas disponibles
@app.route('/')
def index():
    return jsonify({"routes": {
        "/opening": "POST - Abre un casillero. Requiere 'casillero' en el cuerpo JSON."
    }})

# Ruta para abrir un casillero
@app.route('/opening', methods=['POST'])
def open_locker():
    try:
        data = request.get_json()
        if not data or 'casillero' not in data:
            abort(400, description="El cuerpo de la solicitud debe incluir 'casillero'")

        locker = data.get('casillero')
        if not isinstance(locker, int) or locker not in relay_pins:
            abort(400, description="Número de casillero inválido")

        pin = relay_pins[locker]
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(pin, GPIO.LOW)

        return jsonify({"status": f"Casillero {locker} abierto con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Función para limpiar los pines GPIO al cerrar la aplicación
def cleanup_gpio(signal_received, frame):
    GPIO.cleanup()
    print("GPIO limpiado y aplicación cerrada")
    exit(0)

# Asignar la señal de interrupción (Ctrl+C) para limpiar los GPIO
signal(SIGINT, cleanup_gpio)

# Iniciar el servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000)
