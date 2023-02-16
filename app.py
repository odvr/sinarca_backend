from fastapi import FastAPI
from routes.inventarios import rutas_bovinos
app = FastAPI()
app.include_router(rutas_bovinos)