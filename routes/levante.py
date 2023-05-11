'''
Librerias requeridas
'''
import logging

from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_levante
from fastapi import  status,  APIRouter, Response

from routes.rutas_bovinos import eliminarduplicados

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

levante = APIRouter()


"""
Funcion crear Levante
"""
@levante.post(
    "/crear_prod_levante/{id_bovino}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdLevante(id_bovino: str,proposito:str):
    eliminarduplicados()

    try:

        consulta = condb.execute(
            modelo_levante.select().where(
                modelo_levante.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoplevante = modelo_levante.insert().values(id_bovino=id_bovino, proposito=proposito)

            condb.execute(ingresoplevante)
            condb.commit()

        else:

            condb.execute(modelo_levante.update().where(modelo_levante.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino, proposito=proposito))
            condb.commit()

            condb.commit()


    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Levante: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)