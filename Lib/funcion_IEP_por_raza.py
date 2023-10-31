'''
Librerias requeridas

@autor : odvr

'''

import logging


from fastapi import APIRouter


# importa el esquema de los bovinos
from models.modelo_bovinos import modelo_bovinos_inventario,  modelo_leche,modelo_indicadores, modelo_orden_IEP
from sqlalchemy.orm import Session
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

"""la siguiente funcion determina la diferencia que existe
entre el intervalo entre partos promedio de un animal con el 
 intervalo entre partos de la raza de dicho animal, esto con
  el fin de mostrar cuales son los animales mejores en terminos de
  su raza"""

def IEP_por_raza(session: Session,current_user):
    try:
       # la siguiente consulta trae el listado de razas de los animales en el modulo de leche
       razas_IEP_leche = list(set(session.query(modelo_bovinos_inventario.c.raza). \
                join(modelo_leche,modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()))
       # para calcular los IEP y animales por raza se implementa un bucle
       contador_raza = len(razas_IEP_leche)
       b = 0
       while (b < contador_raza):
           raza_a_trabajar = razas_IEP_leche[b][0]
           consulta_IEP_prom_raza = session.query(func.avg(modelo_leche.columns.intervalo_entre_partos),
                                    modelo_bovinos_inventario.c.raza).join(modelo_leche,
                                    modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
               where(modelo_leche.columns.intervalo_entre_partos>0).\
               filter(modelo_bovinos_inventario.columns.raza == raza_a_trabajar,
               modelo_bovinos_inventario.columns.estado=="Vivo",
               modelo_bovinos_inventario.c.usuario_id==current_user).all()
           if consulta_IEP_prom_raza==[] or consulta_IEP_prom_raza is None:
               pass
           else:
               animales_IEP_leche = session.query(modelo_bovinos_inventario.c.raza, modelo_leche.c.id_bovino,
                                                  modelo_leche.c.intervalo_entre_partos,
                                                  modelo_bovinos_inventario.c.estado,
                                                  modelo_bovinos_inventario.c.nombre_bovino). \
                   join(modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino).\
                   filter(modelo_bovinos_inventario.c.usuario_id==current_user).all()
               # recorre el bucle
               for i in animales_IEP_leche:
                   # Toma el ID del bovino, este es el campo numero 1
                   id_bovino_IEP = i[1]
                   # Toma el promedio de litros de un animal, este es el campo numero 2
                   promedio_IEP_bovino = i[2]
                   # Toma la raza del bovino, este es el campo numero 0
                   raza_bovino_IEP = i[0]
                   # Toma la estado del bovino, este es el campo numero 3
                   estado_bovino_IEP = i[3]
                   # Toma el nombre del bovino, este es el campo numero 4
                   nombre_bovino_IEP = i[4]
                   if promedio_IEP_bovino <= 0:
                       session.execute(modelo_orden_IEP.delete(). \
                                       where(modelo_orden_IEP.c.id_bovino == id_bovino_IEP))
                       session.commit()
                   elif estado_bovino_IEP != "Vivo":
                       session.execute(modelo_orden_IEP.delete(). \
                                       where(modelo_orden_IEP.c.id_bovino == id_bovino_IEP))
                       session.commit()
                   elif raza_bovino_IEP==raza_a_trabajar:
                       diferencia = promedio_IEP_bovino - consulta_IEP_prom_raza[0][0]
                       # consulta para saber si el bovino existe
                       consulta_existencia_bovino = session.query(modelo_orden_IEP). \
                           filter(modelo_orden_IEP.columns.id_bovino == id_bovino_IEP).all()
                       # si la consulta es vacia significa que no existe ese animal en la tabla,
                       # entonces ese animal sera insertado
                       if consulta_existencia_bovino == []:
                           ingresoDatos = modelo_orden_IEP.insert().values(id_bovino=id_bovino_IEP,
                                                                           raza=raza_bovino_IEP,
                                                                           intervalo_promedio_raza=
                                                                           consulta_IEP_prom_raza[0][0],
                                                                           intervalo_promedio_animal=promedio_IEP_bovino,
                                                                           diferencia=diferencia,
                                                                           nombre_bovino=nombre_bovino_IEP)

                           session.execute(ingresoDatos)
                           session.commit()
                       # si el animal existe entonces actualiza sus datos
                       else:
                           session.execute(modelo_orden_IEP.update().values(id_bovino=id_bovino_IEP,
                                                                            raza=raza_bovino_IEP,
                                                                            intervalo_promedio_raza=
                                                                            consulta_IEP_prom_raza[0][0],
                                                                            intervalo_promedio_animal=promedio_IEP_bovino,
                                                                            diferencia=diferencia,
                                                                            nombre_bovino=nombre_bovino_IEP).where(
                               modelo_orden_IEP.columns.id_bovino == id_bovino_IEP))
                           session.commit()

           b=b+1

       # el siguiente codigo permite eliminar cualquier animal que no este en el modulo de leche
       consulta_animales_IEP = session.query(modelo_orden_IEP.c.id_bovino).\
           filter(modelo_orden_IEP.c.usuario_id==current_user).all()
       # recorre el bucle
       for i in consulta_animales_IEP:
           # Toma el ID del bovino, este es el campo numero 1
           id_bov = i[0]
           consulta_existencia_en_leche = session.query(modelo_leche). \
               filter(modelo_leche.columns.id_bovino == id_bov).all()
           if consulta_existencia_en_leche==[] or consulta_existencia_en_leche is None:
               session.execute(modelo_orden_IEP.delete(). \
                               where(modelo_orden_IEP.c.id_bovino == id_bov))
               session.commit()
           else:
               pass
       #el siguiente codigo calcula un valor de IEP general del hato
       consulta_IEP_prom_hato = session.query(func.avg(modelo_leche.columns.intervalo_entre_partos),
                                modelo_bovinos_inventario.c.estado).join(modelo_leche,
                                modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino). \
           where(modelo_leche.columns.intervalo_entre_partos > 0). \
           filter(modelo_bovinos_inventario.columns.estado == "Vivo",
                  modelo_bovinos_inventario.c.usuario_id==current_user).all()
       if consulta_IEP_prom_hato is None or consulta_IEP_prom_hato[0][0]==0:
           pass
       else:
           session.execute(modelo_indicadores.update().
                           values(IEP_hato=consulta_IEP_prom_hato[0][0]).
                           where(modelo_indicadores.columns.id_indicadores == current_user))
           session.commit()

       logger.info(f'Funcion IEP_por_raza')
       session.commit()
    except Exception as e:
        logger.error(f'Error Funcion IEP_por_raza: {e}')
        raise
    finally:
        session.close()