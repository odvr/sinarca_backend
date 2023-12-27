'''
Librerias requeridas
@autor : odvr
'''

import logging

from fastapi import APIRouter
from sqlalchemy.orm import Session

# importa la conexion de la base de datos
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_datos_pesaje, \
    modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_arbol_genealogico, modelo_veterinaria_evoluciones, modelo_historial_supervivencia
from sqlalchemy import update, between, asc, desc
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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


def tasa_supervivencia(session:Session,current_user):
 try:
     consulta_primer_muerte = session.query(modelo_bovinos_inventario.c.id_bovino,modelo_datos_muerte.c.fecha_muerte). \
         join(modelo_datos_muerte,modelo_bovinos_inventario.c.id_bovino == modelo_datos_muerte.c.id_bovino)\
         .group_by(asc(modelo_datos_muerte.c.fecha_muerte)).\
         filter(modelo_bovinos_inventario.columns.usuario_id==current_user).first()
     #si retorna una consulta vacia entonces indicara cero muertes
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         periodo_actual= int(datetime.now().year)
         tasa_supervivencia= 100
         consulta_existencia=session.query(modelo_historial_supervivencia). \
             where(modelo_historial_supervivencia.columns.periodo==periodo_actual).\
             filter(modelo_historial_supervivencia.columns.usuario_id==current_user).all()
         if consulta_existencia==[]:
             ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo_actual,
                                                                             supervivencia=tasa_supervivencia,
                                                                             usuario_id=current_user)

             session.execute(ingresoperiodo)
             session.commit()
         else:
             session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                             where(modelo_historial_supervivencia.columns.periodo==periodo_actual).
                             filter(modelo_historial_supervivencia.columns.usuario_id==current_user))
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
                 where(between(modelo_datos_muerte.columns.fecha_muerte, fecha_inicio, fecha_fin)).\
                 filter(modelo_bovinos_inventario.columns.usuario_id==current_user).count()
             # calculo de la tasa de perdida de terneros
             if muertes_periodo == 0:
                 tasa_supervivencia = 100
                 consulta_existencia = session.query(modelo_historial_supervivencia). \
                     where(modelo_historial_supervivencia.columns.periodo == periodo).\
                     filter(modelo_historial_supervivencia.columns.usuario_id==current_user).all()
                 if consulta_existencia == []:
                     ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo,
                                                                             supervivencia=tasa_supervivencia,
                                                                             usuario_id=current_user)

                     session.execute(ingresoperiodo)
                     session.commit()
                 else:
                     session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                                     where(modelo_historial_supervivencia.columns.periodo == periodo).
                                     filter(modelo_historial_supervivencia.columns.usuario_id==current_user))
                     session.commit()
             else:
                 #para determinar los totales es necesario determinar los animales que
                 # existian en ese año (es decir que naciaron antes de ese año)
                 fecha_fin_nacimiento = datetime(periodo, 12, 31)

                 totales=session.query(modelo_bovinos_inventario). \
                 where(modelo_bovinos_inventario.columns.fecha_nacimiento < fecha_fin_nacimiento).\
                     filter(modelo_bovinos_inventario.columns.usuario_id==current_user).count()

                 muertos=session.query(modelo_datos_muerte). \
                 where(modelo_datos_muerte.columns.fecha_muerte < datetime(periodo, 1, 1)).\
                     filter(modelo_datos_muerte.columns.usuario_id==current_user).count()

                 vendidos=session.query(modelo_ventas). \
                     where(modelo_ventas.columns.fecha_venta < datetime((periodo+1), 12, 31)).\
                     filter(modelo_ventas.columns.usuario_id==current_user).count()

                 totales_periodo= totales - muertos - vendidos

                 tasa_supervivencia = ( (totales_periodo-muertes_periodo)* 100)/totales_periodo

             consulta_existencia = session.query(modelo_historial_supervivencia). \
                 where(modelo_historial_supervivencia.columns.periodo == periodo).\
                 filter(modelo_historial_supervivencia.columns.usuario_id==current_user).all()

             if consulta_existencia == []:
                 ingresoperiodo = modelo_historial_supervivencia.insert().values(periodo=periodo,
                                                                                supervivencia=tasa_supervivencia,
                                                                                usuario_id=current_user)

                 session.execute(ingresoperiodo)
                 session.commit()
             else:
                 session.execute(modelo_historial_supervivencia.update().values(supervivencia=tasa_supervivencia). \
                                 where(modelo_historial_supervivencia.columns.periodo == periodo).
                                 filter(modelo_historial_supervivencia.columns.usuario_id==current_user))
                 session.commit()

             c= c+1

     # el siguiente codigo permite actualizar los periodos si se cambia la primer fecha de muerte
     if consulta_primer_muerte is None or consulta_primer_muerte==[]:
         session.execute(modelo_historial_supervivencia.delete().
                         where(modelo_historial_supervivencia.c.periodo!=(datetime.now().year)).
                         filter(modelo_historial_supervivencia.columns.usuario_id==current_user))
         session.commit()
     else:
         consulta_periodos = session.query(modelo_historial_supervivencia.c.periodo). \
             filter(modelo_historial_supervivencia.c.periodo < consulta_primer_muerte[1].year,
                    modelo_historial_supervivencia.columns.usuario_id==current_user).all()
         if consulta_periodos is None or consulta_periodos == []:
             pass
         else:
             session.execute(modelo_historial_supervivencia.delete().
                             where(modelo_historial_supervivencia.c.periodo < consulta_primer_muerte[1].year).
                             filter(modelo_historial_supervivencia.columns.usuario_id==current_user))
             session.commit()

     #actualizacion del valor mas actual en ela tabla de indicadores
     consulta_ultimo_periodo = session.query(modelo_historial_supervivencia.c.supervivencia).\
         group_by(desc(modelo_historial_supervivencia.c.periodo)).\
         filter(modelo_historial_supervivencia.columns.usuario_id==current_user).all()

     session.execute(update(modelo_indicadores).
                     where(modelo_indicadores.c.id_indicadores == current_user).
                     values(tasa_supervivencia=consulta_ultimo_periodo[0][0]))
     session.commit()

 except Exception as e:
     logger.error(f'Error Funcion tasa_supervivencia: {e}')
     raise
 finally:
     session.close()
