"""
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
from pydantic import BaseModel

import  datetime
from  typing import   Optional

class Esquema_bovinos(BaseModel):
    id_inven_Bovino : int
    raza :str
    sexo :str
    edad : int
    peso: int
    marca :str
    lugar_Procedencia: str
    fecha_nacimiento : int
    Mansedumbre : str

    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"







