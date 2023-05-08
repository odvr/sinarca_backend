"""
@autor
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
#,
from pydantic import BaseModel
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
#from passlib.context import CryptContext

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id = str
    username = str
    hashed_password = str






class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class Esquema_bovinos(BaseModel):
    id_bovino : str
    fecha_nacimiento: date
    edad: int
    sexo :str
    raza : str
    peso: int
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
    id_leche:int
    id_bovino:str
    prod_lactancia : int
    dura_lactancia :int
    fecha_primer_parto: date
    edad_primer_parto: int
    fecha_inicial_ordeno : date
    fecha_fin_ordeno: date
    num_partos:int
    tipo_parto:str
    datos_prenez:str
    fecha_ultimo_parto: date
    fecha_ultima_prenez: date
    dias_abiertos: int
    fecha_vida_util:date
    ordeno:str
    proposito: str
    promedio_litros:int
    litros_diarios:int
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
    perdida_de_terneros: int
    tasa_supervivencia: int
    total_animales:int
    vacas_prenadas_porcentaje:int
    animales_levante:int
    animales_ceba:int
    animales_leche:int
    vacas_prenadas:int
    vacas_vacias:int
    animales_fallecidos:int
    animales_vendidos:int
    machos:int
    hembras:int
    vacas_en_ordeno:int
    vacas_no_ordeno:int
    porcentaje_ordeno:int
    animales_rango_edades_0_9:int
    animales_rango_edades_9_12:int
    animales_rango_edades_12_24:int
    animales_rango_edades_24_36:int
    animales_rango_edades_mayor_36:int
    animales_optimos_levante:int
    animales_optimos_ceba:int
    vientres_aptos:int
    relacion_toros_vientres_aptos:int
    interpretacion_relacion_toros_vientres_aptos:str
    total_unidades_animales:str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_macho_reproductor(BaseModel):
    id_macho: int
    id_bovino: str
    id_bovino_madre: str
    id_bovino_padre: str
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
    peso:int
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_veterinaria(BaseModel):
    id_veterinaria: int
    id_bovino: str
    edad: int
    peso: int
    estado: str
    sexo: str
    proposito: str
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
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_descarte(BaseModel):
    id_descarte: int
    id_bovino: str
    edad: int
    peso: float
    razon_descarte: str
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_partos(BaseModel):
    id_parto: int
    id_bovino: str
    edad: int
    peso: int
    fecha_estimada_prenez: date
    fecha_estimada_parto: date
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_carga_animal_y_consumo_agua(BaseModel):
    id_carga_animal: int
    id_bovino: str
    edad: int
    peso: int
    estado: str
    valor_unidad_animal: int
    consumo_forraje_vivo:int
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
    peso: int
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

class modelo_litros_leche(BaseModel):
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

class modelo_orden_litros(BaseModel):
    id_IEP: int
    id_bovino: str
    raza: str
    litros_promedio_raza: float
    litros_promedio_animal: float
    diferencia: float
    class Config:
        orm_mode = True
        env_file = ".env"

class modelo_orden_peso(BaseModel):
    id_peso: int
    id_bovino: str
    raza: str
    peso_promedio_raza: float
    peso_promedio_animal: float
    diferencia: float
    class Config:
        orm_mode = True
        env_file = ".env"