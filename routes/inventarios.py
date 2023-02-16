'''
Librerias requeridas

@autor : odvr

'''
from fastapi import APIRouter, Response, status
#importa la conexion de la base de datos
from config.db import condb,engine
#importa el esquema de los bovinos
from models.modelo_inventarios import modelo_bovinos
from schemas.post_bovinos import Esquema_bovinos
from sqlalchemy import  select,insert,values
from starlette.status import HTTP_204_NO_CONTENT

rutas_bovinos = APIRouter()
"""
La siguiente funcion retorna un diccionario con la consulta general del la tabla bovinos,
 utlizando el decorador execute
"""
@rutas_bovinos.get("/listar_inventarios",
                   response_model=list[Esquema_bovinos], tags=["listar_inventarios"]
                   )
def inventario_bovino():
    items = condb.execute(modelo_bovinos.select()).fetchall()
    return items

"""
La siguiente funcion retorna un diccionario con la consulta de un ID del la tabla bovinos,
"""
@rutas_bovinos.get("/listar_inventarios/{id}",response_model=Esquema_bovinos
                   )
def id_inventario_bovino(id:int):
    consulta = condb.execute(modelo_bovinos.select().where(modelo_bovinos.columns.id == id)).first()
    return consulta


"""
Realiza la creacion de nuevos bovinos en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""
@rutas_bovinos.post("/crear_bovino")
def crear_bovinos(esquemaBovinos:Esquema_bovinos):
    bovinos_dic =esquemaBovinos.dict()
    ingreso = modelo_bovinos.insert().values(bovinos_dic)
    condb.execute(ingreso)
    condb.commit()


'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_estado_bovino/{idbovino}",response_model=Esquema_bovinos)
def cambiar_esta_bovino(data_update:Esquema_bovinos,idbovino:int):
     condb.execute( modelo_bovinos.update().values(
         raza=data_update.raza, sexo=data_update.sexo, edad=data_update.edad, peso=data_update.peso,
         proposito=data_update.proposito, marca=data_update.marca, procedencia=data_update.procedencia,
         observaciones=data_update.observaciones).where(modelo_bovinos.columns.id == idbovino))
     # Retorna una consulta con el id actualizado
     resultado_actualizado =  condb.execute(modelo_bovinos.select().where(modelo_bovinos.columns.id == idbovino)).first()
     condb.commit()
     return resultado_actualizado
"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""
@rutas_bovinos.delete("/eliminar_bovino/{idbovino}",status_code=HTTP_204_NO_CONTENT)
def eliminar_bovino(idbovino:int):
    condb.execute(modelo_bovinos.delete().where(modelo_bovinos.c.id == idbovino))
    condb.commit()
    #retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)
















