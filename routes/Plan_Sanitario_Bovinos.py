
'''
Librerias requeridas
@autor : odvr
'''
import logging
from fastapi import  Depends
from starlette import status
from fastapi import Form
from datetime import date
import crud.crud_bovinos_inventario
from config.db import   get_session
from fastapi import APIRouter,Response
from typing import Optional
from typing import List
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_lotes_bovinos, \
    modelo_manejo_ternero_recien_nacido_lotes, modelo_eventos_asociados_lotes, modelo_descorne_lotes, \
    modelo_control_parasitos_lotes, modelo_registro_vacunas_bovinos, modelo_control_podologia_lotes
from sqlalchemy.orm import Session
from sqlalchemy import and_
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_lotes_bovinos, esquema_eventos_asociados_lotes

# Configuracion de las rutas para fash api
Plan_Sanitario_Bovinos = APIRouter()

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


@Plan_Sanitario_Bovinos.post("/crear_plan_sanitario", status_code=status.HTTP_201_CREATED)
async def crear_lotes_bovinos(SelectPlanSanidad: Optional [str] = Form(None), estado_respiratorio_inicial_lote: Optional [str] = Form(None),
                              comentario_evento: Optional [str] = Form(None),
                              fecha_desinfeccion_lote: Optional [str] = Form(None),
                              nombre_lote_asociado: Optional [str] = Form(None),
                              producto_usado_lote: Optional [str] = Form(None),
                              metodo_aplicacion_lote:  Optional [str] = Form(None),
                              notificar_evento_lote:  Optional [str] = Form(None),
                              FechaNotificacion:  Optional [date] = Form(None),
                              metodo_descorne:  Optional [str] = Form(None),
                              fecha_descorne:  Optional [date] = Form(None),
                              comentario_descorne:  Optional [str] = Form(None),fecha_tratamiento_lote:  Optional [date] = Form(None),
                              tipo_tratamiento:  Optional [str] = Form(None),
                              producto_usado:  Optional [str] = Form(None),
                              comentario_parasitos:  Optional [str] = Form(None),fecha_registrada_usuario:  Optional [date] = Form(None),
                              tipo_vacuna:  Optional [str] = Form(None),
                              FechaNotificacionVacuna:  Optional [date] = Form(None),fecha_registro_podologia:  Optional [date] = Form(None),
                              espacialista_podologia:  Optional [str] = Form(None),
                              comentario_podologia:  Optional [str] = Form(None),FechaNotificacionPodologia:  Optional [date] = Form(None),
                              db: Session = Depends(get_database_session),
                              current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        if SelectPlanSanidad =="Manejo del Ternero Recién Nacido":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadRecienNacidosBovinos(nombre_lote_asociado=nombre_lote_asociado, estado_respiratorio_inicial_lote=estado_respiratorio_inicial_lote, fecha_desinfeccion_lote=fecha_desinfeccion_lote, producto_usado_lote=producto_usado_lote, metodo_aplicacion_lote=metodo_aplicacion_lote, notificar_evento_lote=notificar_evento_lote, FechaNotificacion=FechaNotificacion, db=db, current_user=current_user)
        if SelectPlanSanidad =="Descorne":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadDescorne(nombre_lote_asociado=nombre_lote_asociado,metodo_descorne=metodo_descorne,fecha_descorne=fecha_descorne,comentario_descorne=comentario_descorne,comentario_evento =comentario_evento,db=db,current_user=current_user)
        if SelectPlanSanidad == "Programa de Control de Parásitos":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadControlParasitos(nombre_lote_asociado=nombre_lote_asociado,fecha_tratamiento_lote=fecha_tratamiento_lote,tipo_tratamiento=tipo_tratamiento,producto_usado=producto_usado,comentario_parasitos=comentario_parasitos,comentario_evento=comentario_evento,db=db,current_user=current_user)

        if SelectPlanSanidad == "Vacunaciones":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadVacunacion(nombre_lote_asociado=nombre_lote_asociado,db=db,current_user=current_user,
                                                                                       fecha_registrada_usuario=fecha_registrada_usuario,tipo_vacuna=tipo_vacuna,
                                                                                       FechaNotificacionVacuna=FechaNotificacionVacuna,comentario_evento=comentario_evento

                                                                                      )
        if SelectPlanSanidad == "Podología":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadPodologia(nombre_lote_asociado=nombre_lote_asociado,fecha_registro_podologia=fecha_registro_podologia,
                                                                                      espacialista_podologia=espacialista_podologia,comentario_podologia=comentario_podologia,
                                                                                      FechaNotificacionPodologia=FechaNotificacionPodologia,comentario_evento=comentario_evento,db=db,current_user=current_user
                                                                                      )

        else:
            logger.error(f'Error al Crear Planes Sanitarios: ')




    except Exception as e:
        logger.error(f'Error al Crear Lotes De Bovinos: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)

@Plan_Sanitario_Bovinos.get("/listar_planes_sanitarios_Asociados/{id_eventos_asociados}",response_model=list,tags=["Plan Sanitario"])
async def listar_planes_sanitarios_asociados(id_eventos_asociados:int ,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        ConsultaEventoDescorne = db.query(modelo_descorne_lotes).filter(modelo_descorne_lotes.c.usuario_id == current_user,modelo_descorne_lotes.c.id_evento_lote_asociado == id_eventos_asociados).all()

        ConsultarEventosDesparacitacion = db.query(modelo_control_parasitos_lotes).filter(modelo_control_parasitos_lotes.c.usuario_id == current_user,modelo_control_parasitos_lotes.c.id_evento_lote_asociado == id_eventos_asociados).all()
        ConsultarEventosVacunacion = db.query(modelo_registro_vacunas_bovinos).filter(
            modelo_registro_vacunas_bovinos.c.usuario_id == current_user,
            modelo_registro_vacunas_bovinos.c.id_evento_lote_asociado == id_eventos_asociados).all()
        ConsultarEventosPodologia = db.query(modelo_control_podologia_lotes).filter(
            modelo_control_podologia_lotes.c.usuario_id == current_user,
            modelo_control_podologia_lotes.c.id_evento_lote_asociado == id_eventos_asociados).all()
        ListaEventosAsociados = []

        if ConsultaEventoDescorne is not None:
            for EventosAsociados in ConsultaEventoDescorne:
                historialEventos = {
                    "id_descorne_lote": EventosAsociados.id_descorne_lote,
                    "metodo_descorne": EventosAsociados.metodo_descorne,
                    "fecha_descorne": EventosAsociados.fecha_descorne,
                    "estado_solicitud_descorne": EventosAsociados.estado_solicitud_descorne,
                    "nombre_bovino": EventosAsociados.nombre_bovino,
                    "comentario_descorne": EventosAsociados.comentario_descorne,
                }
                ListaEventosAsociados.append(historialEventos)

            if ConsultarEventosDesparacitacion is not None:
                for EventosAsociadosDesparacitacion in ConsultarEventosDesparacitacion:
                    historialEventosDesparacitacion = {
                        "id_control_parasitos": EventosAsociadosDesparacitacion.id_control_parasitos,
                        "fecha_tratamiento_lote": EventosAsociadosDesparacitacion.fecha_tratamiento_lote,
                        "tipo_tratamiento": EventosAsociadosDesparacitacion.tipo_tratamiento,
                        "producto_usado": EventosAsociadosDesparacitacion.producto_usado,
                        "nombre_bovino": EventosAsociadosDesparacitacion.nombre_bovino,
                        "estado_solicitud_parasitos": EventosAsociadosDesparacitacion.estado_solicitud_parasitos,
                        "comentario_parasitos": EventosAsociadosDesparacitacion.comentario_parasitos,
                    }
                    ListaEventosAsociados.append(historialEventosDesparacitacion)

            if ConsultarEventosVacunacion is not None:
                for EventosAsociadosVacunacion in ConsultarEventosVacunacion:
                    historialEventosVacunacion = {
                        "id_vacunacion_bovinos": EventosAsociadosVacunacion.id_vacunacion_bovinos,
                        "fecha_registrada_usuario": EventosAsociadosVacunacion.fecha_registrada_usuario,
                        "tipo_vacuna": EventosAsociadosVacunacion.tipo_vacuna,
                        "nombre_lote_asociado": EventosAsociadosVacunacion.nombre_lote_asociado,
                        "nombre_bovino": EventosAsociadosVacunacion.nombre_bovino,


                    }
                    ListaEventosAsociados.append(historialEventosVacunacion)
            if ConsultarEventosPodologia is not None:
                for EventosAsociadosPodologia in ConsultarEventosPodologia:
                    historialEventosVacunacion = {
                        "id_control_podologia": EventosAsociadosPodologia.id_control_podologia,
                        "fecha_registro_podologia": EventosAsociadosPodologia.fecha_registro_podologia,
                        "espacialista_podologia": EventosAsociadosPodologia.espacialista_podologia,
                        "comentario_podologia": EventosAsociadosPodologia.comentario_podologia,
                        "nombre_bovino": EventosAsociadosPodologia.nombre_bovino,
                        "estado_solicitud_podologia": EventosAsociadosPodologia.estado_solicitud_podologia,


                    }
                    ListaEventosAsociados.append(historialEventosVacunacion)



        return ListaEventosAsociados


    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()






@Plan_Sanitario_Bovinos.post("/eliminar_plan_sanitario", status_code=status.HTTP_201_CREATED)
async def eliminar_plan_sanitario_bovinos(id_eventos_asociados: Optional [int] = Form(None),db: Session = Depends(get_database_session),
                              current_user: Esquema_Usuario = Depends(get_current_user)):
    try:



        ConsultarTipoEvento = db.query(modelo_eventos_asociados_lotes).filter(
            modelo_eventos_asociados_lotes.columns.id_eventos_asociados == id_eventos_asociados,
            modelo_eventos_asociados_lotes.c.usuario_id == current_user).first()
        NombreEvento = ConsultarTipoEvento.nombre_evento

        if NombreEvento == "Vacunaciones":
            db.execute(modelo_registro_vacunas_bovinos.delete().where(
                modelo_registro_vacunas_bovinos.c.id_evento_lote_asociado == id_eventos_asociados))
            db.commit()
        if NombreEvento == "Descorne":
            db.execute(modelo_descorne_lotes.delete().where(
                modelo_descorne_lotes.c.id_evento_lote_asociado == id_eventos_asociados))
            db.commit()
        if NombreEvento == "Programa de Control de Parásitos":
            db.execute(modelo_control_parasitos_lotes.delete().where(
                modelo_control_parasitos_lotes.c.id_evento_lote_asociado == id_eventos_asociados))
            db.commit()
        if NombreEvento == "Podología":
            db.execute(modelo_control_podologia_lotes.delete().where(
                modelo_control_podologia_lotes.c.id_evento_lote_asociado == id_eventos_asociados))
            db.commit()
        db.execute(modelo_eventos_asociados_lotes.delete().where(modelo_eventos_asociados_lotes.c.id_eventos_asociados == id_eventos_asociados))
        db.commit()






    except Exception as e:
        logger.error(f'Error al Eliminar Plan sanitario Lotes : {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)




@Plan_Sanitario_Bovinos.get("/listar_planes_sanitarios",response_model=list,tags=["Plan Sanitario"])
async def listar_planes_sanitarios(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        ConsultaManejoTerneros = db.query(modelo_manejo_ternero_recien_nacido_lotes).filter(modelo_manejo_ternero_recien_nacido_lotes.c.usuario_id == current_user).all()
        ConsultaEventosAsociados = db.query(modelo_eventos_asociados_lotes).filter(modelo_eventos_asociados_lotes.c.usuario_id == current_user).all()

        ListaPlanesSanitariosLotes = []

        if ConsultaEventosAsociados is not None:
            for EventosAsociados in ConsultaEventosAsociados:
                historialEventos = {
                    "id_eventos_asociados": EventosAsociados.id_eventos_asociados,
                    "id_lote_asociado": EventosAsociados.id_lote_asociado,
                    "nombre_lote": EventosAsociados.nombre_lote,
                    "nombre_evento": EventosAsociados.nombre_evento,
                    "estado_evento": EventosAsociados.estado_evento,
                    "FechaNotificacion": EventosAsociados.FechaNotificacion,
                    "comentario_evento": EventosAsociados.comentario_evento,
                }
                ListaPlanesSanitariosLotes.append(historialEventos)

        if ConsultaManejoTerneros is not None:
            for ManejoTerneros in ConsultaManejoTerneros:
                historial_item = {
                    "id_manejo_recien_nacido_lote": ManejoTerneros.id_manejo_recien_nacido_lote,
                    "estado_solicitud_recien_nacido": ManejoTerneros.estado_solicitud_recien_nacido,
                    "id_bovino": ManejoTerneros.id_bovino,
                    "nombre_lote_asociado": ManejoTerneros.nombre_lote_asociado,
                    "nombre_bovino": ManejoTerneros.nombre_bovino,
                    "estado_respiratorio_inicial_lote": ManejoTerneros.estado_respiratorio_inicial_lote,
                    "fecha_desinfeccion_lote": ManejoTerneros.fecha_desinfeccion_lote,
                    "producto_usado_lote": ManejoTerneros.producto_usado_lote,
                    "metodo_aplicacion_lote": ManejoTerneros.metodo_aplicacion_lote,
                    "notificar_evento_lote": ManejoTerneros.notificar_evento_lote,

                }
                ListaPlanesSanitariosLotes.append(historial_item)




        return ListaPlanesSanitariosLotes


    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()





@Plan_Sanitario_Bovinos.put("/actualizar_plan_sanitario", status_code=status.HTTP_201_CREATED)
async def actualizar_plan_sanitario(id_eventos_asociados: Optional [int] = Form(None),estado_evento: Optional [str] = Form(None),FechaNotificacion: Optional [date] = Form(None),db: Session = Depends(get_database_session),
                              current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultarTipoEvento = db.query(modelo_eventos_asociados_lotes).filter(
            modelo_eventos_asociados_lotes.columns.id_eventos_asociados == id_eventos_asociados,
            modelo_eventos_asociados_lotes.c.usuario_id == current_user).first()
        NombreEvento = ConsultarTipoEvento.nombre_evento

        if NombreEvento == "Vacunaciones":
            db.execute(modelo_registro_vacunas_bovinos.update().where(
            modelo_registro_vacunas_bovinos.c.id_evento_lote_asociado == id_eventos_asociados).values(
            estado_evento_lotes=estado_evento,

             ))
            db.commit()
        if NombreEvento == "Descorne":
            db.execute(modelo_descorne_lotes.update().where(
            modelo_descorne_lotes.c.id_evento_lote_asociado == id_eventos_asociados).values(
            estado_solicitud_descorne=estado_evento,

             ))
            db.commit()
        if NombreEvento == "Programa de Control de Parásitos":
            db.execute(modelo_control_parasitos_lotes.update().where(
                modelo_control_parasitos_lotes.c.id_evento_lote_asociado == id_eventos_asociados).values(
                estado_solicitud_parasitos=estado_evento,

            ))
            db.commit()
        if NombreEvento == "Podología":
            db.execute(modelo_control_podologia_lotes.update().where(
                modelo_control_podologia_lotes.c.id_evento_lote_asociado == id_eventos_asociados).values(
                estado_solicitud_podologia=estado_evento,

            ))
            db.commit()

        db.execute(modelo_eventos_asociados_lotes.update().where(
            modelo_eventos_asociados_lotes.c.id_eventos_asociados == id_eventos_asociados).values(
            estado_evento=estado_evento,
            FechaNotificacion=FechaNotificacion,
             ))
        db.commit()

    except Exception as e:
        logger.error(f'Error al Actualizar Plan sanitario Lotes : {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)

