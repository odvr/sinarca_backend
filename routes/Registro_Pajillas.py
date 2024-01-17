'''
Librerias requeridas
@autor : odvr
'''

import logging



from fastapi import APIRouter, Depends

from Lib.Lib_Calcular_Edad_Bovinos import calculoEdad
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.actualizacion_peso import actualizacion_peso
from Lib.eliminacion_pajillas import eliminacion_pajilla
from Lib.vida_util_macho_reproductor_bovino import vida_util_macho_reproductor
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_usuarios, modelo_bovinos_inventario, modelo_indicadores, \
    modelo_arbol_genealogico, modelo_registro_pajillas
from sqlalchemy.orm import Session

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico, \
    esquema_registro_pajillas

# Configuracion de las rutas para fash api
Pajillas = APIRouter()

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


@Pajillas.post("/crear_registro_pajilla/{Codigo_toro_pajilla}/{raza}/{nombre_toro}/{productor}",status_code=200,tags=["Formualario_Bovinos"])
async def crear_registro_pajilla(Codigo_toro_pajilla:str,raza:str,nombre_toro:str,productor:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        ingresoRegistroPajillas = modelo_registro_pajillas.insert().values(Codigo_toro_pajilla=Codigo_toro_pajilla,
                                                                           raza=raza,
                                                                           nombre_toro=nombre_toro,
                                                                           productor=productor, usuario_id=current_user)
        db.execute(ingresoRegistroPajillas)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE Registro Pajillas: {e}')
        raise
    finally:
        db.close()

    return

@Pajillas.get("/listar_tabla_pajillas",response_model=list[esquema_registro_pajillas])
async def listar_tabla_pajillas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        ConsultaRegistrPajillas = db.query(modelo_registro_pajillas).filter(modelo_registro_pajillas.c.usuario_id == current_user).all()
        return ConsultaRegistrPajillas
    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE PAJILLAS : {e}')
        raise
    finally:
        db.close()



@Pajillas.delete("/eliminar_registro_pajilla/{id_pajillas}")
async def eliminar_pajilla(id_pajillas: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        eliminacion_pajilla(id_pajillas,session=db)
        # retorna un estado de no contenido
        return

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Registro Pajillas: {e}')
        raise
    finally:
        db.close()

