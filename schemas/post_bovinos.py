"""
El siguiente codigo permitira realizar el esquema de bases de datos para el metodo Post
"""
#importar los tipos de datos
# permite modelar los datos o crearlos
from pydantic import BaseModel
from  typing import   Optional

class Esquema_bovinos(BaseModel):
    id : int
    raza :str
    sexo :str
    edad : int
    peso: int
    proposito :str
    marca : str
    procedencia: str
    observaciones : str
    #Este Config La clase se utiliza para proporcionar configuraciones a Pydantic.
    class Config:
        orm_mode = True
        env_file = ".env"







