"""
@autor:odvr
el siguiente codigo realiza la creacion de las tablas que se ge
"""
#librerias requeridas
from sqlalchemy import Table,Column
#importacion del cong para la conexion con la base de datos
from config.db  import meta,engine
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, String, DateTime

"""
 Modelo para la tabla de Bovinos
 cuenta una relacion de uno a muchos para las siguientes tablas: 
 sexo
  
"""
modelo_bovinos_inventario = Table("bovinos", meta, Column("id_bovino", Integer, primary_key=True),
                                  Column("fecha_nacimiento", DateTime),
                                  Column("sexo_id", Integer,ForeignKey("sexo.id_sexo")),
                                  Column("raza", String(300)),
                                  Column("peso", Integer),
                                  Column("marca", String(300)),
                                  Column("id_proposito", Integer,ForeignKey("proposito.id_proposito")),
                                  Column("id_mansedumbre", Integer,ForeignKey("mansedumbre.id_mansedumbre")),
                                  Column("id_estado", Integer,ForeignKey("estado.id_estado")))

"""
modelo de columnas para definir el sexo
"""

modelo_sexo = Table("sexo", meta, Column("id_sexo", Integer, primary_key=True),
                                  Column("descri_sexo", String(300)))


"""
Modelo para el proposito de los animales

"""
modelo_proposito = Table("proposito", meta, Column("id_proposito", Integer, primary_key=True),
                                  Column("descri_proposito", String(300)))



"""
"""
modelo_estado = Table("estado", meta, Column("id_estado", Integer, primary_key=True),
                                  Column("descri_estado", String(300)))


modelo_estado = Table("mansedumbre", meta, Column("id_mansedumbre", Integer, primary_key=True),
                                  Column("descri_mansedumbre", String(300)))


modelo_ceba = Table("produccion_ceba", meta, Column("id_ceba", Integer, primary_key=True),
                                  Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),
                                  Column("id_proposito", Integer,ForeignKey("proposito.id_proposito")),Column("estado_optimo_ceba", String(300)))


modelo_levante = Table("produccion_levante", meta, Column("id_levante", Integer, primary_key=True),
                                  Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),
                                  Column("id_proposito", Integer,ForeignKey("proposito.id_proposito")),Column("estado_optimo_levante", String(300)))

modelo_leche = Table("produccion_leche", meta, Column("id_leche", Integer, primary_key=True),
                                  Column("prod_lactancia",Integer),
                                  Column("dura_lactancia",String(300)),
                                  Column("fecha_inicial_ordeno",DateTime),
                                  Column("fecha_fin_ordeno",DateTime),
                                  Column("num_partos",Integer),
                                  Column("id_proposito", Integer,ForeignKey("proposito.id_proposito")),
                                  Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),
                                  Column("tipo_parto", Integer,ForeignKey("tipo_parto.id_tipo_parto")),
                                  Column("datos_prenez", Integer,ForeignKey("datos_prenez.id_datos_prenez"))
                     )
modelo_tipo_parto = Table("tipo_parto", meta, Column("id_tipo_parto", Integer, primary_key=True),
                                  Column("descri_tipo_parto", String(300)))

modelo_datos_prenez = Table("datos_prenez", meta, Column("id_datos_prenez", Integer, primary_key=True),
                                  Column("descri_datos_prenez", String(300)))

modelo_datos_muerte = Table("datos_muerte", meta, Column("id_datos_muerte", Integer, primary_key=True),
                                  Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),
                                  Column("id_estado", Integer,ForeignKey("estado.id_estado")),Column("razon_muerte", String(300)),Column("fecha_muerte", DateTime))


modelo_arbol_genialogico = Table("arbol_genialogico", meta, Column("id_arbol_genialogico", Integer, primary_key=True),
                                  Column("id_bovino_madre", Integer,ForeignKey("bovinos.id_bovino")),
                                  Column("id_bovino_padre", Integer,ForeignKey("bovinos.id_bovino")),Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),

                                  )

meta.create_all(engine)


