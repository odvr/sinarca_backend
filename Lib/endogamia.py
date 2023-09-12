'''
Librerias requeridas

@autor : odvr

'''

import logging

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_arbol_genealogico

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


"""A continuacion se muestran las funciones que determinan los lazos familiares"""
def abuelo_materno(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 1
            id = i[1]
            # Toma el ID de la madre del bovino, este es el campo numero 2
            id_madre = i[2]
            # consulta de relaciones familiares
            # consulta padre de la madre(abuelo materno)
            consulta_id_abuelo_materno = condb.execute(modelo_arbol_genealogico.select().
                                            where(modelo_arbol_genealogico.columns.id_bovino == id_madre)).fetchall()
            #si no existe registro del abuelo materno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_abuelo_materno==[]:
                id_abuelo_materno = "No registra"
                #actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(abuelo_materno=id_abuelo_materno).where(
                    modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            #si existe registro del abuelo materno entonces este se actualizara en la base de datos
            else:
                for abuelo_m in consulta_id_abuelo_materno:
                    id_abuelo_materno = abuelo_m[3]
                    # actualizacion del campo
                    condb.execute(modelo_arbol_genealogico.update().values(abuelo_materno=id_abuelo_materno).where(
                            modelo_arbol_genealogico.columns.id_bovino == id))
                    condb.commit()
    except Exception as e:
        logger.error(f'Error Funcion abuelo_materno: {e}')
        raise
    finally:
        condb.close()


def abuela_materna(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 1
            id = i[1]
            # Toma el ID de la madre del bovino, este es el campo numero 2
            id_madre = i[2]
            # consulta de relaciones familiares
            # consulta madre de la madre(abuela materna)
            consulta_id_abuela_materna = condb.execute(modelo_arbol_genealogico.select().
                                                where(modelo_arbol_genealogico.columns.id_bovino == id_madre)).fetchall()
            #si no existe registro de abuela materna entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_abuela_materna==[]:
                id_abuela_materna = "No registra"
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(abuela_materna=id_abuela_materna).where(
                    modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            #si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                for abuela_m in consulta_id_abuela_materna:
                    id_abuela_materna = abuela_m[2]
                    # actualizacion del campo
                    condb.execute(modelo_arbol_genealogico.update().values(abuela_materna=id_abuela_materna).where(
                        modelo_arbol_genealogico.columns.id_bovino == id))
                    condb.commit()
    except Exception as e:
        logger.error(f'Error Funcion abuela_materna: {e}')
        raise
    finally:
        condb.close()

def abuelo_paterno(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 1
            id = i[1]
            # Toma el ID del padre del bovino, este es el campo numero 3
            id_padre = i[3]
            # consulta de relaciones familiares
            # consulta padre del padre(abuelo paterno)
            consulta_id_abuelo_paterno = condb.execute(modelo_arbol_genealogico.select().
                                                where(modelo_arbol_genealogico.columns.id_bovino == id_padre)).fetchall()
            # si no existe registro de abuelo paterno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_abuelo_paterno==[]:
                id_padre_de_id_padre = "No registra"
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(abuelo_paterno=id_padre_de_id_padre).where(
                    modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            # si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                for abuelo_p in consulta_id_abuelo_paterno:
                    id_padre_de_id_padre = abuelo_p[3]
                    # actualizacion del campo
                    condb.execute(modelo_arbol_genealogico.update().values(abuelo_paterno=id_padre_de_id_padre).where(
                        modelo_arbol_genealogico.columns.id_bovino == id))
                    condb.commit()
    except Exception as e:
        logger.error(f'Error Funcion abuelo_paterno: {e}')
        raise
    finally:
        condb.close()


def abuela_paterna(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 0
            id = i[1]
            # Toma el ID del padre del bovino, este es el campo numero 3
            id_padre = i[3]
            # consulta de relaciones familiares
             # consulta padre del padre(abuelo paterno)
            consulta_id_abuela_paterna = condb.execute(modelo_arbol_genealogico.select().
                 where(modelo_arbol_genealogico.columns.id_bovino == id_padre)).fetchall()
            # si no existe registro de abuela paterna entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_abuela_paterna==[]:
                id_abuela_paterna = "No registra"
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(abuela_paterna=id_abuela_paterna).where(
                    modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            # si existe registro de abuela materna entonces este se actualizara en la base de datos
            else:
                 for abuela_p in consulta_id_abuela_paterna:
                       id_abuela_paterna = abuela_p[2]
                       # actualizacion del campo
                       condb.execute(modelo_arbol_genealogico.update().values(abuela_paterna=id_abuela_paterna).where(
                           modelo_arbol_genealogico.columns.id_bovino == id))
                       condb.commit()

    except Exception as e:
        logger.error(f'Error Funcion abuela_paterna: {e}')
        raise
    finally:
        condb.close()

def bisabuelo_materno(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 0
            id = i[1]
            # Toma el ID del abuelo paterno del bovino, este es el campo numero 6
            id_abuelo_paterno = i[6]
            # consulta de relaciones familiares
            # consulta padre del padre de la madre (bisabuelo materno)
            consulta_id_bisabuelo_materno = condb.execute(modelo_arbol_genealogico.select().
                where(modelo_arbol_genealogico.columns.id_bovino == id_abuelo_paterno)).fetchall()
            # si no existe registro de bisabuelo materno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_bisabuelo_materno==[]:
                id_bisabuelo_materno = "No Registra"
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(
                    bisabuelo_materno=id_bisabuelo_materno).where(
                    modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            # si existe registro de bisabuelo materno entonces este se actualizara en la base de datos
            else:
              for abuelo in consulta_id_bisabuelo_materno:
                id_bisabuelo_materno = abuelo[3]
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(
                        bisabuelo_materno=id_bisabuelo_materno).where(
                        modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()

    except Exception as e:
        logger.error(f'Error Funcion endogamia: {e}')
        raise
    finally:
        condb.close()

def biabuelo_paterno(condb: Session):
    try:
        # Realiza la consulta general de la tabla de arbol genealogico
        consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
        # Recorre los campos de la consulta
        for i in consulta_bovinos:
            # Toma el ID del bovino, este es el campo numero 0
            id = i[1]
            # Toma el ID del abuelo paterno del bovino, este es el campo numero 3
            id_abuelo_paterno = i[4]
            # consulta de relaciones familiares
            # consulta padre del padre del padre (bisabuelo paterno)
            consulta_id_bisabuelo_paterno = condb.execute(modelo_arbol_genealogico.select().
                where(modelo_arbol_genealogico.columns.id_bovino == id_abuelo_paterno)).fetchall()
            # si no existe registro de bisabuelo paterno entonces sera una consulta vacia (se asignara un no registro por defecto)
            if consulta_id_bisabuelo_paterno==[] :
                id_bisabuelo_paterno = "No registra"
                # actualizacion del campo
                condb.execute(modelo_arbol_genealogico.update().values(bisabuelo_paterno=id_bisabuelo_paterno).where(
                        modelo_arbol_genealogico.columns.id_bovino == id))
                condb.commit()
            # si existe registro de bisabuelo paterno entonces este se actualizara en la base de datos
            else:
                for i in consulta_id_bisabuelo_paterno:
                    id_bisabuelo_paterno = i[3]
                    # actualizacion del campo
                    condb.execute(modelo_arbol_genealogico.update().values(
                        bisabuelo_paterno=id_bisabuelo_paterno).where(
                        modelo_arbol_genealogico.columns.id_bovino == id))
                    condb.commit()
    except Exception as e:
        logger.error(f'Error Funcion endogamia: {e}')
        raise
    finally:
        condb.close()


"""A continuacion se muestra la funcion de indice de endogamia"""
def endogamia(condb: Session):
 #para poder realizar esta funcion correctamente, los lazos familiares y sus campos deben estar listos y llenados
 #por lo tanto se debe llamar a las funcies que establecen dichos lazos familiares
 abuelo_materno(condb=condb)
 abuela_materna(condb=condb)
 abuelo_paterno(condb=condb)
 abuela_paterna(condb=condb)
 bisabuelo_materno(condb=condb)
 biabuelo_paterno(condb=condb)
 try:
     # Realiza la consulta general de la tabla de arbol genealogico
     consulta_bovinos = condb.execute(modelo_arbol_genealogico.select()).fetchall()
     # Recorre los campos de la consulta
     for i in consulta_bovinos:
         # Toma el ID del bovino, este es el campo numero 1
         id = i[1]
         # Toma el ID del padre del bovino, este es el campo numero 3
         id_padre = i[3]
         # Toma el ID de la madre del bovino, este es el campo numero 2
         id_madre = i[2]
         # Toma el ID del abuelo paterno del bovino, este es el campo numero 4
         id_abuelo_paterno = i[4]
         # Toma el ID de la abuela paterna del bovino, este es el campo numero 5
         id_abuela_paterna = i[5]
         # Toma el ID del abuelo materno del bovino, este es el campo numero 6
         id_abuelo_materno = i[6]
         # Toma el ID de la abuela materna del bovino, este es el campo numero 7
         id_abuela_materna = i[7]
         # Toma el ID del bisabuelo materno del bovino, este es el campo numero 8
         id_bisabuelo_materno = i[8]
         # Toma el ID del bisabuelo paterno del bovino, este es el campo numero 9
         id_bisabuelo_paterno = i[9]
         # bucle if que determina la consanguinidad
         #se debe tener en cuenta los animales con un "no registra" en algun lazo familiar
         #si el padre del bovino es el mismo abuelo materno del bovino entoces sera padre x hija:
         if id_padre == id_abuelo_materno:
            if id_abuelo_materno=="No registra":
             apareamiento = "individuos no relacionados"
             porcentaje_endogamia = 0
             notificacion = "ningun grado de consanguinidad"
             # actualizacion del campo
             condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).where(
                 modelo_arbol_genealogico.columns.id_bovino == id))
             condb.commit()
            else:
             apareamiento = "padre x hija"
             porcentaje_endogamia = 25
             notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
             # actualizacion del campo
             condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).where(
                 modelo_arbol_genealogico.columns.id_bovino == id))
             condb.commit()
         #si la madre del bovino es la abula paterna del bovino entonces sera hijo x madre
         elif id_madre == id_abuela_paterna:
             if id_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
              apareamiento = "hijo x madre"
              porcentaje_endogamia = 25
              notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
              # actualizacion del campo
              condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).where(
                 modelo_arbol_genealogico.columns.id_bovino == id))
              condb.commit()
         #si un bovino tiene los mosmos abuelos paternos y maternos entonces sera un cruce de hermanos completos
         elif id_abuelo_paterno == id_abuelo_materno and id_abuela_paterna == id_abuela_materna:
             if id_abuelo_materno=="No registra" or id_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
               apareamiento = "hermanos completos"
               porcentaje_endogamia = 25
               notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
               # actualizacion del campo
               condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).where(
                 modelo_arbol_genealogico.columns.id_bovino == id))
               condb.commit()
         #si un bovino tiene el mismo abuelo paterno y materno o la misma abuela paterna y materna entonces es un cruce de medios hermanos
         elif id_abuelo_paterno == id_abuelo_materno or id_abuela_paterna == id_abuela_materna:
             if id_abuelo_paterno=="No registra" or id_abuela_paterna=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
                 apareamiento = "medio hermano x media hermana"
                 porcentaje_endogamia = 12.5
                 notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()

         #si el padre del bovino es su mismo bisabuelo materno entonces sera un cruce de padre x nieta
         elif id_padre == id_bisabuelo_materno:
             if id_bisabuelo_materno == "No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
                 apareamiento = "padre x nieta"
                 porcentaje_endogamia = 12.5
                 notificacion = "Este individuo tiene un grado demasiado alto de consanguinidad, por favor intenta descartarlo"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()

         #si el abuelo paterno del bovino es su mismo bisabuelo materno entonces sera un cruce de hijo de un padre x nieta de un padre
         elif id_abuelo_paterno == id_bisabuelo_materno:
             if id_abuelo_paterno == "No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
                 apareamiento = "hijo de un padre x nieta de un padre"
                 porcentaje_endogamia = 6.25
                 notificacion = "grado aceptable de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()

         #si el bisabuelo paterno del bovino es su mismo bisabuelo materno entonces sera un cruce de nieto de un padre x nieta del padree
         elif id_bisabuelo_paterno == id_bisabuelo_materno:
             if id_bisabuelo_paterno == "No registra" and id_bisabuelo_materno=="No registra":
                 apareamiento = "individuos no relacionados"
                 porcentaje_endogamia = 0
                 notificacion = "ningun grado de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()
             else:
                 apareamiento = "nieto de un padre x nieta del padre"
                 porcentaje_endogamia = 3.13
                 notificacion = "grado aceptable de consanguinidad"
                 # actualizacion del campo
                 condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                        consanguinidad=porcentaje_endogamia,
                                                                        notificacion=notificacion).where(
                     modelo_arbol_genealogico.columns.id_bovino == id))
                 condb.commit()

         else:
             apareamiento = "individuos no relacionados"
             porcentaje_endogamia = 0
             notificacion = "ningun grado de consanguinidad"
             # actualizacion del campo
             condb.execute(modelo_arbol_genealogico.update().values(tipo_de_apareamiento=apareamiento,
                                                                    consanguinidad=porcentaje_endogamia,
                                                                    notificacion=notificacion).where(
                 modelo_arbol_genealogico.columns.id_bovino == id))
             condb.commit()
 except Exception as e:
     logger.error(f'Error Funcion endogamia: {e}')
     raise
 finally:
    condb.close()