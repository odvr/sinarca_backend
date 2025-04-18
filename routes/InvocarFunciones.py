'''
Librerias requeridas
@autor : odvr
'''

import logging
from http.client import HTTPException
from fastapi import APIRouter
from fastapi import BackgroundTasks
from Lib.Tasa_Supervivencia import tasa_supervivencia
from Lib.actualizacion_peso import actualizacion_peso
from Lib.perdida_Terneros import perdida_Terneros1
from config.db import   get_session
from Lib.Lib_Calcular_Edad_Bovinos import calculoEdad
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from sqlalchemy.orm import Session
from schemas.schemas_bovinos import  Esquema_Usuario
from routes.rutas_bovinos import get_current_user
'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from jose import  JWTError

from fastapi import  Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer("token")
'''**********'''

# Configuracion de las rutas para fash api
invocarFunciones = APIRouter()

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


@invocarFunciones.get("/LLamarFunciones", tags=["Pruebas"])
async def llamarfunciones(background_tasks: BackgroundTasks, db: Session = Depends(get_database_session), current_user: Esquema_Usuario = Depends(get_current_user)):
    def tareas():
        calculoEdad(db=db, current_user=current_user)
        eliminarduplicados(db=db, current_user=current_user)
        actualizacion_peso(session=db, current_user=current_user)
        perdida_Terneros1(db=db, current_user=current_user)
        tasa_supervivencia(session=db, current_user=current_user)
        db.close()

    background_tasks.add_task(tareas)
    return {"mensaje": "Funciones en ejecución en segundo plano"}