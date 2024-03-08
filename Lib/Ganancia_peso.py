'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import timedelta

from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones, modelo_historial_partos, modelo_historial_intervalo_partos, modelo_dias_abiertos, \
    modelo_levante, modelo_datos_pesaje, modelo_ceba
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc

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

"""estas funciones calculan la ganancia media diaria de cada animal para animales de levante y ceba
, para ello toma el primer y el ultimo peso registrado jusnto con sus fechas y divide la 
diferencia entre los dias entre esas dos fecha"""

def ganancia_peso_levante(session: Session,current_user):
    try:
        #la siguiente consulta tare los id y los estados de los bovinos en levante
        consulta_animales_levante= session.query(modelo_levante.c.id_bovino,modelo_levante.c.estado).\
            filter(modelo_levante.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales_levante:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino = i[0]
            # Toma el estado del bovino, este es el campo numero 1
            estado = i[1]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas antigua
            consulta_pesos = session.query(modelo_datos_pesaje.columns.peso,
                                           modelo_datos_pesaje.columns.fecha_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino==id_bovino).\
                order_by(asc(modelo_datos_pesaje.columns.fecha_pesaje)).all()

            cantidad=len(consulta_pesos)
            #si un animal no tiene por lo menos 2 registros de peso no se podra calcular la ganancia diaria de peso
            #lo mismo aplicara para animales que no esten vivos
            if estado!="Vivo" or cantidad<=1:
                session.execute(modelo_levante.update().values(ganancia_media_diaria=None). \
                                where(modelo_levante.columns.id_bovino == id_bovino))
                session.commit()
            else:
                # se identifican los pesos iniciales y finales con sus fechas
                peso_inicial = consulta_pesos[0][0]
                fecha_inicial = consulta_pesos[0][1]

                peso_final = consulta_pesos[cantidad - 1][0]
                fecha_final = consulta_pesos[cantidad - 1][1]

                diferencia_fechas=(fecha_final - fecha_inicial).days

                #si la diferencia entre fechas no es mayor a un dia entonces no se podra calcular la ganancia
                if diferencia_fechas<1 or diferencia_fechas==0:
                    session.execute(modelo_levante.update().values(ganancia_media_diaria=None). \
                                    where(modelo_levante.columns.id_bovino == id_bovino))
                    session.commit()
                else:
                    # se calcula la ganacia media diaria de peso por dia
                    ganancia_media_diaria = ((peso_final - peso_inicial) / (((fecha_final - fecha_inicial).days))) * 1000
                    # Actualiacion de campos
                    session.execute(modelo_levante.update().values(ganancia_media_diaria=round(ganancia_media_diaria,2)). \
                                    where(modelo_levante.columns.id_bovino == id_bovino))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion ganancia_peso_levante: {e}')
        raise
    finally:
        session.close()


def ganancia_peso_ceba(session: Session,current_user):
    try:
        #la siguiente consulta tare los id y los estados de los bovinos en ceba
        consulta_animales_ceba= session.query(modelo_ceba.c.id_bovino,modelo_ceba.c.estado).\
            filter(modelo_ceba.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales_ceba:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino = i[0]
            # Toma el estado del bovino, este es el campo numero 1
            estado = i[1]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas antigua
            consulta_pesos = session.query(modelo_datos_pesaje.columns.peso,
                                           modelo_datos_pesaje.columns.fecha_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino==id_bovino).\
                order_by(asc(modelo_datos_pesaje.columns.fecha_pesaje)).all()

            cantidad=len(consulta_pesos)
            #si un animal no tiene por lo menos 2 registros de peso no se podra calcular la ganancia diaria de peso
            #lo mismo aplicara para animales que no esten vivos
            if estado!="Vivo" or cantidad<=1:
                session.execute(modelo_ceba.update().values(ganancia_media_diaria=None). \
                                where(modelo_ceba.columns.id_bovino == id_bovino))
                session.commit()
            else:
                # se identifican los pesos iniciales y finales con sus fechas
                peso_inicial = consulta_pesos[0][0]
                fecha_inicial = consulta_pesos[0][1]

                peso_final = consulta_pesos[cantidad - 1][0]
                fecha_final = consulta_pesos[cantidad - 1][1]

                diferencia_fechas=(fecha_final - fecha_inicial).days

                # si la diferencia entre fechas no es mayor a un dia entonces no se podra calcular la ganancia
                if diferencia_fechas<1 or diferencia_fechas==0:
                    session.execute(modelo_ceba.update().values(ganancia_media_diaria=None). \
                                    where(modelo_ceba.columns.id_bovino == id_bovino))
                    session.commit()
                else:
                    # se calcula la ganacia media diaria de peso por dia
                    ganancia_media_diaria = ((peso_final - peso_inicial) / (((fecha_final - fecha_inicial).days))) * 1000
                    # Actualiacion de campos
                    session.execute(modelo_ceba.update().values(ganancia_media_diaria=round(ganancia_media_diaria,2)). \
                                    where(modelo_ceba.columns.id_bovino == id_bovino))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion ganancia_peso_ceba: {e}')
        raise
    finally:
        session.close()