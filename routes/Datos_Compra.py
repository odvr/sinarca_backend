'''
Librerias requeridas
@autor : odvr
'''

import logging
import math
from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso

from Lib.endogamia import endogamia
from Lib.funcion_litros_por_raza import litros_por_raza
from Lib.funcion_peso_por_raza import peso_segun_raza
from Lib.funcion_vientres_aptos import vientres_aptos

# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones, modelo_usuarios, MUserOut, \
    MUserAuth, modelo_compra
from routes.rutas_bovinos import get_current_user

from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores, esquema_vientres_aptos, UserOut, UserAuth, Usuarios, \
    UsuariosInDB, TokenSchema, TokenPayload, TokenData, esquema_descarte, esquema_modelo_compra, Esquema_Usuario
from sqlalchemy import update, between, func
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends



'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from uuid import uuid4


oauth2_scheme = OAuth2PasswordBearer("/token")
'''***********'''


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
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from fastapi import FastAPI, status, HTTPException


datos_compra = APIRouter()


@datos_compra.post("/crear_compra/{id_bovino}/{estado}/{numero_bono_compra}/{fecha_compra}/{precio_compra}/{razon_compra}/{medio_pago_compra}/{comprador}",status_code=200)
async def crear_reporte_compras(id_bovino:str,estado:str,numero_bono_compra:str,fecha_compra:date,precio_compra:int,razon_compra:str,medio_pago_compra:str,comprador:str,current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:

        consulta = condb.execute(
            modelo_compra.select().where(
                modelo_compra.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoVentas = modelo_compra.insert().values(id_bovino=id_bovino, estado=estado,
                                                          numero_bono_compra=numero_bono_compra, fecha_compra=fecha_compra,
                                                          precio_compra=precio_compra, razon_compra=razon_compra,
                                                          medio_pago_compra=medio_pago_compra, comprador=comprador)
            condb.execute(ingresoVentas)
            condb.commit()


        else:

            condb.execute(modelo_compra.update().where(modelo_compra.c.id_bovino == id_bovino).values(
                estado=estado,numero_bono_compra=numero_bono_compra, fecha_compra=fecha_compra,
                                                          precio_compra=precio_compra, razon_compra=razon_compra,
                                                          medio_pago_compra=medio_pago_compra, comprador=comprador))
            condb.commit()

            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE COMPRA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""

"""
@datos_compra.get("/id_listar_bovino_compra/{id_bovino}",response_model=esquema_modelo_compra)
async def inventario_bovinos_compra_id(id_bovino:str,current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = session.execute(
            modelo_compra.select().where(modelo_compra.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al obtener Bovinos de Compra: {e}')
        raise
    finally:
        session.close()

    return consulta


@datos_compra.get("/Calcular_animales_Comprados")
async def animales_comprados(current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de total de animales vendidos
    estado_comprados = session.query(modelo_compra). \
        filter(modelo_compra.c.estado == "Vivo").count()
    # actualizacion de campos
    """
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_vendidos=estado_vendido))
    logger.info(f'Funcion animales_vendidos {estado_vendido} ')
    
    """

    session.commit()
  except Exception as e:
    logger.error(f'Error Animales Comprados: {e}')
    raise
  finally:
    session.close()
  return estado_comprados



@datos_compra.get("/listar_tabla_compras",response_model=list[esquema_modelo_compra])
async def listar_tabla_compras(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        items_Compra = condb.execute(modelo_compra.select()).fetchall()
        items_Compra = session.query(modelo_compra). \
            filter(modelo_compra.c.estado == "Vivo").all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE COMPRAS : {e}')
        raise
    finally:
        session.close()

    return items_Compra