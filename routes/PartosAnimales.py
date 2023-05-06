'''
Librerias requeridas
'''

import logging
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status

from schemas.schemas_bovinos import esquema_historial_partos

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

partos_bovinos = APIRouter()
@partos_bovinos.post("/crear_Registro_Partos/{id_bovino}/{fecha_parto}/{tipo_parto}/{id_bovino_hijo}")
async def crear_Registro_Partos(id_bovino:str,fecha_parto: date,tipo_parto:str,id_bovino_hijo:str ):

    try:
        listar_tabla_Partos_Animales()
        ingresoRegistroPartos= modelo_historial_partos.insert().values(id_bovino=id_bovino,
                                                     fecha_parto=fecha_parto,
                                                     tipo_parto=tipo_parto,
                                                     id_bovino_hijo=id_bovino_hijo,
                                                   )


        condb.execute(ingresoRegistroPartos)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear INDICE DE PARTOS: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)



@partos_bovinos.get("/listar_tabla_Historial_Partos",response_model=list[esquema_historial_partos] )
async def listar_tabla_Partos_Animales():
    try:
        itemsListarPartos = session.execute(modelo_historial_partos.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        session.close()
    return itemsListarPartos