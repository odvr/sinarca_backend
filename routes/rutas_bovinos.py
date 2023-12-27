'''
Librerias requeridas
@autor : odvr
'''

import logging
import crud
from http.client import HTTPException
from sqlalchemy import and_
from fastapi import APIRouter, Request

from Lib.Tasa_Supervivencia import tasa_supervivencia
from Lib.perdida_Terneros import perdida_Terneros1
from config.db import   get_session
from crud.crud_bovinos_inventario import CRUDBovinos
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_usuarios, modelo_bovinos_inventario, modelo_indicadores
from sqlalchemy.orm import Session

from schemas.schemas_bovinos import Esquema_Token, Esquema_Usuario, esquema_indicadores

'''***********'''
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from jose import  JWTError

from fastapi import  Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer("token")
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

from datetime import datetime, timedelta

from jose import jwt

from fastapi import FastAPI, status, HTTPException
from sqlalchemy import update,between



'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


# Configuración
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = "1q2w3e4r"

# Crear un contexto de contraseña para hashing
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2PasswordBearer para obtener el token de autorización desde el encabezado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# Función para generar un token de acceso
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
# Ruta para autenticación y emisión de tokens
@rutas_bovinos.post('/token', summary="Create access and refresh tokens for user",response_model=Esquema_Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database_session)):
    user = db.execute(modelo_usuarios.select().where(modelo_usuarios.c.usuario_id == form_data.username)).first()
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    # Almacena el token en la variable de sesión del backend (en este ejemplo, estamos usando FastAPI Session)

    return {"access_token": access_token, "token_type": "bearer"}



# Función para obtener el usuario actual desde el token de autorización
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_database_session)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        logger.error(f'Error Get_current_user ')
        raise credentials_exception
    user = db.query(modelo_usuarios).filter_by(usuario_id=username).first()

    if user is None:
        raise credentials_exception
    return user[1]
def get_token_from_session(request: Request):
    return request.session.get("access_token")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

@rutas_bovinos.post('/Registrar', summary="Create new user",)
async def create_user(data: Esquema_Usuario,db: Session = Depends(get_database_session)):
    user = db.execute(modelo_usuarios.select().where(modelo_usuarios.columns.usuario_id == data.usuario_id)).first()
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    ingreso = modelo_usuarios.insert().values(usuario_id=data.usuario_id,
        hashed_password=get_hashed_password(data.hashed_password)
        )
    # Crea el registro en el Indicador del usuario
    CrearIndicadores = crud.crear_indicadores.Crear_indicadores_db(db=db, current_user=data.usuario_id)
    # Crea el registro en el Capacidad de carga
    CrearIndicadoresCapacidadCarga = crud.crear_indicadores.Crear_indicadores_capacidad_carga(db=db, current_user=data.usuario_id)


    db.execute(ingreso)
    db.execute(CrearIndicadores)
    db.execute(CrearIndicadoresCapacidadCarga)
    db.commit()

    return user

'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''


@rutas_bovinos.get("/Calcular_animales_levante",tags=["dashboard"])
async def animales_levante(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta de total de animales vivos con propósito de levante
        prop_levante = db.query(modelo_bovinos_inventario). \
            filter(modelo_bovinos_inventario.c.estado == "Vivo",
                   modelo_bovinos_inventario.c.proposito == "Levante",modelo_bovinos_inventario.c.usuario_id == current_user).count()
        # actualización de campos
        db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_levante=prop_levante))
        db.commit()
        db.close()
        return prop_levante
    except Exception as e:
        logger.error(f'Error en la función animales_levante: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()

@rutas_bovinos.get("/Calcular_animales_ceba",tags=["dashboard"])
async def animales_ceba(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:

    # consulta de total de animales vivos con proposito de ceba
    prop_ceba = db.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Ceba",modelo_bovinos_inventario.c.usuario_id == current_user).count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_ceba=prop_ceba))
    logger.info(f'Funcion animales_ceba {prop_ceba} ')
    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_ceba: {e}')
      raise
  finally:
      db.close()
  return prop_ceba


@rutas_bovinos.get("/Calcular_animales_edad_0_9",tags=["dashboard"])
async def animales_edad_0_9(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta y conteo de animales con edades entre 0 a 9 meses
    edades_0_9 = db.query(modelo_bovinos_inventario). \
        where(and_(
        between(modelo_bovinos_inventario.columns.edad, 0, 9),
        modelo_bovinos_inventario.c.estado == "Vivo",
        modelo_bovinos_inventario.c.usuario_id == current_user
    )).count()

    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_rango_edades_0_9=edades_0_9))

    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_0_9: {e}')
      raise
  finally:
      db.close()
  return edades_0_9


@rutas_bovinos.get("/Calcular_animales_edad_9_12",tags=["dashboard"])
async def animales_edad_9_12(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta y conteo de animales con edades entre 10 a 12 meses
    edades_9_12 = db.query(modelo_bovinos_inventario). \
        where(and_(
        between(modelo_bovinos_inventario.columns.edad, 10, 12),
        modelo_bovinos_inventario.c.estado == "Vivo",
        modelo_bovinos_inventario.c.usuario_id == current_user
    )).count()

    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_rango_edades_9_12=edades_9_12))
    logger.info(f'Funcion animales_edad_9_12 {edades_9_12} ')
    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_9_12: {e}')
      raise
  finally:
      db.close()
  return edades_9_12


@rutas_bovinos.get("/Calcular_animales_edad_12_24",tags=["dashboard"])
async def animales_edad_12_24(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
 try:
    # consulta y conteo de animales con edades entre 13 a 24 meses
    edades_12_24 = db.query(modelo_bovinos_inventario). \
        where(and_(
        between(modelo_bovinos_inventario.columns.edad, 13, 24),
        modelo_bovinos_inventario.c.estado == "Vivo",
        modelo_bovinos_inventario.c.usuario_id == current_user
    )).count()

    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_rango_edades_12_24=edades_12_24))
    logger.info(f'Funcion animales_edad_12_24 {edades_12_24} ')
    db.commit()
    db.close()
 except Exception as e:
     logger.error(f'Error Funcion animales_edad_12_24: {e}')
     raise
 finally:
     db.close()
 return edades_12_24


@rutas_bovinos.get("/Calcular_animales_edad_24_36",tags=["dashboard"])
async def animales_edad_24_36(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta y conteo de animales con edades entre 25 a 36 meses
        edades_24_36 = db.query(modelo_bovinos_inventario). \
            where(and_(
            between(modelo_bovinos_inventario.columns.edad, 25, 36),
            modelo_bovinos_inventario.c.estado == "Vivo",
            modelo_bovinos_inventario.c.usuario_id == current_user
        )).count()

        # actualización de campos
        db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_rango_edades_24_36=edades_24_36))
        logger.info(f'Función animales_edad_24_36 {edades_24_36} ')
        db.commit()
        return edades_24_36
    except Exception as e:
        logger.error(f'Error en la función animales_edad_24_36: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@rutas_bovinos.get("/Calcular_animales_edad_mayor_36",tags=["dashboard"])
async def animales_edad_mayor_a_36(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta y conteo de animales con edades igual o mayor a 37 meses
    edades_mayor_36 = db.query(modelo_bovinos_inventario). \
        where(and_(
        between(modelo_bovinos_inventario.columns.edad, 37, 500),
        modelo_bovinos_inventario.c.estado == "Vivo",
        modelo_bovinos_inventario.c.usuario_id == current_user
    )).count()

    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_rango_edades_mayor_36=edades_mayor_36))
    logger.info(f'Funcion animales_edad_mayor_a_36 {edades_mayor_36} ')
    db.commit()
  except Exception as e:
      logger.error(f'Error Funcion animales_edad_mayor_a_36: {e}')
      raise
  finally:
      db.close()
  return edades_mayor_36

@rutas_bovinos.get("/Calcular_animales_machos",tags=["dashboard"])
async def animales_sexo_macho(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de total de animales vivos con sexo macho
    machos = db.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Macho",modelo_bovinos_inventario.c.usuario_id == current_user).count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(machos=machos))
    logger.info(f'Funcion animales_sexo_macho {machos} ')
    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_macho: {e}')
      raise
  finally:
      db.close()
  return machos

@rutas_bovinos.get("/Calcular_animales_hembras",tags=["dashboard"])
async def animales_sexo_hembra(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de total de animales vivos con sexo hembra
    hembras = db.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra",modelo_bovinos_inventario.c.usuario_id == current_user).count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(hembras=hembras))
    logger.info(f'Funcion animales_sexo_hembra {hembras} ')
    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_sexo_hembra: {e}')
      raise
  finally:
      db.close()
  return hembras

@rutas_bovinos.get("/Calcular_animales_vendidos",tags=["dashboard"])
async def animales_vendidos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # consulta de total de animales vendidos
        estado_vendido = db.query(modelo_bovinos_inventario).filter(modelo_bovinos_inventario.c.estado == "Vendido",modelo_bovinos_inventario.c.usuario_id == current_user).count()
        # actualización de campos
        db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_vendidos=estado_vendido))

        db.commit()
        db.close()
        return estado_vendido
    except Exception as e:
        logger.error(f'Error en la función animales_vendidos: {e}')
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        db.close()


@rutas_bovinos.get("/Calcular_animales_muertos",tags=["dashboard"])
async def animales_muertos(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
  try:
    # consulta de total de animales muertos
    estado_muerto = db.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto",modelo_bovinos_inventario.c.usuario_id == current_user).count()
    # actualizacion de campos
    db.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == current_user).
                    values(animales_fallecidos=estado_muerto))

    db.commit()
    db.close()
  except Exception as e:
      logger.error(f'Error Funcion animales_muertos: {e}')
      raise
  finally:
      db.close()
  return estado_muerto

@rutas_bovinos.get("/Calcular_perdida_Terneros")
async def perdida_TernerosAPI(db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
 try:
    perdida_Terneros1(db=db,current_user=current_user)
    tasa_supervivencia(session=db,current_user=current_user)
    response= db.query(modelo_indicadores). \
        filter(
        modelo_indicadores.c.id_indicadores == current_user, modelo_indicadores.c.perdida_de_terneros).first()


    if response:
        Perdida_Terneros = response.perdida_de_terneros
        return Perdida_Terneros
    else:
        return {"message": "No se encontraron resultados"}


        #return response

 except Exception as e:
     logger.error(f'Error Funcion perdida_Terneros: {e}')
     raise
 finally:
     db.close()
