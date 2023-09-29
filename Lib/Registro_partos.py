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


def registro_partos_animales(session: Session):
 try:

     consulta_partos = session.query(modelo_historial_partos.c.id_bovino_hijo).all()
     # recorre el bucle
     for i in consulta_partos:
         # Toma el ID del bovino, este es el campo numero 1
         id_bovino_parido = i[0]

         consulta_fecha_nacimiento=session.query(modelo_bovinos_inventario.c.fecha_nacimiento).\
             filter(modelo_bovinos_inventario.c.id_bovino==id_bovino_parido).all()
         for i in consulta_fecha_nacimiento:
             # Toma el ID del bovino, este es el campo numero 1
             fecha_nacimiento = i[0]
             session.execute(modelo_historial_partos.update().values(fecha_parto=fecha_nacimiento). \
                             where(modelo_historial_partos.columns.id_bovino_hijo == id_bovino_parido))
             session.commit()
 except Exception as e:
     logger.error(f'Error Funcion registro_partos_animales: {e}')
     raise
 finally:
     session.close()