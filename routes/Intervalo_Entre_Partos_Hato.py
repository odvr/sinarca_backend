'''
Librerias requeridas
@autor : odvr
'''

import logging
from http.client import HTTPException
from fastapi import APIRouter, Response
# importa la conexion de la base de datos
from config.db import  get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_indicadores


from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import  Esquema_Usuario




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

'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

from fastapi import FastAPI, status, HTTPException
from sqlalchemy.orm import Session

Intervalo_Entre_Partos_Hato = APIRouter()


# Define una función que obtenga una sesión de base de datos
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Intervalo_Entre_Partos_Hato.get("/listar_Intevalo_entre_Partos_Hato")
async def listar_tabla_intervalo_entre_partos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        response = db.query(modelo_indicadores).where(modelo_indicadores.c.IEP_hato).first()

        if response:
            itemsintervalo_entre_partos = response[28]

            return itemsintervalo_entre_partos
        elif response is None:
            return 0

        else:
            raise HTTPException(status_code=404, detail="No se encontraron datos de IEP HATO")
            pass

    except Exception as e:
        logger.error(f'Error al obtener IEP HATO: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")