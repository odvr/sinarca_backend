'''
@autor: odvr

El siguiente codigo realiza la conexion de la base de datos para mariaDB

'''
#Librerias requeridas
import logging
from  sqlalchemy import create_engine,MetaData
import sqlalchemy
from sqlalchemy.orm import sessionmaker
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


"""
Registra tu base de datos siguiendo los parametros en el ejemplo:
mariadb+mariadbconnector://usuario:password@IPbasededatos:puerto/nombreBasededatos"
"""
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:t&G2aL#p9B#z@3.87.217.60:3306/sinarca")
meta = MetaData()
def get_session():
    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:t&G2aL#p9B#z@3.87.217.60:3306/sinarca")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        return session
    except Exception as e:
        logger.error(f'Error al Conectar la Base de datos: {e}')
        raise e













