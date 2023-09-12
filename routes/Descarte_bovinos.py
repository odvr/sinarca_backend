
'''
Librerias requeridas
'''
from sqlalchemy.orm import Session
import logging

from Lib.Lib_Descarte import descarte
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.actualizacion_peso import actualizacion_peso
from Lib.carga_animal_capacidad_carga import carga_animal,capacidad_carga
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_capacidad_carga, modelo_carga_animal_y_consumo_agua, modelo_descarte
from fastapi import  status,  APIRouter, Response

from sqlalchemy import update
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_carga_animal_y_consumo_agua, esquema_capacidad_carga, Esquema_Usuario, \
    esquema_descarte

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

bovinos_descarte = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()



@bovinos_descarte.get("/listar_animales_descarte",response_model=list[esquema_descarte] )
async def listarAnimalesDescarte(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        itemsAnimalesDescarte = db.execute(modelo_descarte.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesDescarte


@bovinos_descarte.get("/listar_contar_animales_descarte" )
async def listar_contar_AnimalesDescarte(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        #itemsAnimalesDescarte = session.execute(modelo_descarte).count()
        itemsAnimalesDescarte = db.query(modelo_descarte). \
            where(modelo_descarte.columns.id_bovino).count()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesDescarte


"""
Crear Descarte
"""
@bovinos_descarte.post(
    "/crear_descarte/{id_bovino}/{razon_descarte}",
    status_code=status.HTTP_201_CREATED)
async def CrearDescarte(id_bovino: str,razon_descarte:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        descarte(db=db)
        ingresodescarte = modelo_descarte.insert().values(id_bovino=id_bovino,razon_descarte=razon_descarte)


        db.execute(ingresodescarte)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de DESCARTE: {e}')
        raise
    finally:
        db.close()

    return Response( status_code=status.HTTP_201_CREATED)
