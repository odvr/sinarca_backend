'''
Librerias requeridas
'''
import logging
from sqlalchemy import func,and_
# # importa la conexion de la base de datos
from sqlalchemy.orm import Session
from datetime import datetime  # Importar el módulo datetime
from models.modelo_bovinos import modelo_litros_leche, modelo_reporte_curva_lactancia_General
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
"""
La siguiente funcion permite tomar el promedio mensual de todos los animales que se encuentran en la tabla de Reportes de Listros Diarios
"""
def Reporte_Curvas_lactancia_Mensuales_General(session:Session):
 try:
    # Calcular el promedio mensual de litros de leche en MariaDB por cada ID de cliente
    resultados_mensuales = session.query(
        modelo_litros_leche.c.id_bovino,
        modelo_litros_leche.c.usuario_id,
        modelo_litros_leche.c.nombre_bovino,

        func.YEAR(modelo_litros_leche.c.fecha_medicion).label('anio'),
        func.MONTH(modelo_litros_leche.c.fecha_medicion).label('mes'),
        func.avg(modelo_litros_leche.c.litros_leche).label('promedio_mensual')
    ).group_by(modelo_litros_leche.c.id_bovino, func.YEAR(modelo_litros_leche.c.fecha_medicion),
               func.MONTH(modelo_litros_leche.c.fecha_medicion)).all()

    for resultado in resultados_mensuales:
        print(resultado)
        id_bovino = resultado.id_bovino
        anio = resultado.anio
        mes = resultado.mes
        promedio = resultado.promedio_mensual
        nombre_bovino = resultado.nombre_bovino
        usuario_id= resultado.usuario_id

        # Obtener la fecha y hora actual
        fecha_actual = datetime.now()

        # Verificar si ya existe un registro con el mismo año, mes y promedio para el mismo bovino
        consulta = session.execute(
            modelo_reporte_curva_lactancia_General.select().where(
                and_(
                    modelo_reporte_curva_lactancia_General.columns.id_bovino == id_bovino,
                    modelo_reporte_curva_lactancia_General.columns.anio == anio,
                    modelo_reporte_curva_lactancia_General.columns.mes == mes

                    # Agrega más condiciones según sea necesario
                )
            )
        ).first()

        if consulta:
            id_curva_lactancia =consulta.id_curva_lactancia_general
            update_query = modelo_reporte_curva_lactancia_General.update().where(
                modelo_reporte_curva_lactancia_General.c.id_curva_lactancia_general == id_curva_lactancia
            ).values(
                promedio=promedio,
                Hora_Reporte=fecha_actual,
                nombre_bovino=nombre_bovino,
                usuario_id=usuario_id
            )
            session.execute(update_query)
            session.commit()
        if consulta is None:
            ingresarDatos = modelo_reporte_curva_lactancia_General.insert().values(
                id_bovino=id_bovino,
                anio=anio,
                mes=mes,
                promedio=promedio,
                Hora_Reporte=fecha_actual,
                nombre_bovino=nombre_bovino,
                usuario_id=usuario_id


            )


            session.execute(ingresarDatos)
            session.commit()
        else:
            logger.error(f'Error al obtener Curvas de lactancia')
 except Exception as e:
    logger.error(f'Error al obtener Curvas de lactancia {e}')
    raise
 finally:
    session.close()
