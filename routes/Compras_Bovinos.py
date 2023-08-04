'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.actualizacion_peso import actualizacion_peso
from Lib.carga_animal_capacidad_carga import carga_animal,capacidad_carga
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_capacidad_carga, modelo_carga_animal_y_consumo_agua
from fastapi import  status,  APIRouter, Response

from sqlalchemy import update

from schemas.schemas_bovinos import esquema_carga_animal_y_consumo_agua, esquema_capacidad_carga

# Configuracion de la libreria para los logs de sinarca
# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Crea un manejador de archivo para guardar el log
log_file = 'Log_Sinarca.log'
file_handler = logging.FileHandler(log_file)
# Define el formato del log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Agrega el manejador de archivo al logger
logger.addHandler(file_handler)

Compras_bovinos = APIRouter()


