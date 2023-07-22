'''
Librerias requeridas
@autor : odvr
'''
import logging

from Lib.EliminacionTotal import eliminacionBovino

from starlette.status import HTTP_204_NO_CONTENT
from config.db import  session

from fastapi import APIRouter


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

Eliminar_Bovino = APIRouter()

@Eliminar_Bovino.delete("/Eliminar_Bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def Eliminar_total(id_bovino: str):
    try:

       eliminacionBovino(id_bovino)

    except Exception as e:
        logger.error(f'al intentar eliminar General un animal: {e}')
        raise
    finally:
        session.close()
