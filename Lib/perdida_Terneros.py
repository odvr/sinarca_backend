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
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones, \
    modelo_historial_perdida_terneros
from routes.Reproductor import vida_util_macho_reproductor
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores
from sqlalchemy import update, between, func
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

"""esta funcion calcula en terminos de porcentaje, cuantos terneros
(animales de 0 a 12 meses) han fallecido, para ello consulta la cantidad 
de animales muertos y el total para mediante una regla de 3 obtener
el porcentaje
"""


def perdida_Terneros1():
 try:
     #el siguiente join trae consigo los años en los que se han reportado muertes de terneros (animales de 0  a 12 meses de edad)
     consulta_periodos_muertes = session.query(modelo_bovinos_inventario.c.id_bovino,modelo_datos_muerte.c.fecha_muerte). \
         join(modelo_datos_muerte,modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino).\
         where(between(modelo_bovinos_inventario.columns.edad, 0, 12))\
         .group_by(func.YEAR(modelo_datos_muerte.c.fecha_muerte)).all()
     #si retorna una consulta vacia entonces indicara cero perdida de terneros
     if consulta_periodos_muertes is None or consulta_periodos_muertes==[]:
         periodo_actual= int(datetime.now().year)
         tasa_perd = 0
         consulta_existencia=session.query(modelo_historial_perdida_terneros). \
             where(modelo_historial_perdida_terneros.columns.periodo==periodo_actual).all()
         if consulta_existencia==[]:
             ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo_actual,
                                                                                  perdida=tasa_perd)

             session.execute(ingresoperiodo)
             session.commit()
         else:
             session.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                             where(modelo_historial_perdida_terneros.columns.periodo==periodo_actual))
             session.commit()
     else:
         # para determinar un contador por años es necesario un bucle
         contador_periodos = len(consulta_periodos_muertes)
         a = 0
         while (a < contador_periodos):
             # se determina periodo a evaluar
             periodo = consulta_periodos_muertes[a][1].year
             # se determinan las fechas del periodo (inicio y fin de año)
             fecha_inicio = datetime(periodo, 1, 1)
             fecha_fin = datetime(periodo, 12, 31)
             # la siguiente consulta trae la cantidad de muertes para cada periodo a evaluar
             muertes_periodo = session.query(modelo_bovinos_inventario.c.id_bovino, modelo_datos_muerte.c.fecha_muerte). \
                 join(modelo_datos_muerte, modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino). \
                 where(between(modelo_datos_muerte.columns.fecha_muerte, fecha_inicio, fecha_fin)) \
                 .filter(between(modelo_bovinos_inventario.columns.edad, 0, 12)).count()
             # calculo de la tasa de perdida de terneros
             if muertes_periodo == 0:
                 tasa_perd = 0
                 consulta_existencia = session.query(modelo_historial_perdida_terneros). \
                     where(modelo_historial_perdida_terneros.columns.periodo == periodo).all()
                 if consulta_existencia == []:
                     ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo,
                                                                                        perdida=tasa_perd)

                     session.execute(ingresoperiodo)
                     session.commit()
                 else:
                     session.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                                     where(modelo_historial_perdida_terneros.columns.periodo == periodo))
                     session.commit()
             else:
                 #para determinar los totales es necesario determinar los animales que
                 # tenian edad de 0 a 12 meses duarante el periodo a evaluar
                 fecha_inicio_nacimiento = datetime((periodo-1), 2, 1)
                 fecha_fin_nacimiento = datetime(periodo, 12, 31)
                 totales_periodo= session.query(modelo_bovinos_inventario). \
                 where(between(modelo_bovinos_inventario.columns.fecha_nacimiento, fecha_inicio_nacimiento, fecha_fin_nacimiento)).count()
                 tasa_perd = (muertes_periodo / totales_periodo) * 100
             consulta_existencia = session.query(modelo_historial_perdida_terneros). \
                 where(modelo_historial_perdida_terneros.columns.periodo == periodo).all()
             if consulta_existencia == []:
                 ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo,
                                                                                    perdida=tasa_perd)

                 session.execute(ingresoperiodo)
                 session.commit()
             else:
                 session.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                                 where(modelo_historial_perdida_terneros.columns.periodo == periodo))
                 session.commit()
             a = a + 1

 except Exception as e:
     logger.error(f'Error Funcion perdida_Terneros1: {e}')
     raise
 finally:
     session.close()