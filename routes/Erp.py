'''
@autor : odvr
Librerias requeridas
'''
import logging
from datetime import  date
from http.client import HTTPException

from fastapi import APIRouter, Depends,Form,Response,status,Body
from sqlalchemy import func
from starlette.status import HTTP_204_NO_CONTENT

import crud

from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_clientes, modelo_cotizaciones, modelo_facturas, modelo_ventas, \
    modelo_bovinos_inventario, modelo_pagos, modelo_empleados, modelo_nomina
from sqlalchemy.orm import Session
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Usuario, esquema_clientes, esquema_cotizaciones, esquema_facturas, \
    esquema_pagos, esquema_empleados, esquema_nomina
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
    descripcion: Optional[str] = Form(None),
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
            usuario_id=current_user,
            descripcion=descripcion
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


            #Valida si se agrego un pago o abono a la factura

            if not pagos:
                print("La Lista Esta Vacia ")
                pass
            else:
                for pago in pagos:
                    PagosAbonos = json.loads(pago)  # Deserializa la cadena JSON
                    fecha_pago = PagosAbonos['fecha_pago']
                    metodo_pago = PagosAbonos['metodo_pago']
                    montoAbono = PagosAbonos['monto']
                    print(montoAbono)

                    IngresoPagos = modelo_pagos.insert().values(factura_id=factura_id, fecha_pago=fecha_pago,
                                                                metodo_pago=metodo_pago,
                                                                monto=montoAbono,
                                                                usuario_id=current_user
                                                                )

                    db.execute(IngresoPagos)
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