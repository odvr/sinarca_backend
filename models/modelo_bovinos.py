"""
@autor:odvr
el siguiente codigo realiza la creacion de las tablas que se ge
"""
import decimal
from datetime import datetime

from pydantic.schema import Decimal
# librerias requeridas
# ,
from sqlalchemy import Table, Column, Date, Float
# importacion del cong para la conexion con la base de datos
from config.db import meta, engine
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, Text, String, DateTime




modelo_usuarios = Table("usuarios", meta, Column("id_usuario", Integer, primary_key=True, unique=True, index=True),
                     Column("usuario_id", String(300), unique=True, index=True),
                     Column("hashed_password", String(300)),
                     Column("nombre_predio", String(300)),
                     Column("correo_electronico", String(300)),
                     Column("telefono", String(300)),
                     Column("ubicacion_predio", String(300)),
                     Column("nombre_apellido", String(300)))





"""
 Modelo para la tabla de Bovinos
 cuenta una relacion de uno a muchos para las siguientes tablas: 
 sexo

"""
modelo_bovinos_inventario = Table("bovinos", meta,
                                  Column("id_bovino", Integer, primary_key=True),
                                  Column("fecha_nacimiento", Date),
                                  Column("edad", Integer),
                                  Column("sexo", String(300)),
                                  Column("raza", String(300)),
                                  Column("peso", Float),
                                  Column("marca", String(300)),
                                  Column("proposito", String(300)),
                                  Column("mansedumbre", String(300)),
                                  Column("estado", String(300)),
                                  Column("compra_bovino", String(300)),
                                  Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                                  Column("nombre_bovino", String(300)),
                                  Column("ruta_imagen_marca", String(300)),
                                  Column("ruta_fisica_foto_perfil",String(300)))


modelo_ceba = Table("produccion_ceba", meta,
                    Column("id_ceba", Integer, primary_key=True),
                    Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                    Column("edad", Integer),
                    Column("peso", Float),
                    Column("estado", String(300)),
                    Column("proposito", String(300)),
                    Column("estado_optimo_ceba", String(300)),
                    Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                    Column("nombre_bovino", String(300))
                    )



modelo_levante = Table("produccion_levante", meta,
                       Column("id_levante", Integer, primary_key=True),
                       Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                       Column("edad", Integer),
                       Column("peso", Float),
                       Column("estado", String(300)),
                       Column("proposito", String(300)),
                       Column("estado_optimo_levante", String(300)),
                       Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                       Column("nombre_bovino", String(300))
                       )

modelo_leche = Table("produccion_leche", meta,
                     Column("id_leche", Integer, primary_key=True),
                     Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                     Column("fecha_primer_parto", Date),
                     Column("edad_primer_parto", Integer),
                     Column("datos_prenez", String(300)),
                     Column("fecha_vida_util", Date),
                     Column("ordeno", String(300)),
                     Column("proposito", String(300)),
                     Column("promedio_litros", Float),
                     Column("num_partos", Integer),
                     Column("intervalo_entre_partos", Float),
                     Column("tipo_ganado", String(300)),
                     Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                     Column("nombre_bovino", String(300)),
                     Column("dias_abiertos", Integer))

modelo_datos_muerte = Table("datos_muerte", meta,
                            Column("id_datos_muerte", Integer, primary_key=True),
                            Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                            Column("razon_muerte", String(300)),
                            Column("estado", String(300)),
                            Column("fecha_muerte", Date),
                            Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                            Column("nombre_bovino", String(300))
                            )

modelo_arbol_genealogico = Table("arbol_genealogico", meta,
                                 Column("id_arbol_genealogico", Integer, primary_key=True),
                                 Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                                 Column("id_bovino_madre", Integer),
                                 Column("id_bovino_padre", Integer),
                                 Column("abuelo_paterno", Integer),
                                 Column("abuela_paterna", Integer),
                                 Column("abuelo_materno", Integer),
                                 Column("abuela_materna", Integer),
                                 Column("bisabuelo_materno", Integer),
                                 Column("bisabuelo_paterno", Integer),
                                 Column("tipo_de_apareamiento", String(300)),
                                 Column("consanguinidad", Float),
                                 Column("notificacion", String(300)),
                                 Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                                 Column("nombre_bovino", String(300)),
                                 Column("nombre_bovino_madre", String(300)),
                                 Column("nombre_bovino_padre", String(300)),
                                 Column("nombre_bovino_abuelo_paterno", String(300)),
                                 Column("nombre_bovino_abuela_paterna", String(300)),
                                 Column("nombre_bovino_abuelo_materno", String(300)),
                                 Column("nombre_bovino_abuela_materna", String(300)),
                                 Column("nombre_bovino_bisabuelo_materno", String(300)),
                                 Column("nombre_bovino_bisabuelo_paterno", String(300)),
                                 Column("inseminacion", String(300))
                                 )
"""modelo para indicadores"""
modelo_indicadores = Table("indicadores", meta, Column("id_indicadores", String(300), primary_key=True),
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
                           Column("total_unidades_animales", String(300)),
                           Column("IEP_hato", Float),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id"))
                           )

modelo_macho_reproductor = Table("macho_reproductor", meta, Column("id_macho", Integer, primary_key=True),
                                 Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino"),
                                        unique=True),
                                 Column("edad", Integer),
                                 Column("peso", Float),
                                 Column("estado", String(300)),
                                 Column("fecha_vida_util", Date),
                                 Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                                 Column("nombre_bovino", String(300))
                                 )

modelo_ventas = Table("ventas", meta, Column("id_venta", Integer, primary_key=True),
Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                      Column("numero_bono_venta", String(300)),
                      Column("estado", String(300)),
                      Column("fecha_venta", Date),
                      Column("precio_venta", Integer),
                      Column("razon_venta", String(300)),
                      Column("medio_pago", String(300)),
                      Column("comprador", String(300)),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                      Column("nombre_bovino", String(300))
                      )


modelo_compra = Table("compra_bovino", meta, Column("id_compra_bovino", Integer, primary_key=True),
Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                      Column("numero_bono_compra", String(300)),
                      Column("estado", String(300)),
                      Column("fecha_compra", Date),
                      Column("precio_compra", Integer),
                      Column("razon_compra", String(300)),
                      Column("medio_pago_compra", String(300)),
                      Column("comprador", String(300)),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                      Column("nombre_bovino", String(300))
                      )


modelo_datos_pesaje  = Table("ReportesPesaje", meta, Column("id_pesaje", Integer, primary_key=True),
                      Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                      Column("fecha_pesaje", Date),
                      Column("peso", Float),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                      Column("nombre_bovino", String(300))
                             )

modelo_veterinaria = Table("veterinaria", meta, Column("id_veterinaria", Integer, primary_key=True),
                           Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
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
                           Column("piel_pelaje", String(255)),
                           Column("estado_Historia_clinica", String(255)),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                           Column("nombre_bovino", String(300))
                           )

modelo_veterinaria_evoluciones = Table("Evoluciones_Bovinos", meta, Column("id_evolucion", Integer, primary_key=True),
                           Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                           Column("tratamiento_evolucion", String(300)),
                           Column("fecha_evolucion", Date),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                           Column("nombre_bovino", String(300))
                                       )

modelo_veterinaria_comentarios = Table("Comentarios_Veterinaria", meta, Column("id_comentario", Integer, primary_key=True),
                           Column("id_veterinaria", Integer, ForeignKey("veterinaria.id_veterinaria")),
                           Column("comentarios", String(300)),
                           Column("fecha_comentario", Date),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id"))
                                       )




modelo_registro_vacunas_bovinos = Table("registro_vacunacion_bovinos", meta, Column("id_vacunacion_bovinos", Integer, primary_key=True),
                        Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                        Column("fecha_registrada_usuario", Date),
                        Column("tipo_vacuna", String(50)),
                        Column("fecha_bitacora_Sistema", DateTime),
                        Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                        Column("nombre_bovino", String(300)))


modelo_descarte = Table("descarte", meta, Column("id_descarte", Integer, primary_key=True),
                        Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino"),unique=True),
                        Column("edad", Integer),
                        Column("peso", Float),
                        Column("razon_descarte", String(300)),
                        Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                        Column("nombre_bovino", String(300)))

modelo_partos = Table("partos", meta, Column("id_parto", Integer, primary_key=True),
                      Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino")),
                      Column("edad", Integer),
                      Column("peso", Float),
                      Column("fecha_estimada_prenez", Date),
                      Column("fecha_estimada_parto", Date),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                      Column("nombre_bovino", String(300)),
                      Column("notificacion", String(300)),
                      Column("tipo", String(300)),
                      Column("id_reproductor", String(300)),
                      Column("nombre_bovino_reproductor", String(300)))

modelo_palpaciones = Table("palpaciones", meta, Column("id_palpacion", Integer, primary_key=True),
                      Column("id_bovino", Integer),
                      Column("fecha_palpacion", Date),
                      Column("diagnostico_prenez", String(300)),
                      Column("observaciones", String(300)),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                      Column("nombre_bovino", String(300)))

modelo_dias_abiertos = Table("dias_abiertos", meta, Column("id_dias_abiertos", Integer, primary_key=True),
                      Column("id_bovino", Integer),
                      Column("nombre_bovino", String(300)),
                      Column("fecha_parto", Date),
                      Column("fecha_prenez", Date),
                      Column("dias_abiertos", Integer),
                      Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

modelo_carga_animal_y_consumo_agua = Table("carga_animal", meta, Column("id_carga_animal", Integer, primary_key=True),
                                           Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino"),unique=True),
                                           Column("edad", Integer),
                                           Column("peso", Float),
                                           Column("valor_unidad_animal", Float),
                                           Column("consumo_forraje_vivo", Float),
                                           Column("raza", String(300)),
                                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                                           Column("nombre_bovino", String(300)))

modelo_capacidad_carga = Table("capacidad_carga", meta, Column("id_capacidad", String(300), primary_key=True),
                               Column("medicion_aforo", Float),
                               Column("hectareas_predio", Float),
                               Column("tipo_de_muestra", String(300)),
                               Column("carga_animal_recomendada", Float),
                               Column("capacidad_carga", String(300)),
                               Column("carga_animal_usuario", Float),
                               Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                               Column("nombre_bovino", String(300)))

modelo_calculadora_hectareas_pastoreo = Table("pastoreo", meta, Column("id_pastoreo", Integer, primary_key=True),
                                              Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino")),
                                              Column("hectareas_necesarias", Float),
                                              Column("consumo_agua", String(300)),
                                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                                              Column("nombre_bovino", String(300)))

modelo_vientres_aptos = Table("vientres_aptos", meta, Column("id_vientre", Integer, primary_key=True),
                              Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("edad", Integer),
                              Column("peso", Float),
                              Column("raza", String(300)),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_historial_partos = Table("historial_partos", meta, Column("id_parto", Integer, primary_key=True),
                              Column("id_bovino", Integer),
                              Column("fecha_parto", Date),
                              Column("tipo_parto", String(300)),
                              Column("id_bovino_hijo", Integer),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_madre", String(300)),
                              Column("nombre_hijo", String(300)))

modelo_historial_intervalo_partos = Table("intervalo_partos", meta, Column("id_intervalo", Integer, primary_key=True),
                              Column("id_bovino", Integer),
                              Column("fecha_parto1", Date),
                              Column("fecha_parto2", Date),
                              Column("intervalo", Float),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_litros_leche = Table("litros_leche", meta, Column("id_litros", Integer, primary_key=True),
                              Column("id_bovino", Integer),
                              Column("fecha_medicion", Date),
                              Column("litros_leche", Float),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_reporte_curva_lactancia_General = Table("reporte_curva_lactancia_general", meta, Column("id_curva_lactancia_general", Integer, primary_key=True),
                              Column("id_bovino", Integer),
                              Column("anio", String(10)),
                              Column("mes", String(10)),
                              Column("promedio", Float),
                              Column("Hora_Reporte", DateTime),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_orden_IEP = Table("orden_por_IEP", meta, Column("id_IEP", Integer, primary_key=True),
                              Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("intervalo_promedio_raza", Float),
                              Column("intervalo_promedio_animal", Float),
                              Column("diferencia", Float),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_orden_litros = Table("orden_por_litros", meta, Column("id_litros_leche", Integer, primary_key=True),
                              Column("id_bovino", Integer, ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("litros_promedio_raza", Float),
                              Column("litros_promedio_animal", Float),
                              Column("diferencia", Float),Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_orden_peso = Table("orden_por_peso", meta, Column("id_peso", Integer, primary_key=True),
                              Column("id_bovino", Integer,ForeignKey("bovinos.id_bovino"),unique=True),
                              Column("raza", String(300)),
                              Column("peso_promedio_raza", Float),
                              Column("peso_promedio_animal", Float),
                              Column("diferencia", Float),Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")),
                              Column("nombre_bovino", String(300)))

modelo_historial_perdida_terneros = Table("historial_perdidas_terneros", meta, Column("id_perdida", Integer, primary_key=True),
                              Column("periodo", Integer),
                              Column("perdida", Float),Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

modelo_historial_supervivencia = Table("historial_supervivencia", meta, Column("id_supervivencia", Integer, primary_key=True),
                              Column("periodo", Integer),
                              Column("supervivencia", Float),Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

modelo_registro_pajillas = Table("registro_pajillas", meta, Column("id_pajillas", Integer, primary_key=True),
                              Column("Codigo_toro_pajilla", String(300)),
                              Column("raza", String(300)),
                              Column("nombre_toro", String(300)),
                              Column("productor", String(300)),
                              Column("unidades", Integer),
                              Column("precio", Integer),
                              Column("nombre_canastilla", String(300)),
                              Column("id_canastilla", Integer, ForeignKey("canatillas.id_canastilla")),
                              Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))


modelo_registro_marca = Table("registro_marca", meta, Column("id_registro_marca", Integer, primary_key=True),
                           Column("ruta_marca", String(500)),
                           Column("nombre_marca_propietario", String(500)),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

modelo_parametros_levante_ceba = Table("parametros_levante_ceba", meta, Column("id_parametros", Integer, primary_key=True),
                           Column("peso_levante", Integer),
                           Column("edad_levante", Integer),
                           Column("peso_ceba", Integer),
                           Column("edad_ceba", Integer),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

modelo_canastillas = Table("canastillas", meta, Column("id_canastilla", Integer, primary_key=True),
                           Column("nombre_canastilla", String(300)),
                           Column("unidades_disponibles", Integer),
                           Column("usuario_id", String(300), ForeignKey("usuarios.usuario_id")))

meta.create_all(engine)