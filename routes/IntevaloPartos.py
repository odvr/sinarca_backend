'''
Librerias requeridas
'''

import logging

from Lib.Lib_Intervalo_Partos import intervalo_partos
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_historial_intervalo_partos

from fastapi import APIRouter


from schemas.schemas_bovinos import esquema_historial_partos, esquema_intervalo_partos

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


IntevaloPartos = APIRouter()

@IntevaloPartos.get("/listar_tabla_Intervalo_Partos",response_model=list[esquema_intervalo_partos] )
async def listar_tabla_Intervalo_Partos():
    try:
        intervalo_partos()
        itemsListarIntevaloPartos = session.execute(modelo_historial_intervalo_partos.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        session.close()
    return itemsListarIntevaloPartos


