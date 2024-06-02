'''
Librerias requeridas
'''
import logging

import crud
from typing import Annotated
from Lib.palpaciones import palpaciones
# # importa la conexion de la base de datos
from config.db import get_session
from fastapi import Form
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_palpaciones
from fastapi import  status,  APIRouter, Response,Request
from datetime import date
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import  Esquema_Usuario, esquema_palpaciones
from sqlalchemy.orm import Session
from typing import Optional
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

Palpaciones_Bovinos = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@Palpaciones_Bovinos.get("/Listar_palpaciones_bovinos",response_model=list[esquema_palpaciones])
async def Listar_Palpaciones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        ItemsPalpaciones = db.query(modelo_palpaciones).filter(modelo_palpaciones.c.usuario_id == current_user).all()



    except Exception as e:
        logger.error(f'Error al obtener inventario de  Palpaciones : {e}')
        raise
    finally:
        db.close()
    return ItemsPalpaciones



@Palpaciones_Bovinos.get("/listar_palpaciones_animal/{id_bovino}",response_model=list[esquema_palpaciones])
async def listado_palpaciones_animal(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        consulta = db.execute(
            modelo_palpaciones.select().where(modelo_palpaciones.columns.id_bovino == id_bovino)).all()
        palpaciones(session=db, current_user=current_user)


    except Exception as e:
        logger.error(f'Error al obtener inventario de palpaciones: {e}')
        raise
    finally:
        db.close()
    return consulta


"""
Crea los Registros de Palpaciones
"""
@Palpaciones_Bovinos.post("/Crear_Registro_Palpaciones_bovino", status_code=status.HTTP_201_CREATED)

async def crear_registro_listros_diarios(id_bovino: str = Form(...),
                                        fecha_palpacion: date = Form(...),
                                        diagnostico_prenez: str = Form(...),
                                        dias_gestacion: Optional [int] = Form(None),
                                        observaciones:  Optional [str] = Form(...),
                                        db: Session = Depends(get_database_session),
                                        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        "Clase para Buscar El Nombre de los Bovinos"
        Nombre_Bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)

        IngrasarPalpacion  = modelo_palpaciones.insert().values(id_bovino=id_bovino,
                                                                 fecha_palpacion=fecha_palpacion,observaciones=observaciones, dias_gestacion=dias_gestacion,diagnostico_prenez=diagnostico_prenez,
                                                                 usuario_id = current_user, nombre_bovino = Nombre_Bovino

                                                                 )

        db.execute(IngrasarPalpacion)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Litros Diarios: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


@Palpaciones_Bovinos.delete("/eliminar_registro_Palpacion/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino(id_bovino: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        db.execute(modelo_palpaciones.delete().where(modelo_palpaciones.c.id_palpacion == id_bovino))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Id Palpacion: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)