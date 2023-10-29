
'''
Librerias requeridas
@autor : odvr
'''
from http.client import HTTPException
from typing import Optional
import logging
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import and_
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_204_NO_CONTENT
import os
import uuid
from fastapi import APIRouter, UploadFile, File
import crud.crud_bovinos_inventario
from Lib.Lib_eliminar_duplicados_bovinos import eliminarduplicados
from Lib.endogamia import endogamia
from Lib.funcion_vientres_aptos import vientres_aptos
from config.db import   get_session
from fastapi import APIRouter, Response,status
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_ventas, modelo_datos_muerte, modelo_ceba, \
    modelo_carga_animal_y_consumo_agua, modelo_levante, modelo_datos_pesaje, modelo_leche, modelo_macho_reproductor, \
    modelo_compra, modelo_arbol_genealogico
from sqlalchemy.orm import Session

from routes.Endogamia import crear_endogamia
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, Esquema_bovinos, esquema_arbol_genealogico

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


@Formulario_Bovino.post("/crear_bovino/{nombre_bovino}/{fecha_nacimiento}/{raza}/{sexo}/{marca}/{proposito}/{mansedumbre}/{estado}/{compra_bovino}/{fecha_pesaje}/{peso}/{datos_prenez}/{ordeno}/{fecha_muerte}/{razon_muerte}/{numero_bono_venta}/{fecha_venta}/{precio_venta}/{razon_venta}/{medio_pago}/{comprador}/{numero_bono_compra}/{fecha_compra}/{precio_compra}/{razon_compra}/{medio_pago_compra}/{comprador_compras}/{id_bovino_madre}/{id_bovino_padre}", status_code=status.HTTP_201_CREATED,tags=["Formualario_Bovinos"])
async def crear_bovinos(nombre_bovino:str,fecha_nacimiento:date,raza:str,sexo:str,marca:str,proposito:str,mansedumbre:str,estado:str,compra_bovino:str,fecha_pesaje:date,peso:float,datos_prenez: str, ordeno: str,fecha_muerte: date,razon_muerte:str,numero_bono_venta:str,fecha_venta:date,precio_venta:int,razon_venta:str,medio_pago:str,comprador:str,numero_bono_compra:str,fecha_compra:date,precio_compra:int,razon_compra:str,medio_pago_compra:str,comprador_compras:str,id_bovino_madre: str,id_bovino_padre:str, db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    eliminarduplicados(db=db)

    vientres_aptos(session=db,current_user=current_user)

    try:

        Consulta_Nomnbres_Bovinos = db.execute(
            modelo_bovinos_inventario.select().where(
                and_(
                    modelo_bovinos_inventario.columns.nombre_bovino == nombre_bovino,
                    modelo_bovinos_inventario.columns.usuario_id == current_user
                )
            )
        ).first()

        if Consulta_Nomnbres_Bovinos is None:
            ingreso = modelo_bovinos_inventario.insert().values(nombre_bovino=nombre_bovino,
                                                                fecha_nacimiento=fecha_nacimiento,
                                                                raza=raza,
                                                                sexo=sexo,
                                                                marca=marca,
                                                                proposito=proposito,
                                                                mansedumbre=mansedumbre,
                                                                estado=estado,
                                                                compra_bovino=compra_bovino,
                                                                usuario_id=current_user
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
                                                                     nombre_bovino=nombre_bovino)

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
                                                             datos_prenez=datos_prenez,
                                                             ordeno=ordeno, proposito=proposito,
                                                             usuario_id=current_user, nombre_bovino=nombre_bovino)

                db.execute(ingresopleche)
                db.commit()
            else:

                db.execute(modelo_leche.update().where(modelo_leche.c.id_bovino == id_bovino).values(
                    id_bovino=id_bovino,
                    datos_prenez=datos_prenez,
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
                                                                            usuario_id=current_user,nombre_bovino=nombre_bovino
                                                                            )
                db.execute(ingresoRegistroMuerte)
                db.commit()


            else:

                db.execute(modelo_datos_muerte.update().where(modelo_datos_muerte.c.id_bovino == id_bovino).values(
                    estado=estado, razon_muerte=razon_muerte, fecha_muerte=fecha_muerte,nombre_bovino=nombre_bovino))

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
                                                              usuario_id=current_user,nombre_bovino=nombre_bovino)
                db.execute(ingresoVentas)
                db.commit()


            else:

                db.execute(modelo_ventas.update().where(modelo_ventas.c.id_bovino == id_bovino).values(
                    estado=estado, numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                    precio_venta=precio_venta, razon_venta=razon_venta,
                    medio_pago=medio_pago, comprador=comprador,nombre_bovino=nombre_bovino))
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
                                                              medio_pago_compra=medio_pago_compra, comprador=comprador_compras,
                                                              usuario_id=current_user,nombre_bovino=nombre_bovino)
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

            #crear_endogamia(id_bovino=id_bovino,id_bovino_madre=id_bovino_madre,id_bovino_padre=id_bovino_padre)
            if id_bovino_madre == "undefined" and id_bovino_padre == "undefined":
                pass
            else:
                ingresoEndogamia = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                                            id_bovino_madre=id_bovino_madre,
                                                                            id_bovino_padre=id_bovino_padre,
                                                                            usuario_id=current_user
                                                                            )

                db.execute(ingresoEndogamia)
                db.commit()
                endogamia(condb=db)


            return Response(status_code=status.HTTP_201_CREATED)

        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)







    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de inventarios: {e}')
        raise
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
    eliminarduplicados(db=db)
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


'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@Formulario_Bovino.put("/cambiar_datos_bovino/{id_bovino}/{fecha_nacimiento}/{edad}/{raza}/{sexo}/{peso}/{marca}/{proposito}/{mansedumbre}/{estado}/{compra_bovino}", status_code=status.HTTP_201_CREATED)
async def cambiar_esta_bovino(id_bovino:str,fecha_nacimiento:date,edad:int,raza:str,sexo:str,peso:float,marca:str,proposito:str,mansedumbre:str,estado:str,compra_bovino:str,db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:


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
            compra_bovino=compra_bovino

            ).where(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        db.commit()

            # Retorna una consulta con el id actualizado
            #resultado_actualizado = condb.execute(
            #modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise

    finally:
        db.close()

    return Response(status_code=HTTP_204_NO_CONTENT)

# Montar la carpeta de archivos estáticos
#Formulario_Bovino.mount("/static", StaticFiles(directory="../static/uploads"), name="static")




@Formulario_Bovino.post("/Guardar/FotoPerfil/{id_bovino}")
async def create_user_profile(id_bovino:str,file: UploadFile = File(...),
                                  db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)
                                  ):
    ConsultarNombre = db.query(modelo_bovinos_inventario).filter(
        modelo_bovinos_inventario.columns.nombre_bovino == id_bovino,
        modelo_bovinos_inventario.c.usuario_id == current_user).first()

    print(current_user)
    print(ConsultarNombre)
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

    if ConsultarNombre is None:
        raise HTTPException(status_code=404, detail="Bovino no encontrado")
    else:
        Nombre_Bovino = ConsultarNombre.nombre_bovino
        print(Nombre_Bovino)
        db.execute(modelo_bovinos_inventario.update().values(ruta_fisica_foto_perfil=file_url).where(
            modelo_bovinos_inventario.c.nombre_bovino == Nombre_Bovino,
            modelo_bovinos_inventario.c.usuario_id == current_user))
        db.commit()
        db.close()
        return {"filename": new_filename, "file_url": file_url}



