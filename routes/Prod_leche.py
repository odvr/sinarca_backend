'''
Librerias requeridas
'''
import logging
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.Registro_partos import registro_partos_animales
from Lib.clasificacion_ganado_leche import tipo_ganado_leche
from Lib.funcion_IEP_por_raza import IEP_por_raza
from Lib.funcion_litros_leche import promedio_litros_leche
from Lib.funcion_litros_por_raza import litros_por_raza
from Lib.funcion_peso_por_raza import peso_segun_raza
# # importa la conexion de la base de datos
from config.db import  get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_leche, modelo_bovinos_inventario, \
    modelo_indicadores, modelo_orden_litros
from fastapi import  status,  APIRouter, Response
from datetime import date,  timedelta
from routes.rutas_bovinos import get_current_user
from sqlalchemy import update
from schemas.schemas_bovinos import esquema_produccion_leche, esquema_orden_litros, Esquema_Usuario
from fastapi import  Depends,HTTPException
from sqlalchemy.orm import Session
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


import crud



def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()



@Produccion_Leche.get("/listar_bovino_prodLeche/{id_bovino}", response_model=esquema_produccion_leche,tags=["Produccion Leche"] )
async def id_inventario_bovino_leche(id_bovino: str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        consulta = db.execute(
            modelo_leche.select().where(modelo_leche.columns.id_bovino == id_bovino)).first()
        # Cerrar la sesión
        db.close()

    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Leche: {e}')
        raise
    finally:
        db.close()
    # condb.commit()
    return consulta


@Produccion_Leche.get("/listar_prod_leche" , response_model=list[esquema_produccion_leche],tags=["Produccion Leche"])
async def inventario_prod_leche(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        "Librerias Requeridas"
        peso_segun_raza(session=db,current_user=current_user)
        Edad_Primer_Parto(session=db)
        Edad_Sacrificio_Lecheras(condb=db)
        promedio_litros_leche(session=db)
        intervalo_partos(session=db,current_user=current_user)
        EliminarDuplicadosLeche(condb=db)
        tipo_ganado_leche(session= db,current_user=current_user)
        IEP_por_raza(session= db,current_user=current_user)
        registro_partos_animales(session= db,current_user=current_user)



        #itemsLeche = db.query(modelo_leche).all()
        itemsLeche = db.query(modelo_leche).filter(modelo_leche.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        db.close()
    return itemsLeche




"""
Promedio Por Razas
"""


@Produccion_Leche.get("/LitrosPorRaza" , response_model=list[esquema_orden_litros])
async def inventario_prod_leche(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        litros_por_raza(session=db)

        #itemsLeche = db.query(modelo_orden_litros).all()
        itemsLeche = db.query(modelo_orden_litros).filter(modelo_orden_litros.c.usuario_id == current_user).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Promedio Por Razas: {e}')
        raise
    finally:
        db.close()
    return itemsLeche




def animales_no_ordeno(session:Session,current_user):
  try:
    # join, consulta y conteo de animales vivos que no son ordenados
    vacas_no_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'No').count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(vacas_no_ordeno=vacas_no_ordeno))

    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_no_ordeno: {e}')
      raise
  finally:
      session.close()
  return vacas_no_ordeno


@Produccion_Leche.get("/Calcular_porcentaje_ordeno")
async def porcentaje_ordeno(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        animales_no_ordeno(session=db,current_user=current_user)
        # consulta de animales ordenados y no ordenados
        ordeno, no_ordeno = db.query \
            (modelo_indicadores.c.vacas_en_ordeno, modelo_indicadores.c.vacas_no_ordeno).first()
        if ordeno == 0 and no_ordeno == 0 or ordeno is None and no_ordeno is None:
            vacas_ordeno_porcentaje = 0
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))
            logger.info(f'Funcion porcentaje_ordeno {vacas_ordeno_porcentaje} ')
            db.commit()
        elif ordeno is None or no_ordeno is None:
            vacas_ordeno_porcentaje = 0
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))

            db.commit()
        else:
            # porcentaje de vacas en ordeno
            vacas_ordeno_porcentaje = (ordeno / (no_ordeno + ordeno)) * 100
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))

            db.commit()
    except Exception as e:
        logger.error(f'Error Funcion porcentaje_ordeno: {e}')
        raise
    finally:
        db.close()
    return vacas_ordeno_porcentaje


@Produccion_Leche.get("/Calcular_vacas_prenadas_porcentaje")
async def vacas_prenadas_porcentaje(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de vacas prenadas y vacas vacias en la base de datos
    prenadas, vacias = db.query(modelo_indicadores.c.vacas_prenadas, modelo_indicadores.c.vacas_vacias).first()
    # calculo del total de animales
    if prenadas is None or vacias is None:
        vacas_estado_pren =0
        # actualizacion de campos
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vacas_prenadas_porcentaje=vacas_estado_pren))
    elif prenadas==0:
        vacas_estado_pren = 0
        # actualizacion de campos
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vacas_prenadas_porcentaje=vacas_estado_pren))
    else:
        # calculo procentaje de vacas prenadas
        totales = prenadas + vacias
        vacas_estado_pren = (prenadas / totales) * 100
        # actualizacion de campos
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vacas_prenadas_porcentaje=vacas_estado_pren))


    db.commit()
  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas_porcentaje: {e}')
      raise
  finally:
      db.close()
  return vacas_estado_pren


@Produccion_Leche.get("/Calcular_animales_ordeno")
async def animales_en_ordeno(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
 try:
    # join, consulta y conteo de animales vivos que son ordenados
    vacas_ordeno = db.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'Si',modelo_leche.c.usuario_id == current_user).count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(vacas_en_ordeno=vacas_ordeno))

    db.commit()
 except Exception as e:
     logger.error(f'Error Funcion animales_en_ordeno: {e}')
     raise
 finally:
     db.close()
 return vacas_ordeno





@Produccion_Leche.get("/Calcular_porcentaje_ordeno")
async def porcentaje_ordeno_calcular(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        animales_no_ordeno(session=db)
        # consulta de animales ordenados y no ordenados
        ordeno, no_ordeno = db.query \
            (modelo_indicadores.c.vacas_en_ordeno, modelo_indicadores.c.vacas_no_ordeno).first()
        if ordeno == 0 and no_ordeno == 0 or ordeno is None and no_ordeno is None:
            vacas_ordeno_porcentaje = 0
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))
            logger.info(f'Funcion porcentaje_ordeno {vacas_ordeno_porcentaje} ')
            db.commit()
        elif ordeno is None or no_ordeno is None:
            vacas_ordeno_porcentaje = 0
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))

            db.commit()
        else:
            # porcentaje de vacas en ordeno
            vacas_ordeno_porcentaje = (ordeno / (no_ordeno + ordeno)) * 100
            # actualizacion de campos
            db.execute(update(modelo_indicadores).
                            where(modelo_indicadores.c.id_indicadores == current_user).
                            values(porcentaje_ordeno=vacas_ordeno_porcentaje))

            db.commit()
    except Exception as e:
        logger.error(f'Error Funcion porcentaje_ordeno: {e}')
        raise
    finally:
        db.close()
    return vacas_ordeno_porcentaje

@Produccion_Leche.get("/Calcular_vacas_vacias")
async def vacas_vacias(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # join de tabla bovinos y tabla leche mediante id_bovino \
        # filtrado y conteo animales con datos prenez Vacia que se encuentren vivos
        consulta_vacias = db.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
            filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Vacia',modelo_leche.c.usuario_id == current_user).count()
        # actualizacion del campo
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vacas_vacias=consulta_vacias))

        db.commit()

    except Exception as e:
        logger.error(f'Error al Calcular Vacas Vacias: {e}')
        raise
    finally:
        db.close()

    return consulta_vacias


@Produccion_Leche.get("/Calcular_vacas_prenadas")
async def vacas_prenadas_calcular(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # join de tabla bovinos y tabla leche mediante id_bovino \
    # filtrado y conteo animales con datos prenez Prenada que se encuentren vivos

    """
    
    
    """
    consulta_prenadas = db.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Prenada',modelo_leche.c.usuario_id==current_user).count()
    # actualizacion del campo
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(vacas_prenadas=consulta_prenadas))

    db.commit()

    return consulta_prenadas


  except Exception as e:
      logger.error(f'Error Funcion vacas_prenadas: {e}')
      raise
  finally:
      db.close()






"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""


@Produccion_Leche.post(
    "/crear_prod_leche/{id_bovino}/{datos_prenez}/{ordeno}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdLeche( id_bovino: str,
                   datos_prenez: str, ordeno: str,proposito:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db)

    try:

        consulta = db.execute(
            modelo_leche.select().where(
                modelo_leche.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresopleche = modelo_leche.insert().values(id_bovino=id_bovino,
                                                          datos_prenez=datos_prenez,
                                                         ordeno=ordeno, proposito=proposito,usuario_id=current_user)

            db.execute(ingresopleche)
            db.commit()
        else:

            db.execute(modelo_leche.update().where(modelo_leche.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino,
                 datos_prenez=datos_prenez,
                ordeno=ordeno, proposito=proposito))
            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Leche: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)





""" Librerias """




"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""


def Edad_Primer_Parto(session:Session):
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
        if fecha_primer_parto is None:
            pass
        else:
            # calculo de la edad al primer parto
            Edad_primer_parto = (fecha_primer_parto.year - fecha_nacimiento.year) * 12 + \
                                fecha_primer_parto.month - fecha_nacimiento.month
            # actualizacion del campo
            session.execute(modelo_leche.update().values(edad_primer_parto=Edad_primer_parto).where(
                modelo_leche.columns.id_bovino == id))

            session.commit()
  except Exception as e:
    logger.error(f'Error Funcion Edad_Primer_Parto: {e}')
    raise
  finally:
      session.close()

"""
esta funcion recibe como parametro la fecha del primer parto y
hace uso de la lidbreria datatime ( timedelta),primero convierte 
la fecha del primer parto a tipo fecha y luego toma este valor
y lo suma con el tiempo util (84 meses) para determinar la fecha
en que dicho animal dejara de ser productivo, posteriormente tambien
devolvera el tiempo restante para llegar a esa fecha mediante la resta
del tiempo actual
"""



def Edad_Sacrificio_Lecheras(condb:Session):
  try:
    # consulta de la fecha de primer parto
    Consulta_P1 = condb.execute(modelo_leche.select()).fetchall()
    # Recorre los campos de la consulta
    for i in Consulta_P1:
        # Toma el ID del bovino para calcular la edad de vida util
        id = i[1]
        # Toma la fecha de primer parto del animal en este caso es el campo 2
        fecha_Parto_1 = i[2]
        if fecha_Parto_1 is None:
            pass
        else:
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



def Dias_Abiertos(condb=Session):
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

def EliminarDuplicadosLeche(condb:Session):
    itemsLeche = condb.execute(modelo_leche.select()).all()



    for ileche in itemsLeche:
        propositoleche = ileche[7]

        idleche = ileche[0]

        if propositoleche == 'Levante':
            condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))

            condb.commit()

        elif propositoleche == 'Ceba':
            condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))
            condb.commit()


"""esta funcion calcula el porcentaje de vacas que se encuentran preñadas"""

