'''
Librerias requeridas
'''
from sqlalchemy.orm import Session
import logging

from Lib.actualizacion_peso import actualizacion_peso
from Lib.carga_animal_capacidad_carga import carga_animal,capacidad_carga
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_capacidad_carga, modelo_carga_animal_y_consumo_agua
from fastapi import  status,  APIRouter, Response

from sqlalchemy import update
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_carga_animal_y_consumo_agua, esquema_capacidad_carga, Esquema_Usuario

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
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@capacidad_carga_rutas.get("/listar_capacidad_carga", response_model=list[esquema_capacidad_carga] )
async def listar_capacidad_carga(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        carga_animal(session=db)
        capacidad_carga(session=db)
        actualizacion_peso(session=db)
        #itemscargaAnimales = db.execute(modelo_capacidad_carga.select()).all()
        itemscargaAnimales = db.query(modelo_capacidad_carga).filter(modelo_capacidad_carga.c.usuario_id == current_user).all()


    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CApacidad Carga: {e}')
        raise
    finally:
        db.close()
    return itemscargaAnimales





@capacidad_carga_rutas.get("/listar_carga_animales", response_model=list[esquema_carga_animal_y_consumo_agua] )
async def listar_carga_animales(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        #consumo_global_agua_y_totalidad_unidades_animales()
        carga_animal(session=db)
        capacidad_carga(session=db)
        #itemscargaAnimales = db.execute(modelo_carga_animal_y_consumo_agua.select()).all()
        itemscargaAnimales = db.query(modelo_carga_animal_y_consumo_agua).filter(
            modelo_carga_animal_y_consumo_agua.c.usuario_id == current_user).all()


    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CARGA ANIMALES: {e}')
        raise
    finally:
        db.close()
    return itemscargaAnimales





@capacidad_carga_rutas.post("/crear_capacidad_carga/{medicion_aforo}/{hectareas_predio}/{tipo_de_muestra}", status_code=status.HTTP_201_CREATED)
async def crear_capacidad_carga(medicion_aforo: float,hectareas_predio :float,tipo_de_muestra:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):


    try:


        hectareas_forraje = update(modelo_capacidad_carga).where(modelo_capacidad_carga.c.id_capacidad == 1).values(
            medicion_aforo=medicion_aforo,hectareas_predio=hectareas_predio,tipo_de_muestra=tipo_de_muestra,usuario_id=current_user)
        db.execute(hectareas_forraje)
        db.commit()
        carga_animal(session=db)
        capacidad_carga(session=db)

    except Exception as e:
        logger.error(f'Error al Crear CAPACIDAD CARGA: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)