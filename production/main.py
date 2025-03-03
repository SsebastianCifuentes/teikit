# main.py
import threading
from app import run_flask  # Importa la función de Flask
from ui import start_ui  # Importa la función de la UI

def start_flask():
    run_flask()  # Inicia Flask

def start_ui_func():
    start_ui()  # Llama la función para iniciar la interfaz de usuario

if __name__ == "__main__":
    # Crea un hilo para Flask
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Inicia la interfaz de usuario (UI) principal
    start_ui_func()
