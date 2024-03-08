'''
Librerias requeridas
'''

import logging
import json
from sqlalchemy import update

from Lib.Ganancia_peso import ganancia_peso_ceba
from Lib.Levante_Ceba_Bovinos import Estado_Optimo_Levante, Estado_Optimo_Ceba
from Lib.Lib_Intervalo_Partos import intervalo_partos, fecha_aproximada_parto
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session

from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.Tasa_Supervivencia import tasa_supervivencia
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos, modelo_partos, modelo_levante, modelo_bovinos_inventario, \
    modelo_indicadores, modelo_ceba, modelo_parametros_levante_ceba
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_produccion_levante, Esquema_Usuario, esquema_produccion_ceba, \
    esquema_parametros_levante_ceba
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

Ceba_Bovinos = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

'''Listar animales en Ceba'''


@Ceba_Bovinos.get("/listar_prod_ceba",response_model=list[esquema_produccion_ceba] )
async def inventario_ceba(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    #llamdo de la funcion para calcular
    Estado_Optimo_Ceba(db=db,current_user=current_user)
    ganancia_peso_ceba(session=db,current_user=current_user)
    eliminarduplicados(db=db)

    #tasa_supervivencia(session=Session, current_user=current_user)

    try:

        #itemsceba = db.execute(modelo_ceba.select()).all()
        itemsceba = db.query(modelo_ceba).filter(modelo_ceba.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()
    return itemsceba


"la siguiente funcion"
@Ceba_Bovinos.get("/Calcular_Animales_Optimo_Ceba")
async def Animales_Optimo_Ceba(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # join,consulta y conteo de animales vivos con estado optimo
    ceba_optimo = db.query(modelo_bovinos_inventario.c.estado, modelo_ceba.c.estado_optimo_ceba). \
        join(modelo_ceba, modelo_bovinos_inventario.c.id_bovino == modelo_ceba.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_ceba.c.estado_optimo_ceba == "Estado Optimo").count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_optimos_ceba=ceba_optimo))
    logger.info(f'Funcion Animales_Optimo_Ceba {ceba_optimo} ')
    db.commit()
  except Exception as e:
      logger.error(f'Error Funcion Animales_Optimo_Ceba: {e}')
      raise
  finally:
      db.close()
  return ceba_optimo

@Ceba_Bovinos.post(
    "/Crear_Paremetros_Ceba/{ParametrizacionEdadCeba}/{ParametrizacionPesoCeba}",
    status_code=status.HTTP_201_CREATED)
async def CrearParametrosCeba(ParametrizacionEdadCeba: int,ParametrizacionPesoCeba:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):


    try:


        consulta = db.execute(
            modelo_parametros_levante_ceba.select().where(
                modelo_parametros_levante_ceba.columns.usuario_id == current_user)).first()


        if consulta is None:
            ingresoparametros = modelo_parametros_levante_ceba.insert().values(edad_ceba=ParametrizacionEdadCeba, peso_ceba=ParametrizacionPesoCeba,usuario_id=current_user)

            db.execute(ingresoparametros)
            db.commit()

        else:

            db.execute(modelo_parametros_levante_ceba.update().where(modelo_parametros_levante_ceba.c.usuario_id == current_user).values(
                edad_ceba=ParametrizacionEdadCeba, peso_ceba=ParametrizacionPesoCeba))
            db.commit()



    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Ceba: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)




@Ceba_Bovinos.get("/listar_datos_ceba",response_model=list[esquema_parametros_levante_ceba],tags=["Levante"] )
async def ListarParametrosLevante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListarParametrosLevante = db.query(modelo_parametros_levante_ceba). \
            filter( modelo_parametros_levante_ceba.c.peso_ceba,modelo_parametros_levante_ceba.c.edad_ceba,modelo_parametros_levante_ceba.c.usuario_id == current_user).all()

        return ListarParametrosLevante
    except Exception as e:
        logger.error(f'Error al obtener TABLA Parametros de Ceba: {e}')
        raise
    finally:
        db.close()
