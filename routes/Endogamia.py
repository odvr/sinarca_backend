
'''
Librerias requeridas
@autor : odvr
'''

import logging

from fastapi import APIRouter, Response,status

from fastapi import APIRouter, Depends

from Lib.endogamia import endogamia, abuelo_materno, abuela_materna, abuelo_paterno, abuela_paterna, bisabuelo_materno, \
    bisabuelo_paterno,actualizacion_nombres_Arbol_genealogico
from Lib.perdida_Terneros import perdida_Terneros1
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_usuarios, modelo_bovinos_inventario, modelo_indicadores, \
    modelo_arbol_genealogico
from sqlalchemy.orm import Session

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico
from fastapi import Form
from typing import Optional
from typing import List

# Configuracion de las rutas para fash api
Endogamia = APIRouter()

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


@Endogamia.get("/listar_tabla_solo_machos",response_model=list[Esquema_bovinos],tags=["Endogamia"] )
async def listar_tabla_solo_machos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        machos = db.query(modelo_bovinos_inventario). \
            filter(
                   modelo_bovinos_inventario.c.sexo == "Macho",modelo_bovinos_inventario.c.usuario_id == current_user).all()
        return machos

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE SOLO MACHOS: {e}')
        raise
    finally:
        db.close()

@Endogamia.get("/listar_tabla_solo_hembras",response_model=list[Esquema_bovinos],tags=["Endogamia"] )
async def listar_tabla_solo_hembras(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        hembras = db.query(modelo_bovinos_inventario). \
            filter( modelo_bovinos_inventario.c.sexo == "Hembra",modelo_bovinos_inventario.c.usuario_id == current_user).all()
        #itemsAnimalesVeterinaria =  session.execute(modelo_veterinaria.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE SOLO Hembra: {e}')
        raise
    finally:
        db.close()
    return hembras



@Endogamia.get("/listar_tabla_endogamia",response_model=list[esquema_arbol_genealogico],tags=["Endogamia"] )
async def listar_tabla_endogamia(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        itemsAnimalesEndogamia = db.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.c.usuario_id == current_user).all()

        actualizacion_nombres_Arbol_genealogico(session=db, current_user=current_user)
        abuelo_materno(session=db, current_user=current_user)
        abuela_materna(session=db, current_user=current_user)
        abuelo_paterno(session=db, current_user=current_user)
        abuela_paterna(session=db, current_user=current_user)
        bisabuelo_materno(session=db, current_user=current_user)
        bisabuelo_paterno(session=db, current_user=current_user)
        endogamia(session=db, current_user=current_user)


    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return itemsAnimalesEndogamia

"""
Crear Indice de Endogamia
"""
@Endogamia.post("/calcular_indice_endogamia/{id_bovino}",status_code=200)
async def crear_endogamia(id_bovino:str,id_bovino_madre: Optional [int] = Form(None),id_bovino_padre:Optional [int] = Form(None),inseminacion:str= Form(...),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ingresoEndogamia = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                     id_bovino_madre=id_bovino_madre,
                                                     id_bovino_padre=id_bovino_padre,usuario_id=current_user,
                                                     inseminacion=inseminacion
                                                   )


        db.execute(ingresoEndogamia)
        db.commit()
        actualizacion_nombres_Arbol_genealogico(session=db, current_user=current_user)
        abuelo_materno(session=db, current_user=current_user)
        abuela_materna(session=db, current_user=current_user)
        abuelo_paterno(session=db, current_user=current_user)
        abuela_paterna(session=db, current_user=current_user)
        bisabuelo_materno(session=db, current_user=current_user)
        bisabuelo_paterno(session=db, current_user=current_user)
        endogamia(session=db, current_user=current_user)

    except Exception as e:
        logger.error(f'Error al Crear INDICE DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@Endogamia.delete("/eliminar_bovino_endogamia/{id_bovino}")
async def Eliminar_endogamia(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        db.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino == id_bovino))
        db.commit()
    except Exception as e:
        logger.error(f'Error al intentar Eliminar Registro de Arbol Genialogico: {e}')
        raise
    finally:
        db.close()

    return
