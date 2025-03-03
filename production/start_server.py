# Archivo: start_services.py
import subprocess
import time
import signal
import sys

def start_flask():
    # Usar un solo worker para evitar conflictos con GPIO
    flask_command = ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
    return subprocess.Popen(flask_command)

def start_ngrok():
    ngrok_command = ["ngrok", "http", "--url", "nicely-valued-chimp.ngrok-free.app", "5000"]
    return subprocess.Popen(ngrok_command)

def start_ui():
    ui_command = ["python", "ui.py"]
    return subprocess.Popen(ui_command)

def signal_handler(sig, frame):
    # Detener todos los procesos al recibir señal de interrupción
    flask_process.terminate()
    ngrok_process.terminate()
    ui_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    flask_process = start_flask()
    ngrok_process = start_ngrok()
    ui_process = start_ui()

    # Configurar manejo de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Mantener el script activo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)