'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response
from pydantic.types import Decimal

# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_levante, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos,modelo_descarte
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_leche, esquema_produccion_levante,esquema_descarte, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func, null
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta


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


"""
La siguiente funcion retorna un diccionario con la consulta general del la tabla bovinos,
 utlizando el decorador execute
"""


@rutas_bovinos.get("/listar_inventarios", response_model=list[Esquema_bovinos], tags=["listar_inventarios"]
                   )
async def inventario_bovino():
    # Se llama la funcion con el fin que esta realice el calculo pertinete a la edad del animal ingresado
    calculoEdad()
    eliminarduplicados()
    EliminarDuplicadosLeche()
    vida_util_macho_reproductor()


    try:
        items = condb.execute(modelo_bovinos_inventario.select()).fetchall()
        logger.info(f'Se obtuvieron {len(items)} registros de inventario de bovinos.')

    except Exception as e:
        logger.error(f'Error al obtener inventario de bovinos: {e}')
        raise
    finally:
        condb.close()

    return items

@rutas_bovinos.get("/listar_bovino_v/{id_bovino}", response_model=Esquema_bovinos)
async def id_inventario_bovino_v(id_bovino: str):
    try:

        consulta = condb.execute(
            modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

        if not consulta:
            raise HTTPException(status_code=404, detail=f"El bovino con el ID {id_bovino} no existe en el inventario.")

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    # condb.commit()
    return consulta



@rutas_bovinos.get("/listar_prod_leche" )
async def inventario_prod_leche():
    # llamado de funciones
    Edad_Primer_Parto()
    Duracion_Lactancia()
    Edad_Sacrificio_Lecheras()
    Dias_Abiertos()
    animales_no_ordeno()
    eliminarduplicados()
    EliminarDuplicadosLeche()

    try:

        itemsLeche = session.execute(modelo_leche.select()).all()
        logger.info(f'Se obtuvieron {len(itemsLeche)} registros de inventario de Produccion Leche.')
    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        session.close()
    return itemsLeche





@rutas_bovinos.get("/listar_animales_descarte" )
async def listarAnimalesDescarte():

    try:

        itemsAnimalesDescarte = session.execute(modelo_descarte.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesDescarte

@rutas_bovinos.get("/listar_contar_animales_descarte" )
async def listar_contar_AnimalesDescarte():

    try:

        #itemsAnimalesDescarte = session.execute(modelo_descarte).count()
        itemsAnimalesDescarte = session.query(modelo_descarte). \
            where(modelo_descarte.columns.id_bovino).count()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesDescarte

"""
Listar animales con vientre apto
"""
@rutas_bovinos.get("/listar_contar_listar_vientres_aptos" )
async def listar_contar_AnimalesDescarte():

    try:
        itemsAnimalesVientresAptos = session.query(modelo_vientres_aptos). \
            where(modelo_vientres_aptos.columns.id_vientre).count()

    except Exception as e:
        logger.error(f'Error al obtener CONTAR VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesVientresAptos





"""
Lista los animales en Levante

"""

@rutas_bovinos.get("/listar_prod_levante",response_model=list[esquema_produccion_levante] )
async def inventario_levante():
    Estado_Optimo_Levante()
    eliminarduplicados()
    EliminarDuplicadosLeche()

    try:
        itemsLevante = session.execute(modelo_levante.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        session.close()
    return itemsLevante



'''Listar animales en Ceba'''


@rutas_bovinos.get("/listar_prod_ceba" )
async def inventario_ceba():
    #llamdo de la funcion para calcular
    Estado_Optimo_Ceba()
    eliminarduplicados()
    EliminarDuplicadosLeche()


    try:

        itemsceba = session.execute(modelo_ceba.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        session.close()
    return itemsceba




@rutas_bovinos.get("/listar_reproductor" )
async def listar_reproductor():
    #llamdo de la funcion para calcular
    vida_util_macho_reproductor()

    try:
        vida_util_macho_reproductor()
        itemsreproductor = session.execute(modelo_macho_reproductor.select()).all()
        logger.info(f'Se obtuvieron {len(itemsreproductor)} registros de inventario de REPRODUCTOR.')
    except Exception as e:
        logger.error(f'Error al obtener inventario de REPRODUCTOR: {e}')
        raise
    finally:
        session.close()
    return itemsreproductor


"""
Lista la tabla de carga de animales
"""

@rutas_bovinos.get("/listar_carga_animales" )
async def listar_carga_animales():

    try:
        consumo_global_agua_y_totalidad_unidades_animales()
        carga_animal()
        itemscargaAnimales = session.execute(modelo_carga_animal_y_consumo_agua.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CARGA ANIMALES: {e}')
        raise
    finally:
        session.close()
    return itemscargaAnimales


"""
Listar  Fecha aproximada de parto
"""

@rutas_bovinos.get("/listar_fecha_parto" )
async def listar_fecha_parto():

    try:
        fecha_aproximada_parto()

        listar_fecha_estimada_parto = session.execute(modelo_partos.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de LISTAR CARGA ANIMALES: {e}')
        raise
    finally:
        session.close()
    return listar_fecha_estimada_parto


"""
Listado de vientres aptos
"""
@rutas_bovinos.get("/listar_vientres_aptos" )
async def listar_vientres_aptos():
    try:
        vida_util_macho_reproductor()
        vientres_aptoss = session.query(modelo_indicadores.c.vientres_aptos).first()


    except Exception as e:
        logger.error(f'Error al obtener inventario de REPRODUCTOR: {e}')
        raise
    finally:
        session.close()
    return vientres_aptoss


"""
Listado de vientres aptos Para el modulo de Vientres Aptos
"""
@rutas_bovinos.get("/listar_vientres_aptos_modulos" )
async def listar_vientres_aptos_modulo():
    try:
        vientres_aptos()
        Eliminacion_total_vientres_aptos()
        tabla_vientres_aptos = session.query(modelo_vientres_aptos).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return tabla_vientres_aptos





"""
Listado de total_unidades_animales
"""
@rutas_bovinos.get("/total_unidades_animales" )
async def total_unidades_animales():
    try:
        total_unidades_animales = session.query(modelo_indicadores.c.total_unidades_animales).first()
    except Exception as e:
        logger.error(f'Error al obtener inventario de total_unidades_animales: {e}')
        raise
    finally:
        session.close()
    return total_unidades_animales



"""
Listado de calculadora_hectareas
"""
@rutas_bovinos.get("/consumo_global_agua" )
async def consumo_global_agua():
    try:


        consumo_global_agua = session.query(modelo_indicadores.c.consumo_global_agua).first()


    except Exception as e:
        logger.error(f'Error al obtener inventario de total_unidades_animales: {e}')
        raise
    finally:
        session.close()
    return consumo_global_agua



" relacion_toros_vientres_aptos Lista la relacion entre el toro y los vientres aptos"

@rutas_bovinos.get("/relacion_toros_vientres_aptos" )
async def relacion_toros_vientres_aptos():
    try:
        vida_util_macho_reproductor()
        toro_Vientres = session.query(modelo_indicadores.c.relacion_toros_vientres_aptos).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de RELACION Y VIENTRES APTOS=  {e}')
        raise
    finally:
        session.close()
    return toro_Vientres

"""



"""

@rutas_bovinos.get("/interpretacion_relacion_toros_vientres_aptos" )
async def interpretacion_relacion_toros_vientres_aptos():
    try:


        interpretacion_relacion_toros_vientres_aptos = session.query(modelo_indicadores.c.interpretacion_relacion_toros_vientres_aptos).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de interpretacion_relacion_toros_vientres_aptos=  {e}')
        raise
    finally:
        session.close()
    return interpretacion_relacion_toros_vientres_aptos


"""

Lista   hectareas_forrajeget

"""


@rutas_bovinos.get("/hectareas_forraje")
async def hectareas_forraje():
    try:

        hectareas_forraje_ = session.query(
            modelo_capacidad_carga.c.hectareas_forraje).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de hectareas_forraje=  {e}')
        raise
    finally:
        session.close()
    return hectareas_forraje_


"""

Lista   hectareas_forrajeget

"""


@rutas_bovinos.get("/capacidad_animales")
async def capacidad_animales():
    try:

        capacidad_animales = session.query(
            modelo_capacidad_carga.c.capacidad_animales).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de capacidad_animales=  {e}')
        raise
    finally:
        session.close()
    return capacidad_animales




"""
Listar la temperatura
"""

@rutas_bovinos.get("/listarTemperatura" )
async def listarTemperatura():
    try:
        listarTempAmbiente = session.query(modelo_indicadores.c.temperatura_ambiente).where(modelo_indicadores.c.id_indicadores == 1).first()
        #listarTempAmbiente = session.execute(modelo_indicadores.c.temperatura_ambiente).first()




    except Exception as e:

        logger.error(f'Error al obtener la consulta de TEMPERATURA=  {e}')
        raise
    finally:
        session.close()
    return listarTempAmbiente





"""
Lista los datos de la tabla prod levante para la opcion de editar bovino
"""

@rutas_bovinos.get("/listar_bovino_proceba/{id_bovino}")
async def id_inventario_bovino_ceba(id_bovino: str):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        consulta = session.execute(
            modelo_ceba.select().where(modelo_ceba.columns.id_bovino == id_bovino)).first()
        logger.info(f'Se listo el siguiente Bovino de Ceba {consulta} ')
    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Ceba: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta





"""
Lista los datos de la tabla prod leche inventario
"""

@rutas_bovinos.get("/listar_bovino_prodLeche/{id_bovino}")
async def id_inventario_bovino_leche(id_bovino: str):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        consulta = session.execute(
            modelo_leche.select().where(modelo_leche.columns.id_bovino == id_bovino)).first()
        logger.info(f'Se listo el siguiente Bovino {consulta} ')
    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Leche: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta





"""
Lista los datos de la tabla prod levante para la opcion de editar bovino
"""

@rutas_bovinos.get("/listar_bovino_prolevante/{id_bovino}")
async def id_inventario_bovino_levante(id_bovino: str):
    try:
        consulta = session.execute(
            modelo_levante.select().where(modelo_levante.columns.id_bovino == id_bovino)).first()
        logger.info(f'Se listo el siguiente Bovino de levante {consulta} ')
    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Leche: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta




"""
La siguiente funcion retorna un diccionario con la consulta de un ID del la tabla bovinos,
"""


@rutas_bovinos.get("/listar_bovino/{id_bovino}", response_model=Esquema_bovinos )
async def id_inventario_bovino(id_bovino: str):
    try:
        consulta = condb.execute(
            modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()



    except Exception as e:

        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    # condb.commit()
    return consulta


"""
Realiza la creacion de nuevos bovinos en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""


@rutas_bovinos.post("/crear_bovino", status_code=HTTP_204_NO_CONTENT)
async def crear_bovinos(esquemaBovinos: Esquema_bovinos):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        bovinos_dic = esquemaBovinos.dict()
        ingreso = modelo_bovinos_inventario.insert().values(bovinos_dic)
        condb.execute(ingreso)
        logger.info(f'Se creo el siguiente Bovino  {ingreso} ')
        condb.commit()
    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de inventarios: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""


@rutas_bovinos.post(
    "/crear_prod_leche/{fecha_primer_parto}/{id_bovino}/{fecha_inicial_ordeno}/{fecha_fin_ordeno}/{fecha_ultimo_parto}/{fecha_ultima_prenez}/{num_partos}/{tipo_parto}/{datos_prenez}/{ordeno}/{proposito}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdLeche(fecha_primer_parto: date, id_bovino: str, fecha_inicial_ordeno: date, fecha_fin_ordeno: date,
                   fecha_ultimo_parto: date, fecha_ultima_prenez: date, num_partos: int, tipo_parto: str,
                   datos_prenez: str, ordeno: str,proposito:str):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        ingresopleche = modelo_leche.insert().values(fecha_primer_parto=fecha_primer_parto, id_bovino=id_bovino,
                                                     fecha_inicial_ordeno=fecha_inicial_ordeno,
                                                     fecha_fin_ordeno=fecha_fin_ordeno,
                                                     fecha_ultimo_parto=fecha_ultimo_parto,
                                                     fecha_ultima_prenez=fecha_ultima_prenez, num_partos=num_partos,
                                                     tipo_parto=tipo_parto, datos_prenez=datos_prenez, ordeno=ordeno,proposito=proposito)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de leche {ingresopleche} ')

        condb.execute(ingresopleche)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Leche: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)






"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""

"""
Funcion crear Levante
"""
@rutas_bovinos.post(
    "/crear_prod_levante/{id_bovino}/{proposito}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdLevante(id_bovino: str,proposito:str):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        ingresoplevante = modelo_levante.insert().values(id_bovino=id_bovino, proposito = proposito)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de leche {ingresoplevante} ')

        condb.execute(ingresoplevante)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Levante: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)






"""
Funcion Caga Animal
"""
@rutas_bovinos.post(
    "/crear_carga_animal/{id_bovino}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearCargaAnimal(id_bovino: str):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(id_bovino=id_bovino)


        condb.execute(ingresoCargaAnimal)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla CARGA ANIMAL: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Crear en la tabla de partos para calcular la fecha aproximada
"""
@rutas_bovinos.post(
    "/crear_fecha_apoximada_parto/{id_bovino}/{fecha_estimada_prenez}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearFechaAproximadaParto(id_bovino: str,fecha_estimada_prenez:date):
    try:
        fecha_aproximada_parto()
        listar_fecha_parto()
        ingresocalcularFechaParto= modelo_partos.insert().values(id_bovino=id_bovino,fecha_estimada_prenez=fecha_estimada_prenez)
        condb.execute(ingresocalcularFechaParto)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear ingresocalcularFechaParto: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)





"""
Funcion crear La temperatura
"""
@rutas_bovinos.post(
    "/crear_temperatura/{temperatura_ambiente}",
    status_code=HTTP_204_NO_CONTENT)
async def crear_temperatura(temperatura_ambiente: float):
    eliminarduplicados()
    EliminarDuplicadosLeche()
    try:
        #temperatura_ambiente_indicadores = modelo_indicadores.insert().values(temperatura_ambiente=temperatura_ambiente).where(modelo_indicadores.c.id_indicadores == 1)

        temperatura_ambiente_indicadores = update(modelo_indicadores).where(modelo_indicadores.c.id_indicadores == 1).values(temperatura_ambiente=temperatura_ambiente)
        condb.execute(temperatura_ambiente_indicadores)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de TEMPERATURA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)






"""
Funcion inserta las hectareas aproximadas para realizar el calculo para el modulo de capacidad de carga  hectareas_forraje
"""
@rutas_bovinos.post(
    "/crear_hectareas_forraje/{hectareas_forraje}",
    status_code=HTTP_204_NO_CONTENT)
async def hectareas_forraje(hectareas_forraje: float):

    try:

        capacidad_carga()
        hectareas_forraje = update(modelo_capacidad_carga).where(modelo_capacidad_carga.c.id_capacidad == 1).values(hectareas_forraje=hectareas_forraje)
        condb.execute(hectareas_forraje)
        condb.commit()
        capacidad_carga()
    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de CAPACIDAD DE CARGA hectareas_forraje : {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)



"""
Crear Ceba
"""
@rutas_bovinos.post(
    "/crear_prod_ceba/{id_bovino}/{proposito}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdCeba(id_bovino: str,proposito:str):

    try:
        ingresopceba = modelo_ceba.insert().values(id_bovino=id_bovino,proposito=proposito)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de leche {ingresopceba} ')

        condb.execute(ingresopceba)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Ceba: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Crear Descarte
"""
@rutas_bovinos.post(
    "/crear_descarte/{id_bovino}/{edad}/{peso}/{razon_descarte}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearDescarte(id_bovino: str,edad:int,peso:float,razon_descarte:str):

    try:
        ingresodescarte = modelo_descarte.insert().values(id_bovino=id_bovino,edad=edad,peso=peso,razon_descarte=razon_descarte)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de DESCARTE {ingresodescarte} ')

        condb.execute(ingresodescarte)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de DESCARTE: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Crear Macho Reproductor
"""
@rutas_bovinos.post(
    "/crear_reproductor/{id_bovino}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearReproductor(id_bovino: str):
    try:
        CrearMacho = modelo_macho_reproductor.insert().values(id_bovino=id_bovino)
        logger.info(f'Se creo el siguiente Bovino en la tabla MACHO REPRODUCTOR {CrearMacho} ')

        condb.execute(CrearMacho)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de MACHO REPRODUCTOR: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)




'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def cambiar_esta_bovino(data_update: Esquema_bovinos, id_bovino: str):
    try:
        condb.execute(modelo_bovinos_inventario.update().values(
            fecha_nacimiento=data_update.fecha_nacimiento, sexo=data_update.sexo, raza=data_update.raza,
            peso=data_update.peso, marca=data_update.marca, proposito=data_update.proposito,
            mansedumbre=data_update.mansedumbre, estado=data_update.estado).where(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        condb.execute(modelo_levante.update().values(proposito=data_update.proposito).where(
            modelo_levante.columns.id_bovino == id_bovino))
        condb.execute(modelo_ceba.update().values(proposito=data_update.proposito).where(
            modelo_ceba.columns.id_bovino == id_bovino))
        condb.execute(modelo_leche.update().values(proposito=data_update.proposito).where(
            modelo_levante.columns.id_bovino == id_bovino))
        condb.commit()

            # Retorna una consulta con el id actualizado
            #resultado_actualizado = condb.execute(
            #modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise

    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)







'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def cambiar_esta_bovino(data_update: Esquema_bovinos, id_bovino: str):
    try:
        condb.execute(modelo_bovinos_inventario.update().values(
            fecha_nacimiento=data_update.fecha_nacimiento, sexo=data_update.sexo, raza=data_update.raza,
            peso=data_update.peso, marca=data_update.marca, proposito=data_update.proposito,
            mansedumbre=data_update.mansedumbre, estado=data_update.estado).where(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        condb.commit()

            # Retorna una consulta con el id actualizado
            #resultado_actualizado = condb.execute(
            #modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise

    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""


@rutas_bovinos.delete("/eliminar_bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino(id_bovino: str):

    try:
        condb.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bovino))
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino: {e}')
        raise
    finally:
        condb.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)




'''
Eliminar duplicados
'''
def eliminarduplicados():
    #consulta_ceba = condb.execute(modelo_bovinos_inventario.select().
                        #where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    itemsCeba = session.execute(modelo_ceba.select()).all()


    for i in itemsCeba:
        proposito = i[5]
        id = i[0]
        if proposito == 'Leche':
            condb.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            condb.commit()
        if proposito == 'Levante':
            condb.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            condb.commit()
    itemsLevante = session.execute(modelo_levante.select()).all()
    for i in itemsLevante:
        proposito = i[5]
        idle = i[0]
        if proposito == 'Leche':
            condb.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            condb.commit()
        if proposito == 'Ceba':
            condb.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            condb.commit()
def EliminarDuplicadosLeche():
    itemsLeche = session.execute(modelo_leche.select()).all()
    for ileche in itemsLeche:
        propositoleche = ileche[16]
        idleche = ileche[0]
        print(propositoleche, idleche)
        if propositoleche == 'Levante':
            eliminarlevanteleche = condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))
            logger.info(f'Se ELIMINA EL DATO REPETIDO DE LECHE LEVANTE =  {eliminarlevanteleche} ')
            condb.commit(eliminarlevanteleche)
        if propositoleche == 'Ceba':
            eliminarcebaleche = condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))
            logger.info(f'Se ELIMINA EL DATO REPETIDO DE LECHE CEBA =  {eliminarcebaleche} ')
            condb.commit(eliminarcebaleche)










"""esta funcion determina la cantidad de vacas vacias (no prenadas)
esto con el  fin de mostrar cuantos vientres NO estan produciendo en el hato"""


@rutas_bovinos.get("/Calcular_vacas_vacias")
async def vacas_vacias():
    try:
        # join de tabla bovinos y tabla leche mediante id_bovino \
        # filtrado y conteo animales con datos prenez Vacia que se encuentren vivos
        consulta_vacias = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
            filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Vacia').count()
        # actualizacion del campo
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(vacas_vacias=consulta_vacias))
        logger.info(f'Funcion Consultar Vacas Vacias  {consulta_vacias} ')
        session.commit()

    except Exception as e:
        logger.error(f'Error al Calcular Vacas Vacias: {e}')
        raise
    finally:
        session.close()

    return consulta_vacias

"""
La siguiente funcion consulta la fecha de nacimiento del bovino mediante su id y
calcula la edad del animal (en meses) utilizando la fecha actual
"""

def calculoEdad():
 try:
    # Realiza la consulta general de la tabla de bovinos
    consulta_fecha_nacimiento = condb.execute(modelo_bovinos_inventario.select().
                                       where(modelo_bovinos_inventario.columns.estado=="Vivo")).fetchall()
    #Recorre los campos de la consulta
    for i in consulta_fecha_nacimiento:
        #Toma el ID del bovino para calcular la edad el campo numero 0
        id = i[0]
        # Toma la fecha de nacimiento del animal en este caso es el campo 2
        fecha_nacimiento = i[1]
        # realiza el calculo correspondiente para calcular entre meses
        Edad_Animal = (datetime.today().year - fecha_nacimiento.year) * 12 + datetime.today().month - fecha_nacimiento.month
        # actualizacion del campo en la base de datos tomando la variable ID
        condb.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
            modelo_bovinos_inventario.columns.id_bovino == id ))
        logger.info(f'Funcion calculo Edad  {Edad_Animal} ')
        condb.commit()
 except Exception as e:
     logger.error(f'Error Funcion calculo Edad: {e}')
     raise
 finally:
    condb.close()



"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""


def Edad_Primer_Parto():
  try:
    # join de las tablas de leche y bovinos con los campos requeridos
    consulta_global = session.query(modelo_bovinos_inventario.c.id_bovino,
                      modelo_bovinos_inventario.c.fecha_nacimiento, modelo_leche.c.fecha_primer_parto). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).all()
    # Recorre los campos de la consulta
    for i in consulta_global:
        # Toma el ID del bovino para calcular la la edad del primer parto de cada animal
        id = i[0]
        # Toma la fecha de nacimiento del animal en este caso es el campo 1
        fecha_nacimiento = i[1]
        # Toma la fecha de primer parto del animal en este caso es el campo 2
        fecha_primer_parto = i[2]
        # calculo de la edad al primer parto
        Edad_primer_parto = (fecha_primer_parto.year - fecha_nacimiento.year) * 12 +\
                        fecha_primer_parto.month - fecha_nacimiento.month
    # actualizacion del campo
        condb.execute(modelo_leche.update().values(edad_primer_parto=Edad_primer_parto).where(
          modelo_leche.columns.id_bovino == id))
        logger.info(f'Funcion Edad_Primer_Parto {Edad_primer_parto} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Edad_Primer_Parto: {e}')
    raise
  finally:
      condb.close()

"""
"para la funcion de Duracion de lactancia se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en dias entre la fecha del ultimo ordeno
y la fecha del primer ordeno y devuelve la cantidad de dias en que se ordeno 
la vaca
"""



def Duracion_Lactancia():
  try:
    #consulta de fecha de incio de ordeno y fecha final de ordeno
    consulta_fechas = condb.execute(modelo_leche.select()).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_fechas:
        # Toma el ID del bovino para calcular la duracion de lactancia de cada animal
        id = i[1]
        # Toma la fecha de inicio de ordeno del animal en este caso es el campo 6
        fecha_inicial_ordeno = i[6]
        # Toma la fecha final de ordeno del animal en este caso es el campo 7
        fecha_fin_ordeno = i[7]
    # calculo de la duracion de la lactancia
        Duracion_Lac = (fecha_fin_ordeno.year - fecha_inicial_ordeno.year) * 360 + \
                   (fecha_fin_ordeno.month - fecha_inicial_ordeno.month) * 30
    # actualizacion del campo
        condb.execute(modelo_leche.update().values(dura_lactancia=Duracion_Lac).where(
          modelo_leche.columns.id_bovino == id))
        logger.info(f'Funcion Duracion_Lactancia {Duracion_Lac} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Duracion_Lactancia: {e}')
    raise
  finally:
      condb.close()
        #return Duracion_Lac
"""
esta funcion recibe como parametro la fecha del primer parto y
hace uso de la lidbreria datatime ( timedelta),primero convierte 
la fecha del primer parto a tipo fecha y luego toma este valor
y lo suma con el tiempo util (84 meses) para determinar la fecha
en que dicho animal dejara de ser productivo, posteriormente tambien
devolvera el tiempo restante para llegar a esa fecha mediante la resta
del tiempo actual
"""



def Edad_Sacrificio_Lecheras():
  try:
    # consulta de la fecha de primer parto
    Consulta_P1 = condb.execute(modelo_leche.select()).fetchall()
    # Recorre los campos de la consulta
    for i in Consulta_P1:
        # Toma el ID del bovino para calcular la edad de vida util
        id = i[1]
        # Toma la fecha de primer parto del animal en este caso es el campo 2
        fecha_Parto_1 = i[2]
     # calculo de la vida util mediante la suma del promedio de vida util con la fecha de parto
        fecha_Vida_Util = fecha_Parto_1 + timedelta(2555)
        # actualizacion del campo
        condb.execute(modelo_leche.update().values(fecha_vida_util=fecha_Vida_Util).where(
          modelo_leche.columns.id_bovino == id))
        logger.info(f'Funcion Edad_Sacrificio_Lecheras {fecha_Vida_Util} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Edad_Sacrificio_Lecheras: {e}')
    raise
  finally:
      condb.close()
        #return fecha_Vida_Util

"""
la siguiente funcion determina si la condicion de un animal para
levante es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 140 kg y edad de 8 a 10 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""



def Estado_Optimo_Levante():
  try:
    consulta_levante = condb.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Levante")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_levante:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
        # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado=="Vivo":
          if peso >= 140 and edad in range(8, 13):
            estado_levante = "Estado Optimo"
          elif peso < 140 and edad in range(8, 13):
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos"
          elif peso < 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y menos de 8 meses de edad"
          elif peso < 140 and edad > 12:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y mas de 12 meses de edad, considera descartarlo"
          elif peso >= 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene menos de 8 meses de edad"
          else:
            estado_levante = "Estado NO Optimo, este animal tiene una edad mayor a 12 meses, considera pasarlo a ceba"
        elif estado=="Muerto":
            estado_levante= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_levante= "Este animal esta Vendido, no se puede calcular su estado"
        #actualizacion del campo
        condb.execute(modelo_levante.update().values(edad=edad,peso=peso,estado=estado,
                      estado_optimo_levante=estado_levante).\
                      where(modelo_levante.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Levante {estado_levante} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Levante: {e}')
    raise
  finally:
      condb.close()
         #return estado_levante
"""
la siguiente funcion determina si la condicion de un animal para
ceba es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 350 kg y edad de 24 a 36 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""



def Estado_Optimo_Ceba():
  try:
    consulta_ceba = condb.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_ceba:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
    # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado == "Vivo":
          if peso >= 350 and edad in range(24, 37):
            estado_ceba = "Estado Optimo"
          elif peso < 350 and edad in range(24, 37):
            estado_ceba = "Estado NO Optimo, este animal tiene un peso menor a 350 kilos"
          elif peso >= 350 and edad < 24:
             estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad"
          elif peso < 350 and edad < 24:
            estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad y menos de 350 kilos"
          else:
            estado_ceba = "Estado NO Optimo, este animal tiene una edad mayor a 36 meses"
        elif estado=="Muerto":
            estado_ceba= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_ceba= "Este animal esta Vendido, no se puede calcular su estado"
        # actualizacion del campo
    # actualizacion del campo
        condb.execute(modelo_ceba.update().values(edad=edad,peso=peso,estado=estado,
                    estado_optimo_ceba=estado_ceba). \
                  where(modelo_ceba.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Ceba {estado_ceba} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Ceba: {e}')
    raise
  finally:
      condb.close()
       # return estado_ceba

"""
esta funcion calcula los dias abiertos apartir de la diferencia en dias
entre la fecha de ultimo parto y fecha de ultima prenez, siendo una medida
de productividad, pues si una vaca tiene mas de 120 dias abiertos, indica 
que no esta teniendo un ternero al ano, lo que indica que no esta siendo
productiva
"""



def Dias_Abiertos():
  try:
    # consulta a la tabla
    Consulta_fechas = condb.execute(modelo_leche.select()).fetchall()
    # Recorre los campos de la consulta
    for i in Consulta_fechas:
        # Toma el ID del bovino para calcular la variable
        id = i[1]
        # Toma la fecha de ultimmo parto del animal en este caso es el campo 11
        fecha_ultimo_p = i[11]
        # Toma la fecha de ultima prenez del animal en este caso es el campo 12
        fecha_ultima_prenez = i[12]
    # calculo de los dias entre las dos fechas (dias abiertos)
        Dias_A = (fecha_ultima_prenez.year - fecha_ultimo_p.year) * 360 + (
                fecha_ultima_prenez.month - fecha_ultimo_p.month) * 30 + \
             (fecha_ultima_prenez.day - fecha_ultimo_p.day)
    # actualizacion del campo
        condb.execute(modelo_leche.update().values(dias_abiertos=Dias_A).\
                      where(modelo_leche.columns.id_bovino == id))
        logger.info(f'Funcion Dias_Abiertos {Dias_A} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Dias_Abiertos: {e}')
    raise
  finally:
      condb.close()
        #return Dias_A

"""esta funcion determina el porcentaje de animales vivos que
existen en el hato,para ello utiliza la cantidad de animales vivos,
muertos y totales"""


@rutas_bovinos.post("/Calcular_Tasa_Sobrevivencia")
def Tasa_Sobrevivencia():
  try:
    # consulta y seleccion de los animales vivos
    estado_vivo = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # consulta y seleccion de los animales muertos
    estado_muerto = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # total de animales(vivos + muertos)
    totales = estado_vivo + estado_muerto
    # calculo de la tasa
    tasa = (estado_vivo / totales) * 100
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(tasa_supervivencia=tasa))
    logger.info(f'Funcion Tasa_Sobrevivencia {tasa} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion Tasa_Sobrevivencia: {e}')
      raise
  finally:
      session.close()
    #return tasa

"""esta funcion calcula en terminos de porcentaje, cuantos terneros
(animales de 0 a 6 meses) han fallecido, para ello consulta la cantidad 
de animales muertos y el total para mediante una regla de 3 obtener
el porcentaje
"""


@rutas_bovinos.get("/Calcular_perdida_Terneros")
async def perdida_Terneros():
 try:
    # consulta, seleccion y conteo de animales con edad de 0 a 6 meses que se encuentren muertos
    muertos = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 6)). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # consulta, seleccion y conteo de animales con edad de 0 a 6 meses
    totales = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 6)).count()
    # calculo de la tasa
    tasa_perd = (muertos / totales) * 100
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(perdida_de_terneros=tasa_perd))
    logger.info(f'Funcion perdida_Terneros {tasa_perd} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion perdida_Terneros: {e}')
     raise
 finally:
     session.close()
 return tasa_perd


"""esta funcion determina la cantidad de vacas no prenadas
esto con el  fin de mostrar cuantos vientres estan produciendo en el hato"""


@rutas_bovinos.get("/Calcular_vacas_prenadas")
async def vacas_prenadas():
  try:
    # join de tabla bovinos y tabla leche mediante id_bovino \
    # filtrado y conteo animales con datos prenez Prenada que se encuentren vivos
    consulta_prenadas = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Prenada').count()
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vacas_prenadas=consulta_prenadas))
    logger.info(f'Funcion vacas_prenadas {consulta_prenadas} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas: {e}')
      raise
  finally:
      session.close()
  return consulta_prenadas


"""esta funcion calcula el porcentaje de vacas que se encuentran preñadas"""


@rutas_bovinos.get("/Calcular_vacas_prenadas_porcentaje")
async def vacas_prenadas_porcentaje():
  try:
    # consulta de vacas prenadas y vacas vacias en la base de datos
    prenadas, vacias = session.query \
        (modelo_indicadores.c.vacas_prenadas, modelo_indicadores.c.vacas_vacias).first()
    # calculo del total de animales
    totales = prenadas + vacias
    # calculo procentaje de vacas prenadas
    vacas_estado_pren = (prenadas / totales) * 100
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vacas_prenadas_porcentaje=vacas_estado_pren))
    logger.info(f'Funcion vacas_prenadas_porcentaje {vacas_estado_pren} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas_porcentaje: {e}')
      raise
  finally:
      session.close()
  return vacas_estado_pren


"""estas funciones muestra la cantidad de animales totales, tambien segun su
proposito, sexo, estado, rango de edades y estado de ordeno"""


@rutas_bovinos.get("/Calcular_animales_totales")
async def animales_totales():


  try:
    # consulta de total de animales vivos
    total_animales = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.columns.id_indicadores == 1).
                    values(total_animales=total_animales))
    logger.info(f'Funcion animales_totales {total_animales} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_totales: {e}')
      raise
  finally:
      session.close()
  return total_animales

@rutas_bovinos.get("/Calcular_animales_ceba")
async def animales_ceba():
  try:
    # consulta de total de animales vivos con proposito de ceba
    prop_ceba = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Ceba").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_ceba=prop_ceba))
    logger.info(f'Funcion animales_ceba {prop_ceba} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_ceba: {e}')
      raise
  finally:
      session.close()
  return prop_ceba


@rutas_bovinos.get("/Calcular_animales_levante")
async def animales_levante():
    # consulta de total de animales vivos con proposito de levante
    prop_levante = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Levante").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_levante=prop_levante))
    session.commit()
    return prop_levante


@rutas_bovinos.post("/Calcular_animales_leche")
def animales_leche():
  try:
    # consulta de total de animales vivos con proposito de leche
    prop_leche = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Leche").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_leche=prop_leche))
    logger.info(f'Funcion animales_leche {prop_leche} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_leche: {e}')
      raise
  finally:
      session.close()
    #return prop_leche


@rutas_bovinos.get("/Calcular_animales_muertos")
async def animales_muertos():
  try:
    # consulta de total de animales muertos
    estado_muerto = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_fallecidos=estado_muerto))
    logger.info(f'Funcion animales_muertos {estado_muerto} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_muertos: {e}')
      raise
  finally:
      session.close()
  return estado_muerto


@rutas_bovinos.get("/Calcular_animales_vendidos")
async def animales_vendidos():
  try:
    # consulta de total de animales vendidos
    estado_vendido = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vendido").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_vendidos=estado_vendido))
    logger.info(f'Funcion animales_vendidos {estado_vendido} ')
    session.commit()
  except Exception as e:
    logger.error(f'Error Funcion animales_vendidos: {e}')
    raise
  finally:
    session.close()
  return estado_vendido


@rutas_bovinos.get("/Calcular_animales_machos")
async def animales_sexo_macho():
  try:
    # consulta de total de animales vivos con sexo macho
    machos = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Macho").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(machos=machos))
    logger.info(f'Funcion animales_sexo_macho {machos} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_macho: {e}')
      raise
  finally:
      session.close()
  return machos


@rutas_bovinos.get("/Calcular_animales_hembras")
async def animales_sexo_hembra():
  try:
    # consulta de total de animales vivos con sexo hembra
    hembras = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(hembras=hembras))
    logger.info(f'Funcion animales_sexo_hembra {hembras} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_hembra: {e}')
      raise
  finally:
      session.close()
  return hembras


@rutas_bovinos.get("/Calcular_animales_ordeno")
async def animales_en_ordeno():
 try:
    # join, consulta y conteo de animales vivos que son ordenados
    vacas_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'Si').count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vacas_en_ordeno=vacas_ordeno))
    logger.info(f'Funcion animales_en_ordeno {vacas_ordeno} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion animales_en_ordeno: {e}')
     raise
 finally:
     session.close()
 return vacas_ordeno

@rutas_bovinos.get("/Calcular_animales_no_ordeno")
async def animales_no_ordeno():
  try:
    # join, consulta y conteo de animales vivos que no son ordenados
    vacas_no_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'No').count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vacas_no_ordeno=vacas_no_ordeno))
    logger.info(f'Funcion animales_no_ordeno {vacas_no_ordeno} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_no_ordeno: {e}')
      raise
  finally:
      session.close()
  return vacas_no_ordeno


@rutas_bovinos.get("/Calcular_porcentaje_ordeno")
async def porcentaje_ordeno():
  try:
    # consulta de animales ordenados y no ordenados
    ordeno, no_ordeno = session.query \
        (modelo_indicadores.c.vacas_en_ordeno, modelo_indicadores.c.vacas_no_ordeno).first()
    # porcentaje de vacas en ordeno
    vacas_ordeno_porcentaje = (ordeno / (no_ordeno + ordeno)) * 100
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(porcentaje_ordeno=vacas_ordeno_porcentaje))
    logger.info(f'Funcion porcentaje_ordeno {vacas_ordeno_porcentaje} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion porcentaje_ordeno: {e}')
      raise
  finally:
      session.close()
  return vacas_ordeno_porcentaje


@rutas_bovinos.get("/Calcular_animales_edad_0_9")
async def animales_edad_0_9():
  try:
    # consulta y conteo de animales con edades entre 0 a 9 meses
    edades_0_9 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 9)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_0_9=edades_0_9))
    logger.info(f'Funcion animales_edad_0_9 {edades_0_9} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_0_9: {e}')
      raise
  finally:
      session.close()
  return edades_0_9


@rutas_bovinos.get("/Calcular_animales_edad_9_12")
async def animales_edad_9_12():
  try:
    # consulta y conteo de animales con edades entre 10 a 12 meses
    edades_9_12 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 10, 12)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_9_12=edades_9_12))
    logger.info(f'Funcion animales_edad_9_12 {edades_9_12} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_9_12: {e}')
      raise
  finally:
      session.close()
  return edades_9_12


@rutas_bovinos.get("/Calcular_animales_edad_12_24")
async def animales_edad_12_24():
 try:
    # consulta y conteo de animales con edades entre 13 a 24 meses
    edades_12_24 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 13, 24)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_12_24=edades_12_24))
    logger.info(f'Funcion animales_edad_12_24 {edades_12_24} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion animales_edad_12_24: {e}')
     raise
 finally:
     session.close()
 return edades_12_24


@rutas_bovinos.get("/Calcular_animales_edad_24_36")
async def animales_edad_24_36():
  try:
    # consulta y conteo de animales con edades entre 25 a 36 meses
    edades_24_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 25, 36)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_24_36=edades_24_36))
    logger.info(f'Funcion animales_edad_24_36 {edades_24_36} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_24_36: {e}')
      raise
  finally:
      session.close()
  return edades_24_36


@rutas_bovinos.get("/Calcular_animales_edad_mayor_36")
async def animales_edad_mayor_a_36():
  try:
    # consulta y conteo de animales con edades igual o mayor a 37 meses
    edades_mayor_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 37, 500)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_mayor_36=edades_mayor_36))
    logger.info(f'Funcion animales_edad_mayor_a_36 {edades_mayor_36} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_mayor_a_36: {e}')
      raise
  finally:
      session.close()
  return edades_mayor_36


@rutas_bovinos.get("/Calcular_Animales_Optimo_Levante")
async def Animales_Optimo_Levante():
 try:
    # join,consulta y conteo de animales vivos con estado optimo
    levante_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_levante.c.estado_optimo_levante). \
        join(modelo_levante, modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_levante.c.estado_optimo_levante == "Estado Optimo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_optimos_levante=levante_optimo))
    logger.info(f'Funcion Animales_Optimo_Levante {levante_optimo} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion Animales_Optimo_Levante: {e}')
     raise
 finally:
     session.close()
 return levante_optimo

"la siguiente funcion"
@rutas_bovinos.get("/Calcular_Animales_Optimo_Ceba")
async def Animales_Optimo_Ceba():
  try:
    # join,consulta y conteo de animales vivos con estado optimo
    ceba_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_ceba.c.estado_optimo_ceba). \
        join(modelo_ceba, modelo_bovinos_inventario.c.id_bovino == modelo_ceba.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_ceba.c.estado_optimo_ceba == "Estado Optimo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_optimos_ceba=ceba_optimo))
    logger.info(f'Funcion Animales_Optimo_Ceba {ceba_optimo} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion Animales_Optimo_Ceba: {e}')
      raise
  finally:
      session.close()
  return ceba_optimo

"""la siguiente funncion la fecha en que un macho empezara a bajar fertilidad, para ello
 suma los dias de vida util con la edad del animal para determinar este campo"""
def vida_util_macho_reproductor():
 try:
     #join con tabla de bovinos y consulta
    consulta_machos_r = session.query(modelo_macho_reproductor.c.id_bovino,modelo_bovinos_inventario.c.edad,modelo_bovinos_inventario.c.peso,
                          modelo_bovinos_inventario.c.estado,modelo_bovinos_inventario.c.fecha_nacimiento).\
        join(modelo_macho_reproductor,modelo_bovinos_inventario.c.id_bovino == modelo_macho_reproductor.c.id_bovino).all()
    # Recorre los campos de la consulta
    for i in consulta_machos_r:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[2]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[3]
        # Toma la fecha de nacimiento en este caso es el campo 4
        fecha_nacimiento = i[4]
        # calculo de la vida util mediante la suma del promedio de vida util con la fecha de nacimiento
        fecha_vida_util = fecha_nacimiento + timedelta(2555)
        # actualizacion del campo
        condb.execute(modelo_macho_reproductor.update().values(edad=edad, peso=peso, estado=estado,
                                                     fecha_vida_util=fecha_vida_util). \
                      where(modelo_macho_reproductor.columns.id_bovino == id))
        logger.info(f'Funcion vida_util_macho_reproductor {fecha_vida_util} ')
        condb.commit()
 except Exception as e:
   logger.error(f'Error Funcion vida_util_macho_reproductor: {e}')
   raise
 finally:
  condb.close()

"""la siguiente funncion determina si la cantidad de machos reproductores es suficciente
o demasiada para las hembras que se pueden preñar """
def relacion_macho_reproductor_vientres_aptos():
  #la siguiente variable debe ser global ya que esta dentro de un bucle if anidado
  global interpretacion
  try:
    # consulta y conteo de toros reproductores vivos
    cantidad_reproductores = session.query(modelo_macho_reproductor). \
        where(modelo_macho_reproductor.columns.estado == "Vivo").count()
    # consulta y conteo de vientres aptos vivos (edad de 16 meses la cual es el periodo de celo de una novilla)
    cantidad_vientres_aptos = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 16, 500)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra").count()
    #calculo de la relacion toros-vientres
    relacion= (cantidad_reproductores/cantidad_vientres_aptos)*100
    #caclulo de cantidad recomendada de reproductores para la cantidad de vientres aptos
    cantidad_recomendada = cantidad_vientres_aptos/25
    #interpretacion del calculo de la relacion toros-vientres
    if relacion < 4:
          interpretacion = f'no Tienes suficientes machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
    elif relacion > 4:
        if cantidad_reproductores==1 and cantidad_vientres_aptos <= 25:
          interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} macho reproductor para tus {cantidad_vientres_aptos} hembras aptas'
        elif cantidad_reproductores > 1 and cantidad_vientres_aptos <= 25:
          interpretacion = f'Tienes demasiados machos reproductores, debes tener solamente un macho reproductor para tus {cantidad_vientres_aptos} hembras aptas '
        else:
          interpretacion = f'Tienes demasiados machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
    elif relacion==4:
          interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas'
    # actualizacion de campo de cantidad de vientres aptos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vientres_aptos=cantidad_vientres_aptos,
                           relacion_toros_vientres_aptos=relacion,
                           interpretacion_relacion_toros_vientres_aptos=interpretacion))
    logger.info(f'Funcion relacion_macho_reproductor_vientres_aptos {cantidad_vientres_aptos,relacion,interpretacion} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion relacion_macho_reproductor_vientres_aptos: {e}')
      raise
  finally:
      session.close()
  return (relacion, interpretacion, cantidad_vientres_aptos)
"""la siguiente funcion determina el consumo de forraje vivo y agua por cada animal"""
def carga_animal():
  global temperatura, consumo_agua
  try:
    # consulta temperatura ambiente del lugar donde esta el ganado
    consulta_temperatura = session.query(modelo_indicadores). \
          where(modelo_indicadores.c.id_indicadores == 1).all()
    for i in consulta_temperatura:
        # Toma la temperatura, el campo 31
        temperatura = i[31]
    #join con tabla de bovinos y consulta
    consulta_bovinos = session.query(modelo_carga_animal_y_consumo_agua.c.id_bovino, modelo_bovinos_inventario.c.edad,
                        modelo_bovinos_inventario.c.peso,modelo_bovinos_inventario.c.estado). \
        join(modelo_carga_animal_y_consumo_agua,
             modelo_bovinos_inventario.c.id_bovino == modelo_carga_animal_y_consumo_agua.c.id_bovino).all()
    # Recorre los campos de la consulta
    for i in consulta_bovinos:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[2]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[3]
        # determinacion de la unidad animal (una unidad animal equivale a 400 kg de peso vivo)
        #si un animal esta muerto o vendido su consumo forraje y agua sera 0
        if estado == "Vivo":
            unidad_animal = peso / 400
            # determinacion del consumo de forraje vivo por animal (cada animal consume un 10% de su peso vivo al dia)
            consumo_forraje = peso * 0.1
            #una unidad animal puede consimir hasta 16 kg de materia seca al dia
            consumo_materia_seca=unidad_animal*16
            # determinacion del consumo de agua por animal(por cada kg de materia seca consumida se necesita 3 o mas litros de agua)
            # el consumo de agua puede variar segun la temperatura
            if temperatura in range(-10, 6):
                consumo_agua = (consumo_materia_seca) * 3
                # actualizacion de campos
                session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                                   valor_unidad_animal=unidad_animal,
                                                                                   consumo_forraje_vivo=consumo_forraje,
                                                                                   consumo_agua=consumo_agua). \
                                where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                session.commit()
            if temperatura in range(6, 16):
                # actualizacion de campos
                consumo_agua = (consumo_materia_seca) * 4
                session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                                   valor_unidad_animal=unidad_animal,
                                                                                   consumo_forraje_vivo=consumo_forraje,
                                                                                   consumo_agua=consumo_agua). \
                                where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                session.commit()
            if temperatura in range(16, 26):
                # actualizacion de campos
                consumo_agua = (consumo_materia_seca) * 5
                session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                                   valor_unidad_animal=unidad_animal,
                                                                                   consumo_forraje_vivo=consumo_forraje,
                                                                                   consumo_agua=consumo_agua). \
                                where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                session.commit()
            if temperatura in range(26, 32):
                # actualizacion de campos
                consumo_agua = (consumo_materia_seca) * 6
                session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                                   valor_unidad_animal=unidad_animal,
                                                                                   consumo_forraje_vivo=consumo_forraje,
                                                                                   consumo_agua=consumo_agua). \
                                where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                session.commit()
            if temperatura >= 32:
                # actualizacion de campos
                consumo_agua = (consumo_materia_seca) * 8
                session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                                   valor_unidad_animal=unidad_animal,
                                                                                   consumo_forraje_vivo=consumo_forraje,
                                                                                   consumo_agua=consumo_agua). \
                                where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                session.commit()
        else:
            unidad_animal = 0
            consumo_forraje = 0
            consumo_agua = 0
            # actualizacion de campos
            session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad, peso=peso, estado=estado,
                                                                               valor_unidad_animal=unidad_animal,
                                                                               consumo_forraje_vivo=consumo_forraje,
                                                                               consumo_agua=consumo_agua). \
                            where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
            session.commit()
        logger.info(f'Funcion carga_animal {unidad_animal} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion carga_animal: {e}')
      raise
  finally:
      session.close()
"""funcion de capacidad de carga"""
def capacidad_carga():
  try:
    # consulta hectareas de forraje vivo disponible en el predio
    consulta_hectareas = session.query(modelo_capacidad_carga.columns.hectareas_forraje). \
          where(modelo_capacidad_carga.c.id_capacidad == 1).all()
    for i in consulta_hectareas:
        # Toma las hectareas de pasto en este caso es el campo 0
        hectareas = i[0]
        #determinacion de produccion de pasto por hectarea
        #conversion de hectareas a metros cuadrados
        metros=hectareas*10000
        #los pastos tropicales producen un aproximado de 0.003 kilogramos de materia seca por metro cuadrado al dia
        produccion_materia_seca=0.003*metros
        #determinacion de la cantidad de unidades animales que esta produccion puede mantener al dia
        #una unidad animal puede consumir hasta 16 kilos de materia seca al dia
        capacidad_unidades_animales_dia=round((produccion_materia_seca/16),2)
        interpertacion_capacidad=f'con tus hectareas de pasto, puedes mantener hasta {capacidad_unidades_animales_dia} unidades animales'
        #actualizacion de campos
        session.execute(modelo_capacidad_carga.update().values(produccion_materia_seca=produccion_materia_seca,
                                                               capacidad_animales=interpertacion_capacidad). \
                        where(modelo_capacidad_carga.columns.id_capacidad == 1))
        logger.info(f'Funcion capacidad_carga {interpertacion_capacidad} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion capacidad_carga: {e}')
      raise
  finally:
      session.close()
"""la siguiente funcion es suma todas las unidades animales existentes"""
def consumo_global_agua_y_totalidad_unidades_animales():
    #la siguiente variable requiere ser global debido a que esta en un bucle for
  global interpretacion
  try:
    # consulta de sumatoria de las unidades animales y su consumo de agua
    consulta_unidades_animales = session.query(func.sum(modelo_carga_animal_y_consumo_agua.columns.valor_unidad_animal)).all()
    consulta_consumo_agua= session.query(func.sum(modelo_carga_animal_y_consumo_agua.columns.consumo_agua)).all()
    for i in consulta_unidades_animales:
        # Toma la totalidad de unidades animales en este caso es el campo 0
        total_unidades_animales =i[0]
        #para determinar el consumo de materia seca total hay que considerar que una unidad animal consume hasta 16000 gramos de materia seca al dia
        consumo_unidades= total_unidades_animales*16000
        #un metro cuadrado de pasto produce hasta 3 gramos de materia seca al dia
        metros_de_forraje_requerido= consumo_unidades/3
        hectareas_requeridas=metros_de_forraje_requerido/10000
        interpretacion=f'Tienes un total de {round(total_unidades_animales,2)} unidades animales, que requieren de {round(hectareas_requeridas,3)} hectareas de o {round(metros_de_forraje_requerido,3)} metros cuadrados forraje para mantenerse'
    for i in consulta_consumo_agua:
        # Toma la totalidad del consumo de agua en este caso es el campo 0
        consumo_agua_litros = round(i[0],2)
        consumo_agua_bebederos= round((consumo_agua_litros/500),0)
        if consumo_agua_bebederos <1:
            consumo_agua_bebederos=1
        total_consumo_agua =f'Tus animales necesitan {consumo_agua_litros} litros de agua al dia (equivalente a {consumo_agua_bebederos} bebedero(s) de 500 litros)'
        session.execute(modelo_indicadores.update().values(consumo_global_agua=total_consumo_agua,
                                                               total_unidades_animales=interpretacion). \
                        where(modelo_indicadores.columns.id_indicadores == 1))
        logger.info(f'Funcion consumo_global_agua_y_totalidad_unidades_animales {consulta_consumo_agua} ')
        logger.info(f'Funcion consumo_global_agua_y_totalidad_unidades_animales {consulta_consumo_agua} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion consumo_global_agua_y_totalidad_unidades_animales: {e}')
      raise
  finally:
      session.close()
"""la siguiente es una funcion que calcula las hectareas de forraje requeridas asi
como la cantidad de agua necesaria para un lote de animales que el usuario desee conocer
cuanto alimento y debida necesita"""
def calculadora_pastoreo():
  try:
    # join de tabla de carga animal y pastoreo
    consulta_bovinos = session.query(modelo_calculadora_hectareas_pastoreo.c.id_bovino, modelo_carga_animal_y_consumo_agua.c.valor_unidad_animal,
                                     modelo_carga_animal_y_consumo_agua.c.consumo_agua). \
        join(modelo_calculadora_hectareas_pastoreo,
             modelo_calculadora_hectareas_pastoreo.c.id_bovino == modelo_carga_animal_y_consumo_agua.c.id_bovino).all()
    for i in consulta_bovinos:
        # Toma el id bovino en este caso es el campo 0
        id =i[0]
        # Toma las unidades animales en este caso es el campo 1
        valor_unidad_animal = i[1]
        # Toma el consumo de agua en este caso es el campo 2
        consumo_agua = i[2]
        #determinacion de las hectareas necesarias por cada animal
        consumo_unidades = valor_unidad_animal * 16000
        metros_de_forraje_requerido = (consumo_unidades / 3)
        hectareas_requeridas = round((metros_de_forraje_requerido / 10000),2)
        session.execute(modelo_calculadora_hectareas_pastoreo.update().values(hectareas_necesarias=hectareas_requeridas,
                                                               consumo_agua=consumo_agua). \
                        where(modelo_calculadora_hectareas_pastoreo.columns.id_bovino == id))
        logger.info(f'Funcion calculadora_pastoreo {hectareas_requeridas} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion calculadora_pastoreo: {e}')
      raise
  finally:
      session.close()
"la siguiente funcion determina los consumos globales para el lote " \
"creado en la calculadora"
def consumo_agua_y_hectareas_por_lote():
  global total_hectareas
  try:
    # consulta de varibles y sumatoria
    consulta_suma_hectareas = session.query(func.sum(modelo_calculadora_hectareas_pastoreo.columns.hectareas_necesarias)).all()
    consulta_suma_consumo_agua = session.query(func.sum(modelo_calculadora_hectareas_pastoreo.columns.consumo_agua)).all()
    #recorre el bucle para cada consulta
    for i in consulta_suma_hectareas:
        # Toma la totalidad de hectareas requeridas por animal en este caso es el campo 0
        total_hectareas =round((i[0]),2)
    for i in consulta_suma_consumo_agua:
        # Toma la totalidad de consumos de agua requeridos al dia por animal en este caso es el campo 0
        consumo_agua_litros = round(i[0], 2)
        consumo_agua_bebederos = round((consumo_agua_litros / 500), 2)
        if consumo_agua_bebederos < 1:
            consumo_agua_bebederos = 1
        total_consumo_agua =f'Tus animales necesitan {consumo_agua_litros} litros de agua al dia (equivalente a {consumo_agua_bebederos} bebederos de 500 litros)'
        #actualizacion de campos
        session.execute(modelo_indicadores.update().values(calculadora_hectareas=total_hectareas,
                                                               calculadora_consumo_agua=total_consumo_agua). \
                        where(modelo_indicadores.columns.id_indicadores == 1))
        logger.info(f'Funcion consumo_agua_y_hectareas_por_lote {total_hectareas} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion consumo_agua_y_hectareas_por_lote: {e}')
      raise
  finally:
      session.close()
"""la siguiente funcion es una calculadora que determina la fecha aproximada de parto
de un animal en base a su fecha de preñez"""
def fecha_aproximada_parto():
  try:
    # join de tablas
    consulta_vacas = session.query(modelo_partos.c.id_bovino,modelo_partos.c.fecha_estimada_prenez, modelo_bovinos_inventario.c.edad,
                                     modelo_bovinos_inventario.c.peso, modelo_bovinos_inventario.c.estado). \
        join(modelo_partos,modelo_partos.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    #recorrer los campos
    for i in consulta_vacas:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        fecha_estimada_prenez = i[1]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[3]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[4]
        #calculo de la fecha aproximada de parto
        if estado=="Vivo":
          fecha_estimada_parto = fecha_estimada_prenez + timedelta(285)
        else:
          fecha_estimada_parto = None
        #actualizacion de campos
        session.execute(modelo_partos.update().values(fecha_estimada_parto=fecha_estimada_parto,edad=edad,
                                                      peso=peso). \
                        where(modelo_partos.columns.id_bovino == id))

        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion fecha_aproximada_parto: {e}')
      raise
  finally:
      session.close()
"""la siguiente funcion elimina todos los vientres aptos de la 
tabla, esto se realiza para evitar la duplicidad de datos"""
def Eliminacion_total_vientres_aptos():
  try:
      #llamada de funcion que elimina todos los datos
        session.execute(modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino))
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion Eliminacion_total_vientres_aptos: {e}')
      raise
  finally:
      session.close()
"""la siguiente funcion muestra los vientres aptos, es decir,
animales hembras vivos con una edad igual o mayor a 16 meses"""
def vientres_aptos():
  try:
    #llamada de funcion que elimina registro anterior
    Eliminacion_total_vientres_aptos()
    # consulta de vacas que cumplen con la condicion
    consulta_vientres = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 16, 500)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra").all()
    for i in consulta_vientres:
        # Toma el ID del bovino en este caso es el campo 0
        id1 = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        #actualizacion de campos
        session.execute(modelo_vientres_aptos.insert().values(id_bovino=id1,edad=edad,
                                                      peso=peso))
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion vientres_aptos: {e}')
      raise
  finally:
      session.close()
"""la siguiente funcion trae los campos de edad y peso de cada animal
a los animales de descarte"""
def descarte():
  try:
      # join de tablas
    consulta_animales = session.query(modelo_descarte.c.id_bovino, modelo_bovinos_inventario.c.edad,
                            modelo_bovinos_inventario.c.peso).\
        join(modelo_descarte, modelo_descarte.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    for i in consulta_animales:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[2]
        # actualizacion de campos
        session.execute(modelo_descarte.update().values( edad=edad,
                                                      peso=peso). \
                        where(modelo_descarte.columns.id_bovino == id))
        logger.info(f'Funcion descarte {peso} ')
        session.commit()
  except Exception as e:
     logger.error(f'Error Funcion descarte: {e}')
     raise
  finally:
     session.close()