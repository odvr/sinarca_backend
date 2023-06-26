'''
Librerias requeridas
@autor : odvr
'''

import logging
import math
from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Response

from Lib.actualizacion_peso import actualizacion_peso

from Lib.endogamia import endogamia
from Lib.funcion_vientres_aptos import vientres_aptos
# importa la conexion de la base de datos
from config.db import condb, session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_veterinaria, modelo_leche, modelo_levante, \
    modelo_ventas, modelo_datos_muerte, \
    modelo_indicadores, modelo_ceba, modelo_macho_reproductor, modelo_carga_animal_y_consumo_agua, modelo_datos_pesaje, \
    modelo_capacidad_carga, modelo_calculadora_hectareas_pastoreo, modelo_partos, modelo_vientres_aptos, \
    modelo_descarte, modelo_users, modelo_arbol_genealogico, modelo_veterinaria_evoluciones, modelo_usuarios, MUserOut, \
    MUserAuth

from routes.Reproductor import vida_util_macho_reproductor
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_levante, \
    esquema_produccion_ceba, esquema_datos_muerte, esquema_modelo_ventas, esquema_arbol_genealogico, \
    esquema_modelo_Reporte_Pesaje, esquema_produccion_leche, esquema_veterinaria, esquema_veterinaria_evoluciones, \
    esquema_partos, esquema_macho_reproductor, esquema_indicadores, esquema_vientres_aptos, UserOut, UserAuth, Usuarios, \
    UsuariosInDB, TokenSchema, TokenPayload, TokenData
from sqlalchemy import update, between, func
from starlette.status import HTTP_204_NO_CONTENT
from datetime import date, datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import  status, HTTPException, Depends



'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError

from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from uuid import uuid4


oauth2_scheme = OAuth2PasswordBearer("/token")
'''***********'''


# Configuracion de las rutas para fash api
rutas_bovinos = APIRouter()

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

'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
#from app.schemas import UserOut, UserAuth
from uuid import uuid4



ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "1q2w3e4r"
JWT_REFRESH_SECRET_KEY = "1q2w3e4r"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt





@rutas_bovinos.post('/signup', summary="Create new user")
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    #user = session.query(MUserOut).filter_by(email=data.email).first()

    user = condb.execute(MUserOut.select().where(MUserOut.columns.email == data.email)).first()


    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    ingreso = MUserAuth.insert().values(email=data.email,
        password=get_hashed_password(data.password)
        )

    condb.execute(ingreso)
    condb.commit()

    return user




@rutas_bovinos.post('/login', summary="Create access and refresh tokens for user",response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = condb.execute(MUserAuth.select().where(MUserAuth.c.email == form_data.username)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user[2]
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="I"
        )

    return {
        "access_token": create_access_token(user[0]),
        "refresh_token": create_refresh_token(user[0]),
    }


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> MUserAuth:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #user = await UserService.get_user_by_id(token_data.sub)
    user = condb.execute(MUserAuth.select().where(MUserAuth.c.email == token_data.username)).first()
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user



'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''









""" Enviar Notificaciones 

def Notificaciones():
    account_sid = 'AC99b97a77f43fd1f944485dbad0f960a0'
    auth_token = '29f8eac6e4ad3b1369f05719fca07db3'
    #client = Client(account_sid, auth_token)
"""
"""
    message = client.messages.create(
        from_='+15075166814',
        body='Hola Este es un Mensaje Para sinarca',
        to='+573232825739'
    )

    print(message.sid)
    
    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: session = Depends(condb)):
    try:
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(email=email)
        user = condb.execute(MUserAuth.select().where(MUserAuth.c.email == token_data.username)).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserModel(id=user[0], email=user[1])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

"""

#Notificaciones()
""" 
La siguiente linea de codigo permite realizar el Login de la aplicacion 

Toma el flujo el token para pasar como parametro para cada una de las rutas 
"""








""""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""

@rutas_bovinos.get("/listar_vientres_aptos", response_model=list[esquema_vientres_aptos])
async def listar_vientres_aptos_modulo(current_user: Annotated[UserAuth, Depends(get_current_user)]):
    try:
        vientres_aptos()

        tabla_vientres_aptos = session.query(modelo_vientres_aptos).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return tabla_vientres_aptos,current_user


@rutas_bovinos.get("/listar_vientres_aptos_Rutas" )
async def listar_vientres_aptos_modulo():
    try:
        #vientres_aptos()

        tabla_vientres_aptos = session.query(modelo_vientres_aptos).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de TABLA VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()
    return tabla_vientres_aptos

"""
La siguiente funcion retorna un diccionario con la consulta general del la tabla bovinos,
 utlizando el decorador execute
"""


@rutas_bovinos.get("/listar_inventarios", response_model=list[Esquema_bovinos],tags=["listar_inventarios"]
                   )
async def inventario_bovino():
    # Se llama la funcion con el fin que esta realice el calculo pertinete a la edad del animal ingresado
    calculoEdad()
    actualizacion_peso()

    eliminarduplicados()

    vida_util_macho_reproductor()


    try:
        items = condb.execute(modelo_bovinos_inventario.select()).fetchall()


    except Exception as e:
        logger.error(f'Error al obtener inventario de bovinos: {e}')
        raise
    finally:
        condb.close()

    return items

@rutas_bovinos.get("/listar_bovino_v/{id_bovino}",status_code=200)
async def id_inventario_bovino_v(id_bovino: str):
    try:

        consulta = condb.execute(
            modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

        if not consulta:
            raise HTTPException(status_code=404, detail="El bovino no se encontró en el inventario")

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    return consulta







@rutas_bovinos.get("/listar_animales_descarte" )
async def listarAnimalesDescarte():

    try:

        itemsAnimalesDescarte = session.execute(modelo_descarte.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesDescarte



@rutas_bovinos.get("/listar_tabla_veterinaria/{id_bovino}", response_model=list[esquema_veterinaria] )
async def listar_tabla_veterinaria(id_bovino:str):

    try:

        #itemsAnimalesVeterinaria =  session.execute(modelo_veterinaria.select()).all()
        itemsAnimalesVeterinaria = session.execute(
            modelo_veterinaria.select().where(modelo_veterinaria.columns.id_bovino == id_bovino)).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE VETERINARIA: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesVeterinaria







@rutas_bovinos.get("/listar_tabla_solo_machos",response_model=list[Esquema_bovinos] )
async def listar_tabla_solo_machos():

    try:
        machos = session.query(modelo_bovinos_inventario). \
            filter(
                   modelo_bovinos_inventario.c.sexo == "Macho").all()


    except Exception as e:
        logger.error(f'Error al obtener TABLA DE SOLO MACHOS: {e}')
        raise
    finally:
        session.close()
    return machos
@rutas_bovinos.get("/listar_tabla_solo_hembras",response_model=list[Esquema_bovinos] )
async def listar_tabla_solo_hembras():

    try:
        hembras = session.query(modelo_bovinos_inventario). \
            filter( modelo_bovinos_inventario.c.sexo == "Hembra").all()
        #itemsAnimalesVeterinaria =  session.execute(modelo_veterinaria.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE SOLO Hembra: {e}')
        raise
    finally:
        session.close()
    return hembras



@rutas_bovinos.get("/listar_tabla_endogamia",response_model=list[esquema_arbol_genealogico] )
async def listar_tabla_endogamia():

    try:
        itemsAnimalesEndogamia =  session.execute(modelo_arbol_genealogico.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener TABLA DE ENDOGAMIA: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesEndogamia





@rutas_bovinos.get("/listar_contar_animales_descarte" )
async def listar_contar_AnimalesDescarte():

    try:

        #itemsAnimalesDescarte = session.execute(modelo_descarte).count()
        itemsAnimalesDescarte = session.query(modelo_descarte). \
            where(modelo_descarte.columns.id_bovino).count()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Anamales de Descarte: {e}')
        raise
    finally:
        session.close()
    return itemsAnimalesDescarte





"""
Lista los animales en Levante

"""

@rutas_bovinos.get("/listar_prod_levante",response_model=list[esquema_produccion_levante])
async def inventario_levante():
    Estado_Optimo_Levante()
    eliminarduplicados()


    try:
        itemsLevante = session.execute(modelo_levante.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        session.close()
    return itemsLevante



'''Listar animales en Ceba'''


@rutas_bovinos.get("/listar_prod_ceba",response_model=list[esquema_produccion_ceba] )
async def inventario_ceba():
    #llamdo de la funcion para calcular
    Estado_Optimo_Ceba()
    eliminarduplicados()



    try:

        itemsceba = session.execute(modelo_ceba.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Produccion Levante: {e}')
        raise
    finally:
        session.close()
    return itemsceba







"""
Lista la tabla de carga de animales
"""



"""
Listar  Fecha aproximada de parto
"""

@rutas_bovinos.get("/listar_fecha_parto",response_model=list[esquema_partos] )
async def listar_fecha_parto():

    try:
        fecha_aproximada_parto()

        listar_fecha_estimada_parto = session.execute(modelo_partos.select()).all()

    except Exception as e:
        logger.error(f'Error al obtener inventario de Fecha de Parto: {e}')
        raise
    finally:
        session.close()
    return listar_fecha_estimada_parto


"""
Listado de vientres aptos
"""
@rutas_bovinos.get("/listar_vientres_aptos" )
async def listar_vientres_aptos():
    try:
        vida_util_macho_reproductor()
        vientres_aptoss = session.query(modelo_indicadores.c.vientres_aptos).first()


    except Exception as e:
        logger.error(f'Error al obtener inventario de REPRODUCTOR: {e}')
        raise
    finally:
        session.close()
    return vientres_aptoss







"""
Listado de total_unidades_animales
"""
@rutas_bovinos.get("/total_unidades_animales" )
async def total_unidades_animales():
    try:
        total_unidades_animales = session.query(modelo_indicadores.c.total_unidades_animales).first()
    except Exception as e:
        logger.error(f'Error al obtener inventario de total_unidades_animales: {e}')
        raise
    finally:
        session.close()
    return total_unidades_animales



"""
Listado de calculadora_hectareas
"""
@rutas_bovinos.get("/consumo_global_agua" )
async def consumo_global_agua():
    try:


        consumo_global_agua = session.query(modelo_indicadores.c.consumo_global_agua).first()


    except Exception as e:
        logger.error(f'Error al obtener inventario de total_unidades_animales: {e}')
        raise
    finally:
        session.close()
    return consumo_global_agua



" relacion_toros_vientres_aptos Lista la relacion entre el toro y los vientres aptos"


@rutas_bovinos.get("/Indicadores", response_model=list[esquema_indicadores])
async def relacion_toros_vientres_aptos():
    try:
        vida_util_macho_reproductor()
        vientres_aptos()
        relacion_macho_reproductor_vientres_aptos()

        response = session.query(modelo_indicadores).all()


        return response


    except Exception as e:
        logger.error(f'Error al obtener la consulta de RELACION Y VIENTRES APTOS: {e}')
        raise
    finally:
        session.close()














"""

Lista   hectareas_forrajeget

"""


@rutas_bovinos.get("/hectareas_forraje")
async def hectareas_forraje():
    try:

        hectareas_forraje_ = session.query(
            modelo_capacidad_carga.c.hectareas_forraje).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de hectareas_forraje=  {e}')
        raise
    finally:
        session.close()
    return hectareas_forraje_


"""

Lista   hectareas_forrajeget

"""


@rutas_bovinos.get("/capacidad_animales")
async def capacidad_animales():
    try:

        capacidad_animales = session.query(
            modelo_capacidad_carga.c.capacidad_animales).first()

    except Exception as e:
        logger.error(f'Error al obtener la consulta de capacidad_animales=  {e}')
        raise
    finally:
        session.close()
    return capacidad_animales




"""
Listar la temperatura
"""

@rutas_bovinos.get("/listarTemperatura" )
async def listarTemperatura():
    try:
        listarTempAmbiente = session.query(modelo_indicadores.c.temperatura_ambiente).where(modelo_indicadores.c.id_indicadores == 1).first()
        #listarTempAmbiente = session.execute(modelo_indicadores.c.temperatura_ambiente).first()

    except Exception as e:

        logger.error(f'Error al obtener la consulta de TEMPERATURA=  {e}')
        raise
    finally:
        session.close()
    return listarTempAmbiente





"""
Lista los datos de la tabla prod levante para la opcion de editar bovino
"""

@rutas_bovinos.get("/listar_bovino_proceba/{id_bovino}")
async def id_inventario_bovino_ceba(id_bovino: str):
    eliminarduplicados()

    try:
        consulta = session.execute(
            modelo_ceba.select().where(modelo_ceba.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Ceba: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta


"""
Utilizada para listar el Arbol Genialogico de un solo Bovino
"""
@rutas_bovinos.get("/listar_bovino_Arbol_genialoco/{id_bovino}")
async def id_arbolgenialogico(id_bovino: str):

    try:
        consulta = session.execute(
            modelo_arbol_genealogico.select().where(modelo_arbol_genealogico.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al obtener Listar ID De arbol genialogico: {e}')
        raise
    finally:
        session.close()

    return consulta


"""
Lista los datos de la tabla prod leche inventario
"""








"""
Lista los datos de la tabla prod levante para la opcion de editar bovino
"""

@rutas_bovinos.get("/listar_bovino_prolevante/{id_bovino}")
async def id_inventario_bovino_levante(id_bovino: str):
    try:
        consulta = session.execute(
            modelo_levante.select().where(modelo_levante.columns.id_bovino == id_bovino)).first()
        logger.info(f'Se listo el siguiente Bovino de levante {consulta} ')
    except Exception as e:
        logger.error(f'Error al obtener Listar Produccion Leche: {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta

""""
Listar Tabla de Animales con Regristro de Muerte

"""

@rutas_bovinos.get("/listar_bovino_muerte",response_model=list[esquema_datos_muerte])
async def id_inventario_bovinos_muertos():
    try:
        # consulta y seleccion de los animales muertos
        consulta = session.query(modelo_datos_muerte). \
            filter(modelo_datos_muerte.c.estado == "Muerto").all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE MUERTE : {e}')
        raise
    finally:
        session.close()
    # condb.commit()
    return consulta




"""
Listar tabla de ventas
"""

@rutas_bovinos.get("/listar_tabla_ventas",response_model=list[esquema_modelo_ventas])
async def listar_tabla_ventas():
    try:

        consultaVentas = session.query(modelo_ventas). \
            filter(modelo_ventas.c.estado == "Vendido").all()

    except Exception as e:
        logger.error(f'Error al obtener Listar REGISTRO DE VENTAS : {e}')
        raise
    finally:
        session.close()

    return consultaVentas



"""
La siguiente funcion retorna un diccionario con la consulta de un ID del la tabla bovinos,
"""


@rutas_bovinos.get("/listar_bovino/{id_bovino}", response_model=Esquema_bovinos )
async def id_inventario_bovino(id_bovino: str):
    try:
        consulta = condb.execute(
            modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()



    except Exception as e:

        logger.error(f'Error al obtener Listar Unico Bovino del Inventario : {e}')
        raise

    # condb.commit()
    return consulta


"""
Realiza la creacion de nuevos bovinos en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""


@rutas_bovinos.post("/crear_bovino/{id_bovino}/{fecha_nacimiento}/{edad}/{raza}/{sexo}/{peso}/{marca}/{proposito}/{mansedumbre}/{estado}", status_code=status.HTTP_201_CREATED)
async def crear_bovinos(id_bovino:str,fecha_nacimiento:date,edad:int,raza:str,sexo:str,peso:float,marca:str,proposito:str,mansedumbre:str,estado:str):
    eliminarduplicados()

    vientres_aptos()

    try:
        #bovinos_dic = esquemaBovinos.dict()
        ingreso = modelo_bovinos_inventario.insert().values(  id_bovino=id_bovino,
        fecha_nacimiento=fecha_nacimiento,
        edad=edad,
        raza=raza,
        sexo=sexo,
        peso=peso,
        marca=marca,
        proposito=proposito,
        mansedumbre=mansedumbre,
        estado=estado)
        condb.execute(ingreso)

        condb.commit()
    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de inventarios: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)








"""
Crear Indice de Endogamia
"""
@rutas_bovinos.post("/calcular_indice_endogamia/{id_bovino}/{id_bovino_madre}/{id_bovino_padre}",status_code=200)
async def crear_endogamia(id_bovino:str,id_bovino_madre: str,id_bovino_padre:str ):

    try:
        ingresoEndogamia = modelo_arbol_genealogico.insert().values(id_bovino=id_bovino,
                                                     id_bovino_madre=id_bovino_madre,
                                                     id_bovino_padre=id_bovino_padre,
                                                   )


        condb.execute(ingresoEndogamia)
        condb.commit()
        endogamia()
    except Exception as e:
        logger.error(f'Error al Crear INDICE DE ENDOGAMIA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)








"""
Ingresa los datos para el reporte de VENTA para el animal





"""
@rutas_bovinos.post("/crear_venta/{id_bovino}/{estado}/{numero_bono_venta}/{fecha_venta}/{precio_venta}/{razon_venta}/{medio_pago}/{comprador}",status_code=200)
async def crear_reporte_ventas(id_bovino:str,estado:str,numero_bono_venta:str,fecha_venta:date,precio_venta:int,razon_venta:str,medio_pago:str,comprador:str ):

    try:

        consulta = condb.execute(
            modelo_ventas.select().where(
                modelo_ventas.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoVentas = modelo_ventas.insert().values(id_bovino=id_bovino, estado=estado,
                                                          numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                                                          precio_venta=precio_venta, razon_venta=razon_venta,
                                                          medio_pago=medio_pago, comprador=comprador)
            condb.execute(ingresoVentas)
            condb.commit()


        else:

            condb.execute(modelo_ventas.update().where(modelo_ventas.c.id_bovino == id_bovino).values(
                estado=estado,numero_bono_venta=numero_bono_venta, fecha_venta=fecha_venta,
                                                          precio_venta=precio_venta, razon_venta=razon_venta,
                                                          medio_pago=medio_pago, comprador=comprador))
            condb.commit()

            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE VENTA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)




"""
Ingresa los datos para el reporte de Animales Muertos

"""
@rutas_bovinos.post("/crear_registro_muerte/{id_bovino}/{estado}/{fecha_muerte}/{razon_muerte}",status_code=200)
async def crear_registro_muerte(id_bovino:str,estado:str,fecha_muerte:date,razon_muerte:str ):

    try:
        consulta = condb.execute(
            modelo_datos_muerte.select().where(
                modelo_datos_muerte.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresoRegistroMuerte = modelo_datos_muerte.insert().values(id_bovino=id_bovino, estado=estado,
                                                                        fecha_muerte=fecha_muerte,
                                                                        razon_muerte=razon_muerte)
            condb.execute(ingresoRegistroMuerte)
            condb.commit()


        else:

            condb.execute(modelo_datos_muerte.update().where(modelo_datos_muerte.c.id_bovino == id_bovino).values(
                estado=estado,razon_muerte=razon_muerte, fecha_muerte=fecha_muerte))

            condb.commit()


    except Exception as e:
        logger.error(f'Error al Crear INGRESO DE MUERTE: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)








"""
La siguiente api crea en la tabla de leche con la llave foranea de id_bovino esto es habilitado en el formulario en la opcion de porposito leche
"""








"""
Funcion Caga Animal
"""
@rutas_bovinos.post(
    "/crear_carga_animal/{id_bovino}",
    status_code=status.HTTP_201_CREATED)
async def CrearCargaAnimal(id_bovino: str):
    eliminarduplicados()

    try:
        ingresoCargaAnimal = modelo_carga_animal_y_consumo_agua.insert().values(id_bovino=id_bovino)


        condb.execute(ingresoCargaAnimal)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla CARGA ANIMAL: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)


"""
Crear en la tabla de partos para calcular la fecha aproximada
"""
@rutas_bovinos.post(
    "/crear_fecha_apoximada_parto/{id_bovino}/{fecha_estimada_prenez}",
    status_code=status.HTTP_201_CREATED)
async def CrearFechaAproximadaParto(id_bovino: str,fecha_estimada_prenez:date):
    try:
        fecha_aproximada_parto()

        consulta = condb.execute(
            modelo_partos.select().where(
                modelo_partos.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresocalcularFechaParto = modelo_partos.insert().values(id_bovino=id_bovino,
                                                                      fecha_estimada_prenez=fecha_estimada_prenez)

            condb.execute(ingresocalcularFechaParto)
            condb.commit()

        else:
            condb.execute(modelo_partos.update().where(modelo_partos.c.id_bovino == id_bovino).values(
                            fecha_estimada_prenez=fecha_estimada_prenez))
            condb.commit()





    except Exception as e:
        logger.error(f'Error al Crear ingresocalcularFechaParto: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)





"""
Funcion crear La temperatura
"""
@rutas_bovinos.post(
    "/crear_temperatura/{temperatura_ambiente}",
    status_code=status.HTTP_201_CREATED)
async def crear_temperatura(temperatura_ambiente: float):
    eliminarduplicados()

    try:
        #temperatura_ambiente_indicadores = modelo_indicadores.insert().values(temperatura_ambiente=temperatura_ambiente).where(modelo_indicadores.c.id_indicadores == 1)

        temperatura_ambiente_indicadores = update(modelo_indicadores).where(modelo_indicadores.c.id_indicadores == 1).values(temperatura_ambiente=temperatura_ambiente)
        condb.execute(temperatura_ambiente_indicadores)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de TEMPERATURA: {e}')
        raise
    finally:
        condb.close()

    return Response(status_code=status.HTTP_201_CREATED)








"""
Crear Ceba
"""
@rutas_bovinos.post(
    "/crear_prod_ceba/{id_bovino}/{proposito}",
    status_code=status.HTTP_201_CREATED)
async def CrearProdCeba(id_bovino: str,proposito:str):

    try:

        consulta = condb.execute(
            modelo_ceba.select().where(
                modelo_ceba.columns.id_bovino == id_bovino)).first()

        if consulta is None:
            ingresopceba = modelo_ceba.insert().values(id_bovino=id_bovino, proposito=proposito)
            condb.execute(ingresopceba)
            condb.commit()
        else:

            condb.execute(modelo_ceba.update().where(modelo_ceba.c.id_bovino == id_bovino).values(
                proposito=proposito))
            condb.commit()






    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de Ceba: {e}')
        raise
    finally:
        condb.close()

    return Response( status_code=status.HTTP_201_CREATED)


"""
Crear Descarte
"""
@rutas_bovinos.post(
    "/crear_descarte/{id_bovino}/{edad}/{peso}/{razon_descarte}",
    status_code=status.HTTP_201_CREATED)
async def CrearDescarte(id_bovino: str,edad:int,peso:float,razon_descarte:str):

    try:
        ingresodescarte = modelo_descarte.insert().values(id_bovino=id_bovino,edad=edad,peso=peso,razon_descarte=razon_descarte)
        logger.info(f'Se creo el siguiente Bovino en la tabla de produccion de DESCARTE {ingresodescarte} ')

        condb.execute(ingresodescarte)
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Crear Bovino para la tabla de Produccion de DESCARTE: {e}')
        raise
    finally:
        condb.close()

    return Response( status_code=status.HTTP_201_CREATED)





'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def cambiar_esta_bovino(data_update: Esquema_bovinos, id_bovino: str):
    try:
        condb.execute(modelo_bovinos_inventario.update().values(
            fecha_nacimiento=data_update.fecha_nacimiento, sexo=data_update.sexo, raza=data_update.raza,
            peso=data_update.peso, marca=data_update.marca, proposito=data_update.proposito,
            mansedumbre=data_update.mansedumbre, estado=data_update.estado).where(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        condb.execute(modelo_levante.update().values(proposito=data_update.proposito).where(
            modelo_levante.columns.id_bovino == id_bovino))
        condb.execute(modelo_ceba.update().values(proposito=data_update.proposito).where(
            modelo_ceba.columns.id_bovino == id_bovino))
        condb.execute(modelo_leche.update().values(proposito=data_update.proposito).where(
            modelo_levante.columns.id_bovino == id_bovino))
        condb.commit()

            # Retorna una consulta con el id actualizado
            #resultado_actualizado = condb.execute(
            #modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise

    finally:
        condb.close()

    return Response( status_code=status.HTTP_201_CREATED)










'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{id_bovino}/{fecha_nacimiento}/{edad}/{raza}/{sexo}/{peso}/{marca}/{proposito}/{mansedumbre}/{estado}", status_code=status.HTTP_201_CREATED)
async def cambiar_esta_bovino(id_bovino:str,fecha_nacimiento:date,edad:int,raza:str,sexo:str,peso:float,marca:str,proposito:str,mansedumbre:str,estado:str):
    try:
        condb.execute(modelo_bovinos_inventario.update().values(


            fecha_nacimiento=fecha_nacimiento,
            edad=edad,
            raza=raza,
            sexo=sexo,
            peso=peso,
            marca=marca,
            proposito=proposito,
            mansedumbre=mansedumbre,
            estado=estado

            ).where(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino))
        condb.commit()

            # Retorna una consulta con el id actualizado
            #resultado_actualizado = condb.execute(
            #modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()

    except Exception as e:
        logger.error(f'Error al Editar Bovino: {e}')
        raise

    finally:
        condb.close()

    return Response(status_code=HTTP_204_NO_CONTENT)


"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""


@rutas_bovinos.delete("/eliminar_bovino/{id_bovino}", status_code=HTTP_204_NO_CONTENT)
async def eliminar_bovino(id_bovino: str):

    try:
        condb.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bovino))
        condb.commit()

    except Exception as e:
        logger.error(f'Error al Intentar Eliminar Bovino: {e}')
        raise
    finally:
        condb.close()

    # retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)




'''
Eliminar duplicados
'''
def eliminarduplicados():
    #consulta_ceba = condb.execute(modelo_bovinos_inventario.select().
                        #where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    itemsCeba = session.execute(modelo_ceba.select()).all()


    for i in itemsCeba:
        proposito = i[5]
        id = i[0]
        if proposito == 'Leche':
            condb.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            condb.commit()
        if proposito == 'Levante':
            condb.execute(modelo_ceba.delete().where(modelo_ceba.c.id_ceba == id))
            condb.commit()
    itemsLevante = session.execute(modelo_levante.select()).all()
    for i in itemsLevante:
        proposito = i[5]
        idle = i[0]
        if proposito == 'Leche':
            condb.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            condb.commit()
        if proposito == 'Ceba':
            condb.execute(modelo_levante.delete().where(modelo_levante.c.id_levante == idle))
            condb.commit()











"""esta funcion determina la cantidad de vacas vacias (no prenadas)
esto con el  fin de mostrar cuantos vientres NO estan produciendo en el hato"""


@rutas_bovinos.get("/Calcular_vacas_vacias")
async def vacas_vacias():
    try:
        # join de tabla bovinos y tabla leche mediante id_bovino \
        # filtrado y conteo animales con datos prenez Vacia que se encuentren vivos
        consulta_vacias = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
            filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Vacia').count()
        # actualizacion del campo
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(vacas_vacias=consulta_vacias))
        logger.info(f'Funcion Consultar Vacas Vacias  {consulta_vacias} ')
        session.commit()

    except Exception as e:
        logger.error(f'Error al Calcular Vacas Vacias: {e}')
        raise
    finally:
        session.close()

    return consulta_vacias

"""
La siguiente funcion consulta la fecha de nacimiento del bovino mediante su id y
calcula la edad del animal (en meses) utilizando la fecha actual
"""

def calculoEdad():
 try:
    # Realiza la consulta general de la tabla de bovinos
    consulta_fecha_nacimiento = condb.execute(modelo_bovinos_inventario.select().
                                       where(modelo_bovinos_inventario.columns.estado=="Vivo")).fetchall()
    #Recorre los campos de la consulta
    for i in consulta_fecha_nacimiento:
        #Toma el ID del bovino para calcular la edad el campo numero 0
        id = i[0]
        # Toma la fecha de nacimiento del animal en este caso es el campo 1
        fecha_nacimiento = i[1]
        # realiza el calculo correspondiente para calcular los meses entre fechas (edad del animal)
        Edad_Animal = (datetime.today().year - fecha_nacimiento.year) * 12 + datetime.today().month - fecha_nacimiento.month
        # actualizacion del campo en la base de datos tomando la variable ID
        condb.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
            modelo_bovinos_inventario.columns.id_bovino == id ))
        logger.info(f'Funcion calculo Edad  {Edad_Animal} ')
        condb.commit()
 except Exception as e:
     logger.error(f'Error Funcion calculo Edad: {e}')
     raise
 finally:
    condb.close()



"""
"para la funcion de Duracion de lactancia se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en dias entre la fecha del ultimo ordeno
y la fecha del primer ordeno y devuelve la cantidad de dias en que se ordeno 
la vaca
"""



def Duracion_Lactancia():
  try:
    #consulta de fecha de incio de ordeno y fecha final de ordeno
    consulta_fechas = condb.execute(modelo_leche.select()).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_fechas:
        # Toma el ID del bovino para calcular la duracion de lactancia de cada animal
        id = i[1]
        # Toma la fecha de inicio de ordeno del animal en este caso es el campo 6
        fecha_inicial_ordeno = i[6]
        # Toma la fecha final de ordeno del animal en este caso es el campo 7
        fecha_fin_ordeno = i[7]
    # calculo de la duracion de la lactancia
        Duracion_Lac = (fecha_fin_ordeno.year - fecha_inicial_ordeno.year) * 360 + \
                   (fecha_fin_ordeno.month - fecha_inicial_ordeno.month) * 30
    # actualizacion del campo
        condb.execute(modelo_leche.update().values(dura_lactancia=Duracion_Lac).where(
          modelo_leche.columns.id_bovino == id))
        logger.info(f'Funcion Duracion_Lactancia {Duracion_Lac} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Duracion_Lactancia: {e}')
    raise
  finally:
      condb.close()
        #return Duracion_Lac


"""
la siguiente funcion determina si la condicion de un animal para
levante es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 140 kg y edad de 8 a 10 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""



def Estado_Optimo_Levante():
  try:
    consulta_levante = condb.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Levante")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_levante:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
        # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado=="Vivo":
          if peso >= 140 and edad in range(8, 13):
            estado_levante = "Estado Optimo"
          elif peso < 140 and edad in range(8, 13):
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos"
          elif peso < 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y menos de 8 meses de edad"
          elif peso < 140 and edad > 12:
            estado_levante = "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y mas de 12 meses de edad, considera descartarlo"
          elif peso >= 140 and edad < 8:
            estado_levante = "Estado NO Optimo, este animal tiene menos de 8 meses de edad"
          else:
            estado_levante = "Estado NO Optimo, este animal tiene una edad mayor a 12 meses, considera pasarlo a ceba"
        elif estado=="Muerto":
            estado_levante= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_levante= "Este animal esta Vendido, no se puede calcular su estado"
        #actualizacion del campo
        condb.execute(modelo_levante.update().values(edad=edad,peso=peso,estado=estado,
                      estado_optimo_levante=estado_levante).\
                      where(modelo_levante.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Levante {estado_levante} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Levante: {e}')
    raise
  finally:
      condb.close()
         #return estado_levante
"""
la siguiente funcion determina si la condicion de un animal para
ceba es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 350 kg y edad de 24 a 36 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""



def Estado_Optimo_Ceba():
  try:
    consulta_ceba = condb.execute(modelo_bovinos_inventario.select().
                        where(modelo_bovinos_inventario.columns.proposito=="Ceba")).fetchall()
    # Recorre los campos de la consulta
    for i in consulta_ceba:
        # Toma el ID del bovino para calcular su estado optimo en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[5]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
    # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
        if estado == "Vivo":
          if peso >= 350 and edad in range(24, 37):
            estado_ceba = "Estado Optimo"
          elif peso < 350 and edad in range(24, 37):
            estado_ceba = "Estado NO Optimo, este animal tiene un peso menor a 350 kilos"
          elif peso >= 350 and edad < 24:
             estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad"
          elif peso < 350 and edad < 24:
            estado_ceba = "Estado NO Optimo, este animal tiene menos de 24 meses de edad y menos de 350 kilos"
          else:
            estado_ceba = "Estado NO Optimo, este animal tiene una edad mayor a 36 meses"
        elif estado=="Muerto":
            estado_ceba= "Este animal esta Muerto, no se puede calcular su estado"
        else:
            estado_ceba= "Este animal esta Vendido, no se puede calcular su estado"
        # actualizacion del campo
    # actualizacion del campo
        condb.execute(modelo_ceba.update().values(edad=edad,peso=peso,estado=estado,
                    estado_optimo_ceba=estado_ceba). \
                  where(modelo_ceba.columns.id_bovino == id))
        logger.info(f'Funcion Estado_Optimo_Ceba {estado_ceba} ')
        condb.commit()
  except Exception as e:
    logger.error(f'Error Funcion Estado_Optimo_Ceba: {e}')
    raise
  finally:
      condb.close()
       # return estado_ceba

"""esta funcion determina el porcentaje de animales vivos que
existen en el hato,para ello utiliza la cantidad de animales vivos,
muertos y totales"""



def Tasa_Sobrevivencia():
  try:
    # consulta y seleccion de los animales vivos
    estado_vivo = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # consulta y seleccion de los animales muertos
    estado_muerto = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # total de animales(vivos + muertos)
    totales = estado_vivo + estado_muerto
    # calculo de la tasa
    tasa = (estado_vivo / totales) * 100
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(tasa_supervivencia=tasa))
    logger.info(f'Funcion Tasa_Sobrevivencia {tasa} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion Tasa_Sobrevivencia: {e}')
      raise
  finally:
      session.close()
    #return tasa

"""esta funcion calcula en terminos de porcentaje, cuantos terneros
(animales de 0 a 12 meses) han fallecido, para ello consulta la cantidad 
de animales muertos y el total para mediante una regla de 3 obtener
el porcentaje
"""


@rutas_bovinos.get("/Calcular_perdida_Terneros")
async def perdida_Terneros():
 try:
    # consulta, seleccion y conteo de animales con edad de 0 a 6 meses que se encuentren muertos
    muertos = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 12)). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # consulta, seleccion y conteo de animales con edad de 0 a 12 meses
    totales = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 12)).count()
    if muertos==0 or totales==0:
        tasa_perd=0
        # actualizacion del campo
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(perdida_de_terneros=tasa_perd))

        session.commit()
    else:
        # calculo de la tasa
        tasa_perd = (muertos / totales) * 100
        # actualizacion del campo
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(perdida_de_terneros=tasa_perd))

        session.commit()
 except Exception as e:
     logger.error(f'Error Funcion perdida_Terneros: {e}')
     raise
 finally:
     session.close()
     return tasa_perd



"""esta funcion determina la cantidad de vacas no prenadas
esto con el  fin de mostrar cuantos vientres estan produciendo en el hato"""







"""estas funciones muestra la cantidad de animales totales, tambien segun su
proposito, sexo, estado, rango de edades y estado de ordeno"""


@rutas_bovinos.get("/Calcular_animales_totales")
async def animales_totales():


  try:
    # consulta de total de animales vivos
    total_animales = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.columns.id_indicadores == 1).
                    values(total_animales=total_animales))

    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_totales: {e}')
      raise
  finally:
      session.close()
  return total_animales

@rutas_bovinos.get("/Calcular_animales_ceba")
async def animales_ceba():
  try:
    # consulta de total de animales vivos con proposito de ceba
    prop_ceba = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Ceba").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_ceba=prop_ceba))
    logger.info(f'Funcion animales_ceba {prop_ceba} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_ceba: {e}')
      raise
  finally:
      session.close()
  return prop_ceba


@rutas_bovinos.get("/Calcular_animales_levante")
async def animales_levante():
    # consulta de total de animales vivos con proposito de levante
    prop_levante = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Levante").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_levante=prop_levante))
    session.commit()
    return prop_levante







@rutas_bovinos.get("/Calcular_animales_muertos")
async def animales_muertos():
  try:
    # consulta de total de animales muertos
    estado_muerto = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_fallecidos=estado_muerto))
    logger.info(f'Funcion animales_muertos {estado_muerto} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_muertos: {e}')
      raise
  finally:
      session.close()
  return estado_muerto


@rutas_bovinos.get("/Calcular_animales_vendidos")
async def animales_vendidos():
  try:
    # consulta de total de animales vendidos
    estado_vendido = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vendido").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_vendidos=estado_vendido))
    logger.info(f'Funcion animales_vendidos {estado_vendido} ')
    session.commit()
  except Exception as e:
    logger.error(f'Error Funcion animales_vendidos: {e}')
    raise
  finally:
    session.close()
  return estado_vendido


@rutas_bovinos.get("/Calcular_animales_machos")
async def animales_sexo_macho():
  try:
    # consulta de total de animales vivos con sexo macho
    machos = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Macho").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(machos=machos))
    logger.info(f'Funcion animales_sexo_macho {machos} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_macho: {e}')
      raise
  finally:
      session.close()
  return machos


@rutas_bovinos.get("/Calcular_animales_hembras")
async def animales_sexo_hembra():
  try:
    # consulta de total de animales vivos con sexo hembra
    hembras = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(hembras=hembras))
    logger.info(f'Funcion animales_sexo_hembra {hembras} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_hembra: {e}')
      raise
  finally:
      session.close()
  return hembras


@rutas_bovinos.get("/Calcular_animales_ordeno")
async def animales_en_ordeno():
 try:
    # join, consulta y conteo de animales vivos que son ordenados
    vacas_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'Si').count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(vacas_en_ordeno=vacas_ordeno))

    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion animales_en_ordeno: {e}')
     raise
 finally:
     session.close()
 return vacas_ordeno






@rutas_bovinos.get("/Calcular_animales_edad_0_9")
async def animales_edad_0_9():
  try:
    # consulta y conteo de animales con edades entre 0 a 9 meses
    edades_0_9 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 9)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_0_9=edades_0_9))
    logger.info(f'Funcion animales_edad_0_9 {edades_0_9} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_0_9: {e}')
      raise
  finally:
      session.close()
  return edades_0_9


@rutas_bovinos.get("/Calcular_animales_edad_9_12")
async def animales_edad_9_12():
  try:
    # consulta y conteo de animales con edades entre 10 a 12 meses
    edades_9_12 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 10, 12)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_9_12=edades_9_12))
    logger.info(f'Funcion animales_edad_9_12 {edades_9_12} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_9_12: {e}')
      raise
  finally:
      session.close()
  return edades_9_12


@rutas_bovinos.get("/Calcular_animales_edad_12_24")
async def animales_edad_12_24():
 try:
    # consulta y conteo de animales con edades entre 13 a 24 meses
    edades_12_24 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 13, 24)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_12_24=edades_12_24))
    logger.info(f'Funcion animales_edad_12_24 {edades_12_24} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion animales_edad_12_24: {e}')
     raise
 finally:
     session.close()
 return edades_12_24


@rutas_bovinos.get("/Calcular_animales_edad_24_36")
async def animales_edad_24_36():
  try:
    # consulta y conteo de animales con edades entre 25 a 36 meses
    edades_24_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 25, 36)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_24_36=edades_24_36))
    logger.info(f'Funcion animales_edad_24_36 {edades_24_36} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_24_36: {e}')
      raise
  finally:
      session.close()
  return edades_24_36


@rutas_bovinos.get("/Calcular_animales_edad_mayor_36")
async def animales_edad_mayor_a_36():
  try:
    # consulta y conteo de animales con edades igual o mayor a 37 meses
    edades_mayor_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 37, 500)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_rango_edades_mayor_36=edades_mayor_36))
    logger.info(f'Funcion animales_edad_mayor_a_36 {edades_mayor_36} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_mayor_a_36: {e}')
      raise
  finally:
      session.close()
  return edades_mayor_36


@rutas_bovinos.get("/Calcular_Animales_Optimo_Levante")
async def Animales_Optimo_Levante():
 try:
    # join,consulta y conteo de animales vivos con estado optimo
    levante_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_levante.c.estado_optimo_levante). \
        join(modelo_levante, modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_levante.c.estado_optimo_levante == "Estado Optimo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_optimos_levante=levante_optimo))
    logger.info(f'Funcion Animales_Optimo_Levante {levante_optimo} ')
    session.commit()
 except Exception as e:
     logger.error(f'Error Funcion Animales_Optimo_Levante: {e}')
     raise
 finally:
     session.close()
 return levante_optimo

"la siguiente funcion"
@rutas_bovinos.get("/Calcular_Animales_Optimo_Ceba")
async def Animales_Optimo_Ceba():
  try:
    # join,consulta y conteo de animales vivos con estado optimo
    ceba_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_ceba.c.estado_optimo_ceba). \
        join(modelo_ceba, modelo_bovinos_inventario.c.id_bovino == modelo_ceba.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_ceba.c.estado_optimo_ceba == "Estado Optimo").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(animales_optimos_ceba=ceba_optimo))
    logger.info(f'Funcion Animales_Optimo_Ceba {ceba_optimo} ')
    session.commit()
  except Exception as e:
      logger.error(f'Error Funcion Animales_Optimo_Ceba: {e}')
      raise
  finally:
      session.close()
  return ceba_optimo



"""la siguiente funncion determina si la cantidad de machos reproductores es suficciente
o demasiada para las hembras que se pueden preñar """
def relacion_macho_reproductor_vientres_aptos():
  #la siguiente variable debe ser global ya que esta dentro de un bucle if anidado
  global interpretacion
  try:
    # consulta y conteo de toros reproductores vivos
    cantidad_reproductores = session.query(modelo_macho_reproductor). \
        where(modelo_macho_reproductor.columns.estado == "Vivo").count()
    # consulta y conteo de vientres aptos vivos
    cantidad_vientres_aptos = session.query(modelo_vientres_aptos).\
        where(modelo_vientres_aptos.columns.id_bovino).count()
    if cantidad_vientres_aptos==0 or cantidad_vientres_aptos is None:
        relacion =0
        interpretacion= f'No posees ninguna hembra apta para reproducirse'
        # actualizacion de campo de cantidad de vientres aptos
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(vientres_aptos=cantidad_vientres_aptos,
                               relacion_toros_vientres_aptos=relacion,
                               interpretacion_relacion_toros_vientres_aptos=interpretacion))
    else:
        # calculo de la relacion toros-vientres
        relacion = (cantidad_reproductores / cantidad_vientres_aptos) * 100
        # caclulo de cantidad recomendada de reproductores para la cantidad de vientres aptos
        cantidad_recomendada = math.ceil(cantidad_vientres_aptos / 25)
        # interpretacion del calculo de la relacion toros-vientres
        if relacion < 4:
            interpretacion = f'no Tienes suficientes machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
        elif relacion > 4:
            if cantidad_reproductores == 1 and cantidad_vientres_aptos <= 25:
                interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} macho reproductor para tus {cantidad_vientres_aptos} hembras aptas'
            elif cantidad_reproductores > 1 and cantidad_vientres_aptos <= 25:
                interpretacion = f'Tienes demasiados machos reproductores, debes tener solamente un macho reproductor para tus {cantidad_vientres_aptos} hembras aptas '
            else:
                interpretacion = f'Tienes demasiados machos reproductores, debes tener {cantidad_recomendada} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas '
        elif relacion == 4:
            interpretacion = f'Tienes la cantidad correcta de reproductores, tienes {cantidad_reproductores} machos reproductores para tus {cantidad_vientres_aptos} hembras aptas'
        # actualizacion de campo de cantidad de vientres aptos
        session.execute(update(modelo_indicadores).
                        where(modelo_indicadores.c.id_indicadores == 1).
                        values(vientres_aptos=cantidad_vientres_aptos,
                               relacion_toros_vientres_aptos=relacion,
                               interpretacion_relacion_toros_vientres_aptos=interpretacion))
        logger.info(f'Funcion relacion_macho_reproductor_vientres_aptos {cantidad_vientres_aptos, relacion, interpretacion} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion relacion_macho_reproductor_vientres_aptos: {e}')
      raise
  finally:
      session.close()
  return (relacion, interpretacion, cantidad_vientres_aptos)

"""funcion de capacidad de carga"""
def capacidad_carga0():
  try:
    # consulta hectareas de forraje vivo disponible en el predio
    consulta_hectareas = session.query(modelo_capacidad_carga.columns.hectareas_forraje). \
          where(modelo_capacidad_carga.c.id_capacidad == 1).all()
    for i in consulta_hectareas:
        # Toma las hectareas de pasto en este caso es el campo 0
        hectareas = i[0]
        #determinacion de produccion de pasto por hectarea
        #conversion de hectareas a metros cuadrados
        metros=hectareas*10000
        #los pastos tropicales producen un aproximado de 0.003 kilogramos de materia seca por metro cuadrado al dia
        produccion_materia_seca=0.003*metros
        #determinacion de la cantidad de unidades animales que esta produccion puede mantener al dia
        #una unidad animal puede consumir hasta 16 kilos de materia seca al dia
        capacidad_unidades_animales_dia=round((produccion_materia_seca/16),2)
        interpertacion_capacidad=f'con tus hectareas de pasto, puedes mantener hasta {capacidad_unidades_animales_dia} unidades animales'
        #actualizacion de campos
        session.execute(modelo_capacidad_carga.update().values(produccion_materia_seca=produccion_materia_seca,
                                                               capacidad_animales=interpertacion_capacidad). \
                        where(modelo_capacidad_carga.columns.id_capacidad == 1))
        logger.info(f'Funcion capacidad_carga {interpertacion_capacidad} ')
        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion capacidad_carga: {e}')
      raise
  finally:
      session.close()


"""la siguiente funcion es una calculadora que determina la fecha aproximada de parto
de un animal en base a su fecha de preñez"""
def fecha_aproximada_parto():
  try:
    # join de tablas


    consulta_vacas = session.query(modelo_partos.c.id_bovino,modelo_partos.c.fecha_estimada_prenez, modelo_bovinos_inventario.c.edad,
                                     modelo_bovinos_inventario.c.peso, modelo_bovinos_inventario.c.estado). \
        join(modelo_partos,modelo_partos.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    #recorrer los campos
    for i in consulta_vacas:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 1
        fecha_estimada_prenez = i[1]
        # Toma la edad del animal en este caso es el campo 1
        edad = i[2]
        # Toma el peso del animal en este caso es el campo 2
        peso = i[3]
        # Toma el estado del animal en este caso es el campo 3
        estado = i[4]
        #calculo de la fecha aproximada de parto (la gestacion dura paorximadamente 280 dias)
        if estado=="Vivo":
          fecha_estimada_parto = fecha_estimada_prenez + timedelta(280)
        else:
          fecha_estimada_parto = None
        #actualizacion de campos
        session.execute(modelo_partos.update().values(fecha_estimada_parto=fecha_estimada_parto,edad=edad,
                                                      peso=peso). \
                        where(modelo_partos.columns.id_bovino == id))

        session.commit()
  except Exception as e:
      logger.error(f'Error Funcion fecha_aproximada_parto: {e}')
      raise
  finally:
      session.close()


"""la siguiente funcion trae los campos de edad y peso de cada animal
a los animales de descarte"""
def descarte():
  try:
      # join de tablas
    consulta_animales = session.query(modelo_descarte.c.id_bovino, modelo_bovinos_inventario.c.edad,
                            modelo_bovinos_inventario.c.peso).\
        join(modelo_descarte, modelo_descarte.c.id_bovino == modelo_bovinos_inventario.c.id_bovino).all()
    for i in consulta_animales:
        # Toma el ID del bovino en este caso es el campo 0
        id = i[0]
        # Toma la edad del animal en este caso es el campo 2
        edad = i[1]
        # Toma el peso del animal en este caso es el campo 5
        peso = i[2]
        # actualizacion de campos
        session.execute(modelo_descarte.update().values( edad=edad,
                                                      peso=peso). \
                        where(modelo_descarte.columns.id_bovino == id))
        logger.info(f'Funcion descarte {peso} ')
        session.commit()
  except Exception as e:
     logger.error(f'Error Funcion descarte: {e}')
     raise
  finally:
     session.close()

#actualizacion_peso()
#vientres_aptos()
#intervalo_partos()
#promedio_intervalo_partos()
#promedio_litros_leche()
#IEP_por_raza()
#litros_por_raza()
#peso_segun_raza()
