'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_arbol_genealogico, modelo_historial_partos, modelo_historial_intervalo_partos, \
    modelo_palpaciones
from schemas.schemas_bovinos import Esquema_bovinos,User, esquema_produccion_leche, esquema_produccion_levante,TokenSchema,esquema_descarte, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func, null, desc, asc
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta


from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends

oauth2_scheme = OAuth2PasswordBearer("/token")








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
#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#from twilio.rest import Client

"""la siguiente funcion suma e inserta la cantidad de partos de un animal
en la base de datos"""
def conteo_partos(session:Session,current_user):
    try:

        consulta_animales_leche=session.query(modelo_leche.c.id_bovino,modelo_leche.c.cantidad_partos_manual). \
        filter(modelo_leche.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales_leche:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_partos = i.id_bovino
            # Toma la cantidad de partos que el usuario indica
            cantidad_partos_manual = i.cantidad_partos_manual

            # cosulta que determina la cantidad de partos de cada animal
            cantidad_partos = session.query(modelo_historial_partos). \
                    filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos).count()

            # cosulta que determina la cantidad de partos rpovenientes por transferencia de embriones de cada animal
            cantidad_partos_TE = session.query(modelo_embriones_transferencias). \
                    filter(modelo_embriones_transferencias.columns.id_receptora == id_bovino_partos,
                    modelo_embriones_transferencias.columns.resultado_trasnplante == "Exitoso").count()

            if cantidad_partos_manual is None:
                 valor_defecto=None
                 # actualizacion de campos
                 if cantidad_partos == 0 and cantidad_partos_TE==0:
                     # tambien se actualizara los valores de edad primer parto y fecha primer parto
                     valor_defecto = None

                     session.execute(modelo_leche.update().values(edad_primer_parto=valor_defecto,
                                                                  fecha_primer_parto=valor_defecto,
                                                                  fecha_vida_util=valor_defecto).where(
                         modelo_leche.columns.id_bovino == id_bovino_partos))

                     session.commit()

                 else:
                     agregar_partos = modelo_leche.update().values(num_partos=(cantidad_partos+cantidad_partos_TE)). \
                         where(modelo_leche.columns.id_bovino == id_bovino_partos)
                     session.execute(agregar_partos)
                     session.commit()



            else:
                 total_num_partos= cantidad_partos +  cantidad_partos_manual + cantidad_partos_TE

                 # actualizacion de campos
                 agregar_partos = modelo_leche.update().values(num_partos=total_num_partos). \
                                where(modelo_leche.columns.id_bovino == id_bovino_partos)
                 session.execute(agregar_partos)
                 session.commit()


            consulta_fecha_primer_parto = session.query(modelo_historial_partos). \
                filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos). \
                order_by(asc(modelo_historial_partos.columns.fecha_parto)).all()


            if consulta_fecha_primer_parto==[] or consulta_fecha_primer_parto[0][2] is None:
                valor_defecto = None
                session.execute(modelo_leche.update().values(edad_primer_parto=valor_defecto,
                                                             fecha_primer_parto=valor_defecto,
                                                             fecha_vida_util=valor_defecto).where(
                    modelo_leche.columns.id_bovino == id_bovino_partos))

                session.commit()

            else:
                session.execute(modelo_leche.update().values(fecha_primer_parto=consulta_fecha_primer_parto[0][2]).where(
                    modelo_leche.columns.id_bovino == id_bovino_partos))

                session.commit()



        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion conteo_partos: {e}')
        raise
    finally:
        session.close()

"""la siguiente funcion calcula los intervalos de partos de cada animal y los inserta
en la base de datos"""
def intervalo_partos(session:Session,current_user):
    try:
        consulta_animales_partos=list(set(session.query(modelo_historial_partos.c.id_bovino,
        modelo_historial_partos.c.nombre_madre,
        modelo_historial_partos.c.usuario_id). \
            filter(modelo_historial_partos.c.usuario_id==current_user).all()))

        for i in consulta_animales_partos:
            # Toma el ID del bovino
            id_bovino_partos = i[0]
            # Toma el nombre
            nombre_bovino = i[1]
            # Toma el usuario_id
            usuario_id = i[2]

            cantidad_partos = session.query(modelo_historial_partos). \
                    filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos).count()

            if cantidad_partos==0 or cantidad_partos==1:
                intervalo_entre_partos_defecto=None

                session.execute(modelo_leche.update().values(intervalo_entre_partos=intervalo_entre_partos_defecto).where(
                        modelo_leche.columns.id_bovino == id_bovino_partos))

                session.commit()
            else:
                # esta consulta trae en orden segun fecha de parto los partos del animal
                consulta_partos = session.query(modelo_historial_partos). \
                    filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos). \
                    order_by(desc(modelo_historial_partos.columns.fecha_parto)).all()
                # para calcular el intervalo entre partos es necesario un bucle
                # si un animal tiene 3 partos, tendra 2 intervalos, si tiene 5 partos, tendra 4 intervalos
                # por ello la cantidad de intervalos es igual a los partos menos 1
                contador = cantidad_partos - 1
                e = 0
                while (e < contador):
                    # determinacion del intervalo entre partos
                    intervalo_parto = int(((consulta_partos[e][2]).year - (consulta_partos[e + 1][2]).year) * 365 + \
                                          ((consulta_partos[e][2]).month - (consulta_partos[e + 1][2]).month) * 30.4 + \
                                          ((consulta_partos[e][2]).day - (consulta_partos[e + 1][2]).day))
                    # consulta que determina si el intervalo calulado ya existe en la tabla
                    consulta_existencia_intervalo = session.query(modelo_historial_intervalo_partos). \
                        filter(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_partos,
                               modelo_historial_intervalo_partos.columns.fecha_parto1 == consulta_partos[e][2],
                               modelo_historial_intervalo_partos.columns.fecha_parto2 == consulta_partos[e + 1][2]).all()
                    # si el intervalo no existe (consulta vacia) entonces sera creado
                    if consulta_existencia_intervalo == []:
                        ingresointervalo = modelo_historial_intervalo_partos.insert().values(id_bovino=id_bovino_partos,
                                                                                             fecha_parto1=
                                                                                             consulta_partos[e][2],
                                                                                             fecha_parto2=
                                                                                             consulta_partos[e + 1][2],
                                                                                             intervalo=intervalo_parto,
                                                                                             usuario_id=usuario_id,
                                                                                             nombre_bovino=nombre_bovino)

                        session.execute(ingresointervalo)
                        session.commit()
                        e = e + 1
                    # si el intervalo existe entonces se actualizan los datos
                    else:
                        session.execute(modelo_historial_intervalo_partos.update().values(id_bovino=id_bovino_partos,
                                                                                             fecha_parto1=
                                                                                             consulta_partos[e][2],
                                                                                             fecha_parto2=
                                                                                             consulta_partos[e + 1][2],
                                                                                             intervalo=intervalo_parto,
                                                                                             usuario_id=usuario_id,
                                                                                          nombre_bovino=nombre_bovino).where(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_partos).filter(modelo_historial_intervalo_partos.columns.fecha_parto1 == consulta_partos[e][2],modelo_historial_intervalo_partos.columns.fecha_parto2 == consulta_partos[e + 1][2]))
                        session.commit()
                        e = e + 1

        consulta_intervalos_partos=session.query(modelo_historial_intervalo_partos). \
            filter(modelo_historial_intervalo_partos.c.usuario_id==current_user).all()

        for i in consulta_intervalos_partos:
            # Toma el ID del bovino
            id_bovino = i.id_bovino
            # Toma el ID del intervalo
            id_intervalo = i.id_intervalo
            # Toma la fecha 1 de parto
            fecha_parto1 = i.fecha_parto1
            # Toma la fecha 2 de parto
            fecha_parto2 = i.fecha_parto2

            consulta_parto_animal=session.query(modelo_historial_partos). \
            filter(modelo_historial_partos.c.usuario_id==current_user,
            modelo_historial_partos.c.id_bovino==id_bovino,
            modelo_historial_partos.c.fecha_parto==fecha_parto1).first()

            if consulta_parto_animal==[] or consulta_parto_animal is None:
                session.execute(modelo_historial_intervalo_partos.delete().where(modelo_historial_intervalo_partos.c.id_intervalo == id_intervalo))
                session.commit()
            else:
                pass

            consulta_parto_animal2=session.query(modelo_historial_partos). \
            filter(modelo_historial_partos.c.usuario_id==current_user,
            modelo_historial_partos.c.id_bovino==id_bovino,
            modelo_historial_partos.c.fecha_parto==fecha_parto2).first()

            if consulta_parto_animal2==[] or consulta_parto_animal2 is None:
                session.execute(modelo_historial_intervalo_partos.delete().where(modelo_historial_intervalo_partos.c.id_intervalo == id_intervalo))
                session.commit()
            else:
                pass

        session.commit()

    except Exception as e:
        logger.error(f'Error Funcion intervalo_partos: {e}')
        raise
    finally:
        session.close()

"""la siguiente funcion calcula el intervalo de parto promedio de cada animal"""
def promedio_intervalo_partos(session:Session,current_user):
    try:
        # Realiza el join co la tabla de bovinos (solo se veran los id de los bovinos)
        # como la tabla de intervalos de parto puede tener un id repetido mas de una vez, se utiliza el conjunto o set
        # el set no permite elementos repetidos, por lo tanto solo nos dara un listado de id unicos
        consulta_animal_intervalos = set(session.query(modelo_bovinos_inventario.c.id_bovino, modelo_historial_intervalo_partos.c.id_bovino). \
            join(modelo_historial_intervalo_partos,modelo_bovinos_inventario.c.id_bovino == modelo_historial_intervalo_partos.c.id_bovino).
            filter( modelo_bovinos_inventario.c.usuario_id==current_user).all())
        # recorre el bucle
        for i in consulta_animal_intervalos:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_intervalos = i[0]
            #con este id consultamos la sumatoria de los itervalos y su cantidad
            #suma de los intervalos
            consulta_suma_intervalos=session.query(func.sum(modelo_historial_intervalo_partos.columns.intervalo)).\
                filter(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_intervalos).all()
            for i in consulta_suma_intervalos:
                # Toma la suma de los intervalos del animal en este caso es el campo 0
                suma_intervalos = i[0]
                # conteo de los intervalos
                cantidad_intervalos = session.query(modelo_historial_intervalo_partos). \
                    filter(modelo_historial_intervalo_partos.columns.id_bovino == id_bovino_intervalos).count()
                # calculo del promedo de intervalo entre partos
                promedio_intervalo = suma_intervalos / cantidad_intervalos
                # actualizacion del campo
                session.execute(modelo_leche.update().values(intervalo_entre_partos=promedio_intervalo). \
                                where(modelo_leche.columns.id_bovino == id_bovino_intervalos))
                session.commit()
        #el siguiente codigo permite establecer si un animal tiene o no registros de parto
        consulta_id_bovinos_leche = session.query(modelo_leche).all()
        for i in consulta_id_bovinos_leche:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovinos_leche = i[1]
            #consulta que determina si el animal tiene algun registro de parto
            consulta_bovinos_en_modulo_partos = session.query(modelo_historial_partos). \
                filter(modelo_historial_partos.columns.id_bovino == id_bovinos_leche).all()
            #en caso de no tener regisros de parto sera actualizado el valor a 0
            if consulta_bovinos_en_modulo_partos == []:
                valor_defecto_intervalo_partos = None
                session.execute(modelo_leche.update().values(intervalo_entre_partos=valor_defecto_intervalo_partos). \
                                where(modelo_leche.columns.id_bovino == id_bovinos_leche))
                session.commit()
            else:
                pass
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion promedio_intervalo_partos: {e}')
        raise
    finally:
        session.close()



"""la siguiente funcion es una calculadora que determina la fecha aproximada de parto
de un animal en base a su fecha de preñez"""
def fecha_aproximada_parto(session=Session):
  try:
    # join de tablas

    consulta_vacas = session.query(modelo_partos.c.id_parto,modelo_partos.c.id_bovino,modelo_partos.c.fecha_estimada_prenez, modelo_bovinos_inventario.c.edad,
                                     modelo_bovinos_inventario.c.peso, modelo_bovinos_inventario.c.estado). \
        join(modelo_partos,modelo_partos.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    #recorrer los campos
    for i in consulta_vacas:
        # Toma el ID de la monta en este caso es el campo 0
        id_monta = i[0]
        # Toma el ID del bovino en este caso es el campo 1
        id = i[1]
        # Toma la edad del animal en este caso es el campo 2
        fecha_estimada_prenez = i[2]
        # Toma la edad del animal en este caso es el campo 3
        edad = i[3]
        # Toma el peso del animal en este caso es el campo 4
        peso = i[4]
        # Toma el estado del animal en este caso es el campo 5
        estado = i[5]
        #calculo de la fecha aproximada de parto (la gestacion dura paorximadamente 283 dias)
        if estado=="Vivo":
          fecha_estimada_parto = fecha_estimada_prenez + timedelta(283)
        else:
          fecha_estimada_parto = None
        #actualizacion de campos
        session.execute(modelo_partos.update().values(fecha_estimada_parto=fecha_estimada_parto,edad=edad,
                                                      peso=peso). \
                        where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.id_parto==id_monta))

        session.commit()

        #el siguiente codigo permite generar notificaciones
        diferencia=(date.today()-fecha_estimada_prenez).days
        if diferencia <45:
            notificacion = None
            session.execute(modelo_partos.update().values(notificacion=notificacion). \
                            where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.id_parto==id_monta))

            session.commit()
        else:
            consulta_animales_palpaciones = session.query(modelo_palpaciones). \
                where(modelo_palpaciones.columns.fecha_palpacion >= (fecha_estimada_prenez)). \
                filter(modelo_palpaciones.columns.id_bovino == id).all()

            if consulta_animales_palpaciones is None or consulta_animales_palpaciones==[]:
                notificacion = f'Han pasado por lo menos 45 dias y no has registrado palpaciones nuevas desde la monta/inseminacion de este animal, seria recomendable que realices una palpacion'
                session.execute(modelo_partos.update().values(notificacion=notificacion). \
                                where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.id_parto==id_monta))

                session.commit()


            else:
                notificacion = None
                session.execute(modelo_partos.update().values(notificacion=notificacion). \
                                where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.id_parto==id_monta))

                session.commit()


  except Exception as e:
      logger.error(f'Error Funcion fecha_aproximada_parto: {e}')
      raise
  finally:
      session.close()