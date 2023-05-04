'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_historial_partos, modelo_historial_intervalo_partos
from schemas.schemas_bovinos import Esquema_bovinos,User, esquema_produccion_leche, esquema_produccion_levante,TokenSchema,esquema_descarte, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func, null, desc
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends

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
"""la siguiente funcion calcula los intervalos de partos de cada animal y los inserta
en la base de datos"""
def intervalo_partos():
    try:
        # se borra el registro anterior para evitar duplicidad de id y generar nuevos datos actualizados
        session.execute(modelo_historial_intervalo_partos.delete().where(modelo_historial_intervalo_partos.c.id_bovino))
        session.commit()
        # Realiza el join co la tabla de bovinos (solo se veran los id de los bovinos)
        #como la tabla de historial de partos puede tener un id repetido mas de una vez, se utiliza el conjunto o set
        #el set no permite elementos repetidos, por lo tanto solo nos dara un listado de id unicos
        consulta_animal_partos= set(session.query(modelo_bovinos_inventario.c.id_bovino, modelo_historial_partos.c.id_bovino). \
            join(modelo_historial_partos, modelo_bovinos_inventario.c.id_bovino == modelo_historial_partos.c.id_bovino).all())
        # recorre el bucle
        for i in consulta_animal_partos:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_partos = i[0]
            # cosulta que determina la cantidad de partos de cada animal
            cantidad_partos = session.query(modelo_historial_partos). \
                filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos).count()
            # actualizacion de campo de numero de partos
            session.execute(modelo_leche.update().values(num_partos=cantidad_partos). \
                            where(modelo_leche.columns.id_bovino == id_bovino_partos))
            session.commit()
            #esta consulta trae en orden segun fecha de parto los partos del animal
            consulta_partos = session.query(modelo_historial_partos).\
                filter(modelo_historial_partos.columns.id_bovino==id_bovino_partos).\
                    order_by(desc(modelo_historial_partos.columns.fecha_parto)).all()
            #para calcular el intervalo entre partos es necesario un bucle
            #si un animal tiene 3 partos, tendra 2 intervalos, si tiene 5 partos, tendra 4 intervalos
            #por ello la cantidad de intervalos es igual a los partos menos 1
            contador = cantidad_partos - 1
            e=0
            while (e<contador):
                    intervalo_parto= int(((consulta_partos[e][2]).year-(consulta_partos[e+1][2]).year)*365 +\
                                     ((consulta_partos[e][2]).month-(consulta_partos[e+1][2]).month)*30.4 + \
                                     ((consulta_partos[e][2]).day-(consulta_partos[e+1][2]).day))
                    ingresointervalo = modelo_historial_intervalo_partos.insert().values(id_bovino=id_bovino_partos,
                                                                                fecha_parto1=consulta_partos[e][2],
                                                                                fecha_parto2=consulta_partos[e+1][2],
                                                                                intervalo=intervalo_parto)

                    session.execute(ingresointervalo)
                    session.commit()
                    e=e+1

        logger.info(f'Funcion intervalo_partos {consulta_animal_partos} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion intervalo_partos: {e}')
        raise
    finally:
        session.close()

"""la siguiente funcion calcula el intervalo de parto promedio de cada animal"""
def promedio_intervalo_partos():
    try:
        # Realiza el join co la tabla de bovinos (solo se veran los id de los bovinos)
        # como la tabla de intervalos de parto puede tener un id repetido mas de una vez, se utiliza el conjunto o set
        # el set no permite elementos repetidos, por lo tanto solo nos dara un listado de id unicos
        consulta_animal_intervalos = set(session.query(modelo_bovinos_inventario.c.id_bovino, modelo_historial_intervalo_partos.c.id_bovino). \
            join(modelo_historial_intervalo_partos,modelo_bovinos_inventario.c.id_bovino == modelo_historial_intervalo_partos.c.id_bovino).all())
        # recorre el bucle
        for i in consulta_animal_intervalos:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_intervalos = i[0]
            #con este id consultamos la sumatoria de los itervalos y su cantidad
            #suma de los intervalos
            consulta_suma_intervalos=session.query(func.sum(modelo_historial_intervalo_partos.columns.intervalo)).\
                filter(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_intervalos).all()
            for i in consulta_suma_intervalos:
                # Toma la suma de los intervalos del animal en este caso es el campo 0
                suma_intervalos = i[0]
                # conteo de los intervalos
                cantidad_intervalos = session.query(modelo_historial_intervalo_partos). \
                    filter(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_intervalos).count()
                # calculo del promedo de intervalo entre partos
                promedio_intervalo = suma_intervalos / cantidad_intervalos
                # actualizacion del campo
                session.execute(modelo_leche.update().values(intervalo_entre_partos=promedio_intervalo). \
                                where(modelo_leche.columns.id_bovino == id_bovino_intervalos))
                session.commit()

        logger.info(f'Funcion promedio_intervalo_partos {consulta_animal_intervalos} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion promedio_intervalo_partos: {e}')
        raise
    finally:
        session.close()