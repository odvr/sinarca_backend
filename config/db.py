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
try:
    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@localhost:3306/sinarcas")
    #Session = sessionmaker(engine)
    meta = MetaData()
    # llama esta variable cuando quieras interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()
    condb = Session()
except:
    print("Valida las credenciales de la base de datos")








