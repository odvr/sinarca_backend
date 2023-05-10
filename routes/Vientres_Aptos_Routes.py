
'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_vientres_aptos, modelo_bovinos_inventario
from fastapi import    APIRouter
from datetime import date
from starlette.status import HTTP_204_NO_CONTENT
from schemas.schemas_bovinos import esquema_litros_leche, esquema_vientres_aptos

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

Vientres_Aptos = APIRouter()




@Vientres_Aptos.get("/listar_vientres_aptos",response_model=list[esquema_vientres_aptos] )
async def listar_tabla_vientres_Aptos():

    try:


        itemsAnimales = session.execute(modelo_vientres_aptos.select()).all()


    except Exception as e:
        logger.error(f'Error al obtener Vientres Aptos: {e}')
        raise
    finally:
        session.close()
    return itemsAnimales




@Vientres_Aptos.get("/listar_contar_listar_vientres_aptos" )
async def listar_contar_AnimalesDescarte():

    try:

        itemsAnimalesVientresAptos = session.query(modelo_vientres_aptos). \
            where(modelo_vientres_aptos.columns.id_vientre).count()

    except Exception as e:
        logger.error(f'Error al obtener CONTAR VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesVientresAptos


"""
Listar animales con vientre apto
"""
@Vientres_Aptos.get("/listar_contar_listar_vientres_aptos" )
async def listar_contar_AnimalesDescarte():

    try:
        itemsAnimalesVientresAptos = session.query(modelo_vientres_aptos). \
            where(modelo_vientres_aptos.columns.id_vientre).count()

    except Exception as e:
        logger.error(f'Error al obtener CONTAR VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesVientresAptos


