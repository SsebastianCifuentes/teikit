from flask import Flask, jsonify, abort, request
from gpio_controller import open_all_lockers, turn_on_locker, turn_off_locker, TOTAL_LOCKERS
from config import API_TOKEN
import RPi.GPIO as GPIO
import threading
import os

app = Flask(__name__)

@app.before_request
def verify_token():
    if request.headers.get('Authorization') != f"Bearer {API_TOKEN}":
        abort(401, "Acceso no autorizado")

@app.route('/locker/opening', methods=['POST'])
def handle_single():
    data = request.get_json()
    locker = data.get('casillero')
    
    if not (1 <= locker <= TOTAL_LOCKERS):
        abort(400, "Número de casillero inválido")
    
    def operation():
        turn_on_locker(locker)
        time.sleep(2)
        turn_off_locker(locker)
    
    threading.Thread(target=operation, daemon=True).start()
    return jsonify(status=f"Casillero {locker} activado")

@app.route('/locker/opening/all', methods=['POST'])
def handle_all():
    threading.Thread(target=open_all_lockers, daemon=True).start()
    return jsonify(status="Apertura total iniciada")

def cleanup(signal, frame):
    GPIO.cleanup()
    os._exit(0)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, cleanup)
    app.run(host='0.0.0.0', port=5000)