"""
@autor:odvr
el siguiente codigo realiza la creacion de las tablas que se ge
"""
#librerias requeridas
#,
from sqlalchemy import Table, Column, Date
#importacion del cong para la conexion con la base de datos
from config.db  import meta,engine
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, String, DateTime

"""
 Modelo para la tabla de Bovinos
 cuenta una relacion de uno a muchos para las siguientes tablas: 
 sexo
  
"""
modelo_bovinos_inventario = Table("bovinos", meta, Column("id_bovino", String(300), primary_key=True),
                                  Column("fecha_nacimiento", Date),
                                  Column("edad", Integer),
                                  Column("sexo", String(300)),
                                  Column("raza", String(300)),
                                  Column("peso", Integer),
                                  Column("marca", String(300)),
                                  Column("proposito", String(300)),
                                  Column("mansedumbre", String(300)),
                                  Column("estado", String(300)))

modelo_ceba = Table("produccion_ceba", meta, Column("id_ceba", Integer, primary_key=True),
                            Column("id_bovino", String(300),ForeignKey("bovinos.id_bovino")),
                            Column("edad", Integer),
                            Column("peso", Integer),
                            Column("estado", String(300)),
Column("proposito", String(300)),
                            Column("estado_optimo_ceba", String(300)))


modelo_levante = Table("produccion_levante", meta, Column("id_levante", Integer, primary_key=True),
                       Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                       Column("edad", Integer),
                       Column("peso", Integer),
                       Column("estado", String(300)),
Column("proposito", String(300)),
                       Column("estado_optimo_levante", String(300)))

modelo_leche = Table("produccion_leche", meta, Column("id_leche", Integer, primary_key=True),
                                  Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                                  Column("fecha_primer_parto", Date),
                                  Column("edad_primer_parto", Integer),
                                  Column("prod_lactancia",Integer),
                                  Column("dura_lactancia",Integer),
                                  Column("fecha_inicial_ordeno",Date),
                                  Column("fecha_fin_ordeno",Date),
                                  Column("num_partos",Integer),
                                  Column("tipo_parto", String(300)),
                                  Column("datos_prenez", String(300)),
                                  Column("fecha_ultimo_parto",Date),
                                  Column("fecha_ultima_prenez",Date),
                                  Column("dias_abiertos", Integer),
                                  Column("fecha_vida_util",Date),
                                  Column("ordeno", String(300)),
Column("proposito", String(300)),
                                  Column("promedio_litros", Integer),
                                  Column("litros_diarios", Integer))


modelo_datos_muerte = Table("datos_muerte", meta, Column("id_datos_muerte", Integer, primary_key=True),
                                  Column("id_bovino", String(300),ForeignKey("bovinos.id_bovino")),
                                  Column("razon_muerte", String(300)),
                                  Column("fecha_muerte", Date))


modelo_arbol_genialogico = Table("arbol_genialogico", meta, Column("id_arbol_genialogico", Integer, primary_key=True),
                                  Column("id_bovino", String(300),ForeignKey("bovinos.id_bovino")),
                                  Column("id_bovino_madre", Integer),
                                  Column("id_bovino_padre", Integer))
"""modelo para indicadores"""
modelo_indicadores = Table("indicadores", meta, Column("id_indicadores", Integer, primary_key=True),
                                  Column("perdida_de_terneros", Integer),
                                  Column("tasa_supervivencia", Integer),
                                  Column("total_animales", Integer),
                                  Column("vacas_prenadas_porcentaje", Integer),
                                  Column("animales_levante", Integer),
                                  Column("animales_ceba", Integer),
                                  Column("animales_leche", Integer),
                                  Column("vacas_prenadas", Integer),
                                  Column("vacas_vacias", Integer),
                                  Column("animales_fallecidos", Integer),
                                  Column("animales_vendidos", Integer),
                                  Column("machos", Integer),
                                  Column("hembras", Integer),
                                  Column("vacas_en_ordeno",Integer),
                                  Column("vacas_no_ordeno",Integer),
                                  Column("porcentaje_ordeno", Integer),
                                  Column("animales_rango_edades_0_9", Integer),
                                  Column("animales_rango_edades_9_12", Integer),
                                  Column("animales_rango_edades_12_24", Integer),
                                  Column("animales_rango_edades_24_36", Integer),
                                  Column("animales_rango_edades_mayor_36", Integer),
                                  Column("animales_optimos_levante", Integer),
                                  Column("animales_optimos_ceba", Integer) )
meta.create_all(engine)



