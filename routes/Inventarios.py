

'''
Librerias requeridas
@autor : odvr
'''

import logging



from fastapi import APIRouter, Depends,Form
import json
from Lib.Lib_Calcular_Edad_Bovinos import calculoEdad
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.actualizacion_peso import actualizacion_peso
from Lib.vida_util_macho_reproductor_bovino import vida_util_macho_reproductor
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_usuarios, modelo_bovinos_inventario, modelo_indicadores, \
    modelo_arbol_genealogico, modelo_ceba, modelo_levante, modelo_datos_pesaje, modelo_macho_reproductor
from sqlalchemy.orm import Session

from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico, \
    esquema_produccion_ceba, esquema_produccion_levante, esquema_modelo_Reporte_Pesaje

# Configuracion de las rutas para fash api
Inventarios = APIRouter()

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


@Inventarios.get("/listar_inventarios", response_model=list[Esquema_bovinos],tags=["Inventarios"]
                   )
async def inventario_bovino(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    # Se llama la funcion con el fin que esta realice el calculo pertinete a la edad del animal ingresado
    calculoEdad(db=db)
    actualizacion_peso(session=db)
    eliminarduplicados(db=db)
    vida_util_macho_reproductor(db=db,current_user=current_user)
    try:
        items = db.query(modelo_bovinos_inventario).filter(modelo_bovinos_inventario.c.usuario_id == current_user ).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de bovinos: {e}')
        raise
    finally:
        db.close()

    return items



@Inventarios.get("/Buscar_Historial_Bovino/{id_bovino}", response_model=list, tags=["Inventarios"])
async def Buscar_Historial_Bovino(id_bovino: int , db: Session = Depends(get_database_session), current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


        consultaCeba = db.query(modelo_ceba).filter(modelo_ceba.columns.id_bovino == id_bovino,
                                                    modelo_ceba.c.usuario_id == current_user).first()

        consultaMachoReproductor = db.query(modelo_macho_reproductor).filter(modelo_macho_reproductor.columns.id_bovino == id_bovino,
                                                    modelo_macho_reproductor.c.usuario_id == current_user).first()


        consultaLevante = db.query(modelo_levante).filter(modelo_levante.columns.id_bovino == id_bovino,
                                                          modelo_levante.c.usuario_id == current_user).first()

        tabla_pesaje = db.query(modelo_datos_pesaje).filter(modelo_datos_pesaje.columns.id_bovino == id_bovino,
                                                          modelo_datos_pesaje.c.usuario_id == current_user).all()
        ConsultaEndogamia = db.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,
                                                                      modelo_arbol_genealogico.columns.id_bovino_madre == id_bovino,
                                                                      modelo_arbol_genealogico.columns.id_bovino_padre == id_bovino,
                                                                      modelo_arbol_genealogico.columns.abuelo_paterno == id_bovino,
                                                                      modelo_arbol_genealogico.columns.abuela_paterna == id_bovino,
                                                                      modelo_arbol_genealogico.columns.abuelo_materno == id_bovino,
                                                                      modelo_arbol_genealogico.columns.abuela_materna == id_bovino,
                                                                      modelo_arbol_genealogico.columns.bisabuelo_materno == id_bovino,
                                                                      modelo_arbol_genealogico.columns.bisabuelo_paterno == id_bovino,

                                                                      modelo_arbol_genealogico.c.usuario_id == current_user).first()



        try:
            Historial = []

            if consultaMachoReproductor is not None:
                Historial.append({

                    "fecha_vida_util": consultaMachoReproductor.fecha_vida_util
                })

            if consultaCeba is not None:
                Historial.append({
                    "peso": consultaCeba.peso,
                    "estado_optimo_ceba": consultaCeba.estado_optimo_ceba,
                    "ganancia_media_diaria": consultaCeba.ganancia_media_diaria
                })

            if consultaLevante is not None:
                Historial.append({
                    "peso": consultaLevante.peso,
                    "estado_optimo_levante": consultaLevante.estado_optimo_levante,
                    "ganancia_media_diaria": consultaLevante.ganancia_media_diaria
                })

            if tabla_pesaje is not None:
                for pesaje in tabla_pesaje:
                    historial_item = {
                        "ListadoPeso": pesaje.peso,
                        "fecha_pesaje": pesaje.fecha_pesaje,
                        "tipo_pesaje": pesaje.tipo_pesaje,

                    }
                    Historial.append(historial_item)



            if ConsultaEndogamia is not None:
                Historial.append({
                    "nombre_bovino_madre": ConsultaEndogamia.nombre_bovino_madre,
                    "nombre_bovino_padre": ConsultaEndogamia.nombre_bovino_padre,
                    "nombre_bovino_abuelo_paterno": ConsultaEndogamia.nombre_bovino_abuelo_paterno,
                    "nombre_bovino_abuela_paterna": ConsultaEndogamia.nombre_bovino_abuela_paterna,
                    "nombre_bovino_abuelo_materno": ConsultaEndogamia.nombre_bovino_abuelo_materno,
                    "nombre_bovino_abuela_materna": ConsultaEndogamia.nombre_bovino_abuela_materna,
                    "nombre_bovino_bisabuelo_materno": ConsultaEndogamia.nombre_bovino_bisabuelo_materno,
                    "nombre_bovino_bisabuelo_paterno": ConsultaEndogamia.nombre_bovino_bisabuelo_paterno,
                    "tipo_de_apareamiento": ConsultaEndogamia.tipo_de_apareamiento,
                    "consanguinidad": ConsultaEndogamia.consanguinidad,
                    "notificacion": ConsultaEndogamia.notificacion,

                })




            return Historial



        except Exception as ErroresHistorial:
            logger.error(f'Error Historial Bovino {ErroresHistorial}')
            raise





    except Exception as e:
        logger.error(f'Error al obtener Historial el Bovino: {e}')
        raise
    finally:
        db.close()

