#start_server
import subprocess
import time
import signal
import sys

def start_flask():
    return subprocess.Popen(["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "--preload", "app:app"])

def start_ngrok():
    time.sleep(2)
    return subprocess.Popen(["ngrok", "http", "--url", "nicely-valued-chimp.ngrok-free.app", "5000"])

def start_ui():
    time.sleep(3)
    return subprocess.Popen(["python", "ui.py"])

def signal_handler(sig, frame):
    for p in [flask_process, ngrok_process, ui_process]:
        if p:
            p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    flask_process = start_flask()
    ngrok_process = start_ngrok()
    ui_process = start_ui()
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)