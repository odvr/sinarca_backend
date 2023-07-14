'''
Librerias requeridas
@autor : odvr
'''
from sqlalchemy.testing.plugin.plugin_base import logging
import logging



# importa la conexion de la base de datos
from config.db import session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_ceba, modelo_macho_reproductor, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_arbol_genealogico, modelo_historial_intervalo_partos, modelo_litros_leche, modelo_orden_IEP, \
    modelo_orden_litros, \
    modelo_orden_peso, modelo_historial_partos

'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

"""la siguiente funcion tiene como objetivo eliminar el bovino que se desee"""
def eliminacionBovino(id_bov_eliminar):
  try:
      #consulta de id de parametro en la base de datos
      #consulta de bovino en la tabla de inventario
      consulta_bovino_inventario = session.query(modelo_bovinos_inventario).\
          filter( modelo_bovinos_inventario.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_inventario ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de produccion leche
      consulta_bovino_leche = session.query(modelo_leche).\
          filter( modelo_leche.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_leche ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_leche.delete().where(modelo_leche.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de arbol genealogico
      consulta_bovino_arbol = session.query(modelo_arbol_genealogico).\
          filter(modelo_arbol_genealogico.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_arbol ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de carga animal
      consulta_bovino_muerte = session.query(modelo_datos_muerte). \
              filter(modelo_datos_muerte.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_muerte == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_datos_muerte.delete().where(modelo_datos_muerte.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de descarte
      consulta_bovino_descarte = session.query(modelo_descarte).\
          filter(modelo_descarte.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_descarte ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_descarte.delete().where(modelo_descarte.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de historial de partos
      consulta_bovino_parto = session.query(modelo_partos).\
          filter(modelo_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_parto ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_partos.delete().where(modelo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de intervalo entre partos
      consulta_bovino_intervalo = session.query(modelo_historial_intervalo_partos).\
          filter(modelo_historial_intervalo_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_intervalo ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_historial_intervalo_partos.delete().where(modelo_historial_intervalo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de litros de leche
      consulta_bovino_litros = session.query(modelo_litros_leche).\
          filter(modelo_litros_leche.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_litros ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_litros_leche.delete().where(modelo_litros_leche.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de macho reproductor
      consulta_bovino_reproductor = session.query(modelo_macho_reproductor). \
          filter(modelo_macho_reproductor.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_reproductor == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_macho_reproductor.delete().where(modelo_macho_reproductor.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por IEP
      consulta_bovino_orden_IEP = session.query(modelo_orden_IEP). \
          filter(modelo_orden_IEP.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_IEP == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_IEP.delete().where(modelo_orden_IEP.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por litros
      consulta_bovino_orden_litros = session.query(modelo_orden_litros). \
          filter(modelo_orden_litros.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_litros == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_litros.delete().where(modelo_orden_litros.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por peso
      consulta_bovino_orden_peso = session.query(modelo_orden_peso). \
          filter(modelo_orden_peso.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_peso == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_peso.delete().where(modelo_orden_peso.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de partos
      consulta_bovino_registro_partos = session.query(modelo_partos). \
          filter(modelo_partos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_registro_partos == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_partos.delete().where(modelo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de ceba
      consulta_bovino_ceba = session.query(modelo_ceba). \
          filter(modelo_ceba.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_ceba == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_ceba.delete().where(modelo_ceba.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de levante
      consulta_bovino_levante = session.query(modelo_levante). \
          filter(modelo_levante.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_levante == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_levante.delete().where(modelo_levante.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de ventas
      consulta_bovino_venta = session.query(modelo_ventas). \
          filter(modelo_ventas.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_venta == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_ventas.delete().where(modelo_ventas.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de veterinaria
      consulta_bovino_veterinaria = session.query(modelo_veterinaria). \
          filter(modelo_veterinaria.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_veterinaria == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_veterinaria.delete().where(modelo_veterinaria.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de vientres aptos
      consulta_bovino_vientre = session.query(modelo_vientres_aptos). \
          filter(modelo_vientres_aptos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_vientre == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de partos
      consulta_bovino_partos_historial = session.query(modelo_historial_partos).\
          filter(modelo_historial_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_partos_historial ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_historial_partos.delete().where(modelo_historial_partos.c.id_bovino == id_bov_eliminar))
          session.commit()
      session.commit()
  except Exception as e:
      logger.error(f'Error Funcion eliminacionBovino:{e}')
      raise
  finally:
      session.close()

