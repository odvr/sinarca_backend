'''
Librerias requeridas

@autor : odvr

'''
from tkinter import INSERT

import sqlalchemy
from fastapi import APIRouter, Response, status
from sqlalchemy.engine import cursor

#importa la conexion de la base de datos
#from APi.config.db import condb
from config.db import condb
#importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_levante, modelo_ceba
from schemas.schemas_bovinos import Esquema_bovinos
from sqlalchemy import select, insert, values, update, bindparam
from starlette.status import HTTP_204_NO_CONTENT

from datetime import date, datetime, timedelta

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
    condb.commit()
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
     condb.commit()
     return resultado_actualizado
"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""
@rutas_bovinos.delete("/eliminar_bovino/{idbovino}",status_code=HTTP_204_NO_CONTENT)
def eliminar_bovino(id_bovino:int):
    condb.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bovino))
    condb.commit()
    #retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)



"""
La siguiente funcion toma el parametro de codigo del bovino retornando un dato data.time que indica la fecha de nacimiento del bovino
def ConsultarFechaNacimiento(cod_bovino:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(modelo_bovinos_inventario.columns.cod_bovino == cod_bovino)).first()
    return consulta_fecha_nacimiento
print(ConsultarFechaNacimiento(2))
"""


@rutas_bovinos.post("/calcular_edad/{id}",response_model=Esquema_bovinos
                   )
def calculoEdad(id_bovino_edad:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino_edad)).first()
    fecha_N = consulta_fecha_nacimiento.__str__().split('(').pop(2).split(')').pop(0)
    fecha_N2 = "".join(fecha_N).replace(', ', '/')
    fecha_N3 = datetime.strptime(fecha_N2, "%Y/%m/%d")
    Edad_Animal = (datetime.today().year - fecha_N3.year) * 12 + datetime.today().month - fecha_N3.month
    condb.execute(update(modelo_bovinos_inventario).
                           where(modelo_bovinos_inventario.columns.id_bovino == id_bovino_edad).
              values(edad=Edad_Animal))
    condb.commit()
"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""
def Edad_Primer_Parto(id_bovino:int):
    fecha_P,fecha_N = condb.execute(select(modelo_leche.columns.fecha_primer_parto,
        modelo_bovinos_inventario.columns.fecha_nacimiento).where(
        modelo_leche.columns.id_bovino == id_bovino,
        modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
    Edad_primer_parto = (fecha_P.year - fecha_N.year) * 12 + fecha_P.month - fecha_N.month
    condb.execute(update(modelo_leche).
                           where(modelo_leche.columns.id_bovino == id_bovino).
              values(edad_primer_parto=Edad_primer_parto))
    condb.commit()
"""
"para la funcion de Duracion de lactancia se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en dias entre la fecha del ultimo ordeño
y la fecha del primer ordeño y devuelve la cantidad de dias en que se ordeño 
la vaca
"""


def Duracion_Lactancia(id_bovino:int):
    fecha_Inicio_O,fecha_Final_O = condb.execute(select(modelo_leche.columns.fecha_inicial_ordeno,
        modelo_leche.columns.fecha_fin_ordeno).where(
        modelo_leche.columns.id_bovino == id_bovino,
        modelo_leche.columns.id_bovino == id_bovino)).first()
    Duracion_Lac = (fecha_Final_O.year - fecha_Inicio_O.year) * 365 + (fecha_Final_O.month - fecha_Inicio_O.month)*30
    condb.execute(update(modelo_leche).
                  where(modelo_leche.columns.id_bovino == id_bovino).
                  values(dura_lactancia=Duracion_Lac))
    condb.commit()

"""
esta funcion recibe como parametro la fecha del primer parto y
hace uso de la lidbreria datatime ( timedelta),primero convierte 
la fecha del primer parto a tipo fecha y luego toma este valor
y lo suma con el tiempo util (72.3 meses) para determinar la fecha
en que dicho animal dejara de ser productivo, posteriormente tambien
devolvera el tiempo restante para llegar a esa fecha mediante la resta
del tiempo actual
"""


def Edad_Sacrificio_Lecheras(id_bovino:int):
    Consulta_P1 = condb.execute(select(modelo_leche.columns.fecha_primer_parto).where(
        modelo_leche.columns.id_bovino == id_bovino)).first()
    fecha_P = Consulta_P1.__str__().split('(').pop(2).split(')').pop(0)
    fecha_P1 = "".join(fecha_P).replace(', ', '/')
    fecha_Parto_1 = datetime.strptime(fecha_P1, "%Y/%m/%d")
    fecha_Vida_Util = fecha_Parto_1 + timedelta(2169)
    condb.execute(update(modelo_leche).
                  where(modelo_leche.columns.id_bovino == id_bovino).
                  values(fecha_vida_util=fecha_Vida_Util))
    condb.commit()

"""
"""
def Estado_Optimo_Levante(id_bovino:int):
    edad,peso = condb.execute(select(modelo_bovinos_inventario.columns.edad,
        modelo_bovinos_inventario.columns.peso).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino,
        modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
    if peso >= 140 and edad in range(8,11):
        estado_levante ="Estado optimo"

    else:
        estado_levante ="Estado nooptimo"
    condb.execute(update(modelo_levante).
                  where(modelo_levante.columns.id_bovino == id_bovino).
                  values(estado_optimo_levante=estado_levante))
    condb.commit()
def Estado_Optimo_Ceba(id_bovino:int):
    edad,peso = condb.execute(select(modelo_bovinos_inventario.columns.edad,
        modelo_bovinos_inventario.columns.peso).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino,
        modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
    if peso >= 350 and edad in range(24, 36):
        estado_ceba = "Estado optimo"
    else:
        estado_ceba = "Estado no optimo"
    condb.execute(update(modelo_ceba).
                  where(modelo_ceba.columns.id_bovino == id_bovino).
                  values(estado_optimo_ceba=estado_ceba))
    condb.commit()
"""
"""

def Dias_Abiertos(id_bovino:int):
    fecha_ultimo_p,fecha_ultima_prenez = condb.execute(select(modelo_leche.columns.fecha_ultimo_parto,
        modelo_leche.columns.fecha_ultima_prenez).where(
        modelo_leche.columns.id_bovino == id_bovino,
        modelo_leche.columns.id_bovino == id_bovino)).first()
    Dias_A = (fecha_ultima_prenez.year - fecha_ultimo_p.year) * 365 + (fecha_ultima_prenez.month - fecha_ultimo_p.month)*30 +\
             (fecha_ultima_prenez.day-fecha_ultimo_p.day)
    condb.execute(update(modelo_leche).
                  where(modelo_leche.columns.id_bovino == id_bovino).
                  values(dias_abiertos=Dias_A))
    condb.commit()
