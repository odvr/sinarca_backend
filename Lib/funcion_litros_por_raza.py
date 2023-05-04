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
from Lib.funcion_intervalo_partos import intervalo_partos, promedio_intervalo_partos
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

"""la siguiente funcion calcula los intervalos de partos de cada animal y los inserta
en la base de datos"""
def litros_por_raza():
    try:
        # consulta de animales listados en el modulo de leche
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
            # se realiza un bucle segun el promedio de litros por raza bovina
            if raza_bovino_litros == "Holstein":
                litros_promedio_dia_raza = 35
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Jersey":
                litros_promedio_dia_raza = 20
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Gyr":
                litros_promedio_dia_raza = 12
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Girolando":
                litros_promedio_dia_raza = 15
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Red Sindhi":
                litros_promedio_dia_raza = 10
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Limousin":
                litros_promedio_dia_raza = 6
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Charolais":
                litros_promedio_dia_raza = 5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Hereford":
                litros_promedio_dia_raza = 4.5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Romagnola":
                litros_promedio_dia_raza = 4
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Brahman":
                litros_promedio_dia_raza = 6
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Guzerat":
                litros_promedio_dia_raza = 8
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Nelore":
                litros_promedio_dia_raza = 4.5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                    raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                    litros_promedio_raza=litros_promedio_dia_raza,
                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                    diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Brangus":
                litros_promedio_dia_raza = 3
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Simmental":
                litros_promedio_dia_raza = 15
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Pardo suizo":
                litros_promedio_dia_raza = 24
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Normando":
                litros_promedio_dia_raza = 14.5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Ayrshire":
                litros_promedio_dia_raza = 20
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Indubrasil":
                litros_promedio_dia_raza = 12
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Blanco orejinegro":
                litros_promedio_dia_raza = 4.5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()


            elif raza_bovino_litros == "Romosinuano":
                litros_promedio_dia_raza = 5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Sanmartinero":
                litros_promedio_dia_raza = 5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Costeño con cuernos":
                litros_promedio_dia_raza = 5.5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Chino santandereano":
                litros_promedio_dia_raza = 7
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Harton del valle":
                litros_promedio_dia_raza = 7
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Casanareño":
                litros_promedio_dia_raza = 4
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "Velasquez":
                litros_promedio_dia_raza = 5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()

            elif raza_bovino_litros == "7 colores (cruce indefinido)":
                litros_promedio_dia_raza = 5
                diferencia = litros_promedio_dia_raza - promedio_litros_bovino
                # consulta para saber si el bovino ya existe en la tabla
                consulta_existencia_bovino = session.query(modelo_orden_litros). \
                    filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                # si la consulta es vacia significa que no existe ese animal en la tabla,
                # entonces ese animal sera insertado
                if consulta_existencia_bovino == []:
                    ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                       raza=raza_bovino_litros,
                                                                       litros_promedio_raza=litros_promedio_dia_raza,
                                                                       litros_promedio_animal=promedio_litros_bovino,
                                                                       diferencia=diferencia)

                    session.execute(ingresoDatos)
                    session.commit()
                # si el animal existe entonces actualiza sus datos
                else:
                    session.execute(modelo_orden_litros.update().values(raza=raza_bovino_litros,
                                                                        litros_promedio_raza=litros_promedio_dia_raza,
                                                                        litros_promedio_animal=promedio_litros_bovino,
                                                                        diferencia=diferencia). \
                                    where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                    session.commit()
        logger.info(f'Funcion intervalo_partos {"p"} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion intervalo_partos: {e}')
        raise
    finally:
        session.close()
