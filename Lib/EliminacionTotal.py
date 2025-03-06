'''
Librerias requeridas
@autor : odvr
'''
from sqlalchemy import Table, Column, Integer, ForeignKey, delete,select
import logging
from config.db import meta, engine



# importa la conexion de la base de datos
from sqlalchemy.orm import Session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_ceba, modelo_macho_reproductor, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_arbol_genealogico, modelo_historial_intervalo_partos, modelo_litros_leche, modelo_orden_IEP, \
    modelo_orden_litros, \
    modelo_orden_peso, modelo_historial_partos, modelo_carga_animal_y_consumo_agua, modelo_veterinaria_evoluciones, \
    modelo_datos_pesaje, modelo_compra, modelo_palpaciones, modelo_registro_celos, modelo_registro_vacunas_bovinos, \
    modelo_periodos_lactancia, modelo_abortos

'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuracion de la libreria para los logs de sinarca
# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Crea un manejador de archivo para guardar el log
log_file = 'Log_Sinarca.log'
file_handler = logging.FileHandler(log_file)

# Define el formato del log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Agrega el manejador de archivo al logger
logger.addHandler(file_handler)


# List of all tables that contain the id_veterinaria column in the order of dependency
dependent_veterinaria_tables = [
    "Comentarios_Veterinaria",  # Dependent on veterinaria
    "Evoluciones_Bovinos"
]

# List of all tables that contain the id_bovino column in the order of dependency
dependent_bovino_tables = [
    "comentarios_veterinaria",
    "veterinaria",  # This should be after comentarios_veterinaria
    "Evoluciones_Bovinos",
    "produccion_ceba",
    "produccion_levante",
    "produccion_leche",
    "datos_muerte",
    "arbol_genealogico",
    "macho_reproductor",
    "ventas",
    "compra_bovino",
    "ReportesPesaje",
    "registro_vacunacion_bovinos",
    "descarte",
    "partos",
    "palpaciones",
    "dias_abiertos",
    "carga_animal",
    "pastoreo",
    "vientres_aptos",
    "historial_partos",
    "intervalo_partos",
    "litros_leche",
    "reporte_curva_lactancia_general",
    "orden_por_IEP",
    "orden_por_litros",
    "orden_por_peso",
    "registro_celos",
    "tasas_concepcion",
    "ganancia_historica_peso",
    "natalidad_o_paricion_real",
    "periodos_lactancia",
    "periodos_secado",
    "abortos",
    "evaluaciones_macho_reproductor",
    "lotes_bovinos",
    "manejo_ternero_recien_nacido_lotes",
    "eventos_asociados_lotes",
    "descorne_lotes",
    "control_parasitos_lote",
    "control_podologia_lotes",
    "notificacion_proximidad_parto"
]

def delete_bovino_data(db: Session, id_bovino: int):
    try:
        # Modelo de la tabla arbol_genealogico
        modelo_arbol_genealogico = Table("arbol_genealogico", meta, autoload_with=engine)

        # Consulta de bovino en la tabla de arbol genealogico
        consulta_bovino_arbol = db.query(modelo_arbol_genealogico).filter(
            modelo_arbol_genealogico.c.id_bovino == id_bovino).all()
        if consulta_bovino_arbol:
            db.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino == id_bovino))
            db.commit()

        consulta_bovino_arbol_padre = db.query(modelo_arbol_genealogico).filter(
            modelo_arbol_genealogico.c.id_bovino_padre == id_bovino).all()
        if consulta_bovino_arbol_padre:
            db.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino_padre == id_bovino))
            db.commit()

        consulta_bovino_arbol_madre = db.query(modelo_arbol_genealogico).filter(
            modelo_arbol_genealogico.c.id_bovino_madre == id_bovino).all()
        if consulta_bovino_arbol_madre:
            db.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino_madre == id_bovino))
            db.commit()

        # Delete from tables that depend on veterinaria first
        for table_name in dependent_veterinaria_tables:
            table = Table(table_name, meta, autoload_with=engine)
            if 'id_veterinaria' in table.c:
                subquery = select(table.c.id_veterinaria).join(
                    Table('veterinaria', meta, autoload_with=engine)).filter(
                    Table('veterinaria', meta, autoload_with=engine).c.id_bovino == id_bovino)
                stmt = delete(table).where(table.c.id_veterinaria.in_(subquery))
                db.execute(stmt)

        # Handle the dependent tables for partos first
        registro_celos_table = Table("registro_celos", meta, autoload_with=engine)
        partos_table = Table("partos", meta, autoload_with=engine)
        subquery_partos = select(partos_table.c.id_parto).where(partos_table.c.id_bovino == id_bovino)
        db.execute(delete(registro_celos_table).where(registro_celos_table.c.id_servicio.in_(subquery_partos)))
        db.commit()

        # Delete from tables that depend on bovinos
        for table_name in dependent_bovino_tables:
            table = Table(table_name, meta, autoload_with=engine)
            if 'id_bovino' in table.c:
                stmt = delete(table).where(table.c.id_bovino == id_bovino)
                db.execute(stmt)

        # Finally, delete from the main bovinos table
        bovino_table = Table("bovinos", meta, autoload_with=engine)
        stmt = delete(bovino_table).where(bovino_table.c.id_bovino == id_bovino)
        db.execute(stmt)

        db.commit()

    except Exception as e:
        db.rollback()



"""la siguiente funcion tiene como objetivo eliminar el bovino que se desee:"""
def eliminacionBovino(id_bov_eliminar,session: Session):
  try:
      #consulta de id de parametro en la base de datos
      #consulta de bovino en la tabla de inventario
      """
      
    """

      #consulta de bovino en la tabla de produccion leche
      consulta_bovino_leche = session.query(modelo_leche).\
          filter( modelo_leche.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_leche ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_leche.delete().where(modelo_leche.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de arbol genealogico
      consulta_bovino_arbol = session.query(modelo_arbol_genealogico).\
          filter(modelo_arbol_genealogico.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_arbol ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de arbol genealogico
      consulta_bovino_arbol_padre = session.query(modelo_arbol_genealogico).\
          filter(modelo_arbol_genealogico.c.id_bovino_padre==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_arbol_padre ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino_padre == id_bov_eliminar))
          session.commit()


      #consulta de bovino en la tabla de arbol genealogico
      consulta_bovino_arbol_madre = session.query(modelo_arbol_genealogico).\
          filter(modelo_arbol_genealogico.c.id_bovino_madre==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_arbol_madre ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_arbol_genealogico.delete().where(modelo_arbol_genealogico.c.id_bovino_madre == id_bov_eliminar))
          session.commit()


      #consulta de bovino en la tabla de registro de celos
      consulta_bovino_celos = session.query(modelo_registro_celos).\
          filter(modelo_registro_celos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_celos ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_registro_celos.delete().where(modelo_registro_celos.c.id_bovino == id_bov_eliminar))
          session.commit()


      #consulta de bovino en la tabla de registro de montas
      consulta_bovino_montas = session.query(modelo_partos).\
          filter(modelo_partos.c.id_reproductor==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_montas ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_partos.delete().where(modelo_partos.c.id_reproductor == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de muertes
      consulta_bovino_muerte = session.query(modelo_datos_muerte). \
              filter(modelo_datos_muerte.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_muerte == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_datos_muerte.delete().where(modelo_datos_muerte.c.id_bovino == id_bov_eliminar))
          session.commit()


      # consulta de bovino en la tabla de vacunaciones
      consulta_bovino_vacuna = session.query(modelo_registro_vacunas_bovinos). \
              filter(modelo_registro_vacunas_bovinos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_vacuna == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_registro_vacunas_bovinos.delete().where(modelo_registro_vacunas_bovinos.c.id_bovino == id_bov_eliminar))
          session.commit()


      #consulta de bovino en la tabla de descarte
      consulta_bovino_descarte = session.query(modelo_descarte).\
          filter(modelo_descarte.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_descarte ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_descarte.delete().where(modelo_descarte.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de historial de partos
      consulta_bovino_parto = session.query(modelo_partos).\
          filter(modelo_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_parto ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_partos.delete().where(modelo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de intervalo entre partos
      consulta_bovino_intervalo = session.query(modelo_historial_intervalo_partos).\
          filter(modelo_historial_intervalo_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_intervalo ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_historial_intervalo_partos.delete().where(modelo_historial_intervalo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de litros de leche
      consulta_bovino_litros = session.query(modelo_litros_leche).\
          filter(modelo_litros_leche.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_litros ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_litros_leche.delete().where(modelo_litros_leche.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de macho reproductor
      consulta_bovino_reproductor = session.query(modelo_macho_reproductor). \
          filter(modelo_macho_reproductor.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_reproductor == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_macho_reproductor.delete().where(modelo_macho_reproductor.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por IEP
      consulta_bovino_orden_IEP = session.query(modelo_orden_IEP). \
          filter(modelo_orden_IEP.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_IEP == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_IEP.delete().where(modelo_orden_IEP.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por litros
      consulta_bovino_orden_litros = session.query(modelo_orden_litros). \
          filter(modelo_orden_litros.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_litros == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_litros.delete().where(modelo_orden_litros.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de orden por peso
      consulta_bovino_orden_peso = session.query(modelo_orden_peso). \
          filter(modelo_orden_peso.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_orden_peso == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_orden_peso.delete().where(modelo_orden_peso.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de partos
      consulta_bovino_registro_partos = session.query(modelo_partos). \
          filter(modelo_partos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_registro_partos == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_partos.delete().where(modelo_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de ceba
      consulta_bovino_ceba = session.query(modelo_ceba). \
          filter(modelo_ceba.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_ceba == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_ceba.delete().where(modelo_ceba.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de levante
      consulta_bovino_levante = session.query(modelo_levante). \
          filter(modelo_levante.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_levante == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_levante.delete().where(modelo_levante.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de ventas
      consulta_bovino_venta = session.query(modelo_ventas). \
          filter(modelo_ventas.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_venta == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_ventas.delete().where(modelo_ventas.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de veterinaria
      consulta_bovino_veterinaria = session.query(modelo_veterinaria). \
          filter(modelo_veterinaria.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_veterinaria == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_veterinaria.delete().where(modelo_veterinaria.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de vientres aptos
      consulta_bovino_vientre = session.query(modelo_vientres_aptos). \
          filter(modelo_vientres_aptos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_vientre == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_vientres_aptos.delete().where(modelo_vientres_aptos.c.id_bovino == id_bov_eliminar))
          session.commit()

          # consulta de bovino en la tabla de periodos de lactancia
      consulta_bovino_lactancia = session.query(modelo_periodos_lactancia). \
          filter(modelo_periodos_lactancia.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_lactancia == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_periodos_lactancia.delete().where(
              modelo_periodos_lactancia.c.id_bovino == id_bov_eliminar))
          session.commit()


          # consulta de bovino en la tabla de abortos
      consulta_bovino_aborto = session.query(modelo_abortos). \
          filter(modelo_abortos.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_aborto == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_abortos.delete().where(
              modelo_abortos.c.id_bovino == id_bov_eliminar))
          session.commit()

      #consulta de bovino en la tabla de partos
      consulta_bovino_partos_historial = session.query(modelo_historial_partos).\
          filter(modelo_historial_partos.c.id_bovino==id_bov_eliminar).all()
      #si el id ya no existe entonces no se hara cambios
      if consulta_bovino_partos_historial ==[]:
          pass
      #caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_historial_partos.delete().where(modelo_historial_partos.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de carga animal
      consulta_bovino_carga = session.query(modelo_carga_animal_y_consumo_agua). \
              filter(modelo_carga_animal_y_consumo_agua.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_carga == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_carga_animal_y_consumo_agua.delete().where(modelo_carga_animal_y_consumo_agua.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de evoluciones veterinarias
      consulta_bovino_evolucion = session.query(modelo_veterinaria_evoluciones). \
              filter(modelo_veterinaria_evoluciones.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_evolucion == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_veterinaria_evoluciones.delete().where(modelo_veterinaria_evoluciones.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de reportes de pesaje
      consulta_bovino_pesaje = session.query(modelo_datos_pesaje). \
              filter(modelo_datos_pesaje.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_pesaje == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_datos_pesaje.delete().where(modelo_datos_pesaje.c.id_bovino == id_bov_eliminar))
          session.commit()
      session.commit()


      # consulta de bovino en la tabla de compras
      consulta_bovino_compra = session.query(modelo_compra). \
              filter(modelo_compra.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_compra == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_compra.delete().where(modelo_compra.c.id_bovino == id_bov_eliminar))
          session.commit()

      # consulta de bovino en la tabla de palpaciones
      consulta_bovino_palpaciones = session.query(modelo_palpaciones). \
              filter(modelo_palpaciones.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_palpaciones == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(modelo_palpaciones.delete().where(modelo_palpaciones.c.id_bovino == id_bov_eliminar))
          session.commit()

      session.commit()

      consulta_bovino_inventario = session.query(modelo_bovinos_inventario). \
          filter(modelo_bovinos_inventario.c.id_bovino == id_bov_eliminar).all()
      # si el id ya no existe entonces no se hara cambios
      if consulta_bovino_inventario == []:
          pass
      # caso contrario se eliminara de la tabla
      else:
          session.execute(
              modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bov_eliminar))
          session.commit()




  except Exception as e:
      logger.error(f'Error Funcion eliminacionBovino:{e}')
      raise
  finally:
      session.close()

