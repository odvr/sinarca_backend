"""
para el desarrollo de una funcion que calcule la edad a partir de la fecha de nacimiento
importamos la libreria datatime y date para poder trabajar con la fecha del sistema
la funcion creada convierte una fecha ingresada (como tipo string) en un formato fecha
para luego extraer la diferencia entre la fecha actual y la de nacimiento obtiendo asi una variable
actualizable en el tiempo
"""
from datetime import datetime, date, timedelta
#importacion del modelo
from models.modelo_bovinos import modelo_bovinos_inventario
# importacion del modulo de base de datos
from config.db import condb,engine

from datetime import date

from sqlalchemy import  select
#libreria Fastapi para realizar la conxion con el modulo temporalmente
from fastapi import APIRouter, Response, status
funciones_bovinos = APIRouter()
from schemas.schemas_bovinos import Esquema_bovinos


"""
La siguiente funcion toma el parametro de codigo del bovino retornando un dato data.time que indica la fecha de nacimiento del bovino
def ConsultarFechaNacimiento(cod_bovino:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(modelo_bovinos_inventario.columns.cod_bovino == cod_bovino)).first()
    return consulta_fecha_nacimiento
print(ConsultarFechaNacimiento(2))
"""

def calculoEdad(cod_bovino:int):
    consulta_fecha_nacimiento = condb.execute(select(modelo_bovinos_inventario.columns.fecha_nacimiento).where(
        modelo_bovinos_inventario.columns.cod_bovino == cod_bovino)).first()
    fecha_N = datetime(consulta_fecha_nacimiento)
    Edad_Animal = (date.today().year - fecha_N.year) * 12 + date.today().month - fecha_N.month
    return Edad_Animal

calculoEdad(2)


""""para la funcion de intervalos partos se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la ficha del ultimo parto
y la fecha del parto anterior y devuelve el resultado en meses"""""


def Intervalo_Partos(Fecha_Ultimo_Parto, Fecha_Anterior_Parto):
    fecha_1 = datetime.strptime(Fecha_Ultimo_Parto, "%d/%m/%Y")
    fecha_2 = datetime.strptime(Fecha_Anterior_Parto, "%d/%m/%Y")
    Inter_Partos = (fecha_1.year - fecha_2.year) * 12 + fecha_1.month - fecha_2.month
    print(Inter_Partos)
    if Inter_Partos > 13:
        print("el animal tiene un intervalo de partos mayor a 13 meses, NO tiene un parto al año")
    else:
        print("el animal tiene un intervalo de partos menor a 13 meses, TIENE un parto al año")


Intervalo_Partos("01/01/2022", "01/02/2021")

"""
para la funcion de edad al primer parto se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en meses entre la fecha del primer parto
y la fecha de nacimiento para devolver la eeda (en meses) en la que la novilla
 tuvo su primer parto
"""


def Edad_Primer_Parto(Fecha_Nacimiento, Fecha_Primer_Parto):
    fecha_1 = datetime.strptime(Fecha_Primer_Parto, "%d/%m/%Y")
    fecha_2 = datetime.strptime(Fecha_Nacimiento, "%d/%m/%Y")
    Edad_1_Parto = (fecha_1.year - fecha_2.year) * 12 + fecha_1.month - fecha_2.month
    print(Edad_1_Parto)
    if Edad_1_Parto > 24:
        print("el animal tuvo su primer parto a una edad MAYOR a 24 meses, valor no recomendable")
    else:
        print("el animal tuvo su primer parto a una edad aproximada de 24 meses, valor recomendado")


Edad_Primer_Parto("01/01/2022", "01/03/2023")

"""
"para la funcion de Duracion de lactancia se utilizan las librerias datetime 
la funcion convierte las fechas ingresadas (tipo string) en un formato fecha
posteriormente calcula la diferencia en dias entre la fecha del ultimo ordeño
y la fecha del primer ordeño y devuelve la cantidad de dias en que se ordeño 
la vaca
"""


def Duracion_Lactancia(Fecha_Ultimo_Ordeno, Fecha_Primer_Ordeno):
    fecha_1 = datetime.strptime(Fecha_Ultimo_Ordeno, "%d/%m/%Y")
    fecha_2 = datetime.strptime(Fecha_Primer_Ordeno, "%d/%m/%Y")
    Duracion = (fecha_1.year - fecha_2.year) * 365 + (fecha_1.month - fecha_2.month) * 30
    print(Duracion)
    if Duracion > 305:
        print("el animal se ordeño durante mas de 305 dias")
    else:
        print("el animal se ordeño durante menos de 305 dias")


Duracion_Lactancia("01/01/2023", "01/01/2022")
"""
para la funcion de Perdida Terneros se utilizan la cantidad de
terneros muertos y la cantidad total de terneros (tipo int)
y mediante una regla de tres, nos muestra el porcentaje de terneros
fallecidos, que se catalogan como perdidas
"""


def Perdida_Terneros(Terneros_Muertos, Terneros_Totales):
    Perdidas = (Terneros_Muertos / Terneros_Totales) * 100
    print(Perdidas)
    if Perdidas > 2:
        print("los terneros fallecidos superan el 2% del total, debes revisar su estado")
    else:
        print("los terneros fallecidos NO superan el 2% del total")


Perdida_Terneros(3, 120)
"""
para el desarroloo de sta funcion se requiere la cantidad de animales vivos
y la cantidad total de animales para mediante una regla de tres se obtiene un
porcentaje de cuantos animales vivos posee el ususario
"""


def Tasa_Sobrevivencia(Estado_Vivo, Total_Animales):
    Tasa = (Estado_Vivo / Total_Animales) * 100
    print("tienes un", Tasa, "% de animales vivos")
    if Tasa >= 97:
        print("felicidades, tienes 97% o mas de tus animales vivos")
    else:
        print("tienes un 3% o mas de fallecimientos, debes revisar tus animales")


Tasa_Sobrevivencia(120, 200)
"""
esta funcion recibe como parametro la fecha del primer parto y
hace uso de la lidbreria datatime ( timedelta),primero convierte 
la fecha del primer parto a tipo fecha y luego toma este valor
y lo suma con el tiempo util (72.3 meses) para determinar la fecha
en que dicho animal dejara de ser productivo, posteriormente tambien
devolvera el tiempo restante para llegar a esa fecha mediante la resta
del tiempo actual
"""


def Edad_Sacrificio_Lecheras(Fecha_Primer_Parto):
    fecha_1 = datetime.strptime(Fecha_Primer_Parto, "%d/%m/%Y")
    Fecha_Vida_Util = fecha_1 + timedelta(2169)
    Tiempo_Restante = round((Fecha_Vida_Util.year - datetime.today().year) + \
                      (Fecha_Vida_Util.month - datetime.today().month )/12 +\
                      (Fecha_Vida_Util.day -datetime.today().day)/365, ndigits=2)
    print("la vida util de este animal llegara aproximadamente hasta ", Fecha_Vida_Util)
    print("El tiempo para que se cumpla la vida util aproximada es", Tiempo_Restante, "años")

Edad_Sacrificio_Lecheras("01/01/2021")
"""
estas funciones deben ser complementarias, puesto que el peso levante
solo puede aplicar en cas de que tengan edad suficiente
"""


def Edad_Levante(Edad):
    print("este animal tiene una edad de", Edad, "meses")
    Falta = 8 - Edad
    if Edad >= 8:
        print("Este animal esta a una edad acta de lenvate, por parvor actuliza su peso")
    else:
        print("Este animal no posee una edad de levante adecuada, por favor espera", Falta, "meses")


Edad_Levante(7.5)


def Peso_Levante(Peso):
    print("este animal tiene un peso de", Peso, "kilos")
    if Peso >= 140:
        print("Este animal tiene un peso optimo de levante")
    else:
        print("Este Animal no tiene peso igual o mayor a 140 Kg, por favor revisalo")


Peso_Levante(136)
"""
"""


def Edad_Ceba(Edad):
    print("este animal tiene una edad de", Edad, "meses")
    Falta = 24 - Edad
    if Edad >= 24:
        print("Este animal esta a una edad acta de Ceba, por parvor actuliza su peso")
    else:
        print("Este animal no posee una edad de Ceba adecuada, por favor espera", Falta, "meses")


Edad_Ceba(23.5)


def Peso_Ceba(Peso):
    print("este animal tiene un peso de", Peso, "kilos")
    if Peso >= 350:
        print("Este animal tiene un peso optimo de Ceba")
    else:
        print("Este Animal no tiene peso igual o mayor a 350 Kg, por favor revisalo")


Peso_Ceba(340)

def Dias_Abiertos(Fecha_Ultimo_Parto, Fecha_Ultima_Prenez):
    fecha_2 = datetime.strptime(Fecha_Ultimo_Parto, "%d/%m/%Y")
    fecha_1 = datetime.strptime(Fecha_Ultima_Prenez, "%d/%m/%Y")
    Dias_A = (fecha_1.year - fecha_2.year) * 365 + (fecha_1.month - fecha_2.month)*30 +\
             (fecha_1.day-fecha_2.day)
    print(Dias_A)
    if Dias_A <= 120:
        print("Este animal se ha preñado en dos meses o menos")
    else:
        print("Este animal lleva mas de meses sin preñarse, debes revisarlo")

Dias_Abiertos("01/01/2021","01/07/2021")

