'''
Librerias requeridas
'''

import logging


from Lib.funcion_IEP_por_raza import IEP_por_raza
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_orden_IEP
from fastapi import  Depends
from fastapi import APIRouter

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_orden_IEP, Esquema_Usuario

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


IEP_Razas = APIRouter()

@IEP_Razas.get("/Tabla_iep_por_raza",response_model=list[esquema_orden_IEP] )
async def listar_tabla_IEP_Razas(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        IEP_por_raza()




        itemsListarIntevaloPartos = session.execute(modelo_orden_IEP.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        session.close()
    return itemsListarIntevaloPartos