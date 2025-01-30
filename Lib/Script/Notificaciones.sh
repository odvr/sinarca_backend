#!/bin/bash
# Diseñado para ambientes Unix
# Ruta del Path
SCRIPT_PATH="/app/Lib/Script/Notificaciones.py"

# Ruta al archivo de log
LOG_PATH="/app/Lib/Script/Logs/Logs.log"

# Configurar PYTHONPATH
export PYTHONPATH="/app"

# Ejecutar el script Python y redirigir los logs
echo "[$(date)] Ejecutando el script Python..." >> "$LOG_PATH"
python3 "$SCRIPT_PATH" >> "$LOG_PATH" 2>&1
echo "[$(date)] Script Python terminado." >> "$LOG_PATH"