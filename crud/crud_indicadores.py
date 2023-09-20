from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session
from sqlalchemy import update
from models.modelo_bovinos import modelo_indicadores


class CRUDIndicadores:
    def __init__(self, model):
        self.model = model

    def get(self, db, id):
        return db.query(self.model).filter(self.model.id == id).first()

    def set_prop_milk(self, db, milk_count,current_user):
        stmt = update(self.model).where(self.model.c.id_indicadores == current_user).values(animales_leche=milk_count)
        db.execute(stmt)
        db.commit()
        db.close()

    def set_Cantidad_Total_Animales(self, db, CantidadAnimalesActuales,current_user):
        sstmt = update(self.model).where(self.model.c.id_indicadores == current_user).values(total_animales=CantidadAnimalesActuales)

        db.execute(sstmt)
        db.commit()
        db.close()


indicadores = CRUDIndicadores(modelo_indicadores)