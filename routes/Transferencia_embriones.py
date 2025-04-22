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
from models.modelo_bovinos import  modelo_periodos_secado, modelo_canastillas, modelo_embriones_transferencias,modelo_hembras_donantes,\
         modelo_bovinos_inventario,modelo_extracciones_embriones, modelo_registro_pajillas, modelo_transferencias_embriones, modelo_termocriogenico_embriones,\
         modelo_canastillas_embriones,modelo_gondolas_embriones,modelo_banco_embriones,modelo_hembras_receptoras, modelo_embriones, modelo_historial_partos
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from routes.rutas_bovinos import get_current_user
import crud
from schemas.schemas_bovinos import Esquema_Usuario, esquema_periodos_secado, esquema_canastillas, \
    esquema_embriones_transferencias,esquema_hembras_donantes
from Lib.transferencia_embriones import registro_embriones

# Configuracion de las rutas para fash api
Transferencia_embriones = APIRouter()

# Configuracion de la libreria para los logs de sinarca
# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Crea un manejador de archivo para guardar el log
log_file = 'LogEmbriones.log'
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


@Transferencia_embriones.post("/crear_registro_donante_embrion", status_code=200, tags=["Embriones"])
async def crear_registro_donante_embrion(
    id_bovino: int = Form(...),

    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_animal=db.query(modelo_bovinos_inventario).\
            filter(modelo_bovinos_inventario.c.id_bovino==id_bovino).first()


        nombre_bovino=consulta_datos_animal.nombre_bovino
        edad=consulta_datos_animal.edad
        raza=consulta_datos_animal.raza
        edad_AA_MM_DD=consulta_datos_animal.edad_YY_MM_DD

        consulta_hembra_donante=db.query(modelo_hembras_donantes).\
            filter(modelo_hembras_donantes.c.id_bovino==id_bovino).all()

        if consulta_hembra_donante is None or consulta_hembra_donante==[]:
            # Insertar los datos en la base de datos
            ingreso_Donante = modelo_hembras_donantes.insert().values(
                id_bovino=id_bovino,
                nombre_bovino=nombre_bovino,
                edad=edad,
                raza=raza,
                edad_AA_MM_DD=edad_AA_MM_DD,
                usuario_id=current_user)

            db.execute(ingreso_Donante)
            db.commit()

        else:
            pass


    except Exception as e:
        logger.error(f"Error al Crear INGRESO DE DONANTE: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_hembras_donantes",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_hembras_donantes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaHembrasDonantes = db.query(modelo_hembras_donantes).filter(modelo_hembras_donantes.c.usuario_id == current_user).all()
        return ConsultaHembrasDonantes
    except Exception as e:
        logger.error(f'Error al obtener lista_hembras_donantes : {e}')
        raise
    finally:
        db.close()

@Transferencia_embriones.post("/crear_registro_extraccion", status_code=200, tags=["Embriones"])
async def crear_registro_extraccion(
    id_bovino: int = Form(...),
    fecha_extraccion: Optional[date] = Form(None),
    observaciones: Optional[str] = Form(None),
    responsable: Optional[str] = Form(None),

    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_animal=db.query(modelo_bovinos_inventario).\
            filter(modelo_bovinos_inventario.c.id_bovino==id_bovino).first()


        nombre_bovino=consulta_datos_animal.nombre_bovino

        ingreso_extraccion = modelo_extracciones_embriones.insert().values(
            id_bovino=id_bovino,
            nombre_bovino=nombre_bovino,
            fecha_extraccion=fecha_extraccion,
            observaciones=observaciones,
            responsable=responsable,
            usuario_id=current_user)

        db.execute(ingreso_extraccion)
        db.commit()


    except Exception as e:
        logger.error(f"Error al Crear INGRESO DE EXTRACCION: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_extracciones",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_extracciones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaExtracciones = db.query(modelo_extracciones_embriones).filter(modelo_extracciones_embriones.c.usuario_id == current_user).all()
        return ConsultaExtracciones
    except Exception as e:
        logger.error(f'Error al obtener lista_extracciones : {e}')
        raise
    finally:
        db.close()


@Transferencia_embriones.post("/crear_registro_embriones_propios", status_code=200, tags=["Embriones"])
async def crear_registro_embriones(
    codigo_identificador: Optional[str] = Form(None),
    id_extraccion: int = Form(...),
    metodo: Optional[str] = Form(None),
    padre_o_pajilla: Optional[str] = Form(None),
    id_padre_pajilla: Optional[int] = Form(None),
    calidad_embrion: Optional[str] = Form(None),
    estado_embrion: Optional[str] = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_extraccion=db.query(modelo_extracciones_embriones).\
            filter(modelo_extracciones_embriones.c.id_extraccion==id_extraccion).first()


        fecha_extraccion=consulta_datos_extraccion.fecha_extraccion
        nombre_donante=consulta_datos_extraccion.nombre_bovino
        id_donante=consulta_datos_extraccion.id_bovino

        extraccion= nombre_donante +", " +str(fecha_extraccion)

        if padre_o_pajilla=="Macho del Hato":
            consulta_datos_animal=db.query(modelo_bovinos_inventario).\
                filter(modelo_bovinos_inventario.c.id_bovino==id_padre_pajilla).first()

            nombre_padre_o_pajilla=consulta_datos_animal.nombre_bovino

            ingreso_embrion = modelo_embriones.insert().values(
                codigo_identificador=codigo_identificador,
                id_extraccion=id_extraccion,
                metodo=metodo,
                extraccion=extraccion,
                id_donante=id_donante,
                nombre_donante=nombre_donante,
                padre_o_pajilla=padre_o_pajilla,
                id_padre_pajilla=id_padre_pajilla,
                nombre_padre_o_pajilla=nombre_padre_o_pajilla,
                calidad_embrion=calidad_embrion,
                productor="Producido en el Hato",
                estado_embrion=estado_embrion,
                usuario_id=current_user)

            db.execute(ingreso_embrion)
            db.commit()

        elif padre_o_pajilla=="Pajilla adquirida":
            consulta_datos_pajilla=db.query(modelo_registro_pajillas).\
                filter(modelo_registro_pajillas.c.id_pajillas==id_padre_pajilla).first()

            Codigo_toro_pajilla=consulta_datos_pajilla.Codigo_toro_pajilla
            nombre_toro=consulta_datos_pajilla.nombre_toro
            nombre_padre_o_pajilla= f'Pajilla {Codigo_toro_pajilla} ({nombre_toro})'

            ingreso_embrion = modelo_embriones.insert().values(
                codigo_identificador=codigo_identificador,
                id_extraccion=id_extraccion,
                metodo=metodo,
                extraccion=extraccion,
                id_donante=id_donante,
                nombre_donante=nombre_donante,
                padre_o_pajilla=padre_o_pajilla,
                id_padre_pajilla=id_padre_pajilla,
                nombre_padre_o_pajilla=nombre_padre_o_pajilla,
                calidad_embrion=calidad_embrion,
                productor="Producido en el Hato",
                estado_embrion=estado_embrion,
                usuario_id=current_user)

            db.execute(ingreso_embrion)
            db.commit()
        else:
            pass
    except Exception as e:
        logger.error(f"Error al Crear EMBRION PRODUCIDO EN EL HATO: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_embriones_producidos_hato",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_embriones_producidos_hato(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaEmbrionesPropios = db.query(modelo_embriones).filter(modelo_embriones.c.productor=="Producido en el Hato",
                                                                   modelo_embriones.c.usuario_id == current_user).all()
        return ConsultaEmbrionesPropios
    except Exception as e:
        logger.error(f'Error al obtener lista_embriones_producidos_hato : {e}')
        raise
    finally:
        db.close()

@Transferencia_embriones.post("/crear_registro_embriones_comprados", status_code=200, tags=["Embriones"])
async def crear_registro_embriones_comprados(
    codigo_identificador: Optional[str] = Form(None),
    nombre_padre_o_pajilla: Optional[str] = Form(None),
    raza_padre: Optional[str] = Form(None),
    pedigree_padre: Optional[str] = Form(None),
    nombre_donante: Optional[str] = Form(None),
    raza_madre: Optional[str] = Form(None),
    pedigree_madre: Optional[str] = Form(None),
    calidad_embrion: Optional[str] = Form(None),
    estado_embrion: Optional[str] = Form(None),
	fecha_produccion_embrion: Optional[date] = Form(None),
    productor: str = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:

            ingreso_embrion = modelo_embriones.insert().values(
                codigo_identificador=codigo_identificador,
                nombre_padre_o_pajilla=nombre_padre_o_pajilla,
                raza_padre=raza_padre,
                pedigree_padre=pedigree_padre,
                nombre_donante=nombre_donante,
                raza_madre=raza_madre,
                pedigree_madre=pedigree_madre,
                calidad_embrion=pedigree_madre,
                estado_embrion=estado_embrion,
                fecha_produccion_embrion=fecha_produccion_embrion,
                productor=productor,
                usuario_id=current_user)

            db.execute(ingreso_embrion)
            db.commit()




    except Exception as e:
        logger.error(f"Error al Crear EMBRION COMPRADO: {e}")
        raise
    finally:
        db.close()

    return


@Transferencia_embriones.get("/listar_embriones_comprados",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_embriones_comprados(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaEmbrionesComprados = db.query(modelo_embriones).filter(modelo_embriones.c.productor!="Producido en el Hato",
                                                                   modelo_embriones.c.usuario_id == current_user).all()
        return ConsultaEmbrionesComprados
    except Exception as e:
        logger.error(f'Error al obtener lista_embriones_comprados : {e}')
        raise
    finally:
        db.close()


@Transferencia_embriones.post("/crear_transferencia_embrion", status_code=200, tags=["Embriones"])
async def crear_transferencia_embrion(
    id_embrion: int = Form(...),
    id_receptora: int = Form(...),
    fecha_transferencia: date = Form(...),
    resultado: str = Form(...),
    observaciones: Optional[str] = Form(None),
    id_parto: Optional[int] = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_animal=db.query(modelo_bovinos_inventario).\
                filter(modelo_bovinos_inventario.c.id_bovino==id_receptora).first()

        nombre_receptora=consulta_datos_animal.nombre_bovino

        consulta_datos_embrion=db.query(modelo_embriones).\
                filter(modelo_embriones.c.id_embrion==id_embrion).first()

        embrion=consulta_datos_embrion.codigo_identificador

        if id_parto is None:
            ingreso_transferencia = modelo_transferencias_embriones.insert().values(
                id_embrion=id_embrion,
                embrion=embrion,
                id_receptora=id_receptora,
                nombre_receptora=nombre_receptora,
                fecha_transferencia=fecha_transferencia,
                resultado=resultado,
                observaciones=observaciones,
                usuario_id=current_user)

            db.execute(ingreso_transferencia)
            db.commit()

        else:

            consulta_datos_parto=db.query(modelo_historial_partos).\
                filter(modelo_historial_partos.c.id_parto==id_parto).first()

            nombre_cria=consulta_datos_parto.nombre_hijo
            id_cria=consulta_datos_parto.id_bovino_hijo
            id_parto=consulta_datos_parto.id_parto

            ingreso_transferencia = modelo_transferencias_embriones.insert().values(
                id_embrion=id_embrion,
                embrion=embrion,
                id_receptora=id_receptora,
                nombre_receptora=nombre_receptora,
                fecha_transferencia=fecha_transferencia,
                resultado=resultado,
                nombre_cria=nombre_cria,
                id_cria=id_cria,
                id_parto=id_parto,
                observaciones=observaciones,
                usuario_id=current_user)

            db.execute(ingreso_transferencia)
            db.commit()

        session.execute(modelo_embriones.update().values(estado_embrion="Transferido"). \
                                 where(modelo_embriones.c.id_embrion == id_embrion))
        session.commit()




    except Exception as e:
        logger.error(f"Error al Crear TRANSFERENCIA EMBRION: {e}")
        raise
    finally:
        db.close()

    return


@Transferencia_embriones.get("/listar_transferencias",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_transferencias(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaTransferenciasEmbriones = db.query(modelo_transferencias_embriones).filter(modelo_transferencias_embriones.c.usuario_id == current_user).all()
        return ConsultaTransferenciasEmbriones
    except Exception as e:
        logger.error(f'Error al obtener lista_transferencias : {e}')
        raise
    finally:
        db.close()



@Transferencia_embriones.post("/crear_termo_criogenico", status_code=200, tags=["Embriones"])
async def crear_termo(
    nombre_termo_identificador: str = Form(...),
    ubicacion: str = Form(...),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        ingreso_termo = modelo_termocriogenico_embriones.insert().values(
                nombre_termo_identificador=nombre_termo_identificador,
                ubicacion=ubicacion,
                usuario_id=current_user)

        db.execute(ingreso_termo)
        db.commit()


    except Exception as e:
        logger.error(f"Error al Crear TERMO: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_termos_criogenicos",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_termos_criogenicos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaTermos_criogenicos = db.query(modelo_termocriogenico_embriones).filter(modelo_termocriogenico_embriones.c.usuario_id == current_user).all()
        return ConsultaTermos_criogenicos
    except Exception as e:
        logger.error(f'Error al obtener lista_termos_criogenicos : {e}')
        raise
    finally:
        db.close()



@Transferencia_embriones.post("/crear_canastillas_embriones", status_code=200, tags=["Embriones"])
async def canastillas_embriones(
    id_termo: int = Form(...),
    nombre_codigo_canastilla: str = Form(...),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_termo=db.query(modelo_termocriogenico_embriones).\
                filter(modelo_termocriogenico_embriones.c.id_termo==id_termo).first()

        nombre_termo_identificador=consulta_datos_termo.nombre_termo_identificador

        ingreso_canastilla = modelo_canastillas_embriones.insert().values(
                usuario_id=current_user,
                id_termo=id_termo,
                nombre_termo_identificador=nombre_termo_identificador,
                nombre_codigo_canastilla=nombre_codigo_canastilla)

        db.execute(ingreso_canastilla)
        db.commit()


    except Exception as e:
        logger.error(f"Error al Crear CANASTILLA EMBRIONES: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_canastillas_embriones",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_canastillas_embriones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaCanastillas = db.query(modelo_canastillas_embriones).filter(modelo_canastillas_embriones.c.usuario_id == current_user).all()
        return ConsultaCanastillas
    except Exception as e:
        logger.error(f'Error al obtener lista_canastillas_embriones : {e}')
        raise
    finally:
        db.close()

@Transferencia_embriones.post("/crear_gondola_embrion", status_code=200, tags=["Embriones"])
async def crear_gondola_embrion(
    id_termo: int = Form(...),
    id_canastilla_embrion: int = Form(...),
    nombre_posicion_gondola: str = Form(...),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_datos_termo=db.query(modelo_termocriogenico_embriones).\
                filter(modelo_termocriogenico_embriones.c.id_termo==id_termo).first()

        nombre_termo_identificador=consulta_datos_termo.nombre_termo_identificador

        consulta_datos_canastilla=db.query(modelo_canastillas_embriones).\
                filter(modelo_canastillas_embriones.c.id_canastilla_embrion==id_canastilla_embrion).first()

        nombre_codigo_canastilla=consulta_datos_canastilla.nombre_codigo_canastilla

        ingreso_gondola = modelo_gondolas_embriones.insert().values(
                id_termo=id_termo,
                id_canastilla_embrion=id_canastilla_embrion,
                nombre_termo_identificador=nombre_termo_identificador,
                nombre_codigo_canastilla=nombre_codigo_canastilla,
                nombre_posicion_gondola=nombre_posicion_gondola,
                usuario_id=current_user)

        db.execute(ingreso_gondola)
        db.commit()


    except Exception as e:
        logger.error(f"Error al Crear GONDOLA EMBRIONES: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_Gondolas",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_Gondolas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaGondolas = db.query(modelo_gondolas_embriones).filter(modelo_gondolas_embriones.c.usuario_id == current_user).all()
        return ConsultaGondolas
    except Exception as e:
        logger.error(f'Error al obtener lista_Gondolas : {e}')
        raise
    finally:
        db.close()

@Transferencia_embriones.post("/insertar_embrion_en_banco", status_code=200, tags=["Embriones"])
async def insertar_embrion_en_banco(
    id_embrion: int = Form(...),
    id_termo: int = Form(...),
    id_canastilla_embrion: int = Form(...),
    id_gondola: str = Form(...),
    fecha_ingreso: Optional[date] = Form(None),
    fecha_salida: Optional[date] = Form(None),
    observaciones: Optional[str] = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:
        consulta_existencia_embrion=db.query(modelo_banco_embriones).\
                filter(modelo_banco_embriones.c.id_embrion==id_embrion).first()


        if consulta_existencia_embrion is None or consulta_existencia_embrion==[]:

            consulta_datos_termo=db.query(modelo_termocriogenico_embriones).\
                    filter(modelo_termocriogenico_embriones.c.id_termo==id_termo).first()

            consulta_datos_canastilla=db.query(modelo_canastillas_embriones).\
                    filter(modelo_canastillas_embriones.c.id_canastilla_embrion==id_canastilla_embrion).first()

            consulta_datos_Gondola=db.query(modelo_gondolas_embriones).\
                    filter(modelo_gondolas_embriones.c.id_gondola==id_gondola).first()

            termo=consulta_datos_termo.nombre_termo_identificador
            nombre_codigo_canastilla=consulta_datos_canastilla.nombre_codigo_canastilla
            gondola_posicion=consulta_datos_Gondola.nombre_posicion_gondola

            consulta_datos_embrion=db.query(modelo_embriones).\
                    filter(modelo_embriones.c.id_embrion==id_embrion).first()

            nombre_codigo_embrion=consulta_datos_embrion.codigo_identificador

            ingreso_en_banco = modelo_banco_embriones.insert().values(
                id_embrion=id_embrion,
                nombre_codigo_embrion=nombre_codigo_embrion,
                id_termo=id_termo,
                id_canastilla_embrion=id_canastilla_embrion,
                id_gondola=id_gondola,
                observaciones=observaciones,
                usuario_id=current_user,
                termo=termo,
                nombre_codigo_canastilla=nombre_codigo_canastilla,
                gondola_posicion=gondola_posicion,
                fecha_ingreso=fecha_ingreso,
                fecha_salida=fecha_salida)

            db.execute(ingreso_en_banco)
            db.commit()

        else:
            pass

    except Exception as e:
        logger.error(f"Error al INSERTAR EMBRION EN BANCO: {e}")
        raise
    finally:
        db.close()

    return

@Transferencia_embriones.get("/listar_Banco_Embriones",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_Banco_Embriones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        ConsultaBanco = db.query(modelo_banco_embriones).filter(modelo_banco_embriones.c.usuario_id == current_user).all()
        return ConsultaBanco
    except Exception as e:
        logger.error(f'Error al obtener Banco_Embriones : {e}')
        raise
    finally:
        db.close()







@Transferencia_embriones.post("/crear_registro_embrion", status_code=200, tags=["Embriones"])
async def crear_registro_embrion(
    codigo_nombre_embrion: str = Form(...),
    raza: str = Form(...),
    inf_madre_biologica: str = Form(...),
    inf_padre_biologico: str = Form(...),
    estado: str = Form(...),
    fecha_implante: Optional[date] = Form(None),
    id_receptora: Optional[int] = Form(None),
    resultado_trasnplante: Optional[str] = Form(None),
    id_bovino_hijo: Optional[int] = Form(None),
    observaciones: Optional[str] = Form(None),

    # Nuevos campos
    raza_madre_biologica: Optional[str] = Form(None),
    genetica_madre_biologica: Optional[str] = Form(None),
    edad_madre_biologica: Optional[str] = Form(None),
    historial_madre_biologica: Optional[str] = Form(None),
    tratamientos_hormonales_madre_biologica: Optional[str] = Form(None),
    raza_padre_biologico: Optional[str] = Form(None),
    genetica_padre_biologico: Optional[str] = Form(None),
    edad_padre_biologico: Optional[str] = Form(None),
    historial_reproductivo_padre_biologico: Optional[str] = Form(None),
    fecha_extracion: Optional[date] = Form(None),
    calidad_embrion: Optional[str] = Form(None),
    metodo_recoleccion: Optional[str] = Form(None),
    codigo_unico: Optional[str] = Form(None),
    lote_procedencia: Optional[str] = Form(None),
    caracteristicas_geneticas: Optional[str] = Form(None),
    tanque_nitrogeno: Optional[str] = Form(None),
    pajilla: Optional[str] = Form(None),
    numero_canister: Optional[str] = Form(None),
    historial_completo: Optional[str] = Form(None),
    programacion_transferencia: Optional[str] = Form(None),
    tecnica_utilizada: Optional[str] = Form(None),

    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:


        # Insertar los datos en la base de datos
        ingresoRegistroEmbrion = modelo_embriones_transferencias.insert().values(
            codigo_nombre_embrion=codigo_nombre_embrion,
            raza=raza,
            inf_madre_biologica=inf_madre_biologica,
            inf_padre_biologico=inf_padre_biologico,
            estado=estado,
            fecha_implante=fecha_implante,
            id_receptora=id_receptora,
            resultado_trasnplante=resultado_trasnplante,
            id_bovino_hijo=id_bovino_hijo,
            observaciones=observaciones,
            usuario_id=current_user,

            # Nuevos campos
            raza_madre_biologica=raza_madre_biologica,
            genetica_madre_biologica=genetica_madre_biologica,
            edad_madre_biologica=edad_madre_biologica,
            historial_madre_biologica=historial_madre_biologica,
            tratamientos_hormonales_madre_biologica=tratamientos_hormonales_madre_biologica,
            raza_padre_biologico=raza_padre_biologico,
            genetica_padre_biologico=genetica_padre_biologico,
            edad_padre_biologico=edad_padre_biologico,
            historial_reproductivo_padre_biologico=historial_reproductivo_padre_biologico,
            fecha_extracion=fecha_extracion,
            calidad_embrion=calidad_embrion,
            metodo_recoleccion=metodo_recoleccion,
            codigo_unico=codigo_unico,
            lote_procedencia=lote_procedencia,
            caracteristicas_geneticas=caracteristicas_geneticas,
            tanque_nitrogeno=tanque_nitrogeno,
            pajilla=pajilla,
            numero_canister=numero_canister,
            historial_completo=historial_completo,
            programacion_transferencia=programacion_transferencia,
            tecnica_utilizada=tecnica_utilizada,
        )

        db.execute(ingresoRegistroEmbrion)
        db.commit()
        registro_embriones(session=db, current_user=current_user)

    except Exception as e:
        logger.error(f"Error al Crear INGRESO DE registro_embrion: {e}")
        raise
    finally:
        db.close()

    return
@Transferencia_embriones.put("/Editar_registro_embrion/{id_embrion}", status_code=200, tags=["Embriones"])
async def editar_registro_embrion(
    id_embrion: int,
    codigo_nombre_embrion: str = Form(...),
    raza: str = Form(...),
    inf_madre_biologica: str = Form(...),
    inf_padre_biologico: str = Form(...),
    estado: str = Form(...),
    fecha_implante: Optional[date] = Form(None),
    id_receptora: Optional[int] = Form(None),
    resultado_trasnplante: Optional[str] = Form(None),
    id_bovino_hijo: Optional[int] = Form(None),
    observaciones: Optional[str] = Form(None),

    # Nuevos campos
    raza_madre_biologica: Optional[str] = Form(None),
    genetica_madre_biologica: Optional[str] = Form(None),
    edad_madre_biologica: Optional[str] = Form(None),
    historial_madre_biologica: Optional[str] = Form(None),
    tratamientos_hormonales_madre_biologica: Optional[str] = Form(None),
    raza_padre_biologico: Optional[str] = Form(None),
    genetica_padre_biologico: Optional[str] = Form(None),
    edad_padre_biologico: Optional[str] = Form(None),
    historial_reproductivo_padre_biologico: Optional[str] = Form(None),
    fecha_extracion: Optional[date] = Form(None),
    calidad_embrion: Optional[str] = Form(None),
    metodo_recoleccion: Optional[str] = Form(None),
    codigo_unico: Optional[str] = Form(None),
    lote_procedencia: Optional[str] = Form(None),
    caracteristicas_geneticas: Optional[str] = Form(None),
    tanque_nitrogeno: Optional[str] = Form(None),
    pajilla: Optional[str] = Form(None),
    numero_canister: Optional[str] = Form(None),
    historial_completo: Optional[str] = Form(None),
    programacion_transferencia: Optional[str] = Form(None),
    tecnica_utilizada: Optional[str] = Form(None),

    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user),
):
    try:

        nombre_receptora = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_receptora, current_user=current_user)
        nombre_hijo = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_receptora,
                                                                 current_user=current_user)
        db.execute(
            modelo_embriones_transferencias.update().values(
                codigo_nombre_embrion=codigo_nombre_embrion,
                raza=raza,
                inf_madre_biologica=inf_madre_biologica,
                inf_padre_biologico=inf_padre_biologico,
                estado=estado,
                fecha_implante=fecha_implante,
                observaciones=observaciones,
                id_receptora=id_receptora,
                nombre_receptora = nombre_receptora,
                resultado_trasnplante=resultado_trasnplante,
                id_bovino_hijo=id_bovino_hijo,
                nombre_hijo = nombre_hijo,
                # Nuevos campos
                raza_madre_biologica=raza_madre_biologica,
                genetica_madre_biologica=genetica_madre_biologica,
                edad_madre_biologica=edad_madre_biologica,
                historial_madre_biologica=historial_madre_biologica,
                tratamientos_hormonales_madre_biologica=tratamientos_hormonales_madre_biologica,
                raza_padre_biologico=raza_padre_biologico,
                genetica_padre_biologico=genetica_padre_biologico,
                edad_padre_biologico=edad_padre_biologico,
                historial_reproductivo_padre_biologico=historial_reproductivo_padre_biologico,
                fecha_extracion=fecha_extracion,
                calidad_embrion=calidad_embrion,
                metodo_recoleccion=metodo_recoleccion,
                codigo_unico=codigo_unico,
                lote_procedencia=lote_procedencia,
                caracteristicas_geneticas=caracteristicas_geneticas,
                tanque_nitrogeno=tanque_nitrogeno,
                pajilla=pajilla,
                numero_canister=numero_canister,
                historial_completo=historial_completo,
                programacion_transferencia=programacion_transferencia,
                tecnica_utilizada=tecnica_utilizada
            ).where(modelo_embriones_transferencias.columns.id_embrion == id_embrion)
        )
        db.commit()
        #registro_embriones(session=db, current_user=current_user)





    except Exception as e:
        logger.error(f'Error al Editar_registro_embrion: {e}')
        raise
    finally:
        db.close()

    return



@Transferencia_embriones.get("/listar_tabla_embriones",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_tabla_embriones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        registro_embriones(session=db, current_user=current_user)
        ConsultaRegistroEmbriones = db.query(modelo_embriones_transferencias).filter(modelo_embriones_transferencias.c.usuario_id == current_user).all()
        return ConsultaRegistroEmbriones
    except Exception as e:
        logger.error(f'Error al obtener tabla_embriones_transferencias : {e}')
        raise
    finally:
        db.close()

@Transferencia_embriones.get("/listar_tabla_embriones/{id_embrion}",response_model=list[esquema_embriones_transferencias],tags=["Embriones"])
async def listar_embriones_registro(id_embrion: int ,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:



        ConsultaRegistroEmbriones = db.query(modelo_embriones_transferencias).filter(modelo_embriones_transferencias.c.usuario_id == current_user,modelo_embriones_transferencias.c.id_embrion == id_embrion).all()
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

