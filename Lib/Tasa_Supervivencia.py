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
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones, modelo_historial_supervivencia
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

"""esta funcion calcula en terminos de porcentaje, cuantos animales han sobrevivido
por año
"""


def tasa_supervivencia():
 try:
     consulta_primer_muerte = session.query(modelo_bovinos_inventario.c.id_bovino,modelo_datos_muerte.c.fecha_muerte). \
         join(modelo_datos_muerte,modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino)\
         .group_by(asc(modelo_datos_muerte.c.fecha_muerte)).first()
     #si retorna una consulta vacia entonces indicara cero muertes
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         periodo_actual= int(datetime.now().year)
         tasa_supervivencia= 0
         consulta_existencia=session.query(modelo_historial_supervivencia). \
             where(modelo_historial_supervivencia.columns.periodo==periodo_actual).all()
         if consulta_existencia==[]:
             ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo_actual,
                                                                             supervivencia=tasa_supervivencia)

             session.execute(ingresoperiodo)
             session.commit()
         else:
             session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                             where(modelo_historial_supervivencia.columns.periodo==periodo_actual))
             session.commit()
     #en caso de que exista uno o mas registros de muertes, se tomara la fecha mas antigua para el bucle
     # a partir de ese año se realizara un listado de supervivencias por cada periodo hasta el actual
     else:
         contador=(datetime.now().year-consulta_primer_muerte[1].year)+1
         c=0
         while (c < contador):
             periodo = consulta_primer_muerte[1].year +c
             # se determinan las fechas del periodo (inicio y fin de año)
             fecha_inicio = datetime(periodo, 1, 1)
             fecha_fin = datetime(periodo, 12, 31)
             # la siguiente consulta trae la cantidad de muertes para cada periodo a evaluar
             muertes_periodo = session.query(modelo_bovinos_inventario.c.id_bovino, modelo_datos_muerte.c.fecha_muerte). \
                 join(modelo_datos_muerte, modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino). \
                 where(between(modelo_datos_muerte.columns.fecha_muerte, fecha_inicio, fecha_fin)).count()
             # calculo de la tasa de perdida de terneros
             if muertes_periodo == 0:
                 tasa_supervivencia = 0
                 consulta_existencia = session.query(modelo_historial_supervivencia). \
                     where(modelo_historial_supervivencia.columns.periodo == periodo).all()
                 if consulta_existencia == []:
                     ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo,
                                                                             supervivencia=tasa_supervivencia)

                     session.execute(ingresoperiodo)
                     session.commit()
                 else:
                     session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                                     where(modelo_historial_supervivencia.columns.periodo == periodo))
                     session.commit()
             else:
                 #para determinar los totales es necesario determinar los animales que
                 # existian en ese año (es decir que naciaron antes de ese año)
                 fecha_fin_nacimiento = datetime(periodo, 12, 31)

                 totales=session.query(modelo_bovinos_inventario). \
                 where(modelo_bovinos_inventario.columns.fecha_nacimiento < fecha_fin_nacimiento).count()

                 muertos=session.query(modelo_datos_muerte). \
                 where(modelo_datos_muerte.columns.fecha_muerte < datetime(periodo, 1, 1)).count()

                 vendidos=session.query(modelo_ventas). \
                     where(modelo_ventas.columns.fecha_venta < datetime((periodo+1), 12, 31)).count()

                 totales_periodo= totales - muertos - vendidos

                 tasa_supervivencia = ( (totales_periodo-muertes_periodo)* 100)/totales_periodo
             consulta_existencia = session.query(modelo_historial_supervivencia). \
                 where(modelo_historial_supervivencia.columns.periodo == periodo).all()
             if consulta_existencia == []:
                 ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo,
                                                                                supervivencia=tasa_supervivencia)

                 session.execute(ingresoperiodo)
                 session.commit()
             else:
                 session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                                 where(modelo_historial_supervivencia.columns.periodo == periodo))
                 session.commit()

             c= c+1

     # el siguiente codigo permite actualizar los periodos si se cambia la primer fecha de muerte
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         session.execute(modelo_historial_supervivencia.delete().
                         where(modelo_historial_supervivencia.c.periodo!=datetime.now().year))
         session.commit()
     else:
         consulta_periodos = session.query(modelo_historial_supervivencia.c.periodo). \
             filter(modelo_historial_supervivencia.c.periodo < consulta_primer_muerte[1].year).all()
         if consulta_periodos is None or consulta_periodos == []:
             pass
         else:
             session.execute(modelo_historial_supervivencia.delete().
                             where(modelo_historial_supervivencia.c.periodo < consulta_primer_muerte[1].year))
             session.commit()

     #actualizacion del valor mas actual en ela tabla de indicadores
     consulta_ultimo_periodo = session.query(modelo_historial_supervivencia.c.supervivencia).\
         group_by(asc(modelo_historial_supervivencia.c.supervivencia)).all()
     session.execute(update(modelo_indicadores).
                     where(modelo_indicadores.c.id_indicadores == 1).
                     values(tasa_supervivencia=consulta_ultimo_periodo[0][0]))
     session.commit()

 except Exception as e:
     logger.error(f'Error Funcion tasa_supervivencia: {e}')
     raise
 finally:
     session.close()
