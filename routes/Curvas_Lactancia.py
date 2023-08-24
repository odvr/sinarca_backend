'''
Librerias requeridas
'''
import logging
from sqlalchemy import func, desc, asc

from Lib.cuvas_lactancias import Reporte_Curvas_lactancia_Mensuales_General
# # importa la conexion de la base de datos
from config.db import condb, session


from fastapi import  status,  APIRouter, Response

from models.modelo_bovinos import modelo_litros_leche, modelo_reporte_curva_lactancia_General
from schemas.schemas_bovinos import esquema_reporte_curva_lactancia_General

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

Curvas_Lantacia = APIRouter()



@Curvas_Lantacia.get("/CurvasLactancia/{id_bovino}",response_model=list[esquema_reporte_curva_lactancia_General])
async def Listar_curvas_lactancia(id_bovino:str):
    try:
        Reporte_Curvas_lactancia_Mensuales_General()

        consulta = list(condb.execute(modelo_reporte_curva_lactancia_General.select(). \
                                            where(modelo_reporte_curva_lactancia_General.columns.id_bovino == id_bovino). \
                                            order_by(desc(modelo_reporte_curva_lactancia_General.columns.Hora_Reporte))).all())

        return  consulta










    except Exception as e:
        logger.error(f'Error al obtener Curvas de lactancia {e}')
        raise
    finally:
        session.close()
