#start_server.py
import subprocess
import time
import sys
from threading import Thread
from ui import start_ui
from gpio_controller import cleanup_gpio

# Variables globales para los procesos
flask_process = None
ngrok_process = None

def start_flask():
    global flask_process
    flask_process = subprocess.Popen([
        "gunicorn", 
        "-w", "1",
        "-b", "0.0.0.0:5000", 
        "--preload", 
        "app:app"
    ])

def start_ngrok():
    global ngrok_process
    time.sleep(3)
    ngrok_process = subprocess.Popen([
        "ngrok", 
        "http", 
        "--url", "nicely-valued-chimp.ngrok-free.app", 
        "5000"
    ])

def cleanup():
    print("Cerrando aplicación...")
    
    if ngrok_process:
        ngrok_process.terminate()
        try:
            ngrok_process.wait(timeout=5) 
        except subprocess.TimeoutExpired:
            ngrok_process.kill() 
    
    if flask_process:
        flask_process.terminate()
        try:
            flask_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            flask_process.kill()
    
    cleanup_gpio()
    print("Aplicación cerrada correctamente.")
    sys.exit(0)

if __name__ == "__main__":
    start_flask()
    start_ngrok()
    start_ui()