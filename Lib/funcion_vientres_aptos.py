'''
Librerias requeridas

@autor : odvr

'''

import logging

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_vientres_aptos, modelo_leche

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
"""la siguiente funcion muestra los vientres aptos para realizar alguna inseminacion, en este caso, 
mostrara las hembras que esten en leche que tengan como categoria vaca vacia y 
que no tengan categoria de hembra de levante"""
#Advertencia: ara que se jeceute corectamente esta funcion,
# debe haberser ejecutado la funcion peso_segun_raza() y
# tipo_ganado_leche()
def vientres_aptos(session: Session):
  try:
      #la siguiente consulta trae los animales hembras vacios
      consulta_vientres = session.query(modelo_leche.c.id_bovino,modelo_bovinos_inventario.c.edad,
                                        modelo_bovinos_inventario.c.peso, modelo_bovinos_inventario.c.raza). \
          join(modelo_leche, modelo_bovinos_inventario.c.id_bovino==modelo_leche.c.id_bovino).\
          where(modelo_bovinos_inventario.c.estado=="Vivo").\
          filter( modelo_leche.columns.datos_prenez == "Vacia",
                  modelo_leche.columns.tipo_ganado != "Hembra de levante").all()

      for i in consulta_vientres:
          # Toma el ID del bovino en este caso es el campo 0
          idBovinoConsultaVientresAptos = i[0]
          # Toma la edad del animal en este caso es el campo 1
          edadBovinoConsultaVientresAptos = i[1]
          # Toma la raza del animal en este caso es el campo 3
          razaBovinoConsultaVientresAptos = i[3]
          # Toma el peso del animal en este caso es el campo 2
          pesoBovinoConsultaVientresAptos = i[2]

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
              #si el animal ya existe actualiza sus datos
              session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                    peso=pesoBovinoConsultaVientresAptos,
                                                                    raza=razaBovinoConsultaVientresAptos). \
                              where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
              session.commit()
      else:
          pass
      #el siguiente codigo permite eliminar animales cuyo estado o condicion sea cambiada
      #consulta de los vientres aptos
      consulta_vientres_aptos = session.query(modelo_vientres_aptos.c.id_bovino).all()
      for i in consulta_vientres_aptos:
          # Toma el ID del bovino en este caso es el campo 0
          idBov = i[0]

          consulta_prenez= session.query(modelo_leche). \
              where(modelo_leche.c.id_bovino == idBov).\
              filter( modelo_leche.columns.datos_prenez == "Prenada").all()

          if consulta_prenez != []:
              session.execute(modelo_vientres_aptos.delete(). \
                              where(modelo_vientres_aptos.c.id_bovino == idBov))
              session.commit()

          else:
              pass

          consulta_tipo_ganado= session.query(modelo_leche). \
              where(modelo_leche.c.id_bovino == idBov).\
              filter(modelo_leche.columns.tipo_ganado == "Hembra de levante").all()

          if consulta_tipo_ganado != []:
              session.execute(modelo_vientres_aptos.delete(). \
                              where(modelo_vientres_aptos.c.id_bovino == idBov))
              session.commit()

          else:
              pass

          consulta_cambio_sexo = session.query(modelo_bovinos_inventario). \
              where(modelo_bovinos_inventario.c.id_bovino == idBov) \
              .filter(modelo_bovinos_inventario.c.sexo != "Hembra").all()

          if consulta_cambio_sexo is None or consulta_cambio_sexo == []:
              pass
          else:
              session.execute(modelo_vientres_aptos.delete(). \
                              where(modelo_vientres_aptos.c.id_bovino == idBov))
              session.commit()

          consulta_cambio_estado = session.query(modelo_bovinos_inventario). \
              where(modelo_bovinos_inventario.c.id_bovino == idBov) \
              .filter(modelo_bovinos_inventario.c.estado != "Vivo").all()

          if consulta_cambio_estado is None or consulta_cambio_estado == []:
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