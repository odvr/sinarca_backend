

'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Depends
from config.db import   get_session,Rutabase
import os
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_registro_marca
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, Esquema_bovinos, esquema_registro_marca
import crud.crud_bovinos_inventario
# Configuracion de las rutas para fash api
Marcas_Bovinos = APIRouter()
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


"""
La siguiente API realiza el Listado de las imagenes de las Marcas
"""
@Marcas_Bovinos.get("/listar_Marcas", response_model=list[esquema_registro_marca],tags=["Marcas"]
                   )
async def inventario_bovino(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        items = db.query(modelo_registro_marca).filter(modelo_registro_marca.c.usuario_id == current_user ).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Marcas: {e}')
        raise
    finally:
        db.close()

    return items


@Marcas_Bovinos.delete("/Eliminar_Marca/{id_registro_marca}", status_code=200)
async def EliminarMarca(id_registro_marca: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        "Busca la ruta Fisica para eliminar"
        BuscarFotoMarca = crud.bovinos_inventario.Buscar_Ruta_Foto_Marca(db=db, id_registro_marca=id_registro_marca,
                                                                                   current_user=current_user)
        RutasUnida = Rutabase + BuscarFotoMarca

        try:
            os.remove(RutasUnida)
        except:
            pass

        db.execute(modelo_registro_marca.delete().where(modelo_registro_marca.c.id_registro_marca == id_registro_marca))
        db.commit()

        return
    except Exception as e:
        logger.error(f'Error al intentar id_registro_marca: {e}')
        raise
    finally:
        db.close()

