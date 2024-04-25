import socketio  # Importa la librería para la comunicación mediante sockets
import flet as ft  # Importa la librería para la interfaz de usuario
import asyncio  # Importa la librería para operaciones asíncronas
import RPi.GPIO as GPIO  # Importa la librería para el control de pines GPIO del Raspberry Pi
import requests
import time  # Importa la librería para operaciones de tiempo

GPIO.cleanup()  # Limpia los pines GPIO para evitar interferencias

sio = socketio.AsyncClient(ssl_verify=False)

# # Configuración de los pines GPIO del Raspberry Pi
GPIO.setmode(GPIO.BOARD)  # Configura los pines GPIO en modo BOARD
pines_relays = [3,10,16,8,5,11,12,7, 32, 26, 24, 22, 21, 19, 18, 15]  # Lista de pines de los relés
for pin in pines_relays:
    GPIO.setup(pin, GPIO.OUT)  # Configura el pin como salida
    GPIO.output(pin, GPIO.HIGH)  # Establece el pin en estado alto (Bajo para el modulo de relé)

# Función principal
async def main(page: ft.Page):
    await sio.connect('https://brainlinkspa.zapto.org', socketio_path='/api/socket.io/')
    await page.add_async(ft.Text("Teikit"))
    await page.add_async(ft.Text("Somos Teikit, un casillero inteligente para tus comidas favoritas!"))  
    await page.add_async(ft.Text("Recuerda que debes abrir la aplicación para hacer retiro de tu pedido."))  

    @sio.event
    async def abrir_casillero_espesifico(data):
        await page.clean_async()
        await page.add_async(ft.Text("Teikit"))
        await page.add_async(ft.Text("Abriendo casillero..."))

        seleccion = data - 1
        GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
        await asyncio.sleep(8)
        GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
        await page.clean_async()
        await page.add_async(ft.Text("Teikit"))
        await page.add_async(ft.Text("El casillero ha sido cerrado."))

    @sio.event
    async def abrir_todos_casilleros():
        await page.clean_async()
        await page.add_async(ft.Text("Teikit"))
        await page.add_async(ft.Text("Abriendo todos los casilleros..."))

        for pin in pines_relays:
            GPIO.output(pin, GPIO.LOW)
        await asyncio.sleep(8)

        for pin in pines_relays:
            GPIO.output(pin, GPIO.HIGH)
        await page.clean_async()
        await page.add_async(ft.Text("Teikit"))
        await page.add_async(ft.Text("Todos los casilleros han sido cerrados."))


    @sio.event
    async def abrir_pedido_casillero_cafeta(data):
        await page.clean_async()
        await page.add_async(ft.Text("Teikit")) 

        mensaje = ""
        if data is not None:
            mensaje = f"El pedido {data['id']} debe ser entregado en el casillero {data['id_casillero']}."
            await page.add_async(ft.Text(mensaje))

            seleccion = int(data['id_casillero'])
            GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
            await asyncio.sleep(8)
            GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
            
            await page.clean_async()
            await page.add_async(ft.Text("Teikit"))
            await page.add_async(ft.Text("Gracias por entregar el pedido."))
            
            # Definir la URL a la que deseas hacer la petición POST
            url = 'https://brainlinkspa.zapto.org/api/pedidos/' + data['id'] + '/nuevoestado'

            # Definir los datos que deseas enviar en el cuerpo de la petición
            datos = {"nuevoEstado": "Entregado"}

            # Realizar la petición POST
            respuesta = requests.post(url, json=datos)

            # Verificar el estado de la respuesta
            if respuesta.status_code == 200:
                print("Petición exitosa!")
                print("Respuesta del servidor:")
                print(respuesta.text)
            else:
                print("Error en la petición. Código de estado:", respuesta.status_code)
            await asyncio.sleep(30)  # Espera 30 segundos

    @sio.event
    async def abrir_pedido_casillero_usuario(data):
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
            await page.add_async(ft.Text("Gracias por hacer tu pedido con nosotros."))
            await page.add_async(ft.Text("Recuerda seguirnos en redes sociales!"))
            import requests

            # Definir la URL a la que deseas hacer la petición POST
            url = 'https://brainlinkspa.zapto.org/api/pedidos/' + data['id'] + '/nuevoestado'

            # Definir los datos que deseas enviar en el cuerpo de la petición
            datos = {"nuevoEstado": "Retirado"}

            # Realizar la petición POST
            respuesta = requests.post(url, json=datos)

            # Verificar el estado de la respuesta
            if respuesta.status_code == 200:
                print("Petición exitosa!")
                print("Respuesta del servidor:")
                print(respuesta.text)
            else:
                print("Error en la petición. Código de estado:", respuesta.status_code)

            await asyncio.sleep(30)  # Espera 30 segundos

# Función para desconectar del servidor socketio
async def desconectar():
    await sio.disconnect()

# Inicia la aplicación con la función principal
ft.app(target=main)

# Ejecuta la función de desconexión
asyncio.run(desconectar())
