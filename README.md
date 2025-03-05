# Teikit Casilleros

## Descripción

Teikit Casilleros es un sistema que permite la apertura de casilleros de manera automatizada mediante un servidor, una interfaz de usuario (UI) y una integración con **ngrok** para accesibilidad remota. Este documento describe los pasos para la instalación, configuración y ejecución del servicio.

---

## Tabla de Contenidos

- [Requisitos](#requisitos)  
- [Instalación](#instalación)  
- [Configuración de ngrok](#configuración-de-ngrok)  
- [Configuración del entorno](#configuración-del-entorno)  
- [Uso](#uso)  
  - [Activar el entorno virtual](#activar-el-entorno-virtual)  
  - [Ejecutar el programa](#ejecutar-el-programa)  
  - [Desactivar el entorno virtual](#desactivar-el-entorno-virtual)  
- [Automatización con systemd](#automatización-con-systemd)  
  - [Crear el servicio](#crear-el-servicio)  
  - [Gestión del servicio](#gestión-del-servicio)  
- [Logs y Diagnóstico](#logs-y-diagnóstico)  
- [Interfaz de Usuario](#interfaz-de-usuario)  

---

## Requisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3**  
- **ngrok** (instalado correctamente, ver instrucciones más abajo)  
- **systemd** (para la automatización del servicio)  

---

## Instalación

### 1️⃣ Instalar ngrok

Ejecuta el siguiente comando para instalar **ngrok** correctamente:

```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc   | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null   && echo "deb https://ngrok-agent.s3.amazonaws.com buster main"   | sudo tee /etc/apt/sources.list.d/ngrok.list   && sudo apt update   && sudo apt install ngrok
```

### 2️⃣ Crear y activar un entorno virtual

Dirígete a la carpeta donde deseas crear el entorno virtual y ejecuta:

```bash
python3 -m venv teikit-env
```

Luego, actívalo con:

```bash
source teikit-env/bin/activate
```

### 3️⃣ Instalar dependencias

Dentro del entorno virtual, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

---

## Configuración de ngrok

Luego de la instalación, es necesario configurar el token de autenticación:

```bash
ngrok config add-authtoken <TOKEN>
```

Reemplaza `<TOKEN>` con tu clave de autenticación de **ngrok**.

---

## Configuración del entorno

Debes crear un archivo **.env** dentro del proyecto con las siguientes variables:

```bash
nano .env
```

Agrega el siguiente contenido:

```
API_TOKEN=<TOKEN_BACKEND>
EXTERNAL_API=<URL_API_EXTERNA>
```

📌 **Explicación**  
- `API_TOKEN`: Token compartido con el backend para apertura remota.  
- `EXTERNAL_API`: Reservado para futuras integraciones con el backend.  

Guarda los cambios (`CTRL + X`, luego `Y` y `ENTER`).

---

## Uso

### Activar el entorno virtual

Dirígete al directorio de trabajo:

```bash
cd Desktop/Teikit/teikit-env
```

Activa el entorno virtual:

```bash
source bin/activate
```

### Ejecutar el programa

Navega hasta la carpeta donde se encuentra el ejecutable:

```bash
cd ../production/src
```

Ejecuta el programa para la apertura de casilleros:

```bash
python3 start_server.py
```

Este programa iniciará:

- **Gunicorn** (servidor WSGI para ejecutar aplicaciones web)  
- **ngrok** (para accesibilidad remota)  
- **UI** (interfaz de usuario para la cafetería)  

### Desactivar el entorno virtual

Cuando hayas terminado, desactiva el entorno virtual con:

```bash
deactivate
```

---

## Automatización con systemd

Este proceso permite que el sistema se inicie automáticamente cuando la Raspberry Pi se encienda y que el servicio se reinicie si se cierra.

### Crear el servicio

Edita o crea el archivo de servicio en **systemd**:

```bash
sudo nano /etc/systemd/system/teikit.service
```

Agrega el siguiente contenido:

```
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
```

Guarda los cambios y cierra el archivo.

### Gestión del servicio

Habilita el servicio para que se ejecute automáticamente al inicio:

```bash
sudo systemctl enable teikit.service
```

Inicia el servicio:

```bash
sudo systemctl start teikit.service
```

Verifica su estado:

```bash
sudo systemctl status teikit.service
```

Si necesitas detener el servicio:

```bash
sudo systemctl stop teikit.service
```

Para reiniciarlo:

```bash
sudo systemctl restart teikit.service
```

Si quieres deshabilitar el servicio para que no se inicie automáticamente:

```bash
sudo systemctl disable teikit.service
```

✅ **Una vez configurado, el script se ejecutará automáticamente cada vez que la Raspberry Pi se inicie y, si se cierra, se volverá a abrir indefinidamente.**

---

## Logs y Diagnóstico

Verifica si el servicio está habilitado para inicio automático:

```bash
sudo systemctl is-enabled teikit.service
```

Recarga la configuración de **systemd** después de realizar cambios:

```bash
sudo systemctl daemon-reload
```

Consulta el estado detallado del servicio:

```bash
sudo systemctl status teikit.service -l
```

Para ver los logs en tiempo real:

```bash
sudo journalctl -f -u teikit.service
```

---

## Interfaz de Usuario

Aquí puedes ver la interfaz de usuario utilizada en la cafetería:

![UI Cafetería](production/assets/UI_CAFETERIA.png)

---
