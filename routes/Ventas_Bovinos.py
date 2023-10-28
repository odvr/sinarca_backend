

'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Depends, HTTPException
from config.db import   get_session
from sqlalchemy.orm import Session

from models.modelo_bovinos import modelo_datos_muerte, modelo_ventas
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_datos_muerte, Esquema_Usuario, esquema_modelo_ventas

# Configuracion de las rutas para fash api
Ventas_Bovinos = APIRouter()

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



@Ventas_Bovinos.get("/id_listar_bovino_venta/{id_bovino}",response_model=esquema_modelo_ventas,tags=["Ventas Bovinos"])
async def inventario_bovinos_venta_id(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = db.execute(
            modelo_ventas.select().where(modelo_ventas.columns.id_bovino == id_bovino)).first()
        if consulta is None:
            raise HTTPException(status_code=404, detail="Bovino no encontrado")
        else:
            return consulta
    except Exception as e:
        logger.error(f'Error al obtener Bovinos de venta: {e}')
        raise
    finally:
        db.close()




@Ventas_Bovinos.get("/listar_tabla_ventas",response_model=list[esquema_modelo_ventas])
async def listar_tabla_ventas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        consultaVentas = db.query(modelo_ventas). \
            filter(modelo_ventas.c.estado == "Vendido",modelo_ventas.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE VENTAS : {e}')
        raise
    finally:
        db.close()

    return consultaVentas
