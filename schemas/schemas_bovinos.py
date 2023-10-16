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

class Esquema_Usuario(BaseModel):
    id_usuario : int
    usuario_id :str
    hashed_password: str

    class Config:
        orm_mode = True
        env_file = ".env"
class Esquema_Token(BaseModel):
    access_token: str
    token_type: str
    class Config:
        orm_mode = True
        env_file = ".env"



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
    id_bovino : int
    fecha_nacimiento: date
    edad: Optional[int] = None
    sexo :str
    raza : str
    peso: Optional[float] = None
    marca :str
    proposito: str
    mansedumbre : str
    estado: str
    compra_bovino: Optional[str] = None
    usuario_id:Optional[str] = None
    nombre_bovino:Optional[str] = None
    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_produccion_ceba(BaseModel):
    id_ceba: int
    proposito: Optional[str] = None
    id_bovino : Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[int] = None
    estado: Optional[str] = None
    estado_optimo_ceba: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_levante(BaseModel):
    id_levante:int
    id_bovino:int
    edad: int
    peso: int
    estado: str
    proposito: str
    estado_optimo_levante : str
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_leche(BaseModel):
    id_leche: int
    id_bovino: int
    fecha_primer_parto: Optional[date] = None
    edad_primer_parto: Optional[int] = None
    datos_prenez: Optional[str] = None
    fecha_vida_util: Optional[date] = None
    ordeno: Optional[str] = None
    proposito: Optional[str] = None
    promedio_litros : Optional[float] = None
    num_partos: Optional[int] = None
    intervalo_entre_partos : Optional[float] = None
    tipo_ganado: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_datos_muerte(BaseModel):
    id_datos_muerte: int
    id_bovino: int
    estado: Optional[str] = None
    razon_muerte: Optional[str] = None
    fecha_muerte: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_arbol_genealogico(BaseModel):
    id_arbol_genealogico: int
    id_bovino: int
    id_bovino_madre: int
    id_bovino_padre: int
    abuelo_paterno:Optional[int] = None
    abuela_paterna:Optional[int] = None
    abuelo_materno:Optional[int] = None
    abuela_materna:Optional[int] = None
    bisabuelo_materno:Optional[int] = None
    bisabuelo_paterno:Optional[int] = None
    tipo_de_apareamiento:Optional[str] = None
    consanguinidad:Optional[float] = None
    notificacion:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    nombre_bovino_madre:Optional[str] = None
    nombre_bovino_padre:Optional[str] = None
    nombre_bovino_abuelo_paterno:Optional[str] = None
    nombre_bovino_abuela_paterna:Optional[str] = None
    nombre_bovino_abuelo_materno:Optional[str] = None
    nombre_bovino_abuela_materna:Optional[str] = None
    nombre_bovino_bisabuelo_materno:Optional[str] = None
    nombre_bovino_bisabuelo_paterno:Optional[str] = None

    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_indicadores(BaseModel):
    id_indicadores: str
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
    IEP_hato:Optional[float] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_macho_reproductor(BaseModel):
    id_macho: int
    id_bovino: int
    edad: int
    peso: int
    estado: str
    fecha_vida_util: date
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_modelo_ventas(BaseModel):
    id_venta: int
    id_bovino: Optional[int] = None
    numero_bono_venta: Optional[str] = None
    estado: Optional[str] = None
    fecha_venta: Optional[date] = None
    precio_venta: Optional[int] = None
    razon_venta: Optional[str] = None
    medio_pago: Optional[str] = None
    comprador: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_modelo_compra(BaseModel):
    id_compra_bovino: int
    id_bovino: int
    numero_bono_compra: Optional[str] = None
    estado: Optional[str] = None
    fecha_compra: Optional[date] = None
    precio_compra: Optional[int] = None
    razon_compra: Optional[str] = None
    medio_pago_compra: Optional[str] = None
    comprador: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_modelo_Reporte_Pesaje(BaseModel):
    id_pesaje: int
    id_bovino: int
    fecha_pesaje: date
    peso:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_veterinaria(BaseModel):
    id_veterinaria:int
    id_bovino:Optional[int] = None
    sintomas:Optional[str] = None
    fecha_sintomas:Optional[date] = None
    comportamiento:Optional[str] = None
    condicion_corporal:Optional[str] = None
    postura:Optional[str] = None
    mucosa_ocular:Optional[str] = None
    mucosa_bucal:Optional[str] = None
    mucosa_rectal:Optional[str] = None
    mucosa_vulvar_prepusial:Optional[str] = None
    tratamiento:Optional[str] = None
    evolucion:Optional[str] = None
    piel_pelaje:Optional[str] = None
    estado_Historia_clinica:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"





class esquema_veterinaria_evoluciones(BaseModel):
    id_evolucion: int
    id_bovino: int
    tratamiento_evolucion:Optional[str] = None
    fecha_evolucion: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_registro_vacunas_bovinos(BaseModel):
    id_vacunacion_bovinos: int
    id_bovino: int
    fecha_registrada_usuario:Optional[date] = None
    tipo_vacuna: Optional[str] = None
    fecha_bitacora_Sistema: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_veterinaria_comentarios(BaseModel):
    id_comentario: int
    id_veterinaria: int
    comentarios:Optional[str] = None
    fecha_comentario: date
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"



class esquema_descarte(BaseModel):
    id_descarte: int
    id_bovino: int
    edad:Optional[int] = None
    peso:Optional[float] = None
    razon_descarte:Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_partos(BaseModel):
    id_parto: int
    id_bovino: int
    edad: Optional[int] = None
    peso: Optional[int] = None
    fecha_estimada_prenez: Optional[date] = None
    fecha_estimada_parto: Optional[date] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None


    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_carga_animal_y_consumo_agua(BaseModel):
    id_carga_animal: int
    id_bovino: Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[int] = None
    valor_unidad_animal: float
    consumo_forraje_vivo:float
    raza: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_capacidad_carga(BaseModel):
    id_capacidad: str
    medicion_aforo: float
    hectareas_predio: float
    tipo_de_muestra: str
    carga_animal_recomendada: float
    capacidad_carga: str
    carga_animal_usuario: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_calculadora_hectareas_pastoreo(BaseModel):
    id_pastoreo: int
    id_bovino: int
    hectareas_necesarias: int
    consumo_agua: int
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_vientres_aptos(BaseModel):
    id_vientre: int
    id_bovino: Optional[int] = None
    edad: Optional[int] = None
    peso: Optional[float] = None
    raza: Optional[str] = None
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_partos(BaseModel):
    id_parto: int
    id_bovino: int
    fecha_parto: Optional[date] = None
    tipo_parto: str
    id_bovino_hijo:int
    usuario_id: Optional[str] = None
    nombre_madre:Optional[str] = None
    nombre_hijo: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_intervalo_partos(BaseModel):
    id_intervalo: int
    id_bovino: int
    fecha_parto1: date
    fecha_parto2: date
    intervalo:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_litros_leche(BaseModel):
    id_litros: int
    id_bovino: int
    fecha_medicion: date
    litros_leche:float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_reporte_curva_lactancia_General(BaseModel):
    id_curva_lactancia_general: int
    id_bovino:int
    anio: str
    mes: str
    promedio:float
    Hora_Reporte:date
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_IEP(BaseModel):
    id_IEP: int
    id_bovino: int
    raza: str
    intervalo_promedio_raza: float
    intervalo_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_litros(BaseModel):
    id_litros_leche: int
    id_bovino: int
    raza: str
    litros_promedio_raza: float
    litros_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_orden_peso(BaseModel):
    id_peso: int
    id_bovino: int
    raza: str
    peso_promedio_raza: float
    peso_promedio_animal: float
    diferencia: float
    usuario_id: Optional[str] = None
    nombre_bovino:Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_perdida_terneros(BaseModel):
    id_perdida: int
    periodo: int
    perdida:float
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_historial_supervivencia(BaseModel):
    id_supervivencia: int
    periodo: int
    supervivencia:float
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_registro_pajillas(BaseModel):
    id_pajillas: int
    Codigo_toro_pajilla: Optional[str] = None
    raza: Optional[str] = None
    nombre_toro: Optional[str] = None
    productor: Optional[str] = None
    usuario_id: Optional[str] = None
    class Config:
        orm_mode = True
        env_file = ".env"