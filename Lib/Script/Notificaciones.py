
"""

import sys
import os

from Lib.Lib_notificacion_palpaciones_partos import notificacion_proximidad_parto

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Importación de Funciones para Notificar
from Lib.Cambiar_Estado_Facturas import CambiarEstadoFactura


CambiarEstadoFactura()
notificacion_proximidad_parto()


"""
import schedule
import time
import threading

def mi_funcion():
    print("Ejecutando función...")

def ejecutar_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Revisar cada 60 segundos

# Programar la función para ejecutarse cada minuto
schedule.every(1).minutes.do(mi_funcion)

# Iniciar `schedule` en un hilo separado
thread = threading.Thread(target=ejecutar_schedule, daemon=True)
thread.start()

# Aquí continúa la ejecución normal de Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mi_app:app", host="0.0.0.0", port=8000, reload=True)