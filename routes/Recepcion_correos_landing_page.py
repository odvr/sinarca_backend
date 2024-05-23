'''
Librerias requeridas
@autor : odvr
'''

import logging
from Lib.enviar_correos import enviar_correo
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordBearer
from config.db import get_session
from fastapi import  status

oauth2_scheme = OAuth2PasswordBearer("/token")

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

CorreosLandingPage = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@CorreosLandingPage.post("/EnviarCorreoLandingPage/{nombre}/{email}/{mensaje}")
async def envioCorreolandingPage(nombre, email,mensaje):

    """
     Función para enviar correo segun la plantilla
    Definición de Variables
    :param db:
    :param current_user:
    :return:
    """
    destinatario = "rutaganadera.co@gmail.com"
    asunto = nombre +" "+ email
    Notificacion = mensaje


    enviar_correo(destinatario, asunto, Notificacion)

    return Response(status_code=status.HTTP_201_CREATED)

