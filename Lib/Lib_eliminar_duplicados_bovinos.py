"""

@autor : odvr

"""

from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_ceba, modelo_levante
import logging
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


'''
Eliminar duplicados
'''
def eliminarduplicados(db: Session ):
    #consulta_ceba = condb.execute(modelo_bovinos_inventario.select().
                        #where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    itemsCeba = db.execute(modelo_ceba.select()).all()


    for i in itemsCeba:
        proposito = i[5]
        id = i[0]
        if proposito == 'Leche':
            db.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            db.commit()
        if proposito == 'Levante':
            db.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            db.commit()
    itemsLevante = db.execute(modelo_levante.select()).all()
    for i in itemsLevante:
        proposito = i[5]
        idle = i[0]
        if proposito == 'Leche':
            db.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            db.commit()
        if proposito == 'Ceba':
            db.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            db.commit()

