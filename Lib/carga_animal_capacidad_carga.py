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
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_arbol_genealogico, modelo_lotes_bovinos, modelo_registro_ocupaciones_potreros
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
              # Toma el nombre del lote del animal en este caso es el campo 18
              nombre_lote = i[18]

              # determinacion de la unidad animal (una unidad animal equivale a 400 kg de peso vivo)
              unidad_animal = peso / 400
              # determinacion del consumo de forraje vivo por animal (cada animal consume un 10% de su peso vivo al dia)
              consumo_forraje = peso * 0.1

              #El siguiente codigo busca el id del lote y actuliza el campo

              consultarLote = session.query(modelo_lotes_bovinos.c.id_lote_bovinos).filter(
                  modelo_lotes_bovinos.columns.nombre_lote == nombre_lote,
                  modelo_lotes_bovinos.c.usuario_id == current_user).first()

              if consultarLote is None:
                  pass
              else:
                  session.execute(modelo_carga_animal_y_consumo_agua.update().values(id_lote=consultarLote[0],
                                                                                     nombre_lote=nombre_lote). \
                                  where(modelo_carga_animal_y_consumo_agua.columns.id_bovino == id))
                  session.commit()

              # consulta que determina si el bovino ya existe en la tabla
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
          where(modelo_capacidad_carga.c.medicion_aforo != None,
                modelo_capacidad_carga.c.id_lote != None,
                modelo_capacidad_carga.c.usuario_id == current_user).all()
    for i in consulta_aforo:
        # Toma el resultado del aforo (campo 1)
        # el aforo determina cuantos kilogramos de materia seca produce un metro cuadrado de pasto en el predio
        aforo = i[1]
        # Toma el id del poteror o aforo realizado (campo)
        id_capacidad = i[0]
        # Toma la cantidad de hectareas que posee el usuario(campo 2)
        hectareas_predio = i[2]
        # Toma el periodo de ocupacion
        # Toma el lote
        id_lote = i[8]
        # Toma la fecha de incio de ocupacion
        fecha_inicio_ocupacion = i[11]
        # al ingresar un lote, se considera en ocupacion o uso
        estado="En Uso"

        consultarLote = session.query(modelo_lotes_bovinos.c.nombre_lote).filter(
            modelo_lotes_bovinos.columns.id_lote_bovinos == id_lote,
            modelo_lotes_bovinos.c.usuario_id == current_user).first()

        #el siguiente codigo consulta el nombre del lote
        if consultarLote is None:
            pass
        else:
            session.execute(modelo_capacidad_carga.update().values(nombre_lote=consultarLote[0]). \
                            where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
            session.commit()



        #se convierten las hectareas a metros
        metros_predio=hectareas_predio*10000

        #se calcula la disponibilidad se forraje (se obtienen en Kg por metro cuadrado).
        #adicionalmente se utliza un factor de uso del 60% (solo se tuliza 60% del pasto)
        #pues se pierde pasto por zonas de descanso, excretas, pisadas, etc..

        factor_uso=0.6
        forraje_verde_disponible=(metros_predio*(aforo/1000))*factor_uso

        #se conoce que una nimal come entre el 12 al 15% de su pso vivo en forraje
        #un vaca de 400 kilos comeria entre 48 a 60 kilos de forraje verde al dia
        #se utiliza un promedrio de 54 kg

        consumo_promedio=54

        #Se obtiene la carga animal del lote seleccionado
        consulta_carga_lote= session.query(func.sum(modelo_carga_animal_y_consumo_agua.c.valor_unidad_animal)). \
          filter(modelo_carga_animal_y_consumo_agua.c.usuario_id == current_user,
                 modelo_carga_animal_y_consumo_agua.c.id_lote == id_lote).first()

        if consulta_carga_lote[0]==None:
            pass
        else:
            consumo_lote = consulta_carga_lote[0] * consumo_promedio

            capacidad_carga_animal_ajustada = (forraje_verde_disponible / consumo_lote)
            # se obtienen lod dias de ocupacion que podra estar el lote en el predio
            ocupacion = round(capacidad_carga_animal_ajustada, 0)

            # se asigna una interpretacion dependiendo de la cantidad de dias de ocupacion

            if ocupacion < 1:
                interpretacion = f'Este Lote puede permanecer menos de un día en este predio, por favor, reconsidera cambiarlo a un lote con más forraje disponible'
                # actualizacion de campos
                session.execute(modelo_capacidad_carga.update().values(interpretacion=interpretacion,
                                                                       carga_animal_usuario=consulta_carga_lote[0],
                                                                       estado=estado). \
                                where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
                session.commit()


            else:
                interpretacion = f'Puedes tener este Lote hasta {ocupacion} días en este predio'
                # actualizacion de campos
                session.execute(modelo_capacidad_carga.update().values(interpretacion=interpretacion,
                                                                       carga_animal_usuario=consulta_carga_lote[0],
                                                                       periodo_ocupacion=ocupacion,
                                                                       estado=estado). \
                                where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
                session.commit()

            # el siguiente codigo determina la fecha recomendada de duracion de la ocupacion
            fecha_final_recomendada = fecha_inicio_ocupacion + timedelta(ocupacion)
            session.execute(modelo_capacidad_carga.update().values(fecha_final_recomendada=fecha_final_recomendada). \
                            where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
            session.commit()





  except Exception as e:
      logger.error(f'Error Funcion capacidad_carga: {e}')
      raise
  finally:
      session.close()




def finalizar_ocupacion(id_capacidad, session: Session):
    try:
        consulta_capacidad=session.query(modelo_capacidad_carga).\
          filter(modelo_capacidad_carga.c.id_capacidad==id_capacidad).all()

        if consulta_capacidad is None:
            pass
        else:
            for i in consulta_capacidad:
                id_lote = i[8]
                nombre_lote= i[9]
                nombre_potrero= i[6]
                fecha_inicio_ocupacion=i[11]
                fecha_final_recomendada=i[12]
                fecha_final_real=i[13]
                dias_descanso=i[16]
                usuario_id=i[5]


                var1 = 1
                fecha_inicio_descanso = fecha_final_real + timedelta(var1)

                fecha_final_descanso = fecha_inicio_descanso + timedelta(dias_descanso)
                estado = "En descanso"
                valor_vacio = None

                #si un predio ya ha pasado su tiempo de descanso, se actualizaran sus valores y estados (estara en descanso)
                session.execute(
                    modelo_capacidad_carga.update().values(medicion_aforo=valor_vacio, hectareas_predio=valor_vacio,
                                                           carga_animal_usuario=valor_vacio,
                                                           interpretacion=valor_vacio, id_lote=valor_vacio,
                                                           nombre_lote=valor_vacio, estado=estado,
                                                           fecha_inicio_ocupacion=valor_vacio,
                                                           periodo_ocupacion=valor_vacio,
                                                           fecha_final_recomendada=valor_vacio,
                                                           fecha_final_real=valor_vacio,
                                                           fecha_inicio_descanso=fecha_inicio_descanso,
                                                           fecha_final_descanso=fecha_final_descanso). \
                    where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
                session.commit()

                if fecha_final_real > fecha_final_recomendada :
                    observacion = "Ocupación más larga de la fecha recomendada"
                    ingresoRegistro = modelo_registro_ocupaciones_potreros.insert().values(id_potrero=id_capacidad,
                                                                                           nombre_potrero=nombre_potrero,
                                                                                           id_lote=id_lote,
                                                                                           nombre_lote=nombre_lote,
                                                                                           fecha_inicio_ocupacion=fecha_inicio_ocupacion,
                                                                                           fecha_final_recomendada=fecha_final_recomendada,
                                                                                           fecha_final_real=fecha_final_real,
                                                                                           observacion=observacion,usuario_id=usuario_id)

                    session.execute(ingresoRegistro)
                    session.commit()
                else:
                    observacion = "tiempo de Ocupación correcto "
                    ingresoRegistro = modelo_registro_ocupaciones_potreros.insert().values(id_potrero=id_capacidad,
                                                                                           nombre_potrero=nombre_potrero,
                                                                                           id_lote=id_lote,
                                                                                           nombre_lote=nombre_lote,
                                                                                           fecha_inicio_ocupacion=fecha_inicio_ocupacion,
                                                                                           fecha_final_recomendada=fecha_final_recomendada,
                                                                                           fecha_final_real=fecha_final_real,
                                                                                           observacion=observacion,usuario_id=usuario_id)

                    session.execute(ingresoRegistro)
                    session.commit()






    except Exception as e:
        logger.error(f'Error Funcion finalizar_ocupacion:{e}')
        raise
    finally:
        session.close()


def actualizar_estados_ocupacion(session:Session,current_user):
  try:
    # consulta del resultado del aforo
    consulta_potreros = session.query(modelo_capacidad_carga). \
          where(modelo_capacidad_carga.c.estado == "En descanso",
                modelo_capacidad_carga.c.usuario_id == current_user).all()
    for i in consulta_potreros:
        id_capacidad = i[0]
        fecha_final_descanso = i[15]

        fecha_actual= date.today()

        estado="Disponible"

        if fecha_actual>fecha_final_descanso:
            session.execute(modelo_capacidad_carga.update().values(estado=estado). \
                            where(modelo_capacidad_carga.columns.id_capacidad == id_capacidad))
            session.commit()

        else:
            pass
  except Exception as e:
      logger.error(f'Error Funcion actualizar_estados_ocupacion: {e}')
      raise
  finally:
      session.close()


"la siguiente funcione tiene como objetivo eliminar un registro de capacidad de carga"

def eliminacion_capacidad_carga(id_capacidad_eliminar, session: Session):
    try:
        consulta_capacidad=session.query(modelo_capacidad_carga).\
          filter(modelo_capacidad_carga.c.id_capacidad==id_capacidad_eliminar).all()
        if consulta_capacidad is None:
            pass
        else:

            session.execute(modelo_capacidad_carga.delete().where(modelo_capacidad_carga.c.id_capacidad==id_capacidad_eliminar))

            session.commit()

    except Exception as e:
        logger.error(f'Error Funcion eliminacion_capacidad_carga:{e}')
        raise
    finally:
        session.close()
