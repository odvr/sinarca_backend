"""
Autor: odvr
Fecha Modificación: 16/12/2024


Consideraciones

Las funciones que son llamadas por el Recurso deben de es
"""

# Librerías
from sqlalchemy.orm import Session
import crud.crud_bovinos_inventario
from Lib.enviar_correos import enviar_correo
from config.db import get_session
from models.modelo_bovinos import modelo_facturas
from datetime import datetime


def CambiarEstadoFactura():
    # Crear una sesión de base de datos
    session: Session = get_session()
    try:
        # Obtener la fecha actual
        FechaActual = datetime.now().date()
        # Consultar facturas que no han vencido
        ConsultarFechaFactura = session.query(modelo_facturas).all()

        for factura in ConsultarFechaFactura:
            fechaVencimiento = factura.fecha_vencimiento
            estadoFactura = factura.estado
            if fechaVencimiento < FechaActual and estadoFactura == "pendiente":
                # Consultar facturas que no han vencido
                ConsultarFechaFactura = session.query(modelo_facturas). \
                    filter(modelo_facturas.c.fecha_vencimiento >= FechaActual).all()

                # Actualizar el estado de las facturas vencidas
                for Factura in ConsultarFechaFactura:
                    session.execute(
                        modelo_facturas.update().values(
                            estado="vencida"
                        ).where(
                            modelo_facturas.c.factura_id == Factura.factura_id
                        )
                    )
                    # ID Usuario a Notificar
                    IdUsuario = Factura.usuario_id

                    CorreoElectronico = crud.bovinos_inventario.Buscar_Correo_Usuario(db=session, usuario_id=IdUsuario)

                    "El dato que Retorna es tipo Byte se realiza la conversión"
                    Correo = str(CorreoElectronico, encoding='utf-8')

                    # Radicado de Factura para Notificar
                    RadicadoFactura = str(Factura.radicado_factura, encoding='utf-8')

                    # Envia La notificación
                    enviar_correo(Correo, "Notificación de Vencimiento de Factura",
                                  "Estimado/a, le informamos que la factura con número de radicado " + RadicadoFactura + " ha vencido.")

                session.commit()

    except Exception as e:
        # Revertir cambios si ocurre un error
        session.rollback()
        raise e
    finally:
        # Cerrar la sesión
        session.close()

def CambiarEstadoFacturaSinEnviarNotificacion():
    """
    Usa la siguiente función para realizar el cambio de estado de las Facturas
    :return:
    """
    session: Session = get_session()
    try:
        # Obtener la fecha actual
        FechaActual = datetime.now().date()

        # Consultar facturas que no han vencido
        ConsultarFechaFactura = session.query(modelo_facturas).all()


        for factura in ConsultarFechaFactura:
            fechaVencimiento = factura.fecha_vencimiento
            estadoFactura  =  factura.estado
            if fechaVencimiento < FechaActual and  estadoFactura == "pendiente":
                session.execute(
                    modelo_facturas.update().values(
                        estado="vencida"
                    ).where(
                        modelo_facturas.c.factura_id == factura.factura_id
                    )
                )

                session.commit()

    except Exception as e:
        # Revertir cambios si ocurre un error
        session.rollback()
        raise e
    finally:
        # Cerrar la sesión
        session.close()
