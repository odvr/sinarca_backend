'''
@autor : odvr
Librerias requeridas
'''
import logging
from datetime import  date
from fastapi import APIRouter, Depends,Form,Response,status

import crud
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_clientes, modelo_cotizaciones, modelo_facturas, modelo_ventas, \
    modelo_bovinos_inventario
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_clientes, esquema_cotizaciones, esquema_facturas
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
async def CrearClientes(nombre_cliente: Optional [str] = Form(None),direccion: Optional [str] = Form(None),telefono: Optional [str] = Form(None),email: Optional [str] = Form(None),tipo_cliente: Optional [str] = Form(None),fecha_creacion: Optional [date] = Form(None),db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
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
    fecha_emision: Optional[date] = Form(None),
    fecha_vencimiento: Optional[date] = Form(None),
    monto_total: Optional[float] = Form(None),
    precio_kg: Optional[float] = Form(None),
    estado: Optional[str] = Form(None),
    metodo_pago: Optional[str] = Form(None),
    detalle: Optional[str] = Form(None),
    tipo_venta: Optional[str] = Form(None),
    animales: Optional[List[str]] = Form(None),
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user)
):

    try:
        # Crea la factura
        CrearFactura = modelo_facturas.insert().values(
            cliente_id=cliente_id,
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            monto_total=monto_total,
            estado=estado,
            tipo_venta=tipo_venta,
            metodo_pago=metodo_pago,
            detalle=detalle,
            usuario_id=current_user
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
                print(fecha_emision)

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