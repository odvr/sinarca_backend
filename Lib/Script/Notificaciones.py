import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Importación de Funciones para Notificar
from Lib.Cambiar_Estado_Facturas import CambiarEstadoFactura


CambiarEstadoFactura()

