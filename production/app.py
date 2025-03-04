import RPi.GPIO as GPIO
from flask import Flask, request, jsonify, abort
from signal import signal, SIGINT
from ui import start_ui, open_locker_ui, open_all_lockers_ui
from gpio_controller import open_all_lockers
from config import API_TOKEN
from threading import Thread
import time

# Configuración de la API Flask
app = Flask(__name__)

@app.before_request
def verify_token():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        abort(401, description="Acceso no autorizado")

@app.route('/')
def index():
    return jsonify({"routes": {
        "/locker": "GET - Devuelve el número total de casilleros.",
        "/locker/opening": "POST - Abre un casillero específico vía API.",
        "/locker/opening/all": "POST - Abre todos los casilleros."
    }})

@app.route('/locker', methods=['GET'])
def get_locker_count():
    return jsonify({"total_lockers": TOTAL_LOCKERS}), 200

@app.route('/locker/opening', methods=['POST'])
def open_locker():
    data = request.get_json()
    if not data or 'casillero' not in data:
        abort(400, description="El cuerpo de la solicitud debe incluir 'casillero'")

    locker = data.get('casillero')
    if not isinstance(locker, int) or locker < 1 or locker > TOTAL_LOCKERS:
        abort(400, description=f"Casillero inválido. Seleccione entre 1 y {TOTAL_LOCKERS}.")

    open_locker_ui(locker)
    return jsonify({"status": f"Casillero {locker} abierto con éxito"}), 200

@app.route('/locker/opening/all', methods=['POST'])
def open_all_lockers_api():
    try:
        open_all_lockers()
        return jsonify({"status": "Todos los casilleros han sido abiertos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def cleanup_gpio(signal_received, frame):
    GPIO.cleanup()
    print("GPIO limpiado y aplicación cerrada")
    os._exit(0)

signal(SIGINT, cleanup_gpio)

if __name__ == '__main__':
    # Solo se ejecuta cuando se inicia directamente (no con Gunicorn)
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup_gpio(None, None)