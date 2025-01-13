import RPi.GPIO as GPIO
import tkinter as tk
import requests
import time
import os
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from signal import signal, SIGINT
from threading import Thread, Lock

# Cargar configuración del token desde variables de entorno
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API = os.getenv("EXTERNAL_API")
if not API_TOKEN or not EXTERNAL_API:
    raise ValueError("API_TOKEN o EXTERNAL_API no configurados en las variables de entorno")

# Número total de casilleros
TOTAL_LOCKERS = 16  # Número total de casilleros

# Diccionario que mapea números de casilleros a pines GPIO
relay_pins = {1: 7, 2: 12, 3: 15, 4: 16, 5: 18, 6: 22, 7: 24, 8: 26,
              9: 31, 10: 32, 11: 33, 12: 35, 13: 36, 14: 37, 15: 38, 16: 40}

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BOARD)
def configure_gpio(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

configure_gpio(relay_pins.values())

# Bloqueo para acceso seguro a GPIO
gpio_lock = Lock()

# Función compartida para manejar GPIO
def control_gpio(locker_number=None, all_lockers=False):
    with gpio_lock:  # Asegurar acceso exclusivo
        if all_lockers:
            print("Abriendo todos los casilleros")
            for pin in relay_pins.values():
                GPIO.output(pin, GPIO.HIGH)
            time.sleep(3)
            for pin in relay_pins.values():
                GPIO.output(pin, GPIO.LOW)
            print("Todos los casilleros cerrados")
        elif locker_number:
            pin = relay_pins[locker_number]
            print(f"Abriendo casillero {locker_number} en pin {pin}")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(pin, GPIO.LOW)
            print(f"Casillero {locker_number} cerrado")

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
        control_gpio(locker_number=locker_number)
        notify_external_api(locker_number)

    def on_closing():
        GPIO.cleanup()
        root.destroy()

    root = tk.Tk()
    root.title("Relé UI - Teikit")
    
    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Establecer el tamaño de la ventana a la resolución de la pantalla
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    # Configurar la ventana para que sea borderless
    root.overrideredirect(True)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crear un botón de "Cerrar"
    close_button = tk.Button(
        root,
        text="Cerrar",
        font=("Helvetica", 20),
        command=on_closing
    )
    close_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Configurar la cuadrícula para los botones de los casilleros
    for i in range(TOTAL_LOCKERS // 4 + 1):
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):
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
        button.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nsew")

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
    try:
        data = request.get_json()
        if not data or 'casillero' not in data:
            abort(400, description="El cuerpo de la solicitud debe incluir 'casillero'")

        locker = data.get('casillero')
        if not isinstance(locker, int) or locker < 1 or locker > TOTAL_LOCKERS:
            abort(400, description=f"Casillero inválido. Seleccione entre 1 y {TOTAL_LOCKERS}.")

        control_gpio(locker_number=locker)

        return jsonify({"status": f"Casillero {locker} abierto con éxito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/locker/opening/all', methods=['POST'])
def open_all_lockers():
    try:
        control_gpio(all_lockers=True)
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
    try:
        Thread(target=start_ui, daemon=True).start()
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
