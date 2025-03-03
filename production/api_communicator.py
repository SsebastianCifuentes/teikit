# api_communicator.py
import requests
import os
from dotenv import load_dotenv

# Cargar configuración del token desde variables de entorno
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API = os.getenv("EXTERNAL_API")

if not API_TOKEN or not EXTERNAL_API:
    raise ValueError("API_TOKEN o EXTERNAL_API no configurados en las variables de entorno")

# Notificar a la API externa
def notify_external_api(locker_number):
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(
            EXTERNAL_API,
            json={"casillero": locker_number},
            headers=headers
        )
        if response.status_code == 200:
            print(f"Notificación enviada a la API externa: Casillero {locker_number}")
        else:
            print(f"Error al notificar a la API externa: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al intentar notificar a la API externa: {e}")

def notify_all_lockers_open():
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(
            EXTERNAL_API,
            json={"casillero": "todos"},
            headers=headers
        )
        if response.status_code == 200:
            print(f"Notificación enviada a la API externa: Todos los casilleros abiertos")
        else:
            print(f"Error al notificar a la API externa: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al intentar notificar a la API externa: {e}")
