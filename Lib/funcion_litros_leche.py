'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.Lib_Intervalo_Partos import intervalo_partos, promedio_intervalo_partos
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_litros_leche
from schemas.schemas_bovinos import Esquema_bovinos,User, esquema_produccion_leche, esquema_produccion_levante,TokenSchema,esquema_descarte, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func, null
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
"""la siguinete funcion determina e promedio de produccion de litros de leche
de cada animal"""
def promedio_litros_leche():
    try:
        # Realiza el join co la tabla de bovinos (solo se veran los id de los bovinos)
        # como la tabla de litros_leche puede tener un id repetido mas de una vez, se utiliza el conjunto o set
        # el set no permite elementos repetidos, por lo tanto solo nos dara un listado de id unicos
        consulta_animal_litros = set(session.query(modelo_bovinos_inventario.c.id_bovino, modelo_litros_leche.c.id_bovino). \
            join(modelo_litros_leche,modelo_bovinos_inventario.c.id_bovino == modelo_litros_leche.c.id_bovino).all())
        # recorre el bucle
        for i in consulta_animal_litros:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_litros = i[0]
            # con este id consultamos la sumatoria de todos los litros de leche medidos de ese animal
            # suma de los litros
            consulta_suma_litros_leche = session.query(func.sum(modelo_litros_leche.columns.litros_leche)). \
                filter(modelo_litros_leche.columns.id_bovino == id_bovino_litros).all()
            for i in consulta_suma_litros_leche:
                # Toma la suma de los litros del animal en este caso es el campo 0
                suma_litros = i[0]
                # conteo de las veces que se realizo la medida de litros en un animal
                cantidad_de_mediciones = session.query(modelo_litros_leche). \
                    filter(modelo_litros_leche.columns.id_bovino == id_bovino_litros).count()
                # calculo del promedo de litros de leche del animal
                promedio_litros = round((suma_litros / cantidad_de_mediciones), 2)
                # actualizacion del campo
                session.execute(modelo_leche.update().values(promedio_litros=promedio_litros). \
                                where(modelo_leche.columns.id_bovino == id_bovino_litros))
                session.commit()
        # consulta para evaluar aquellos animales que no tengan medidas de leche
        consulta_litros_promedio = session.query(modelo_leche).all()
        for i in consulta_litros_promedio:
            # Toma el id del bovino en este caso es el campo 1
            id_bovino_consulta_litros_promedio = i[1]
            # toma el pormedio de litros del animal
            promedio_litros_bovino = i[8]
            # se define un valor por defecto en caso de que un animal no tenga medidas
            valor_por_defecto = 0
            # Si el valor no existe entonces sera insertado u  0 por defecto
            if promedio_litros_bovino == None:
                session.execute(modelo_leche.update().values(promedio_litros=valor_por_defecto). \
                                where(modelo_leche.columns.id_bovino == id_bovino_consulta_litros_promedio))
                session.commit()
            # caso contrario no se realizaran cambios
            else:
                pass
            # esta consulta Actualiza los dato en caso de que se borren todos los registros de medicion de leche de un animal
            consulta_animal_en_historial_litros = session.query(modelo_litros_leche). \
                filter(modelo_litros_leche.columns.id_bovino == id_bovino_consulta_litros_promedio).all()
            # si la consulta es vacia significa que el animal no tienen mediciones de leche
            if consulta_animal_en_historial_litros == []:
                # entonces su promedio de litros pasara a ser 0
                session.execute(modelo_leche.update().values(promedio_litros=valor_por_defecto). \
                                where(modelo_leche.columns.id_bovino == id_bovino_consulta_litros_promedio))
                session.commit()
            else:
                pass
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion promedio_litros_leche: {e}')
        raise
    finally:
        session.close()