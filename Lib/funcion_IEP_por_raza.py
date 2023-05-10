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
from Lib.funcion_litros_leche import promedio_litros_leche
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_orden_IEP
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

"""la siguiente funcion determina la diferencia que existe
entre el intervalo entre partos promedio de un animal con el 
 intervalo entre partos de la raza de dicho animal, esto con
  el fin de mostrar cuales son los animales mejores en terminos de
  su raza"""

def IEP_por_raza():
    try:
       #consulta de animales listados en el modulo de leche
       animales_leche = session.query(modelo_bovinos_inventario.c.raza, modelo_leche.c.id_bovino,
                                              modelo_leche.c.intervalo_entre_partos). \
           join(modelo_leche,modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
           filter(modelo_leche.c.intervalo_entre_partos!=0).all()
       #recorre el bucle
       for i in animales_leche:
           # Toma el ID del bovino, este es el campo numero 1
           id_bovino_leche = i[1]
           # Toma el intervalo entre partos (IEP) del bovino, este es el campo numero 2
           IEP_bovino = i[2]
           # Toma la raza del bovino, este es el campo numero 0
           raza_bovino = i[0]
           #se realiza un bucle segun el intervalo entre partos promedo por raza bovina
           if raza_bovino=="Holstein":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Jersey":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino ya existe en la tabla
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Gyr":
               IEP_raza=390
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Girolando":
               IEP_raza=410
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Red Sindhi":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Limousin":
               IEP_raza=390
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Charolais":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Hereford":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Romagnola":
               IEP_raza=390
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Brahman":
               IEP_raza=410
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Guzerat":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Nelore":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Brangus":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Simmental":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()


           elif raza_bovino=="Pardo suizo":
               IEP_raza=390
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Normando":
               IEP_raza=410
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Ayrshire":
               IEP_raza=400
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Indubrasil":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Blanco orejinegro":
               IEP_raza=380
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Romosinuano":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Sanmartinero":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Costeño con cuernos":
               IEP_raza=353
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Chino santandereano":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()


           elif raza_bovino=="Harton del valle":
               IEP_raza=400
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Casanareño":
               IEP_raza=390
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="Velasquez":
               IEP_raza=420
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()

           elif raza_bovino=="7 colores (cruce indefinido)":
               IEP_raza=430
               diferencia=IEP_raza-IEP_bovino
               #consulta para saber si el bovino existe
               consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                   filter(modelo_orden_IEP.columns.id_bovino == id_bovino_leche).all()
               #si la consulta es vacia significa que no existe ese animal en la tabla,
               # entonces ese animal sera insertado
               if consulta_existencia_bovino==[]:
                   ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_leche,
                                                                   raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia)

                   session.execute(ingresoDatos)
                   session.commit()
               #si el animal existe entonces actualiza sus datos
               else:
                   session.execute(modelo_orden_IEP.update().values(raza=raza_bovino,
                                                                   intervalo_promedio_raza=IEP_raza,
                                                                   intervalo_promedio_animal=IEP_bovino,
                                                                   diferencia=diferencia). \
                                   where(modelo_orden_IEP.columns.id_bovino == id_bovino_leche))
                   session.commit()
       # el siguiente codigo permite emilinar cualquier animal con intervalos entre partos de 0
       consulta_id_bovinos_leche = session.query(modelo_leche).all()
       for i in consulta_id_bovinos_leche:
           # Toma el ID del bovino, este es el campo numero
           id_bovinos_leche = i[1]
           # Toma el intervalo entre partos, este es el campo numero 10
           intervalo_p_promedio = i[10]
           # en caso de tener valor 0 sera eliminado
           if intervalo_p_promedio == 0:
               session.execute(modelo_orden_IEP.delete(). \
                               where(modelo_orden_IEP.c.id_bovino == id_bovinos_leche))
               session.commit()
           else:
               pass
       logger.info(f'Funcion IEP_por_raza {animales_leche} ')
       session.commit()
    except Exception as e:
        logger.error(f'Error Funcion IEP_por_raza: {e}')
        raise
    finally:
        session.close()