import subprocess
import time
import signal
import sys

def start_process(cmd, delay=0):
    time.sleep(delay)
    return subprocess.Popen(cmd)

def signal_handler(sig, frame):
    for p in processes: p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    processes = [
        start_process(["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]),
        start_process(["ngrok", "http", "5000"], 2),
        start_process(["python", "ui.py"], 3)
    ]
    
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        time.sleep(1)