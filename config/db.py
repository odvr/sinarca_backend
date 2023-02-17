'''
@autor: odvr

El siguiente codigo realiza la conexion de la base de datos para mariaDB

'''
#Librerias requeridas
from  sqlalchemy import create_engine,MetaData
import sqlalchemy

"""
Registra tu base de datos siguiendo los parametros en el ejemplo:
mariadb+mariadbconnector://usuario:password@IPbasededatos:puerto/nombreBasededatos"
"""
try:
    engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@localhost:3306/sinarca")
    meta = MetaData()
    # llama esta variable cuando quieras interactuar con la base de datos
    condb = engine.connect()
except:
    print("Valida las credenciales de la base de datos"+condb)








