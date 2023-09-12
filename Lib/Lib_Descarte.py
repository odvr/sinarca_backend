from sqlalchemy.orm import Session
import logging
from models.modelo_bovinos import modelo_descarte, modelo_bovinos_inventario
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

"""la siguiente funcion trae los campos de edad y peso de cada animal
a los animales de descarte"""
def descarte(db: Session ):
  try:
      # join de tablas
    consulta_animales = db.query(modelo_descarte.c.id_bovino, modelo_bovinos_inventario.c.edad,
                            modelo_bovinos_inventario.c.peso).\
        join(modelo_descarte, modelo_descarte.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    for i in consulta_animales:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[2]
        # actualizacion de campos
        db.execute(modelo_descarte.update().values( edad=edad,
                                                      peso=peso). \
                        where(modelo_descarte.columns.id_bovino == id))
        logger.info(f'Funcion descarte {peso} ')
        db.commit()
  except Exception as e:
     logger.error(f'Error Funcion descarte: {e}')
     raise
  finally:
     db.close()