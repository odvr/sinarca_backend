'''
Librerias requeridas

@autor : odvr

'''

import logging
from fastapi import APIRouter, Response

# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_levante, \
    modelo_indicadores, modelo_ceba
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_leche, esquema_produccion_levante, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func
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
    try:
        items = condb.execute(modelo_bovinos_inventario.select()).fetchall()
        logger.info(f'Se obtuvieron {len(items)} registros de inventario de bovinos.')

    except Exception as e:
        logger.error(f'Error al obtener inventario de bovinos: {e}')
        raise
    finally:
        condb.close()

    return items




@rutas_bovinos.get("/listar_prod_leche" )
async def inventario_prod_leche():

    # llamado de funciones
    Edad_Primer_Parto()
    Duracion_Lactancia()
    Edad_Sacrificio_Lecheras()
    Dias_Abiertos()
    animales_no_ordeno()
    try:
        itemsLeche = session.execute(modelo_leche.select()).all()
        logger.info(f'Se obtuvieron {len(itemsLeche)} registros de inventario de Produccion Leche.')
    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        session.close()
    return itemsLeche

"""
Lista los animales en Levante

"""

@rutas_bovinos.get("/listar_prod_levante" )
async def inventario_levante():
    Estado_Optimo_Levante()
    try:
        itemsLevante = session.execute(modelo_levante.select()).all()
        #itemsLevante = session.query(modelo_bovinos_inventario.c.estado).join( modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino).all()


        logger.info(f'Se obtuvieron {len(itemsLevante)} registros de inventario de Produccion Levante.')
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
    try:
        itemsceba = session.execute(modelo_ceba.select()).all()
        logger.info(f'Se obtuvieron {len(itemsceba)} registros de inventario de Produccion Levante.')
    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        session.close()
    return itemsceba


"""
Lista los datos de la tabla prod leche inventario
"""

@rutas_bovinos.get("/listar_bovino_prodLeche/{id_bovino}")
async def id_inventario_bovino_leche(id_bovino: str):
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
        logger.error(f'Error al obtener Listar Produccion Ceba: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta



"""
Lista los datos de la tabla prod levante para la opcion de editar bovino
"""

@rutas_bovinos.get("/listar_bovino_proceba/{id_bovino}")
async def id_inventario_bovino_ceba(id_bovino: str):
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
    "/crear_prod_leche/{fecha_primer_parto}/{id_bovino}/{fecha_inicial_ordeno}/{fecha_fin_ordeno}/{fecha_ultimo_parto}/{fecha_ultima_prenez}/{num_partos}/{tipo_parto}/{datos_prenez}/{ordeno}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdLeche(fecha_primer_parto: date, id_bovino: str, fecha_inicial_ordeno: date, fecha_fin_ordeno: date,
                   fecha_ultimo_parto: date, fecha_ultima_prenez: date, num_partos: int, tipo_parto: str,
                   datos_prenez: str, ordeno: str):

    try:
        ingresopleche = modelo_leche.insert().values(fecha_primer_parto=fecha_primer_parto, id_bovino=id_bovino,
                                                     fecha_inicial_ordeno=fecha_inicial_ordeno,
                                                     fecha_fin_ordeno=fecha_fin_ordeno,
                                                     fecha_ultimo_parto=fecha_ultimo_parto,
                                                     fecha_ultima_prenez=fecha_ultima_prenez, num_partos=num_partos,
                                                     tipo_parto=tipo_parto, datos_prenez=datos_prenez, ordeno=ordeno)
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
Eliminar los duplicados
"""
def eliminarduplicados():

    consultaduplicados = session.query(modelo_leche.c.id_bovino).union_all(session.query(modelo_levante.c.id_bovino)).union_all(session.query(modelo_ceba.c.id_bovino))
    print(consultaduplicados)

eliminarduplicados()




"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""

"""
Funcion crear Levante
"""
@rutas_bovinos.post(
    "/crear_prod_levante/{id_bovino}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdLevante(id_bovino: str):

    try:
        ingresoplevante = modelo_levante.insert().values(id_bovino=id_bovino)
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
Crear Ceba
"""
@rutas_bovinos.post(
    "/crear_prod_ceba/{id_bovino}",
    status_code=HTTP_204_NO_CONTENT)
async def CrearProdCeba(id_bovino: str):

    try:
        ingresopceba = modelo_ceba.insert().values(id_bovino=id_bovino)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de leche {ingresopceba} ')

        condb.execute(ingresopceba)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Ceba: {e}')
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
    consulta_fecha_nacimiento = condb.execute(modelo_bovinos_inventario.select()).fetchall()
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
y lo suma con el tiempo util (72.3 meses) para determinar la fecha
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
        fecha_Vida_Util = fecha_Parto_1 + timedelta(2169)
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
