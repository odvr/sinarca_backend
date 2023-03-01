"""
@autor
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
#,
from pydantic import BaseModel
from datetime import date

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
    id_bovino : int
    estado_optimo_ceba:str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_levante(BaseModel):
    id_levante : int
    id_bovino :int
    estado_optimo_levante : str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_leche(BaseModel):
    id_leche:int
    id_bovino:str
    prod_lactancia : int
    dura_lactancia :int
    id_proposito:int
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
    promedio_litros:int
    litros_diarios:int
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_datos_muerte(BaseModel):
    id_datos_muerte: int
    id_bovino: str
    razon_muerte:str
    fecha_muerte:date
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_arbol_genialogico(BaseModel):
    id_arbol_genialogico: int
    id_bovino: str
    id_bovino_madre: str
    id_bovino_padre: str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_indicadores(BaseModel):
    id_indicadores: int
    perdida_de_terneros: int
    tasa_supervivencia: int
    total_animales:int
    vacas_vacias:int
    vacas_prenadas:int
    animales_levante:int
    animales_ceba:int
    animales_leche:int
    animales_fallecidos:int
    animales_vendidos:int
    machos:int
    hembras:int
    vacas_en_ordeno:int
    porcentaje_ordeno:int
    animales_rango_edades_0_9:int
    animales_rango_edades_9_12:int
    animales_rango_edades_12_24:int
    animales_rango_edades_24_36:int
    animales_rango_edades_mayor_36:int
    animales_optimos_levante:int
    animales_optimos_ceba:int
    class Config:
        orm_mode = True
        env_file = ".env"