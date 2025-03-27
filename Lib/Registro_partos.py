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
    modelo_historial_supervivencia, modelo_historial_partos,modelo_detalles_partos
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

"""esta funcion trae y registra automaticamente los partos del modulo de arbol genealogico
"""


def registro_partos_animales(session: Session,current_user):
 try:
     #consulta que trae los datos de madre e hijos
     consulta_partos = session.query(modelo_arbol_genealogico.c.id_bovino_madre,
                                     modelo_arbol_genealogico.c.id_bovino,
                                     modelo_bovinos_inventario.c.fecha_nacimiento,
                                     modelo_arbol_genealogico.c.nombre_bovino_madre,
                                     modelo_bovinos_inventario.c.nombre_bovino,
                                     modelo_arbol_genealogico.c.id_bovino_padre,
                                     modelo_arbol_genealogico.c.nombre_bovino_padre). \
         join(modelo_arbol_genealogico, modelo_bovinos_inventario.c.id_bovino == modelo_arbol_genealogico.c.id_bovino). \
         filter(modelo_bovinos_inventario.c.usuario_id == current_user,
         modelo_arbol_genealogico.c.nombre_bovino_madre!="No registra").all()
     #recorre el bucle for
     for i in consulta_partos:
         #toma los datos de cada parto
         id_bovino_madre = i[0]
         id_bovino = i[1]
         fecha_nacimiento = i[2]
         nombre_bovino_madre = i[3]
         nombre_bovino = i[4]
         id_bovino_padre = i[5]
         nombre_bovino_padre = i[6]

         #esta consulta determina si el parto ya ha sido registrado
         existencia = session.query(modelo_detalles_partos). \
                 where(modelo_detalles_partos.c.id_bovino_hijo == id_bovino).all()
         #en caso de no existir, se insertara el parto
         if existencia==[] or existencia is None:
                 ingresoPartos = modelo_detalles_partos.insert().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_nacimiento,
                                                                         id_bovino_hijo=id_bovino,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombre_bovino)
                 session.execute(ingresoPartos)
                 session.commit()
         #caso contrario, se actualizan sus datos
         else:
                 session.execute(modelo_detalles_partos.update().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_nacimiento,
                                                                         id_bovino_hijo=id_bovino,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombre_bovino). \
                                 where(modelo_detalles_partos.c.id_bovino_hijo == id_bovino))
                 session.commit()

     #el siguiente codigo permite eliminar partos en caso de que un animal haya sido eliminado de arbol genealogico
     existencia_en_arbol = session.query(modelo_detalles_partos).all()
     for i in existencia_en_arbol:
         # Toma el ID del hijo
         id_bovino_hijo = i[6]
         existencia = session.query(modelo_arbol_genealogico). \
             where(modelo_arbol_genealogico.c.id_bovino == id_bovino_hijo).all()
         if existencia is None or existencia == []:
             session.execute(modelo_detalles_partos.delete(). \
                             where(modelo_detalles_partos.c.id_bovino_hijo == id_bovino_hijo))
             session.commit()
         else:
             pass

     #consulta que trae los datos de madre e hijos
     consulta_detalles_partos = session.query(modelo_detalles_partos). \
         filter(modelo_detalles_partos.c.usuario_id == current_user).all()



     #recorre el bucle for
     for i in consulta_detalles_partos:
         nombre_madre = i[3]
         nombre_padre = i[4]
         nombre_hijo = i[7]
         fecha_parto = i[5]
         id_bovino_hijo = i[6]
         id_bovino_madre = i[1]
         id_bovino_padre = i[2]


         consulta_partos_multiples=session.query(modelo_detalles_partos.c.nombre_hijo). \
                 filter(modelo_detalles_partos.c.nombre_madre == nombre_madre,
                 modelo_detalles_partos.c.nombre_padre == nombre_padre,
                 modelo_detalles_partos.c.fecha_parto == fecha_parto,
                 modelo_detalles_partos.c.usuario_id == current_user,
                 modelo_detalles_partos.c.nombre_madre!="No registra").all()




         cantidad=len(consulta_partos_multiples)

         if cantidad==1:
             nombre_hijo=consulta_partos_multiples[0][0]
             tipo="Único"
             existencia = session.query(modelo_historial_partos). \
                 where(modelo_historial_partos.c.id_bovino_hijo == id_bovino_hijo).all()
             if existencia==[] or existencia is None:
                 ingresoPartos = modelo_historial_partos.insert().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_parto,
                                                                         id_bovino_hijo=id_bovino_hijo,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombre_hijo,
                                                                         cantidad=cantidad,
                                                                         tipo_parto=tipo)
                 session.execute(ingresoPartos)
                 session.commit()

             else:
                 session.execute(modelo_historial_partos.update().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_parto,
                                                                         id_bovino_hijo=id_bovino_hijo,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombre_hijo,
                                                                         cantidad=cantidad,
                                                                         tipo_parto=tipo). \
                                 where(modelo_historial_partos.c.id_bovino_hijo == id_bovino_hijo))
                 session.commit()

         else:
             tipo="Múltiple"
             nombres_hijos = (", ".join(str(sublista[0]) for sublista in consulta_partos_multiples))


             existencia = session.query(modelo_historial_partos). \
                 where(modelo_historial_partos.c.nombre_hijo == nombres_hijos).all()
             if existencia==[] or existencia is None:
                 ingresoPartos = modelo_historial_partos.insert().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_parto,
                                                                         id_bovino_hijo=None,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombres_hijos,
                                                                         cantidad=cantidad,
                                                                         tipo_parto=tipo)
                 session.execute(ingresoPartos)
                 session.commit()

             else:
                 session.execute(modelo_historial_partos.update().values(id_bovino_madre=id_bovino_madre,
                                                                        id_bovino_padre=id_bovino_padre,
                                                                        nombre_madre=nombre_bovino_madre,
                                                                        nombre_padre=nombre_bovino_padre,
                                                                         fecha_parto=fecha_parto,
                                                                         id_bovino_hijo=None,
                                                                         usuario_id=current_user,
                                                                         nombre_hijo=nombres_hijos,
                                                                         cantidad=cantidad,
                                                                         tipo_parto=tipo). \
                                 where(modelo_historial_partos.c.nombre_hijo == nombres_hijos))
                 session.commit()



         existencia_en_partos = session.query(modelo_historial_partos).all()
         for i in existencia_en_partos:
             # Toma el ID del hijo
             id_parto = i[0]
             id_bovino_hijo = i[4]
             nombre_hijo=i[10]
             fecha_parto=i[2]
             nombre_madre=i[8]
             nombre_padre=i[9]
             cantidad=i[11]

             if cantidad==1:
                 consulta_existencia_partos=session.query(modelo_detalles_partos.c.nombre_hijo). \
                     filter(modelo_detalles_partos.c.id_bovino_hijo==id_bovino_hijo).all()


                 if consulta_existencia_partos==[] or consulta_existencia_partos is None:
                     session.execute(modelo_historial_partos.delete(). \
                                             where(modelo_historial_partos.c.id_parto == id_parto))
                     session.commit()
                 else:
                     pass

             elif  cantidad>1:
                 consulta_partos_multiples=session.query(modelo_detalles_partos.c.nombre_hijo). \
                     filter(modelo_detalles_partos.c.nombre_madre == nombre_madre,
                     modelo_detalles_partos.c.nombre_padre == nombre_padre,
                     modelo_detalles_partos.c.fecha_parto == fecha_parto,
                     modelo_detalles_partos.c.usuario_id == current_user,
                     modelo_detalles_partos.c.nombre_madre!="No registra").all()

                 nombres_hijos= (", ".join(str(sublista[0]) for sublista in consulta_partos_multiples))

                 if nombres_hijos==nombre_hijo:
                         pass
                 else:
                         session.execute(modelo_historial_partos.delete(). \
                                     where(modelo_historial_partos.c.id_parto == id_parto))
                         session.commit()


 except Exception as e:
     logger.error(f'Error Funcion registro_partos_animales: {e}')
     raise
 finally:
     session.close()