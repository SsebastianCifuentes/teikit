#!/bin/bash

# Función para verificar la conexión a internet
check_internet() {
    ping -c 1 google.com > /dev/null 2>&1
    return $?
}

# Espera hasta que haya conexión a internet
while ! check_internet; do
    echo "Esperando conexión a internet..."
    sleep 10  # Espera 10 segundos antes de volver a verificar
done

# Una vez conectado, procede con la ejecución
echo "Conexión a internet detectada. Iniciando Teikit Casilleros..."

# Navega a la carpeta del proyecto
cd /home/teikit/Desktop/Teikit/teikit-env

# Activa el entorno virtual
source bin/activate

# Navega a la carpeta de producción
cd ../production/src

# Ejecuta el script de Python
python3 start_server.py
