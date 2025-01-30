'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import date, timedelta


from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.sql.functions import current_user

# importa la conexion de la base de datos
from sqlalchemy.orm import Session

import crud
from Lib.enviar_correos import enviar_correo
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import   modelo_palpaciones, modelo_notificacion_proximidad_parto, modelo_usuarios

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

def notificacion_proximidad_parto():
    # Crear una sesión de base de datos
    session: Session = get_session()
    try:
        #consulta que trae el el listado de animales preñadas
        animales_palapaciones_partos= session.query(modelo_palpaciones).\
            filter(modelo_palpaciones.c.diagnostico_prenez=="Preñada").all()
        # recorre el bucle
        for i in animales_palapaciones_partos:
            # Toma el ID del bovino
            id_bovino = i.id_bovino
            # Toma la fecha estimada de parto
            fecha_estimada_parto = i.fecha_estimada_parto
            # Toma el nombre del bovino
            nombre_bovino = i.nombre_bovino
            #toma el usuario
            usuario_id= i.usuario_id

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
                    mensaje = f'El bovino {nombre_bovino}, tiene una fecha aproximada de parto para el día {fecha_estimada_parto}, considera estar atento'
                    fecha_mensaje = date.today()

                    #consulta que averigua si la notificacion ya se genero
                    consulta_notificacion = session.query(modelo_notificacion_proximidad_parto). \
                        filter(modelo_notificacion_proximidad_parto.c.id_bovino == id_bovino,
                               modelo_notificacion_proximidad_parto.c.fecha_estimada_parto == fecha_estimada_parto,
                               modelo_notificacion_proximidad_parto.c.usuario_id == usuario_id).all()


                    if consulta_notificacion is None or consulta_notificacion==[]:
                        #si no se ha generado, se genera y se carga
                        ingresoNotificacion = modelo_notificacion_proximidad_parto.insert().values(id_bovino=id_bovino,
                                                                           nombre_bovino=nombre_bovino,
                                                                           fecha_estimada_parto=fecha_estimada_parto,
                                                                           fecha_mensaje=fecha_mensaje,
                                                                           mensaje=mensaje,
                                                                           usuario_id=usuario_id)

                        session.execute(ingresoNotificacion)
                        session.commit()


                        #finalmente se consulta el correo del usuario y se envia la notificacion por correo
                        correo_usuario = crud.bovinos_inventario.Buscar_Correo_Usuario(db=session,
                                                                                          usuario_id=usuario_id)

                        enviar_correo(correo_usuario,"Bovino con fecha próxima de parto",mensaje)

                        session.commit()

                    else:
                        pass


            else:
                pass


        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion notificacion_proximidad_parto: {e}')
        # Revertir cambios si ocurre un error
        session.rollback()
        raise e
    finally:
        session.close()