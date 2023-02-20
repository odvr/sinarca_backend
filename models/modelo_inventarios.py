"""
@autor:odvr
el siguiente codigo realiza la creacion de la tabla inventarios
"""
#librerias requeridas
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String,DateTime
#importacion del cong para la conexion con la base de datos
from config.db  import meta,engine

from datetime import date

#Crea las tablas de los bovinos utilizando la libreria sqlalchemy
modelo_bovinos_inventario = Table("inventario_bovino",meta, Column("cod_bovino",Integer,primary_key=True),
                       Column("fecha_nacimiento",DateTime),
                       Column("sexo",Integer),
                       Column("raza",String(300)),
                       Column("peso",Integer),
                       Column("marca",String(300)),
                       Column("cod_proposito",Integer),
                       Column("mansedumbre",Integer),
                       Column("cod_estado",Integer))

meta.create_all(engine)