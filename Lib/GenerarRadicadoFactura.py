from datetime import datetime
import os
from config.db import Rutabase

# Ruta al archivo donde se guardará el contador
archivo_contador = Rutabase+'/Lib/Plantillas/contador_radicado.txt'

def cargar_contador():
    """Carga el contador desde el archivo, si existe, o lo inicializa en 0."""
    if os.path.exists(archivo_contador):
        with open(archivo_contador, "r") as f:
            return int(f.read().strip())
    return 0

def guardar_contador(contador):
    """Guarda el contador en el archivo."""
    with open(archivo_contador, "w") as f:
        f.write(str(contador))

def generar_radicado():
    global contador_radicados

    # Cargar el contador desde el archivo
    contador_radicados = cargar_contador()

    # Incrementar el contador
    contador_radicados += 1

    # Obtener el año actual
    año_vigente = datetime.now().year

    # Formatear el radicado con el año y el contador
    radicado = f"{año_vigente}{contador_radicados:05d}"

    # Guardar el nuevo contador
    guardar_contador(contador_radicados)

    return radicado