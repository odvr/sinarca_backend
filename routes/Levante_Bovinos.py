'''
Librerias requeridas
'''

import logging
import json
from sqlalchemy import update

import crud
from Lib.Ganancia_peso import ganancia_peso_levante
from Lib.Levante_Ceba_Bovinos import Estado_Optimo_Levante
from Lib.Lib_Intervalo_Partos import intervalo_partos, fecha_aproximada_parto
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session

from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos, modelo_partos, modelo_levante, modelo_bovinos_inventario, \
    modelo_indicadores, modelo_parametros_levante_ceba
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_produccion_levante, Esquema_Usuario, esquema_parametros_levante_ceba
from routes.rutas_bovinos import get_current_user
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

Levante_Bovinos = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

"""
Lista los animales en Levante

"""

@Levante_Bovinos.get("/listar_prod_levante",response_model=list[esquema_produccion_levante])
async def inventario_levante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    Estado_Optimo_Levante(db=db,current_user=current_user)
    ganancia_peso_levante(session=db,current_user=current_user)
    eliminarduplicados(db=db)


    try:
        #itemsLevante = db.execute(modelo_levante.select()).all()
        itemsLevante = db.query(modelo_levante).filter(modelo_levante.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()
    return itemsLevante

@Levante_Bovinos.get("/Calcular_Animales_Optimo_Levante")
async def Animales_Optimo_Levante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
 try:
    # join,consulta y conteo de animales vivos con estado optimo
    levante_optimo = db.query(modelo_bovinos_inventario.c.estado, modelo_levante.c.estado_optimo_levante). \
        join(modelo_levante, modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_levante.c.estado_optimo_levante == "Estado Optimo").count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_optimos_levante=levante_optimo))

    db.commit()
 except Exception as e:
     logger.error(f'Error Funcion Animales_Optimo_Levante: {e}')
     raise
 finally:
     db.close()
 return levante_optimo


@Levante_Bovinos.post(
    "/crear_prod_levante/{id_bovino}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdLevante(id_bovino: str,proposito:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db)

    try:

        consulta = db.execute(
            modelo_levante.select().where(
                modelo_levante.columns.id_bovino == id_bovino)).first()

        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)
        if consulta is None:
            ingresoplevante = modelo_levante.insert().values(id_bovino=id_bovino, proposito=proposito,usuario_id=current_user,nombre_bovino=nombre_bovino)

            db.execute(ingresoplevante)
            db.commit()

        else:

            db.execute(modelo_levante.update().where(modelo_levante.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino, proposito=proposito))
            db.commit()

            db.commit()


    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Levante: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)



"""
Crea los parametros de levante de acuerdo a los criterios del usuario

"""


@Levante_Bovinos.post(
    "/Crear_Paremetros_Levante/{ParametrizacionEdadLevante}/{ParametrizacionPesoLevante}",
    status_code=status.HTTP_201_CREATED)
async def CrearParametrosLevante(ParametrizacionEdadLevante: int,ParametrizacionPesoLevante:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):


    try:


        consulta = db.execute(
            modelo_parametros_levante_ceba.select().where(
                modelo_parametros_levante_ceba.columns.usuario_id == current_user)).first()


        if consulta is None:
            ingresoparametros = modelo_parametros_levante_ceba.insert().values(edad_levante=ParametrizacionEdadLevante, peso_levante=ParametrizacionPesoLevante,usuario_id=current_user)

            db.execute(ingresoparametros)
            db.commit()

        else:

            db.execute(modelo_parametros_levante_ceba.update().where(modelo_parametros_levante_ceba.c.usuario_id == current_user).values(
                edad_levante=ParametrizacionEdadLevante, peso_levante=ParametrizacionPesoLevante))
            db.commit()



    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Levante: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)




@Levante_Bovinos.get("/listar_datos_levante",response_model=list[esquema_parametros_levante_ceba],tags=["Levante"] )
async def ListarParametrosLevante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        Estado_Optimo_Levante(db=db, current_user=current_user)
        ListarParametrosLevante = db.query(modelo_parametros_levante_ceba). \
            filter( modelo_parametros_levante_ceba.c.peso_levante,modelo_parametros_levante_ceba.c.edad_levante,modelo_parametros_levante_ceba.c.usuario_id == current_user).all()

        return ListarParametrosLevante
    except Exception as e:
        logger.error(f'Error al obtener TABLA Parametros de LEVANTE: {e}')
        raise
    finally:
        db.close()
