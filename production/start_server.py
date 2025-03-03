import subprocess
import time
import signal
import sys

def start_flask():
    return subprocess.Popen([
        "gunicorn", 
        "-w", "1", 
        "-b", "0.0.0.0:5000", 
        "--preload",  # Importante para GPIO
        "app:app"
    ])

def start_ngrok():
    return subprocess.Popen([
        "ngrok", 
        "http", 
        "--url", 
        "nicely-valued-chimp.ngrok-free.app", 
        "5000"
    ])

def signal_handler(sig, frame):
    processes = [flask_process, ngrok_process]
    for p in processes:
        if p:
            p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    flask_process = start_flask()
    time.sleep(5)  # Mayor tiempo de espera para inicialización de GPIO
    ngrok_process = start_ngrok()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)