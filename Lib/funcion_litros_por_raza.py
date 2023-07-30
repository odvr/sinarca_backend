'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.funcion_IEP_por_raza import IEP_por_raza
from Lib.Lib_Intervalo_Partos import intervalo_partos, promedio_intervalo_partos
from Lib.funcion_litros_leche import promedio_litros_leche
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_orden_litros
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


def litros_por_raza():
    try:
        """#la siguiente consulta trae eel listado de razas de los animales en el modulo de leche
        razas_litros_leche = list(set(session.query(modelo_bovinos_inventario.c.raza). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).all()))
        #para calcular los litros y animales por raza se implementa un bucle
        contador_raza= len(razas_litros_leche)
        b=0
        while(b<contador_raza):
            raza_a_trabajar=razas_litros_leche[b][0]
            #consulta de litros promedio por raza
            consulta_litros_prom_raza = session.query(
                func.avg(modelo_leche.columns.promedio_litros)).\
                filter(modelo_leche.columns.raza==raza_a_trabajar).all()

            animales_litros_leche = session.query(modelo_bovinos_inventario.c.raza, modelo_leche.c.id_bovino,
                                                  modelo_leche.c.promedio_litros). \
                join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).all()
            # recorre el bucle
            for i in animales_litros_leche:
                # Toma el ID del bovino, este es el campo numero 1
                id_bovino_litros = i[1]
                # Toma el promedio de litros de un animal, este es el campo numero 2
                promedio_litros_bovino = i[2]
                # Toma la raza del bovino, este es el campo numero 0
                raza_bovino_litros = i[0]
                if consulta_litros_prom_raza[0][0] is None or consulta_litros_prom_raza[0][0] == 0:
                    pass
                else:
                    diferencia = promedio_litros_bovino - consulta_litros_prom_raza[0][0]
                    if raza_bovino_litros == raza_a_trabajar:
                        # consulta para saber si el bovino existe
                        consulta_existencia_bovino = session.query(modelo_orden_litros). \
                            filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                        # si la consulta es vacia significa que no existe ese animal en la tabla,
                        # entonces ese animal sera insertado
                        if consulta_existencia_bovino == []:
                            ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=consulta_litros_prom_raza[0][0],
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                            session.execute(ingresoDatos)
                            session.commit()
                        # si el animal existe entonces actualiza sus datos
                        else:
                            session.execute(modelo_orden_litros.update().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=consulta_litros_prom_raza[0][0],
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                            where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                            session.commit()
            b=b+1

            # el siguiente codigo elimina los bovinos cuyo estado sea cambiado
            consulta_animales = session.query(modelo_bovinos_inventario.c.estado, modelo_orden_litros.c.id_bovino). \
                join(modelo_orden_litros,
                     modelo_bovinos_inventario.c.id_bovino == modelo_orden_litros.c.id_bovino).all()
            for i in consulta_animales:
                # Toma el ID del bovino en este caso es el campo 1
                idBovino = i[1]
                # Toma el estado del bovino en este caso es el campo 0
                estadoBovino = i[0]
                if estadoBovino == "Muerto" or estadoBovino == "Vendido":
                    session.execute(modelo_orden_litros.delete().where(modelo_orden_litros.c.id_bovino == idBovino))
                    session.commit()
                else:
                    pass"""
        logger.info(f'Funcion litros_por_raza {"p"} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion litros_por_raza: {e}')
        raise
    finally:
        session.close()
