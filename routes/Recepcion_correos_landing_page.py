'''
Librerias requeridas
@autor : odvr
'''

import logging

from Lib.Envia_Boletines_Informativos import enviar_Boletines
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

            if tipoDestinatario == "Noticias":
                Asunto = "  Boletín Informativo"
                mensaje = """ <div class="container">
    
        <h2>¡Recuerda Pesar tu Ganado Periódicamente!</h2>
        <p>En <strong>Ruta Ganadera</strong>, queremos recordarte la <strong>importancia del pesaje periódico</strong> de tu ganado bovino. Esta práctica esencial te ayudará a mantener el control de tu producción, mejorar el bienestar de tus animales y optimizar los recursos de tu finca.</p>

        <h2>📋 ¿Por qué es fundamental pesar tu ganado?</h2>
        <ul>
            <li>✅ <strong>Monitoreo del crecimiento:</strong> Detecta si los animales están alcanzando sus metas de peso en cada etapa de su desarrollo.</li>
            <li>✅ <strong>Salud y bienestar:</strong> Identifica rápidamente posibles problemas de salud relacionados con el peso.</li>
            <li>✅ <strong>Trazabilidad y mercado:</strong> Mantén un registro actualizado para cumplir con estándares de calidad.</li>
            <li>✅ <strong>Optimización económica:</strong> Ajusta la alimentación y evita gastos innecesarios, aumentando la rentabilidad.</li>
        </ul>

        <h2>📅 Recomendación de frecuencia</h2>
        <p>Te recomendamos realizar el pesaje de tus animales <strong>al menos una vez al mes</strong> o adaptarlo según las necesidades de tu sistema de producción.</p>
      
        <h2>📈 Beneficios del pesaje regular</h2>
        <ul>
            <li>🔹 Asegura que tu ganado alcance su máximo potencial productivo.</li>
            <li>🔹 Facilita la planificación de reproducción y comercialización.</li>
            <li>🔹 Contribuye al bienestar general de tus animales, lo que se traduce en mayor calidad y rendimiento.</li>
        </ul>

        <p><strong>¡Haz del pesaje periódico una prioridad!</strong></p>
        <p>Una acción tan simple como monitorear el peso de tu ganado puede marcar una gran diferencia en los resultados de tu negocio. Si necesitas más información o quieres recibir recomendaciones personalizadas, estamos a tu disposición.</p>

                """
                enviar_Boletines(correo,Asunto, mensaje )
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