
'''
Librerias requeridas
'''
from sqlalchemy.orm import Session
import logging

import crud
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
        descarte(db=db,current_user=current_user)
        #itemsAnimalesDescarte = db.execute(modelo_descarte.select()).all()
        itemsAnimalesDescarte = db.query(modelo_descarte).filter(modelo_descarte.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesDescarte


@bovinos_descarte.get("/listar_contar_animales_descarte" )
async def listar_contar_AnimalesDescarte(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        descarte(db=db)

        #itemsAnimalesDescarte = db.query(modelo_descarte).where(modelo_descarte.columns.id_descarte).count()
        itemsAnimalesDescarte = db.query(modelo_descarte).filter(modelo_descarte.c.usuario_id == current_user,modelo_descarte.columns.id_descarte).count()


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
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)
        ingresodescarte = modelo_descarte.insert().values(id_bovino=id_bovino,razon_descarte=razon_descarte,usuario_id=current_user,nombre_bovino=nombre_bovino)


        db.execute(ingresodescarte)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de DESCARTE: {e}')
        raise
    finally:
        db.close()

    return Response( status_code=status.HTTP_201_CREATED)





@bovinos_descarte.delete("/eliminar_registro_Descarte/{id_descarte}")
async def eliminar_descarte(id_descarte: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_descarte.delete().where(modelo_descarte.c.id_descarte == id_descarte))
        db.commit()
        # retorna un estado de no contenido
        return

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Registro Pajillas: {e}')
        raise
    finally:
        db.close()
