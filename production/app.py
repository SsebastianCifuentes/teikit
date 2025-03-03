# app.py
import RPi.GPIO as GPIO
from flask import Flask, request, jsonify, abort
from signal import signal, SIGINT
from gpio_controller import open_locker_gpio, open_all_lockers_gpio
from api_communicator import notify_external_api, notify_all_lockers_open
from ui import start_ui
from config import API_TOKEN, EXTERNAL_API 
from threading import Thread

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

    open_locker_gpio(locker)
    return jsonify({"status": f"Casillero {locker} abierto con éxito"}), 200

@app.route('/locker/opening/all', methods=['POST'])
def open_all_lockers():
    try:
        open_all_lockers_gpio()
        return jsonify({"status": "Todos los casilleros han sido abiertos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def cleanup_gpio(signal_received, frame):
    GPIO.cleanup()
    print("GPIO limpiado y aplicación cerrada")
    exit(0)

signal(SIGINT, cleanup_gpio)

if __name__ == '__main__':
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    flask_thread.daemon = True
    flask_thread.start()

    start_ui()
