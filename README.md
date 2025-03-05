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
cd Desktop/Teikit/teikit-env
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
WorkingDirectory=/home/teikit/Desktop/Teikit/teikit-env
Restart=always
User=teikit
Environment="DISPLAY=:0"
Environment="PATH=/home/teikit/Desktop/Teikit/teikit-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target

# Habilitar el servicio para que se ejecute al inicio
sudo systemctl enable teikit.service

# Iniciar el servicio
sudo systemctl start teikit.service

# Ver el estado del servicio
sudo systemctl status teikit.service

# Revisar los logs del servicio
sudo journalctl -u teikit.service

# Detener el servicio
sudo systemctl stop teikit.service

# Reiniciar el servicio
sudo systemctl restart teikit.service

# Deshabilitar el servicio para que no se ejecute al inicio
sudo systemctl disable teikit.service

# Ver si el servicio está habilitado para el inicio automático
sudo systemctl is-enabled teikit.service

# Recargar la configuración de systemd después de hacer cambios
sudo systemctl daemon-reload

# Ver el estado del servicio con más detalles
sudo systemctl status teikit.service -l

# Seguir viendo los logs en tiempo real
sudo journalctl -f -u teikit.service
