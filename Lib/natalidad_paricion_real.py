'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import asc, func, between
from sqlalchemy.orm import Session

# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_levante, modelo_datos_pesaje, modelo_ceba, \
    modelo_ganancia_historica_peso, modelo_historial_intervalo_partos, modelo_natalidad_paricion_real

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

"""estas funciones calculan la natalidad o paricion real del hato año a año"""

def natalidad_paricion_real(session: Session,current_user):
    try:
        # la siguiente consulta trae el primer anyo en que se registran intervalos entre partos
        consulta_anyo = session.query(modelo_historial_intervalo_partos.c.fecha_parto1)\
            .group_by(asc(modelo_historial_intervalo_partos.c.fecha_parto1)).\
            filter(modelo_historial_intervalo_partos.c.usuario_id == current_user).first()

        # si retorna una consulta vacia entonces indicara cero paricion real
        if consulta_anyo is None or consulta_anyo == []:
            periodo_actual = int(datetime.now().year)
            tasa_natalidad_paricion = 0

            consulta_existencia = session.query(modelo_natalidad_paricion_real). \
                where(modelo_natalidad_paricion_real.columns.periodo == periodo_actual). \
                filter(modelo_natalidad_paricion_real.c.usuario_id == current_user).all()

            #si el valor correspondiente al año actual

            if consulta_existencia == []:
                intervalo_entre_partos_periodo=0
                ingresoperiodo = modelo_natalidad_paricion_real.insert().values(periodo=periodo_actual,
                                                                                intervalo_entre_partos_periodo=intervalo_entre_partos_periodo,
                                                                                natalidad_paricion_real=tasa_natalidad_paricion,
                                                                                usuario_id=current_user)

                session.execute(ingresoperiodo)
                session.commit()
            else:
                intervalo_entre_partos_periodo = 0
                session.execute(modelo_natalidad_paricion_real.update().values(periodo=periodo_actual,
                                                                                intervalo_entre_partos_periodo=intervalo_entre_partos_periodo,
                                                                                natalidad_paricion_real=tasa_natalidad_paricion). \
                           where(modelo_natalidad_paricion_real.columns.periodo == periodo_actual).
                           filter(modelo_natalidad_paricion_real.c.usuario_id == current_user))
                session.commit()

        else:
            contador = (datetime.now().year - consulta_anyo[0].year) + 1
            c = 0
            while (c < contador):
                periodo = consulta_anyo[0].year + c
                # se determinan las fechas del periodo (inicio y fin de año)
                fecha_inicio = datetime(periodo, 1, 1)
                fecha_fin = datetime(periodo, 12, 31)
                # la siguiente consulta trae la cantidad de muertes para cada periodo a evaluar
                intervalo_entre_partos_periodo = session.query(func.avg(modelo_historial_intervalo_partos.c.intervalo)).\
                    where(between(modelo_historial_intervalo_partos.columns.fecha_parto1, fecha_inicio, fecha_fin)).\
                    filter(modelo_historial_intervalo_partos.c.usuario_id==current_user).all()


                if intervalo_entre_partos_periodo[0][0]==None or intervalo_entre_partos_periodo is None:

                    valor_natalidad_paricion_real=0

                    consulta_existencia_natalidad = session.query(modelo_natalidad_paricion_real). \
                        where(modelo_natalidad_paricion_real.columns.periodo == periodo). \
                        filter(modelo_natalidad_paricion_real.c.usuario_id == current_user).all()

                    if consulta_existencia_natalidad == []:
                        ingresoperiodo = modelo_natalidad_paricion_real.insert().values(periodo=periodo,
                                                                                        intervalo_entre_partos_periodo=0,
                                                                                        natalidad_paricion_real=valor_natalidad_paricion_real,
                                                                                        usuario_id=current_user)

                        session.execute(ingresoperiodo)
                        session.commit()
                        c = c + 1
                    else:
                        session.execute(
                            modelo_natalidad_paricion_real.update().values(periodo=periodo,
                                                                                intervalo_entre_partos_periodo=0,
                                                                                natalidad_paricion_real=valor_natalidad_paricion_real). \
                                where(modelo_natalidad_paricion_real.columns.periodo == periodo).
                                filter(modelo_natalidad_paricion_real.c.usuario_id == current_user))
                        session.commit()
                        c = c + 1

                else:
                    calculo_natalidad_paricion_real = (365 / (intervalo_entre_partos_periodo[0][0])) * 100
                    valor_natalidad_paricion_real = round(calculo_natalidad_paricion_real, 2)

                    consulta_existencia_natalidad = session.query(modelo_natalidad_paricion_real). \
                        where(modelo_natalidad_paricion_real.columns.periodo == periodo). \
                        filter(modelo_natalidad_paricion_real.c.usuario_id == current_user).all()

                    if consulta_existencia_natalidad == []:
                        ingresoperiodo = modelo_natalidad_paricion_real.insert().values(periodo=periodo,
                                                                                        intervalo_entre_partos_periodo=
                                                                                        intervalo_entre_partos_periodo[0][0],
                                                                                        natalidad_paricion_real=valor_natalidad_paricion_real,
                                                                                        usuario_id=current_user)

                        session.execute(ingresoperiodo)
                        session.commit()
                        c = c + 1
                    else:
                        session.execute(
                            modelo_natalidad_paricion_real.update().values(
                                intervalo_entre_partos_periodo=intervalo_entre_partos_periodo[0][0],
                                natalidad_paricion_real=valor_natalidad_paricion_real). \
                                where(modelo_natalidad_paricion_real.columns.periodo == periodo).
                                filter(modelo_natalidad_paricion_real.c.usuario_id == current_user))
                        session.commit()
                        c = c + 1


        #codigo que permite actualizar en caso de que se cambien las fechas de intrvalos entre partos
        if consulta_anyo is None or consulta_anyo==[]:
            session.execute(modelo_natalidad_paricion_real.delete().
                       where(modelo_natalidad_paricion_real.c.periodo != datetime.now().year).
                       filter(modelo_natalidad_paricion_real.c.usuario_id == current_user))
            session.commit()

        else:
            consulta_periodos= session.query(modelo_natalidad_paricion_real). \
                where(modelo_natalidad_paricion_real.columns.periodo < consulta_anyo[0].year). \
                filter(modelo_natalidad_paricion_real.c.usuario_id == current_user).all()

            if consulta_periodos is None or consulta_periodos == []:
                pass
            else:
                session.execute(modelo_natalidad_paricion_real.delete().
                                where(modelo_natalidad_paricion_real.c.periodo < consulta_anyo[0].year).
                                filter(modelo_natalidad_paricion_real.c.usuario_id == current_user))
                session.commit()


    except Exception as e:
        logger.error(f'Error Funcion natalidad_paricion_real: {e}')
        raise
    finally:
        session.close()