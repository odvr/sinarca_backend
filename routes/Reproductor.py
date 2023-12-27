'''
Librerias requeridas
@autor : odvr
'''

import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response

import crud
from Lib.funcion_vientres_aptos import vientres_aptos
from Lib.vida_util_macho_reproductor_bovino import vida_util_macho_reproductor, \
    relacion_macho_reproductor_vientres_aptos
# importa la conexion de la base de datos
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos
from routes.rutas_bovinos import get_current_user

from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, Esquema_Usuario, esquema_indicadores
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



def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
@ReproductorRutas.get("/listar_reproductor",response_model=list[esquema_macho_reproductor] )
async def listar_reproductor(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):



    try:


        vida_util_macho_reproductor(db=db, current_user=current_user)
        vientres_aptos(session=db, current_user=current_user)
        relacion_macho_reproductor_vientres_aptos(db=db, current_user=current_user)
        #itemsreproductor = db.execute(modelo_macho_reproductor.select()).all()
        itemsreproductor = db.query(modelo_macho_reproductor).filter(modelo_macho_reproductor.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de REPRODUCTOR: {e}')
        raise
    finally:
        db.close()
    return itemsreproductor



"""
Crear Macho Reproductor
"""
@ReproductorRutas.post(
    "/crear_reproductor/{id_bovino}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearReproductor(id_bovino: str,proposito:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        if proposito == "Macho Reproductor":
            consulta = db.execute(
                modelo_macho_reproductor.select().where(
                    modelo_macho_reproductor.columns.id_bovino == id_bovino)).first()
            nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)
            if consulta is None:
                CrearMacho = modelo_macho_reproductor.insert().values(id_bovino=id_bovino, usuario_id=current_user,
                                                                      nombre_bovino=nombre_bovino)

                db.execute(CrearMacho)
                db.commit()
            else:

                db.execute(
                    modelo_macho_reproductor.update().where(modelo_macho_reproductor.c.id_bovino == id_bovino).values(
                        id_bovino=id_bovino))
                db.commit()

        else:
            pass






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de MACHO REPRODUCTOR: {e}')
        raise
    finally:
        db.close()

    return Response( status_code=status.HTTP_201_CREATED)








@ReproductorRutas.delete("/eliminar_bovino_reproductor/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino_reproductor(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        db.execute(modelo_macho_reproductor.delete().where(modelo_macho_reproductor.c.id_bovino == id_bovino))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino REPRODUCTOR: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)


@ReproductorRutas.get("/Indicadores",response_model=list[esquema_indicadores] )
async def relacion_toros_vientres_aptos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        vida_util_macho_reproductor(db=db,current_user=current_user)
        vientres_aptos(session=db,current_user=current_user)
        relacion_macho_reproductor_vientres_aptos(db=db,current_user=current_user)

        response = db.query(modelo_indicadores).filter(modelo_indicadores.c.id_indicadores == current_user).all()

        if response:
            return response
        else:
            return {"message": "No se encontraron resultados"}

    except Exception as e:
        logger.error(f'Error al obtener la consulta de RELACION Y VIENTRES APTOS: {e}')
        raise
    finally:
        db.close()