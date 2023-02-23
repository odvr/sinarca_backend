'''
Librerias requeridas

@autor : odvr

'''
from fastapi import APIRouter, Response, status
#importa la conexion de la base de datos
from config.db import condb,engine
#importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario
from schemas.schemas_bovinos import Esquema_bovinos
from sqlalchemy import  select,insert,values
from starlette.status import HTTP_204_NO_CONTENT

from datetime import date, datetime

rutas_bovinos = APIRouter()
"""
La siguiente funcion retorna un diccionario con la consulta general del la tabla bovinos,
 utlizando el decorador execute
"""
@rutas_bovinos.get("/listar_inventarios",
                   response_model=list[Esquema_bovinos], tags=["listar_inventarios"]
                   )
def inventario_bovino():
    items = condb.execute(modelo_bovinos_inventario.select()).fetchall()
    return items

"""
La siguiente funcion retorna un diccionario con la consulta de un ID del la tabla bovinos,
"""
@rutas_bovinos.get("/listar_bovino/{id}",response_model=Esquema_bovinos
                   )
def id_inventario_bovino(idbovino:int):
    consulta = condb.execute(modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == idbovino)).first()
    return consulta


"""
Realiza la creacion de nuevos bovinos en la base de datos, 
la clase Esquema_bovinos  recibira como base para crear el animal esto con fin de realizar la consulta
"""
@rutas_bovinos.post("/crear_bovino",status_code=HTTP_204_NO_CONTENT)
def crear_bovinos(esquemaBovinos:Esquema_bovinos):
    bovinos_dic =esquemaBovinos.dict()
    ingreso = modelo_bovinos_inventario.insert().values(bovinos_dic)
    condb.execute(ingreso)
    return Response(status_code=HTTP_204_NO_CONTENT)



'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{idbovino}",response_model=Esquema_bovinos)
def cambiar_esta_bovino(data_update:Esquema_bovinos,idbovino:int):
     condb.execute( modelo_bovinos_inventario.update().values(
         fecha_nacimiento=data_update.fecha_nacimiento, sexo_id=data_update.sexo_id, raza=data_update.raza,
          peso=data_update.peso, marca=data_update.marca,id_proposito=data_update.id_proposito,
         id_mansedumbre=data_update.id_mansedumbre,id_estado=data_update.id_estado).where(modelo_bovinos_inventario.columns.id_bovino == idbovino))
     # Retorna una consulta con el id actualizado
     resultado_actualizado =  condb.execute(modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == idbovino)).first()
     #condb.commit()
     return resultado_actualizado
"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""
@rutas_bovinos.delete("/eliminar_bovino/{idbovino}",status_code=HTTP_204_NO_CONTENT)
def eliminar_bovino(id_bovino:int):
    condb.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bovino))
    #condb.commit()
    #retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)



"""
La siguiente funcion toma el parametro de codigo del bovino retornando un dato data.time que indica la fecha de nacimiento del bovino
def ConsultarFechaNacimiento(cod_bovino:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(modelo_bovinos_inventario.columns.cod_bovino == cod_bovino)).first()
    return consulta_fecha_nacimiento
print(ConsultarFechaNacimiento(2))
"""


@rutas_bovinos.get("/calcular_edad/{id}",response_model=Esquema_bovinos
                   )
def calculoEdad(id_bovino_edad:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino_edad)).first()
    fecha_N = datetime(consulta_fecha_nacimiento)
    Edad_Animal = (date.today().year - fecha_N.year) * 12 + date.today().month - fecha_N.month
    return Edad_Animal














