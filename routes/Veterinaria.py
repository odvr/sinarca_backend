'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config.db import condb, session
from models.modelo_bovinos import modelo_veterinaria, modelo_veterinaria_evoluciones, modelo_veterinaria_comentarios
from schemas.schemas_bovinos import esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_veterinaria_comentarios
from datetime import date, datetime, timedelta
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

Veterinaria = APIRouter()

@Veterinaria.get("/listar_bovino_Veterinaria/{id_veterinaria}",response_model=esquema_veterinaria)
async def id_inventario_bovino_Veterinaria(id_veterinaria: int):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        consulta = condb.execute(
            modelo_veterinaria.select().where(modelo_veterinaria.columns.id_veterinaria == id_veterinaria)).first()
        # Cerrar la sesión
        session.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta




@Veterinaria.post("/CrearRegistroVeterinaria/{id_bovino}/{sintomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}",status_code=200)
async def CrearRegistroVeterinaria(id_bovino:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str ):

    try:
        ingresoVeterinaria = modelo_veterinaria.insert().values(id_bovino=id_bovino,sintomas=sintomas,fecha_sintomas=fecha_sintomas,comportamiento=comportamiento,condicion_corporal=condicion_corporal,postura=postura,mucosa_bucal= mucosa_bucal,mucosa_ocular=mucosa_ocular,mucosa_rectal=mucosa_rectal,mucosa_vulvar_prepusial=mucosa_vulvar_prepusial, evolucion=evolucion,tratamiento=tratamiento,piel_pelaje=piel_pelaje)
        condb.execute(ingresoVeterinaria)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)



@Veterinaria.post("/ActualizarDetallesVeterinaria/{id_veterinaria}/{sintomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}",status_code=200)
async def ActualizarDetallesVeterinaria(id_veterinaria:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str ):

    try:

        condb.execute(modelo_veterinaria.update().where(
            modelo_veterinaria.c.id_veterinaria == id_veterinaria).values(
            sintomas=sintomas,fecha_sintomas=fecha_sintomas,comportamiento=comportamiento,condicion_corporal=condicion_corporal,postura=postura,mucosa_bucal= mucosa_bucal,mucosa_ocular=mucosa_ocular,mucosa_rectal=mucosa_rectal,mucosa_vulvar_prepusial=mucosa_vulvar_prepusial, evolucion=evolucion,tratamiento=tratamiento,piel_pelaje=piel_pelaje))
        condb.commit()
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)






@Veterinaria.get("/listar_bovino_Veterinaria_Comentarios/{id_veterinaria}",response_model=list[esquema_veterinaria_comentarios])
async def id_inventario_bovino_Comentarios(id_veterinaria: int):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        consulta = condb.execute(
            modelo_veterinaria_comentarios.select().where(modelo_veterinaria_comentarios.columns.id_veterinaria == id_veterinaria)).all()
        # Cerrar la sesión
        session.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta

"Eliminar Comentarios de Veterinaria"

@Veterinaria.delete("/eliminar_comentarios_evoluciones/{id_veterinaria}")
async def Eliminar_Comentarios_Evoluciones(id_veterinaria: str):

    try:

        condb.execute(modelo_veterinaria_comentarios.delete().where(modelo_veterinaria_comentarios.c.id_veterinaria == id_veterinaria))
        condb.commit()
    except Exception as e:
        logger.error(f'Error al intentar Eliminar Comentarios Y Evoluciones: {e}')
        raise
    finally:
        session.close()

    return



@Veterinaria.get("/listar_bovino_Veterinaria_Evoluciones",  response_model=list[esquema_veterinaria_evoluciones] )
async def id_inventario_bovino_Veterinaria_Evoluciones():

    try:

        tabla_pesaje = session.query(modelo_veterinaria_evoluciones).where(
            modelo_veterinaria_evoluciones.columns.id_bovino).all()

        consulta = condb.execute(
            modelo_veterinaria_evoluciones.select()).all()
        # Cerrar la sesión
        session.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta



@Veterinaria.post("/Crear_Comentario/{id_veterinaria}/{comentarios}/{fecha_comentario}",status_code=200)
async def crear_Comentario(id_veterinaria:int,comentarios:str,fecha_comentario:date ):

    try:

            ingresoEvolucion = modelo_veterinaria_comentarios.insert().values(id_veterinaria=id_veterinaria,comentarios=comentarios,fecha_comentario=fecha_comentario)

            condb.execute(ingresoEvolucion)
            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE Comentarios: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)


'''


'''
@Veterinaria.post("/Crear_Evolucion/{id_bovino}/{tratamiento_evolucion}/{fecha_evolucion}",status_code=200)
async def crear_evolucion(id_bovino:str,tratamiento_evolucion:str,fecha_evolucion:date ):

    try:
        consulta = condb.execute(
            modelo_veterinaria_evoluciones.select().where(
                modelo_veterinaria_evoluciones.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoEvolucion = modelo_veterinaria_evoluciones.insert().values(id_bovino=id_bovino,tratamiento_evolucion=tratamiento_evolucion,fecha_evolucion=fecha_evolucion)

            condb.execute(ingresoEvolucion)
            condb.commit()
        else:

            condb.execute(modelo_veterinaria_evoluciones.update().where(modelo_veterinaria_evoluciones.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino,tratamiento_evolucion=tratamiento_evolucion,fecha_evolucion=fecha_evolucion))
            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE EVOLUCION: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)






