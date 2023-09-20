
'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.funcion_vientres_aptos import vientres_aptos
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from sqlalchemy.orm import Session
from fastapi import    APIRouter

from models.modelo_bovinos import modelo_vientres_aptos
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario
from fastapi import  Depends
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



def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()



@Vientres_Aptos.get("/listar_vientres_aptos" )
async def listar_vientres_aptos_modulo(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        vientres_aptos(session=db)
        #Eliminacion_total_vientres_aptos()
        #tabla_vientres_aptos = db.query(modelo_vientres_aptos).all()
        tabla_vientres_aptos = db.query(modelo_vientres_aptos).filter(modelo_vientres_aptos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA VIENTRES APTOS: {e}')
        raise
    finally:
        db.close()
    return tabla_vientres_aptos

@Vientres_Aptos.get("/listar_contar_listar_vientres_aptos" )
async def listar_contar_AnimalesDescarte(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        itemsAnimalesVientresAptos = db.query(modelo_vientres_aptos).filter(modelo_vientres_aptos.c.usuario_id == current_user,modelo_vientres_aptos.columns.id_vientre).count()

    except Exception as e:
        logger.error(f'Error al obtener CONTAR VIENTRES APTOS: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesVientresAptos


"""
Listar animales con vientre apto
@Vientres_Aptos.get("/listar_contar_listar_vientres_aptos" )
async def listar_contar_AnimalesDescarte(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        itemsAnimalesVientresAptos = db.query(modelo_vientres_aptos). \
            where(modelo_vientres_aptos.columns.id_vientre).count()
        

    except Exception as e:
        logger.error(f'Error al obtener CONTAR VIENTRES APTOS: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesVientresAptos
"""



