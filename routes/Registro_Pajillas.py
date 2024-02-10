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

from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_registro_pajillas, modelo_canastillas
from sqlalchemy.orm import Session
from typing import Optional
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import  Esquema_Usuario, esquema_registro_pajillas, esquema_canastillas

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


@Pajillas.post("/crear_registro_pajilla",status_code=200,tags=["Formualario_Bovinos"])
async def crear_registro_pajilla(Codigo_toro_pajilla:str= Form(...),raza:str= Form(...),nombre_toro:str= Form(...),productor:str= Form(...), unidades:Optional[int] = Form(None), precio:Optional[int] = Form(None), id_canastilla:Optional[int] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        ingresoRegistroPajillas = modelo_registro_pajillas.insert().values(Codigo_toro_pajilla=Codigo_toro_pajilla,
                                                                           raza=raza,
                                                                           nombre_toro=nombre_toro,
                                                                           productor=productor, usuario_id=current_user,unidades=unidades,precio=precio,id_canastilla=id_canastilla)

        nombre_canastilla(session=db, current_user=current_user)
        db.execute(ingresoRegistroPajillas)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE Registro Pajillas: {e}')
        raise
    finally:
        db.close()

    return


@Pajillas.put("/Editar_registro_pajilla",status_code=200,tags=["Pajillas"])
async def editar_registro_pajilla(id_pajillas:int= Form(...), unidades:Optional[int] = Form(None), precio:Optional[int] = Form(None),id_canastilla:Optional[int] = Form(None), db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        print(id_canastilla)

        db.execute(modelo_registro_pajillas.update().values( usuario_id=current_user,unidades=unidades,precio=precio,id_canastilla=id_canastilla).where(modelo_registro_pajillas.columns.id_pajillas == id_pajillas))
        db.commit()
        nombre_canastilla(session=db, current_user=current_user)




    except Exception as e:
        logger.error(f'Error al Editar DE Registro Pajillas: {e}')
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


"""
API para la creación de canastillas
"""

@Pajillas.post("/crear_registro_canastillas/{nombre_Canastilla}",status_code=200,tags=["Canatillas"])
async def crear_registro_canastilla(nombre_Canastilla:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ingresoRegistroPajillas = modelo_canastillas.insert().values(nombre_canastilla=nombre_Canastilla,
                                                                    usuario_id=current_user)


        db.execute(ingresoRegistroPajillas)
        db.commit()



    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE Registro Pajillas: {e}')
        raise
    finally:
        db.close()

    return

@Pajillas.get("/listar_canastillas", response_model=list[esquema_canastillas],tags=["Canastillas"]
                   )
async def inventario_Canastillas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        nombre_canastilla(session=db, current_user=current_user)
        conteo_pajillas(session=db, current_user=current_user)
        items = db.query(modelo_canastillas).filter(modelo_canastillas.c.usuario_id == current_user ).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Canastillas: {e}')
        raise
    finally:
        db.close()

    return items

@Pajillas.delete("/eliminar_Canastilla/{id_canastilla}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_Canastilla(id_canastilla: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        eliminacion_canastilla(id_canastilla_eliminar=id_canastilla,session=db)



    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Canastilla: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)


