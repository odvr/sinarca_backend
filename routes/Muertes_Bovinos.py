


'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import APIRouter, Depends, HTTPException,Response,status
from config.db import   get_session
from sqlalchemy.orm import Session

from models.modelo_bovinos import modelo_datos_muerte, modelo_abortos
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_datos_muerte, Esquema_Usuario

# Configuracion de las rutas para fash api
Muertes_Bovinos = APIRouter()

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



""""
Listar Tabla de Animales con Regristro de Muerte

"""

@Muertes_Bovinos.get("/listar_bovino_muerte",response_model=list)
async def id_inventario_bovinos_muertos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta y seleccion de los animales muertos
        consultaMuertes = db.query(modelo_datos_muerte). \
            filter(modelo_datos_muerte.c.estado == "Muerto",modelo_datos_muerte.c.usuario_id == current_user).all()

        #Consulta La tabla de abortos
        ConsultaAbortos = db.query(modelo_abortos).filter(modelo_abortos.c.usuario_id == current_user).all()
        #Lista que retorna un json para mostrar en el FrondEnd
        Historial = []

        #Valida si la consulta no este vacia
        if consultaMuertes is not None:
            #Recorre la consulta para enviar los datos
            for MuertesBovinos in consultaMuertes:
                Historial.append({

                    "id_datos_muerte": MuertesBovinos.id_datos_muerte,
                    "id_bovino": MuertesBovinos.id_bovino,
                    "razon_muerte": MuertesBovinos.razon_muerte,
                    "estado": MuertesBovinos.estado,
                    "fecha_muerte": MuertesBovinos.fecha_muerte,
                    "usuario_id": MuertesBovinos.usuario_id,
                    "nombre_bovino": MuertesBovinos.nombre_bovino,

                })
                # Valida si la consulta no este vacia
        if ConsultaAbortos is not None:
            # Recorre la consulta para enviar los datos
            for AbortosBovinos in ConsultaAbortos:
                Historial.append({

                    "id_aborto": AbortosBovinos.id_aborto,
                    "id_bovino_abortos": AbortosBovinos.id_bovino,
                    "nombre_bovino_abortos": AbortosBovinos.nombre_bovino,
                    "fecha_aborto": AbortosBovinos.fecha_aborto,
                    "causa": AbortosBovinos.causa,
                    "usuario_id": AbortosBovinos.usuario_id,


                })

        return Historial
    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE MUERTE : {e}')
        raise
    finally:
        db.close()
    # condb.commit()



@Muertes_Bovinos.get("/id_listar_bovino_muerte/{id_bovino}",response_model=esquema_datos_muerte)
async def inventario_bovinos_muertos_id(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = db.execute(
            modelo_datos_muerte.select().where(modelo_datos_muerte.columns.id_bovino == id_bovino)).first()
        if consulta is None:
            raise HTTPException(status_code=404, detail="Bovino no encontrado")
        else:
            return consulta
    except Exception as e:
        logger.error(f'Error al obtener Listar ID de Bovino: {e}')
        raise
    finally:
        db.close()



@Muertes_Bovinos.delete("/eliminar_registro_Aborto/{id_aborto}")
async def Eliminar_Registro_Abortos(id_aborto: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_abortos.delete().where(modelo_abortos.c.id_aborto == id_aborto))
        db.commit()

        return Response(status_code=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Registro Abortos: {e}')
        raise
    finally:
        db.close()

