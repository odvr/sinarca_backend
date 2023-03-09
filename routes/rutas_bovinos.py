'''
Librerias requeridas

@autor : odvr

'''
import threading
from tkinter import INSERT

import sqlalchemy
from typing import Dict, Any
from fastapi import APIRouter, Response, status
from sqlalchemy.engine import cursor, row

#importa la conexion de la base de datos
#from APi.config.db import condb
from config.db import condb,session
# importa el esquema de los bovinos

#importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_leche, modelo_levante, \
    modelo_indicadores, modelo_ceba
from schemas.schemas_bovinos import Esquema_bovinos, esquema_produccion_leche, esquema_produccion_levante, \
    esquema_produccion_ceba
from sqlalchemy import select, insert, values, update, bindparam, between, join, func
from starlette.status import HTTP_204_NO_CONTENT
import apply
from sqlalchemy.orm import query

from datetime import date, datetime, timedelta, time

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
Lista los datos de la tabla prod leche inventario
"""
@rutas_bovinos.get("/listar_bovino_prodLeche/{id_bovino}"
                   )
def id_inventario_bovino_leche(id_bovino: str):
    try:
        consulta = session.execute(
            modelo_leche.select().where(modelo_leche.columns.id_bovino == id_bovino)).first()
    finally:
        session.close()
    # condb.commit()
    return consulta
"""
La siguiente funcion retorna un diccionario con la consulta de un ID del la tabla bovinos,
"""
@rutas_bovinos.get("/listar_bovino/{id_bovino}",  response_model=Esquema_bovinos,
                   )
def id_inventario_bovino(id_bovino:str):
    consulta = condb.execute(modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
    #condb.commit()
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


"""
La siguiente api inserte 
 
"""
@rutas_bovinos.post("/crear_prod_leche/{fecha_primer_parto}/{id_bovino}/{fecha_inicial_ordeno}/{fecha_fin_ordeno}/{fecha_ultimo_parto}/{fecha_ultima_prenez}/{num_partos}/{tipo_parto}/{datos_prenez}/{ordeno}",status_code=HTTP_204_NO_CONTENT)
def CrearProdLeche(fecha_primer_parto: date,id_bovino:str,fecha_inicial_ordeno:date,fecha_fin_ordeno:date,fecha_ultimo_parto:date,fecha_ultima_prenez:date,num_partos:int,tipo_parto:str,datos_prenez:str,ordeno:str):
    ingresopleche = modelo_leche.insert().values(fecha_primer_parto=fecha_primer_parto,id_bovino=id_bovino,fecha_inicial_ordeno=fecha_inicial_ordeno,fecha_fin_ordeno=fecha_fin_ordeno,fecha_ultimo_parto=fecha_ultimo_parto,fecha_ultima_prenez=fecha_ultima_prenez,num_partos=num_partos,tipo_parto=tipo_parto,datos_prenez=datos_prenez,ordeno=ordeno)
    condb.execute(ingresopleche)
    return Response(status_code=HTTP_204_NO_CONTENT)


'''
La siguiente funcion realiza la actualizacion completa de la tabla de bovinos para cambiar los registros
'''
@rutas_bovinos.put("/cambiar_datos_bovino/{id_bovino}",response_model=Esquema_bovinos)
def cambiar_esta_bovino(data_update:Esquema_bovinos,id_bovino:str):
     condb.execute( modelo_bovinos_inventario.update().values(
         fecha_nacimiento=data_update.fecha_nacimiento, sexo=data_update.sexo, raza=data_update.raza,
          peso=data_update.peso, marca=data_update.marca,proposito=data_update.proposito,
         mansedumbre=data_update.mansedumbre,estado=data_update.estado).where(modelo_bovinos_inventario.columns.id_bovino == id_bovino))
     # Retorna una consulta con el id actualizado
     resultado_actualizado =  condb.execute(modelo_bovinos_inventario.select().where(modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
     #condb.commit()
     return resultado_actualizado
"""
Esta funcion elimina por ID los registros de la tabla de bovinos
"""
@rutas_bovinos.delete("/eliminar_bovino/{id_bovino}",status_code=HTTP_204_NO_CONTENT)
def eliminar_bovino(id_bovino:str):
    condb.execute(modelo_bovinos_inventario.delete().where(modelo_bovinos_inventario.c.id_bovino == id_bovino))
    condb.commit()
    #retorna un estado de no contenido
    return Response(status_code=HTTP_204_NO_CONTENT)



"""
La siguiente funcion consulta la fecha de nacimiento del bovino mediante su id y
calcula la edad del animal (en meses) utilizando la fecha actual
"""
@rutas_bovinos.post("/calcular_edad/{id_bovino}")
def calculoEdad(id_bovino:str):
    #consulta fecha de nacimmiento con el id_bovino
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino)).first()
    #transformaacion de dato a tipo string y luego a tipo date
    fecha_N = consulta_fecha_nacimiento.__str__().split('(').pop(2).split(')').pop(0)
    fecha_N2 = "".join(fecha_N).replace(', ', '/')
    fecha_N3 = datetime.strptime(fecha_N2, "%Y/%m/%d")
    #calculo de la edad a partir de la fecha actual
    Edad_Animal = (datetime.today().year - fecha_N3.year) * 12 + datetime.today().month - fecha_N3.month
    #actualizacion del campo en la base de datos
    condb.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
        modelo_bovinos_inventario.columns.id_bovino == id_bovino))
    condb.commit()
    return Edad_Animal
"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""
@rutas_bovinos.post("/calcular_edad_parto_1/{id_bovino}")
def Edad_Primer_Parto(id_bovino:str):
    #consulta de las fecha de primer parto y fecha de nacimiento
    fecha_P,fecha_N = session.query \
        (modelo_leche.c.fecha_primer_parto,
         modelo_bovinos_inventario.c.fecha_nacimiento). \
        where(modelo_leche.c.id_bovino == id_bovino,
              modelo_bovinos_inventario.c.id_bovino == id_bovino).first()
    #calculo de la edad al primer parto
    Edad_primer_parto = (fecha_P.year - fecha_N.year) * 12 + fecha_P.month - fecha_N.month
    #actualizacin del campo
    session.execute(update(modelo_leche).
            where(modelo_leche.c.id_bovino == id_bovino).
              values(edad_primer_parto=Edad_primer_parto))
    session.commit()
    return Edad_primer_parto
"""
"para la funcion de Duracion de lactancia se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en dias entre la fecha del ultimo ordeno
y la fecha del primer ordeno y devuelve la cantidad de dias en que se ordeno 
la vaca
"""

@rutas_bovinos.post("/calcular_Dur_Lac/{id}")
def Duracion_Lactancia(id_bovino:str):
    #consulta de la fecha inicial y final de ordeno
    fecha_Inicio_O,fecha_Final_O = session.query \
        (modelo_leche.c.fecha_inicial_ordeno,
         modelo_leche.c.fecha_fin_ordeno). \
        where(modelo_bovinos_inventario.c.id_bovino == id_bovino,
              modelo_bovinos_inventario.c.id_bovino == id_bovino).first()
    #calculo de la duracion de la lactancia
    Duracion_Lac = (fecha_Final_O.year - fecha_Inicio_O.year) * 360 +\
                   (fecha_Final_O.month - fecha_Inicio_O.month)*30
    #actualizacion del campo
    session.execute(update(modelo_leche).
                  where(modelo_leche.c.id_bovino == id_bovino).
                  values(dura_lactancia=Duracion_Lac))
    session.commit()
    return Duracion_Lac
"""
esta funcion recibe como parametro la fecha del primer parto y
hace uso de la lidbreria datatime ( timedelta),primero convierte 
la fecha del primer parto a tipo fecha y luego toma este valor
y lo suma con el tiempo util (72.3 meses) para determinar la fecha
en que dicho animal dejara de ser productivo, posteriormente tambien
devolvera el tiempo restante para llegar a esa fecha mediante la resta
del tiempo actual
"""
@rutas_bovinos.post("/calcular_Edad_Sacrificio/{id}")
def Edad_Sacrificio_Lecheras(id_bovino:str):
    #consulta de la fecha de primer parto
    Consulta_P1 = session.query \
        (modelo_leche.c.fecha_primer_parto). \
        where(modelo_leche.c.id_bovino == id_bovino).first()
    #conversion de la fecha a tipo string y luago a tipo date
    fecha_P = Consulta_P1.__str__().split('(').pop(2).split(')').pop(0)
    fecha_P1 = "".join(fecha_P).replace(', ', '/')
    fecha_Parto_1 = datetime.strptime(fecha_P1, "%Y/%m/%d")
    #calculo de la vida util mediante la suma del promedio de vida util con la fecha de parto
    fecha_Vida_Util = fecha_Parto_1 + timedelta(2169)
    #actualizacion del campo
    session.execute(update(modelo_leche).
                  where(modelo_leche.c.id_bovino == id_bovino).
                  values(fecha_vida_util=fecha_Vida_Util))
    session.commit()
    return fecha_Vida_Util
"""
la siguiente funcion determina si la condicion de un animal para
levante es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 140 kg y edad de 8 a 10 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""
@rutas_bovinos.post("/calcular_Estado_levante/{id}")
def Estado_Optimo_Levante(id_bovino:str):
    # consulta de la edad y peso del animal
    edad,peso = session.query \
        (modelo_bovinos_inventario.c.edad,
         modelo_bovinos_inventario.c.peso). \
        where(modelo_bovinos_inventario.c.id_bovino == id_bovino,
              modelo_bovinos_inventario.c.id_bovino == id_bovino).first()
    # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
    if peso>=140 and edad in range(8,13):
        estado_levante= "Estado Optimo"
    elif peso<140 and edad in range(8,13):
        estado_levante= "Estado NO Optimo, este animal tiene un peso menor a 140 kilos"
    elif peso<140 and edad<8:
        estado_levante= "Estado NO Optimo, este animal tiene un peso menor a 140 kilos y menos de 8 meses de edad"
    elif peso>=140 and edad<8:
        estado_levante= "Estado NO Optimo, este animal tiene menos de 8 meses de edad"
    else:
        estado_levante = "Estado NO Optimo, este animal tiene una edad mayor a 12 meses, considera pasarlo a ceba"
    #actualizacion del campo
    session.execute(update(modelo_levante).
            where(modelo_levante.c.id_bovino == id_bovino).
                  values(estado_optimo_levante=estado_levante))
    session.commit()
    return estado_levante
"""
la siguiente funcion determina si la condicion de un animal para
ceba es optima, para ello, trae los valores de la edad y peso 
del animal y los compara con los rangos recomendados (peso igual o
mayor a 350 kg y edad de 24 a 36 meses), delvolviendo asi un string
que dicta si la condicion es o no optima
"""
@rutas_bovinos.post("/calcular_Estado_ceba/{id}",)
def Estado_Optimo_Ceba(id_bovino:str):
    # consulta de la edad y peso del animal
    edad,peso = session.query \
        (modelo_bovinos_inventario.c.edad,
        modelo_bovinos_inventario.c.peso). \
        where(modelo_bovinos_inventario.c.id_bovino == id_bovino,
        modelo_bovinos_inventario.c.id_bovino == id_bovino).first()
    # bucle if que determina si cumple con el estado optimo o no y el porque no cumple
    if peso>=350 and edad in range(24,37):
        estado_ceba= "Estado Optimo"
    elif peso<350 and edad in range(24,37):
        estado_ceba= "Estado NO Optimo, este animal tiene un peso menor a 350 kilos"
    elif peso>=350 and edad<24:
        estado_ceba= "Estado NO Optimo, este animal tiene menos de 24 meses de edad"
    elif peso<350 and edad<24:
        estado_ceba= "Estado NO Optimo, este animal tiene menos de 24 meses de edad y menos de 350 kilos"
    else:
        estado_ceba = "Estado NO Optimo, este animal tiene una edad mayor a 36 meses"
        # actualizacion del campo
    session.execute(update(modelo_ceba).
                  where(modelo_ceba.c.id_bovino == id_bovino).
                  values(estado_optimo_ceba=estado_ceba))
    session.commit()
    return estado_ceba
"""
esta funcion calcula los dias abiertos apartir de la diferencia en dias
entre la fecha de ultimo parto y fecha de ultima prenez, siendo una medida
de productividad, pues si una vaca tiene mas de 120 dias abiertos, indica 
que no esta teniendo un ternero al ano, lo que indica que no esta siendo
productiva
"""
@rutas_bovinos.post("/calcular_dias_abiertos/{id}")
def Dias_Abiertos(id_bovino:str):
    #consulta fecha ultimo parto y fecha ultima prenez del animal
    fecha_ultimo_p,fecha_ultima_prenez = session.query \
        (modelo_leche.c.fecha_ultimo_parto,
        modelo_leche.c.fecha_ultima_prenez). \
        where(modelo_leche.c.id_bovino == id_bovino,
        modelo_leche.c.id_bovino == id_bovino).first()
    #calculo de los dias entre las dos fechas (dias abiertos)
    Dias_A = (fecha_ultima_prenez.year - fecha_ultimo_p.year) * 360 + (fecha_ultima_prenez.month - fecha_ultimo_p.month)*30 +\
             (fecha_ultima_prenez.day-fecha_ultimo_p.day)
    #actualizacion del campo
    session.execute(update(modelo_leche).
                  where(modelo_leche.c.id_bovino == id_bovino).
                  values(dias_abiertos=Dias_A))
    session.commit()
    return Dias_A
"""esta funcion determina el porcentaje de animales vivos que
existen en el hato,para ello utiliza la cantidad de animales vivos,
muertos y totales"""
@rutas_bovinos.post("/Calcular_Tasa_Sobrevivencia/{}")
def Tasa_Sobrevivencia():
    #consulta y seleccion de los animales vivos
    estado_vivo=session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #consulta y seleccion de los animales muertos
    estado_muerto=session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    #total de animales(vivos + muertos)
    totales= estado_vivo+estado_muerto
    #calculo de la tasa
    tasa = (estado_vivo/totales)*100
    #actualizacion del campo
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores == 1).
                  values(tasa_supervivencia=tasa))
    session.commit()
    return tasa
"""esta funcion calcula en terminos de porcentaje, cuantos terneros
(animales de 0 a 6 meses) han fallecido, para ello consulta la cantidad 
de animales muertos y el total para mediante una regla de 3 obtener
el porcentaje
"""
@rutas_bovinos.post("/Calcular_perdida_Terneros/{}")
def perdida_Terneros():
    # consulta, seleccion y conteo de animales con edad de 0 a 6 meses que se encuentren muertos
    muertos = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 6)). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    # consulta, seleccion y conteo de animales con edad de 0 a 6 meses
    totales = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad, 0, 6)).count()
    # calculo de la tasa
    tasa_perd = (muertos / totales) * 100
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                    where(modelo_indicadores.c.id_indicadores == 1).
                    values(perdida_de_terneros=tasa_perd))
    session.commit()
    return tasa_perd
"""esta funcion determina la cantidad de vacas vacias (no prenadas)
esto con el  fin de mostrar cuantos vientres NO estan produciendo en el hato"""
@rutas_bovinos.post("/Calcular_vacas_vacias/{}")
def vacas_vacias():
    #join de tabla bovinos y tabla leche mediante id_bovino \
    # filtrado y conteo animales con datos prenez Vacia que se encuentren vivos
    consulta_vacias = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Vacia').count()
    #actualizacion del campo
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(vacas_vacias=consulta_vacias))
    session.commit()
    return consulta_vacias
"""esta funcion determina la cantidad de vacas no prenadas
esto con el  fin de mostrar cuantos vientres estan produciendo en el hato"""
@rutas_bovinos.post("/Calcular_vacas_prenadas/{}")
def vacas_prenadas():
    # join de tabla bovinos y tabla leche mediante id_bovino \
    # filtrado y conteo animales con datos prenez Prenada que se encuentren vivos
    consulta_prenadas = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.datos_prenez). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.datos_prenez == 'Prenada').count()
    # actualizacion del campo
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(vacas_prenadas=consulta_prenadas))
    session.commit()
    return consulta_prenadas

"""esta funcion calcula el porcentaje de vacas que se encuentran preñadas"""
@rutas_bovinos.post("/Calcular_vacas_prenadas_porcentaje/{}")
def vacas_prenadas_porcentaje():
    #consulta de vacas prenadas y vacas vacias en la base de datos
    prenadas,vacias = session.query\
        (modelo_indicadores.c.vacas_prenadas,modelo_indicadores.c.vacas_vacias).first()
    #calculo del total de animales
    totales= prenadas + vacias
    #calculo procentaje de vacas prenadas
    vacas_estado_pren= (prenadas/totales)*100
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(vacas_prenadas_porcentaje=vacas_estado_pren))
    session.commit()
    return vacas_estado_pren
"""estas funciones muestra la cantidad de animales totales, tambien segun su
proposito, sexo, estado, rango de edades y estado de ordeno"""
@rutas_bovinos.post("/Calcular_animales_totales/{}")
def animales_totales():
    #consulta de total de animales vivos
    total_animales = session.query(modelo_bovinos_inventario).\
        filter(modelo_bovinos_inventario.c.estado=="Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.columns.id_indicadores==1).
                  values(total_animales=total_animales))
    session.commit()
    return total_animales
@rutas_bovinos.post("/Calcular_animales_ceba/{}")
def animales_ceba():
    #consulta de total de animales vivos con proposito de ceba
    prop_ceba = session.query(modelo_bovinos_inventario).\
        filter(modelo_bovinos_inventario.c.estado=="Vivo",
               modelo_bovinos_inventario.c.proposito=="Ceba").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_ceba=prop_ceba))
    session.commit()
    return prop_ceba
@rutas_bovinos.post("/Calcular_animales_levante/{}")
def animales_levante():
    #consulta de total de animales vivos con proposito de levante
    prop_levante = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Levante").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_levante=prop_levante))
    session.commit()
    return prop_levante
@rutas_bovinos.post("/Calcular_animales_leche/{}")
def animales_leche():
    #consulta de total de animales vivos con proposito de leche
    prop_leche = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.proposito == "Leche").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_leche=prop_leche))
    session.commit()
    return prop_leche
@rutas_bovinos.post("/Calcular_animales_muertos/{}")
def animales_muertos():
    #consulta de total de animales muertos
    estado_muerto = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Muerto").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_fallecidos=estado_muerto))
    session.commit()
    return estado_muerto
@rutas_bovinos.post("/Calcular_animales_vendidos/{}")
def animales_vendidos():
    #consulta de total de animales vendidos
    estado_vendido = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vendido").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_vendidos=estado_vendido))
    session.commit()
    return estado_vendido
@rutas_bovinos.post("/Calcular_animales_machos/{}")
def animales_sexo_macho():
    # consulta de total de animales vivos con sexo macho
    machos = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Macho").count()
    # actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(machos=machos))
    session.commit()
    return machos
@rutas_bovinos.post("/Calcular_animales_hembras/{}")
def animales_sexo_hembra():
    #consulta de total de animales vivos con sexo hembra
    hembras = session.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo",
               modelo_bovinos_inventario.c.sexo == "Hembra").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(hembras=hembras))
    session.commit()
    return hembras
@rutas_bovinos.post("/Calcular_animales_ordeno/{}")
def animales_en_ordeno():
    #join, consulta y conteo de animales vivos que son ordenados
    vacas_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'Si').count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(vacas_en_ordeno=vacas_ordeno))
    session.commit()
    return vacas_ordeno
@rutas_bovinos.post("/Calcular_animales_no_ordeno/{}")
def animales_no_ordeno():
    #join, consulta y conteo de animales vivos que no son ordenados
    vacas_no_ordeno = session.query(modelo_bovinos_inventario.c.estado, modelo_leche.c.ordeno). \
        join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo', modelo_leche.c.ordeno == 'No').count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(vacas_no_ordeno=vacas_no_ordeno))
    session.commit()
    return vacas_no_ordeno
@rutas_bovinos.post("/Calcular_porcentaje_ordeno/{}")
def porcentaje_ordeno():
    #consulta de animales ordenados y no ordenados
    ordeno,no_ordeno = session.query\
        (modelo_indicadores.c.vacas_en_ordeno,modelo_indicadores.c.vacas_no_ordeno).first()
    #porcentaje de vacas en ordeno
    vacas_ordeno_porcentaje= (ordeno/(no_ordeno+ordeno))*100
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(porcentaje_ordeno=vacas_ordeno_porcentaje))
    session.commit()
    return vacas_ordeno_porcentaje
@rutas_bovinos.post("/Calcular_animales_edad_0_9/{}")
def animales_edad_0_9():
    #consulta y conteo de animales con edades entre 0 a 9 meses
    edades_0_9 = session.query(modelo_bovinos_inventario).\
        where(between(modelo_bovinos_inventario.columns.edad,0,9)).\
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_rango_edades_0_9=edades_0_9))
    session.commit()
    return edades_0_9
@rutas_bovinos.post("/Calcular_animales_edad_9_12/{}")
def animales_edad_9_12():
    #consulta y conteo de animales con edades entre 10 a 12 meses
    edades_9_12 = session.query(modelo_bovinos_inventario).\
        where(between(modelo_bovinos_inventario.columns.edad,10,12)).\
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_rango_edades_9_12=edades_9_12))
    session.commit()
    return edades_9_12
@rutas_bovinos.post("/Calcular_animales_edad_12_24/{}")
def animales_edad_12_24():
    #consulta y conteo de animales con edades entre 13 a 24 meses
    edades_12_24 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad,13,24)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_rango_edades_12_24=edades_12_24))
    session.commit()
    return edades_12_24
@rutas_bovinos.post("/Calcular_animales_edad_24_36/{}")
def animales_edad_24_36():
    #consulta y conteo de animales con edades entre 25 a 36 meses
    edades_24_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad,25,36)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_rango_edades_24_36=edades_24_36))
    session.commit()
    return edades_24_36
@rutas_bovinos.post("/Calcular_animales_edad_mayor_36/{}")
def animales_edad_mayor_a_36():
    #consulta y conteo de animales con edades igual o mayor a 37 meses
    edades_mayor_36 = session.query(modelo_bovinos_inventario). \
        where(between(modelo_bovinos_inventario.columns.edad,37,500)). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_rango_edades_mayor_36=edades_mayor_36))
    session.commit()
    return edades_mayor_36
@rutas_bovinos.post("/Calcular_Animales_Optimo_Levante/{}")
def Animales_Optimo_Levante():
    #join,consulta y conteo de animales vivos con estado optimo
    levante_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_levante.c.estado_optimo_levante). \
        join(modelo_levante, modelo_bovinos_inventario.c.id_bovino == modelo_levante.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_levante.c.estado_optimo_levante == "Estado Optimo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_optimos_levante=levante_optimo))
    session.commit()
    return levante_optimo
@rutas_bovinos.post("/Calcular_Animales_Optimo_Ceba/{}")
def Animales_Optimo_Ceba():
    # join,consulta y conteo de animales vivos con estado optimo
    ceba_optimo = session.query(modelo_bovinos_inventario.c.estado, modelo_ceba.c.estado_optimo_ceba). \
        join(modelo_ceba, modelo_bovinos_inventario.c.id_bovino == modelo_ceba.c.id_bovino). \
        filter(modelo_bovinos_inventario.c.estado == 'Vivo',
               modelo_ceba.c.estado_optimo_ceba == "Estado Optimo").count()
    #actualizacion de campos
    session.execute(update(modelo_indicadores).
                  where(modelo_indicadores.c.id_indicadores==1).
                  values(animales_optimos_ceba=ceba_optimo))
    session.commit()
    return ceba_optimo