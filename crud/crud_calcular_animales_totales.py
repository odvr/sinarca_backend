from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import   func
from sqlalchemy.orm import Session


from models.modelo_bovinos import modelo_bovinos_inventario

class CRUDcalcular_animales_totales:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = modelo_bovinos_inventario

    def get(self, db: Session, id: Any) -> Any:
        return db.query(self.model).filter(self.model.id == id).first()

    def ContarAnimalesCrud(self,db: Session):
        Contar = db.query(modelo_bovinos_inventario). \
        filter(modelo_bovinos_inventario.c.estado == "Vivo").count()

        db.close()
        return Contar



TotalBovinos = CRUDcalcular_animales_totales()