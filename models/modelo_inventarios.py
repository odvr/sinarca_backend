from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from config.db  import meta,engine

#Crea las tablas de los bovinos utilizando la libreria sqlalchemy
modelo_bovinos = Table("bovinos",meta, Column("id",Integer,primary_key=True),
                       Column("raza",String(60)),
                       Column("sexo",String(60)),
                       Column("edad",Integer),
                       Column("peso",Integer),
                       Column("proposito",String(100)),
                       Column("marca",String(3)),
                       Column("procedencia",String(100)),
                       Column("observaciones",String(100)))
#modelo_bovinos = Table("bovinos",meta, Column("id",Integer,primary_key=True),Column("raza",String(60)))
# engien es la constante que realiza la coneccion con la base de datos
meta.create_all(engine)