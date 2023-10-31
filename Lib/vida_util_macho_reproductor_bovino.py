
"""

@autor : odvr

"""
from sqlalchemy import update
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_macho_reproductor, modelo_vientres_aptos, \
    modelo_indicadores, modelo_leche
import logging
import math
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


"""la siguiente funncion la fecha en que un macho empezara a bajar fertilidad, para ello
 suma los dias de vida util con la edad del animal para determinar este campo"""
def vida_util_macho_reproductor(db: Session,current_user):
 try:
     #join con tabla de bovinos y consulta

    consulta_machos_r = db.query(modelo_macho_reproductor.c.id_bovino,modelo_bovinos_inventario.c.edad,modelo_bovinos_inventario.c.peso,
                          modelo_bovinos_inventario.c.estado,modelo_bovinos_inventario.c.fecha_nacimiento).\
        join(modelo_macho_reproductor,modelo_bovinos_inventario.c.id_bovino == modelo_macho_reproductor.c.id_bovino).\
        filter(modelo_macho_reproductor.c.usuario_id==current_user).all()


    # Recorre los campos de la consulta
    for i in consulta_machos_r:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[2]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[3]
        # Toma la fecha de nacimiento en este caso es el campo 4
        fecha_nacimiento = i[4]
        # calculo de la vida util mediante la suma del promedio de vida util con la fecha de nacimiento
        fecha_vida_util = fecha_nacimiento + timedelta(2555)
        # actualizacion del campo
        db.execute(modelo_macho_reproductor.update().values(edad=edad, peso=peso, estado=estado,
                                                     fecha_vida_util=fecha_vida_util). \
                      where(modelo_macho_reproductor.columns.id_bovino == id))

        db.commit()
 except Exception as e:
   logger.error(f'Error Funcion vida_util_macho_reproductor: {e}')
   raise
 finally:
  db.close()

"""la siguiente funncion determina si la cantidad de machos reproductores es suficiente
o demasiada para las hembras que se pueden preñar """
def relacion_macho_reproductor_vientres_aptos(db: Session, current_user):
  #la siguiente variable debe ser global ya que esta dentro de un bucle if anidado
  global interpretacion
  try:
    # consulta y conteo de toros reproductores vivos
    cantidad_reproductores = db.query(modelo_macho_reproductor). \
        where(modelo_macho_reproductor.columns.estado == "Vivo").\
        filter(modelo_macho_reproductor.c.usuario_id==current_user).count()

    # consulta y conteo de vientres aptos vivos
    cantidad_vientres_aptos = db.query(modelo_leche.c.id_bovino,modelo_bovinos_inventario.c.edad,
                                        modelo_bovinos_inventario.c.peso, modelo_bovinos_inventario.c.raza). \
          join(modelo_leche, modelo_bovinos_inventario.c.id_bovino==modelo_leche.c.id_bovino).\
          where(modelo_bovinos_inventario.c.estado=="Vivo").\
          filter(modelo_leche.columns.tipo_ganado != "Hembra de levante",
                  modelo_leche.columns.usuario_id==current_user).count()

    if cantidad_vientres_aptos==0 or cantidad_vientres_aptos is None:
        relacion =0
        interpretacion= f'No posees ninguna hembra apta para reproducirse'
        # actualizacion de campo de cantidad de vientres aptos
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vientres_aptos=cantidad_vientres_aptos,
                               relacion_toros_vientres_aptos=relacion,
                               interpretacion_relacion_toros_vientres_aptos=interpretacion))
    else:
        # calculo de la relacion toros-vientres
        relacion = (cantidad_reproductores / cantidad_vientres_aptos) * 100
        # caclulo de cantidad recomendada de reproductores para la cantidad de vientres aptos
        cantidad_recomendada = math.ceil(cantidad_vientres_aptos / 25)
        # interpretacion del calculo de la relacion toros-vientres
        if relacion < 4:
            interpretacion = f'no Tienes suficientes machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
        elif relacion > 4:
            if cantidad_reproductores == 1 and cantidad_vientres_aptos <= 25:
                interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} macho reproductor para tus {cantidad_vientres_aptos} hembras aptas'
            elif cantidad_reproductores > 1 and cantidad_vientres_aptos <= 25:
                interpretacion = f'Tienes demasiados machos reproductores, debes tener solamente un macho reproductor para tus {cantidad_vientres_aptos} hembras aptas '
            else:
                interpretacion = f'Tienes demasiados machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
        elif relacion == 4:
            interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas'
        # actualizacion de campo de cantidad de vientres aptos
        db.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == current_user).
                        values(vientres_aptos=cantidad_vientres_aptos,
                               relacion_toros_vientres_aptos=relacion,
                               interpretacion_relacion_toros_vientres_aptos=interpretacion))

        db.commit()
  except Exception as e:
      logger.error(f'Error Funcion relacion_macho_reproductor_vientres_aptos: {e}')
      raise
  finally:
      db.close()
  return (relacion, interpretacion, cantidad_vientres_aptos)
