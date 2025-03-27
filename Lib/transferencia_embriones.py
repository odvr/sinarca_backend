'''
Librerias requeridas
@autor : odvr
'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response
from sqlalchemy.sql.functions import current_user

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte,  modelo_arbol_genealogico, modelo_veterinaria_evoluciones, \
    modelo_historial_supervivencia, modelo_historial_partos,modelo_detalles_partos,modelo_embriones_transferencias
from routes.Reproductor import vida_util_macho_reproductor
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores
from sqlalchemy import update, between, func, asc, desc
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta
import crud



from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends

oauth2_scheme = OAuth2PasswordBearer("/token")

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

"""esta funcion trae y registra automaticamente los partos del modulo de arbol genealogico
"""


def registro_embriones(session: Session,current_user):
 try:
     embriones = session.query(modelo_embriones_transferencias). \
                 where(modelo_embriones_transferencias.c.usuario_id == current_user).all()

     #recorre el bucle for
     for i in embriones:
         #toma los datos
         id_embrion = i[0]
         estado = i[3]
         id_receptora = i[5]
         resultado_trasnplante = i[7]
         id_bovino_hijo = i[9]

         if estado=="Transferido" and id_receptora!=None:
             nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_receptora, current_user=current_user)

             session.execute(modelo_embriones_transferencias.update().values(nombre_receptora=nombre_bovino). \
                                 where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
             session.commit()

         elif  resultado_trasnplante=="Exitoso" and id_bovino_hijo!=None:
             nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_receptora, current_user=current_user)

             fecha_parto = session.query(modelo_bovinos_inventario). \
                 where(modelo_bovinos_inventario.c.id_bovino == id_bovino_hijo).all()

             session.execute(modelo_embriones_transferencias.update().values(nombre_hijo=nombre_bovino,fecha_parto=fecha_parto[0][1]). \
                                 where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
             session.commit()

         elif resultado_trasnplante=="Fallido" and estado!="Transferido":
             session.execute(modelo_embriones_transferencias.update().values(nombre_receptora=None,
             nombre_hijo=None,fecha_parto=None,id_receptora=None,id_bovino_hijo=None). \
                                 where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
             session.commit()

         elif resultado_trasnplante=="Fallido":
             nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_receptora, current_user=current_user)
             session.execute(modelo_embriones_transferencias.update().values(nombre_receptora=nombre_bovino,
             nombre_hijo=None,fecha_parto=None,id_receptora=id_receptora,id_bovino_hijo=None). \
                                 where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
             session.commit()

         else:
             session.execute(modelo_embriones_transferencias.update().values(nombre_receptora=None,
             nombre_hijo=None,fecha_parto=None,id_receptora=None,id_bovino_hijo=None). \
                                 where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
             session.commit()



 except Exception as e:
     logger.error(f'Error Funcion registro_partos_embriones: {e}')
     raise
 finally:
     session.close()