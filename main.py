import socketio
import flet as ft
import asyncio
import RPi.GPIO as GPIO
import time

GPIO.cleanup() # Liberar los pines GPIO

sio = socketio.AsyncClient()

# Configuración de la biblioteca RPi.GPIO
GPIO.setmode(GPIO.BOARD)
pines_relays = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]
for pin in pines_relays:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

async def main(page: ft.Page):
    await sio.connect('http://192.168.0.17:3030')
    await page.add_async(ft.Text("Esperando que un casillero se abra..."))

    @sio.event
    async def abrir_pedido_casillero_cafeta(data):
        await page.clean_async()
        
        mensaje = ""
        if data is not None:
            mensaje = f""" 
                El pedido {data['id']} ha sido abierto 
                En el casillero {data['id_casillero']}
            """
            await page.add_async(ft.Text(mensaje))
        # Abre el casillero
            try:
                seleccion = int(data['id_casillero'])
                if 1 <= seleccion <= 16:
                    GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
                    print(f"Casillero {seleccion} activado.")
                    await asyncio.sleep(8)  # Espera un momento
                    GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
                    print(f"Casillero {seleccion} desactivado.")
                else:
                    print("ID de casillero no válido. Seleccione un número entre 1 y 16.")
            except ValueError:
                print("ID de casillero no válido. Debe ser un número entre 1 y 16.")

    # @sio.event
    # async def abrir_pedido_casillero_usuario(data):            pass

        
        
async def desconectar():
    await sio.disconnect()

ft.app(main)
asyncio.run(desconectar())
