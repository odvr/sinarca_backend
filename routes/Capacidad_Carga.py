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

capacidad_carga_rutas = APIRouter()



@capacidad_carga_rutas.get("/listar_capacidad_carga", response_model=list[esquema_capacidad_carga] )
async def listar_capacidad_carga():

    try:

        carga_animal()
        capacidad_carga()
        actualizacion_peso()
        itemscargaAnimales = session.execute(modelo_capacidad_carga.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CApacidad Carga: {e}')
        raise
    finally:
        session.close()
    return itemscargaAnimales





@capacidad_carga_rutas.get("/listar_carga_animales", response_model=list[esquema_carga_animal_y_consumo_agua] )
async def listar_carga_animales():

    try:
        #consumo_global_agua_y_totalidad_unidades_animales()
        carga_animal()
        capacidad_carga()
        itemscargaAnimales = session.execute(modelo_carga_animal_y_consumo_agua.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CARGA ANIMALES: {e}')
        raise
    finally:
        session.close()
    return itemscargaAnimales





@capacidad_carga_rutas.post("/crear_capacidad_carga/{medicion_aforo}/{hectareas_predio}/{tipo_de_muestra}", status_code=status.HTTP_201_CREATED)
async def crear_capacidad_carga(medicion_aforo: float,hectareas_predio :float,tipo_de_muestra:str):


    try:


        hectareas_forraje = update(modelo_capacidad_carga).where(modelo_capacidad_carga.c.id_capacidad == 1).values(
            medicion_aforo=medicion_aforo,hectareas_predio=hectareas_predio,tipo_de_muestra=tipo_de_muestra)
        condb.execute(hectareas_forraje)
        condb.commit()
        carga_animal()
        capacidad_carga()

    except Exception as e:
        logger.error(f'Error al Crear CAPACIDAD CARGA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)