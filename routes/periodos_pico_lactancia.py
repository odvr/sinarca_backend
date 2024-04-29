'''
Librerias requeridas
'''
import logging
from datetime import date
from typing import Optional

from fastapi import Form,Response
from fastapi import APIRouter, Depends
from fastapi import status, APIRouter, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

import crud
from Lib.periodos_lactancia import periodos_lactancia, pico_y_produccion_lactancia
# # importa la conexion de la base de datos
from config.db import get_session
from crud import crud_bovinos_inventario
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_registro_celos, modelo_partos, modelo_periodos_lactancia, \
    modelo_historial_partos
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_registro_celos, esquema_partos, esquema_historial_partos, \
    esquema_periodos_lactancia

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

registro_periodo_lactancia_rutas = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@registro_periodo_lactancia_rutas.post("/crear_periodo_lactancia", status_code=status.HTTP_201_CREATED)
async def crear_periodo_lactancia(id_bovino: int= Form(...),id_parto: int= Form(...),fecha_inicio_lactancia :date= Form(...),fecha_final_lactancia :Optional[date] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):


    try:
        nombre_bovino=crud.bovinos_inventario.Buscar_Nombre(db=db,id_bovino=id_bovino,current_user=current_user)

        consulta_id=db.query(modelo_periodos_lactancia).\
            filter(modelo_periodos_lactancia.c.id_bovino==id_bovino).all()

        if consulta_id == [] or consulta_id is None:
            ingresoLactancia = modelo_periodos_lactancia.insert().values(id_bovino=id_bovino,
                                                                         nombre_bovino=nombre_bovino,
                                                                         fecha_inicio_lactancia=fecha_inicio_lactancia,
                                                                         fecha_final_lactancia=fecha_final_lactancia,
                                                                         id_parto=id_parto,
                                                                         usuario_id=current_user)

            db.execute(ingresoLactancia)
            db.commit()

            periodos_lactancia(session=db, current_user=current_user)

        else:
            pass

        pico_y_produccion_lactancia(session=db, current_user=current_user)

    except Exception as e:
        logger.error(f'Error al Crear periodo_lactancia: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@registro_periodo_lactancia_rutas.get("/listar_tabla_lactancias", response_model=list[esquema_periodos_lactancia] )
async def listar_tabla_lactancia(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        itemsAnimalesLactancias = db.query(modelo_periodos_lactancia).filter(modelo_periodos_lactancia.c.usuario_id == current_user).all()
        return itemsAnimalesLactancias

    except Exception as e:
        logger.error(f'Error al obtener tabla_lactancias: {e}')
        raise
    finally:
        db.close()


@registro_periodo_lactancia_rutas.delete("/eliminar_lactancia/{id_lactancia}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_lactancia(id_lactancia: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_periodos_lactancia.delete().where(modelo_periodos_lactancia.c.id_lactancia == id_lactancia))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar eliminar_lactancia: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)



@registro_periodo_lactancia_rutas.get("/listar_Partos_Animal/{id_bovino}",response_model=list[esquema_historial_partos] )
async def listar_Partos_animal(id_bovino:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        ListarPartos = db.query(modelo_historial_partos).filter(modelo_historial_partos.c.usuario_id == current_user,modelo_historial_partos.c.id_bovino == id_bovino).all()
        return ListarPartos
    except Exception as e:
        logger.error(f'Error al obtener inventario de Fecha de Parto: {e}')
        raise
    finally:
        db.close()

