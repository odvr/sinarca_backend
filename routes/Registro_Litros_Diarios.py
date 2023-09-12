'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.cuvas_lactancias import Reporte_Curvas_lactancia_Mensuales_General
# # importa la conexion de la base de datos
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_litros_leche
from fastapi import  status,  APIRouter, Response
from datetime import date
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_litros_leche, Esquema_Usuario
from sqlalchemy.orm import Session
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

Produccion_Leche_Litros_Diarios = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@Produccion_Leche_Litros_Diarios.get("/listar_prod_leche_litros_diarios",response_model=list[esquema_litros_leche])
async def inventario_prod_leche_Ls_diarios(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        itemsLeche = db.execute(modelo_litros_leche.select()).all()



    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        db.close()
    return itemsLeche

"""
Realiza la creacion de nuevos del litros diarios en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""

@Produccion_Leche_Litros_Diarios.post("/crear_registro_listros_diarios/{id_bovino}/{fecha_medicion}/{litros_leche}", status_code=status.HTTP_201_CREATED)
async def crear_registro_listros_diarios(id_bovino:str,fecha_medicion:date,litros_leche:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        """
        La siguiente funcion realiza el llamdo para actualizar la curva de lactancia de los animales En general
        """
        Reporte_Curvas_lactancia_Mensuales_General(session=db)

        ingresoFechaLitraje = modelo_litros_leche.insert().values(id_bovino=id_bovino,
                                                                 fecha_medicion=fecha_medicion, litros_leche=litros_leche

                                                                 )

        db.execute(ingresoFechaLitraje)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Litros Diarios: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)



@Produccion_Leche_Litros_Diarios.delete("/eliminar_registro_litros/{id_litros}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino(id_litros: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        db.execute(modelo_litros_leche.delete().where(modelo_litros_leche.c.id_litros == id_litros))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)