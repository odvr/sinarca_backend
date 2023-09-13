'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Response



# importa la conexion de la base de datos
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_compra
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_modelo_compra, Esquema_Usuario
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, status, HTTPException



# Configuracion de las rutas para fash api
rutas_bovinos = APIRouter()

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

'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''





datos_compra = APIRouter()



def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@datos_compra.post("/crear_compra/{id_bovino}/{estado}/{numero_bono_compra}/{fecha_compra}/{precio_compra}/{razon_compra}/{medio_pago_compra}/{comprador}",status_code=200)
async def crear_reporte_compras(id_bovino:str,estado:str,numero_bono_compra:str,fecha_compra:date,precio_compra:int,razon_compra:str,medio_pago_compra:str,comprador:str ,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        consulta = db.execute(
            modelo_compra.select().where(
                modelo_compra.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoVentas = modelo_compra.insert().values(id_bovino=id_bovino, estado=estado,
                                                          numero_bono_compra=numero_bono_compra, fecha_compra=fecha_compra,
                                                          precio_compra=precio_compra, razon_compra=razon_compra,
                                                          medio_pago_compra=medio_pago_compra, comprador=comprador,usuario_id=current_user)
            db.execute(ingresoVentas)
            db.commit()


        else:

            db.execute(modelo_compra.update().where(modelo_compra.c.id_bovino == id_bovino).values(
                estado=estado,numero_bono_compra=numero_bono_compra, fecha_compra=fecha_compra,
                                                          precio_compra=precio_compra, razon_compra=razon_compra,
                                                          medio_pago_compra=medio_pago_compra, comprador=comprador,usuario_id=current_user))
            db.commit()

            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE COMPRA: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""

"""
@datos_compra.get("/id_listar_bovino_compra/{id_bovino}",response_model=esquema_modelo_compra)
async def inventario_bovinos_compra_id(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = db.execute(
            modelo_compra.select().where(modelo_compra.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        pass
        logger.error(f'Error al obtener Bovinos de Compra: {e}')
        raise
    finally:
        db.close()

    return consulta


@datos_compra.get("/Calcular_animales_Comprados")
async def animales_comprados(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de total de animales vendidos
    estado_comprados = db.query(modelo_compra). \
        filter(modelo_compra.c.estado == "Vivo",modelo_compra.c.usuario_id == current_user).count()


    db.commit()
  except Exception as e:
    logger.error(f'Error Animales Comprados: {e}')
    raise
  finally:
    db.close()
  return estado_comprados



@datos_compra.get("/listar_tabla_compras",response_model=list[esquema_modelo_compra])
async def listar_tabla_compras(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        items_Compra = db.query(modelo_compra). \
            filter(modelo_compra.c.estado == "Vivo",modelo_compra.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE COMPRAS : {e}')
        raise
    finally:
        db.close()

    return items_Compra