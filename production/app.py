# app.py
from flask import Flask, request, jsonify, abort
import os
import requests
from dotenv import load_dotenv

# Cargar configuración del token desde variables de entorno
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API = os.getenv("EXTERNAL_API")
if not API_TOKEN or not EXTERNAL_API:
    raise ValueError("API_TOKEN o EXTERNAL_API no configurados en las variables de entorno")

app = Flask(__name__)

@app.before_request
def verify_token():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        abort(401, description="Acceso no autorizado")

@app.route('/')
def index():
    return jsonify({"routes": {
        "/locker": "GET - Devuelve el número total de casilleros.",
        "/locker/opening": "POST - Abre un casillero específico vía API.",
        "/locker/opening/all": "POST - Abre todos los casilleros."
    }})

@app.route('/locker', methods=['GET'])
def get_locker_count():
    return jsonify({"total_lockers": 16}), 200

@app.route('/locker/opening', methods=['POST'])
def open_locker():
    data = request.get_json()
    if not data or 'casillero' not in data:
        abort(400, description="El cuerpo de la solicitud debe incluir 'casillero'")

    locker = data.get('casillero')
    # Lógica para abrir el casillero
    return jsonify({"status": f"Casillero {locker} abierto con éxito"}), 200

@app.route('/locker/opening/all', methods=['POST'])
def open_all_lockers():
    # Lógica para abrir todos los casilleros
    return jsonify({"status": "Todos los casilleros han sido abiertos"}), 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)
