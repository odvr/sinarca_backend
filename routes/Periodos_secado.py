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
from models.modelo_bovinos import  modelo_periodos_secado, modelo_canastillas
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from routes.rutas_bovinos import get_current_user
import crud
from schemas.schemas_bovinos import  Esquema_Usuario, esquema_periodos_secado, esquema_canastillas

# Configuracion de las rutas para fash api
Periodos_secado = APIRouter()

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


@Periodos_secado.post("/crear_registro_periodo_secado",status_code=200,tags=["Periodos_secado"])
async def crear_registro_periodo_secado(id_bovino:int= Form(...),fecha_inicio_secado: Optional [date] = Form(None),fecha_final_secado: Optional [date] = Form(None),tratamiento: Optional [str] = Form(None), observaciones: Optional [str] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)
        ingresoRegistroPeriodoSecado = modelo_periodos_secado.insert().values(id_bovino=id_bovino,
                                                                           nombre_bovino=nombre_bovino,
                                                                           fecha_inicio_secado=fecha_inicio_secado,
                                                                           fecha_final_secado=fecha_final_secado,
                                                                           tratamiento=tratamiento,
                                                                           observaciones=observaciones,
                                                                           usuario_id=current_user,)

        db.execute(ingresoRegistroPeriodoSecado)
        db.commit()
        duracion_secado(session=db, current_user=current_user)



    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE registro_periodo_secado: {e}')
        raise
    finally:
        db.close()

    return


@Periodos_secado.put("/Editar_registro_periodo_secado",status_code=200,tags=["Periodos_secado"])
async def editar_registro_periodo_secado(id_secado:int= Form(...),fecha_inicio_secado: Optional [date] = Form(None),fecha_final_secado: Optional [date] = Form(None),tratamiento: Optional [str] = Form(None), observaciones: Optional [str] = Form(None), db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        db.execute(modelo_periodos_secado.update().values(usuario_id=current_user,fecha_inicio_secado=fecha_inicio_secado,fecha_final_secado=fecha_final_secado,tratamiento=tratamiento,observaciones=observaciones).where(modelo_periodos_secado.columns.id_secado==id_secado))
        db.commit()
        duracion_secado(session=db, current_user=current_user)





    except Exception as e:
        logger.error(f'Error al Editar_registro_periodo_secado: {e}')
        raise
    finally:
        db.close()

    return



@Periodos_secado.get("/listar_tabla_periodos_secado",response_model=list[esquema_periodos_secado],tags=["Periodos_secado"])
async def listar_tabla_periodos_secado(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        ConsultaRegistroPeriodosSecado = db.query(modelo_periodos_secado).filter(modelo_periodos_secado.c.usuario_id == current_user).all()
        return ConsultaRegistroPeriodosSecado
    except Exception as e:
        logger.error(f'Error al obtener tabla_periodos_secadoS : {e}')
        raise
    finally:
        db.close()



@Periodos_secado.delete("/eliminar_registro_periodos_secado/{id_secado}",tags=["Periodos_secado"])
async def eliminar_periodos_secado(id_secado: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
      #consulta el periodo
      consulta_periodo_secado = db.query(modelo_periodos_secado).\
          filter(modelo_periodos_secado.c.id_secado==id_secado).all()
      #si el periodo no existe no habra cambios
      if consulta_periodo_secado ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          db.execute(modelo_periodos_secado.delete().where(modelo_periodos_secado.c.id_secado == id_secado))
          db.commit()
      # retorna un estado de no contenido
      return

    except Exception as e:
        logger.error(f'Error al Intentar eliminar_registro_periodos_secado: {e}')
        raise
    finally:
        db.close()

