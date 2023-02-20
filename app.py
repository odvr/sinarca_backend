from fastapi import FastAPI
from routes.inventarios import rutas_bovinos
from routes.Funciones_Sinarca.Funciones_S import funciones_bovinos
app = FastAPI()

app.include_router(funciones_bovinos)