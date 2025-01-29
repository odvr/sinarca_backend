'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import date, timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.sql.functions import current_user

# importa la conexion de la base de datos
from sqlalchemy.orm import Session

from Lib.enviar_correos import enviar_correo
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_historial_partos, \
    modelo_orden_peso, modelo_palpaciones, modelo_notificacion_proximidad_parto, modelo_usuarios

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
#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#from twilio.rest import Client
"""la siguinete funcion determina e"""

def notificacion_proximidad_parto(session:Session,current_user):
    try:
        #consulta que trae el el listado de animales preñadas
        animales_palapaciones_partos= session.query(modelo_palpaciones).\
            filter(modelo_palpaciones.c.diagnostico_prenez=="Preñada",
                   modelo_palpaciones.c.usuario_id==current_user).all()
        # recorre el bucle
        for i in animales_palapaciones_partos:
            # Toma el ID del bovino
            id_bovino = i.id_bovino
            # Toma la fecha estimada de parto
            fecha_estimada_parto = i.fecha_estimada_parto
            # Toma el nombre del bovino
            nombre_bovino = i.nombre_bovino

            #estima la diferencia en dias entre la fecha estimada de parto y la fecha actual
            diferencia= fecha_estimada_parto-date.today()
            diferencia_dias=diferencia.days

            #si falta 15 o menos para el parto se notifica
            if diferencia_dias <=15:
                #si la fecha de parto ya paso no se genera notificacion
                if diferencia_dias <=-1:
                    pass
                #caso contrario se genera
                else:
                    mensaje = f'el bovino {nombre_bovino}, tiene una fecha aproximada de parto para el día {fecha_estimada_parto}, considera estar atento'
                    fecha_mensaje = date.today()

                    #consulta que averigua si la notificacion ya se genero
                    consulta_notificacion = session.query(modelo_notificacion_proximidad_parto). \
                        filter(modelo_notificacion_proximidad_parto.c.id_bovino == id_bovino,
                               modelo_notificacion_proximidad_parto.c.fecha_estimada_parto == fecha_estimada_parto,
                               modelo_notificacion_proximidad_parto.c.usuario_id == current_user).all()

                    if consulta_notificacion is None or consulta_notificacion==[]:
                        #si no se ha generado, se genera y se carga
                        ingresoNotificacion = modelo_notificacion_proximidad_parto.insert().values(id_bovino=id_bovino,
                                                                           nombre_bovino=nombre_bovino,
                                                                           fecha_estimada_parto=fecha_estimada_parto,
                                                                           fecha_mensaje=fecha_mensaje,
                                                                           mensaje=mensaje,
                                                                           usuario_id=current_user)

                        session.execute(ingresoNotificacion)

                        #finalmente se consulta el correo del usuario y se envia la notificacion por correo
                        consulta_usuario = session.query(modelo_usuarios). \
                            filter(modelo_usuarios.c.usuario_id == current_user).first()

                        correo_usuario= consulta_usuario[4]

                        enviar_correo(correo_usuario,"Bovino con fecha próxima de parto",mensaje)

                        session.commit()

                    else:
                        pass


            else:
                pass


        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion tipo_ganado_leche: {e}')
        raise
    finally:
        session.close()