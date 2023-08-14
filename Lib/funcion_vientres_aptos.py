'''
Librerias requeridas

@autor : odvr

'''

import logging

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_vientres_aptos, modelo_orden_peso

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
"""la siguiente funcion muestra los vientres aptos, es decir,
animales hembras vivos con un peso igual o superior al 75% de su peso adulto"""
def vientres_aptos():
  try:
      #la siguiente consulta trae los animales hembras de la tabla de peso por raza
      consulta_pesos_para_vientres = session.query(modelo_orden_peso.c.id_bovino,
                                              modelo_bovinos_inventario.c.edad,
                                              modelo_orden_peso.c.raza,
                                              modelo_orden_peso.c.peso_promedio_raza,
                                              modelo_orden_peso.c.peso_promedio_animal). \
          join(modelo_orden_peso, modelo_bovinos_inventario.c.id_bovino == modelo_orden_peso.c.id_bovino). \
          filter( modelo_bovinos_inventario.columns.sexo == "Hembra").all()

      for i in consulta_pesos_para_vientres:
          # Toma el ID del bovino en este caso es el campo 0
          idBovinoConsultaVientresAptos = i[0]
          # Toma la edad del animal en este caso es el campo 1
          edadBovinoConsultaVientresAptos = i[1]
          # Toma la raza del animal en este caso es el campo 2
          razaBovinoConsultaVientresAptos = i[2]
          # Toma el peso de la raza del animal en este caso es el campo 3
          pesoRazaBovinoConsultaVientresAptos = i[3]
          # Toma el peso del animal en este caso es el campo 4
          pesoBovinoConsultaVientresAptos = i[4]

          if pesoBovinoConsultaVientresAptos >= (0.75*pesoRazaBovinoConsultaVientresAptos):
              #
              # consulta para saber si el bovino ya existe
              consulta_existencia_bovino = session.query(modelo_vientres_aptos). \
                      filter(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos).all()
              # si la consulta es vacia significa que no existe ese animal en la tabla,
              # entonces ese animal sera insertado
              if consulta_existencia_bovino == []:

                  ingresoVientresAptos = modelo_vientres_aptos.insert().values(
                          id_bovino=idBovinoConsultaVientresAptos,
                          edad=edadBovinoConsultaVientresAptos,
                          peso=pesoBovinoConsultaVientresAptos,
                          raza=razaBovinoConsultaVientresAptos)
                  condb.execute(ingresoVientresAptos)
                  condb.commit()
              else:
                  #
                  session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                  session.commit()
          else:
              pass

      consulta_vientres = session.query(modelo_vientres_aptos.c.id_bovino).all()
      for i in consulta_vientres:
          # Toma el ID del bovino en este caso es el campo 0
          idBov = i[0]

          consulta_existencia_en_tabla=session.query(modelo_orden_peso).\
              where(modelo_orden_peso.c.id_bovino==idBov).all()

          if consulta_existencia_en_tabla is None or consulta_existencia_en_tabla==[]:
              session.execute(modelo_vientres_aptos.delete(). \
                              where(modelo_vientres_aptos.c.id_bovino == idBov))
              session.commit()
          else:
              pass

          consulta_cambio_sexo=session.query(modelo_bovinos_inventario).\
              where(modelo_bovinos_inventario.c.id_bovino==idBov)\
              .filter(modelo_bovinos_inventario.c.sexo!="Hembra").all()

          if consulta_cambio_sexo is None or consulta_cambio_sexo==[]:
              pass
          else:
              session.execute(modelo_vientres_aptos.delete(). \
                              where(modelo_vientres_aptos.c.id_bovino == idBov))
              session.commit()

      session.commit()

  except Exception as e:
      logger.error(f'Error Funcion vientres_aptos: {e}')
      raise
  finally:
      session.close()