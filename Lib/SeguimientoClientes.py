"""
Autor: odvr
Fecha Modificación: 26/02/2025
La siguiente libreria se implementará para realizar seguimiento a los clientes
"""

# Librerías
from sqlalchemy.orm import Session
import crud.crud_bovinos_inventario
from Lib.enviar_correos import enviar_correo
from config.db import get_session
from models.modelo_bovinos import modelo_facturas
from datetime import datetime


def EnviarSeguimientoClientes():
    pass