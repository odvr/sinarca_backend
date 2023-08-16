from fastapi import FastAPI

from routes.Datos_Compra import datos_compra
from routes.Historial_Perdida_Terneros import  Historial_Perdida_Compras
#from routes.Archivos import appArchivos
from routes.Pesaje import pesaje
from routes.Prod_leche import Produccion_Leche
from routes.Registro_Litros_Diarios import Produccion_Leche_Litros_Diarios
from routes.Reproductor import ReproductorRutas
from routes.Vientres_Aptos_Routes import Vientres_Aptos
from routes.rutas_bovinos import rutas_bovinos
from routes.PartosAnimales import partos_bovinos
from routes.IEP_Razas import IEP_Razas
from routes.Capacidad_Carga import capacidad_carga_rutas
from routes.levante import levante
from routes.IntevaloPartos import IntevaloPartos
from routes.Veterinaria import Veterinaria
from fastapi.middleware.cors import CORSMiddleware
from routes.Eliminar_Bovino import Eliminar_Bovino
from routes.Intervalo_Entre_Partos_Hato import Intervalo_Entre_Partos_Hato

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


app.include_router(rutas_bovinos)
app.include_router(partos_bovinos)
app.include_router(IEP_Razas)
app.include_router(Produccion_Leche)
app.include_router(Produccion_Leche_Litros_Diarios)
app.include_router(Vientres_Aptos)
app.include_router(capacidad_carga_rutas)
app.include_router(pesaje)
app.include_router(levante)
app.include_router(IntevaloPartos)
app.include_router(Veterinaria)
app.include_router(ReproductorRutas)
app.include_router(Eliminar_Bovino)
app.include_router(datos_compra)
app.include_router(Historial_Perdida_Compras)
app.include_router(Intervalo_Entre_Partos_Hato)

#app.include_router(appArchivos)





