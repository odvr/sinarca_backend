#!/bin/bash

# Ejecutar el script de Python en segundo plano y redirigir la salida a un archivo de log
nohup python /app/Lib/Script/Notificaciones.py > /app/Lib/Script/Notificaciones_output.log 2>&1 &