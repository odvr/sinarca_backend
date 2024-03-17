'''
Librerias requeridas
'''
import logging

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from Lib.Ganancia_peso import ganancia_peso_historica
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_ganancia_historica_peso
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, \
    esquema_ganancia_historica_peso

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

Ganancia_historica_rutas = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Ganancia_historica_rutas.get("/listar_tabla_ganancias_historicas_pesos",response_model=list[esquema_ganancia_historica_peso] )
async def listar_tabla_Intervalo_Partos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        ganancia_peso_historica(session=db,current_user=current_user)
        itemsListarGananciasPesos = db.query(modelo_ganancia_historica_peso).filter(modelo_ganancia_historica_peso.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener listar_tabla_ganancias_historicas_pesos: {e}')
        raise
    finally:
        db.close()
    return itemsListarGananciasPesos

