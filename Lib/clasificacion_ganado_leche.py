'''
Librerias requeridas

@autor : odvr

'''

import logging
from datetime import date, timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import desc
from sqlalchemy.sql.functions import current_user

# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_historial_partos, \
    modelo_orden_peso

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
"""la siguinete funcion determina el tipo de vaca: es decir si es escotera,
 parida o una novilla de vientre"""
#Advertencia: para que se jeceute corectamente esta funcion,
# debe haberser ejecutado la funcion peso_segun_raza()
def tipo_ganado_leche():
    try:
        #consulta que trae el listado de animales en leche
        animales_leche= session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.id_bovino,
                                      modelo_bovinos_inventario.c.raza,modelo_bovinos_inventario.c.peso,
                                      modelo_bovinos_inventario.c.edad). \
                   join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
            filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()
        # recorre el bucle
        for i in animales_leche:
            # Toma el ID del bovino, este es el campo numero 1
            id_bovino_leche = i[1]
            # Toma el estado del bovino, este es el campo numero 0
            estado_bovino_leche = i[0]
            # Toma la raza del bovino, este es el campo numero 2
            raza_bovino_leche = i[2]
            # Toma el peso del bovino, este es el campo numero 3
            peso_bovino_leche = i[3]
            # Toma la edad del bovino, este es el campo numero 4
            edad_bovino_leche = i[4]
            #si el animal esta muerto o vendido se indicara esto
            if estado_bovino_leche=="Muerto":
                tipo_ganado = "Este animal ha fallecido"
                session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                where(modelo_leche.columns.id_bovino == id_bovino_leche))
                session.commit()

            elif estado_bovino_leche=="Vendido":
                tipo_ganado = "Este animal ha sido vendido"
                session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                where(modelo_leche.columns.id_bovino == id_bovino_leche))
                session.commit()

            #si el animal esta vivo entonces se sometera al siguiente bucle
            elif estado_bovino_leche=="Vivo":
                #se trae el numero d epartos del animal
                consulta_num_partos=session.query(modelo_leche.c.num_partos). \
                   where(modelo_leche.c.id_bovino==id_bovino_leche).first()
                #si un animal no posee partos, entonces se evaluara si es novilla de vientre o una hembra de levante
                if consulta_num_partos[0]==0 or consulta_num_partos[0] is None:
                    #para ello se consulta el peso promedio de las hembras adultas de su raza
                    consulta_peso_raza = session.query(modelo_orden_peso.c.peso_promedio_raza,modelo_bovinos_inventario.c.raza). \
                        join(modelo_orden_peso, modelo_bovinos_inventario.c.id_bovino == modelo_orden_peso.c.id_bovino). \
                        filter(modelo_bovinos_inventario.columns.sexo == "Hembra",
                               modelo_orden_peso.c.raza==raza_bovino_leche).first()
                    #si no existe un peso para su raza entonces se evaluara segun su edad
                    if consulta_peso_raza is None or consulta_peso_raza==[]:
                        #si el anaimal posee 28 o mas meses de edad sera una novilla de vientre
                         if edad_bovino_leche >= 28:
                             tipo_ganado = "Novilla de Vientre"
                             session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                             where(modelo_leche.columns.id_bovino == id_bovino_leche))
                             session.commit()
                         #si no cumle con la edad sera una hembra de levante
                         else:
                             tipo_ganado = "Hembra de levante"
                             session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                             where(modelo_leche.columns.id_bovino == id_bovino_leche))
                             session.commit()
                    #si existe un peso para su raza se evaluara acorde al peso
                    else:
                        #si cumple con 75% o mas del peso de su raza sera una novilla de vientre
                        if peso_bovino_leche >= (0.75 * consulta_peso_raza[0]):
                            tipo_ganado = "Novilla de Vientre"
                            session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                            where(modelo_leche.columns.id_bovino == id_bovino_leche))
                            session.commit()
                        #si no lo cumple sera una hembra de levante
                        else:
                            tipo_ganado = "Hembra de levante"
                            session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                            where(modelo_leche.columns.id_bovino == id_bovino_leche))
                            session.commit()
                #si posee por lo menos un parto entonces se evalua si sera escotera o parida
                elif consulta_num_partos[0] > 0:
                    #se consulta la fecha de su ultimo parto y la cria que pario
                    consulta_ultimo_parto = list(condb.execute(modelo_historial_partos.select(). \
                                                        where(modelo_historial_partos.columns.id_bovino == id_bovino_leche). \
                                                        order_by(desc(modelo_historial_partos.columns.fecha_parto))).first())
                    #se consulta el estado de la cria parida
                    consulta_estado_cria= session.query(modelo_bovinos_inventario.c.estado). \
                   where(modelo_bovinos_inventario.c.id_bovino==consulta_ultimo_parto[4]).first()
                    #si la cria esta muerta o vendida entonces la vaca sera escotera
                    if consulta_estado_cria[0]!="Vivo":
                        tipo_ganado = "Escotera"
                        session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                        where(modelo_leche.columns.id_bovino == id_bovino_leche))
                        session.commit()
                    #si la cria esta viva se evaluara si es escotera o pradida segun la edad de la cria
                    elif consulta_estado_cria[0]=="Vivo":
                        #se calcula el tiempo entre el ultimo parto y la fecha actual
                        tiempo_ultimo_parto = date.today() - consulta_ultimo_parto[2]
                        #si han transcurrido por lo menos 305 dias,
                        # el ternero ya debio haber destetado, entonces la vaca sera escotera
                        if tiempo_ultimo_parto >= timedelta(305):
                            tipo_ganado = "Escotera"
                            session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                            where(modelo_leche.columns.id_bovino == id_bovino_leche))
                            session.commit()
                        #si no ha transcurrido este timpo, la vaca sera una vaca parida
                        else:
                            tipo_ganado = "Parida"
                            session.execute(modelo_leche.update().values(tipo_ganado=tipo_ganado). \
                                            where(modelo_leche.columns.id_bovino == id_bovino_leche))
                            session.commit()
            else:
                pass

        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion tipo_ganado_leche: {e}')
        raise
    finally:
        session.close()