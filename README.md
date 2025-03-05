# Teikit Casilleros

Un entorno virtual es una herramienta que te permite crear un espacio aislado para instalar y gestionar dependencias (paquetes de Python) necesarias para un proyecto específico.

Importante instalar ngrok via apt y no ngrok 
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok

y luego configurar el token
ngrok config add-authtoken <token>

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

Para automatizar el servicio por primera vez se debe

sudo nano /etc/systemd/system/teikit.service

[Unit]
Description=Ejecutar Teikit Casilleros al conectarse a internet
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash /home/teikit/Desktop/Teikit/start_teikit.sh
WorkingDirectory=/home/teikit/Desktop/Teikit/teikit-casillero
Restart=always
User=teikit
Environment="DISPLAY=:0"
Environment="PATH=/home/teikit/Desktop/Teikit/teikit-casillero/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target

habilitarlo para que se ejecute en inicio
sudo systemctl enable teikit.service
para probarlo usar
sudo systemctl start teikit.service
para ver status
sudo systemctl status teikit.service
para revisar logs (importante)
sudo journalctl -u teikit.service