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
# # importa la conexion de la base de datos
from config.db import get_session
from crud import crud_bovinos_inventario
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_registro_celos
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_registro_celos

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

registro_celos_rutas = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@registro_celos_rutas.post("/crear_registro_celos", status_code=status.HTTP_201_CREATED)
async def crear_registro_celos(id_bovino: int= Form(...),fecha_celo :date= Form(...),observaciones:str= Form(...),servicio:str= Form(...),id_servicio:Optional[int] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):


    try:
        nombre_bovino=crud.bovinos_inventario.Buscar_Nombre(db=db,id_bovino=id_bovino,current_user=current_user)


        ingresoCelo = modelo_registro_celos.insert().values(id_bovino=id_bovino,
                                                                  fecha_celo=fecha_celo,
                                                                  observaciones=observaciones,
                                                                  servicio=servicio,
                                                                  id_servicio=id_servicio,
                                                                  usuario_id=current_user,
                                                                  nombre_bovino=nombre_bovino)


        db.execute(ingresoCelo)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear registro_celos: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)






@registro_celos_rutas.get("/listar_tabla_celos", response_model=list[esquema_registro_celos] )
async def listar_tabla_celos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        itemsAnimalesEnCelo = db.query(modelo_registro_celos).filter(modelo_registro_celos.c.usuario_id == current_user).all()
        return itemsAnimalesEnCelo

    except Exception as e:
        logger.error(f'Error al obtener Tabla de Celos: {e}')
        raise
    finally:
        db.close()



@registro_celos_rutas.delete("/eliminar_celo_bovino/{id_celo}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_celo_bovino(id_celo: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_registro_celos.delete().where(modelo_registro_celos.c.id_celo == id_celo))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Celo Bovino: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)