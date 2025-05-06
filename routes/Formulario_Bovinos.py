
'''
Librerias requeridas
@autor : odvr
'''
from http.client import HTTPException
from typing import Optional
import logging
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends ,Form
from sqlalchemy import and_,or_
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_204_NO_CONTENT
import os
from typing import List
import uuid
from fastapi import APIRouter, UploadFile, File
import crud.crud_bovinos_inventario
from Lib.Lib_Calcular_Edad_Bovinos import calculoEdad
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.actualizacion_peso import actualizacion_peso
from Lib.endogamia import endogamia, abuelo_materno, abuela_materna, abuelo_paterno, abuela_paterna, bisabuelo_materno, \
    bisabuelo_paterno
from Lib.funcion_vientres_aptos import vientres_aptos
from config.db import   get_session,Rutabase
from fastapi import APIRouter, Response,status
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_ventas, modelo_datos_muerte, modelo_ceba, \
    modelo_carga_animal_y_consumo_agua, modelo_levante, modelo_datos_pesaje, modelo_leche, modelo_macho_reproductor, \
    modelo_compra, modelo_arbol_genealogico, modelo_registro_marca, modelo_abortos
from sqlalchemy.orm import Session

from routes.Endogamia import crear_endogamia
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico, \
    esquema_registro_marca
from fastapi.responses import JSONResponse
# Configuracion de las rutas para fash api
Formulario_Bovino = APIRouter()

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






"""
Realiza la creacion de nuevos bovinos en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""

"""
id_capacidad: Optional [int] = Form(None)
"""
@Formulario_Bovino.post(
    "/crear_bovino",
    status_code=status.HTTP_201_CREATED, tags=["Formualario_Bovinos"])
async def crear_bovinos(nombre_bovino: Optional [str] = Form(None), numero_chapeta: Optional [str] = Form(None), numero_upp: Optional [str] = Form(None), numero_siniiga: Optional [str] = Form(None),chip_asociado: Optional [str] = Form(None),fecha_nacimiento:  Optional [date] = Form(None), raza:  Optional [str] = Form(None), sexo:  Optional [str] = Form(None), marca:  Optional [str] = Form(None), proposito:  Optional [str] = Form(None),
                        mansedumbre:  Optional [str] = Form(None), estado:  Optional [str] = Form(None), compra_bovino:  Optional [str] = Form(None), fecha_pesaje:  Optional [date] = Form(None), peso:  Optional [float] = Form(None),
                        ordeno:  Optional [str] = Form(None), fecha_muerte:  Optional [date] = Form(None), razon_muerte:  Optional [str] = Form(None), numero_bono_venta:  Optional [str] = Form(None),
                        fecha_venta:  Optional [date] = Form(None), precio_venta:  Optional [int] = Form(None), razon_venta:  Optional [str] = Form(None), medio_pago:  Optional [str] = Form(None), comprador:  Optional [str] = Form(None),
                        numero_bono_compra:  Optional [str] = Form(None), fecha_compra: Optional [date] = Form(None), precio_compra: Optional [int] = Form(None), razon_compra: Optional [str] = Form(None),
                        medio_pago_compra: Optional [str] = Form(None), comprador_compras: Optional [str] = Form(None), id_bovino_madre: Optional [str] = Form(None), id_bovino_padre: Optional [str] = Form(None), inseminacion:Optional [str] = Form(None),TiposPesaje:Optional [str] = Form(None),
                        id_registro_marca: Optional [str] = Form(None),LoteSeleccionado:Optional [str] = Form(None), db: Session = Depends(get_database_session),
                        current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db,current_user=current_user)
    vientres_aptos(session=db, current_user=current_user)

    try:

        # Verifica si existe un bovino con el nombre dado
        Consulta_Nomnbres_Bovinos = db.execute(
            modelo_bovinos_inventario.select().where(
                modelo_bovinos_inventario.columns.nombre_bovino == nombre_bovino,  # Usamos el nombre enviado
                modelo_bovinos_inventario.columns.usuario_id == current_user  # Usamos el usuario actual
            )
        ).first()

        # Verifica si existe un bovino con el chip dado
        Consulta_Nomnbres_Chip = db.execute(
            modelo_bovinos_inventario.select().where(
                modelo_bovinos_inventario.columns.chip_asociado == chip_asociado,  # Usamos el chip enviado
                modelo_bovinos_inventario.columns.usuario_id == current_user  # Usamos el usuario actual
            )
        ).first()

        if Consulta_Nomnbres_Bovinos or (Consulta_Nomnbres_Chip and Consulta_Nomnbres_Chip.chip_asociado is not None):
            if Consulta_Nomnbres_Bovinos:
                print(f"Nombre duplicado: {Consulta_Nomnbres_Bovinos.nombre_bovino}")
            if Consulta_Nomnbres_Chip and Consulta_Nomnbres_Chip.chip_asociado is not None:
                print(f"Chip duplicado: {Consulta_Nomnbres_Chip.chip_asociado}")

            # Devuelve un conflicto si hay duplicados
            return Response(status_code=status.HTTP_409_CONFLICT)
        else:


            FechaDeRegistroBovino = datetime.now()
            Ruta_marca = crud.bovinos_inventario.Buscar_Ruta_Fisica_Marca(db=db, id_registro_marca=id_registro_marca,
                                                                          current_user=current_user)

            ingreso = modelo_bovinos_inventario.insert().values(nombre_bovino=nombre_bovino,
                                                                fecha_nacimiento=fecha_nacimiento,
                                                                raza=raza,
                                                                numero_chapeta = numero_chapeta,
                                                                numero_siniiga = numero_siniiga,
                                                                numero_upp=numero_upp,
                                                                chip_asociado=chip_asociado,
                                                                sexo=sexo,
                                                                marca=marca,
                                                                proposito=proposito,
                                                                mansedumbre=mansedumbre,
                                                                estado=estado,
                                                                compra_bovino=compra_bovino,
                                                                usuario_id=current_user,
                                                                ruta_imagen_marca=Ruta_marca,
                                                                fecha_de_ingreso_sistema=FechaDeRegistroBovino
                                                                )

            result = db.execute(ingreso)
            db.commit()

            # Obtener el ID del bovino insertado
            id_bovino = result.inserted_primary_key[0]

            # Animales de Ceba

            consulta = db.execute(
                modelo_ceba.select().where(
                    modelo_ceba.columns.id_bovino == id_bovino)).first()

            if consulta is None and proposito == "Ceba":
                ingresopceba = modelo_ceba.insert().values(id_bovino=id_bovino, proposito=proposito,
                                                           usuario_id=current_user, nombre_bovino=nombre_bovino)
                db.execute(ingresopceba)
                db.commit()
            else:

                db.execute(modelo_ceba.update().where(modelo_ceba.c.id_bovino == id_bovino).values(
                    proposito=proposito))
                db.commit()

            # Realiza la validacion para el macho reproductor
            consulta_macho_reproductor_bovino = db.execute(
                modelo_macho_reproductor.select().where(
                    modelo_macho_reproductor.columns.id_bovino == id_bovino)).first()

            if consulta_macho_reproductor_bovino is None and proposito == "Macho Reproductor":
                CrearMacho = modelo_macho_reproductor.insert().values(id_bovino=id_bovino, usuario_id=current_user,
                                                                      nombre_bovino=nombre_bovino)

                db.execute(CrearMacho)
                db.commit()
            else:

                db.execute(
                    modelo_macho_reproductor.update().where(modelo_macho_reproductor.c.id_bovino == id_bovino).values(
                        id_bovino=id_bovino))
                db.commit()

            # Crea los animales de levante

            consultaLevante = db.execute(
                modelo_levante.select().where(
                    modelo_levante.columns.id_bovino == id_bovino)).first()

            if consultaLevante is None and proposito == "Levante":
                ingresoplevante = modelo_levante.insert().values(id_bovino=id_bovino, proposito=proposito,
                                                                 usuario_id=current_user, nombre_bovino=nombre_bovino)

                db.execute(ingresoplevante)
                db.commit()

            else:

                db.execute(modelo_levante.update().where(modelo_levante.c.id_bovino == id_bovino).values(
                    id_bovino=id_bovino, proposito=proposito, nombre_bovino=nombre_bovino))
                db.commit()

                db.commit()
            # Crea el animal con la fecha de pesaje

            ingresoFechaPesaje = modelo_datos_pesaje.insert().values(id_bovino=id_bovino, fecha_pesaje=fecha_pesaje,
                                                                     peso=peso, usuario_id=current_user,
                                                                     nombre_bovino=nombre_bovino,
                                                                     tipo_pesaje=TiposPesaje)

            db.execute(ingresoFechaPesaje)

            db.commit()

            # Crea la carga Animal

            ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(id_bovino=id_bovino,
                                                                                    usuario_id=current_user,
                                                                                    nombre_bovino=nombre_bovino)
            db.execute(ingresoCargaAnimal)

            db.commit()

            """
            Codigo para crear produccion de leche
            """
            consultaLeche = db.execute(
                modelo_leche.select().where(
                    modelo_leche.columns.id_bovino == id_bovino)).first()

            if consultaLeche is None and proposito == "Leche":
                ingresopleche = modelo_leche.insert().values(id_bovino=id_bovino,

                                                             ordeno=ordeno, proposito=proposito,
                                                             usuario_id=current_user, nombre_bovino=nombre_bovino)

                db.execute(ingresopleche)
                db.commit()
            else:

                db.execute(modelo_leche.update().where(modelo_leche.c.id_bovino == id_bovino).values(
                    id_bovino=id_bovino,

                    ordeno=ordeno, proposito=proposito))
                db.commit()

            """
            Crea el registro de Muerte si el estado es muerto 
            """
            consulta_Estado_Muerte = db.execute(
                modelo_datos_muerte.select().where(
                    modelo_datos_muerte.columns.id_bovino == id_bovino)).first()

            if consulta_Estado_Muerte is None and estado == "Muerto":
                ingresoRegistroMuerte = modelo_datos_muerte.insert().values(id_bovino=id_bovino, estado=estado,
                                                                            fecha_muerte=fecha_muerte,
                                                                            razon_muerte=razon_muerte,
                                                                            usuario_id=current_user,
                                                                            nombre_bovino=nombre_bovino
                                                                            )
                db.execute(ingresoRegistroMuerte)
                db.commit()


            else:

                db.execute(modelo_datos_muerte.update().where(modelo_datos_muerte.c.id_bovino == id_bovino).values(
                    estado=estado, razon_muerte=razon_muerte, fecha_muerte=fecha_muerte, nombre_bovino=nombre_bovino))

                db.commit()

            """
            Crea la venta 
            """
            consulta_Venta = db.execute(
                modelo_ventas.select().where(
                    modelo_ventas.columns.id_bovino == id_bovino)).first()

            if consulta_Venta is None and estado == "Vendido":
                ingresoVentas = modelo_ventas.insert().values(id_bovino=id_bovino, estado=estado,
                                                              numero_bono_venta=numero_bono_venta,
                                                              fecha_venta=fecha_venta,
                                                              precio_venta=precio_venta, razon_venta=razon_venta,
                                                              medio_pago=medio_pago, comprador=comprador,
                                                              usuario_id=current_user, nombre_bovino=nombre_bovino)
                db.execute(ingresoVentas)
                db.commit()


            else:

                db.execute(modelo_ventas.update().where(modelo_ventas.c.id_bovino == id_bovino).values(
                    estado=estado, numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                    precio_venta=precio_venta, razon_venta=razon_venta,
                    medio_pago=medio_pago, comprador=comprador, nombre_bovino=nombre_bovino))
                db.commit()

            """ 
                    Crea la compra si  valida que sea comprado
                    """
            consulta_Compra = db.execute(
                modelo_compra.select().where(
                    modelo_compra.columns.id_bovino == id_bovino)).first()

            if consulta_Compra is None and compra_bovino == "Si":
                ingresoCompra = modelo_compra.insert().values(id_bovino=id_bovino, estado=estado,
                                                              numero_bono_compra=numero_bono_compra,
                                                              fecha_compra=fecha_compra,
                                                              precio_compra=precio_compra, razon_compra=razon_compra,
                                                              medio_pago_compra=medio_pago_compra,
                                                              comprador=comprador_compras,
                                                              usuario_id=current_user, nombre_bovino=nombre_bovino)
                db.execute(ingresoCompra)

                db.commit()


            else:

                db.execute(modelo_compra.update().where(modelo_compra.c.id_bovino == id_bovino).values(
                    estado=estado, numero_bono_compra=numero_bono_compra, fecha_compra=fecha_compra,
                    precio_compra=precio_compra, razon_compra=razon_compra,
                    medio_pago_compra=medio_pago_compra, comprador=comprador_compras, usuario_id=current_user))
                db.commit()

            """
            Crear Indice de Endogamia

            """

            # Asigna el Lota no esta seleccionado pasa al siguiente items

            if LoteSeleccionado == "undefined":
                pass
            else:

                db.execute(modelo_bovinos_inventario.update().values(

                    nombre_lote_bovino=LoteSeleccionado

                ).where(
                    modelo_bovinos_inventario.columns.id_bovino == id_bovino))
                db.commit()

            if id_bovino_madre == "undefined" and id_bovino_padre == "undefined":
                pass

            if inseminacion == "Si":
                id_bovino_padre = crud.bovinos_inventario.Buscar_ID_Nombre_Padre(db=db, id_bovino_padre=id_bovino_padre,current_user=current_user)
                print(type(id_bovino_padre))
                ingresoEndogamiaInseminacion = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                                            id_bovino_madre=id_bovino_madre,
                                                                            id_bovino_padre=id_bovino_padre,
                                                                            inseminacion=inseminacion,
                                                                            usuario_id=current_user
                                                                            )

                db.execute(ingresoEndogamiaInseminacion)
                db.commit()

            if inseminacion == "0":
                pass
            if inseminacion == "No":

                ingresoEndogamia = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                                            id_bovino_madre=id_bovino_madre,
                                                                            id_bovino_padre=id_bovino_padre,
                                                                            usuario_id=current_user,
                                                                            inseminacion=inseminacion
                                                                            )

                db.execute(ingresoEndogamia)
                db.commit()
                """
                    ingresoEndogamia = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                     id_bovino_madre=id_bovino_madre,
                                                     id_bovino_padre=id_bovino_padre,usuario_id=current_user,
                                                     inseminacion=inseminacion
                                                   )


                     db.execute(ingresoEndogamia)
                    db.commit()
                """
            calculoEdad(db=db, current_user=current_user)
            actualizacion_peso(session=db, current_user=current_user)
            eliminarduplicados(db=db, current_user=current_user)


            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id_bovino": nombre_bovino})


    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de inventarios: {e}')
        raise
    finally:
        db.close()


@Formulario_Bovino.post(
    "/CrearBovinosMasivo",
    status_code=status.HTTP_201_CREATED, tags=["Formualario_Bovinos"]
)
async def crear_bovino_masivo(bovinos: List[dict], db: Session = Depends(get_database_session),
                              current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        existentes = []  # Lista para almacenar los bovinos que ya existían
        creados = 0  # Contador de bovinos creados exitosamente

        for bovino in bovinos:
            nombre_bovino = bovino['nombre_bovino']

            # Verificar si el bovino ya existe
            Consulta_Nomnbres_Bovinos = db.execute(modelo_bovinos_inventario.select().where(
                modelo_bovinos_inventario.columns.nombre_bovino == nombre_bovino,
                modelo_bovinos_inventario.columns.usuario_id == current_user)).all()

            if Consulta_Nomnbres_Bovinos:
                existentes.append(nombre_bovino)
                continue  # Saltar este bovino y continuar con el siguiente

            # Si no existe, proceder con la creación
            fecha_nacimiento = bovino['fecha_nacimiento']
            raza = bovino['raza']
            sexo = bovino['sexo']
            marca = bovino['marca']
            id_registro_marca = bovino['idRegistroMarca']
            proposito = bovino['proposito']
            numero_chapeta = bovino['numero_chapeta']
            numero_siniiga = bovino['numero_siniiga']
            numero_upp = bovino['numero_upp']
            lote = bovino['lote']
            mansedumbre = "Manso"
            estado = bovino['estado']
            ordeno = "No"
            peso = 0
            if estado == "Vivo":
                estado = "Vivo"

            Ruta_marca = crud.bovinos_inventario.Buscar_Ruta_Fisica_Marca(db=db, id_registro_marca=id_registro_marca,
                                                                          current_user=current_user)

            FechaDeRegistroBovino = datetime.now()

            ingreso = modelo_bovinos_inventario.insert().values(
                nombre_bovino=nombre_bovino,
                fecha_nacimiento=fecha_nacimiento,
                raza=raza,
                peso=peso,
                sexo=sexo,
                marca=marca,
                ruta_imagen_marca=Ruta_marca,
                proposito=proposito,
                mansedumbre=mansedumbre,
                estado=estado,
                usuario_id=current_user,
                numero_chapeta=numero_chapeta,
                nombre_lote_bovino=lote,
                numero_siniiga=numero_siniiga,
                numero_upp=numero_upp,
                fecha_de_ingreso_sistema=FechaDeRegistroBovino
            )

            result = db.execute(ingreso)
            db.commit()
            calculoEdad(db=db, current_user=current_user)
            crud.crud_bovinos_inventario.bovinos_inventario.ActualizarCantidadAnimalesEnLote(db=db,
                                                                                             current_user=current_user)

            # Obtener el ID del bovino insertado
            id_bovino = result.inserted_primary_key[0]

            # Animales de Ceba
            if proposito == "Ceba":
                consulta = db.execute(
                    modelo_ceba.select().where(
                        modelo_ceba.columns.id_bovino == id_bovino)).first()
                if consulta is None:
                    ingresopceba = modelo_ceba.insert().values(
                        id_bovino=id_bovino,
                        proposito=proposito,
                        usuario_id=current_user,
                        nombre_bovino=nombre_bovino
                    )
                    db.execute(ingresopceba)
                    db.commit()

            # Macho reproductor
            if proposito == "Macho Reproductor":
                consulta_macho_reproductor_bovino = db.execute(
                    modelo_macho_reproductor.select().where(
                        modelo_macho_reproductor.columns.id_bovino == id_bovino)).first()
                if consulta_macho_reproductor_bovino is None:
                    CrearMacho = modelo_macho_reproductor.insert().values(
                        id_bovino=id_bovino,
                        usuario_id=current_user,
                        nombre_bovino=nombre_bovino
                    )
                    db.execute(CrearMacho)
                    db.commit()

            # Animales de levante
            if proposito == "Levante":
                consultaLevante = db.execute(
                    modelo_levante.select().where(
                        modelo_levante.columns.id_bovino == id_bovino)).first()
                if consultaLevante is None:
                    ingresoplevante = modelo_levante.insert().values(
                        id_bovino=id_bovino,
                        proposito=proposito,
                        usuario_id=current_user,
                        nombre_bovino=nombre_bovino
                    )
                    db.execute(ingresoplevante)
                    db.commit()

            # Crea la carga Animal
            ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(
                id_bovino=id_bovino,
                usuario_id=current_user,
                nombre_bovino=nombre_bovino
            )
            db.execute(ingresoCargaAnimal)
            db.commit()

            # Producción de leche
            if proposito == "Leche":
                consultaLeche = db.execute(
                    modelo_leche.select().where(
                        modelo_leche.columns.id_bovino == id_bovino)).first()
                if consultaLeche is None:
                    ingresopleche = modelo_leche.insert().values(
                        id_bovino=id_bovino,
                        ordeno=ordeno,
                        proposito=proposito,
                        usuario_id=current_user,
                        nombre_bovino=nombre_bovino
                    )
                    db.execute(ingresopleche)
                    db.commit()

            # Registro de ventas
            if estado == "Vendido":
                consulta_Venta = db.execute(
                    modelo_ventas.select().where(
                        modelo_ventas.columns.id_bovino == id_bovino)).first()

                if consulta_Venta is None:
                    ingresoVentas = modelo_ventas.insert().values(
                        id_bovino=id_bovino,
                        estado=estado,
                        numero_bono_venta=None,
                        fecha_venta=datetime.now(),
                        precio_venta=None,
                        razon_venta=None,
                        medio_pago=None,
                        comprador=None,
                        usuario_id=current_user,
                        nombre_bovino=nombre_bovino
                    )
                    db.execute(ingresoVentas)
                    db.commit()

            creados += 1  # Incrementar contador de bovinos creados

        # Preparar respuesta
        response = {
            "message": f"Se crearon {creados} bovinos exitosamente",
            "creados": creados,
            "total_recibidos": len(bovinos)
        }

        if existentes:
            response["existentes"] = existentes
            response["total_existentes"] = len(existentes)

        return response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar los bovinos: {e}")
    finally:
        db.close()

"""
Ingresa los datos para el reporte de VENTA para el animal

"""
@Formulario_Bovino.post("/crear_venta/{id_bovino}/{estado}/{numero_bono_venta}/{fecha_venta}/{precio_venta}/{razon_venta}/{medio_pago}/{comprador}",status_code=200,tags=["Formualario_Bovinos"])
async def crear_reporte_ventas(id_bovino:str,estado:str,numero_bono_venta:str,fecha_venta:date,precio_venta:int,razon_venta:str,medio_pago:str,comprador:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        consulta = db.execute(
            modelo_ventas.select().where(
                modelo_ventas.columns.id_bovino == id_bovino)).first()
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db,id_bovino=id_bovino,current_user=current_user)

        if consulta is None:
            ingresoVentas = modelo_ventas.insert().values(id_bovino=id_bovino, estado=estado,
                                                          numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                                                          precio_venta=precio_venta, razon_venta=razon_venta,
                                                          medio_pago=medio_pago, comprador=comprador,usuario_id=current_user,nombre_bovino=nombre_bovino)
            db.execute(ingresoVentas)
            db.commit()


        else:

            db.execute(modelo_ventas.update().where(modelo_ventas.c.id_bovino == id_bovino).values(
                estado=estado,numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                                                          precio_venta=precio_venta, razon_venta=razon_venta,
                                                          medio_pago=medio_pago, comprador=comprador))
            db.commit()








    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE VENTA: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)




"""
Ingresa los datos para el reporte de Animales Muertos

"""
@Formulario_Bovino.post("/crear_registro_muerte/{id_bovino}/{estado}/{fecha_muerte}/{razon_muerte}",status_code=200,tags=["Formualario_Bovinos"])
async def crear_registro_muerte(id_bovino:str,estado:str,fecha_muerte:date,razon_muerte:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        """
        Valida si el animal ya existe en la tabla 
        """
        consulta = db.execute(
            modelo_datos_muerte.select().where(
                modelo_datos_muerte.columns.id_bovino == id_bovino)).first()
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino,current_user=current_user)
        if consulta is None:
            ingresoRegistroMuerte = modelo_datos_muerte.insert().values(id_bovino=id_bovino, estado=estado,
                                                                        fecha_muerte=fecha_muerte,
                                                                        razon_muerte=razon_muerte,usuario_id=current_user,nombre_bovino=nombre_bovino)
            db.execute(ingresoRegistroMuerte)
            db.commit()


        else:

            db.execute(modelo_datos_muerte.update().where(modelo_datos_muerte.c.id_bovino == id_bovino).values(
                estado=estado,razon_muerte=razon_muerte, fecha_muerte=fecha_muerte,nombre_bovino=nombre_bovino))

            db.commit()


    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE MUERTE: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)




@Formulario_Bovino.post("/CrearAborto/{id_bovino}/{fecha_aborto}/{causas_aborto}",status_code=200,tags=["Formualario_Bovinos"])
async def crear_registro_abortos_bovinos(id_bovino:str,fecha_aborto:date,causas_aborto:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:
        #busca el nombre del animal
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino, current_user=current_user)
        ingresoRegistroAborto = modelo_abortos.insert().values(id_bovino=id_bovino, fecha_aborto=fecha_aborto,
                                                                    causa=causas_aborto,
                                                                    usuario_id=current_user,
                                                                    nombre_bovino=nombre_bovino)
        db.execute(ingresoRegistroAborto)
        db.commit()







    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE ABORTOS: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""
Crear Ceba
"""
@Formulario_Bovino.post(
    "/crear_prod_ceba/{id_bovino}/{proposito}",
    status_code=status.HTTP_201_CREATED,tags=["Formualario_Bovinos"])
async def CrearProdCeba(id_bovino: str,proposito:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):

    try:

        consulta = db.execute(
            modelo_ceba.select().where(
                modelo_ceba.columns.id_bovino == id_bovino)).first()
        nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino,
                                                                               current_user=current_user)



        if consulta is None:
            ingresopceba = modelo_ceba.insert().values(id_bovino=id_bovino, proposito=proposito,usuario_id=current_user,nombre_bovino=nombre_bovino)
            db.execute(ingresopceba)
            db.commit()
        else:

            db.execute(modelo_ceba.update().where(modelo_ceba.c.id_bovino == id_bovino).values(
                proposito=proposito,nombre_bovino=nombre_bovino))
            db.commit()






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Ceba: {e}')
        raise
    finally:
        db.close()

    return Response( status_code=status.HTTP_201_CREATED)


"""
Funcion Caga Animal
"""
@Formulario_Bovino.post(
    "/crear_carga_animal/{id_bovino}",
    status_code=status.HTTP_201_CREATED,tags=["Formualario_Bovinos"])
async def CrearCargaAnimal(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db,current_user=current_user)
    nombre_bovino = crud.bovinos_inventario.Buscar_Nombre(db=db, id_bovino=id_bovino,
                                                                           current_user=current_user)

    try:
        ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(id_bovino=id_bovino,usuario_id=current_user,nombre_bovino=nombre_bovino)


        db.execute(ingresoCargaAnimal)
        db.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla CARGA ANIMAL: {e}')
        raise
    finally:
        db.close()

    return Response(status_code=status.HTTP_201_CREATED)


@Formulario_Bovino.get("/listar_bovino/{id_bovino}", response_model=Esquema_bovinos ,tags=["Formualario_Bovinos"])
async def id_inventario_bovino(id_bovino: str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        consulta = db.execute(
            modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()



    except Exception as e:

        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    # condb.commit()
    return consulta

"""
La siguiente función realiza la Busqueda del Codigo generado Por los Chip Bovinos 
"""

@Formulario_Bovino.get("/BuscarChip/{chipManual}", response_model=int, tags=["Formualario_Bovinos"])
async def Buscar_id_Chip(
    chipManual: str,
    db: Session = Depends(get_database_session),
    current_user: Esquema_Usuario = Depends(get_current_user)
):
    try:
        consulta = db.execute(
            modelo_bovinos_inventario.select().where(
                modelo_bovinos_inventario.columns.chip_asociado == chipManual
            )
        ).first()

        if consulta is None:
            raise HTTPException(status_code=404, detail="Chip no encontrado en la base de datos")

        # Extraer y retornar solo el id_bovino
        return consulta.id_bovino

    except Exception as e:
        logger.error(f'Error al obtener Chip del Bovino: {e}')
        raise





'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@Formulario_Bovino.put("/cambiar_datos_bovino/{id_bovino}", status_code=status.HTTP_201_CREATED)
async def cambiar_esta_bovino(
        id_bovino:str,
        fecha_nacimiento: Optional[date] = Form(None),
        edad: Optional[int] = Form(None),
        raza: Optional[str] = Form(None),
        sexo: Optional[str] = Form(None),
        peso: Optional[float] = Form(None),
        marca: Optional[str] = Form(None),
        proposito: Optional[str] = Form(None),
        mansedumbre: Optional[str] = Form(None),
        estado: Optional[str] = Form(None),
        compra_bovino: Optional[str] = Form(None),
        ruta_imagen_marca: Optional[str] = Form(None),
        numero_chapeta: Optional[str] = Form(None),
        numero_siniiga: Optional[str] = Form(None),
        numero_upp: Optional[str] = Form(None),
        db: Session = Depends(get_database_session),
        current_user: Esquema_Usuario = Depends(get_current_user)
):
    try:

        if not id_bovino:
            logger.error("El ID del bovino no puede ser None")
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="El ID del bovino es requerido")

              # Busca la ruta física del path de la foto Marca ya que desde el frontend se envía el ID de la tabla
        Ruta_marca = crud.bovinos_inventario.Buscar_Ruta_Fisica_Marca(db=db, id_registro_marca=ruta_imagen_marca,
                                                                      current_user=current_user)


        # Realiza la actualización
        db.execute(modelo_bovinos_inventario.update().values(
            fecha_nacimiento=fecha_nacimiento,
            edad=edad,
            raza=raza,
            sexo=sexo,
            peso=peso,
            marca=marca,
            proposito=proposito,
            mansedumbre=mansedumbre,
            estado=estado,
            compra_bovino=compra_bovino,
            ruta_imagen_marca=Ruta_marca,

            numero_chapeta=numero_chapeta,
            numero_siniiga = numero_siniiga,
            numero_upp=numero_upp
        ).where(modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        db.commit()

        if ruta_imagen_marca == "null":
            db.execute(modelo_bovinos_inventario.update().values(
                fecha_nacimiento=fecha_nacimiento,
                edad=edad,
                raza=raza,
                sexo=sexo,
                peso=peso,
                marca=marca,
                proposito=proposito,
                mansedumbre=mansedumbre,
                estado=estado,
                compra_bovino=compra_bovino,
                numero_chapeta=numero_chapeta,
                numero_siniiga = numero_siniiga,
                numero_upp = numero_upp
            ).where(modelo_bovinos_inventario.columns.id_bovino == id_bovino))
            db.commit()

        logger.info(f'Bovino con ID {id_bovino} actualizado correctamente')
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise
    finally:
        db.close()
# Montar la carpeta de archivos estáticos
#Formulario_Bovino.mount("/static", StaticFiles(directory="../static/uploads"), name="static")




@Formulario_Bovino.post("/Guardar/FotoPerfil/{id_bovino}")
async def create_user_profile(id_bovino:str,file: UploadFile = File(...),
                                  db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)
                                  ):
    ConsultarNombre = db.query(modelo_bovinos_inventario).filter(
        modelo_bovinos_inventario.columns.nombre_bovino == id_bovino,
        modelo_bovinos_inventario.c.usuario_id == current_user).first()



    contents = await file.read()
    # Obtiene el nombre del archivo sin la extensión
    filename, file_extension = os.path.splitext(file.filename)
    new_filename = f"{id_bovino}_{filename}_{uuid.uuid4().hex}{file_extension}"
    # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original

    # Ruta donde guardar el archivo
    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, new_filename)

    # Guarda el archivo en la ubicación deseada
    with open(file_path, "wb") as f:
        f.write(contents)

    # Devuelve la URL del archivo para que el usuario pueda acceder a él
    file_url = f"/static/uploads/{new_filename}"

    Buscar_Datos_Foto_Perfil = crud.bovinos_inventario.Buscar_Ruta_Foto_Perfil(db=db, id_bovino=id_bovino,
                                                                               current_user=current_user)

    if ConsultarNombre is None:
        raise HTTPException(status_code=404, detail="Bovino no encontrado")


    else:
        Nombre_Bovino = ConsultarNombre.nombre_bovino

        db.execute(modelo_bovinos_inventario.update().values(ruta_fisica_foto_perfil=file_url).where(
            modelo_bovinos_inventario.c.nombre_bovino == Nombre_Bovino,
            modelo_bovinos_inventario.c.usuario_id == current_user))
        db.commit()
        db.close()
        return {"filename": new_filename, "file_url": file_url}

""" 
API Que realiza el cambio de la foto de Perfil
"""


@Formulario_Bovino.post("/GuardarCambiar/FotoPerfil/{id_bovino}")
async def CambiarFotoPerfilBovino(id_bovino: str, file: UploadFile = File(...),
                              db: Session = Depends(get_database_session),
                              current_user: Esquema_Usuario = Depends(get_current_user)
                              ):
    ConsultarNombre = db.query(modelo_bovinos_inventario).filter(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino,
        modelo_bovinos_inventario.c.usuario_id == current_user).first()
    Buscar_Datos_Foto_Perfil = crud.bovinos_inventario.Buscar_Ruta_Foto_Perfil(db=db, id_bovino=id_bovino,
                                                                               current_user=current_user)


    Buscar = crud.bovinos_inventario.VerificarConsultaDatosFotoPerfilBovino(Buscar_Datos_Foto_Perfil=Buscar_Datos_Foto_Perfil,Rutabase=Rutabase)




    try:
        while Buscar:
            if ConsultarNombre is None:
                raise HTTPException(status_code=404, detail="Bovino no encontrado")

            if Buscar == "ConsultaVacia":

                contents = await file.read()
                # Obtiene el nombre del archivo sin la extensión
                filename, file_extension = os.path.splitext(file.filename)
                # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original
                new_filename = f"{id_bovino}_{filename}_{uuid.uuid4().hex}{file_extension}"

                # Ruta donde guardar el archivo
                upload_folder = os.path.join("static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, new_filename)

                # Guarda el archivo en la ubicación deseada
                with open(file_path, "wb") as f:
                    f.write(contents)

                # Devuelve la URL del archivo para que el usuario pueda acceder a él
                file_url = f"/static/uploads/{new_filename}"

                Nombre_Bovino = ConsultarNombre.nombre_bovino
                print(Nombre_Bovino)

                db.execute(modelo_bovinos_inventario.update().values(ruta_fisica_foto_perfil=file_url).where(
                    modelo_bovinos_inventario.c.nombre_bovino == Nombre_Bovino,
                    modelo_bovinos_inventario.c.usuario_id == current_user))

                db.commit()
                db.close()

                return {"filename": new_filename, "file_url": file_url}
                break

            else:
                # print(RutasUnidas) os.path.isfile(RutasUnidas) and Buscar_Datos_Foto_Perfil != None
                os.remove(Buscar)

                contents = await file.read()
                # Obtiene el nombre del archivo sin la extensión
                filename, file_extension = os.path.splitext(file.filename)
                # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original
                new_filename = f"{id_bovino}_{filename}_{uuid.uuid4().hex}{file_extension}"

                # Ruta donde guardar el archivo
                upload_folder = os.path.join("static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, new_filename)

                # Guarda el archivo en la ubicación deseada
                with open(file_path, "wb") as f:
                    f.write(contents)

                # Devuelve la URL del archivo para que el usuario pueda acceder a él
                file_url = f"/static/uploads/{new_filename}"

                Nombre_Bovino = ConsultarNombre.nombre_bovino

                db.execute(modelo_bovinos_inventario.update().values(ruta_fisica_foto_perfil=file_url).where(
                    modelo_bovinos_inventario.c.nombre_bovino == Nombre_Bovino,
                    modelo_bovinos_inventario.c.usuario_id == current_user))

                db.commit()
                db.close()

                return {"filename": new_filename, "file_url": file_url}

                break

    except FileNotFoundError and NotADirectoryError as e:
        logger.error("Nose pudo Cargar Imagen "+ e)


@Formulario_Bovino.post("/GuardarMarca/{nombre_marca_propietario}")
async def Crear_Marca_bovino(nombre_marca_propietario: str, file: UploadFile = File(...),
                             db: Session = Depends(get_database_session), current_user: Esquema_Usuario = Depends(get_current_user)):

    contents = await file.read()

    hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Obtiene el nombre del archivo y la extensión
    filename, file_extension = os.path.splitext(file.filename)
    new_filename = f"{current_user}_{filename}_{uuid.uuid4().hex}{file_extension}"
    # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original

    # Ruta donde guardar el archivo
    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, new_filename)

    # Guarda el archivo en la ubicación deseada
    with open(file_path, "wb") as f:
        f.write(contents)

    # Devuelve la URL del archivo para que el usuario pueda acceder a él
    url_registro_marca = f"/static/uploads/{new_filename}"

    db.execute(modelo_registro_marca.insert().values(ruta_marca=url_registro_marca, nombre_marca_propietario=nombre_marca_propietario, usuario_id=current_user))
    db.commit()
    db.close()

    return {"filename": new_filename, "file_url": url_registro_marca}
@Formulario_Bovino.get("/ListarMarcasImagenes", response_model=list[esquema_registro_marca],tags=["Formualario_Bovinos"])
async def id_inventario_bovino(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:

        Marca = db.query(modelo_registro_marca). \
            filter(modelo_registro_marca.c.usuario_id == current_user).all()



    except Exception as e:

        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    # condb.commit()
    return Marca



