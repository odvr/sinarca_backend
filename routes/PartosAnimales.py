'''
Librerias requeridas
'''

import logging
import json
from Lib.Lib_Intervalo_Partos import intervalo_partos, fecha_aproximada_parto
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session

from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos, modelo_partos
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_historial_partos, Esquema_Usuario, esquema_partos
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

partos_bovinos = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
@partos_bovinos.post("/crear_Registro_Partos/{id_bovino}/{fecha_parto}/{tipo_parto}/{id_bovino_hijo}")
async def crear_Registro_Partos(id_bovino:str,fecha_parto: date,tipo_parto:str,id_bovino_hijo:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:

        ingresoRegistroPartos= modelo_historial_partos.insert().values(id_bovino=id_bovino,
                                                     fecha_parto=fecha_parto,
                                                     tipo_parto=tipo_parto,
                                                     id_bovino_hijo=id_bovino_hijo,
                                                     usuario_id=current_user
                                                   )


        db.execute(ingresoRegistroPartos)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INDICE DE PARTOS: {e}')
        raise
    finally:
        db.close()

    return Response(content=json.dumps({"message": "Registro de partos creado exitosamente"}),
                    status_code=status.HTTP_201_CREATED, media_type="application/json")



@partos_bovinos.get("/listar_tabla_Historial_Partos",response_model=list[esquema_historial_partos] )
async def listar_tabla_Partos_Animales(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        intervalo_partos(session=db)
        #itemsListarPartos = db.execute(modelo_historial_partos.select()).all()
        itemsListarPartos = db.query(modelo_historial_partos).filter(modelo_historial_partos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return itemsListarPartos


@partos_bovinos.delete("/eliminar_bovino_partos/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino_fecha_partos(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_partos.delete().where(modelo_partos.c.id_bovino == id_bovino))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)

"""
Crear en la tabla de partos para calcular la fecha aproximada
"""
@partos_bovinos.post(
    "/crear_fecha_apoximada_parto/{id_bovino}/{fecha_estimada_prenez}",
    status_code=status.HTTP_201_CREATED,)
async def CrearFechaAproximadaParto(id_bovino: str,fecha_estimada_prenez:date,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        fecha_aproximada_parto(session=db)

        consulta = db.execute(
            modelo_partos.select().where(
                modelo_partos.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresocalcularFechaParto = modelo_partos.insert().values(id_bovino=id_bovino,
                                                                      fecha_estimada_prenez=fecha_estimada_prenez,usuario_id=current_user)

            db.execute(ingresocalcularFechaParto)
            db.commit()

        else:
            db.execute(modelo_partos.update().where(modelo_partos.c.id_bovino == id_bovino).values(
                            fecha_estimada_prenez=fecha_estimada_prenez))
            db.commit()





    except Exception as e:
        logger.error(f'Error al Crear ingresocalcularFechaParto: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""
Listar  Fecha aproximada de parto
"""

@partos_bovinos.get("/listar_fecha_parto",response_model=list[esquema_partos] )
async def listar_fecha_parto(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        fecha_aproximada_parto(session=db)

        #listar_fecha_estimada_parto = db.execute(modelo_partos.select()).all()
        listar_fecha_estimada_parto = db.query(modelo_partos).filter(modelo_partos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Fecha de Parto: {e}')
        raise
    finally:
        db.close()
    return listar_fecha_estimada_parto