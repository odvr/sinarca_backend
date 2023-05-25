"""
@autor:odvr
el siguiente codigo realiza la creacion de las tablas que se ge
"""
import decimal

from pydantic.schema import Decimal
# librerias requeridas
# ,
from sqlalchemy import Table, Column, Date, Float
# importacion del cong para la conexion con la base de datos
from config.db import meta, engine
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, String, DateTime

""" id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)"""

modelo_users = Table("users", meta, Column("id", String(300), primary_key=True, unique=True, index=True),
                     Column("email", String(300), unique=True, index=True), Column("password", String(300)))

modelo_usuarios = Table("usuarios", meta, Column("id_usuario", String(300), primary_key=True, unique=True, index=True),
                     Column("full_name", String(300), unique=True, index=True), Column("hashed_password", String(300)))

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
                                  Column("peso", Float),
                                  Column("marca", String(300)),
                                  Column("proposito", String(300)),
                                  Column("mansedumbre", String(300)),
                                  Column("estado", String(300)),
                                  Column("descarte", String(300)))

modelo_ceba = Table("produccion_ceba", meta, Column("id_ceba", Integer, primary_key=True),
                    Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                    Column("edad", Integer),
                    Column("peso", Float),
                    Column("estado", String(300)),
                    Column("proposito", String(300)),
                    Column("estado_optimo_ceba", String(300)))




modelo_levante = Table("produccion_levante", meta, Column("id_levante", Integer, primary_key=True),
                       Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                       Column("edad", Integer),
                       Column("peso", Float),
                       Column("estado", String(300)),
                       Column("proposito", String(300)),
                       Column("estado_optimo_levante", String(300)))

modelo_leche = Table("produccion_leche", meta, Column("id_leche", Integer, primary_key=True),
                     Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                     Column("fecha_primer_parto", Date),
                     Column("edad_primer_parto", Integer),
                     Column("datos_prenez", String(300)),
                     Column("fecha_vida_util", Date),
                     Column("ordeno", String(300)),
                     Column("proposito", String(300)),
                     Column("promedio_litros", Float),
                     Column("num_partos", Integer),
                     Column("intervalo_entre_partos", Float))

modelo_datos_muerte = Table("datos_muerte", meta, Column("id_datos_muerte", Integer, primary_key=True),
                            Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                            Column("razon_muerte", String(300)),
                            Column("estado", String(300)),
                            Column("fecha_muerte", Date))

modelo_arbol_genealogico = Table("arbol_genealogico", meta, Column("id_arbol_genealogico", Integer, primary_key=True),
                                 Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                                 Column("id_bovino_madre", String(300), ForeignKey("bovinos.id_bovino")),
                                 Column("id_bovino_padre", String(300), ForeignKey("bovinos.id_bovino")),
                                 Column("abuelo_paterno", String(300)),
                                 Column("abuela_paterna", String(300)),
                                 Column("abuelo_materno", String(300)),
                                 Column("abuela_materna", String(300)),
                                 Column("bisabuelo_materno", String(300)),
                                 Column("bisabuelo_paterno", String(300)),
                                 Column("tipo_de_apareamiento", String(300)),
                                 Column("consanguinidad", Float),
                                 Column("notificacion", String(300)))
"""modelo para indicadores"""
modelo_indicadores = Table("indicadores", meta, Column("id_indicadores", Integer, primary_key=True),
                           Column("perdida_de_terneros", Float),
                           Column("tasa_supervivencia", Float),
                           Column("total_animales", Integer),
                           Column("vacas_prenadas_porcentaje", Float),
                           Column("animales_levante", Integer),
                           Column("animales_ceba", Integer),
                           Column("animales_leche", Integer),
                           Column("vacas_prenadas", Integer),
                           Column("vacas_vacias", Integer),
                           Column("animales_fallecidos", Integer),
                           Column("animales_vendidos", Integer),
                           Column("machos", Integer),
                           Column("hembras", Integer),
                           Column("vacas_en_ordeno", Integer),
                           Column("vacas_no_ordeno", Integer),
                           Column("porcentaje_ordeno", Float),
                           Column("animales_rango_edades_0_9", Integer),
                           Column("animales_rango_edades_9_12", Integer),
                           Column("animales_rango_edades_12_24", Integer),
                           Column("animales_rango_edades_24_36", Integer),
                           Column("animales_rango_edades_mayor_36", Integer),
                           Column("animales_optimos_levante", Integer),
                           Column("animales_optimos_ceba", Integer),
                           Column("vientres_aptos", Integer),
                           Column("relacion_toros_vientres_aptos", Integer),
                           Column("interpretacion_relacion_toros_vientres_aptos", String(300)),
                           Column("total_unidades_animales", String(300)))

modelo_macho_reproductor = Table("macho_reproductor", meta, Column("id_macho", Integer, primary_key=True),
                                 Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                                 Column("edad", Integer),
                                 Column("peso", Float),
                                 Column("estado", String(300)),
                                 Column("fecha_vida_util", Date))

modelo_ventas = Table("ventas", meta, Column("id_venta", Integer, primary_key=True),
                      Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                      Column("numero_bono_venta", String(300)),
                      Column("estado", String(300)),
                      Column("fecha_venta", Date),
                      Column("precio_venta", Integer),
                      Column("razon_venta", String(300)),
                      Column("medio_pago", String(300)),
                      Column("comprador", String(300)))

modelo_datos_pesaje  = Table("ReportesPesaje", meta, Column("id_pesaje", Integer, primary_key=True),
                      Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                      Column("fecha_pesaje", Date),
                      Column("peso", Float))

modelo_veterinaria = Table("veterinaria", meta, Column("id_veterinaria", Integer, primary_key=True),
                           Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                           Column("sintomas", String(300)),
                           Column("fecha_sintomas", Date),
                           Column("comportamiento", String(300)),
                           Column("condicion_corporal", String(300)),
                           Column("postura", String(300)),
                           Column("mucosa_ocular", String(300)),
                           Column("mucosa_bucal", String(300)),
                           Column("mucosa_rectal", String(300)),
                           Column("mucosa_vulvar_prepusial", String(300)),
                           Column("tratamiento", String(300)),
                           Column("evolucion", String(300)),
                           Column("piel_pelaje", String(255)))

modelo_veterinaria_evoluciones = Table("Evoluciones_Bovinos", meta, Column("id_evolucion", Integer, primary_key=True),
                           Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                           Column("tratamiento_evolucion", String(300)),
                           Column("fecha_evolucion", Date))

modelo_veterinaria_comentarios = Table("Comentarios_Veterinaria", meta, Column("id_comentario", Integer, primary_key=True),
                           Column("id_veterinaria", Integer, ForeignKey("veterinaria.id_veterinaria")),
                           Column("comentarios", String(300)),
                           Column("fecha_comentario", Date))


modelo_descarte = Table("descarte", meta, Column("id_descarte", Integer, primary_key=True),
                        Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino"),unique=True),
                        Column("edad", Integer),
                        Column("peso", Float),
                        Column("razon_descarte", String(300)))

modelo_partos = Table("partos", meta, Column("id_parto", Integer, primary_key=True),
                      Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                      Column("edad", Integer),
                      Column("peso", Float),
                      Column("fecha_estimada_prenez", Date),
                      Column("fecha_estimada_parto", Date))

modelo_carga_animal_y_consumo_agua = Table("carga_animal", meta, Column("id_carga_animal", Integer, primary_key=True),
                                           Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                                           Column("edad", Integer),
                                           Column("peso", Float),
                                           Column("valor_unidad_animal", Float),
                                           Column("consumo_forraje_vivo", Float),
                                           Column("raza", String(300)))

modelo_capacidad_carga = Table("capacidad_carga", meta, Column("id_capacidad", Integer, primary_key=True),
                               Column("medicion_aforo", Float),
                               Column("hectareas_predio", Float),
                               Column("tipo_de_muestra", String(300)),
                               Column("carga_animal_recomendada", Float),
                               Column("capacidad_carga", String(300)),
                               Column("carga_animal_usuario", Float))

modelo_calculadora_hectareas_pastoreo = Table("pastoreo", meta, Column("id_pastoreo", Integer, primary_key=True),
                                              Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino")),
                                              Column("hectareas_necesarias", Float),
                                              Column("consumo_agua", String(300)))

modelo_vientres_aptos = Table("vientres_aptos", meta, Column("id_vientre", Integer, primary_key=True),
                              Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("edad", Integer),
                              Column("peso", Float),
                              Column("raza", String(300)))

modelo_historial_partos = Table("historial_partos", meta, Column("id_parto", Integer, primary_key=True),
                              Column("id_bovino", String(300)),
                              Column("fecha_parto", Date),
                              Column("tipo_parto", String(300)),
                              Column("id_bovino_hijo", String(300)))

modelo_historial_intervalo_partos = Table("intervalo_partos", meta, Column("id_intervalo", Integer, primary_key=True),
                              Column("id_bovino", String(300)),
                              Column("fecha_parto1", Date),
                              Column("fecha_parto2", Date),
                              Column("intervalo", Float))

modelo_litros_leche = Table("litros_leche", meta, Column("id_litros", Integer, primary_key=True),
                              Column("id_bovino", String(300)),
                              Column("fecha_medicion", Date),
                              Column("litros_leche", Float))

modelo_orden_IEP = Table("orden_por_IEP", meta, Column("id_IEP", Integer, primary_key=True),
                              Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("intervalo_promedio_raza", Float),
                              Column("intervalo_promedio_animal", Float),
                              Column("diferencia", Float))

modelo_orden_litros = Table("orden_por_litros", meta, Column("id_litros_leche", Integer, primary_key=True),
                              Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("litros_promedio_raza", Float),
                              Column("litros_promedio_animal", Float),
                              Column("diferencia", Float))

modelo_orden_peso = Table("orden_por_peso", meta, Column("id_peso", Integer, primary_key=True),
                              Column("id_bovino", String(300), ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("peso_promedio_raza", Float),
                              Column("peso_promedio_animal", Float),
                              Column("diferencia", Float))

meta.create_all(engine)