# start_server.py
import subprocess
import time
from threading import Thread
from ui import start_ui
from cleanup import set_processes

def start_flask():
    """Inicia el servidor Flask usando Gunicorn."""
    flask_process = subprocess.Popen([
        "gunicorn", 
        "-w", "1",  # Un solo worker para evitar problemas con GPIO
        "-b", "0.0.0.0:5000", 
        "--preload", 
        "app:app"
    ])
    return flask_process

def start_ngrok():
    """Inicia Ngrok para acceso remoto."""
    time.sleep(3)  # Esperar que Flask esté listo
    ngrok_process = subprocess.Popen([
        "ngrok", 
        "http", 
        "--url", "nicely-valued-chimp.ngrok-free.app", 
        "5000"
    ])
    return ngrok_process

if __name__ == "__main__":
    # Iniciar Flask y Ngrok
    flask_process = start_flask()
    ngrok_process = start_ngrok()
    
    # Establecer las referencias a los procesos en cleanup.py
    set_processes(flask_process, ngrok_process)
    
    # Iniciar la interfaz gráfica
    start_ui()