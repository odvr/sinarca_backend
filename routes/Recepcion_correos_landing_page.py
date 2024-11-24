'''
Librerias requeridas
@autor : odvr
'''

import logging
from Lib.enviar_correos import enviar_correo
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response,Form
from fastapi.security import OAuth2PasswordBearer
from fastapi import  Depends
from Lib.enviar_correos_publicidad import enviar_correo_publicidad, enviar_correo_bienvenida, \
    enviar_correo_publicidad_Asociaciones
from config.db import get_session
from fastapi import  status
from typing import Optional

from typing import List

from datetime import  datetime
from sqlalchemy.orm import Session
from models.modelo_bovinos import modelo_envio_correo_publicidad



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

@CorreosLandingPage.post("/EnviarCorreosPublicidad",status_code=status.HTTP_201_CREATED, tags=["Envio de Correos"])
async def envioCorreolandingPage(destinatario:  Optional [List[str]] = Form(None),tipoDestinatario: Optional [str] = Form(None),db: Session = Depends(get_database_session)):
    """
    :param destinatario:
    :return:
    """

    for correos in destinatario:

        #Separa los correos por correo
        correos_separados = correos.split(',')
        for correo in correos_separados:
            if tipoDestinatario == "Ganaderos Común":
                enviar_correo_publicidad(correo)

            if tipoDestinatario == "Asociaciones":
                enviar_correo_publicidad_Asociaciones(correo)

            FechaDeEnvioCorreo = datetime.now()

            ingresoEnvio = modelo_envio_correo_publicidad.insert().values(correo_enviado=correo,
                                                                          fecha_envio=FechaDeEnvioCorreo,

                                                                          )
            db.execute(ingresoEnvio)
            db.commit()
    return Response(status_code=status.HTTP_201_CREATED)


@CorreosLandingPage.post("/EnviarCorreoBienvenida",status_code=status.HTTP_201_CREATED, tags=["Envio de Correos"])
async def envioCorreolandingPage(destinatario: Optional [str] = Form(None),db: Session = Depends(get_database_session)):
    """
    :param destinatario:
    :return:
    """

    enviar_correo_bienvenida(destinatario)




    return Response(status_code=status.HTTP_201_CREATED)