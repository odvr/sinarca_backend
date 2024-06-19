
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
from typing import List
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

                                        observaciones:  Optional [str] = Form(None),
                                        db: Session = Depends(get_database_session),
                                        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:




        IngresarLote  = modelo_lotes_bovinos.insert().values(
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




@Lotes_Bovinos.delete("/eliminar_lote_bovino/{id_lote_bovinos}")
async def eliminar_Lote_Bovinos(id_lote_bovinos: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:

        """Consulta el nombre del Lote que será utulizado para la eliminación de la tabla de Bovinos"""
        ConsultarNombreLote =  db.query(modelo_lotes_bovinos).filter(
            modelo_lotes_bovinos.columns.id_lote_bovinos == id_lote_bovinos,
            modelo_lotes_bovinos.c.usuario_id == current_user).first()

        NombreLote = ConsultarNombreLote.nombre_lote
        """Listado de Inventarios"""
        ConsultarTablaBovinosListado = db.query(modelo_bovinos_inventario).filter(
            modelo_bovinos_inventario.c.usuario_id == current_user).all()
        """Recorre la Lista de Bovinos en el inventario de un solo usuario para poder actualizar  el campo de lote"""
        for Bovinos in ConsultarTablaBovinosListado:
            #Id Bovino para actualizar
            IDBovino = Bovinos.id_bovino
            db.execute(modelo_bovinos_inventario.update().values(nombre_lote_bovino="-").where(
                modelo_bovinos_inventario.c.id_bovino == IDBovino,
                modelo_bovinos_inventario.c.nombre_lote_bovino == NombreLote,
                modelo_bovinos_inventario.c.usuario_id == current_user))
            db.commit()

        db.execute(modelo_lotes_bovinos.delete().where(modelo_lotes_bovinos.c.id_lote_bovinos == id_lote_bovinos))
        db.commit()
        return







    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Lote: {e}')
        raise
    finally:
        db.close()




@Lotes_Bovinos.post("/Asociar_Actualizar_Lote_Bovino", status_code=status.HTTP_201_CREATED)
async def Asociar_Actualizar_Lote_Bovino(nombre_lote: str = Form(...),
                                        ListadoBovinos: Optional [List[str]] = Form(None),
                                        db: Session = Depends(get_database_session),
                                        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        """El siguiente For Recorre la Lista de Animales por usuario
        Recibe solamente los ID'S de los animales que son unicos en la base de datos
        """
        for Bovinos in ListadoBovinos:

            db.execute(modelo_bovinos_inventario.update().values(

                nombre_lote_bovino=nombre_lote

            ).where(
                modelo_bovinos_inventario.columns.id_bovino == Bovinos))


            db.commit()
            db.close()


    except Exception as e:
        logger.error(f'Error al Actualizar el Campo del Lote: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)
