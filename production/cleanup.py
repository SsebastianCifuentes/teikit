# cleanup.py
import subprocess
import sys
from gpio_controller import cleanup_gpio

# Variables globales para los procesos
flask_process = None
ngrok_process = None

def set_processes(flask_proc, ngrok_proc):
    """Establece las referencias a los procesos de Flask y Ngrok."""
    global flask_process, ngrok_process
    flask_process = flask_proc
    ngrok_process = ngrok_proc

def cleanup():
    """Cierra todos los procesos y libera recursos."""
    print("Cerrando aplicación...")
    
    # Cerrar Ngrok
    if ngrok_process:
        ngrok_process.terminate()
        try:
            ngrok_process.wait(timeout=5)  # Esperar hasta 5 segundos
        except subprocess.TimeoutExpired:
            ngrok_process.kill()  # Fuerza el cierre si no responde
    
    # Cerrar Flask
    if flask_process:
        flask_process.terminate()
        try:
            flask_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            flask_process.kill()
    
    # Limpiar GPIO
    cleanup_gpio()
    print("Aplicación cerrada correctamente.")
    sys.exit(0)