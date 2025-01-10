from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

# Configuración inicial de Flask y GPIO
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

# Diccionario que mapea números de casilleros a pines GPIO
relay_pins = {
    1: 16,  # Casillero 1 conectado al pin físico 16
    2: 11,  # Casillero 2 conectado al pin físico 11
    3: 12,  # Casillero 3 conectado al pin físico 12
    4: 7,   # Casillero 4 conectado al pin físico 7
    # Añade más casilleros según sea necesario
}

# Configurar pines GPIO como salidas y desactivarlos inicialmente
for pin in relay_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Token de autenticación para mayor seguridad
API_TOKEN = "t2e0i2k4IT"

# Middleware para verificar el token en cada solicitud
@app.before_request
def verificar_token():
    token = request.headers.get('Authorization')
    if token != f"Bearer {API_TOKEN}":
        return jsonify({"error": "Acceso no autorizado"}), 401

# Ruta para abrir un casillero
@app.route('/opening', methods=['POST'])
def abrir_casillero():
    try:
        data = request.json
        casillero = data.get('casillero')

        # Validar si el número de casillero es válido
        if casillero not in relay_pins:
            return jsonify({"error": "Numero de casillero invalido"}), 400

        pin = relay_pins[casillero]

        # Activar el relé (abre el casillero)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(3)  # Mantener el casillero abierto por 3 segundos
        GPIO.output(pin, GPIO.LOW)

        return jsonify({"status": f"Casillero {casillero} abierto con exito"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para liberar los pines GPIO y apagar el sistema
@app.route('/shutdown', methods=['POST'])
def shutdown():
    GPIO.cleanup()
    return jsonify({"status": "Sistema apagado"}), 200

# Iniciar el servidor Flask
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=50000)  # Escucha en todas las interfaces, puerto 5000
    except KeyboardInterrupt:
        GPIO.cleanup()
