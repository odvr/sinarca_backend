'''
Librerias requeridas

@autor : odvr

'''

import logging

from fastapi import APIRouter
from sqlalchemy import asc
from sqlalchemy.orm import Session

# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_periodos_secado, modelo_levante, modelo_datos_pesaje, modelo_ceba, \
    modelo_ganancia_historica_peso

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

""""""

def duracion_secado(session: Session,current_user):
    try:
        #la siguiente consulta tare los id y los estados de los bovinos en levante
        consulta_periodos_secado= session.query(modelo_periodos_secado).\
            filter(modelo_periodos_secado.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_periodos_secado:
            # Toma el ID del bovino, este es el campo numero 0
            id_secado = i.id_secado
            # Toma el estado del bovino, este es el campo numero 1
            fecha_inicio_secado = i.fecha_inicio_secado
            # Toma el estado del bovino, este es el campo numero 1
            fecha_final_secado = i.fecha_final_secado

            if fecha_inicio_secado is None or fecha_final_secado is None:
                session.execute(modelo_periodos_secado.update().values(duracion=None). \
                                where(modelo_periodos_secado.columns.id_secado == id_secado))
                session.commit()
            else:
                diferencia=fecha_final_secado-fecha_inicio_secado
                diferencia_dias= diferencia.days
                session.execute(modelo_periodos_secado.update().values(duracion=diferencia_dias). \
                                where(modelo_periodos_secado.columns.id_secado == id_secado))
                session.commit()

    except Exception as e:
        logger.error(f'Error Funcion duracion_secado: {e}')
        raise
    finally:
        session.close()