'''
Librerias requeridas

@autor : odvr

'''

import logging

from fastapi import APIRouter
from sqlalchemy import asc
from sqlalchemy.orm import Session

# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_levante, modelo_datos_pesaje, modelo_ceba, \
    modelo_ganancia_historica_peso

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

"""estas funciones calculan la ganancia media diaria de cada animal para animales de levante y ceba
, para ello toma el primer y el ultimo peso registrado jusnto con sus fechas y divide la 
diferencia entre los dias entre esas dos fecha"""

def ganancia_peso_levante(session: Session,current_user):
    try:
        #la siguiente consulta tare los id y los estados de los bovinos en levante
        consulta_animales_levante= session.query(modelo_levante.c.id_bovino,modelo_levante.c.estado).\
            filter(modelo_levante.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales_levante:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino = i[0]
            # Toma el estado del bovino, este es el campo numero 1
            estado = i[1]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas antigua
            consulta_pesos = session.query(modelo_datos_pesaje.columns.peso,
                                           modelo_datos_pesaje.columns.fecha_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino==id_bovino).\
                order_by(asc(modelo_datos_pesaje.columns.fecha_pesaje)).all()

            cantidad=len(consulta_pesos)
            #si un animal no tiene por lo menos 2 registros de peso no se podra calcular la ganancia diaria de peso
            #lo mismo aplicara para animales que no esten vivos
            if estado!="Vivo" or cantidad<=1:
                session.execute(modelo_levante.update().values(ganancia_media_diaria=None). \
                                where(modelo_levante.columns.id_bovino == id_bovino))
                session.commit()
            else:
                # se identifican los pesos iniciales y finales con sus fechas
                peso_inicial = consulta_pesos[0][0]
                fecha_inicial = consulta_pesos[0][1]

                peso_final = consulta_pesos[cantidad - 1][0]
                fecha_final = consulta_pesos[cantidad - 1][1]

                diferencia_fechas=(fecha_final - fecha_inicial).days

                #si la diferencia entre fechas no es mayor a un dia entonces no se podra calcular la ganancia
                if diferencia_fechas<1 or diferencia_fechas==0:
                    session.execute(modelo_levante.update().values(ganancia_media_diaria=None). \
                                    where(modelo_levante.columns.id_bovino == id_bovino))
                    session.commit()
                else:
                    # se calcula la ganacia media diaria de peso por dia
                    ganancia_media_diaria = ((peso_final - peso_inicial) / (((fecha_final - fecha_inicial).days))) * 1000
                    # Actualiacion de campos
                    session.execute(modelo_levante.update().values(ganancia_media_diaria=round(ganancia_media_diaria,2)). \
                                    where(modelo_levante.columns.id_bovino == id_bovino))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion ganancia_peso_levante: {e}')
        raise
    finally:
        session.close()


def ganancia_peso_ceba(session: Session,current_user):
    try:
        #la siguiente consulta tare los id y los estados de los bovinos en ceba
        consulta_animales_ceba= session.query(modelo_ceba.c.id_bovino,modelo_ceba.c.estado).\
            filter(modelo_ceba.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales_ceba:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino = i[0]
            # Toma el estado del bovino, este es el campo numero 1
            estado = i[1]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas antigua
            consulta_pesos = session.query(modelo_datos_pesaje.columns.peso,
                                           modelo_datos_pesaje.columns.fecha_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino==id_bovino).\
                order_by(asc(modelo_datos_pesaje.columns.fecha_pesaje)).all()

            cantidad=len(consulta_pesos)
            #si un animal no tiene por lo menos 2 registros de peso no se podra calcular la ganancia diaria de peso
            #lo mismo aplicara para animales que no esten vivos
            if estado!="Vivo" or cantidad<=1:
                session.execute(modelo_ceba.update().values(ganancia_media_diaria=None). \
                                where(modelo_ceba.columns.id_bovino == id_bovino))
                session.commit()
            else:
                # se identifican los pesos iniciales y finales con sus fechas
                peso_inicial = consulta_pesos[0][0]
                fecha_inicial = consulta_pesos[0][1]

                peso_final = consulta_pesos[cantidad - 1][0]
                fecha_final = consulta_pesos[cantidad - 1][1]

                diferencia_fechas=(fecha_final - fecha_inicial).days

                # si la diferencia entre fechas no es mayor a un dia entonces no se podra calcular la ganancia
                if diferencia_fechas<1 or diferencia_fechas==0:
                    session.execute(modelo_ceba.update().values(ganancia_media_diaria=None). \
                                    where(modelo_ceba.columns.id_bovino == id_bovino))
                    session.commit()
                else:
                    # se calcula la ganacia media diaria de peso por dia
                    ganancia_media_diaria = ((peso_final - peso_inicial) / (((fecha_final - fecha_inicial).days))) * 1000
                    # Actualiacion de campos
                    session.execute(modelo_ceba.update().values(ganancia_media_diaria=round(ganancia_media_diaria,2)). \
                                    where(modelo_ceba.columns.id_bovino == id_bovino))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion ganancia_peso_ceba: {e}')
        raise
    finally:
        session.close()



"""la siguiente funcion calcula e inserta todos los registros de ganancia de peso existentes"""

def ganancia_peso_historica(session: Session,current_user):
    try:
        #la siguiente consulta trae los id de los bovinos
        consulta_animales= session.query(modelo_bovinos_inventario.c.id_bovino,modelo_bovinos_inventario.c.nombre_bovino).\
            filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()

        # recorre el bucle
        for i in consulta_animales:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino = i[0]
            # Toma el nombre del bovino, este es el campo numero 0
            nombre_bovino=i[1]

            # Realiza la consulta general de la tabla de registro de pesos
            #la consulta esta ordenada segun la fecha mas antigua
            consulta_pesos = session.query(modelo_datos_pesaje.columns.peso,
                                           modelo_datos_pesaje.columns.fecha_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino==id_bovino).\
                order_by(asc(modelo_datos_pesaje.columns.fecha_pesaje)).all()

            cantidad=len(consulta_pesos)
            #si un animal no tiene por lo menos 2 registros de peso no se podra calcular la ganancia diaria de peso
            if cantidad<=1:
                pass
            else:
                contador=cantidad-1
                c=0
                while(c<contador):
                    # se identifican los pesos iniciales y finales con sus fechas
                    peso_inicial = consulta_pesos[c][0]
                    fecha_inicial = consulta_pesos[c][1]

                    peso_final = consulta_pesos[c + 1][0]
                    fecha_final = consulta_pesos[c + 1][1]

                    diferencia_fechas = (fecha_final - fecha_inicial).days

                    # si la diferencia entre fechas no es mayor a un dia entonces no se podra calcular la ganancia
                    if diferencia_fechas < 1 or diferencia_fechas == 0:
                        c=c+1
                        pass

                    else:
                        # se calcula la ganacia media diaria de peso por dia
                        ganancia_media_diaria = ((peso_final - peso_inicial) / (
                        ((fecha_final - fecha_inicial).days))) * 1000

                        # consulta que determina si las fecha y ganancia calulado ya existe en la tabla
                        consulta_existencia_intervalo = session.query(modelo_ganancia_historica_peso). \
                            filter(modelo_ganancia_historica_peso.columns.id_bovino == id_bovino,
                                   modelo_ganancia_historica_peso.columns.fecha_anterior == fecha_inicial,
                                   modelo_ganancia_historica_peso.columns.fecha_posterior == fecha_final).all()
                        #si no existe sera insertado

                        if consulta_existencia_intervalo is None or consulta_existencia_intervalo==[]:
                            ingresoGanancia = modelo_ganancia_historica_peso.insert().values(id_bovino=id_bovino,
                                                                                             nombre_bovino=nombre_bovino,
                                                                                             peso_anterior=peso_inicial,
                                                                                             peso_posterior=peso_final,
                                                                                             fecha_anterior=fecha_inicial,
                                                                                             fecha_posterior=fecha_final,
                                                                                             dias=diferencia_fechas,
                                                                                             ganancia_diaria_media=round(ganancia_media_diaria,2),
                                                                                             usuario_id=current_user)

                            session.execute(ingresoGanancia)
                            session.commit()
                            c=c+1
                        #si existe se actilizaran los campos
                        else:
                            session.execute(
                                modelo_ganancia_historica_peso.update().values(nombre_bovino=nombre_bovino,
                                                                               dias=diferencia_fechas,
                                                                               ganancia_diaria_media=round(ganancia_media_diaria,2)). \
                                    filter(modelo_ganancia_historica_peso.columns.id_bovino == id_bovino,
                                   modelo_ganancia_historica_peso.columns.fecha_anterior == fecha_inicial,
                                   modelo_ganancia_historica_peso.columns.fecha_posterior == fecha_final))
                            session.commit()
                            c=c+1



        #ya que el usuario puede eliminar y modificar los registros de peso,
        #el siguiente codigo elimina y actualiza los intervalos acorde a los pesos eliminados o modificados
        consulta_fechas_pesaje=session.query(modelo_ganancia_historica_peso).all()

        #se consulta en la tabla de ganancias historicas las fechas de pesaje

        for i in consulta_fechas_pesaje:
            # Toma el ID del bovino, este es el campo numero 1
            id_bovino_peso = i[1]
            # Toma la fecha_anterior del peso del bovino, este es el campo numero 5
            fecha_anterior = i[5]
            # Toma la fecha_posterior del peso del bovinoo, este es el campo numero 6
            fecha_posterior = i[6]

            #se consulta si existen estas fechas en los registros de pesos
            consulta_existencia_fecha_anterior = session.query(modelo_datos_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino == id_bovino_peso,
                       modelo_datos_pesaje.columns.fecha_pesaje == fecha_anterior).all()

            consulta_existencia_fecha_posterior = session.query(modelo_datos_pesaje). \
                filter(modelo_datos_pesaje.columns.id_bovino == id_bovino_peso,
                       modelo_datos_pesaje.columns.fecha_pesaje == fecha_posterior).all()

            #en caso de no existir indicara que el usuario ha eliminado o modificado algun peso
            #en eese caso se eliminara el intervalo

            if consulta_existencia_fecha_anterior==[] or consulta_existencia_fecha_posterior==[]:
                if consulta_existencia_fecha_anterior==[] :
                    session.execute(modelo_ganancia_historica_peso.delete(). \
                                    filter(modelo_ganancia_historica_peso.c.id_bovino == id_bovino_peso,
                                           modelo_ganancia_historica_peso.columns.fecha_anterior == fecha_anterior))
                    session.commit()
                else:
                    session.execute(modelo_ganancia_historica_peso.delete(). \
                                    filter(modelo_ganancia_historica_peso.c.id_bovino == id_bovino_peso,
                                           modelo_ganancia_historica_peso.columns.fecha_posterior == fecha_posterior))
                    session.commit()

            elif consulta_existencia_fecha_anterior is None or consulta_existencia_fecha_posterior is None:
                if consulta_existencia_fecha_anterior is None :
                    session.execute(modelo_ganancia_historica_peso.delete(). \
                                    filter(modelo_ganancia_historica_peso.c.id_bovino == id_bovino_peso,
                                           modelo_ganancia_historica_peso.columns.fecha_anterior == fecha_anterior))
                    session.commit()
                else:
                    session.execute(modelo_ganancia_historica_peso.delete(). \
                                    filter(modelo_ganancia_historica_peso.c.id_bovino == id_bovino_peso,
                                           modelo_ganancia_historica_peso.columns.fecha_posterior == fecha_posterior))
                    session.commit()
            else:
                pass


    except Exception as e:
        logger.error(f'Error Funcion ganancia_peso_historica: {e}')
        raise
    finally:
        session.close()