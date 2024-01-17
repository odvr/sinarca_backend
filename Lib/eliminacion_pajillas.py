'''
Librerias requeridas
@autor : odvr
'''
import logging

# importa la conexion de la base de datos
from sqlalchemy.orm import Session

# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_arbol_genealogico, modelo_registro_pajillas

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


def eliminacion_pajilla(id_pajilla_eliminar, session: Session):
    try:
        consulta_pajilla=session.query(modelo_registro_pajillas).\
          filter(modelo_registro_pajillas.c.id_pajillas==id_pajilla_eliminar).all()
        if consulta_pajilla is None:
            pass
        else:
            session.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino_padre == id_pajilla_eliminar).filter(modelo_arbol_genealogico.c.inseminacion=="Si"))

            session.execute(modelo_registro_pajillas.delete().where(modelo_registro_pajillas.c.id_pajillas == id_pajilla_eliminar))

            session.commit()


    except Exception as e:
        logger.error(f'Error Funcion eliminacion_pajilla:{e}')
        raise
    finally:
        session.close()

