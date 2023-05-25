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
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_vientres_aptos

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


      # consulta de vacas que cumplen con la condicion
      consulta_vientres = session.query(modelo_bovinos_inventario). \
          where(modelo_bovinos_inventario.c.estado == "Vivo").\
          filter(modelo_bovinos_inventario.c.sexo == "Hembra").all()

      for i in consulta_vientres:   
          # Toma el ID del bovino en este caso es el campo 0
          idBovinoConsultaVientresAptos = i[0]
          # Toma la edad del animal en este caso es el campo 2
          edadBovinoConsultaVientresAptos = i[2]
          # Toma la raza del animal en este caso es el campo 4
          razaBovinoConsultaVientresAptos = i[4]
          # Toma el peso del animal en este caso es el campo 5
          pesoBovinoConsultaVientresAptos = i[5]
          #el peso sulto promedio varia segun la raza
          #se establece un bucle segun la raza
          if razaBovinoConsultaVientresAptos=="Holstein":
              #las hembras adultas Holstein tienen un peso promedio de 650 kg (el 75% es 487.5)
              if pesoBovinoConsultaVientresAptos >= 487.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Jersey":
              # las hembras adultas Jersey tienen un peso promedio de 430 kg (el 75% es 322.5)
              if pesoBovinoConsultaVientresAptos >= 322.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass
          elif razaBovinoConsultaVientresAptos == "Gyr":
              # las hembras adultas Gyr tienen un peso promedio de 450 kg (el 75% es 337.5 kg)
              if pesoBovinoConsultaVientresAptos >= 337.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Girolando":
              # las hembras adultas Girolando tienen un peso promedio de 450 kg (el 75% es 337.5 kg)
              if pesoBovinoConsultaVientresAptos >= 337.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Red Sindhi":
              # las hembras adultas Red Sindhi tienen un peso promedio de 350 kg (el 75% es 262.5kg)
              if pesoBovinoConsultaVientresAptos >= 262.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Limousin":
              # las hembras adultas Limousin tienen un peso promedio de 500 kg (el 75% es 375 kg)
              if pesoBovinoConsultaVientresAptos >= 375:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Charolais":
              # las hembras adultas Charolais tienen un peso promedio de 600 kg (el 75% es 450 kg)
              if pesoBovinoConsultaVientresAptos >= 450:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Hereford":
              # las hembras adultas Hereford tienen un peso promedio de 550 kg (el 75% es 412.5 kg)
              if pesoBovinoConsultaVientresAptos >= 412.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Romagnola":
              # # las hembras adultas Romagnola tienen un peso promedio de 600 kg (el 75% es 450 kg)
              if pesoBovinoConsultaVientresAptos >= 450:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Brahman":
              # las hembras adultas Brahman tienen un peso promedio de 500 kg (el 75% es 337.5 kg)
              if pesoBovinoConsultaVientresAptos >= 375:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Guzerat":
              # las hembras adultas Guzerat tienen un peso promedio de 450 kg (el 75% es 337.5 kg)
              if pesoBovinoConsultaVientresAptos >= 337.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Nelore":
              # las hembras adultas Nelore tienen un peso promedio de 500 kg (el 75% es 375 kg)
              if pesoBovinoConsultaVientresAptos >= 375:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Brangus":
              # las hembras adultas Brangus tienen un peso promedio de 545 kg (el 75% es 408.75 kg)
              if pesoBovinoConsultaVientresAptos >= 408.75 :
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Simmental":
              # las hembras adultas Simmental tienen un peso promedio de 750 kg (el 75% es 562.5kg)
              if pesoBovinoConsultaVientresAptos >= 562.5 :
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Pardo suizo":
              # # las hembras adultas Pardo suizo tienen un peso promedio de 600 kg (el 75% es 450 kg)
              if pesoBovinoConsultaVientresAptos >= 450:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Normando":
              # # las hembras adultas Normando tienen un peso promedio de 700 kg (el 75% es 525 kg)
              if pesoBovinoConsultaVientresAptos >= 525:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Ayrshire":
              # las hembras adultas Ayrshire tienen un peso promedio de 450 kg (el 75% es 300)
              if pesoBovinoConsultaVientresAptos >= 337.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Indubrasil":
              # # las hembras Indubrasil  tienen un peso promedio de 600 kg (el 75% es 450 kg)
              if pesoBovinoConsultaVientresAptos >= 450:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Blanco orejinegro":
              # las hembras adultas Blanco orejinegro tienen un peso promedio de 350 kg (el 75% es 262.5kg)
              if pesoBovinoConsultaVientresAptos >= 262.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Romosinuano":
              # las hembras adultas Romosinuano tienen un peso promedio de 383 kg (el 75% es 287.25 kg)
              if pesoBovinoConsultaVientresAptos >= 287.25:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Sanmartinero":
              # las hembras adultas Sanmartinero tienen un peso promedio de 400 kg (el 75% es 300)
              if pesoBovinoConsultaVientresAptos >= 300:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Costeño con cuernos":
              # las hembras adultas Costeño con cuernos tienen un peso promedio de 380 kg (el 75% es 285 kg)
              if pesoBovinoConsultaVientresAptos >= 285:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Chino santandereano":
              # las hembras adultas Chino santandereano tienen un peso promedio de 487 kg (el 75% es 365.25 kg)
              if pesoBovinoConsultaVientresAptos >= 365.25:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Harton del valle":
              # las hembras adultas Harton del valle tienen un peso promedio de 454 kg (el 75% es 340.5 kg)
              if pesoBovinoConsultaVientresAptos >= 340.5:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Casanareño":
              # las hembras adultas Casanareño tienen un peso promedio de 380 kg (el 75% es 285 kg)
              if pesoBovinoConsultaVientresAptos >= 285:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "Velasquez":
              # las hembras adultas Harton del valle tienen un peso promedio de 440 kg (el 75% es 330 kg)
              if pesoBovinoConsultaVientresAptos >= 330:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass

          elif razaBovinoConsultaVientresAptos == "7 colores (cruce indefinido)":
              # las hembras adultas 7 colores (cruce indefinido) tienen un peso promedio de 400 kg (el 75% es 300 kg)
              if pesoBovinoConsultaVientresAptos >= 300:
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
                      session.execute(modelo_vientres_aptos.update().values(edad=edadBovinoConsultaVientresAptos,
                                                                            peso=pesoBovinoConsultaVientresAptos,
                                                                            raza=razaBovinoConsultaVientresAptos). \
                                      where(modelo_vientres_aptos.columns.id_bovino == idBovinoConsultaVientresAptos))
                      session.commit()
              else:
                  pass
          # consulta para realizar eliminacion de animales cuyo sexo o estado fue cambiado
          consulta_animales = session.query(modelo_bovinos_inventario.c.estado, modelo_bovinos_inventario.c.sexo,
                                            modelo_vientres_aptos.c.id_bovino, modelo_bovinos_inventario.c.peso,
                                            modelo_vientres_aptos.c.peso). \
              join(modelo_vientres_aptos, modelo_bovinos_inventario.c.id_bovino == modelo_vientres_aptos.c.id_bovino).all()
          for i in consulta_animales:
              # Toma el ID del bovino en este caso es el campo 2
              idBovino = i[2]
              # Toma el estado del bovino en este caso es el campo 0
              estadoBovino = i[0]
              # Toma el sexo del bovino en este caso es el campo 1
              sexoBovino = i[1]
              # Toma el peso del bovino en este caso es el campo 1
              pesoBovino = i[3]
              # Toma el peso del bovino en este caso es el campo 1
              pesoenVientresAptos = i[4]
              if estadoBovino == "Muerto" or estadoBovino == "Vendido":
                  session.execute(modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino == idBovino))
                  session.commit()
              elif sexoBovino == "Macho":
                  session.execute(modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino == idBovino))
                  session.commit()
              elif pesoBovino != pesoenVientresAptos:
                  session.execute(modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino == idBovino))
                  session.commit()

      session.commit()

  except Exception as e:
      logger.error(f'Error Funcion vientres_aptos: {e}')
      raise
  finally:
      session.close()