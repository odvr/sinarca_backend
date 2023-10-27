"""

@autor : odvr

"""

from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from models.modelo_bovinos import modelo_bovinos_inventario, modelo_datos_muerte, modelo_ventas
import logging
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

def calculoEdad(db: Session ):
 try:
    # Realiza la consulta general de la tabla de bovinos
    consulta_fecha_nacimiento = db.execute(modelo_bovinos_inventario.select()).fetchall()
    #Recorre los campos de la consulta
    for i in consulta_fecha_nacimiento:
        #Toma el ID del bovino para calcular la edad el campo numero 0
        id = i[0]
        # Toma la fecha de nacimiento del animal en este caso es el campo 1
        fecha_nacimiento = i[1]
        # Toma el estado del animal en este caso es el campo 9
        estado = i[9]
        #
        if estado=="Vivo":
            # realiza el calculo correspondiente para calcular los meses entre fechas (edad del animal)
            Edad_Animal = (datetime.today().year - fecha_nacimiento.year) * 12 + datetime.today().month - fecha_nacimiento.month
            # actualizacion del campo en la base de datos tomando la variable ID
            db.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
                modelo_bovinos_inventario.columns.id_bovino == id))

            db.commit()


        elif estado == "Vendido":
            fecha_venta = list(db.execute(modelo_ventas.select().
                                           where(modelo_ventas.columns.id_bovino == id)).first())
            if fecha_venta is None or fecha_venta==[]:
                pass
            else:
                # realiza el calculo correspondiente para calcular los meses entre fechas (edad del animal)
                Edad_Animal = (fecha_venta[4].year - fecha_nacimiento.year) * 12 + (
                            fecha_venta[4].month - fecha_nacimiento.month)
                # actualizacion del campo en la base de datos tomando la variable ID
                db.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
                    modelo_bovinos_inventario.columns.id_bovino == id))

                db.commit()

        elif estado=="Muerto":
               fecha_muerte = list(db.execute(modelo_datos_muerte.select().
                                   where(modelo_datos_muerte.columns.id_bovino == id)).first())
               if fecha_muerte is None or fecha_muerte==[]:
                   pass
               else:
                   # realiza el calculo correspondiente para calcular los meses entre fechas (edad del animal)
                   Edad_Animal = (fecha_muerte[4].year - fecha_nacimiento.year) * 12 + (
                               fecha_muerte[4].month - fecha_nacimiento.month)
                   # actualizacion del campo en la base de datos tomando la variable ID
                   db.execute(modelo_bovinos_inventario.update().values(edad=Edad_Animal).where(
                       modelo_bovinos_inventario.columns.id_bovino == id))

                   db.commit()



 except Exception as e:
     logger.error(f'Error Funcion calculo Edad: {e}')
     raise
 finally:
    db.close()