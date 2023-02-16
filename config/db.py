
#Librerias requeridas
from  sqlalchemy import create_engine,MetaData
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
"""
create_engine requiere una URL
donde se encuentren las credenciales 
Registra las credenciales de la base de datos ejempo mysql+pymysql://usuario:password@rutaDB
"""
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:1q2w3e4r@localhost:3306/sinarca")
meta = MetaData()
#llama esta variable cuando quieras interactuar con la base de datos
condb = engine.connect()







