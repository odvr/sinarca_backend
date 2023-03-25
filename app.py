from fastapi import FastAPI
from routes.rutas_bovinos import rutas_bovinos



from fastapi.middleware.cors import CORSMiddleware

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