from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session


from models.modelo_bovinos import modelo_bovinos_inventario, modelo_registro_marca, modelo_registro_pajillas


class CRUDBovinos:
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

    def count_animals(self,db: Session,current_user):
        contar = db.query(modelo_bovinos_inventario).filter(modelo_bovinos_inventario.c.estado == "Vivo",
                                                   modelo_bovinos_inventario.c.proposito == "Leche",modelo_bovinos_inventario.c.usuario_id == current_user).count()
        db.close()
        return contar
    def Buscar_Nombre(self,db: Session,id_bovino, current_user):
        ConsultarNombre = db.query(modelo_bovinos_inventario).filter(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino,
            modelo_bovinos_inventario.c.usuario_id == current_user).first()
        if ConsultarNombre is None:
            return None
        else:
            Nombre_Bovino = ConsultarNombre.nombre_bovino
            db.close()
            return Nombre_Bovino
    def Buscar_Nombre_Pajilla(self,db: Session,Codigo_toro_pajilla, current_user):
        ConsultarNombre_pajilla = db.query(modelo_registro_pajillas).filter(
            modelo_registro_pajillas.columns.Codigo_toro_pajilla == Codigo_toro_pajilla,
            modelo_registro_pajillas.c.usuario_id == current_user).first()
        Nombre_Bovino_pajilla = ConsultarNombre_pajilla.nombre_toro
        db.close()
        return Nombre_Bovino_pajilla
    def Buscar_Ruta_Fisica_Marca(self,db: Session,id_registro_marca, current_user):
        BuscarRutaFisica = db.query(modelo_registro_marca).filter(
            modelo_registro_marca.columns.id_registro_marca == id_registro_marca,
            modelo_registro_marca.c.usuario_id == current_user).first()
        Ruta_Marca = BuscarRutaFisica.ruta_marca
        db.close()
        return Ruta_Marca

bovinos_inventario = CRUDBovinos()