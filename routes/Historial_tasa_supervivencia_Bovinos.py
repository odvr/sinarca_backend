'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Response
from sqlalchemy.orm import Session

from Lib.natalidad_paricion_real import natalidad_paricion_real
# importa la conexion de la base de datos
from config.db import get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_perdida_terneros, modelo_historial_supervivencia, \
    modelo_natalidad_paricion_real

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_historial_perdida_terneros, Esquema_Usuario, esquema_historial_supervivencia

'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


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



Historial_Tasa_Supervivencia = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@Historial_Tasa_Supervivencia.get("/listar_tabla_historial_tasa_supervivencia",response_model=list)
async def listar_tabla_perdida_terneros(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        natalidad_paricion_real(session=db, current_user=current_user)
        itemsListarNtalidades = db.query(modelo_natalidad_paricion_real).filter(
            modelo_natalidad_paricion_real.c.usuario_id == current_user).all()
        items_tasa_supervivencia = db.query(modelo_historial_supervivencia).filter(modelo_historial_supervivencia.c.usuario_id == current_user).all()
        db.close()
        # Declara la Variable que contiene una lista
        HistorialTasaParicionReal = []
        #Valida si la consulta no esta vacia
        if itemsListarNtalidades is not None:
            for Natalidad in itemsListarNtalidades:
                #define la validable para agregar la lista y ingresa el diccionario de la información
                ItemsNatalidad = {
                    "periodoNatalidad": Natalidad.periodo,
                    "intervalo_entre_partos_periodo": Natalidad.intervalo_entre_partos_periodo,
                    "natalidad_paricion_real": Natalidad.natalidad_paricion_real,

                }

                HistorialTasaParicionReal.append(ItemsNatalidad)
        else:
            pass
        if items_tasa_supervivencia is not None:
            for supervivencia in items_tasa_supervivencia:
                # define la validable para agregar la lista
                ItemsSupervivencia = {
                    "periodo": supervivencia.periodo,
                    "supervivencia": supervivencia.supervivencia,


                }
                print(ItemsSupervivencia)
                HistorialTasaParicionReal.append(ItemsSupervivencia)




        # Retorna la lista
        return HistorialTasaParicionReal

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE TASA SUPERVIVENCIA y Natalidad: {e}')
        raise
    finally:
        db.close()

