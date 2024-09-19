'''
@autor : odvr
Librerias requeridas
'''
import logging
from datetime import  date
from fastapi import APIRouter, Depends,Form,Response,status
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_clientes, modelo_cotizaciones
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_clientes, esquema_cotizaciones
from typing import Optional

# Configuracion de las rutas para fash api
ERP = APIRouter()

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


@ERP.get("/Clientes",response_model=list[esquema_clientes],tags=["ERP"] )
async def Listar_Clientes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        Clientes = db.query(modelo_clientes).filter(modelo_clientes.c.usuario_id == current_user).all()
        return Clientes

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()


@ERP.post("/CrearClientes",status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearClientes(nombre_cliente: Optional [str] = Form(None),direccion: Optional [str] = Form(None),telefono: Optional [str] = Form(None),email: Optional [str] = Form(None),tipo_cliente: Optional [str] = Form(None),fecha_creacion: Optional [date] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    """
    API Para realizar la  creacion de clientes
    :param nombre_cliente:
    :param direccion:
    :param telefono:
    :param email:
    :param tipo_cliente:
    :param fecha_creacion:
    :param db:
    :param current_user:
    :return:
    """
    try:
        CrearCliente = modelo_clientes.insert().values(nombre_cliente=nombre_cliente,direccion=direccion,telefono=telefono,email=email,fecha_creacion=fecha_creacion,tipo_cliente=tipo_cliente,usuario_id=current_user)
        db.execute(CrearCliente)
        db.commit()

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


@ERP.delete("/Eliminar_Cliente/{cliente_id}")
async def Eliminar_cliente(cliente_id: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        db.execute(modelo_clientes.delete().where(modelo_clientes.c.cliente_id == cliente_id))
        db.commit()
        return
    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Cliente: {e}')
        raise
    finally:
        db.close()

"""
Cotizaciones
"""

@ERP.get("/Cotizaciones",response_model=list[esquema_cotizaciones],tags=["ERP"] )
async def Listar_Cotizaciones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        Cotizaciones = db.query(modelo_cotizaciones).filter(modelo_cotizaciones.c.usuario_id == current_user).all()
        return Cotizaciones

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()
@ERP.get("/Listar_Clientes",response_model=list[esquema_cotizaciones] )
async def listar_clientes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        ListarClientes = db.query(modelo_clientes).filter(modelo_clientes.c.usuario_id == current_user).all()
        return ListarClientes
    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        db.close()
