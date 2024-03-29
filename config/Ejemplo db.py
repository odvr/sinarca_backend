'''
@autor: odvr

El siguiente codigo realiza la conexion de la base de datos para mariaDB

Versión del producto V.1.0.1

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
Configuaración del Correo
"""

remitente = 'rutaganadera.co@gmail.com'
password = 'ppxg ldje ckty ktmd'
servidor_smtp = 'smtp.gmail.com'
puerto_smtp = 587


"""
Registra tu base de datos siguiendo los parametros en el ejemplo:
mariadb+mariadbconnector://usuario:password@IPbasededatos:puerto/nombreBasededatos"
"""
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@localhost:3306/sinarca")
meta = MetaData()
def get_session():
    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@localhost:3306/sinarca")
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        return session
    except Exception as e:
        logger.error(f'Error al Conectar la Base de datos: {e}')
        raise e
"""
Se incluye la ruta base para realizar la eliminación del path fisico de las Imagenes de Perfil
Ejemplo Windowns Rutabase = "C:/Users/ovega/Desktop/Gana/Ganaderia_Sinarca/sinarca_backend"
Ejemplo Linux Rutabase = "/app"

"""

Rutabase = "/app"









