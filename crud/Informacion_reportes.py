from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from http.client import HTTPException

from models.modelo_bovinos import modelo_bovinos_inventario, modelo_datos_muerte, modelo_ventas, modelo_compra, \
    modelo_facturas, modelo_pagos, modelo_empleados

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

class InformacionReportes:
    def __init__(self):
        """

        """
        self.model = modelo_bovinos_inventario



    def get(self, db: Session, id: Any) -> Any:
        return db.query(self.model).filter(self.model.id == id).first()

    def Buscar_Animales_Nacidos_EnlosUltimos_7_dias(self,db: Session,current_user):
        hace_7_dias = datetime.utcnow() - timedelta(days=7)
        print(hace_7_dias)

        BuscarAnimales = (
            db.query(modelo_bovinos_inventario)
            .filter(
                modelo_bovinos_inventario.c.fecha_nacimiento >= hace_7_dias,
                modelo_bovinos_inventario.c.usuario_id == current_user
            )
            .count()
        )

        db.close()
        return BuscarAnimales

    def Buscar_Animales_Muertos_Ultimos_7_dias(self, db: Session, current_user):
        """
        Realiza la busqueda de los animales Muertos de los ultimos 7 días

        :param db:
        :param current_user:
        :return:
        """
        hace_7_dias = datetime.utcnow() - timedelta(days=7)


        BuscarAnimales = (
            db.query(modelo_datos_muerte)
            .filter(
                modelo_datos_muerte.c.fecha_muerte >= hace_7_dias,
                modelo_datos_muerte.c.usuario_id == current_user
            )
            .count()
        )

        db.close()
        return BuscarAnimales


    def Buscar_Animales_Vendidos_Ultimos_7_dias(self, db: Session, current_user):
        """
        Realiza la busqueda de los animales Muertos de los ultimos 7 días

        :param db:
        :param current_user:
        :return:
        """
        hace_7_dias = datetime.utcnow() - timedelta(days=7)


        BuscarAnimales = (
            db.query(modelo_ventas)
            .filter(
                modelo_ventas.c.fecha_venta >= hace_7_dias,
                modelo_ventas.c.usuario_id == current_user
            )
            .count()
        )

        db.close()
        return BuscarAnimales


    def Buscar_Total_Nomina(self, db: Session, current_user):
        """

        :param db:
        :param current_user:
        :return:
        """

        try:
            # Realiza la Busqueda del Salirio
            ConsultaNomina = db.query(func.sum(modelo_empleados.columns.salario_base)).filter(
                modelo_empleados.c.estado != "Retirado",
                modelo_empleados.c.usuario_id == current_user).all()
            ListaConsultaNomina = ConsultaNomina[0][0]

            return ListaConsultaNomina
        except Exception as e:
            logger.error(f'Error en Calcular Nomina Total: {e}')
            raise HTTPException(status_code=500, detail="Error interno del servidor")
        finally:
            db.close()


    def Buscar_Animales_Comprados_Ultimos_7_dias(self, db: Session, current_user):
        """
       Busqueda de animales comprados en los ultimos

        :param db:
        :param current_user:
        :return:
        """
        hace_7_dias = datetime.utcnow() - timedelta(days=7)

        BuscarAnimales = (
            db.query(modelo_compra)
            .filter(
                modelo_compra.c.fecha_compra >= hace_7_dias,
                modelo_compra.c.usuario_id == current_user
            )
            .count()
        )

        db.close()
        return BuscarAnimales

    def Buscar_Animales_TotalVentas_Ultimos_7_dias(self, db: Session, current_user):

        try:
            hace_7_dias = datetime.utcnow() - timedelta(days=7)
            "Consulta del total de la factura"
            ConsultaVentas = db.query(func.sum(modelo_facturas.columns.monto_total)).filter(
                modelo_facturas.c.detalle == "Factura de Venta",
                modelo_facturas.c.estado == "pagada",
                modelo_facturas.c.fecha_emision >= hace_7_dias,
                modelo_facturas.c.usuario_id == current_user
            ).all()
            ConsultaVentas = ConsultaVentas[0][0] if ConsultaVentas[0][0] is not None else 0

            """
            La siguiente consulta realiza una validación entre la tabla de Pagos Abonos y la tabla de facturas esto con el fin de validar qué facturas están activas 
            """
            ConsultarPagosConFacturasActivas = set(
                db.query(modelo_facturas.c.estado, modelo_facturas.c.factura_id, modelo_pagos.c.monto).
                join(modelo_pagos, modelo_facturas.c.factura_id == modelo_pagos.c.factura_id).filter(
                    modelo_pagos.c.usuario_id == current_user).all()
            )


            total_pagos_activos = sum(
                monto for estado, _, monto in ConsultarPagosConFacturasActivas if estado not in ['anulada', 'pagada'])

            total_ventas = ConsultaVentas + total_pagos_activos

            return total_ventas
        except Exception as e:
            logger.error(f'Error en Calcular TotalVentas: {e}')
            raise HTTPException(status_code=500, detail="Error interno del servidor")
        finally:
            db.close()

InformacionReportesUsuarios = InformacionReportes()