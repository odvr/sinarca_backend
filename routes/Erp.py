'''
@autor : odvr
Librerias requeridas
'''
import logging
from datetime import date, datetime
from http.client import HTTPException

from fastapi import APIRouter, Depends,Form,Response,status,Body
from sqlalchemy import func, or_, extract
from starlette.status import HTTP_204_NO_CONTENT

import crud
from Lib.GenerarRadicadoFactura import generar_radicado

from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_clientes, modelo_cotizaciones, modelo_facturas, modelo_ventas, \
    modelo_bovinos_inventario, modelo_pagos, modelo_empleados, modelo_nomina, modelo_proveedores
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_clientes, esquema_cotizaciones, esquema_facturas, \
    esquema_pagos, esquema_empleados, esquema_nomina, esquema_provedores
from typing import Optional,List
import json



# Configuracion de las rutas para fash api
ERP = APIRouter()

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

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@ERP.get("/Clientes",response_model=list[esquema_clientes],tags=["ERP"] )
async def Listar_Clientes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        Clientes = db.query(modelo_clientes).filter(modelo_clientes.c.usuario_id == current_user).all()
        return Clientes

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()


@ERP.post("/CrearClientes",status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearClientes(nombre_cliente: Optional [str] = Form(None),direccion: Optional [str] = Form(None),telefono: Optional [str] = Form(None),email: Optional [str] = Form(None),tipo_cliente: Optional [str] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    """
    API Para realizar la  creacion de clientes
    :param nombre_cliente:
    :param direccion:
    :param telefono:
    :param email:
    :param tipo_cliente:
    :param fecha_creacion:
    :param db:
    :param current_user:
    :return:
    """
    try:
        fecha_creacion= datetime.now()
        CrearCliente = modelo_clientes.insert().values(nombre_cliente=nombre_cliente,direccion=direccion,telefono=telefono,email=email,fecha_creacion=fecha_creacion,tipo_cliente=tipo_cliente,usuario_id=current_user)
        db.execute(CrearCliente)
        db.commit()

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


@ERP.delete("/Eliminar_Cliente/{cliente_id}")
async def Eliminar_cliente(cliente_id: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        db.execute(modelo_clientes.delete().where(modelo_clientes.c.cliente_id == cliente_id))
        db.commit()
        return
    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Cliente: {e}')
        raise
    finally:
        db.close()

"""
Cotizaciones
"""

@ERP.get("/Cotizaciones",  response_model=list[esquema_cotizaciones],tags=["ERP"] )
async def Listar_Cotizaciones(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        Cotizaciones = db.query(modelo_cotizaciones).filter(modelo_cotizaciones.c.usuario_id == current_user).all()
        return Cotizaciones

    except Exception as e:
        logger.error(f'Error al obtener tabla Clientes: {e}')
        raise
    finally:
        db.close()
@ERP.get("/Listar_Clientes",response_model=list[esquema_cotizaciones] )
async def listar_clientes(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        ListarClientes = db.query(modelo_clientes).filter(modelo_clientes.c.usuario_id == current_user).all()
        return ListarClientes
    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        db.close()
@ERP.post("/CrearCotizacion",status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearCotizacion(cliente_id: Optional [int] = Form(None),producto: Optional [str] = Form(None),cantidad: Optional [int] = Form(None),fecha_cotizacion: Optional [date] = Form(None),total_cotizacion: Optional [int] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    """
    :param cliente_id:
    :param producto:
    :param cantidad:
    :param fecha_cotizacion:
    :param total_cotizacion:
    :param db:
    :param current_user:
    :return:  status_code=status.HTTP_201_CREATE
    """
    try:
        CrearCotizaciones = modelo_cotizaciones.insert().values(cliente_id=cliente_id,producto=producto,cantidad=cantidad,fecha_cotizacion=fecha_cotizacion,total_cotizacion=total_cotizacion,usuario_id=current_user)
        db.execute(CrearCotizaciones)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear Cotización: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


"""
/**********************

Facturación
/*/*******

"""


@ERP.post("/CrearFactura", status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearFactura(
    cliente_id: Optional[int] = Form(None),
    nombre_cliente_proveedor: Optional[str] = Form(None),
    fecha_emision: Optional[date] = Form(None),
    fecha_vencimiento: Optional[date] = Form(None),
    monto_total: Optional[float] = Form(None),
    precio_kg: Optional[float] = Form(None),
    estado: Optional[str] = Form(None),
    lote_asociado: Optional[str] = Form(None),
    destino: Optional[str] = Form(None),
    metodo_pago: Optional[str] = Form(None),
    detalle: Optional[str] = Form(None),
    tipo_venta: Optional[str] = Form(None),
    animales: Optional[List[str]] = Form(None),
    descripcion: Optional[str] = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user)
):

    try:

        #Genera el Numero de Radicado
        Radicado =generar_radicado()

        # Crea la factura
        CrearFactura = modelo_facturas.insert().values(

            fecha_emision=fecha_emision,
            radicado_factura=Radicado,
            fecha_vencimiento=fecha_vencimiento,
            monto_total=monto_total,
            destino=destino,
            estado=estado,
            lote_asociado=lote_asociado,
            tipo_venta=tipo_venta,
            metodo_pago=metodo_pago,
            detalle=detalle,
            usuario_id=current_user,
            descripcion=descripcion,
            nombre_cliente_proveedor=nombre_cliente_proveedor
        )


        IngresoFacturacion = db.execute(CrearFactura)
        db.commit()
        # Obtener el ID de la factura para asociar a la tabla
        id_factura_asociada = IngresoFacturacion.inserted_primary_key[0]

        if tipo_venta == "Venta de Animales":
            for animal in animales:
                Bovino = json.loads(animal)  # Deserializa la cadena JSON
                id_bovino = Bovino['id_bovino']  # Accede al id_bovino
                peso = Bovino['peso']  # Accede al peso
                valorUnitario = Bovino['valorUnitario']  # Accede al peso


                nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino,
                                                                      current_user=current_user)

                estado = "Vendido"

                ingresoVentas = modelo_ventas.insert().values(id_bovino=id_bovino, estado=estado,nombre_bovino=nombre_bovino,
                                                              fecha_venta=fecha_emision,
                                                              precio_venta=valorUnitario,
                                                              valor_kg_venta=precio_kg,
                                                              id_factura_asociada = id_factura_asociada,
                                                              peso_venta=peso,
                                                              usuario_id=current_user)

                db.execute(modelo_bovinos_inventario.update().values(
                    estado=estado,
                ).where(
                    modelo_bovinos_inventario.columns.id_bovino == id_bovino))

                db.execute(ingresoVentas)
                db.commit()





    except Exception as e:
        # Ampliar el log de errores para incluir detalles de la excepción y los datos recibidos
        logger.error(f'Error al Crear Factura: {e} - Datos: Cliente ID: {cliente_id}, '
                     f'Fecha de Emisión: {fecha_emision}, Fecha de Vencimiento: {fecha_vencimiento}, '
                     f'Monto Total: {monto_total}, Estado: {estado}, Método de Pago: {metodo_pago}, '
                     f'Usuario ID: {current_user}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@ERP.get("/ListarFacturas",  response_model=list[esquema_facturas],tags=["ERP"] )
async def ListarFacturas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListarFacturas = db.query(modelo_facturas).filter(modelo_facturas.c.usuario_id == current_user).all()
        return ListarFacturas

    except Exception as e:
        logger.error(f'Error al obtener tabla Facturas: {e}')
        raise
    finally:
        db.close()

@ERP.get("/ListarFactura/{factura_id}",  response_model=list[esquema_facturas],tags=["ERP"] )
async def ListarFactura(factura_id : int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListarFactura = db.query(modelo_facturas).filter(modelo_facturas.c.usuario_id == current_user,modelo_facturas.c.factura_id == factura_id).all()
        return ListarFactura

    except Exception as e:
        logger.error(f'Error al obtener la factura: {e}')
        raise
    finally:
        db.close()


@ERP.put("/EditarFactura/{factura_id}", status_code=status.HTTP_204_NO_CONTENT)
async def CambiarDatosFactura(
         factura_id : int,
         estado: Optional[str] = Form(None),
         fecha_vencimiento: Optional[date] = Form(None),
         pagos: Optional[List[str]] = Form(None),
         descripcion: Optional[str] = Form(None),
         db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    """
    Cuando se editan  Facturas y existen Abonos el realiza el Ingreso de los Abonos
    :param factura_id:
    :param estado:
    :param fecha_vencimiento:
    :param db:
    :param current_user:
    :return:
    """
    try:

            db.execute(modelo_facturas.update().values(
                estado=estado,
                fecha_vencimiento = fecha_vencimiento,
                descripcion=descripcion



            ).where(
                modelo_facturas.columns.factura_id == factura_id))
            db.commit()

            if not pagos:
                print("La lista de pagos está vacía")
            else:
                # Consultar el monto total de la factura y verificar que exista
                factura = db.query(modelo_facturas).filter(
                    modelo_facturas.c.usuario_id == current_user,
                    modelo_facturas.c.factura_id == factura_id
                ).first()

                if factura is None:
                    print("Factura no encontrada.")
                else:
                    monto_total_factura = factura[4]  # Campo del monto total de la factura
                    saldo_restante = factura[5]  # Campo del saldo restante inicial

                    # Calcular total de abonos existentes en la base de datos para esta factura
                    total_abonos_actuales = db.query(func.sum(modelo_pagos.c.monto)).filter(
                        modelo_pagos.c.factura_id == factura_id,
                        modelo_pagos.c.usuario_id == current_user
                    ).scalar() or 0  # Si no hay abonos previos, asigna 0

                    for pago in pagos:
                        abono = json.loads(pago)
                        fecha_pago = abono['fecha_pago']
                        metodo_pago = abono['metodo_pago']
                        monto_abono = float(abono['monto'])

                        # Actualizar el total de abonos con el nuevo monto de abono
                        total_abonos_actuales += monto_abono

                        # Insertar el nuevo pago en la tabla de pagos
                        db.execute(modelo_pagos.insert().values(
                            factura_id=factura_id,
                            fecha_pago=fecha_pago,
                            metodo_pago=metodo_pago,
                            monto=monto_abono,
                            usuario_id=current_user
                        ))

                        # Calcular el nuevo saldo restante
                        saldo_restante = monto_total_factura - total_abonos_actuales

                        # Determinar si la factura debe marcarse como pagada o permanecer pendiente
                        estado_factura = "pagada" if saldo_restante <= 0 else "pendiente"

                        # Actualizar saldo restante y estado de la factura en la base de datos
                        db.execute(modelo_facturas.update().values(
                            saldo_restante=saldo_restante,
                            estado=estado_factura
                        ).where(
                            modelo_facturas.c.factura_id == factura_id
                        ))
                        db.commit()


    except Exception as e:
        logger.error(f'Error al Editar Factura: {e}')
        raise

    finally:
        db.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


@ERP.get("/Abonos_Asociados/{factura_id}",response_model=list[esquema_pagos] )
async def ListarAbonosAsociados(factura_id:int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        ListaAbonos = db.query(modelo_pagos).where(modelo_pagos.columns.factura_id == factura_id).all()
        if ListaAbonos is None:
            raise HTTPException(status_code=404, detail="Factura  no encontrada")
        else:
            return ListaAbonos

    except Exception as e:
        logger.error(f'Error al obtener Abonos Asociados a las facturas : {e}')
        raise
    finally:
        db.close()

"""
*/****Cartera
"""
@ERP.get("/ConsultarCartera/{fecha_inicio}/{fecha_fin}/{tipo_factura}",  response_model=list[esquema_facturas],tags=["ERP"] )
async def ConsultarCartera(fecha_inicio : date,fecha_fin : date,tipo_factura : str, db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        # Solo realiza la consulta de los datos con los estados de pendientes y vencidas
        consulta = db.query(modelo_facturas).filter(
            modelo_facturas.c.usuario_id == current_user,
            or_(
                modelo_facturas.c.estado == "pendiente",
                modelo_facturas.c.estado == "vencida"
            )
        )

        if fecha_inicio:
            consulta = consulta.filter(modelo_facturas.c.fecha_emision >= fecha_inicio)
        if fecha_fin:
            consulta = consulta.filter(modelo_facturas.c.fecha_emision <= fecha_fin)
        if tipo_factura:
            consulta = consulta.filter(modelo_facturas.c.detalle == tipo_factura)
        print(consulta)
        return consulta.all()

    except Exception as e:
        logger.error(f'Error al obtener la factura: {e}')
        raise
    finally:
        db.close()

@ERP.get("/Calcular_Total_Ventas",tags=["ERP"])
async def CalcularVentas(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        "Consulta del total de la factura"
        ConsultaVentas = db.query(func.sum(modelo_facturas.columns.monto_total)).filter(modelo_facturas.c.detalle == "Factura de Venta",modelo_facturas.c.estado == "pagada",
                   modelo_facturas.c.usuario_id == current_user).all()
        ConsultaVentas = ConsultaVentas[0][0]

        return ConsultaVentas
    except Exception as e:
        logger.error(f'Error en Calcular TotalVentas: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()

@ERP.get("/Calcular_Total_Compras",tags=["ERP"])
async def CalcularCompras(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        "Consulta del total de la factura de compras"
        ConsultaCompras = db.query(func.sum(modelo_facturas.columns.monto_total)).filter(modelo_facturas.c.detalle == "Factura de Compra",
                   modelo_facturas.c.estado == "pagada",modelo_facturas.c.usuario_id == current_user).all()
        ConsultaCompra = ConsultaCompras[0][0]

        return ConsultaCompra
    except Exception as e:
        logger.error(f'Error en Calcular Compras: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()


@ERP.get("/Ventas_Trimestrales" )
async def VentasTrimestrales(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    La siguiente función Retorna el historial  Trimestrales

    """
    try:
        # Consulta para agrupar ventas por año y trimestre
        ventas_trimestrales = (
            db.query(
                extract('year', modelo_facturas.c.fecha_emision).label('año'),
                extract('quarter', modelo_facturas.c.fecha_emision).label('trimestre'),
                func.sum(modelo_facturas.c.monto_total).label('total_ventas')
            )
            .filter(
                modelo_facturas.c.usuario_id == current_user,
                modelo_facturas.c.detalle == "Factura de Venta",
                modelo_facturas.c.estado == "pagada"
            )
            .group_by(
                extract('year', modelo_facturas.c.fecha_emision),
                extract('quarter', modelo_facturas.c.fecha_emision)
            )
            .order_by(
                extract('year', modelo_facturas.c.fecha_emision),
                extract('quarter', modelo_facturas.c.fecha_emision)
            )
            .all()
        )

        # Formatear los resultados como lista de diccionarios
        resultado = [
            {
                "año": int(venta.año),
                "trimestre": int(venta.trimestre),
                "total_ventas": float(venta.total_ventas)
            }
            for venta in ventas_trimestrales
        ]

        return resultado

    except Exception as e:
        logger.error(f'Error al obtener reporte de ventas trimestrales: {e}')
        raise HTTPException(status_code=500, detail="Error al obtener el reporte de ventas trimestrales")
    finally:
        db.close()



@ERP.get("/facturas_estado")
async def facturas_estado(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    Comparación entre el número de facturas pagadas y las pendientes.
    """
    estados = (
        db.query(modelo_facturas.c.estado, func.count(modelo_facturas.c.factura_id).label("cantidad"))
        .group_by(modelo_facturas.c.estado)
        .filter(modelo_facturas.c.usuario_id == current_user)
        .all()
    )
    return [{"estado": e.estado, "cantidad": e.cantidad} for e in estados]

@ERP.get("/ingresos_por_destino")
async def ingresos_por_destino(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    Muestra los ingresos totales según el destino Centro de Costos
    """
    destinos = (
        db.query(modelo_facturas.c.destino, func.sum(modelo_facturas.c.monto_total).label("ingreso_total"))
        .group_by(modelo_facturas.c.destino)
        .filter(modelo_facturas.c.usuario_id == current_user)
        .all()
    )
    return [{"destino": d.destino, "ingreso_total": d.ingreso_total} for d in destinos]

@ERP.get("/analisis_saldo_restante")
async def analisis_saldo_restante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    Proporciona el promedio y total del saldo restante en las facturas.
    """
    resultado = (
        db.query(
            func.sum(modelo_facturas.c.saldo_restante).label("saldo_total"),
            func.avg(modelo_facturas.c.saldo_restante).label("saldo_promedio")
        )
        .filter(modelo_facturas.c.usuario_id == current_user)
        .one()
    )
    return {"saldo_total": resultado.saldo_total, "saldo_promedio": resultado.saldo_promedio}

@ERP.get("/tendencias_mensuales")
async def tendencias_mensuales(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    Tendencias mensuales de ventas dentro del año actual.
    """
    tendencias = (
        db.query(
            extract('month', modelo_facturas.c.fecha_emision).label("mes"),
            func.sum(modelo_facturas.c.monto_total).label("ingreso_mensual")
        )
        .filter(modelo_facturas.c.usuario_id == current_user,extract('year', modelo_facturas.c.fecha_emision) == func.extract('year', func.now()))
        .group_by(extract('month', modelo_facturas.c.fecha_emision))
        .order_by(extract('month', modelo_facturas.c.fecha_emision))
        .all()
    )
    return [{"mes": int(t.mes), "ingreso_mensual": t.ingreso_mensual} for t in tendencias]

@ERP.get("/facturacion_anual")
async def facturacion_anual(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    """
    Comparación de facturación total entre diferentes años.
    """
    facturacion = (
        db.query(
            extract('year', modelo_facturas.c.fecha_emision).label("año"),
            func.sum(modelo_facturas.c.monto_total).label("ingreso_anual")
        )
        .group_by(extract('year', modelo_facturas.c.fecha_emision))
        .filter(modelo_facturas.c.usuario_id == current_user,modelo_facturas.c.detalle == "Factura de Venta")
        .order_by(extract('year', modelo_facturas.c.fecha_emision))
        .all()
    )
    return [{"año": int(f.año), "ingreso_anual": f.ingreso_anual} for f in facturacion]





"""
/**********************

Empleados
/*/*******

"""


@ERP.post("/CrearEmpleado", status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearEmpleado(

    nombre_empleado: Optional[str] = Form(None),
    puesto: Optional[str] = Form(None),
    salario_base: Optional[float] = Form(None),
    fecha_contratacion: Optional[date] = Form(None),
    numero_seguridad_social: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    departamento: Optional[str]= Form(None),
    tipo_contrato: Optional[str]= Form(None),
    periodicidad_pago: Optional[str]= Form(None),
    detalles: Optional[str]= Form(None),

    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user)
):

    try:

        #Envia el Dato como Activo
        estado= "Activo"
        # Crea la Empleado
        Crear_Empleado = modelo_empleados.insert().values(
            nombre_empleado=nombre_empleado,
            puesto=puesto,
            salario_base=salario_base,
            fecha_contratacion=fecha_contratacion,
            numero_seguridad_social=numero_seguridad_social,
            email=email,
            telefono=telefono,
            direccion=direccion,
            departamento=departamento,
            tipo_contrato=tipo_contrato,
            periodicidad_pago=periodicidad_pago,
            detalles=detalles,
            estado=estado,
            usuario_id=current_user

        )


        db.execute(Crear_Empleado)
        db.commit()
    except Exception as e:
        logger.error(f'Error al crear Empleados: {e}')
        raise
    finally:
        db.close()



@ERP.get("/ListarEmpleados",  response_model=list[esquema_empleados],tags=["ERP"] )
async def ListarEmpleados(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListaEmpleados = db.query(modelo_empleados).filter(modelo_empleados.c.usuario_id == current_user).all()
        return ListaEmpleados

    except Exception as e:
        logger.error(f'Error al obtener tabla Empeados: {e}')
        raise
    finally:
        db.close()


@ERP.get("/ListarEmpleadosActivos",  response_model=list[esquema_empleados],tags=["ERP"] )
async def ListarEmpleadosActivos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListaEmpleados = db.query(modelo_empleados).filter(modelo_empleados.c.usuario_id == current_user,modelo_empleados.c.estado == "Activo").all()
        return ListaEmpleados

    except Exception as e:
        logger.error(f'Error al obtener tabla Empeados: {e}')
        raise
    finally:
        db.close()



@ERP.get("/Listar_Empleado/{empleado_id}",  response_model=list[esquema_empleados],tags=["ERP"] )
async def ListaEmpleado(empleado_id : int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        ListarEmpleado = db.query(modelo_empleados).filter(modelo_empleados.c.usuario_id == current_user,modelo_empleados.c.empleado_id == empleado_id).all()
        return ListarEmpleado

    except Exception as e:
        logger.error(f'Error al obtener Empleado: {e}')
        raise
    finally:
        db.close()



@ERP.put("/Editar_Empleado/{empleado_id}", status_code=status.HTTP_204_NO_CONTENT)
async def EditarEmpleado(
         empleado_id : int,
         nombre_empleado: Optional[str] = Form(None),
         puesto: Optional[str] = Form(None),
         salario_base: Optional[float] = Form(None),
         fecha_contratacion: Optional[date] = Form(None),
         numero_seguridad_social: Optional[str] = Form(None),
         email: Optional[str] = Form(None),
         telefono: Optional[str] = Form(None),
         direccion: Optional[str] = Form(None),
         departamento: Optional[str] = Form(None),
         estado: Optional[str] = Form(None),
         fecha_retiro: Optional[date] = Form(None),
         db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

            db.execute(modelo_empleados.update().values(

                nombre_empleado = nombre_empleado,
                puesto=puesto,
                salario_base=salario_base,
                fecha_contratacion=fecha_contratacion,
                numero_seguridad_social=numero_seguridad_social,
                email=email,
                telefono=telefono,
                direccion=direccion,
                departamento=departamento,
                estado=estado,
                fecha_retiro=fecha_retiro

            ).where(
                modelo_empleados.columns.empleado_id == empleado_id))
            db.commit()


    except Exception as e:
        logger.error(f'Error al Editar Empleado: {e}')
        raise

    finally:
        db.close()

    return Response(status_code=HTTP_204_NO_CONTENT)

@ERP.get("/Calcular_Total_Nomina",tags=["ERP"])
async def CalcularNomina(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        #Realiza la Busqueda del Salirio
        ConsultaNomina = db.query(func.sum(modelo_empleados.columns.salario_base)).filter(modelo_empleados.c.estado != "Retirado",
                   modelo_empleados.c.usuario_id == current_user).all()
        ListaConsultaNomina = ConsultaNomina[0][0]

        return ListaConsultaNomina
    except Exception as e:
        logger.error(f'Error en Calcular Nomina Total: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()




@ERP.post("/liquidar_nomina",tags=["ERP"])
async def LiquidarNomina(db: Session = Depends(get_database_session),
                         data: dict = Body(...),
                         current_user: Esquema_Usuario = Depends(get_current_user)):

    """
    Body(...): Utilizamos Body(...) para recibir el contenido del JSON directamente como un diccionario (dict) sin envolverlo en clases adicionales.    :param db:
    :param data:
    :param current_user:
    :return:
    """
    try:

        nomina = data.get("nomina", [])

        for empleado in nomina:

            PagoNomina = modelo_nomina.insert().values(
                empleado_id=empleado["empleado_id"],

                periodo=empleado["periodo"],
                salario_bruto=empleado["salario_bruto"],
                deducciones=empleado["deducciones"],
                recargos=empleado["recargos"],
                salario_neto=empleado["salario_neto"],
                fecha_pago=empleado["fecha_pago"],
                usuario_id=current_user

            )

            db.execute(PagoNomina)
            db.commit()




    except Exception as e:
        logger.error(f'Error al Pagar Nomina: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()

"""
Proveedores

"""


@ERP.post("/CrearProvedor",status_code=status.HTTP_201_CREATED, tags=["ERP"])
async def CrearProvedor(nombre: Optional [str] = Form(None),direccion: Optional [str] = Form(None),telefono: Optional [str] = Form(None),correo: Optional [str] = Form(None),tipoCliente: Optional [str] = Form(None),tipoPersona: Optional [str] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    """
        Registra Los proveedores
    """
    try:

        CrearProvedor = modelo_proveedores.insert().values(nombre=nombre,direccion=direccion,telefono=telefono,correo=correo,tipoCliente=tipoCliente,tipoPersona=tipoPersona,usuario_id=current_user)
        db.execute(CrearProvedor)
        db.commit()

    except Exception as e:
        logger.error(f'Error al obtener tabla Provedores: {e}')
        raise
    finally:
        db.close()
    return Response(status_code=status.HTTP_201_CREATED)


@ERP.get("/Listar_Proveedores",response_model=list[esquema_provedores] )
async def listar_proveedores(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        ListarProvedores = db.query(modelo_proveedores).filter(modelo_proveedores.c.usuario_id == current_user).all()
        return ListarProvedores
    except Exception as e:
        logger.error(f'Error  Listar Proveedores: {e}')
        raise
    finally:
        db.close()



@ERP.delete("/Eliminar_Provedor/{proveedor_id}")
async def Eliminar_cliente(proveedor_id: int,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:
        db.execute(modelo_proveedores.delete().where(modelo_proveedores.c.proveedor_id == proveedor_id))
        db.commit()
        return
    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Proveedor: {e}')
        raise
    finally:
        db.close()





"""
@ERP.get("/IndicadoresERP",response_model=list )
async def indicadores_erp(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user) ):
    try:


        itemsListarPartos = db.execute(
            modelo_historial_partos.select().where(modelo_historial_partos.columns.id_bovino == id_bovino)).all()

        itemsListarAbortos = db.execute(
            modelo_abortos.select().where(modelo_abortos.columns.id_bovino == id_bovino)).all()

        Historial = []

        # Valida si la consulta no este vacia
        if itemsListarPartos is not None:
            # Recorre la consulta para enviar los datos
            for ListarPartos in itemsListarPartos:
                Historial.append({

                    "id_bovino": ListarPartos.id_bovino,
                    "fecha_parto": ListarPartos.fecha_parto,
                    "tipo_parto": ListarPartos.tipo_parto,
                    "id_bovino_hijo": ListarPartos.id_bovino_hijo,
                    "usuario_id": ListarPartos.usuario_id,
                    "nombre_madre": ListarPartos.nombre_madre,
                    "nombre_hijo": ListarPartos.nombre_hijo,

                })
                # Valida si la consulta no este vacia
        if itemsListarAbortos is not None:
            # Recorre la consulta para enviar los datos
            for AbortosBovinos in itemsListarAbortos:
                Historial.append({

                    "id_aborto": AbortosBovinos.id_aborto,
                    "id_bovino_abortos": AbortosBovinos.id_bovino,
                    "nombre_bovino_abortos": AbortosBovinos.nombre_bovino,
                    "fecha_aborto": AbortosBovinos.fecha_aborto,
                    "causa": AbortosBovinos.causa,
                    "usuario_id": AbortosBovinos.usuario_id,

                })


        return Historial



    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        db.close()
    return consulta




"""

