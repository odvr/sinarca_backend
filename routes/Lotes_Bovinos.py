
'''
Librerias requeridas
@autor : odvr
'''
import logging
from fastapi import  Depends
from starlette import status
from fastapi import Form
from config.db import   get_session
from fastapi import APIRouter,Response
from typing import Optional
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_lotes_bovinos
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import  Esquema_Usuario, esquema_lotes_bovinos

# Configuracion de las rutas para fash api
Lotes_Bovinos = APIRouter()

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






@Lotes_Bovinos.get("/listar_tabla_lotes",response_model=list[esquema_lotes_bovinos],tags=["Lotes"] )
async def listar_tabla_lotes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        LotesBovinos = db.query(modelo_lotes_bovinos). \
            filter( modelo_lotes_bovinos.c.usuario_id == current_user).all()
        #itemsAnimalesVeterinaria =  session.execute(modelo_veterinaria.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener Tabla Lotes: {e}')
        raise
    finally:
        db.close()
    return LotesBovinos



@Lotes_Bovinos.post("/crear_lotes_bovinos", status_code=status.HTTP_201_CREATED)
async def crear_lotes_bovinos(nombre_lote: str = Form(...),
                                        estado: Optional [str] = Form(None),
                                        ubicacion: Optional [str] = Form(None),
                                        tipo_uso:  Optional [str] = Form(None),
                                        tamano_lote:  Optional [str] = Form(None),
                                        observaciones:  Optional [str] = Form(None),
                                        db: Session = Depends(get_database_session),
                                        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:




        IngresarLote  = modelo_lotes_bovinos.insert().values( tamano_lote=tamano_lote,
                                                                 nombre_lote=nombre_lote,estado=estado, ubicacion=ubicacion,tipo_uso=tipo_uso,observaciones=observaciones,
                                                                 usuario_id = current_user

                                                                 )

        db.execute(IngresarLote)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear Lotes De Bovinos: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


