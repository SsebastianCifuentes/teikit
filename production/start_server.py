import subprocess
import time
import os

# Ejecutar Flask con Gunicorn
def start_flask():
    flask_command = ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"] 
    subprocess.Popen(flask_command)

# Ejecutar Ngrok
def start_ngrok():
    ngrok_command = ["ngrok", "http", "--url", "nicely-valued-chimp.ngrok-free.app", "5000"]
    subprocess.Popen(ngrok_command)

if __name__ == "__main__":
    start_flask()
    time.sleep(2)
    start_ngrok()

    print("Servidor Flask con Gunicorn y Ngrok están corriendo...")
