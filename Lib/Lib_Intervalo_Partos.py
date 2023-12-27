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
"""la siguiente funcion calcula los intervalos de partos de cada animal y los inserta
en la base de datos"""
def intervalo_partos(session:Session,current_user):
    try:
        # Realiza el join co la tabla de bovinos (solo se veran los id de los bovinos)
        #como la tabla de historial de partos puede tener un id repetido mas de una vez, se utiliza el conjunto o set
        #el set no permite elementos repetidos, por lo tanto solo nos dara un listado de id unicos
        consulta_animal_partos= set(session.query(modelo_bovinos_inventario.c.id_bovino, modelo_leche.c.id_bovino,
                                                  modelo_bovinos_inventario.c.usuario_id,
                                                  modelo_bovinos_inventario.c.nombre_bovino). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).
            filter( modelo_bovinos_inventario.c.usuario_id==current_user).all())

        # recorre el bucle
        for i in consulta_animal_partos:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_partos = i[0]
            # Toma el ID del usuario, este es el campo numero 2
            usuario_id = i[2]
            # Toma el nombre del bovino, este es el campo numero 3
            nombre_bovino = i[3]
            #la siguiente consulta permte saber si el animal existe en el registro de partos
            consulta_existencia_partos = session.query(modelo_historial_partos). \
                filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos).all()
            #si el animal no existe en el registro de partos significara que tendra un intervalo entre partos
            #de cero
            if consulta_existencia_partos==[]:
                partos_defecto=0
                intervalo_entre_partos_defecto=0
                # actualizacion de campos
                session.execute(modelo_leche.update().values(num_partos=partos_defecto,
                                                             intervalo_entre_partos=intervalo_entre_partos_defecto). \
                                where(modelo_leche.columns.id_bovino == id_bovino_partos))
                session.commit()
                #tambien se actualizara los valores de edad primer parto y fecha primer parto
                valor_defecto = None
                session.execute(modelo_leche.update().values(edad_primer_parto=valor_defecto,
                                                             fecha_primer_parto=valor_defecto,
                                                             fecha_vida_util=valor_defecto).where(
                    modelo_leche.columns.id_bovino == id_bovino_partos))

                session.commit()
            else:
                # cosulta que determina la cantidad de partos de cada animal
                cantidad_partos = session.query(modelo_historial_partos). \
                    filter(modelo_historial_partos.columns.id_bovino == id_bovino_partos).count()
                # actualizacion de campo de numero de partos
                session.execute(modelo_leche.update().values(num_partos=cantidad_partos). \
                                where(modelo_leche.columns.id_bovino == id_bovino_partos))
                session.commit()
                # esta consulta determina cual es el primer parto del bovino
                # para ello ordena las fechas de registro de partos desde las mas antiguas y toma la fecha mas antigua
                consulta_fecha_primer_parto = list(session.execute(modelo_historial_partos.select(). \
                   where(modelo_historial_partos.columns.id_bovino == id_bovino_partos). \
                    order_by(asc(modelo_historial_partos.columns.fecha_parto))).first())
                # actualizacion del campo
                session.execute(modelo_leche.update().values(fecha_primer_parto=consulta_fecha_primer_parto[2]). \
                                where(modelo_leche.columns.id_bovino == id_bovino_partos))
                session.commit()
                # si la cantidad de partos es menor a 1 entonces no existe intervalo entre partos
                if cantidad_partos == 1:
                    intervalo_entre_partos_defecto = 0
                    session.execute(modelo_leche.update().values(intervalo_entre_partos=intervalo_entre_partos_defecto). \
                                    where(modelo_leche.columns.id_bovino == id_bovino_partos))
                    session.commit()
                else:
                    pass
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
                               modelo_historial_intervalo_partos.columns.fecha_parto2 == consulta_partos[e + 1][
                                   2]).all()
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
                # debido a que el usuario puede alterar y eliminar las fechas de partos
                # es necesario eliminar los intervalos que tienen las fechas antes de ser cambiadas
                # Esta consulta permite averiguar todos los intervalos existentes
                consulta_fechas = session.query(modelo_historial_intervalo_partos).all()
                for i in consulta_fechas:
                    # Toma el ID del bovino, este es el campo numero 1
                    id_bovino_fecha = i[1]
                    # Toma la primera fecha de parto, este es el campo numero 2
                    f_parto1 = i[2]
                    # Toma la segunda fecha de parto, este es el campo numero 3
                    f_parto2 = i[3]
                    # consulta en el historial de partos si existe la primera fecha de parto de ese bovino
                    consulta_f1 = session.query(modelo_historial_partos). \
                        where(modelo_historial_partos.c.id_bovino == id_bovino_fecha). \
                        filter(modelo_historial_partos.c.fecha_parto == f_parto1).all()
                    # si no existe esa fecha en el historial de parto siginifica que fue cambiada o eliminada
                    # entonces se debe eliminar el intervalo que contenga la fecha (pues esta trabajando con una fecha vieja)
                    if consulta_f1 == []:
                        session.execute(modelo_historial_intervalo_partos.delete(). \
                                        where(modelo_historial_intervalo_partos.c.id_bovino == id_bovino_partos). \
                                        filter(modelo_historial_intervalo_partos.c.fecha_parto1 == f_parto1))
                        session.commit()
                    # en caso de existir no se realizaran cambios
                    else:
                        pass
                    # aplicamos el metodo anterior con la segunda fecha de parto
                    consulta_f2 = session.query(modelo_historial_partos). \
                        where(modelo_historial_partos.c.id_bovino == id_bovino_fecha). \
                        filter(modelo_historial_partos.c.fecha_parto == f_parto2).all()
                    if consulta_f2 == []:
                        session.execute(modelo_historial_intervalo_partos.delete(). \
                                        where(modelo_historial_intervalo_partos.c.id_bovino == id_bovino_partos). \
                                        filter(modelo_historial_intervalo_partos.c.fecha_parto2 == f_parto2))
                        session.commit()
                    else:
                        pass
                # el siguiente codigo permite establecer si un animal tiene o no registros de parto
            consulta_id_bovinos_leche = session.query(modelo_leche).all()
            for i in consulta_id_bovinos_leche:
                # Toma el ID del bovino, este es el campo numero 0
                id_bovino_partos_consulta_id_bovinos_leche = i[1]
                # consulta que determina si el animal tiene algun registro de parto
                consulta_bovinos_en_modulo_partos = session.query(modelo_historial_partos). \
                    filter(
                    modelo_historial_partos.columns.id_bovino == id_bovino_partos_consulta_id_bovinos_leche).all()
                # en caso de no tener regisros de parto sera actualizado al valor a 0
                if consulta_bovinos_en_modulo_partos == []:
                    valor_defecto_cantidad_partos = 0
                    session.execute(modelo_leche.update().values(num_partos=valor_defecto_cantidad_partos). \
                                    where(modelo_leche.columns.id_bovino == id_bovino_partos_consulta_id_bovinos_leche))
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
                valor_defecto_intervalo_partos = 0
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
        #calculo de la fecha aproximada de parto (la gestacion dura paorximadamente 283 dias)
        if estado=="Vivo":
          fecha_estimada_parto = fecha_estimada_prenez + timedelta(283)
        else:
          fecha_estimada_parto = None
        #actualizacion de campos
        session.execute(modelo_partos.update().values(fecha_estimada_parto=fecha_estimada_parto,edad=edad,
                                                      peso=peso). \
                        where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.fecha_estimada_prenez==fecha_estimada_prenez))

        session.commit()

        #el siguiente codigo permite generar notificaciones
        diferencia= (datetime.today().year - fecha_estimada_prenez.year) * 12 + (datetime.today().month - fecha_estimada_prenez.month) *30.4 + (datetime.today().day-fecha_estimada_prenez.day)
        if diferencia <45:
            notificacion = None
            session.execute(modelo_partos.update().values(notificacion=notificacion). \
                            where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.fecha_estimada_prenez==fecha_estimada_prenez))

            session.commit()
        else:
            consulta_animales_palpaciones = session.query(modelo_palpaciones). \
                where(modelo_palpaciones.columns.fecha_palpacion >= (fecha_estimada_prenez)). \
                filter(modelo_palpaciones.columns.id_bovino == id).all()

            if consulta_animales_palpaciones is None or consulta_animales_palpaciones==[]:
                notificacion = f'Han pasado por lo menos 45 dias y no has registrado palpaciones nuevas desde la monta/inseminacion de este animal, seria recomendable que realices una palpacion'
                session.execute(modelo_partos.update().values(notificacion=notificacion). \
                                where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.fecha_estimada_prenez==fecha_estimada_prenez))

                session.commit()


            else:
                notificacion = None
                session.execute(modelo_partos.update().values(notificacion=notificacion). \
                                where(modelo_partos.columns.id_bovino == id).filter(modelo_partos.columns.fecha_estimada_prenez==fecha_estimada_prenez))

                session.commit()


  except Exception as e:
      logger.error(f'Error Funcion fecha_aproximada_parto: {e}')
      raise
  finally:
      session.close()