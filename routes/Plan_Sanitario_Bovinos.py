
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
    modelo_manejo_ternero_recien_nacido_lotes, modelo_eventos_asociados_lotes
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
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadDescorne(nombre_lote_asociado=nombre_lote_asociado,metodo_descorne=metodo_descorne,fecha_descorne=fecha_descorne,comentario_descorne=comentario_descorne,db=db,current_user=current_user)
        if SelectPlanSanidad == "Programa de Control de Parásitos":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadControlParasitos(nombre_lote_asociado=nombre_lote_asociado,fecha_tratamiento_lote=fecha_tratamiento_lote,tipo_tratamiento=tipo_tratamiento,producto_usado=producto_usado,comentario_parasitos=comentario_parasitos,db=db,current_user=current_user)

        if SelectPlanSanidad == "Vacunaciones":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadVacunacion(nombre_lote_asociado=nombre_lote_asociado,db=db,current_user=current_user,
                                                                                       fecha_registrada_usuario=fecha_registrada_usuario,tipo_vacuna=tipo_vacuna,
                                                                                       FechaNotificacionVacuna=FechaNotificacionVacuna

                                                                                      )
        if SelectPlanSanidad == "Podología":
            crud.crud_bovinos_inventario.bovinos_inventario.CrearPlanSanidadPodologia(nombre_lote_asociado=nombre_lote_asociado,fecha_registro_podologia=fecha_registro_podologia,
                                                                                      espacialista_podologia=espacialista_podologia,comentario_podologia=comentario_podologia,
                                                                                      FechaNotificacionPodologia=FechaNotificacionPodologia,db=db,current_user=current_user
                                                                                      )

        else:
            logger.error(f'Error al Crear Planes Sanitarios: ')




    except Exception as e:
        logger.error(f'Error al Crear Lotes De Bovinos: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)

@Plan_Sanitario_Bovinos.get("/listar_planes_sanitarios",response_model=list,tags=["Plan Sanitario"])
async def listar_planes_sanitarios(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        #itemsListarGananciasPesos = db.query(modelo_manejo_ternero_recien_nacido_lotes).filter(modelo_ganancia_historica_peso.c.usuario_id == current_user).first()
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
                    "historialEventos":historialEventos
                }
                ListaPlanesSanitariosLotes.append(historial_item)




        return ListaPlanesSanitariosLotes


    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        db.close()
