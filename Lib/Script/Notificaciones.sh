#!/bin/bash
# Diseñado para ambientes Unix

# Ruta del script Python
SCRIPT_PATH="/app/Lib/Script/Notificaciones.py"

# Ruta al archivo de log
LOG_PATH="/app/Lib/Script/Logs/Logs.log"

# Configurar PYTHONPATH
export PYTHONPATH="/app"

# Ejecutar el script Python con la ruta absoluta de Python
echo "[$(date)] Ejecutando el script Python..." >> "$LOG_PATH"
/usr/local/bin/python3 "$SCRIPT_PATH" >> "$LOG_PATH" 2>&1
echo "[$(date)] Script Python terminado." >> "$LOG_PATH"
