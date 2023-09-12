'''
Librerias requeridas
@autor : odvr
'''
import logging

from Lib.EliminacionTotal import eliminacionBovino
from starlette.status import HTTP_204_NO_CONTENT
from config.db import  get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario

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

Eliminar_Bovino = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@Eliminar_Bovino.delete("/Eliminar_Bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT,tags=["Inventarios"])
async def Eliminar_total(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

       eliminacionBovino(id_bovino,session=db)


    except Exception as e:
        logger.error(f'al intentar eliminar General un animal: {e}')
        raise
    finally:
        db.close()
