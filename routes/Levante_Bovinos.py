'''
Librerias requeridas
'''

import logging
import json
from sqlalchemy import update
from Lib.Levante_Ceba_Bovinos import Estado_Optimo_Levante
from Lib.Lib_Intervalo_Partos import intervalo_partos, fecha_aproximada_parto
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session

from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos, modelo_partos, modelo_levante, modelo_bovinos_inventario, \
    modelo_indicadores
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_produccion_levante, Esquema_Usuario
from routes.rutas_bovinos import get_current_user
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

Levante_Bovinos = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

"""
Lista los animales en Levante

"""

@Levante_Bovinos.get("/listar_prod_levante",response_model=list[esquema_produccion_levante])
async def inventario_levante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    Estado_Optimo_Levante(db=db)
    eliminarduplicados(db=db)


    try:
        itemsLevante = db.execute(modelo_levante.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()
    return itemsLevante

@Levante_Bovinos.get("/Calcular_Animales_Optimo_Levante")
async def Animales_Optimo_Levante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
 try:
    # join,consulta y conteo de animales vivos con estado optimo
    levante_optimo = db.query(modelo_bovinos_inventario.c.estado, modelo_levante.c.estado_optimo_levante). \
        join(modelo_levante, modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_levante.c.estado_optimo_levante == "Estado Optimo").count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_optimos_levante=levante_optimo))

    db.commit()
 except Exception as e:
     logger.error(f'Error Funcion Animales_Optimo_Levante: {e}')
     raise
 finally:
     db.close()
 return levante_optimo