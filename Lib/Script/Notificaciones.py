import sys
import os

from Lib.Lib_notificacion_palpaciones_partos import notificacion_proximidad_parto

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Importación de Funciones para Notificar
from Lib.Cambiar_Estado_Facturas import CambiarEstadoFactura


CambiarEstadoFactura()
notificacion_proximidad_parto()
