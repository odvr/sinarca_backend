'''
Librerias requeridas
'''
import logging

from Lib.actualizacion_peso import actualizacion_peso
from Lib.funcion_peso_por_raza import peso_segun_raza
# # importa la conexion de la base de datos
from config.db import get_session
from sqlalchemy.orm import Session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_datos_pesaje, modelo_orden_peso
from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  status, HTTPException, Depends
from sqlalchemy import func
from datetime import date, datetime, timedelta
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_modelo_Reporte_Pesaje, esquema_orden_peso, Esquema_Usuario

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

pesaje = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
"""
Ingresa los datos para el reporte de pesaje del animal 
"""
@pesaje.post("/fecha_pesaje/{id_bovino}/{fecha_pesaje}/{peso}",status_code=200,tags=["Formualario_Bovinos"])
async def crear_fecha_pesaje(id_bovino:str,fecha_pesaje:date,peso:float,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        ingresoFechaPesaje = modelo_datos_pesaje.insert().values(id_bovino=id_bovino,fecha_pesaje=fecha_pesaje,peso=peso,usuario_id=current_user)


        db.execute(ingresoFechaPesaje)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@pesaje.delete("/Eliminar_Registro_Peso/{id_pesaje}", status_code=200)
async def Eliminar_Re(id_pesaje: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        db.execute(modelo_datos_pesaje.delete().where(modelo_datos_pesaje.c.id_pesaje == id_pesaje))
        db.commit()

    except Exception as e:
        logger.error(f'Error al intentar Eliminar Registro de Arbol Genialogico: {e}')
        raise
    finally:
        db.close()

    return


@pesaje.get("/Promedio_Peso_Raza" , response_model=list[esquema_orden_peso])
async def inventario_prod_leche(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        peso_segun_raza(session=db)
        #itemsPromedioRaza = db.query(modelo_orden_peso).all()
        itemsPromedioRaza = db.query(modelo_orden_peso).filter(modelo_orden_peso.c.usuario_id == current_user).all()
        print(itemsPromedioRaza)

    except Exception as e:
        logger.error(f'Error al obtener inventario de Promedio Por Razas: {e}')
        raise
    finally:
        db.close()
    return itemsPromedioRaza



@pesaje.get("/listar_tabla_pesaje", response_model=list[esquema_modelo_Reporte_Pesaje], tags=["Pesaje"] )
async def listar_tabla_pesaje(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        actualizacion_peso(session=db)
        #tabla_pesaje = db.query(modelo_datos_pesaje).all()
        tabla_pesaje = db.query(modelo_datos_pesaje).filter(modelo_datos_pesaje.c.usuario_id == current_user).all()


    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA PESAJE: {e}')
        raise
    finally:
        db.close()
    return tabla_pesaje




@pesaje.get("/listar_tabla_pesaje_por_animal/{id_bovino}",response_model=list[esquema_modelo_Reporte_Pesaje] )
async def listar_tabla_pesaje_Por_Animal(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        tabla_pesaje = db.query(modelo_datos_pesaje).where(modelo_datos_pesaje.columns.id_bovino == id_bovino).all()


    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA PESAJE POR ANIMAL: {e}')
        raise
    finally:
        db.close()
    return tabla_pesaje