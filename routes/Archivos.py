
import os
import uuid
from fastapi import APIRouter, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

appArchivos = APIRouter()

# Ruta para servir los archivos estáticos
#appArchivos.mount("/static", StaticFiles(directory='../static'), name="static")


# Ruta para servir los archivos estáticos
#static_folder = os.path.join(os.path.dirname(__file__), "static")
#static_folder = os.path.join(os.path.dirname(__file__), "static")

print(os.getcwd())
appArchivos.mount("/static", StaticFiles(directory=r"./static"), name="static")








async def create_user_profile(file: UploadFile = File(...)):
    contents = await file.read()
    # Obtiene el nombre del archivo sin la extensión
    filename, file_extension = os.path.splitext(file.filename)
    new_filename = f"{filename}_{uuid.uuid4().hex}{file_extension}"
    # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original

    # Ruta donde guardar el archivo
    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, new_filename)

    # Guarda el archivo en la ubicación deseada
    with open(file_path, "wb") as f:
        f.write(contents)

    # Devuelve la URL del archivo para que el usuario pueda acceder a él
    file_url = f"static/uploads/{new_filename}"
    return {"filename": new_filename, "file_url": file_url}


@appArchivos.post("/Guardar/FotoPerfil")
async def create_user_profile(file: UploadFile = File(...)):
    contents = await file.read()
    # Obtiene el nombre del archivo sin la extensión
    filename, file_extension = os.path.splitext(file.filename)
    new_filename = f"{filename}_{uuid.uuid4().hex}{file_extension}"
    # Genera un nuevo nombre de archivo único agregando un identificador único (UUID) al nombre original

    # Ruta donde guardar el archivo
    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, new_filename)

    # Guarda el archivo en la ubicación deseada
    with open(file_path, "wb") as f:
        f.write(contents)

    # Devuelve la URL del archivo para que el usuario pueda acceder a él
    file_url = f"/static/uploads/{new_filename}"
    return {"filename": new_filename, "file_url": file_url}


@appArchivos.get("/users/profile/{filename}")
async def get_user_profile(filename: str):
    file_path = os.path.join("static", "uploads", filename)
    return FileResponse(file_path)