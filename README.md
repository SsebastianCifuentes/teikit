# Teikit electronica

Un entorno virtual es una herramienta que te permite crear un espacio aislado para instalar y gestionar dependencias (paquetes de Python) necesarias para un proyecto específico.

Lo primero es dirigirse a la ruta en donde esta ubicado el directorio de trabajo
```
cd /Desktop/Teikit
```

Una vez ahí, se debe activar el entorno virtual
```
source teikit-casillero/bin/activate
```

Para desactivar el entorno virtual (por si acaso)
```
deactivate
```

Ejecutamos el servidor Flask para la apertura de casilleros
```
python3 relay_API.py
```
Esto permite que la API empiece a escuchar mediante la direccion 192.168.0.100:50000

Luego se debe activar el tunel ngrok, el cual asigna un dominio publico para acceder al servidor Flask desde cualquier lugar (Abrir en otra terminal)
```
ngrok http --url nicely-valued-chimp.ngrok-free.app 50000
```
