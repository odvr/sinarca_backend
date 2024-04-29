'''
Librerias requeridas

@autor : odvr

'''
import datetime
import logging
from datetime import timedelta

from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones, modelo_historial_partos, modelo_historial_intervalo_partos, modelo_dias_abiertos, \
    modelo_periodos_lactancia, modelo_litros_leche
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, between

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

"""estas funciones calculan los periodos de lactancia para los animales en produccion de leche, su pico de produccion
y el total de litros producidos en esa lactancia"""

def periodos_lactancia(session: Session,current_user):
    try:
        #consulta que trae los animales en produccion de leche
        consulta_animales_lactancia= session.query(modelo_periodos_lactancia).\
            filter(modelo_periodos_lactancia.c.usuario_id==current_user).all()


        # recorre el bucle
        for i in consulta_animales_lactancia:
            # Toma la fecha de inicio de lactancia del bovino, este es el campo numero 3
            fecha_inicio_lactancia = i[3]
            # toma la fecha de final de lactancia del bovinoo, este es el campo numero 4
            fecha_final_lactancia = i[4]
            # Toma el ID del bovino, este es el campo numero 1
            id_parto_lactancia = i[11]

            #si el usuario no ingresa fecha final de lactancia, se calculara el periodo desde la fecha
            # de inicio de lactancia hasta la fecha actual
            if fecha_final_lactancia is None:
                duracion= (datetime.date.today()- fecha_inicio_lactancia).days
                if duracion>305:
                    tipo="extendido"
                    mensaje="la lactancia de este animal ha superado los 305 dias"
                    session.execute(modelo_periodos_lactancia.update().values(duracion=duracion, mensaje=mensaje,tipo=tipo). \
                                    where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()

                else:
                    tipo="normal"
                    session.execute(modelo_periodos_lactancia.update().values(duracion=duracion,tipo=tipo). \
                                    where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()

            else:
                duracion=(fecha_final_lactancia-fecha_inicio_lactancia).days

                if duracion>305:
                    tipo="extendido"
                    mensaje="la lactancia de este animal ha superado los 305 dias"
                    session.execute(modelo_periodos_lactancia.update().values(duracion=duracion, mensaje=mensaje,tipo=tipo). \
                                    where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()
                elif duracion<140:
                    tipo="anormal"
                    mensaje = "lactancia anormalmente corta"
                    session.execute(modelo_periodos_lactancia.update().values(duracion=duracion,tipo=tipo,mensaje=mensaje). \
                                    where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()

                else:
                    tipo="normal"
                    session.execute(modelo_periodos_lactancia.update().values(duracion=duracion,tipo=tipo). \
                                    where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()

    except Exception as e:
        logger.error(f'Error Funcion periodos_lactancia: {e}')
        raise
    finally:
        session.close()


def pico_y_produccion_lactancia(session: Session,current_user):
    try:
        #consulta que trae los animales en produccion de leche
        consulta_animales_lactancia= session.query(modelo_periodos_lactancia).\
            filter(modelo_periodos_lactancia.c.usuario_id==current_user).all()


        # recorre el bucle
        for i in consulta_animales_lactancia:
            # Toma el ID del bovino, este es el campo numero 1
            id_bovino_lactancia = i[1]
            # Toma la fecha de inicio de lactancia del bovino, este es el campo numero 3
            fecha_inicio_lactancia = i[3]
            # toma la fecha de final de lactancia del bovinoo, este es el campo numero 4
            fecha_final_lactancia = i[4]
            # Toma el ID del bovino, este es el campo numero 1
            id_parto_lactancia = i[11]

            #si el usuario no ingresa fecha final de lactancia, se calculara el periodo desde la fecha
            # de inicio de lactancia hasta la fecha actual
            if fecha_final_lactancia is None:
                fecha_inicio=fecha_inicio_lactancia
                fecha_fin=datetime.date.today()

                total_litros=session.query(func.sum(modelo_litros_leche.columns.litros_leche)). \
                 where(between(modelo_litros_leche.columns.fecha_medicion, fecha_inicio, fecha_fin)).\
                    filter(modelo_litros_leche.columns.id_bovino==id_bovino_lactancia,
                         modelo_litros_leche.c.usuario_id==current_user).first()


                pico_fecha=session.query(modelo_litros_leche.c.litros_leche,modelo_litros_leche.c.fecha_medicion).\
                where(modelo_litros_leche.columns.id_bovino==id_bovino_lactancia).\
                    order_by(desc(modelo_litros_leche.columns.litros_leche)).first()

                if total_litros[0] is None:
                    pass
                else:
                    session.execute(
                        modelo_periodos_lactancia.update().values(pico=pico_fecha[0], fecha_pico=pico_fecha[1],
                                                                  total_litros_producidos=total_litros[0]). \
                        where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()



            else:
                fecha_inicio=fecha_inicio_lactancia
                fecha_fin=fecha_final_lactancia

                total_litros=session.query(func.sum(modelo_litros_leche.columns.litros_leche)). \
                 where(between(modelo_litros_leche.columns.fecha_medicion, fecha_inicio, fecha_fin)).\
                    filter(modelo_litros_leche.columns.id_bovino==id_bovino_lactancia,
                         modelo_litros_leche.c.usuario_id==current_user).first()


                pico_fecha=session.query(modelo_litros_leche.c.litros_leche,modelo_litros_leche.c.fecha_medicion).\
                where(modelo_litros_leche.columns.id_bovino==id_bovino_lactancia).\
                    order_by(desc(modelo_litros_leche.columns.litros_leche)).first()

                if total_litros[0] is None:
                    pass
                else:
                    session.execute(
                        modelo_periodos_lactancia.update().values(pico=pico_fecha[0], fecha_pico=pico_fecha[1],
                                                                  total_litros_producidos=total_litros[0]). \
                        where(modelo_periodos_lactancia.columns.id_parto == id_parto_lactancia))
                    session.commit()



    except Exception as e:
        logger.error(f'Error Funcion periodos_lactancia: {e}')
        raise
    finally:
        session.close()