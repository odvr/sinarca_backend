"""
@autor
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
from pydantic import BaseModel
from datetime import date

class Esquema_bovinos(BaseModel):
    id_bovino : int
    fecha_nacimiento: date
    edad: int
    sexo_id :int
    raza : str
    peso: int
    marca :str
    id_proposito: int
    id_mansedumbre : int
    id_estado: int
    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_sexo(BaseModel):
    id_sexo : int
    descri_sexo :str
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_proposito(BaseModel):
    id_proposito : int
    descri_proposito :str
    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_estado(BaseModel):
    id_estado : int
    descri_estado :str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_mansedumbre(BaseModel):
    id_mansedumbre : int
    descri_mansedumbre :str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_ceba(BaseModel):
    id_bovino : int
    id_proposito :int
    estado_optimo_ceba:str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_levante(BaseModel):
    id_levante : int
    id_bovino :int
    id_proposito:int
    estado_optimo_levante : str
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_produccion_leche(BaseModel):
    prod_lactancia : int
    dura_lactancia :int
    id_proposito:int
    fecha_primer_parto: date
    edad_primer_parto: int
    fecha_inicial_ordeno : date
    fecha_fin_ordeno: date
    num_partos:int
    id_proposito:int
    id_bovino:int
    tipo_parto:int
    datos_prenez:int
    fecha_ultimo_parto: date
    fecha_ultima_prenez: date
    dias_abiertos: int
    fecha_vida_util:date
    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_tipo_parto(BaseModel):
    id_tipo_parto : int
    descri_tipo_parto :str

    class Config:
        orm_mode = True
        env_file = ".env"


class esquema_datos_prenez(BaseModel):
    id_datos_prenez: int
    descri_datos_prenez: str

    class Config:
        orm_mode = True
        env_file = ".env"

class esquema_datos_muerte(BaseModel):
    id_datos_muerte: int
    id_bovino: int
    id_estado: int
    razon_muerte:int
    fecha_muerte:date
    class Config:
        orm_mode = True
        env_file = ".env"
class esquema_arbol_genialogico(BaseModel):
    id_arbol_genialogico: int
    id_bovino_madre: int
    id_bovino_padre: int
    id_bovino:int
    class Config:
        orm_mode = True
        env_file = ".env"