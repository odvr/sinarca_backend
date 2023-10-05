'''
Librerias requeridas

@autor : odvr

'''

import logging
from http.client import HTTPException

from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia
from Lib.funcion_IEP_por_raza import IEP_por_raza
from Lib.Lib_Intervalo_Partos import intervalo_partos, promedio_intervalo_partos
from Lib.funcion_litros_leche import promedio_litros_leche
from Lib.funcion_litros_por_raza import litros_por_raza
from Lib.funcion_peso_por_raza import peso_segun_raza
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario,modelo_veterinaria, modelo_leche, modelo_levante,modelo_ventas,modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua,modelo_datos_pesaje, \
    modelo_capacidad_carga,  modelo_arbol_genealogico
from schemas.schemas_bovinos import Esquema_bovinos,User, esquema_produccion_leche, esquema_produccion_levante,TokenSchema,esquema_descarte, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func, null
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta


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

def carga_animal(session:Session,current_user):
  try:
      # join  tabla de bovinos y tabla de carga animal
      consulta_bovinos = session.query(modelo_bovinos_inventario).\
          filter(modelo_bovinos_inventario.c.estado=="Vivo",
                 modelo_bovinos_inventario.columns.usuario_id==current_user).all()
      if consulta_bovinos==[]:
          pass
      else:
          # Recorre los campos de la consulta
          for i in consulta_bovinos:
              # Toma el ID del bovino en este caso es el campo 0
              id = i[0]
              # Toma la edad del animal en este caso es el campo 2
              edad = i[2]
              # Toma el peso del animal en este caso es el campo 5
              peso = i[5]
              # Toma la raza del animal en este caso es el campo 2
              raza = i[4]
              # determinacion de la unidad animal (una unidad animal equivale a 400 kg de peso vivo)
              unidad_animal = peso / 400
              # determinacion del consumo de forraje vivo por animal (cada animal consume un 10% de su peso vivo al dia)
              consumo_forraje = peso * 0.1
              # consulta que determina su el bovino ya existe en la tabla
              consulta_existencia_bovino = session.query(modelo_carga_animal_y_consumo_agua). \
                  filter(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id).all()
              if consulta_existencia_bovino == []:
                  ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(
                      id_bovino=id,
                      edad=edad,
                      peso=peso,
                      raza=raza,
                      valor_unidad_animal=unidad_animal,
                      consumo_forraje_vivo=consumo_forraje)
                  session.execute(ingresoCargaAnimal)
                  session.commit()
              else:
                  session.execute(modelo_carga_animal_y_consumo_agua.update().values(edad=edad,
                                                                                     peso=peso,
                                                                                     raza=raza,
                                                                                     valor_unidad_animal=unidad_animal,
                                                                                     consumo_forraje_vivo=consumo_forraje). \
                                  where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                  session.commit()
              # actualizacion de datos (tener en cuenta animales muertos y vendidos)
              consulta_bovinos_modulo = session.query(modelo_bovinos_inventario.c.id_bovino,
                                                      modelo_bovinos_inventario.c.estado). \
                  join(modelo_carga_animal_y_consumo_agua,
                       modelo_bovinos_inventario.c.id_bovino == modelo_carga_animal_y_consumo_agua.c.id_bovino).\
                  filter(modelo_bovinos_inventario.columns.usuario_id==current_user).all()
              for i in consulta_bovinos_modulo:
                  # Toma el ID del bovino en este caso es el campo 0
                  id_bov = i[0]
                  # Toma el estado del bovino en este caso es el campo 1
                  estado_animal = i[1]
                  # bucle que elima o actuliza los datos de los bovinos
                  if estado_animal == "Muerto" or estado_animal == "Vendido":
                      session.execute(modelo_carga_animal_y_consumo_agua.delete().where(
                          modelo_carga_animal_y_consumo_agua.c.id_bovino == id_bov))
                      session.commit()
                  else:
                      pass
          # consulta de sumatoria de las unidades animales
          consulta_unidades_animales = session.query(
              func.sum(modelo_carga_animal_y_consumo_agua.columns.valor_unidad_animal)).\
              filter(modelo_carga_animal_y_consumo_agua.columns.usuario_id==current_user).all()
          for i in consulta_unidades_animales:
              # Toma la totalidad de unidades animales en este caso es el campo 0
              total_unidades_animales = i[0]
              # interpretacion y actualizacion del campo
              interpretacion = f'Tienes un total de {round((total_unidades_animales), 2)} unidades animales'
              session.execute(modelo_indicadores.update().values(total_unidades_animales=interpretacion). \
                              where(modelo_indicadores.columns.id_indicadores == current_user))
              session.commit()
          session.commit()
      session.commit()
  except Exception as e:
      logger.error(f'Error Funcion carga_animal: {e}')
      raise
  finally:
      session.close()


"""funcion de capacidad de carga"""

def capacidad_carga(session:Session,current_user):
  try:
    # consulta del resultado del aforo
    consulta_aforo = session.query(modelo_capacidad_carga). \
          where(modelo_capacidad_carga.c.id_capacidad == current_user).all()
    for i in consulta_aforo:
        # Toma el resultado del aforo (campo 1)
        # el aforo determina cuantos kilogramos de materia seca produce un metro cuadrado de pasto en el predio
        aforo = i[1]
        # Toma la cantidad de hectareas que posee el usuario(campo 2)
        hectareas_predio = i[2]
        # Toma el tipo de muestra el usuario(campo 3)
        tipo_aforo = i[3]
        # consulta de sumatoria de las unidades animales
        if aforo is None or aforo==0:
            interpertacion_capacidad = "No posees aforos registrados hasta el momento"
            carga_animal_recomendada = 0
            carga_animal_usuario = 0
            aforo_defecto=0
            hectareas_defecto=0
            tipo_de_muestra_defecto="Sin seleccionar"
            session.execute(modelo_capacidad_carga.update().values(medicion_aforo=aforo_defecto,
                                                                   tipo_de_muestra=tipo_de_muestra_defecto,
                                                                    hectareas_predio=hectareas_defecto,
                                                                   capacidad_carga=interpertacion_capacidad,
                                                                   carga_animal_recomendada=carga_animal_recomendada,
                                                                   carga_animal_usuario=carga_animal_usuario). \
                            where(modelo_capacidad_carga.columns.id_capacidad == current_user))
            session.commit()
        elif hectareas_predio is None or hectareas_predio==0:
            interpertacion_capacidad = "No posees aforos registrados hasta el momento"
            carga_animal_recomendada = 0
            carga_animal_usuario = 0
            aforo_defecto=0
            hectareas_defecto=0
            tipo_de_muestra_defecto="Sin seleccionar"
            session.execute(modelo_capacidad_carga.update().values(medicion_aforo=aforo_defecto,
                                                                   tipo_de_muestra=tipo_de_muestra_defecto,
                                                                    hectareas_predio=hectareas_defecto,
                                                                   capacidad_carga=interpertacion_capacidad,
                                                                   carga_animal_recomendada=carga_animal_recomendada,
                                                                   carga_animal_usuario=carga_animal_usuario). \
                            where(modelo_capacidad_carga.columns.id_capacidad == current_user))
            session.commit()
        elif tipo_aforo is None:
            interpertacion_capacidad = "No posees aforos registrados hasta el momento"
            carga_animal_recomendada = 0
            carga_animal_usuario = 0
            aforo_defecto=0
            hectareas_defecto=0
            tipo_de_muestra_defecto="Sin seleccionar"
            session.execute(modelo_capacidad_carga.update().values(medicion_aforo=aforo_defecto,
                                                                   tipo_de_muestra=tipo_de_muestra_defecto,
                                                                    hectareas_predio=hectareas_defecto,
                                                                   capacidad_carga=interpertacion_capacidad,
                                                                   carga_animal_recomendada=carga_animal_recomendada,
                                                                   carga_animal_usuario=carga_animal_usuario). \
                            where(modelo_capacidad_carga.columns.id_capacidad == current_user))
            session.commit()
        else:
            consulta_unidades_animales_usuario = session.query(
                func.sum(modelo_carga_animal_y_consumo_agua.columns.valor_unidad_animal)).\
                filter(modelo_capacidad_carga.columns.usuario_id == current_user).all()
            for i in consulta_unidades_animales_usuario:
                # Toma la totalidad de unidades animales en este caso es el campo 0
                total_unidades_animales = i[0]
                # se calula la carga animal (Unidades animales por hectarea) del usuario
                carga_animal_usuario = total_unidades_animales / hectareas_predio
                # determinacion de produccion de pasto por hectarea
                # conversion de hectareas del predio a metros cuadrados
                metros_predio = hectareas_predio * 10000
                # dependiendo de la seleccion de tipo de muestra o aforo varia el calculo de la capacidad de carga
                if tipo_aforo == "Pasto recien cortado":
                    # determinacion de la materia seca
                    # el porcentaje de humedad del pasto es 80% (tiene un 20% de materia seca)
                    materia_seca_por_metro_cuadrado = 0.2 * aforo
                    produccion_materia_seca = materia_seca_por_metro_cuadrado * metros_predio
                    # determinacion de la cantidad de unidades animales que esta produccion puede mantener al dia
                    # una unidad animal puede consumir hasta 16 kilos de materia seca al dia
                    capacidad_unidades_animales_dia = round((produccion_materia_seca / 16), 2)
                    interpertacion_capacidad = f'con tus hectareas de pasto, puedes mantener hasta {capacidad_unidades_animales_dia} unidades animales'
                    # calculo de carga animal recomendada (cuentas unidades animales puede soportar una hectarea)
                    materia_seca_por_hectarea = materia_seca_por_metro_cuadrado * 10000
                    carga_animal_recomendada = materia_seca_por_hectarea / 16
                    # actualizacion de campos
                    session.execute(modelo_capacidad_carga.update().values(capacidad_carga=interpertacion_capacidad,
                                                                           carga_animal_recomendada=carga_animal_recomendada,
                                                                           carga_animal_usuario=carga_animal_usuario). \
                                    where(modelo_capacidad_carga.columns.id_capacidad == current_user))
                    session.commit()

                elif tipo_aforo == "Materia seca":
                    # determinacion de la materia seca
                    # al tratarse de paso seco, la materia seca sera el mismo pasto seco
                    materia_seca_por_metro_cuadrado = aforo
                    produccion_materia_seca = materia_seca_por_metro_cuadrado * metros_predio
                    # determinacion de la cantidad de unidades animales que esta produccion puede mantener al dia
                    # una unidad animal puede consumir hasta 16 kilos de materia seca al dia
                    capacidad_unidades_animales_dia = round((produccion_materia_seca / 16), 2)
                    interpertacion_capacidad = f'con tus hectareas de pasto, puedes mantener hasta {capacidad_unidades_animales_dia} unidades animales'
                    # calculo de carga animal recomendada (cuentas unidades animales puede soportar una hectarea)
                    materia_seca_por_hectarea = materia_seca_por_metro_cuadrado * 10000
                    carga_animal_recomendada = materia_seca_por_hectarea / 16
                    # actualizacion de campos
                    session.execute(modelo_capacidad_carga.update().values(capacidad_carga=interpertacion_capacidad,
                                                                           carga_animal_recomendada=carga_animal_recomendada,
                                                                           carga_animal_usuario=carga_animal_usuario). \
                                    where(modelo_capacidad_carga.columns.id_capacidad == current_user))
                    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion capacidad_carga: {e}')
      raise
  finally:
      session.close()