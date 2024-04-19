import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


from routes.Archivos import appArchivos
from routes.Capacidad_Carga import capacidad_carga_rutas
from routes.Ceba_Bovinos import Ceba_Bovinos
from routes.Curvas_Lactancia import Curvas_Lantacia
from routes.Datos_Compra import datos_compra
from routes.Descarte_bovinos import bovinos_descarte
from routes.Formulario_Bovinos import Formulario_Bovino
from routes.Historial_Perdida_Terneros import Historial_Perdida_Terneros
from routes.Historial_tasa_supervivencia_Bovinos import Historial_Tasa_Supervivencia
from routes.Palpaciones_Bovinos import Palpaciones_Bovinos
from routes.PartosAnimales import partos_bovinos
from routes.Pesaje import pesaje
from routes.Prod_leche import Produccion_Leche
from routes.Registro_Pajillas import Pajillas
from routes.Reproductor import ReproductorRutas
from routes.Total_Animales import Pruebas_TotalAnimales
from routes.Total_animales_leche import Pruebas_Leche
from routes.Vientres_Aptos_Routes import Vientres_Aptos
from routes.rutas_bovinos import rutas_bovinos
from routes.Intervalo_Entre_Partos_Hato import Intervalo_Entre_Partos_Hato
from routes.Endogamia import Endogamia
from routes.Inventarios import Inventarios
from routes.Eliminar_Bovino import Eliminar_Bovino
from routes.Levante_Bovinos import Levante_Bovinos
from routes.Muertes_Bovinos import Muertes_Bovinos
from routes.Ventas_Bovinos import Ventas_Bovinos
from routes.IEP_Razas import IEP_Razas
from routes.IntevaloPartos import IntevaloPartos
from routes.Registro_Litros_Diarios import Produccion_Leche_Litros_Diarios
from routes.Veterinaria import Veterinaria
from routes.registro_celos import registro_celos_rutas
from routes.Ganancia_historica_pesos import Ganancia_historica_rutas
from routes.Natalidad_y_Paricion_real import natalidad_paricion_real_rutas
from routes.Marcas_Bovinos import  Marcas_Bovinos
'''
CORS o "intercambio de recursos de origen cruzado"se refiere a las situaciones 
en las que una interfaz que se ejecuta en un navegador tiene código JavaScript que se comunica
 con un backend, y el backend tiene un "origen" diferente al de la interfaz.

'''
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "static")), name="static")

app.include_router(Endogamia)
app.include_router(rutas_bovinos)
app.include_router(Pruebas_Leche)
app.include_router(Pruebas_TotalAnimales)
app.include_router(Intervalo_Entre_Partos_Hato)
app.include_router(Inventarios)
app.include_router(Eliminar_Bovino)
app.include_router(Formulario_Bovino)
app.include_router(datos_compra)
app.include_router(pesaje)
app.include_router(Produccion_Leche)
app.include_router(Levante_Bovinos)
app.include_router(Muertes_Bovinos)
app.include_router(Ventas_Bovinos)
app.include_router(Curvas_Lantacia)
app.include_router(partos_bovinos)
app.include_router(IEP_Razas)
app.include_router(IntevaloPartos)
app.include_router(Produccion_Leche_Litros_Diarios)
app.include_router(Veterinaria)
app.include_router(Ceba_Bovinos)
app.include_router(ReproductorRutas)
app.include_router(Vientres_Aptos)
app.include_router(capacidad_carga_rutas)
app.include_router(bovinos_descarte)
app.include_router(Historial_Perdida_Terneros)
app.include_router(Pajillas)
app.include_router(appArchivos)
app.include_router(Palpaciones_Bovinos)
app.include_router(Historial_Tasa_Supervivencia)
app.include_router(registro_celos_rutas)
app.include_router(Ganancia_historica_rutas)
app.include_router(natalidad_paricion_real_rutas)
app.include_router(Marcas_Bovinos)



