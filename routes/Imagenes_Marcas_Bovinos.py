'''
Librerias requeridas
'''
import base64
import logging
import uuid
from Lib.actualizacion_peso import actualizacion_peso
from Lib.funcion_peso_por_raza import peso_segun_raza
# # importa la conexion de la base de datos
from config.db import get_session
from sqlalchemy.orm import Session
# # importa el esquema de los bovinos
from models.modelo_bovinos import modelo_datos_pesaje, modelo_orden_peso
from fastapi import APIRouter, Response
from starlette.status import HTTP_204_NO_CONTENT
from fastapi import  status, HTTPException, Depends
import os
from sqlalchemy import func
from datetime import date, datetime, timedelta
from fastapi import  Depends
from routes.rutas_bovinos import get_current_user
from schemas.schemas_bovinos import esquema_modelo_Reporte_Pesaje, esquema_orden_peso, Esquema_Usuario

# Configuracion de la libreria para los logs de sinarca
# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Crea un manejador de archivo para guardar el log
log_file = 'Log_Sinarca.log'
file_handler = logging.FileHandler(log_file)
# Define el formato del log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Agrega el manejador de archivo al logger
logger.addHandler(file_handler)

Imagenes_Marca = APIRouter()
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()





def guardar_imagen_en_archivo(imagen_base64):
    # Directorio donde se guardarán las imágenes
    directorio = "Marcas"

    # Crea el directorio si no existe
    os.makedirs(directorio, exist_ok=True)

    # Genera un nombre de archivo único
    nombre_archivo = f"marca_{uuid.uuid4().hex}.png"

    # Guarda la imagen en el sistema de archivos
    with open(os.path.join(directorio, nombre_archivo), "wb") as archivo:
        archivo.write(base64.b64decode(imagen_base64))

    # Devuelve la ruta del archivo
    return os.path.join(directorio, nombre_archivo)

def guardar_marca_en_base_de_datos(ruta_archivo):
    nueva_firma = Firma(ruta_archivo=ruta_archivo)
    session.add(nueva_firma)
    session.commit()

@Imagenes_Marca.post("/guardar_firma/")
async def guardar_firma(Marca_Bovino: str, db: Session = Depends(get_database_session),current_user: Esquema_Usuario = Depends(get_current_user)):
    try:
        # Directorio donde se guardarán las imágenes
        directorio = "Marcas"
        # Guardar la imagen en el sistema de archivos
        nombre_archivo = f"Marca_{uuid.uuid4().hex}.png"
        ruta_archivo = os.path.join(directorio, nombre_archivo)
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(base64.b64decode(Marca_Bovino.imagen))

        # Guardar la referencia en la base de datos

        nueva_firma= db.execute(modelo_bovinos_inventario.update().where(modelo_bovinos_inventario.c.id_bovino == id_bovino).values(
            proposito=proposito))

        db.add(nueva_firma)
        db.commit()

        return {"mensaje": "Firma guardada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))