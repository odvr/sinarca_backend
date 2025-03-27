'''
Librerias requeridas
@autor : odvr
'''

import logging
from fastapi import Form,Response
from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from Lib.canastillas_pajillas import nombre_canastilla, conteo_pajillas, eliminacion_canastilla
from Lib.eliminacion_pajillas import eliminacion_pajilla
from Lib.duracion_secado import duracion_secado

from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_periodos_secado, modelo_canastillas, modelo_embriones_transferencias
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from routes.rutas_bovinos import get_current_user
import crud
from schemas.schemas_bovinos import  Esquema_Usuario, esquema_periodos_secado, esquema_canastillas
from Lib.transferencia_embriones import registro_embriones

# Configuracion de las rutas para fash api
Transferencia_embriones = APIRouter()

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


@Transferencia_embriones.post("/crear_registro_embrion",status_code=200,tags=["Embriones"])
async def crear_registro_embrion(raza:str= Form(...),inf_madre_biologica:str= Form(...),inf_padre_biologico:str= Form(...),estado:str= Form(...),fecha_implante: Optional [date] = Form(None),id_receptora: Optional [int] = Form(None),resultado_trasnplante: Optional [str] = Form(None),id_bovino_hijo: Optional [int] = Form(None), observaciones: Optional [str] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        ingresoRegistroEmbrion = modelo_embriones_transferencias.insert().values(raza=raza,
                                                                           inf_madre_biologica=inf_madre_biologica,
                                                                           inf_padre_biologico=inf_padre_biologico,
                                                                           estado=estado,
                                                                           fecha_implante=fecha_implante,
                                                                           observaciones=observaciones,
                                                                           id_receptora=id_receptora,
                                                                           resultado_trasnplante=resultado_trasnplante,
                                                                           id_bovino_hijo=id_bovino_hijo)

        db.execute(ingresoRegistroEmbrion)
        db.commit()
        registro_embriones(session=db, current_user=current_user)



    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE registro_embrion: {e}')
        raise
    finally:
        db.close()

    return


@Transferencia_embriones.put("/Editar_registro_embrion",status_code=200,tags=["Embriones"])
async def editar_registro_embrion(id_embrion:int= Form(...),raza:str= Form(...),inf_madre_biologica:str= Form(...),inf_padre_biologico:str= Form(...),estado:str= Form(...),fecha_implante: Optional [date] = Form(None),id_receptora: Optional [int] = Form(None),resultado_trasnplante: Optional [str] = Form(None),id_bovino_hijo: Optional [int] = Form(None), observaciones: Optional [str] = Form(None), db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        db.execute(modelo_embriones_transferencias.update().values(raza=raza,
                                                                   inf_madre_biologica=inf_madre_biologica,
                                                                   inf_padre_biologico=inf_padre_biologico,
                                                                   estado=estado,
                                                                   fecha_implante=fecha_implante,
                                                                   observaciones=observaciones,
                                                                   id_receptora=id_receptora,
                                                                   resultado_trasnplante=resultado_trasnplante,
                                                                   id_bovino_hijo=id_bovino_hijo).where(modelo_embriones_transferencias.columns.id_embrion==id_embrion))
        db.commit()
        registro_embriones(session=db, current_user=current_user)





    except Exception as e:
        logger.error(f'Error al Editar_registro_embrion: {e}')
        raise
    finally:
        db.close()

    return



@Transferencia_embriones.get("/listar_tabla_embriones",response_model=list[esquema_periodos_secado],tags=["Embriones"])
async def listar_tabla_periodos_secado(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        ConsultaRegistroEmbriones = db.query(modelo_embriones_transferencias).filter(modelo_embriones_transferencias.c.usuario_id == current_user).all()
        return ConsultaRegistroEmbriones
    except Exception as e:
        logger.error(f'Error al obtener tabla_embriones_transferencias : {e}')
        raise
    finally:
        db.close()



@Transferencia_embriones.delete("/eliminar_registro_embriones{id_embrion}",tags=["Embriones"])
async def eliminar_embrion(id_embrion: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
      #consulta el periodo
      consulta_embrion = db.query(modelo_embriones_transferencias).\
          filter(modelo_embriones_transferencias.c.id_embrion==id_embrion).all()
      #si el periodo no existe no habra cambios
      if consulta_embrion ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          db.execute(modelo_embriones_transferencias.delete().where(modelo_embriones_transferencias.c.id_embrion == id_embrion))
          db.commit()
      # retorna un estado de no contenido
      return

    except Exception as e:
        logger.error(f'Error al Intentar eliminar_registro_embrion: {e}')
        raise
    finally:
        db.close()

