"""
@autor
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
#,
from pydantic import BaseModel
from datetime import date
from typing import Optional,Union
from uuid import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
#from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id = str
    username = str
    hashed_password = str

class Usuarios(BaseModel):
    id_usuario : str
    full_name : Union[str,None]=None
    hashed_password: str


class UsuariosInDB(Usuarios):
     hashed_password:str


class TokenData(BaseModel):
    email:str

    class Config:
        orm_mode = True
        env_file = ".env"
class UserAuth(BaseModel):
    email:str
    username: str
    password: str

    class Config:
        orm_mode = True
        env_file = ".env"


class UserOut(BaseModel):
    user_id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    class Config:
        orm_mode = True
        env_file = ".env"


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True
        env_file = ".env"


class TokenPayload(BaseModel):
    sub: UUID = None
    exp: int = None

    class Config:
        orm_mode = True
        env_file = ".env"

class Esquema_bovinos(BaseModel):
    id_bovino : str
    fecha_nacimiento: date
    edad: int
    sexo :str
    raza : str
    peso: float
    marca :str
    proposito: str
    mansedumbre : str
    estado: str





    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_produccion_ceba(BaseModel):
    id_ceba:int
    proposito: str
    id_bovino : str
    edad: int
    peso: int
    estado: str
    estado_optimo_ceba:str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_levante(BaseModel):
    id_levante:int
    id_bovino:str
    edad: int
    peso: int
    estado: str
    proposito: str
    estado_optimo_levante : str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_leche(BaseModel):
    id_leche: int
    id_bovino: str
    fecha_primer_parto: Optional[date] = None
    edad_primer_parto: Optional[int] = None
    datos_prenez: Optional[str] = None
    fecha_vida_util: Optional[date] = None
    ordeno: Optional[str] = None
    proposito: Optional[str] = None
    promedio_litros : Optional[float] = None
    num_partos: Optional[int] = None
    intervalo_entre_partos : Optional[float] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_datos_muerte(BaseModel):
    id_datos_muerte: int
    id_bovino: str
    estado: str
    razon_muerte:str
    fecha_muerte:date
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_arbol_genealogico(BaseModel):
    id_arbol_genealogico: int
    id_bovino: str
    id_bovino_madre: str
    id_bovino_padre: str
    abuelo_paterno:str
    abuela_paterna:str
    abuelo_materno:str
    abuela_materna:str
    bisabuelo_materno:str
    bisabuelo_paterno:str
    tipo_de_apareamiento:str
    consanguinidad:float
    notificacion:str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_indicadores(BaseModel):
    id_indicadores: int
    perdida_de_terneros: Optional[float] = None
    tasa_supervivencia: Optional[float] = None
    total_animales:Optional[int] = None
    vacas_prenadas_porcentaje:Optional[float] = None
    animales_levante:Optional[int] = None
    animales_ceba:Optional[int] = None
    animales_leche:Optional[int] = None
    vacas_prenadas:Optional[int] = None
    vacas_vacias:Optional[int] = None
    animales_fallecidos:Optional[int] = None
    animales_vendidos:Optional[int] = None
    machos:Optional[int] = None
    hembras:Optional[int] = None
    vacas_en_ordeno:Optional[int] = None
    vacas_no_ordeno:Optional[int] = None
    porcentaje_ordeno:Optional[float] = None
    animales_rango_edades_0_9:Optional[int] = None
    animales_rango_edades_9_12:Optional[int] = None
    animales_rango_edades_12_24:Optional[int] = None
    animales_rango_edades_24_36:Optional[int] = None
    animales_rango_edades_mayor_36:Optional[int] = None
    animales_optimos_levante:Optional[int] = None
    animales_optimos_ceba:Optional[int] = None
    vientres_aptos:Optional[int] = None
    relacion_toros_vientres_aptos:Optional[int]
    interpretacion_relacion_toros_vientres_aptos:Optional[str]
    total_unidades_animales:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_macho_reproductor(BaseModel):
    id_macho: int
    id_bovino: str
    edad: int
    peso: int
    estado: str
    fecha_vida_util: date
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_modelo_ventas(BaseModel):
    id_venta: int
    id_bovino: str
    numero_bono_venta: str
    estado: str
    fecha_venta: date
    precio_venta:int
    razon_venta:str
    medio_pago: str
    comprador: str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_modelo_Reporte_Pesaje(BaseModel):
    id_pesaje: int
    id_bovino: str
    fecha_pesaje: date
    peso:float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_veterinaria(BaseModel):
    id_veterinaria: int
    id_bovino: str
    sintomas: str
    fecha_sintomas: date
    comportamiento:str
    condicion_corporal: str
    postura: str
    mucosa_ocular: str
    mucosa_bucal: str
    mucosa_rectal: str
    mucosa_vulvar_prepusial: str
    tratamiento: str
    evolucion: str
    piel_pelaje:str
    class Config:
        orm_mode = True
        env_file = ".env"





class esquema_veterinaria_evoluciones(BaseModel):
    id_evolucion: int
    id_bovino: str
    tratamiento_evolucion: str
    fecha_evolucion: date
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_veterinaria_comentarios(BaseModel):
    id_comentario: int
    id_veterinaria: int
    comentarios: str
    fecha_comentario: date
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_descarte(BaseModel):
    id_descarte: int
    id_bovino: str
    edad:Optional[int] = None
    peso:Optional[float] = None
    razon_descarte: str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_partos(BaseModel):
    id_parto: int
    id_bovino: str
    edad: int
    peso: int
    fecha_estimada_prenez: Optional[date] = None
    fecha_estimada_parto: Optional[date] = None


    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_carga_animal_y_consumo_agua(BaseModel):
    id_carga_animal: int
    id_bovino: str
    edad: int
    peso: int
    valor_unidad_animal: float
    consumo_forraje_vivo:float
    raza:str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_capacidad_carga(BaseModel):
    id_capacidad: int
    medicion_aforo: float
    hectareas_predio: float
    tipo_de_muestra: str
    carga_animal_recomendada: float
    capacidad_carga: str
    carga_animal_usuario: float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_calculadora_hectareas_pastoreo(BaseModel):
    id_pastoreo: int
    id_bovino: str
    hectareas_necesarias: int
    consumo_agua: int
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_vientres_aptos(BaseModel):
    id_vientre: int
    id_bovino: str
    edad: int
    peso: float
    raza:str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_partos(BaseModel):
    id_parto: int
    id_bovino: str
    fecha_parto: date
    tipo_parto: str
    id_bovino_hijo:str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_intervalo_partos(BaseModel):
    id_intervalo: int
    id_bovino: str
    fecha_parto1: date
    fecha_parto2: date
    intervalo:float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_litros_leche(BaseModel):
    id_litros: int
    id_bovino: str
    fecha_medicion: date
    litros_leche:float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_IEP(BaseModel):
    id_IEP: int
    id_bovino: str
    raza: str
    intervalo_promedio_raza: float
    intervalo_promedio_animal: float
    diferencia: float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_litros(BaseModel):
    id_litros_leche: int
    id_bovino: str
    raza: str
    litros_promedio_raza: float
    litros_promedio_animal: float
    diferencia: float
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_peso(BaseModel):
    id_peso: int
    id_bovino: str
    raza: str
    peso_promedio_raza: float
    peso_promedio_animal: float
    diferencia: float
    class Config:
        orm_mode = True
        env_file = ".env"