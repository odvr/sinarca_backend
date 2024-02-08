'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import timedelta

from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_indicadores, modelo_orden_IEP, \
    modelo_palpaciones, modelo_historial_partos, modelo_historial_intervalo_partos, modelo_dias_abiertos, \
    modelo_canastillas, modelo_registro_pajillas
from sqlalchemy.orm import session
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

"""estas funciones relizan el conteo de las pajillas segun su canastillas asi como la eliminacion de la canastilla"""

def conteo_pajillas(session: session,current_user):
    try:
        #La siguiente consulta tare el listado de los id de las canastillas
        consulta_listado_canastillas=session.query(modelo_canastillas.c.id_canastilla).\
            filter(modelo_canastillas.c.usuario_id==current_user).all()
        #se establece un bucle para realizar la sumatoria de las unidades de cada canastilla
        contador= len(consulta_listado_canastillas)
        c=0
        while (c < contador):
            #la siguiente consulta tare la sumatoria de todas las unidades de cada canastilla
            consulta_cantidad_unidades = session.query(
                func.sum(modelo_registro_pajillas.columns.unidades)). \
                filter(modelo_registro_pajillas.columns.id_canastilla == consulta_listado_canastillas[c][0],
                       modelo_registro_pajillas.columns.unidades!=None).first()
            #si no existen unidades, su valor sera 0 en las unidades de la canastilla
            if consulta_cantidad_unidades[0] is None:
                session.execute(modelo_canastillas.update().values(unidades_disponibles=0). \
                                where(modelo_canastillas.columns.id_canastilla == consulta_listado_canastillas[c][0]))
                session.commit()
            #caso contrario se actualizara el valor real
            else:
                session.execute(modelo_canastillas.update().values(unidades_disponibles=consulta_cantidad_unidades[0]). \
                                where(modelo_canastillas.columns.id_canastilla == consulta_listado_canastillas[c][0]))
                session.commit()
            c=c+1

    except Exception as e:
        logger.error(f'Error Funcion conteo_pajillas: {e}')
        raise
    finally:
        session.close()


def nombre_canastilla(session: session,current_user):
    try:
        #se consulta la canastilla a eliminar
        consulta_canastilla = session.query(modelo_canastillas).filter(modelo_canastillas.c.usuario_id==current_user).all()

        for i in consulta_canastilla:
            # Toma el ID del bovino, este es el campo numero 0
            id_canastilla= i[0]
            # Toma el ID del bovino, este es el campo numero 0
            nombre_canastilla= i[1]

            session.execute(modelo_registro_pajillas.update().values(nombre_canastilla=nombre_canastilla). \
                            where(modelo_registro_pajillas.columns.id_canastilla ==id_canastilla ))

            session.commit()

    except Exception as e:
        logger.error(f'Error Funcion eliminacion_canastilla: {e}')
        raise
    finally:
        session.close()


def eliminacion_canastilla(id_canastilla_eliminar,session: session):
    try:
        #se consulta la canastilla a eliminar
        consulta_canastilla = session.query(modelo_canastillas). \
            filter(modelo_canastillas.c.id_canastilla == id_canastilla_eliminar).all()
        #si ya ha sido eliminada, se detendra la funcion
        if consulta_canastilla is None:
            pass
        #caso contrario, se eliminara la canastilla
        else:
            #se actualizan los valores de id y nombre de canastilla en el registro de ajillas por valores vacios
            valor_nulo=None
            session.execute(modelo_registro_pajillas.update().values(nombre_canastilla=valor_nulo,id_canastilla=valor_nulo). \
                            where(modelo_registro_pajillas.columns.id_canastilla == id_canastilla_eliminar))
            #se eliminara la canstilla de la base de datos
            session.execute(modelo_canastillas.delete().where(modelo_canastillas.c.id_canastilla == id_canastilla_eliminar))
            session.commit()

    except Exception as e:
        logger.error(f'Error Funcion eliminacion_canastilla: {e}')
        raise
    finally:
        session.close()