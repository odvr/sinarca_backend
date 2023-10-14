'''
Librerias requeridas
@autor : odvr
'''

import logging
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy.orm import Session
from fastapi import APIRouter, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

import crud
from config.db import get_session
from models.modelo_bovinos import modelo_veterinaria, modelo_veterinaria_evoluciones, modelo_veterinaria_comentarios, \
    modelo_registro_vacunas_bovinos, modelo_bovinos_inventario
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_veterinaria_comentarios, Esquema_Usuario, esquema_registro_vacunas_bovinos
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
        #consulta = db.execute( modelo_veterinaria.select().where(modelo_veterinaria.columns.id_veterinaria == id_veterinaria)).first()

        consulta = db.query(modelo_veterinaria).filter(modelo_veterinaria.columns.id_veterinaria == id_veterinaria,modelo_veterinaria.c.usuario_id == current_user).first()

        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta




@Veterinaria.post("/CrearRegistroVeterinaria/{id_bovino}/{sintomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}/{EstadoHistoriaClinica}",status_code=200,tags=["Veterinaria"])
async def CrearRegistroVeterinaria(id_bovino:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str,EstadoHistoriaClinica:str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        ingresoVeterinaria = modelo_veterinaria.insert().values(id_bovino=id_bovino,sintomas=sintomas,fecha_sintomas=fecha_sintomas,comportamiento=comportamiento,condicion_corporal=condicion_corporal,postura=postura,mucosa_bucal= mucosa_bucal,mucosa_ocular=mucosa_ocular,mucosa_rectal=mucosa_rectal,mucosa_vulvar_prepusial=mucosa_vulvar_prepusial, evolucion=evolucion,tratamiento=tratamiento,piel_pelaje=piel_pelaje,usuario_id=current_user,estado_Historia_clinica=EstadoHistoriaClinica)
        db.execute(ingresoVeterinaria)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)



@Veterinaria.put("/ActualizarDetallesVeterinaria/{id_veterinaria}/{sintomas}/{fecha_sintomas}/{comportamiento}/{condicion_corporal}/{postura}/{mucosa_ocular}/{mucosa_bucal}/{mucosa_rectal}/{mucosa_vulvar_prepusial}/{evolucion}/{tratamiento}/{piel_pelaje}/{estado}",status_code=200,tags=["Veterinaria"])
async def ActualizarDetallesVeterinaria(id_veterinaria:str,sintomas:str,fecha_sintomas:date,comportamiento:str,condicion_corporal:str,postura:str,mucosa_bucal :str, mucosa_ocular:str,mucosa_rectal:str,mucosa_vulvar_prepusial:str,evolucion:str,tratamiento:str,piel_pelaje:str,estado:str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_veterinaria.update().where(
            modelo_veterinaria.c.id_veterinaria == id_veterinaria).values(
            sintomas=sintomas, fecha_sintomas=fecha_sintomas, comportamiento=comportamiento,
            condicion_corporal=condicion_corporal, postura=postura, mucosa_bucal=mucosa_bucal,
            mucosa_ocular=mucosa_ocular, mucosa_rectal=mucosa_rectal, mucosa_vulvar_prepusial=mucosa_vulvar_prepusial,
            evolucion=evolucion, tratamiento=tratamiento, piel_pelaje=piel_pelaje,estado_Historia_clinica=estado))
        db.commit()
        db.commit()


    except Exception as e:
        logger.error(f'Error al Editar Bovino Veterinaria: {e}')
        raise

    finally:
        db.close()

    return Response(status_code=HTTP_204_NO_CONTENT)





@Veterinaria.get("/listar_bovino_Veterinaria_Comentarios/{id_veterinaria}",response_model=list[esquema_veterinaria_comentarios],tags=["Veterinaria"])
async def id_inventario_bovino_Comentarios(id_veterinaria: int,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        #consulta = db.execute(modelo_veterinaria_comentarios.select().where(modelo_veterinaria_comentarios.columns.id_veterinaria == id_veterinaria)).all()

        consulta = db.query(modelo_veterinaria_comentarios).filter(modelo_veterinaria_comentarios.columns.id_veterinaria == id_veterinaria,modelo_veterinaria_comentarios.c.usuario_id == current_user).all()
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

@Veterinaria.delete("/eliminar_comentarios_evoluciones/{id_comentario}",tags=["Veterinaria"])
async def Eliminar_Comentarios_Evoluciones(id_comentario: int,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        db.execute(modelo_veterinaria_comentarios.delete().where(modelo_veterinaria_comentarios.c.id_comentario == id_comentario))
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

        #consulta = db.execute( modelo_veterinaria_evoluciones.select()).all()
        consulta = db.query(modelo_veterinaria_evoluciones).filter(modelo_veterinaria_evoluciones.c.usuario_id == current_user).all()
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

            ingresoEvolucion = modelo_veterinaria_comentarios.insert().values(id_veterinaria=id_veterinaria,comentarios=comentarios,fecha_comentario=fecha_comentario,usuario_id=current_user)

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
@Veterinaria.post("/Crear_Evolucion/{id_bovino}/{fecha_evolucion}",status_code=200,tags=["Veterinaria"])
async def crear_evolucion(id_bovino:str,fecha_evolucion:date,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        consulta = db.execute( modelo_veterinaria_evoluciones.select().where(modelo_veterinaria_evoluciones.columns.id_bovino == id_bovino)).first()
        """Se realizan las consultas para indexar los nombres de los animales"""
        Nombre_Bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)


        if consulta is None:
            ingresoEvolucion = modelo_veterinaria_evoluciones.insert().values(id_bovino=id_bovino,fecha_evolucion=fecha_evolucion,usuario_id=current_user,nombre_bovino = Nombre_Bovino)

            db.execute(ingresoEvolucion)
            db.commit()
        else:

            db.execute(modelo_veterinaria_evoluciones.update().where(modelo_veterinaria_evoluciones.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino,fecha_evolucion=fecha_evolucion,usuario_id=current_user))
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

        itemsAnimalesVeterinaria = db.query(modelo_veterinaria).filter(modelo_veterinaria.c.usuario_id == current_user,modelo_veterinaria.columns.id_bovino == id_bovino).all()
    except Exception as e:
        logger.error(f'Error al obtener TABLA DE VETERINARIA: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesVeterinaria


@Veterinaria.delete("/eliminar_bovino_veterinaria_historial_clinico/{id_bovino}")
async def Eliminar_endogamia(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        db.execute(modelo_veterinaria.delete().where(modelo_veterinaria.c.id_veterinaria == id_bovino))
        db.commit()
    except Exception as e:
        logger.error(f'Error al intentar Eliminar Registro de Arbol Genialogico: {e}')
        raise
    finally:
        db.close()

    return


# Registro de Vacunacion Bovinos


@Veterinaria.post("/CrearRegistroVacunacion/{id_bovino}/{fecha_registro_vacunacion}/{tipo_vacuna}",status_code=200,tags=["Veterinaria"])
async def CrearRegistroVacunacionBovinos(id_bovino:str,fecha_registro_vacunacion:date,tipo_vacuna:str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        fecha_bitacora_Sistema = datetime.now()
        ingresoRegistroVacunacion = modelo_registro_vacunas_bovinos.insert().values(id_bovino=id_bovino,fecha_registrada_usuario=fecha_registro_vacunacion,tipo_vacuna=tipo_vacuna,fecha_bitacora_Sistema=fecha_bitacora_Sistema,usuario_id=current_user)
        db.execute(ingresoRegistroVacunacion)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE REGISTRO DE VACUNAS: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)

@Veterinaria.get("/listar_Registros_Vacunas",  response_model=list[esquema_registro_vacunas_bovinos],tags=["Veterinaria"])
async def Listar_Registro_Vacunas_Bovinos(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        consulta = db.query(modelo_registro_vacunas_bovinos).filter(modelo_registro_vacunas_bovinos.c.usuario_id == current_user).all()
        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Veterinaria Registro Vacunas: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta


@Veterinaria.delete("/Eliminar_Registros_Vacunacion/{id_vacunacion_bovinos}",tags=["Veterinaria"])
async def Eliminar_Registros_Vacunacion(id_vacunacion_bovinos: int,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        db.execute(modelo_registro_vacunas_bovinos.delete().where(modelo_registro_vacunas_bovinos.c.id_vacunacion_bovinos == id_vacunacion_bovinos))
        db.commit()
    except Exception as e:
        logger.error(f'Error al intentar Eliminar Registro Vacunas: {e}')
        raise
    finally:
        db.close()

    return
