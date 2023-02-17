"""
@autor:odvr
el siguiente codigo realiza la creacion de la tabla inventarios
"""
#librerias requeridas
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime
#importacion del cong para la conexion con la base de datos
from config.db  import meta,engine

#Crea las tablas de los bovinos utilizando la libreria sqlalchemy
modelo_bovinos_inventario = Table("inventario_bovino",meta, Column("id_inven_Bovino",Integer,primary_key=True),
                       Column("raza",String(100)),
                       Column("sexo",String(100)),
                       Column("edad",Integer),
                       Column("peso",Integer),
                       Column("marca",String(100)),
                       Column("lugar_Procedencia",String(100)),
                       Column("fecha_nacimiento",Integer),
                       Column("Mansedumbre",String(100)))
#modelo_bovinos = Table("bovinos",meta, Column("id",Integer,primary_key=True),Column("raza",String(60)))
# engien es la constante que realiza la coneccion con la base de datos
meta.create_all(engine)