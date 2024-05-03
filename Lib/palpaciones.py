'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import timedelta

from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones
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

"""la siguiente permite actualizar el ultimo resultado de las palpaciones
para actualizar el estado de prenez de un animal en el modulo de leche"""

def palpaciones(session: Session,current_user):
    try:
        # consulta de animales en el modulo de leche
        consulta_animales_leche = session.query(modelo_leche).\
            filter(modelo_leche.columns.usuario_id==current_user).all()
        for i in consulta_animales_leche:
            # Toma el id del bovino en este caso es el campo 1
            id_bovino_leche = i[1]
            # Toma el nombre del bovino en este caso es el campo 13
            nombre_bovino_leche = i[13]
            #con el id consulta la ultima palpacion para actualizar el estado de prenez
            # del animal
            consulta_prenez = session.query(modelo_palpaciones).where(modelo_palpaciones.columns.id_bovino == id_bovino_leche). \
                                              order_by(desc(modelo_palpaciones.columns.fecha_palpacion)).first()
            #si la consulta es vacia se añade un valor por defecto
            if consulta_prenez==[] or consulta_prenez is None:
                valor_defecto="Vacia"
                session.execute(modelo_leche.update().values(datos_prenez=valor_defecto,nombre_bovino=nombre_bovino_leche). \
                                where(modelo_leche.columns.id_bovino == id_bovino_leche))
                session.commit()
            #caso contrario se actualiza el valor de la ultima palpacion realizada
            else:
                session.execute(modelo_leche.update().values(datos_prenez=consulta_prenez[3],nombre_bovino=nombre_bovino_leche). \
                                where(modelo_leche.columns.id_bovino == id_bovino_leche))
                session.commit()


        # el siguiente codigo calcula las fechas de partos para animales preñadas
        # consulta de animales preñadas en el modulo de palpaciones
        consulta_animales_prenadas = session.query(modelo_palpaciones).\
            filter(modelo_palpaciones.columns.diagnostico_prenez=="Preñada",
                   modelo_palpaciones.columns.usuario_id==current_user).all()

        for i in consulta_animales_prenadas:
            # Toma el id de la palpacion en este caso es el campo 0
            id_palpacion = i[0]
            # Toma la fecha de palpacion del bovino en este caso es el campo 2
            fecha_palpacion=i[2]
            # Toma los dias de gestacion,en este caso es el campo 7
            dias_gestacion = i[7]

            #con la fecha de palpacion y los dis de gestacion, se calula la fecha estimada de preñez
            fecha_estimada_prenez=fecha_palpacion-timedelta(dias_gestacion)
            #con la fecha de preñez se calula la fecha aproximada de parto(la gestacion dura aproximadamente 283 dias)
            fecha_estimada_parto=fecha_estimada_prenez + timedelta(283)

            #actualiza los campos
            session.execute(
                modelo_palpaciones.update().values(fecha_estimada_prenez=fecha_estimada_prenez,
                                                   fecha_estimada_parto=fecha_estimada_parto). \
                where(modelo_palpaciones.columns.id_palpacion == id_palpacion))
            session.commit()

    except Exception as e:
        logger.error(f'Error Funcion palpaciones: {e}')
        raise
    finally:
        session.close()

