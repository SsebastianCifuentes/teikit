# Teikit Casilleros

Un entorno virtual es una herramienta que te permite crear un espacio aislado para instalar y gestionar dependencias (paquetes de Python) necesarias para un proyecto específico.

Lo primero es dirigirse a la ruta en donde esta ubicado el directorio de trabajo
```
cd Desktop/Teikit/teikit-casillero
```

Una vez ahí, se debe activar el entorno virtual
```
source bin/activate
```

Luego es dirirse a la carpeta en donde se encuentra el archivo ejecutable
```
cd ../production/src
```

Ejecutamos el programa para la apertura de casilleros
```
python3 start_server.py
```
Este programa incluye el servidor gunicorn, ngrok y UI para el usuario de la cafeteria en simultaneo.

Para desactivar el entorno virtual
```
deactivate
```