import sys
import os
import time
import threading
import logging
from datetime import datetime

# Añadir la ruta al directorio 'Lib' al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importación de Funciones para Notificar
from Lib.Cambiar_Estado_Facturas import CambiarEstadoFactura
from Lib.Lib_notificacion_palpaciones_partos import notificacion_proximidad_parto

# Configuración de la librería para los logs de sinarca
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'Log_Sinarca.log')
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def job():
    logger.info("Ejecutando Tarea")
    try:
        CambiarEstadoFactura()
        notificacion_proximidad_parto()
        logger.info("Tarea Completada")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def schedule_job(interval, action):
    while True:
        action()
        time.sleep(interval)

# Programar la tarea para que se ejecute cada 12 horas (43200 segundos)
interval = 43200
thread = threading.Thread(target=schedule_job, args=(interval, job))
thread.daemon = True
thread.start()

logger.info("Scheduler started...")
# Mantener el script en ejecución para que las tareas programadas se ejecuten
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Scheduler stopped by user")