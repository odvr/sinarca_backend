"""
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
from pydantic import BaseModel

from datetime import date


class Esquema_bovinos(BaseModel):
    cod_bovino : int
    fecha_nacimiento: date
    sexo :int
    raza : str
    peso: int
    marca :str
    cod_proposito: int
    mansedumbre : int
    cod_estado: int
    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"







