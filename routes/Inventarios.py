

'''
Librerias requeridas
@autor : odvr
'''

import logging



from fastapi import APIRouter, Depends

from Lib.Lib_Calcular_Edad_Bovinos import calculoEdad
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.actualizacion_peso import actualizacion_peso
from Lib.vida_util_macho_reproductor_bovino import vida_util_macho_reproductor
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_usuarios, modelo_bovinos_inventario, modelo_indicadores, \
    modelo_arbol_genealogico
from sqlalchemy.orm import Session

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico

# Configuracion de las rutas para fash api
Inventarios = APIRouter()

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


@Inventarios.get("/listar_inventarios", response_model=list[Esquema_bovinos],tags=["Inventarios"]
                   )
async def inventario_bovino(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    # Se llama la funcion con el fin que esta realice el calculo pertinete a la edad del animal ingresado
    calculoEdad(db=db)
    actualizacion_peso(session=db)

    eliminarduplicados(db=db)

    vida_util_macho_reproductor(db=db)


    try:
        items = db.execute(modelo_bovinos_inventario.select()).fetchall()


    except Exception as e:
        logger.error(f'Error al obtener inventario de bovinos: {e}')
        raise
    finally:
        db.close()

    return items