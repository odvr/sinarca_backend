'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos, promedio_intervalo_partos
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_historial_intervalo_partos
from fastapi import APIRouter
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_historial_partos, esquema_intervalo_partos, Esquema_Usuario

# Configuracion de la libreria para los logs de sinarca
# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Crea un manejador de archivo para guardar el log
log_file = 'Log_Sinarca.log'
file_handler = logging.FileHandler(log_file)
from fastapi import  Depends
# Define el formato del log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Agrega el manejador de archivo al logger
logger.addHandler(file_handler)

IntevaloPartos = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
@IntevaloPartos.get("/listar_tabla_Intervalo_Partos",response_model=list[esquema_intervalo_partos] )
async def listar_tabla_Intervalo_Partos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        intervalo_partos(session=db,current_user=current_user)
        promedio_intervalo_partos(session=db,current_user=current_user)
        #itemsListarIntevaloPartos = db.execute(modelo_historial_intervalo_partos.select()).all()
        itemsListarIntevaloPartos = db.query(modelo_historial_intervalo_partos).filter(modelo_historial_intervalo_partos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return itemsListarIntevaloPartos


