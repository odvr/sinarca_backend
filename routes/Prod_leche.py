'''
Librerias requeridas
'''
from datetime import  datetime
import logging
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.functions import current_user
from Lib.Lib_Intervalo_Partos import intervalo_partos
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.Registro_partos import registro_partos_animales
from Lib.clasificacion_ganado_leche import tipo_ganado_leche
from Lib.dias_abiertos import dias_abiertos
from Lib.funcion_litros_leche import promedio_litros_leche
from Lib.funcion_litros_por_raza import litros_por_raza
from typing import Optional,List
from Lib.palpaciones import palpaciones
import json
# # importa la conexion de la base de datos
from config.db import  get_session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_leche, modelo_bovinos_inventario, \
    modelo_indicadores, modelo_orden_litros, modelo_dias_abiertos, modelo_produccion_general_leche
from fastapi import  status,  APIRouter, Response,Form
from datetime import date,  timedelta
from routes.rutas_bovinos import get_current_user
from sqlalchemy import update
from schemas.schemas_bovinos import esquema_produccion_leche, esquema_orden_litros, Esquema_Usuario, \
    esquema_dias_abiertos
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



@Produccion_Leche.get("/listar_bovino_prodLeche/{id_bovino}",response_model=esquema_produccion_leche,tags=["Produccion Leche"] )
async def id_inventario_bovino_leche(id_bovino: str,db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        # Consultar los datos de producción de leche del bovino especificado
        promedio_litros_leche(session=db, current_user=current_user)
        consulta = db.execute(
            modelo_leche.select().where(modelo_leche.columns.id_bovino == id_bovino)).first()
        # Cerrar la sesión
        db.close()
        if consulta is None:
            raise HTTPException(status_code=404, detail="Bovino no encontrado")
        else:
            return consulta

    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Leche: {e}')
        raise
    finally:
        db.close()
    # condb.commit()



@Produccion_Leche.get("/listar_prod_leche" , response_model=list[esquema_produccion_leche],tags=["Produccion Leche"])
async def inventario_prod_leche(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        itemsLeche = db.query(modelo_leche).filter(modelo_leche.c.usuario_id == current_user).all()
        "Librerias Requeridas"
        registro_partos_animales(session=db,current_user=current_user)



        tipo_ganado_leche(session=db, current_user=current_user)

        EliminarDuplicadosLeche(condb=db,current_user=current_user)

        crud.crear_indicadores.Cargar_Indicadores_Gestion(db=db,current_user=current_user)
        #itemsLeche = db.query(modelo_leche).all()
        return itemsLeche

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Leche: {e}')
        raise
    finally:
        db.close()





"""
Promedio Por Razas
"""


@Produccion_Leche.get("/LitrosPorRaza" , response_model=list[esquema_orden_litros])
async def inventario_prod_leche(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        promedio_litros_leche(session=db, current_user=current_user)

        litros_por_raza(session=db,current_user=current_user)

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
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_leche.columns.tipo_ganado != "Hembra de levante",
               modelo_leche.c.ordeno == 'No',
               modelo_bovinos_inventario.columns.usuario_id==current_user).count()
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
        animales_no_ordeno(session=db, current_user=current_user)
        porcentaje = db.query(modelo_indicadores.c.porcentaje_ordeno).filter(
            modelo_indicadores.c.id_indicadores == current_user).first()

        # Retorna directamente el valor de porcentaje_ordeno
        if porcentaje:
            return porcentaje.porcentaje_ordeno
        else:
            return None

    except Exception as e:
        logger.error(f'Error Funcion porcentaje_ordeno: {e}')
        raise
    finally:
        db.close()



@Produccion_Leche.get("/Calcular_vacas_prenadas_porcentaje")
async def vacas_prenadas_porcentaje(db: Session = Depends(get_database_session),
                                    current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # Consulta de vacas prenadas y vacas vacías en la base de datos
        Edad_Sacrificio_Lecheras(condb=db, current_user=current_user)
        vacas_prenadas_porcentaje = db.query(modelo_indicadores.c.vacas_prenadas_porcentaje). \
            filter(modelo_indicadores.c.id_indicadores == current_user).first()

        # Verificar que el resultado no sea None
        if vacas_prenadas_porcentaje is None:
            return 0

        # Retornar el porcentaje de vacas prenadas como un valor simple
        return vacas_prenadas_porcentaje[0] if vacas_prenadas_porcentaje else 0

    except Exception as e:
        logger.error(f'Error Funcion vacas_prenadas_porcentaje: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()



@Produccion_Leche.get("/Calcular_animales_ordeno")
async def animales_en_ordeno(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        calcular_animales_ordeno = db.query(modelo_indicadores.c.vacas_en_ordeno).filter(
            modelo_indicadores.c.id_indicadores == current_user).first()

        # Retorna directamente el valor de vacas_en_ordeno
        if calcular_animales_ordeno:
            return calcular_animales_ordeno.vacas_en_ordeno
        else:
            return None

    except Exception as e:
        logger.error(f'Error Funcion animales_en_ordeno: {e}')
        raise
    finally:
        db.close()






@Produccion_Leche.get("/Calcular_porcentaje_ordeno")
async def vacas_prenadas_porcentaje(db: Session = Depends(get_database_session),
                                    current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        intervalo_partos(session=db, current_user=current_user)
        # Consulta de vacas prenadas y vacas vacías en la base de datos
        vacas_prenadas_porcentaje = db.query(modelo_indicadores.c.vacas_prenadas_porcentaje). \
            filter(modelo_indicadores.c.id_indicadores == current_user).first()

        # Verificar que el resultado no sea None
        if vacas_prenadas_porcentaje is None:
            return {"vacas_prenadas_porcentaje": 0}

        # Convertir el resultado a un diccionario si es necesario
        if isinstance(vacas_prenadas_porcentaje, dict):
            result = vacas_prenadas_porcentaje
        else:
            result = {"vacas_prenadas_porcentaje": vacas_prenadas_porcentaje[0]}

        return jsonable_encoder(result)

    except Exception as e:
        logger.error(f'Error Funcion vacas_prenadas_porcentaje: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()

@Produccion_Leche.get("/Calcular_vacas_vacias")
async def vacas_vacias(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        Edad_Primer_Parto(session=db, current_user=current_user)
        vacas_vacias = db.query(modelo_indicadores.c.vacas_vacias).filter(
            modelo_indicadores.c.id_indicadores == current_user).first()

        # Retorna directamente el valor de vacas_vacias
        if vacas_vacias:
            return vacas_vacias.vacas_vacias
        else:
            return None

    except Exception as e:
        logger.error(f'Error al Calcular Vacas Vacias: {e}')
        raise
    finally:
        db.close()



@Produccion_Leche.get("/Calcular_vacas_prenadas")
async def vacas_prenadas_calcular(db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta_prenadas = db.query(modelo_indicadores.c.vacas_prenadas).filter(
            modelo_indicadores.c.id_indicadores == current_user).first()

        # Retorna directamente el valor de vacas_prenadas
        if consulta_prenadas:
            return consulta_prenadas.vacas_prenadas
        else:
            return None

    except Exception as e:
        logger.error(f'Error al Calcular Vacas Prenadas: {e}')
        raise
    finally:
        db.close()


"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""


@Produccion_Leche.post(
    "/crear_prod_leche/{id_bovino}/{ordeno}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdLeche( id_bovino: str,
                   ordeno: str,proposito:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db,current_user=current_user)

    try:

        consulta = db.execute(
            modelo_leche.select().where(
                modelo_leche.columns.id_bovino == id_bovino)).first()
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)

        if consulta is None:
            ingresopleche = modelo_leche.insert().values(id_bovino=id_bovino,

                                                         ordeno=ordeno, proposito=proposito,usuario_id=current_user,nombre_bovino=nombre_bovino)

            db.execute(ingresopleche)
            db.commit()
        else:

            db.execute(modelo_leche.update().where(modelo_leche.c.id_bovino == id_bovino).values(
                id_bovino=id_bovino,

                ordeno=ordeno, proposito=proposito))
            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Leche: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)








@Produccion_Leche.get("/listar_Historial_Dias_Abiertos/{id_bovino}",response_model=list[esquema_dias_abiertos])
async def Listar_Historial_Dias_Abiertos(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        dias_abiertos(session=db, current_user=current_user)
        consulta = db.execute(
            modelo_dias_abiertos.select().where(modelo_dias_abiertos.columns.id_bovino == id_bovino)).all()
        palpaciones(session=db, current_user=current_user)


    except Exception as e:
        logger.error(f'Error al obtener sinventario de Dias Abiertos: {e}')
        raise
    finally:
        db.close()
    return consulta






""" Librerias """




"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""


def Edad_Primer_Parto(session:Session,current_user):
  try:
    # join de las tablas de leche y bovinos con los campos requeridos
    consulta_global = session.query(modelo_bovinos_inventario.c.id_bovino,
                      modelo_bovinos_inventario.c.fecha_nacimiento, modelo_leche.c.fecha_primer_parto). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).where(
                    modelo_bovinos_inventario.columns.usuario_id==current_user).all()
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



def Edad_Sacrificio_Lecheras(condb:Session,current_user):
  try:
    # consulta de la fecha de primer parto
    Consulta_P1 = condb.execute(modelo_leche.select().where(
                    modelo_leche.columns.usuario_id==current_user)).fetchall()
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
    Consulta_fechas = condb.execute(modelo_leche.select().where(
                    modelo_leche.columns.usuario_id==current_user)).fetchall()
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

def EliminarDuplicadosLeche(condb:Session,current_user):
    itemsLeche = condb.execute(modelo_leche.select().where(
                    modelo_leche.columns.usuario_id==current_user)).all()



    for ileche in itemsLeche:
        propositoleche = ileche[7]

        idleche = ileche[0]

        if propositoleche == 'Levante':
            condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))

            condb.commit()

        elif propositoleche == 'Ceba':
            condb.execute(modelo_leche.delete().where(modelo_leche.c.id_leche == idleche))
            condb.commit()





@Produccion_Leche.post("/agregar_litros_diarios_leche_general", status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearFactura(
    leche: Optional[List[str]] = Form(None),
     db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user)
):

    """
    La Siguiente API agrega la cantidad de leche en el inventario de Producción de Leche General
    :param leche:
    :param db:
    :param current_user:
    :return:
    """

    try:

        fecha_actual = datetime.now()
        for listros_leche in leche:
            ListrosLeche = json.loads(listros_leche)  # Deserializa la cadena JSON
            leche = ListrosLeche['cantidadLitros']  # Accede al id_bovino
            fecha_ordeno = ListrosLeche['fecha']
            precio_venta = ListrosLeche['precio_venta']  # Accede al peso
            id_factura_asociada = ListrosLeche['id_factura']  # Accede al peso

            ingreso_tabla_general_leche = modelo_produccion_general_leche.insert().values(leche=leche,
                                                                                          fecha_ordeno=fecha_ordeno,
                                                                                          precio_venta=precio_venta,
                                                                                          fecha_registro_sistema=fecha_actual,
                                                                                          factura_id=id_factura_asociada,
                                                                                          usuario_id=current_user)
            db.execute(ingreso_tabla_general_leche)
            db.commit()



    except Exception as e:
        # Ampliar el log de errores para incluir detalles de la excepción y los datos recibidos
        logger.error(f'Error al Crear Factura: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@Produccion_Leche.delete("/eliminar_litro_diario/{id_produccion_leche}")
async def Eliminar_cliente(id_produccion_leche: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        db.execute(modelo_produccion_general_leche.delete().where(modelo_produccion_general_leche.c.id_produccion_leche == id_produccion_leche))
        db.commit()
        return
    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Proveedor: {e}')
        raise
    finally:
        db.close()