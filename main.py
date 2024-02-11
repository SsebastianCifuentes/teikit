import socketio
import flet as ft
import asyncio
# sio = socketio.AsyncClient()


sio = socketio.AsyncClient()
async def main(page: ft.Page):
    global sio
    await sio.connect('http://192.168.0.17:3030')
    await page.add_async(ft.Text("Esperando que un casillero se abra..."))

    @sio.event
    async def abrir_pedido_casillero(data):
        
        await page.clean_async()
        
        mensaje = ""
        if(data != None):
            print(data)
            mensaje = f""" 
                El pedido {data['id']} ha sido abierto 
                En el casillero {data['id_casillero']}
            """
        
        await page.add_async(ft.Text(mensaje))

        #Busca el casillero y lo abre

        # for pedido in data:
            
        # await page.add_async(ft.Text(data))
            
    # await sio.disconnect()


async def desconectar():
    await sio.disconnect()


ft.app(main)
asyncio.run(desconectar())

# import RPi.GPIO as GPIO
# import time

# # Configuración de la biblioteca RPi.GPIO
# GPIO.setmode(GPIO.BOARD)

# # Lista de pines GPIO conectados a los relés
# pines_relays = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

# try:
#     # Configuración de los pines GPIO como salidas
#     for pin in pines_relays:
#         GPIO.setup(pin, GPIO.OUT)
#         GPIO.output(pin, GPIO.HIGH)

#     while True:
#         print("Seleccione un relé (1-16) o presione 'q' para salir:")
#         seleccion = input()

#         if seleccion.lower() == 'q':
#             break

#         try:
#             seleccion = int(seleccion)
#             if 1 <= seleccion <= 16:
#                 # Activar el relé seleccionado
#                 GPIO.output(pines_relays[seleccion - 1], GPIO.LOW)
#                 print(f"Relé {seleccion} activado.")

#                 # Esperar un momento (puedes ajustar según sea necesario)
#                 time.sleep(2)

#                 # Desactivar el relé
#                 GPIO.output(pines_relays[seleccion - 1], GPIO.HIGH)
#                 print(f"Relé {seleccion} desactivado.")
#             else:
#                 print("Seleccione un número entre 1 y 16.")
#         except ValueError:
#             print("Entrada no válida. Introduzca un número entre 1 y 16.")
# except KeyboardInterrupt:
#     pass
# finally:
#     # Limpiar la configuración de los pines GPIO al salir
#     GPIO.cleanup()

# import requests
# import asyncio
# import os


# async def main():
#     # URL de la API que deseas consumir
    


# while True:
    
#     asyncio.run(main())
