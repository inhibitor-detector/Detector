#!/bin/bash

ls

# Verificar si la carpeta venv existe
if [ ! -d "venv" ]; then
    echo "Cre
    ando entorno virtual..."
    # Crear un entorno virtual llamado venv
    python3 -m venv venv
    echo "Entorno virtual creado."
fi
# Activar el entorno virtual
source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

uvicorn main:app --port 4141

echo "done, bye!"
exit
