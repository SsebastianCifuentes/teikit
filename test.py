import socketio  # Importa la librería para la comunicación mediante sockets
import flet as ft  # Importa la librería para la interfaz de usuario
import asyncio  # Importa la librería para operaciones asíncronas
import RPi.GPIO as GPIO  # Importa la librería para el control de pines GPIO del Raspberry Pi
import time  # Importa la librería para operaciones de tiempo

GPIO.cleanup()  # Limpia los pines GPIO para evitar interferencias

sio = socketio.AsyncClient()  # Crea un cliente socketio asíncrono

# Configuración de los pines GPIO del Raspberry Pi
GPIO.setmode(GPIO.BOARD)  # Configura los pines GPIO en modo BOARD
pines_relays = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]  # Lista de pines de los relés
for pin in pines_relays:
    GPIO.setup(pin, GPIO.OUT)  # Configura el pin como salida
    GPIO.output(pin, GPIO.HIGH)  # Establece el pin en estado alto (Bajo para el modulo de relé)

# Función principal
async def main(page: ft.Page):
    await sio.connect('http://192.168.0.17:3030')  # Conecta al servidor socketio
    await page.add_async(ft.Text("Teikit"))  
    await page.add_async(ft.Text("Somos Teikit, un casillero inteligente para tus comidas favoritas!"))  
    await page.add_async(ft.Text("Recuerda que debes abrir la aplicación para hacer retiro de tu pedido."))  

    # Maneja el evento de apertura de casillero
    @sio.event
    async def abrir_pedido_casillero(data):
        await page.clean_async()
        await page.add_async(ft.Text("Teikit"))  

        mensaje = ""
        if data is not None:
            mensaje = f"El pedido {data['id']} está listo para retirar y se encuentra en el casillero {data['id_casillero']}."
            await page.add_async(ft.Text(mensaje))

            seleccion = int(data['id_casillero'])
            GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
            await asyncio.sleep(8)
            GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
            
            await page.clean_async()
            await page.add_async(ft.Text("Teikit"))
            await page.add_async(ft.Text("Gracias por hacer tu pedido."))
            await page.add_async(ft.Text("Recuerda seguirnos en redes sociales!"))
            await asyncio.sleep(30)  # Espera 30 segundos

# Función para desconectar del servidor socketio
async def desconectar():
    await sio.disconnect()

# Inicia la aplicación con la función principal
ft.app(main)

# Ejecuta la función de desconexión
asyncio.run(desconectar())
