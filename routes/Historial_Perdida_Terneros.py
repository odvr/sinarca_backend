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
from Lib.perdida_Terneros import perdida_Terneros1
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones, modelo_usuarios, MUserOut, \
    MUserAuth, modelo_compra, modelo_historial_perdida_terneros

from routes.Reproductor import vida_util_macho_reproductor
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores, esquema_vientres_aptos, UserOut, UserAuth, Usuarios, \
    UsuariosInDB, TokenSchema, TokenPayload, TokenData, esquema_descarte, esquema_modelo_compra, \
    esquema_historial_perdida_terneros
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


Historial_Perdida_Compras = APIRouter()


@Historial_Perdida_Compras.get("/listar_tabla_historial_perdida_compras",response_model=list[esquema_historial_perdida_terneros])
async def listar_tabla_perdida_terneros():
    try:
        perdida_Terneros1()
        items_Perdida_terneros = condb.execute(modelo_historial_perdida_terneros.select()).fetchall()


    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE PERDIDA TERNEROS : {e}')
        raise
    finally:
        session.close()

    return items_Perdida_terneros