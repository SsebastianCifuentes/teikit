import requests

 # Definir la URL a la que deseas hacer la petición POST
url = 'http://192.168.0.17:3030/pedido/' + '682f157e9220' + '/estado'

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