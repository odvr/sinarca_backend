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
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones

from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, Esquema_Usuario
from sqlalchemy import update, between, func
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta
from fastapi import  Depends

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends


ReproductorRutas = APIRouter()


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




@ReproductorRutas.get("/listar_reproductor",response_model=list[esquema_macho_reproductor] )
async def listar_reproductor():
    #llamdo de la funcion para calcular
    #vida_util_macho_reproductor()

    try:
        vida_util_macho_reproductor()
        itemsreproductor = session.execute(modelo_macho_reproductor.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de REPRODUCTOR: {e}')
        raise
    finally:
        session.close()
    return itemsreproductor



"""
Crear Macho Reproductor
"""
@ReproductorRutas.post(
    "/crear_reproductor/{id_bovino}",
    status_code=status.HTTP_201_CREATED)
async def CrearReproductor(id_bovino: str):
    try:
        consulta = condb.execute(
            modelo_macho_reproductor.select().where(
                modelo_macho_reproductor.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            CrearMacho = modelo_macho_reproductor.insert().values(id_bovino=id_bovino)

            condb.execute(CrearMacho)
            condb.commit()
        else:

            condb.execute(modelo_macho_reproductor.update().where(modelo_macho_reproductor.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino))
            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de MACHO REPRODUCTOR: {e}')
        raise
    finally:
        condb.close()

    return Response( status_code=status.HTTP_201_CREATED)






"""la siguiente funncion la fecha en que un macho empezara a bajar fertilidad, para ello
 suma los dias de vida util con la edad del animal para determinar este campo"""
def vida_util_macho_reproductor():
 try:
     #join con tabla de bovinos y consulta

    consulta_machos_r = session.query(modelo_macho_reproductor.c.id_bovino,modelo_bovinos_inventario.c.edad,modelo_bovinos_inventario.c.peso,
                          modelo_bovinos_inventario.c.estado,modelo_bovinos_inventario.c.fecha_nacimiento).\
        join(modelo_macho_reproductor,modelo_bovinos_inventario.c.id_bovino == modelo_macho_reproductor.c.id_bovino).all()


    # Recorre los campos de la consulta
    for i in consulta_machos_r:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[2]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[3]
        # Toma la fecha de nacimiento en este caso es el campo 4
        fecha_nacimiento = i[4]
        # calculo de la vida util mediante la suma del promedio de vida util con la fecha de nacimiento
        fecha_vida_util = fecha_nacimiento + timedelta(2555)
        # actualizacion del campo
        condb.execute(modelo_macho_reproductor.update().values(edad=edad, peso=peso, estado=estado,
                                                     fecha_vida_util=fecha_vida_util). \
                      where(modelo_macho_reproductor.columns.id_bovino == id))

        condb.commit()
 except Exception as e:
   logger.error(f'Error Funcion vida_util_macho_reproductor: {e}')
   raise
 finally:
  condb.close()

@ReproductorRutas.delete("/eliminar_bovino_reproductor/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino_reproductor(id_bovino: str):

    try:
        condb.execute(modelo_macho_reproductor.delete().where(modelo_macho_reproductor.c.id_bovino == id_bovino))
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino REPRODUCTOR: {e}')
        raise
    finally:
        condb.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)
