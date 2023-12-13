'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import timedelta

from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones, modelo_historial_partos, modelo_historial_intervalo_partos, modelo_dias_abiertos
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

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

"""esta funcion calcula los dias abiertos apartir de la diferencia en dias
entre la fecha de ultimo parto y fecha de ultima prenez, siendo una medida
de productividad, pues si una vaca tiene mas de 120 dias abiertos, indica 
que no esta teniendo un ternero al ano, lo que indica que no esta siendo
productiva"""

def dias_abiertos(session: Session,current_user):
    try:
        consulta_animales_leche= session.query(modelo_historial_intervalo_partos.c.id_bovino,
                                                  modelo_historial_intervalo_partos.c.nombre_bovino,
                                               modelo_historial_intervalo_partos.c.fecha_parto1,
                                               modelo_historial_intervalo_partos.c.fecha_parto2).\
            filter(modelo_historial_intervalo_partos.c.usuario_id==current_user).all()


        # recorre el bucle
        for i in consulta_animales_leche:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_dias = i[0]
            # Toma el nombre del bovino, este es el campo numero 3
            nombre_bovino = i[1]
            # Toma la fecha de parto del bovino para la fecha de prenez, este es el campo numero 4
            fecha_parto1 = i[2]
            # toma la fecha de parto del bovino, este es el campo numero 5
            fecha_parto2 = i[3]

            #determina la fecha de prenez
            fecha_prenez = fecha_parto1 - timedelta(283)
            dias_abiertos_parto = (fecha_prenez - fecha_parto2).days

            # consulta que determina si el periodo de dias calulado ya existe en la tabla
            consulta_existencia_dias_abiertos = session.query(modelo_dias_abiertos). \
                filter(modelo_dias_abiertos.columns.id_bovino == id_bovino_dias,
                       modelo_dias_abiertos.columns.fecha_prenez == fecha_prenez,
                       modelo_dias_abiertos.columns.fecha_parto == fecha_parto2).all()

            # si el periodo de dias abiertos no existe (consulta vacia) entonces sera creado
            if consulta_existencia_dias_abiertos == []:
                ingresodias = modelo_dias_abiertos.insert().values(id_bovino=id_bovino_dias,
                                                                   fecha_prenez=
                                                                   fecha_prenez,
                                                                   fecha_parto=fecha_parto2,
                                                                   dias_abiertos=dias_abiertos_parto,
                                                                   usuario_id=current_user,
                                                                   nombre_bovino=nombre_bovino)

                session.execute(ingresodias)
                session.commit()
            #si ya existe el periodo de dias abierto entonces no se realizara ningun cambio
            else:
                pass


        # debido a que el usuario puede alterar y eliminar las fechas de partos
        # es necesario eliminar los periodos de dias abiertos que tengan las fechas antes de modificarse
        # Esta consulta permite averiguar todos los intervalos existentes
        consulta_animales_dias = session.query(modelo_dias_abiertos.c.id_bovino,
                                                    modelo_dias_abiertos.c.fecha_parto,
                                                    modelo_dias_abiertos.c.fecha_prenez). \
                filter(modelo_dias_abiertos.c.usuario_id == current_user).all()


        # recorre el bucle
        for i in consulta_animales_dias:
                # Toma el ID del bovino, este es el campo numero 0
                id_bovino = i[0]
                # Toma la fecha de parto, este es el campo numero 3
                fecha_parto_2 = i[1]
                # Toma el nombre del bovino, este es el campo numero 3
                fecha_prenez_dias = i[2]
                # caalcula la fecha de parto a partir de la prenez, este es el campo numero 3
                fecha_parto_1 = (i[2] + timedelta(283))

                consulta_existencia = session.query(modelo_historial_intervalo_partos). \
                    filter(modelo_historial_intervalo_partos.c.id_bovino == id_bovino,
                           modelo_historial_intervalo_partos.c.fecha_parto2 == fecha_parto_2,
                           modelo_historial_intervalo_partos.c.fecha_parto1 == fecha_parto_1).all()

                if consulta_existencia == [] or consulta_existencia is None:
                    session.execute(modelo_dias_abiertos.delete(). \
                                    where(modelo_dias_abiertos.c.id_bovino == id_bovino). \
                                    filter(modelo_dias_abiertos.c.fecha_prenez == fecha_prenez_dias,
                                           modelo_dias_abiertos.c.fecha_parto == fecha_parto_2))
                    session.commit()

                else:
                    pass

        # Actualizacion del valor mas actual en el campo del modulo de leche
        consulta_id= session.query(modelo_leche.c.id_bovino). \
            filter(modelo_leche.c.usuario_id == current_user).all()

        for i in consulta_id:
            # Toma el ID del bovino, este es el campo numero 0
            id_bovino_d_a = i[0]

            consulta_dias_abiertos = session.query(modelo_dias_abiertos). \
                where(modelo_dias_abiertos.columns.id_bovino == id_bovino_d_a). \
                order_by(desc(modelo_dias_abiertos.columns.fecha_prenez)).first()

            if consulta_dias_abiertos == [] or consulta_dias_abiertos is None:
                valor_defecto=None
                session.execute(modelo_leche.update().values(dias_abiertos=valor_defecto). \
                                where(modelo_leche.columns.id_bovino == id_bovino_d_a))
                session.commit()
            else:
                session.execute(modelo_leche.update().values(dias_abiertos=consulta_dias_abiertos[5]). \
                                where(modelo_leche.columns.id_bovino == id_bovino_d_a))
                session.commit()


    except Exception as e:
        logger.error(f'Error Funcion dias_abiertos: {e}')
        raise
    finally:
        session.close()