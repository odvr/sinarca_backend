from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session


from models.modelo_bovinos import modelo_bovinos_inventario, modelo_indicadores, modelo_capacidad_carga


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
    def Crear_indicadores_capacidad_carga(self, db: Session, current_user):
        ingreso = modelo_capacidad_carga.insert().values(id_capacidad=current_user )
        db.commit()
        db.close()
        return ingreso




crear_indicadores = Crear_Indicadores()