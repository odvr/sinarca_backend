'''
Librerias requeridas
@autor : odvr
'''

import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from config.db import get_session
from models.modelo_bovinos import modelo_veterinaria, modelo_veterinaria_evoluciones, modelo_veterinaria_comentarios
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_veterinaria_comentarios, Esquema_Usuario
from datetime import date, datetime, timedelta
from fastapi import  status, HTTPException, Depends
from fastapi import  Depends
oauth2_scheme = OAuth2PasswordBearer("/token")

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

Veterinaria = APIRouter()

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@Veterinaria.get("/listar_bovino_Veterinaria/{id_veterinaria}",response_model=esquema_veterinaria,tags=["Veterinaria"])
async def id_inventario_bovino_Veterinaria(id_veterinaria: int,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        consulta = db.execute(
            modelo_veterinaria.select().where(modelo_veterinaria.columns.id_veterinaria == id_veterinaria)).first()
        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta




@Veterinaria.post("/CrearRegistroVeterinaria/{id_bovino}/{sintomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}",status_code=200,tags=["Veterinaria"])
async def CrearRegistroVeterinaria(id_bovino:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        ingresoVeterinaria = modelo_veterinaria.insert().values(id_bovino=id_bovino,sintomas=sintomas,fecha_sintomas=fecha_sintomas,comportamiento=comportamiento,condicion_corporal=condicion_corporal,postura=postura,mucosa_bucal= mucosa_bucal,mucosa_ocular=mucosa_ocular,mucosa_rectal=mucosa_rectal,mucosa_vulvar_prepusial=mucosa_vulvar_prepusial, evolucion=evolucion,tratamiento=tratamiento,piel_pelaje=piel_pelaje)
        db.execute(ingresoVeterinaria)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)



@Veterinaria.post("/ActualizarDetallesVeterinaria/{id_veterinaria}/{sinomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}",status_code=200,tags=["Veterinaria"])
async def ActualizarDetallesVeterinaria(id_veterinaria:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:

        db.execute(modelo_veterinaria.update().where(
            modelo_veterinaria.c.id_veterinaria == id_veterinaria).values(
            sintomas=sintomas,fecha_sintomas=fecha_sintomas,comportamiento=comportamiento,condicion_corporal=condicion_corporal,postura=postura,mucosa_bucal= mucosa_bucal,mucosa_ocular=mucosa_ocular,mucosa_rectal=mucosa_rectal,mucosa_vulvar_prepusial=mucosa_vulvar_prepusial, evolucion=evolucion,tratamiento=tratamiento,piel_pelaje=piel_pelaje))
        db.commit()
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)






@Veterinaria.get("/listar_bovino_Veterinaria_Comentarios/{id_veterinaria}",response_model=list[esquema_veterinaria_comentarios],tags=["Veterinaria"])
async def id_inventario_bovino_Comentarios(id_veterinaria: int,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        consulta = db.execute(
            modelo_veterinaria_comentarios.select().where(modelo_veterinaria_comentarios.columns.id_veterinaria == id_veterinaria)).all()
        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta

"Eliminar Comentarios de Veterinaria"

@Veterinaria.delete("/eliminar_comentarios_evoluciones/{id_veterinaria}",tags=["Veterinaria"])
async def Eliminar_Comentarios_Evoluciones(id_veterinaria: str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        db.execute(modelo_veterinaria_comentarios.delete().where(modelo_veterinaria_comentarios.c.id_veterinaria == id_veterinaria))
        db.commit()
    except Exception as e:
        logger.error(f'Error al intentar Eliminar Comentarios Y Evoluciones: {e}')
        raise
    finally:
        db.close()

    return



@Veterinaria.get("/listar_bovino_Veterinaria_Evoluciones",  response_model=list[esquema_veterinaria_evoluciones],tags=["Veterinaria"])
async def id_inventario_bovino_Veterinaria_Evoluciones(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        tabla_pesaje = db.query(modelo_veterinaria_evoluciones).where(
            modelo_veterinaria_evoluciones.columns.id_bovino).all()

        consulta = db.execute(
            modelo_veterinaria_evoluciones.select()).all()
        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta



@Veterinaria.post("/Crear_Comentario/{id_veterinaria}/{comentarios}/{fecha_comentario}",status_code=200,tags=["Veterinaria"])
async def crear_Comentario(id_veterinaria:int,comentarios:str,fecha_comentario:date,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:

            ingresoEvolucion = modelo_veterinaria_comentarios.insert().values(id_veterinaria=id_veterinaria,comentarios=comentarios,fecha_comentario=fecha_comentario)

            db.execute(ingresoEvolucion)
            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE Comentarios: {e}')
        raise
    finally:
        db.close()

    return Response(content=json.dumps({"message": "Registro de partos creado exitosamente"}),
                    status_code=status.HTTP_201_CREATED, media_type="application/json")


'''


'''
@Veterinaria.post("/Crear_Evolucion/{id_bovino}/{tratamiento_evolucion}/{fecha_evolucion}",status_code=200,tags=["Veterinaria"])
async def crear_evolucion(id_bovino:str,tratamiento_evolucion:str,fecha_evolucion:date,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        consulta = db.execute(
            modelo_veterinaria_evoluciones.select().where(
                modelo_veterinaria_evoluciones.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoEvolucion = modelo_veterinaria_evoluciones.insert().values(id_bovino=id_bovino,tratamiento_evolucion=tratamiento_evolucion,fecha_evolucion=fecha_evolucion)

            db.execute(ingresoEvolucion)
            db.commit()
        else:

            db.execute(modelo_veterinaria_evoluciones.update().where(modelo_veterinaria_evoluciones.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino,tratamiento_evolucion=tratamiento_evolucion,fecha_evolucion=fecha_evolucion))
            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE EVOLUCION: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)



@Veterinaria.get("/listar_tabla_veterinaria/{id_bovino}", response_model=list[esquema_veterinaria],tags=["Veterinaria"] )
async def listar_tabla_veterinaria(id_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        #itemsAnimalesVeterinaria =  session.execute(modelo_veterinaria.select()).all()
        itemsAnimalesVeterinaria = db.execute(
            modelo_veterinaria.select().where(modelo_veterinaria.columns.id_bovino == id_bovino)).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE VETERINARIA: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesVeterinaria



