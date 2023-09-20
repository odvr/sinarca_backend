'''
Librerias requeridas
@autor : odvr
'''

import logging


from fastapi import APIRouter, Response



# importa la conexion de la base de datos
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_datos_muerte, \
    modelo_indicadores,modelo_historial_perdida_terneros


from sqlalchemy import update, between,  asc
from datetime import  datetime

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from fastapi import   Depends

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

def perdida_Terneros1(db: Session,current_user):
 try:

     consulta_primer_muerte = db.query(modelo_bovinos_inventario.c.id_bovino,modelo_datos_muerte.c.fecha_muerte). \
         join(modelo_datos_muerte,modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino).\
         where(between(modelo_bovinos_inventario.columns.edad, 0, 12))\
         .group_by(asc(modelo_datos_muerte.c.fecha_muerte)).first()
     #si retorna una consulta vacia entonces indicara cero perdida de terneros
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         periodo_actual= int(datetime.now().year)
         tasa_perd = 0
         consulta_existencia=db.query(modelo_historial_perdida_terneros). \
             where(modelo_historial_perdida_terneros.columns.periodo==periodo_actual).all()
         if consulta_existencia==[]:
             ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo_actual,
                                                                                  perdida=tasa_perd)

             db.execute(ingresoperiodo)
             db.commit()
         else:
             db.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                             where(modelo_historial_perdida_terneros.columns.periodo==periodo_actual))
             db.commit()
     #en caso de que exista uno o mas registros de muertes, se tomara la fecha mas antigua para el bucle
     # a partir de ese año se realizara un listado de perdidas de tenero por cada periodo hasta el actual
     else:
         contador=(datetime.now().year-consulta_primer_muerte[1].year)+1
         c=0
         while (c < contador):
             periodo = consulta_primer_muerte[1].year + c
             print(periodo)
             # se determinan las fechas del periodo (inicio y fin de año)
             fecha_inicio = datetime(periodo, 1, 1)
             fecha_fin = datetime(periodo, 12, 31)
             # la siguiente consulta trae la cantidad de muertes para cada periodo a evaluar
             muertes_periodo = db.query(modelo_bovinos_inventario.c.id_bovino, modelo_datos_muerte.c.fecha_muerte). \
                 join(modelo_datos_muerte, modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino). \
                 where(between(modelo_datos_muerte.columns.fecha_muerte, fecha_inicio, fecha_fin)) \
                 .filter(between(modelo_bovinos_inventario.columns.edad, 0, 12)).count()
             # calculo de la tasa de perdida de terneros
             if muertes_periodo == 0:
                 tasa_perd = 0
                 consulta_existencia = db.query(modelo_historial_perdida_terneros). \
                     where(modelo_historial_perdida_terneros.columns.periodo == periodo).all()
                 if consulta_existencia == []:
                     ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo,
                                                                                        perdida=tasa_perd)

                     db.execute(ingresoperiodo)
                     db.commit()
                 else:
                     db.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                                     where(modelo_historial_perdida_terneros.columns.periodo == periodo))
                     db.commit()
             else:
                 #para determinar los totales es necesario determinar los animales que
                 # tenian edad de 0 a 12 meses duarante el periodo a evaluar
                 fecha_inicio_nacimiento = datetime((periodo-1), 2, 1)
                 fecha_fin_nacimiento = datetime(periodo, 12, 31)

                 totales_periodo= db.query(modelo_bovinos_inventario). \
                 where(between(modelo_bovinos_inventario.columns.fecha_nacimiento, fecha_inicio_nacimiento, fecha_fin_nacimiento)).count()

                 tasa_perd = (muertes_periodo / totales_periodo) * 100
             consulta_existencia = db.query(modelo_historial_perdida_terneros). \
                 where(modelo_historial_perdida_terneros.columns.periodo == periodo).all()
             if consulta_existencia == []:
                 ingresoperiodo = modelo_historial_perdida_terneros.insert().values(periodo=periodo,
                                                                                    perdida=tasa_perd)

                 db.execute(ingresoperiodo)
                 db.commit()
             else:
                 db.execute(modelo_historial_perdida_terneros.update().values(perdida=tasa_perd). \
                                 where(modelo_historial_perdida_terneros.columns.periodo == periodo))
                 db.commit()
             c= c+1

     # el siguiente codigo permite actualizar los periodos si se cambia la primer fecha de muerte
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         db.execute(modelo_historial_perdida_terneros.delete().
                         where(modelo_historial_perdida_terneros.c.periodo!=datetime.now().year))
         db.commit()
     else:
         consulta_periodos = db.query(modelo_historial_perdida_terneros.c.periodo). \
             filter(modelo_historial_perdida_terneros.c.periodo < consulta_primer_muerte[1].year).all()
         if consulta_periodos is None or consulta_periodos == []:
             pass
         else:
             db.execute(modelo_historial_perdida_terneros.delete().
                             where(modelo_historial_perdida_terneros.c.periodo < consulta_primer_muerte[1].year))
             db.commit()

     #actualizacion del valor mas actual en ela tabla de indicadores
     consulta_ultimo_periodo = db.query(modelo_historial_perdida_terneros.c.perdida).\
         group_by(asc(modelo_historial_perdida_terneros.c.perdida)).all()
     db.execute(update(modelo_indicadores).
                     where(modelo_indicadores.c.id_indicadores == current_user).
                     values(perdida_de_terneros=consulta_ultimo_periodo[0][0]))
     db.commit()
     db.close()

 except Exception as e:
     logger.error(f'Error Funcion perdida_Terneros1: {e}')
     raise

