"""
Autor: odvr
Modificación:

La siguiente función realiza el calculo para realizar el pago de la Nomina

"""

#Librerias requeridas
from datetime import datetime

import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import desc
from fastapi import  Depends
# importa la conexion de la base de datos
from config.db import   get_session
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_nomina, modelo_empleados

def calcular_nomina(empleado_id,current_user,db):
    """
    :param empleado_id:E
    :param current_user:
    :param db:
    :return:
    """
    # La siguiente Consulta Realiza la Busqueda del Ultimo  en la tabla de nomiona
    ultimo_pago  = db.query(modelo_nomina.c.fecha_pago).filter(
        modelo_nomina.c.usuario_id == current_user,
        modelo_nomina.c.empleado_id == empleado_id
    ).first()
    # La validación de fecha de ingreso en caso dado que no exista una fecha de ultimo pago con esto tomará el primer día para los pagos
    fecha_ingreso = db.query(modelo_empleados.c.fecha_contratacion).filter(modelo_empleados.c.usuario_id == current_user,
                                                       modelo_empleados.c.empleado_id == empleado_id).first()
    salario_base = db.query(modelo_empleados.c.salario_base).filter(modelo_empleados.c.usuario_id == current_user,
                                                       modelo_empleados.c.empleado_id == empleado_id).first()
    #La Fecha actual para calcular las fechas de pafpgo y de corte de nomina
    fecha_actual = datetime.now().date()
    if not ultimo_pago:
        # Si es un nuevo empleado, usamos la fecha de ingreso
        ultimo_pago = fecha_ingreso
    # Calcular días trabajados desde el último pago
    dias_trabajados = (fecha_actual - ultimo_pago[0]).days
    dias_en_mes = 30  # Asumimos meses de 30 días para el cálculo
    # Calcular salario proporcional según días trabajados
    salario_proporcional = (salario_base[0] / dias_en_mes) * dias_trabajados

    """
    #Aplicar deducciones
    salario_neto = salario_proporcional - deducciones
    return salario_neto
    
    """




