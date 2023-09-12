from models.modelo_bovinos import modelo_bovinos_inventario, modelo_levante, modelo_ceba
import logging
from sqlalchemy.orm import Session
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

def Estado_Optimo_Levante(db: Session ):
  try:
    consulta_levante = db.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Levante")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_levante:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
        # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado=="Vivo":
          if peso >= 140 and edad in range(8, 13):
            estado_levante = "Estado Optimo"
          elif peso < 140 and edad in range(8, 13):
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos"
          elif peso < 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y menos de 8 meses de edad"
          elif peso < 140 and edad > 12:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y mas de 12 meses de edad, considera descartarlo"
          elif peso >= 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene menos de 8 meses de edad"
          else:
            estado_levante = "Estado NO Optimo, este animal tiene una edad mayor a 12 meses, considera pasarlo a ceba"
        elif estado=="Muerto":
            estado_levante= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_levante= "Este animal esta Vendido, no se puede calcular su estado"
        #actualizacion del campo
        db.execute(modelo_levante.update().values(edad=edad,peso=peso,estado=estado,
                      estado_optimo_levante=estado_levante).\
                      where(modelo_levante.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Levante {estado_levante} ')
        db.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Levante: {e}')
    raise
  finally:
      db.close()
         #return estado_levante
"""
la siguiente funcion determina si la condicion de un animal para
ceba es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 350 kg y edad de 24 a 36 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""



def Estado_Optimo_Ceba(db: Session):
  try:
    consulta_ceba = db.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_ceba:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
    # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado == "Vivo":
          if peso >= 350 and edad in range(24, 37):
            estado_ceba = "Estado Optimo"
          elif peso < 350 and edad in range(24, 37):
            estado_ceba = "Estado NO Optimo, este animal tiene un peso menor a 350 kilos"
          elif peso >= 350 and edad < 24:
             estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad"
          elif peso < 350 and edad < 24:
            estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad y menos de 350 kilos"
          else:
            estado_ceba = "Estado NO Optimo, este animal tiene una edad mayor a 36 meses"
        elif estado=="Muerto":
            estado_ceba= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_ceba= "Este animal esta Vendido, no se puede calcular su estado"
        # actualizacion del campo
    # actualizacion del campo
        db.execute(modelo_ceba.update().values(edad=edad,peso=peso,estado=estado,
                    estado_optimo_ceba=estado_ceba). \
                  where(modelo_ceba.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Ceba {estado_ceba} ')
        db.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Ceba: {e}')
    raise
  finally:
      db.close()