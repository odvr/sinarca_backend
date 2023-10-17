'''
Librerias requeridas
@autor : odvr
'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response
from sqlalchemy.sql.functions import current_user

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte,  modelo_arbol_genealogico, modelo_veterinaria_evoluciones, \
    modelo_historial_supervivencia, modelo_historial_partos
from routes.Reproductor import vida_util_macho_reproductor
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores
from sqlalchemy import update, between, func, asc, desc
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

"""esta funcion
"""


def registro_partos_animales(session: Session,current_user):
 try:
     #consulta que trae los datos de madre e hijos
     consulta_partos = session.query(modelo_arbol_genealogico.c.id_bovino_madre,
                                     modelo_arbol_genealogico.c.id_bovino,
                                     modelo_bovinos_inventario.c.fecha_nacimiento,
                                     modelo_arbol_genealogico.c.nombre_bovino_madre,
                                     modelo_bovinos_inventario.c.nombre_bovino). \
         join(modelo_arbol_genealogico, modelo_bovinos_inventario.c.id_bovino == modelo_arbol_genealogico.c.id_bovino). \
         filter(modelo_bovinos_inventario.c.usuario_id == current_user).all()
     #recorre el bucle for
     for i in consulta_partos:
         # Toma el ID de la bovino madre, este es el campo numero 0
         id_bovino_madre = i[0]
         # Toma el ID del bovino, este es el campo numero 1
         id_bovino = i[1]
         # Toma la fecha de nacimiento del bovino, este es el campo numero 2
         fecha_nacimiento = i[2]
         # Toma el nombre de la madre, este es el campo numero 3
         nombre_bovino_madre = i[3]
         # Toma el nombre de la madre, este es el campo numero 3
         nombre_bovino = i[4]
         #la siguiente consulta se realiza con el fin de identificar
         # los animales que esten en produccion de leche
         consulta_proposito = session.query(modelo_bovinos_inventario). \
             where(modelo_bovinos_inventario.c.id_bovino == id_bovino_madre). \
             filter(modelo_bovinos_inventario.c.proposito == "Leche").all()

         if consulta_proposito is None or consulta_proposito == []:
             existencia = session.query(modelo_historial_partos). \
                 where(modelo_historial_partos.c.id_bovino == id_bovino_madre).all()
             if existencia == []:
                 pass
             else:
                 session.execute(modelo_historial_partos.delete(). \
                                 where(modelo_historial_partos.c.id_bovino == id_bovino_madre))
                 session.commit()
         else:
             existencia = session.query(modelo_historial_partos). \
                 where(modelo_historial_partos.c.id_bovino_hijo == id_bovino).all()
             if existencia==[] or existencia is None:
                 ingresoPartos = modelo_historial_partos.insert().values(id_bovino=id_bovino_madre,
                                                                         fecha_parto=fecha_nacimiento,
                                                                         id_bovino_hijo=id_bovino,
                                                                         usuario_id=current_user,
                                                                         nombre_madre=nombre_bovino_madre,
                                                                         nombre_hijo=nombre_bovino)
                 session.execute(ingresoPartos)
                 session.commit()

             else:
                 session.execute(modelo_historial_partos.update().values(fecha_parto=fecha_nacimiento,
                                                                         nombre_madre=nombre_bovino_madre,
                                                                         nombre_hijo=nombre_bovino). \
                                 where(modelo_historial_partos.columns.id_bovino == id_bovino))
                 session.commit()

     existencia_en_arbol = session.query(modelo_historial_partos).all()
     for i in existencia_en_arbol:
         # Toma el ID del hijo
         id_bovino_hijo = i[4]
         existencia = session.query(modelo_arbol_genealogico). \
             where(modelo_arbol_genealogico.c.id_bovino == id_bovino_hijo).all()
         if existencia is None or existencia == []:
             session.execute(modelo_historial_partos.delete(). \
                             where(modelo_historial_partos.c.id_bovino_hijo == id_bovino_hijo))
             session.commit()
         else:
             pass

 except Exception as e:
     logger.error(f'Error Funcion registro_partos_animales: {e}')
     raise
 finally:
     session.close()