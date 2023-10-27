'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

# importa la conexion de la base de datos
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario,modelo_orden_peso

from sqlalchemy import  between, func


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

"""la siguiente funcion calcula el promedio por peso de cada raza dentro del hato ganadero con el
 fin de obtener un listado de animales ordenado del mas pesado al menos pesado segun su raza
  esta funcion solo aplicara para animales con edad mayor o igual a 24 meses que es la edad donde
  se considera que han alcanzado su peso adulto o estan por alcanzarlo"""
def peso_segun_raza(session:Session,current_user):
    try:
        #obtencion de un listado de todas las razas a trabajar
        razas =  list(set(session.query(modelo_bovinos_inventario.columns.raza). \
               where(between(modelo_bovinos_inventario.columns.edad, 24, 500)).filter(modelo_bovinos_inventario.columns.usuario_id==current_user).all()))
        #para calcular los pesos y animales por raza se implementa un bucle
        contador_raza= len(razas)
        b=0
        while(b<contador_raza):
            raza_a_trabajar=razas[b][0]
            #consulta de peso promedio por raza para animales de sexo macho
            consulta_peso_prom_por_raza_macho = session.query(
                func.avg(modelo_bovinos_inventario.columns.peso)).\
                where(between(modelo_bovinos_inventario.columns.edad, 24, 500)).\
                filter(modelo_bovinos_inventario.columns.sexo=="Macho",
                       modelo_bovinos_inventario.columns.raza==raza_a_trabajar,
                       modelo_bovinos_inventario.columns.estado=="Vivo",
                       modelo_bovinos_inventario.columns.usuario_id==current_user).all()
            # consulta de peso promedio por raza para animales de sexo hembra
            consulta_peso_prom_por_raza_hembra = session.query(
                func.avg(modelo_bovinos_inventario.columns.peso)).\
                where(between(modelo_bovinos_inventario.columns.edad, 24, 500)).\
                filter(modelo_bovinos_inventario.columns.sexo=="Hembra",
                       modelo_bovinos_inventario.columns.raza==raza_a_trabajar,
                       modelo_bovinos_inventario.columns.estado=="Vivo",
                       modelo_bovinos_inventario.columns.usuario_id==current_user).all()
            #esta consulta trae los bovinos vivos con edad igual o mayor a dos anos
            consulta_bovinos_peso = session.query(modelo_bovinos_inventario). \
                where(between(modelo_bovinos_inventario.columns.edad, 24, 500)). \
                filter(modelo_bovinos_inventario.c.estado == "Vivo",
                       modelo_bovinos_inventario.columns.usuario_id==current_user).all()
            #se recorre la consulta
            for i in consulta_bovinos_peso:
                # Toma el ID del bovino, este es el campo numero 0
                id_bovino_peso = i[0]
                # Toma el peso actual del bovino, este es el campo numero 5
                peso_bovino = i[5]
                # Toma la raza del bovino, este es el campo numero 4
                raza_bovino = i[4]
                # Toma el sexo bovino, este es el campo numero 3
                sexo_bovino = i[3]
                # Toma el usuario, este es el campo numero 11
                usuario = i[11]
                # Toma el nombre del animal, este es el campo numero 12
                nombre_bovino = i[12]
                #si el bovino es macho se aplicara lo siguiente
                if sexo_bovino=="Macho":
                    #si el promedio segun raza es una consulta vacia entonces no se realizara ningun cambio
                    if consulta_peso_prom_por_raza_macho[0][0] is None or consulta_peso_prom_por_raza_macho[0][0]==0:
                        pass
                    else:
                        diferencia = peso_bovino - consulta_peso_prom_por_raza_macho[0][0]
                        if raza_bovino == raza_a_trabajar:
                            # consulta para saber si el bovino existe
                            consulta_existencia_bovino = session.query(modelo_orden_peso). \
                                filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                            # si la consulta es vacia significa que no existe ese animal en la tabla,
                            # entonces ese animal sera insertado
                            if consulta_existencia_bovino == []:
                                ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                                 raza=raza_bovino,
                                                                                 peso_promedio_animal=peso_bovino,
                                                                                 peso_promedio_raza=
                                                                                 consulta_peso_prom_por_raza_macho[0][
                                                                                     0],
                                                                                 diferencia=diferencia,
                                                                                 usuario_id=usuario,
                                                                                 nombre_bovino=nombre_bovino)

                                session.execute(ingresoDatos)
                                session.commit()
                            # si el animal existe entonces actualiza sus datos
                            else:
                                session.execute(modelo_orden_peso.update().values(id_bovino=id_bovino_peso,
                                                                                  raza=raza_bovino,
                                                                                  peso_promedio_animal=peso_bovino,
                                                                                  peso_promedio_raza=
                                                                                  consulta_peso_prom_por_raza_macho[0][
                                                                                      0],
                                                                                  diferencia=diferencia,
                                                                                 usuario_id=usuario,
                                                                                  nombre_bovino=nombre_bovino). \
                                                where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                                session.commit()
                        else:
                            pass

                elif sexo_bovino=="Hembra":
                    if consulta_peso_prom_por_raza_hembra[0][0] is None or consulta_peso_prom_por_raza_hembra[0][0]==0:
                        pass
                    else:
                        diferencia = peso_bovino - consulta_peso_prom_por_raza_hembra[0][0]
                        if raza_bovino == raza_a_trabajar:
                            # consulta para saber si el bovino existe
                            consulta_existencia_bovino = session.query(modelo_orden_peso). \
                                filter(modelo_orden_peso.columns.id_bovino == id_bovino_peso).all()
                            # si la consulta es vacia significa que no existe ese animal en la tabla,
                            # entonces ese animal sera insertado
                            if consulta_existencia_bovino == []:
                                ingresoDatos = modelo_orden_peso.insert().values(id_bovino=id_bovino_peso,
                                                                                 raza=raza_bovino,
                                                                                 peso_promedio_animal=peso_bovino,
                                                                                 peso_promedio_raza=
                                                                                 consulta_peso_prom_por_raza_hembra[0][
                                                                                     0],
                                                                                 diferencia=diferencia,
                                                                                 usuario_id=usuario,
                                                                                 nombre_bovino=nombre_bovino)

                                session.execute(ingresoDatos)
                                session.commit()
                            # si el animal existe entonces actualiza sus datos
                            else:
                                session.execute(modelo_orden_peso.update().values(id_bovino=id_bovino_peso,
                                                                                  raza=raza_bovino,
                                                                                  peso_promedio_animal=peso_bovino,
                                                                                  peso_promedio_raza=
                                                                                  consulta_peso_prom_por_raza_hembra[0][
                                                                                      0],
                                                                                  diferencia=diferencia,
                                                                                 usuario_id=usuario,
                                                                                  nombre_bovino=nombre_bovino). \
                                                where(modelo_orden_peso.columns.id_bovino == id_bovino_peso))
                                session.commit()
                        else:
                            pass

            b=b+1

        #el siguiente codigo elimina los bovinos cuya edad o estado sea cambiado
        consulta_animales = session.query(modelo_bovinos_inventario.c.estado,modelo_orden_peso.c.id_bovino,
                                          modelo_bovinos_inventario.c.edad).\
            join(modelo_orden_peso,modelo_bovinos_inventario.c.id_bovino == modelo_orden_peso.c.id_bovino).\
            filter(modelo_bovinos_inventario.columns.usuario_id==current_user).all()
        for i in consulta_animales:
            # Toma el ID del bovino en este caso es el campo 1
            idBovino = i[1]
            # Toma el estado del bovino en este caso es el campo 0
            estadoBovino = i[0]
            # Toma el peso del bovino en este caso es el campo 2
            edadBovino = i[2]
            if estadoBovino == "Muerto" or estadoBovino == "Vendido":
                session.execute(modelo_orden_peso.delete().where(modelo_orden_peso.c.id_bovino == idBovino))
                session.commit()
            elif edadBovino <24:
                session.execute(modelo_orden_peso.delete().where(modelo_orden_peso.c.id_bovino == idBovino))
                session.commit()
    except Exception as e:
        logger.error(f'Error Funcion peso_segun_raza: {e}')
        raise
    finally:
        session.close()