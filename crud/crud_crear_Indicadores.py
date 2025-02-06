from typing import Any
from sqlalchemy import update
from sqlalchemy.orm import Session


from models.modelo_bovinos import  modelo_indicadores


class Crear_Indicadores:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = modelo_indicadores

    def get(self, db: Session, id: Any) -> Any:
        return db.query(self.model).filter(self.model.id == id).first()

    def Crear_indicadores_db(self, db: Session, current_user):
        ingreso = modelo_indicadores.insert().values(id_indicadores=current_user )
        db.commit()
        db.close()
        return ingreso

    def Cargar_Indicadores_Gestion(self, db: Session, current_user):
        """
        Carga y actualiza los indicadores de gestión para el usuario actual en la base de datos.

        :param db: Sesión de la base de datos.
        :param current_user: Usuario actual.
        """

        # Consulta de vacas prenadas y vacas vacías en la base de datos
        prenadas, vacias = db.query(modelo_indicadores.c.vacas_prenadas, modelo_indicadores.c.vacas_vacias). \
            filter(modelo_indicadores.c.id_indicadores == current_user).first()
        ordeno, no_ordeno = db.query(modelo_indicadores.c.vacas_en_ordeno, modelo_indicadores.c.vacas_no_ordeno). \
            filter(modelo_indicadores.c.id_indicadores == current_user).first()

        # Actualización del porcentaje de vacas prenadas
        vacas_estado_pren = 0
        if prenadas is not None and vacias is not None and prenadas != 0:
            totales = prenadas + vacias
            vacas_estado_pren = (prenadas / totales) * 100

        db.execute(update(modelo_indicadores).
                   where(modelo_indicadores.c.id_indicadores == current_user).
                   values(vacas_prenadas_porcentaje=vacas_estado_pren))
        db.commit()
        # Actualización del porcentaje de vacas en ordeño
        vacas_ordeno_porcentaje = 0
        if ordeno is not None and no_ordeno is not None and (ordeno != 0 or no_ordeno != 0):
            vacas_ordeno_porcentaje = (ordeno / (ordeno + no_ordeno)) * 100

        db.execute(update(modelo_indicadores).
                   where(modelo_indicadores.c.id_indicadores == current_user).
                   values(porcentaje_ordeno=vacas_ordeno_porcentaje))

        # Confirmar las transacciones
        db.commit()

crear_indicadores = Crear_Indicadores()