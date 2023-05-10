'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.funcion_litros_leche import promedio_litros_leche
# # importa la conexion de la base de datos
from config.db import condb, session
# # importa el esquema de los bovinos
from models.modelo_bovinos import  modelo_leche, modelo_bovinos_inventario, \
    modelo_indicadores
from fastapi import  status,  APIRouter, Response
from datetime import date,  timedelta
from routes.rutas_bovinos import eliminarduplicados
from sqlalchemy import update
from schemas.schemas_bovinos import  esquema_produccion_leche

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

Produccion_Leche = APIRouter()



@Produccion_Leche.get("/listar_prod_leche" , response_model=list[esquema_produccion_leche])
async def inventario_prod_leche():

    try:
        Edad_Primer_Parto()
        Edad_Sacrificio_Lecheras()
        promedio_litros_leche()
        intervalo_partos()

        itemsLeche = session.query(modelo_leche).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        session.close()
    return itemsLeche


@Produccion_Leche.get("/Calcular_animales_no_ordeno")
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

    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_no_ordeno: {e}')
      raise
  finally:
      session.close()
  return vacas_no_ordeno


@Produccion_Leche.get("/Calcular_vacas_prenadas_porcentaje")
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

    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas_porcentaje: {e}')
      raise
  finally:
      session.close()
  return vacas_estado_pren



@Produccion_Leche.get("/Calcular_vacas_prenadas")
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

    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas: {e}')
      raise
  finally:
      session.close()
  return consulta_prenadas





"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""


@Produccion_Leche.post(
    "/crear_prod_leche/{fecha_primer_parto}/{id_bovino}/{datos_prenez}/{ordeno}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdLeche(fecha_primer_parto: date, id_bovino: str,
                   datos_prenez: str, ordeno: str,proposito:str):
    eliminarduplicados()

    try:

        consulta = condb.execute(
            modelo_leche.select().where(
                modelo_leche.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresopleche = modelo_leche.insert().values(fecha_primer_parto=fecha_primer_parto, id_bovino=id_bovino,
                                                          datos_prenez=datos_prenez,
                                                         ordeno=ordeno, proposito=proposito)

            condb.execute(ingresopleche)
            condb.commit()
        else:

            condb.execute(modelo_leche.update().where(modelo_leche.c.id_bovino == id_bovino).values(
                fecha_primer_parto=fecha_primer_parto, id_bovino=id_bovino,
                 datos_prenez=datos_prenez,
                ordeno=ordeno, proposito=proposito))
            condb.commit()

            condb.commit()




    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Leche: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)





""" Librerias """




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

        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Edad_Primer_Parto: {e}')
    raise
  finally:
      condb.close()

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
        Dias_A = (fecha_ultima_prenez.year - fecha_ultimo_p.year) * 365 + (
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

def EliminarDuplicadosLeche():
    itemsLeche = session.execute(modelo_leche.select()).all()
    for ileche in itemsLeche:
        propositoleche = ileche[16]
        idleche = ileche[0]

        if propositoleche == 'Levante' or propositoleche == 'Ceba':
            eliminarlevanteleche = condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))
            logger.info(f'Se ELIMINA EL DATO REPETIDO DE LECHE LEVANTE =  {eliminarlevanteleche} ')
            condb.commit(eliminarlevanteleche)
        else:
            pass


"""esta funcion calcula el porcentaje de vacas que se encuentran preñadas"""


