


'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Depends
from config.db import   get_session
from sqlalchemy.orm import Session

from models.modelo_bovinos import modelo_datos_muerte
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_datos_muerte, Esquema_Usuario

# Configuracion de las rutas para fash api
Muertes_Bovinos = APIRouter()

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

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()



""""
Listar Tabla de Animales con Regristro de Muerte

"""

@Muertes_Bovinos.get("/listar_bovino_muerte",response_model=list[esquema_datos_muerte])
async def id_inventario_bovinos_muertos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta y seleccion de los animales muertos
        consulta = db.query(modelo_datos_muerte). \
            filter(modelo_datos_muerte.c.estado == "Muerto",modelo_datos_muerte.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE MUERTE : {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta


@Muertes_Bovinos.get("/id_listar_bovino_muerte/{id_bovino}",response_model=esquema_datos_muerte)
async def inventario_bovinos_muertos_id(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = db.execute(
            modelo_datos_muerte.select().where(modelo_datos_muerte.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al obtener Listar ID de Bovino: {e}')
        raise
    finally:
        db.close()

    return consulta