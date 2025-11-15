#!/bin/bash

echo "========== START SERVICES =========="
export PYTHONPATH=$(pwd)
echo "PYTHONPATH seteado en $(pwd)"

# Activar entorno virtual (compatibilidad Windows + Linux)
if [ -f .venv/bin/activate ]; then
    # Linux / Mac
    source .venv/bin/activate
    echo "Activando entorno virtual en .venv (bin)"
elif [ -f .venv/Scripts/activate ]; then
    # Windows Git Bash / Powershell
    source .venv/Scripts/activate
    echo "Activando entorno virtual en .venv (Scripts)"
elif [ -f venv/bin/activate ]; then
    source venv/bin/activate
    echo "Activando entorno virtual en venv (bin)"
elif [ -f venv/Scripts/activate ]; then
    source venv/Scripts/activate
    echo "Activando entorno virtual en venv (Scripts)"
else
    echo "⚠ No se encontró entorno virtual. Crealo con:"
    echo "python -m venv .venv"
    exit 1
fi

# Cargar .env manualmente
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "Variables de entorno cargadas"
else
    echo "⚠ No se encontró el archivo .env"
fi

echo "🚀 Iniciando FastAPI en el puerto 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

wait
