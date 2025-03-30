'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import timedelta

from fastapi import APIRouter

from config import db
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones, modelo_historial_partos, modelo_historial_intervalo_partos, modelo_dias_abiertos, \
    modelo_arbol_genealogico, modelo_registro_pajillas
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import crud.crud_bovinos_inventario

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

""""A continuacion se muestran las funciones que determinan los lazos familiares"""

def actualizacion_nombres_Arbol_genealogico(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            filter(modelo_arbol_genealogico.columns.usuario_id == current_user).all()


        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            id_bovino = i.id_bovino
            id_bovino_madre = i.id_bovino_madre
            id_bovino_padre = i.id_bovino_padre
            inseminacion = i.inseminacion


            nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=session, id_bovino=id_bovino, current_user=current_user)
            #actualizacion del campo
            session.execute(modelo_arbol_genealogico.update().values(nombre_bovino=nombre_bovino).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,modelo_arbol_genealogico.columns.usuario_id == current_user))
            session.commit()

            if inseminacion=="Si":
                 pajilla = session.query(modelo_registro_pajillas).where(
                 modelo_registro_pajillas.columns.id_pajillas == id_bovino_padre).\
                 filter(modelo_registro_pajillas.columns.usuario_id == current_user).first()

                 if pajilla==() or pajilla is None:
                     nombre_pajilla= "No registra"
                     session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_padre=nombre_pajilla).filter(
                        modelo_arbol_genealogico.columns.id_bovino == id_bovino))
                     session.commit()

                 elif pajilla==[] or pajilla is None:
                     nombre_pajilla= "No registra"
                     session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_padre=nombre_pajilla).filter(
                        modelo_arbol_genealogico.columns.id_bovino == id_bovino))
                     session.commit()

                 else:
                     try:
                         nombre_pajilla= f'Pajilla {pajilla[1]} ({pajilla[3]})'
                         session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_padre=nombre_pajilla).filter(
                           modelo_arbol_genealogico.columns.id_bovino == id_bovino))
                         session.commit()

                     except Exception as e:
                         logger.error(f'AL CONSULTAR PAJILLAS nombre_pajilla : {e}')
                         raise


            else:
                if id_bovino_padre is None:
                    nombre_bovino_padre="No registra"
                    #actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_padre=nombre_bovino_padre).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,modelo_arbol_genealogico.columns.usuario_id == current_user))
                    session.commit()
                else:
                    nombre_bovino_padre = crud.bovinos_inventario.Buscar_Nombre(db=session, id_bovino=id_bovino_padre, current_user=current_user)
                    #actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_padre=nombre_bovino_padre).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,modelo_arbol_genealogico.columns.usuario_id == current_user))
                    session.commit()


            if id_bovino_madre is None:
                nombre_bovino_madre="No registra"
                #actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_madre=nombre_bovino_madre).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,modelo_arbol_genealogico.columns.usuario_id == current_user))
                session.commit()

            else:
                nombre_bovino_madre = crud.bovinos_inventario.Buscar_Nombre(db=session, id_bovino=id_bovino_madre, current_user=current_user)
                #actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_madre=nombre_bovino_madre).filter(modelo_arbol_genealogico.columns.id_bovino == id_bovino,modelo_arbol_genealogico.columns.usuario_id == current_user))
                session.commit()

    except Exception as e:
        logger.error(f'Error Funcion actualizacion_nombres_Arbol_genealogico: {e}')
        raise


def abuelo_materno(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            filter(modelo_arbol_genealogico.columns.usuario_id == current_user).all()

        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 14
            nombre_bovino = i[14]
            # Toma el nombre de la madre del bovino, este es el campo numero 15
            nombre_bovino_madre = i[15]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]

            # consulta de relaciones familiares
            # consulta padre de la madre(abuelo materno)
            consulta_nombre_abuelo_materno = session.query(modelo_arbol_genealogico).\
                filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_madre).all()
            #si no existe registro del abuelo materno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_nombre_abuelo_materno==[]:

                nombre_bovino_abuelo_materno="No registra"
                #actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuelo_materno=nombre_bovino_abuelo_materno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            #si existe registro del abuelo materno entonces este se actualizara en la base de datos
            else:
                for abuelo_m in consulta_nombre_abuelo_materno:
                    nombre_bovino_abuelo_materno = abuelo_m[16]

                    # actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuelo_materno=nombre_bovino_abuelo_materno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion abuelo_materno: {e}')
        raise


def abuela_materna(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            filter(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 14
            nombre_bovino = i[14]
            # Toma el nombre de la madre del bovino, este es el campo numero 15
            nombre_bovino_madre = i[15]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]
            # consulta de relaciones familiares
            # consulta madre de la madre(abuela materna)
            consulta_nombre_abuela_materna = session.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_madre).all()
            #si no existe registro de abuela materna entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_nombre_abuela_materna==[]:

                nombre_bovino_abuela_materna= "No registra"
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuela_materna=nombre_bovino_abuela_materna).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            #si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                for abuela_m in consulta_nombre_abuela_materna:
                    nombre_bovino_abuela_materna = abuela_m[15]
                    # actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuela_materna=nombre_bovino_abuela_materna).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                    session.commit()
    except Exception as e:
        logger.error(f'Error Funcion abuela_materna: {e}')
        raise



def abuelo_paterno(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            where(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 14
            nombre_bovino = i[14]
            # Toma el nombre de la padre del bovino, este es el campo numero 16
            nombre_bovino_padre = i[16]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]
            # consulta de relaciones familiares
            # consulta padre del padre(abuelo paterno)
            consulta_id_abuelo_paterno = session.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_padre).all()
            # si no existe registro de abuelo paterno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_abuelo_paterno==[]:
                nombre_bovino_abuelo_paterno = "No registra"
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuelo_paterno=nombre_bovino_abuelo_paterno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            # si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                for abuelo_p in consulta_id_abuelo_paterno:
                    nombre_bovino_abuelo_paterno = abuelo_p[16]
                    # actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuelo_paterno=nombre_bovino_abuelo_paterno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                    session.commit()
    except Exception as e:
        logger.error(f'Error Funcion abuelo_paterno: {e}')
        raise


def abuela_paterna(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            where(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 1
            nombre_bovino = i[14]
            # Toma el nombre del padre del bovino, este es el campo numero 16
            nombre_bovino_padre = i[16]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]
            # consulta de relaciones familiares
            # consulta padre del padre(abuelo paterno)
            consulta_nombre_abuela_paterna = session.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_padre).all()
            # si no existe registro de abuela paterna entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_nombre_abuela_paterna==[]:
                nombre_bovino_abuela_paterna = "No registra"
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuela_paterna=nombre_bovino_abuela_paterna).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            # si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                 for abuela_p in consulta_nombre_abuela_paterna:
                       nombre_bovino_abuela_paterna = abuela_p[15]
                       # actualizacion del campo
                       session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_abuela_paterna=nombre_bovino_abuela_paterna).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                       session.commit()

    except Exception as e:
        logger.error(f'Error Funcion abuela_paterna: {e}')
        raise



def bisabuelo_materno(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            where(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 14
            nombre_bovino = i[14]
            # Toma el nombre del abuelo del bovino, este es el campo numero 19
            nombre_bovino_abuelo_materno = i[19]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]
            # consulta de relaciones familiares
            # consulta padre del padre de la madre (bisabuelo materno)
            consulta_nombre_bisabuelo_materno = session.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_abuelo_materno).all()
            # si no existe registro de bisabuelo materno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_nombre_bisabuelo_materno==[]:
                nombre_bovino_bisabuelo_materno = "No Registra"
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(
                    nombre_bovino_bisabuelo_materno=nombre_bovino_bisabuelo_materno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            # si existe registro de bisabuelo materno entonces este se actualizara en la base de datos
            else:
              for abuelo in consulta_nombre_bisabuelo_materno:
                nombre_bovino_bisabuelo_materno = abuelo[16]
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_bisabuelo_materno=nombre_bovino_bisabuelo_materno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()

    except Exception as e:
        logger.error(f'Error Funcion endogamia: {e}')
        raise



def bisabuelo_paterno(session: Session,current_user):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = session.query(modelo_arbol_genealogico).\
            where(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
        for i in consulta_bovinos:
            # Toma el nombre del bovino, este es el campo numero 14
            nombre_bovino = i[14]
            # Toma el nombre del abuelo paterno del bovino, este es el campo numero 17
            nombre_bovino_abuelo_paterno = i[17]
            # Toma el ID del usuario, este es el campo numero 13
            usuario_id = i[13]
            # consulta de relaciones familiares
            # consulta padre del padre del padre (bisabuelo paterno)
            consulta_nombre_bisabuelo_paterno = session.query(modelo_arbol_genealogico).filter(modelo_arbol_genealogico.columns.usuario_id==usuario_id,
                       modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino_abuelo_paterno).all()
            # si no existe registro de bisabuelo paterno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_nombre_bisabuelo_paterno==[] :
                nombre_bovino_bisabuelo_paterno = "No registra"
                # actualizacion del campo
                session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_bisabuelo_paterno=nombre_bovino_bisabuelo_paterno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                session.commit()
            # si existe registro de bisabuelo paterno entonces este se actualizara en la base de datos
            else:
                for i in consulta_nombre_bisabuelo_paterno:
                    nombre_bovino_bisabuelo_paterno = i[16]
                    # actualizacion del campo
                    session.execute(modelo_arbol_genealogico.update().values(nombre_bovino_bisabuelo_paterno=nombre_bovino_bisabuelo_paterno).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre_bovino,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                    session.commit()
    except Exception as e:
        logger.error(f'Error Funcion biabuelo_paterno: {e}')
        raise


"""A continuacion se muestra la funcion de indice de endogamia"""
def endogamia(session: Session,current_user):
 try:

     # para poder realizar esta funcion correctamente, los lazos familiares y sus campos deben estar listos y llenados
     # por lo tanto se debe llamar a las funcies que establecen dichos lazos familiares

     # Realiza la consulta general de la tabla de arbol genealogico
     consulta_bovinos = session.query(modelo_arbol_genealogico).\
            where(modelo_arbol_genealogico.columns.usuario_id == current_user).all()
     # Recorre los campos de la consulta
     for i in consulta_bovinos:
         # Toma el ID del usuario, este es el campo numero 13
         usuario_id = i[13]
         # Toma el nombre del bovino, este es el campo numero 14
         nombre = i[14]
         # Toma el nombre del padre del bovino, este es el campo numero 16
         nombre_padre = i[16]
         # Toma el nombre de la madre del bovino, este es el campo numero 15
         nombre_madre = i[15]
         # Toma el nombre del abuelo paterno del bovino, este es el campo numero 17
         nombre_abuelo_paterno = i[17]
         # Toma el nombre de la abuela paterna del bovino, este es el campo numero 18
         nombre_abuela_paterna = i[18]
         # Toma el nombre del abuelo materno del bovino, este es el campo numero 19
         nombre_abuelo_materno = i[19]
         # Toma el nombre de la abuela materna del bovino, este es el campo numero 20
         nombre_abuela_materna = i[20]
         # Toma el nombre del bisabuelo materno del bovino, este es el campo numero 21
         nombre_bisabuelo_materno = i[21]
         # Toma el nombre del bisabuelo paterno del bovino, este es el campo numero 22
         nombre_bisabuelo_paterno = i[22]
         # bucle if que determina la consanguinidad
         #se debe tener en cuenta los animales con un "no registra" en algun lazo familiar
         #si el padre del bovino es el mismo abuelo materno del bovino entoces sera padre x hija:

         if nombre_padre=="No registra" or nombre_madre=="No registra":
             apareamiento = "No existe información disponible"
             porcentaje_endogamia = None
             notificacion = "No existe información disponible"
             # actualizacion del campo
             session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
             session.commit()

         elif nombre_padre == nombre_abuelo_materno:
            if nombre_abuelo_materno=="No registra":
             apareamiento = "individuos no relacionados"
             porcentaje_endogamia = 0
             notificacion = "ningun grado de consanguinidad"
             # actualizacion del campo
             session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
             session.commit()
            else:
             apareamiento = "padre x hija"
             porcentaje_endogamia = 25
             notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
             # actualizacion del campo
             session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
             session.commit()
         #si la madre del bovino es la abula paterna del bovino entonces sera hijo x madre
         elif nombre_madre == nombre_abuela_paterna:
             if nombre_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
              apareamiento = "hijo x madre"
              porcentaje_endogamia = 25
              notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
              # actualizacion del campo
              session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
              session.commit()
         #si un bovino tiene los mosmos abuelos paternos y maternos entonces sera un cruce de hermanos completos
         elif nombre_abuelo_paterno == nombre_abuelo_materno and nombre_abuela_paterna == nombre_abuela_materna:
             if nombre_abuelo_materno=="No registra" or nombre_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
               apareamiento = "hermanos completos"
               porcentaje_endogamia = 25
               notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
               # actualizacion del campo
               session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
               session.commit()
         #si un bovino tiene el mismo abuelo paterno y materno o la misma abuela paterna y materna entonces es un cruce de medios hermanos
         elif nombre_abuelo_paterno == nombre_abuelo_materno or nombre_abuela_paterna == nombre_abuela_materna:
             if nombre_abuelo_paterno=="No registra" or nombre_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
                 apareamiento = "medio hermano x media hermana"
                 porcentaje_endogamia = 12.5
                 notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()

         #si el padre del bovino es su mismo bisabuelo materno entonces sera un cruce de padre x nieta
         elif nombre_padre == nombre_bisabuelo_materno:
             if nombre_bisabuelo_materno == "No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
                 apareamiento = "padre x nieta"
                 porcentaje_endogamia = 12.5
                 notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()

         #si el abuelo paterno del bovino es su mismo bisabuelo materno entonces sera un cruce de hijo de un padre x nieta de un padre
         elif nombre_abuelo_paterno == nombre_bisabuelo_materno:
             if nombre_abuelo_paterno == "No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
                 apareamiento = "hijo de un padre x nieta de un padre"
                 porcentaje_endogamia = 6.25
                 notificacion = "grado aceptable de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()

         #si el bisabuelo paterno del bovino es su mismo bisabuelo materno entonces sera un cruce de nieto de un padre x nieta del padree
         elif nombre_bisabuelo_paterno == nombre_bisabuelo_materno:
             if nombre_bisabuelo_paterno == "No registra" and nombre_bisabuelo_materno=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()
             else:
                 apareamiento = "nieto de un padre x nieta del padre"
                 porcentaje_endogamia = 3.13
                 notificacion = "grado aceptable de consanguinidad"
                 # actualizacion del campo
                 session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
                 session.commit()

         else:
             apareamiento = "individuos no relacionados"
             porcentaje_endogamia = 0
             notificacion = "ningun grado de consanguinidad"
             # actualizacion del campo
             session.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).filter(modelo_arbol_genealogico.columns.nombre_bovino == nombre,modelo_arbol_genealogico.columns.usuario_id == usuario_id))
             session.commit()
 except Exception as e:
     logger.error(f'Error Funcion endogamia: {e}')
     raise
 finally:
    session.close()