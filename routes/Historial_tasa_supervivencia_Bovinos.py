'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Response
from sqlalchemy.orm import Session

# importa la conexion de la base de datos
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_perdida_terneros, modelo_historial_supervivencia

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_historial_perdida_terneros, Esquema_Usuario, esquema_historial_supervivencia

'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer("/token")
'''***********'''


# Configuracion de las rutas para fash api
rutas_bovinos = APIRouter()

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



Historial_Tasa_Supervivencia = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Historial_Tasa_Supervivencia.get("/listar_tabla_historial_tasa_supervivencia",response_model=list[esquema_historial_supervivencia])
async def listar_tabla_perdida_terneros(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        items_tasa_supervivencia = db.query(modelo_historial_supervivencia).filter(modelo_historial_supervivencia.c.usuario_id == current_user).all()
        db.close()

        return items_tasa_supervivencia

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE TASA SUPERVIVENCIA: {e}')
        raise
    finally:
        db.close()

