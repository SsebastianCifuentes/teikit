# main.py
import threading
from app import run_flask
from ui import start_ui

def start_flask():
    run_flask()

def start_ui():
    start_ui()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    start_ui()
