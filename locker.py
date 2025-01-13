import RPi.GPIO as GPIO
import tkinter as tk
import requests
import time
import os
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from signal import signal, SIGINT
from threading import Thread

# Cargar configuración del token desde variables de entorno
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API = os.getenv("EXTERNAL_API")
if not API_TOKEN or not EXTERNAL_API:
    raise ValueError("API_TOKEN o EXTERNAL_API no configurados en las variables de entorno")

# Configuración de GPIO y casilleros
relay_pins = {
    1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26,
    9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40
}
TOTAL_LOCKERS = len(relay_pins)

GPIO.setmode(GPIO.BOARD)
def setup_gpio(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

setup_gpio(relay_pins.values())

# Abrir un casillero por 3 segundos
def open_locker_gpio(locker_number):
    pin = relay_pins[locker_number]
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(pin, GPIO.LOW)

# Notificar a la API externa
def notify_external_api(locker_number):
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(
            EXTERNAL_API,
            json={"casillero": locker_number},
            headers=headers
        )
        if response.status_code == 200:
            print(f"Notificación enviada a la API externa: Casillero {locker_number}")
        else:
            print(f"Error al notificar a la API externa: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al intentar notificar a la API externa: {e}")

# --------------------------------------
# Configuración de la UI (Tkinter)
# --------------------------------------
def start_ui():
    def open_locker_ui(locker_number):
        open_locker_gpio(locker_number)
        notify_external_api(locker_number)

    def on_closing():
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")
    
    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana a la resolución de la pantalla
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Configurar la ventana para que sea borderless
    root.overrideredirect(True)  # Elimina el borde de la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un botón de "Cerrar" que estará en la parte superior de la ventana
    close_button = tk.Button(
        root,
        text="Cerrar",
        font=("Helvetica", 20),
        command=on_closing
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")  # Se coloca en la esquina superior izquierda

    # Configurar la cuadrícula para los botones de los casilleros
    for i in range(TOTAL_LOCKERS // 4 + 1):  # Configurar filas
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):  # Máximo 4 columnas
        root.grid_columnconfigure(j, weight=1)

    # Crear botones para cada casillero
    for i, locker_number in enumerate(relay_pins.keys(), start=1):
        row, col = (i - 1) // 4, (i - 1) % 4
        button = tk.Button(
            root,
            text=f"Casillero {locker_number}",
            font=("Helvetica", 20),
            command=lambda ln=locker_number: open_locker_ui(ln)
        )
        button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")  # Desplazar las filas para dejar espacio al botón de cerrar

    root.mainloop()


# --------------------------------------
# Configuración del Servidor Flask
# --------------------------------------
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
        for locker in relay_pins.keys():
            open_locker_gpio(locker)
        return jsonify({"status": "Todos los casilleros han sido abiertos"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def cleanup_gpio(signal_received, frame):
    GPIO.cleanup()
    print("GPIO limpiado y aplicación cerrada")
    exit(0)

signal(SIGINT, cleanup_gpio)

# --------------------------------------
# Iniciar Flask y Tkinter
# --------------------------------------
if __name__ == '__main__':
    start_ui()
    app.run(host='0.0.0.0', port=5000)