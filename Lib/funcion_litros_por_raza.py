'''
Librerias requeridas

@autor : odvr

'''

import logging
from fastapi import APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

# importa la conexion de la base de datos
# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario,modelo_leche, modelo_orden_litros

from sqlalchemy import  func



# Configuracion de las rutas para fash api
rutas_bovinos = APIRouter()

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
#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#from twilio.rest import Client


def litros_por_raza(session:Session,current_user):
    try:
        #la siguiente consulta trae el listado de razas de los animales en el modulo de leche
        razas_litros_leche = list(set(session.query(modelo_bovinos_inventario.c.raza). \
            join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()))
        #para calcular los litros y animales por raza se implementa un bucle
        contador_raza= len(razas_litros_leche)
        b=0
        while(b<contador_raza):
            raza_a_trabajar=razas_litros_leche[b][0]
            #consulta de litros promedio por raza
            consulta_litros_prom_raza = session.query(func.avg(modelo_leche.columns.promedio_litros),
                                                      modelo_bovinos_inventario.c.estado).\
                join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
                where(modelo_leche.columns.promedio_litros>0).\
                filter(modelo_bovinos_inventario.columns.raza==raza_a_trabajar,
                       modelo_bovinos_inventario.columns.estado=="Vivo",
                       modelo_bovinos_inventario.c.usuario_id==current_user).all()

            if consulta_litros_prom_raza is None or consulta_litros_prom_raza==[]:
                pass
            else:
                animales_litros_leche = session.query(modelo_bovinos_inventario.c.raza, modelo_leche.c.id_bovino,
                                                      modelo_leche.c.promedio_litros, modelo_bovinos_inventario.c.estado,
                                                      modelo_bovinos_inventario.c.nombre_bovino). \
                    join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
                    filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()
                # recorre el bucle
                for i in animales_litros_leche:
                    # Toma el ID del bovino, este es el campo numero 1
                    id_bovino_litros = i[1]
                    # Toma el promedio de litros de un animal, este es el campo numero 2
                    promedio_litros_bovino = i[2]
                    # Toma la raza del bovino, este es el campo numero 0
                    raza_bovino_litros = i[0]
                    # Toma el estado del bovino, este es el campo numero 3
                    estado_bovino_litros = i[3]
                    # Toma el nombre del bovino, este es el campo numero 4
                    nombre_bovino_litros = i[4]

                    if promedio_litros_bovino is None or promedio_litros_bovino == 0:
                        session.execute(modelo_orden_litros.delete().
                                        where(modelo_orden_litros.c.id_bovino == id_bovino_litros))
                        session.commit()

                    elif estado_bovino_litros!="Vivo":
                        session.execute(modelo_orden_litros.delete().
                                        where(modelo_orden_litros.c.id_bovino == id_bovino_litros))
                        session.commit()

                    else:
                        if raza_bovino_litros==raza_a_trabajar:
                            diferencia = promedio_litros_bovino - consulta_litros_prom_raza[0][0]
                            # consulta para saber si el bovino existe
                            consulta_existencia_bovino = session.query(modelo_orden_litros). \
                                filter(modelo_orden_litros.columns.id_bovino == id_bovino_litros).all()
                            # si la consulta es vacia significa que no existe ese animal en la tabla,
                            # entonces ese animal sera insertado
                            if consulta_existencia_bovino == []:
                                ingresoDatos = modelo_orden_litros.insert().values(id_bovino=id_bovino_litros,
                                                                                   raza=raza_bovino_litros,
                                                                                   litros_promedio_raza=
                                                                                   consulta_litros_prom_raza[0][0],
                                                                                   litros_promedio_animal=promedio_litros_bovino,
                                                                                   diferencia=diferencia,
                                                                                   nombre_bovino=nombre_bovino_litros,
                                                                                   usuario_id=current_user)

                                session.execute(ingresoDatos)
                                session.commit()
                            # si el animal existe entonces actualiza sus datos
                            else:
                                session.execute(modelo_orden_litros.update().values(id_bovino=id_bovino_litros,
                                                                                    raza=raza_bovino_litros,
                                                                                    litros_promedio_raza=
                                                                                    consulta_litros_prom_raza[0][0],
                                                                                    litros_promedio_animal=promedio_litros_bovino,
                                                                                    diferencia=diferencia,
                                                                                    nombre_bovino=nombre_bovino_litros,
                                                                                    usuario_id=current_user). \
                                                where(modelo_orden_litros.columns.id_bovino == id_bovino_litros))
                                session.commit()
            b=b+1

            # el siguiente codigo permite eliminar cualquier animal que no este en el modulo de leche
            consulta_animales_litros = session.query(modelo_orden_litros.c.id_bovino).all()
            # recorre el bucle
            for i in consulta_animales_litros:
                # Toma el ID del bovino, este es el campo numero 1
                id_bov = i[0]
                consulta_existencia_en_leche = session.query(modelo_leche). \
                    filter(modelo_leche.columns.id_bovino == id_bov).all()
                if consulta_existencia_en_leche == [] or consulta_existencia_en_leche is None:
                    session.execute(modelo_orden_litros.delete(). \
                                    where(modelo_orden_litros.c.id_bovino == id_bov))
                    session.commit()
                else:
                    pass

        logger.info(f'Funcion litros_por_raza {"p"} ')
        session.commit()
    except Exception as e:
        logger.error(f'Error Funcion litros_por_raza: {e}')
        raise
    finally:
        session.close()
