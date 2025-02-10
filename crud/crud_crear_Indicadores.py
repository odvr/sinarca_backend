from typing import Any
from sqlalchemy import update,func
from sqlalchemy.orm import Session


from models.modelo_bovinos import modelo_indicadores, modelo_bovinos_inventario, modelo_leche


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

        # Combina consultas para reducir la cantidad de llamadas a la base de datos
        indicadores = db.query(
            modelo_indicadores.c.vacas_prenadas,
            modelo_indicadores.c.vacas_vacias,
            modelo_indicadores.c.vacas_en_ordeno,
            modelo_indicadores.c.vacas_no_ordeno
        ).filter(modelo_indicadores.c.id_indicadores == current_user).first()

        prenadas, vacias, ordeno, no_ordeno = indicadores

        # Calcula el porcentaje de vacas prenadas y en ordeño
        vacas_estado_pren = (prenadas / (prenadas + vacias) * 100) if prenadas and vacias else 0
        vacas_ordeno_porcentaje = (ordeno / (ordeno + no_ordeno) * 100) if ordeno or no_ordeno else 0

        # Actualiza los porcentajes calculados
        db.execute(
            update(modelo_indicadores)
            .where(modelo_indicadores.c.id_indicadores == current_user)
            .values(
                vacas_prenadas_porcentaje=vacas_estado_pren,
                porcentaje_ordeno=vacas_ordeno_porcentaje
            )
        )

        # Consulta y conteo de animales vivos que son ordenados y vacas vacías y preñadas
        vacas_ordeno = db.query(func.count()).select_from(
            modelo_bovinos_inventario
        ).join(
            modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino
        ).filter(
            modelo_bovinos_inventario.c.estado == 'Vivo',
            modelo_leche.c.ordeno == 'Si',
            modelo_leche.c.usuario_id == current_user,
            modelo_bovinos_inventario.c.usuario_id == current_user
        ).scalar()

        consulta_vacias = db.query(func.count()).select_from(
            modelo_bovinos_inventario
        ).join(
            modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino
        ).filter(
            modelo_bovinos_inventario.c.estado == 'Vivo',
            modelo_leche.c.datos_prenez == 'Vacia',
            modelo_leche.c.tipo_ganado != "Hembra de levante",
            modelo_leche.c.usuario_id == current_user
        ).scalar()

        consulta_prenadas = db.query(func.count()).select_from(
            modelo_bovinos_inventario
        ).join(
            modelo_leche, modelo_bovinos_inventario.c.id_bovino == modelo_leche.c.id_bovino
        ).filter(
            modelo_bovinos_inventario.c.estado == 'Vivo',
            modelo_leche.c.datos_prenez == 'Preñada',
            modelo_leche.c.usuario_id == current_user
        ).scalar()

        # Actualiza los campos calculados
        db.execute(
            update(modelo_indicadores)
            .where(modelo_indicadores.c.id_indicadores == current_user)
            .values(
                vacas_en_ordeno=vacas_ordeno,
                vacas_vacias=consulta_vacias,
                vacas_prenadas=consulta_prenadas
            )
        )

        # Confirma las transacciones
        db.commit()


crear_indicadores = Crear_Indicadores()