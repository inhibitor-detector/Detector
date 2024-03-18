#!/bin/bash

# Verificar si la carpeta venv existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    # Crear un entorno virtual llamado venv
    python3 -m venv venv
    echo "Entorno virtual creado."
fi
# Activar el entorno virtual
echo "Activando entorno virtual"
source venv/bin/activate

echo "Chequeando version de pip"
pip install --upgrade pip > /dev/null 2>&1

echo "Chequeando dependencias"
pip install -r requirements.txt > /dev/null 2>&1

echo "Iniciando uvicorn"
uvicorn main:app --port 4141 --host 0.0.0.0

echo "done, bye!"
exit
