'''
Librerias requeridas

@autor : odvr

'''

import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import desc

# importa la conexion de la base de datos
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_datos_pesaje, modelo_bovinos_inventario

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
#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""la siguiente funcion consulta los pesos de cada animal, toma el ultimo peso registrado
segun fecha y lo actualiza en el campo peso de la tabla de bovinos"""

def actualizacion_peso(session: Session):
    try:


        # Realiza la consulta general de la tabla de registro de pesos


        consulta_id = session.query(modelo_bovinos_inventario).all()


        # Recorre los campos de la consulta
        for i in consulta_id:
            # Toma el ID del bovino, este es el campo numero 0
            id = i[0]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas reciente
            # la consulta solo muestra los valores asociados a la fecha mas reciente
            consulta_pesos =  (session.execute(modelo_datos_pesaje.select().\
                where(modelo_datos_pesaje.columns.id_bovino==id).\
                    order_by(desc(modelo_datos_pesaje.columns.fecha_pesaje))).first())
            if consulta_pesos is None:
                logger.error(f'Error Funcion actualizacion_peso: {consulta_pesos}')
                pass
            else:
                # actualizacion del campo
                # segun la posicion en la lista se actualizan los campos
                # el campo de peso tiene la posicion 3
                # el campo de id bovino tiene la posicion 1
                # se actualizara el peso en el id igual al de la lista

                session.execute(modelo_bovinos_inventario.update().values(peso=consulta_pesos[3]).where(
                    modelo_bovinos_inventario.columns.id_bovino == consulta_pesos[1]))
                session.commit()


    except Exception as e:
        logger.error(f'Error Funcion actualizacion_peso: {e}')
        raise
    finally:
        session.close()
