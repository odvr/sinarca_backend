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
from Lib.funcion_litros_por_raza import litros_por_raza
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_orden_peso
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

"""la siguiente funcion compara el peso promedio del animal con el peso de su raza con el
 fin de obtener un listado de animales ordenado del mas pesado al menos pesado segun su raza
  esta funcio solo aplicara para nimales con edad mayor o igual a 24 meses que es la edad donde
  se considera que han alcanzado su peso adulto o estan por alcanzarlo"""
def peso_segun_raza():
    try:
        # consulta de animales listados en el modulo de leche
        animales_peso =  session.query(modelo_bovinos_inventario). \
               where(between(modelo_bovinos_inventario.columns.edad, 24, 500)).\
            filter(modelo_bovinos_inventario.c.estado == "Vivo").all()
        # recorre el bucle
        for i in animales_peso:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_peso = i[0]
            # Toma el peso actual del bovino, este es el campo numero 2
            peso_bovino = i[5]
            # Toma la raza del bovino, este es el campo numero 0
            raza_bovino = i[4]
            # Toma el peso actual del bovino, este es el campo numero 2
            edad_bovino = i[2]
            # Toma la raza del bovino, este es el campo numero 0
            sexo_bovino = i[3]
            # Toma el peso actual del bovino, este es el campo numero 2
            estado_bovino = i[9]
            #bucle que compara el animal segun su raza
            if raza_bovino=="Holstein":
                if sexo_bovino=="Macho":
                    peso_raza=1000
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=650
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Jersey":
                if sexo_bovino=="Macho":
                    peso_raza=680
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=430
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Gyr":
                if sexo_bovino=="Macho":
                    peso_raza=750
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=450
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Girolando":
                if sexo_bovino=="Macho":
                    peso_raza=750
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=450
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Red Sindhi":
                if sexo_bovino=="Macho":
                    peso_raza=700
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=350
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Limousin":
                if sexo_bovino=="Macho":
                    peso_raza=900
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=500
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Charolais":
                if sexo_bovino=="Macho":
                    peso_raza=1000
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=650
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Hereford":
                if sexo_bovino=="Macho":
                    peso_raza=1100
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=550
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino=="Romagnola":
                if sexo_bovino=="Macho":
                    peso_raza=1100
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values( raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino=="Hembra":
                    peso_raza=600
                    diferencia=peso_raza-peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                        raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                        peso_promedio_raza=peso_raza,
                                                                        peso_promedio_animal=peso_bovino,
                                                                        diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Brahman":
                if sexo_bovino == "Macho":
                    peso_raza = 1000
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 500
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Guzerat":
                if sexo_bovino == "Macho":
                    peso_raza = 900
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 450
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Nelore":
                if sexo_bovino == "Macho":
                    peso_raza = 1000
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 500
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Brangus":
                if sexo_bovino == "Macho":
                    peso_raza = 932
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 545
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Simmental":
                if sexo_bovino == "Macho":
                    peso_raza = 1100
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 750
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Pardo suizo":
                if sexo_bovino == "Macho":
                    peso_raza = 1000
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 600
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Normando":
                if sexo_bovino == "Macho":
                    peso_raza = 1000
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 700
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Ayrshire":
                if sexo_bovino == "Macho":
                    peso_raza = 840
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 450
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Indubrasil":
                if sexo_bovino == "Macho":
                    peso_raza = 1100
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 600
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Blanco orejinegro":
                if sexo_bovino == "Macho":
                    peso_raza = 650
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 350
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Romosinuano":
                if sexo_bovino == "Macho":
                    peso_raza = 750
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 383
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Sanmartinero":
                if sexo_bovino == "Macho":
                    peso_raza = 550
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 400
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Costeño con cuernos":
                if sexo_bovino == "Macho":
                    peso_raza = 690
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 380
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Chino santandereano":
                if sexo_bovino == "Macho":
                    peso_raza = 658
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 487
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Harton del valle":
                if sexo_bovino == "Macho":
                    peso_raza = 767
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 487
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Casanareño":
                if sexo_bovino == "Macho":
                    peso_raza = 610
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 380
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "Velasquez":
                if sexo_bovino == "Macho":
                    peso_raza = 750
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 450
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()

            if raza_bovino == "7 colores (cruce indefinido)":
                if sexo_bovino == "Macho":
                    peso_raza = 700
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
                if sexo_bovino == "Hembra":
                    peso_raza = 380
                    diferencia = peso_raza - peso_bovino
                    # consulta para saber si el bovino existe
                    consulta_existencia_bovino = session.query(modelo_orden_peso). \
                        filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                    # si la consulta es vacia significa que no existe ese animal en la tabla,
                    # entonces ese animal sera insertado
                    if consulta_existencia_bovino == []:
                        ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                         raza=raza_bovino,
                                                                         peso_promedio_raza=peso_raza,
                                                                         peso_promedio_animal=peso_bovino,
                                                                         diferencia=diferencia)

                        session.execute(ingresoDatos)
                        session.commit()
                    # si el animal existe entonces actualiza sus datos
                    else:
                        session.execute(modelo_orden_peso.update().values(raza=raza_bovino,
                                                                          peso_promedio_raza=peso_raza,
                                                                          peso_promedio_animal=peso_bovino,
                                                                          diferencia=diferencia). \
                                        where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                        session.commit()
        logger.info(f'Funcion peso_segun_raza {animales_peso} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion intervalo_partos: {e}')
        raise
    finally:
        session.close()
