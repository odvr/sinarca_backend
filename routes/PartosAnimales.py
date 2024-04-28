'''
Librerias requeridas
'''

import logging
import json

import crud
from Lib.Lib_Intervalo_Partos import intervalo_partos, fecha_aproximada_parto
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session

from Lib.Registro_partos import registro_partos_animales
from config.db import get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_historial_partos, modelo_partos, modelo_bovinos_inventario, \
    modelo_registro_celos, modelo_abortos
from datetime import date
from fastapi import APIRouter, Response
from fastapi import  status
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_historial_partos, Esquema_Usuario, esquema_partos
from routes.rutas_bovinos import get_current_user
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

partos_bovinos = APIRouter()


def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
@partos_bovinos.post("/crear_Registro_Partos/{id_bovino}/{tipo_parto}/{id_bovino_hijo}")
async def crear_Registro_Partos(id_bovino:str,tipo_parto:str,id_bovino_hijo:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:


        """Se realizan las consultas para indexar los nombres de los animales"""
        ConsultarMadre = db.query(modelo_bovinos_inventario).filter(modelo_bovinos_inventario.columns.id_bovino == id_bovino,
                                                       modelo_bovinos_inventario.c.usuario_id == current_user).first()
        Nombre_Madre = ConsultarMadre.nombre_bovino

        ConsultarHijo = db.query(modelo_bovinos_inventario).filter(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino_hijo,
            modelo_bovinos_inventario.c.usuario_id == current_user).first()
        Nombre_Hijo = ConsultarHijo.nombre_bovino

        ingresoRegistroPartos= modelo_historial_partos.insert().values(id_bovino=id_bovino,

                                                     tipo_parto=tipo_parto,
                                                     id_bovino_hijo=id_bovino_hijo,
                                                     usuario_id=current_user,
                                                     nombre_madre = Nombre_Madre,
                                                     nombre_hijo=Nombre_Hijo,

                                                   )


        db.execute(ingresoRegistroPartos)
        db.commit()
        registro_partos_animales(session=db)
    except Exception as e:
        logger.error(f'Error al Crear INDICE DE PARTOS: {e}')
        raise
    finally:
        db.close()

    return Response(content=json.dumps({"message": "Registro de partos creado exitosamente"}),
                    status_code=status.HTTP_201_CREATED, media_type="application/json")



@partos_bovinos.get("/listar_tabla_Historial_Partos",response_model=list[esquema_historial_partos] )
async def listar_tabla_Partos_Animales(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        intervalo_partos(session=db,current_user=current_user)
        #itemsListarPartos = db.execute(modelo_historial_partos.select()).all()
        itemsListarPartos = db.query(modelo_historial_partos).filter(modelo_historial_partos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return itemsListarPartos


@partos_bovinos.get("/listar_tabla_Historial_Partos_Unidad/{id_bovino}",response_model=list )
async def listar_tabla_Partos_Individual(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        intervalo_partos(session=db,current_user=current_user)

        itemsListarPartos = db.execute(
            modelo_historial_partos.select().where(modelo_historial_partos.columns.id_bovino == id_bovino)).all()

        itemsListarAbortos = db.execute(
            modelo_abortos.select().where(modelo_abortos.columns.id_bovino == id_bovino)).all()

        Historial = []

        # Valida si la consulta no este vacia
        if itemsListarPartos is not None:
            # Recorre la consulta para enviar los datos
            for ListarPartos in itemsListarPartos:
                Historial.append({

                    "id_bovino": ListarPartos.id_bovino,
                    "fecha_parto": ListarPartos.fecha_parto,
                    "tipo_parto": ListarPartos.tipo_parto,
                    "id_bovino_hijo": ListarPartos.id_bovino_hijo,
                    "usuario_id": ListarPartos.usuario_id,
                    "nombre_madre": ListarPartos.nombre_madre,
                    "nombre_hijo": ListarPartos.nombre_hijo,

                })
                # Valida si la consulta no este vacia
        if itemsListarAbortos is not None:
            # Recorre la consulta para enviar los datos
            for AbortosBovinos in itemsListarAbortos:
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
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return consulta



@partos_bovinos.delete("/eliminar_bovino_partos/{id_parto}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino_fecha_partos(id_parto: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        consulta_servicio = db.query(modelo_registro_celos).filter(
            modelo_registro_celos.c.id_servicio == id_parto).all()
        if consulta_servicio is None:
            pass
        else:
            db.execute(modelo_registro_celos.delete().where(modelo_registro_celos.c.id_servicio == id_parto))
            db.commit()
        db.execute(modelo_partos.delete().where(modelo_partos.c.id_parto == id_parto))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino: {e}')
        raise
    finally:
        db.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)

"""
Crear en la tabla de partos para calcular la fecha aproximada
"""
@partos_bovinos.post(
    "/crear_fecha_apoximada_parto/{id_bovino}/{fecha_estimada_prenez}/{id_bovino_padre}/{tipo_monta}",
    status_code=status.HTTP_201_CREATED,)
async def CrearFechaAproximadaParto(id_bovino: str,fecha_estimada_prenez:date, id_bovino_padre:str,tipo_monta:str, db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:

        """Busca el Nombre del Bovino"""


        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)

        if tipo_monta == "Inseminación":
            nombre_pajilla = crud.bovinos_inventario.Buscar_Nombre_Pajilla(db=db,
                                                                           Codigo_toro_pajilla=id_bovino_padre,
                                                                           current_user=current_user)

            ingresocalcularFechaParto_pajilla = modelo_partos.insert().values(id_bovino=id_bovino,
                                                                              fecha_estimada_prenez=fecha_estimada_prenez,
                                                                              usuario_id=current_user,
                                                                              nombre_bovino=nombre_bovino,
                                                                              id_reproductor=id_bovino_padre,
                                                                              nombre_bovino_reproductor=nombre_pajilla,
                                                                              tipo=tipo_monta)
            db.execute(ingresocalcularFechaParto_pajilla)
            db.commit()
        else:
            nombre_bovino_repro = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino_padre,
                                                                        current_user=current_user)

            ingresocalcularFechaParto = modelo_partos.insert().values(id_bovino=id_bovino,
                                                                      fecha_estimada_prenez=fecha_estimada_prenez,
                                                                      usuario_id=current_user,
                                                                      nombre_bovino=nombre_bovino,
                                                                      id_reproductor=id_bovino_padre,
                                                                      nombre_bovino_reproductor=nombre_bovino_repro,
                                                                      tipo=tipo_monta)

            db.execute(ingresocalcularFechaParto)
            db.commit()

        fecha_aproximada_parto(session=db)
        intervalo_partos(session=db, current_user=current_user)


    except Exception as e:
        logger.error(f'Error al Crear ingresocalcularFechaParto: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""
Listar  Fecha aproximada de parto
"""

@partos_bovinos.get("/listar_fecha_parto",response_model=list[esquema_partos] )
async def listar_fecha_parto(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        fecha_aproximada_parto(session=db)
        intervalo_partos(session=db, current_user=current_user)

        #listar_fecha_estimada_parto = db.execute(modelo_partos.select()).all()
        listar_fecha_estimada_parto = db.query(modelo_partos).filter(modelo_partos.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Fecha de Parto: {e}')
        raise
    finally:
        db.close()
    return listar_fecha_estimada_parto


@partos_bovinos.get("/listar_sevcios_Animal/{id_bovino}",response_model=list[esquema_partos] )
async def listar_sevicios_animal(id_bovino:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        listar_fecha_estimada_parto = db.query(modelo_partos).filter(modelo_partos.c.usuario_id == current_user,modelo_partos.c.id_bovino == id_bovino).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Fecha de Parto: {e}')
        raise
    finally:
        db.close()
    return listar_fecha_estimada_parto



@partos_bovinos.delete("/eliminar_registro_Partos_Bovinos/{id_parto}")
async def eliminar_Parto_Bovinos(id_parto: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:
        db.execute(modelo_historial_partos.delete().where(modelo_historial_partos.c.id_parto == id_parto))
        db.commit()
        # retorna un estado de no contenido
        return

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Registro Partos Bovinos: {e}')
        raise
    finally:
        db.close()
