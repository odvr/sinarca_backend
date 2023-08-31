'''
Librerias requeridas
'''
import logging

from Lib.actualizacion_peso import actualizacion_peso
from Lib.funcion_peso_por_raza import peso_segun_raza
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_datos_pesaje, modelo_orden_peso
from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  status, HTTPException, Depends
from sqlalchemy import func
from datetime import date, datetime, timedelta
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_modelo_Reporte_Pesaje, esquema_orden_peso, Esquema_Usuario

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

pesaje = APIRouter()
"""
Ingresa los datos para el reporte de pesaje del animal 
"""
@pesaje.post("/fecha_pesaje/{id_bovino}/{fecha_pesaje}/{peso}",status_code=200)
async def crear_fecha_pesaje(id_bovino:str,fecha_pesaje:date,peso:float,current_user: Esquema_Usuario = Depends(get_current_user) ):

    try:


        ingresoFechaPesaje = modelo_datos_pesaje.insert().values(id_bovino=id_bovino,fecha_pesaje=fecha_pesaje,peso=peso)


        condb.execute(ingresoFechaPesaje)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE PESAJE: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)


@pesaje.delete("/Eliminar_Registro_Peso/{id_pesaje}", status_code=200)
async def Eliminar_Re(id_pesaje: str,current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        condb.execute(modelo_datos_pesaje.delete().where(modelo_datos_pesaje.c.id_pesaje == id_pesaje))
        condb.commit()

    except Exception as e:
        logger.error(f'Error al intentar Eliminar Registro de Arbol Genialogico: {e}')
        raise
    finally:
        session.close()

    return


@pesaje.get("/Promedio_Peso_Raza" , response_model=list[esquema_orden_peso])
async def inventario_prod_leche(current_user: Esquema_Usuario = Depends(get_current_user)):

    try:


        peso_segun_raza()

        itemsPromedioRaza = session.query(modelo_orden_peso).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Promedio Por Razas: {e}')
        raise
    finally:
        session.close()
    return itemsPromedioRaza



@pesaje.get("/listar_tabla_pesaje", response_model=list[esquema_modelo_Reporte_Pesaje] )
async def listar_tabla_pesaje(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        actualizacion_peso()
        tabla_pesaje = session.query(modelo_datos_pesaje).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA PESAJE: {e}')
        raise
    finally:
        session.close()
    return tabla_pesaje


@pesaje.get("/listar_reporte_pesaje/Enero")
async def listar_reporte_pesaje_enero(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosEnero = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                        func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 1) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosEnero:
            Enero = row[1]
            return Enero
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Enero {e}')
        raise
    finally:
        session.close()



@pesaje.get("/listar_reporte_pesaje/Febrero")
async def listar_reporte_pesaje_febrero(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosFebrero = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                        func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 2) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosFebrero:
            Febrero = row[1]
            return Febrero

    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Enero {e}')
        raise
    finally:
        session.close()
    
'''

'''
@pesaje.get("/listar_reporte_pesaje/Marzo" )
async def listar_reporte_pesaje_Marzo(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:



        resultadosMarzo = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 3) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosMarzo:
            Marzo = row[1]
            return Marzo


    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs MArzo {e}')
        raise
    finally:
        session.close()


@pesaje.get("/listar_reporte_pesaje/Abril" )
async def listar_reporte_pesaje_Abril(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosAbril = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 4) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosAbril:
            Abril = row[1]
            return Abril

    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Abril {e}')
        raise
    finally:
        session.close()

@pesaje.get("/listar_reporte_pesaje/Mayo" )
async def listar_reporte_pesaje_Mayo(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosMayo = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 5) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosMayo:
            Mayo = row[1]
            return Mayo

    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs MAyo {e}')
        raise
    finally:
        session.close()


@pesaje.get("/listar_reporte_pesaje/Junio" )
async def listar_reporte_pesaje_Junio(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosJunio = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 6) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosJunio:
            Junio = row[1]
            return Junio
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Junio {e}')
        raise
    finally:
        session.close()

@pesaje.get("/listar_reporte_pesaje/Julio" )
async def listar_reporte_pesaje_Julio(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosJulio = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 7) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosJulio:
            Julio = row[1]
            return Julio
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Julio {e}')
        raise
    finally:
        session.close()


@pesaje.get("/listar_reporte_pesaje/Agosto" )
async def listar_reporte_pesaje_Agosto(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosAgosto = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 8) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosAgosto:
            Agosto = row[1]
            return Agosto
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Agosto {e}')
        raise
    finally:
        session.close()


@pesaje.get("/listar_reporte_pesaje/Septiembre" )
async def listar_reporte_pesaje_Septiembre(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosSeptiembre = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 9) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosSeptiembre:
            Septiembre = row[1]
            return Septiembre

    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Septiembre {e}')
        raise
    finally:
        session.close()



@pesaje.get("/listar_reporte_pesaje/Octubre" )
async def listar_reporte_pesaje_Octubre(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosOctubre = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 10) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosOctubre:
            Octubre = row[1]
            return Octubre
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Octubre {e}')
        raise
    finally:
        session.close()

@pesaje.get("/listar_reporte_pesaje/Noviembre" )
async def listar_reporte_pesaje_Noviembre(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosNoviembre = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 11) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()

        for row in resultadosNoviembre:
            Noviembre = row[1]
            return Noviembre
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Noviembre {e}')
        raise
    finally:
        session.close()

@pesaje.get("/listar_reporte_pesaje/Diciembre" )
async def listar_reporte_pesaje_Diciembre(current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        resultadosDiciembre = session.query(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje),
                                   func.sum(modelo_datos_pesaje.c.peso).label('Peso')) \
            .filter(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje) == 12) \
            .group_by(func.MONTH(modelo_datos_pesaje.c.fecha_pesaje)) \
            .all()
        for row in resultadosDiciembre:
            Diciembre = row[1]
            return Diciembre
    except Exception as e:
        logger.error(f'Error al obtener inventario de De Promedios Por MEs Diciembre {e}')
        raise
    finally:
        session.close()





@pesaje.get("/listar_tabla_pesaje_por_animal/{id_bovino}",response_model=list[esquema_modelo_Reporte_Pesaje] )
async def listar_tabla_pesaje_Por_Animal(id_bovino:str,current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        tabla_pesaje = session.query(modelo_datos_pesaje).where(modelo_datos_pesaje.columns.id_bovino == id_bovino).all()


    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA PESAJE POR ANIMAL: {e}')
        raise
    finally:
        session.close()
    return tabla_pesaje