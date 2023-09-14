'''
@autor: odvr

El siguiente codigo realiza la conexion de la base de datos para mariaDB

'''
#Librerias requeridas
from  sqlalchemy import create_engine,MetaData
import sqlalchemy
from sqlalchemy.orm import sessionmaker

"""
Registra tu base de datos siguiendo los parametros en el ejemplo:
mariadb+mariadbconnector://usuario:password@IPbasededatos:puerto/nombreBasededatos"
"""
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@sinarcadb.cc3ho0ocanpp.us-east-1.rds.amazonaws.com:3306/sinarca")
meta = MetaData()
def get_session():
    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@sinarcadb.cc3ho0ocanpp.us-east-1.rds.amazonaws.com:3306/sinarca")
    try:

        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except Exception as e:
        raise e













