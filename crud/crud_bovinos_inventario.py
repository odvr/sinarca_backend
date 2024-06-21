from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session



from models.modelo_bovinos import modelo_bovinos_inventario, modelo_registro_marca, modelo_registro_pajillas, \
    modelo_usuarios, modelo_lotes_bovinos


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

    def Buscar_Lote_Bovino(self,db: Session,id_bovino, current_user):
        """

        :param db:
        :param id_bovino:
        :param current_user:
        :return:  LoteAnimal

        Consulta el lote de animal
        """
        ConsultarLote = db.query(modelo_bovinos_inventario).filter(
            modelo_bovinos_inventario.columns.id_bovino == id_bovino,
            modelo_bovinos_inventario.c.usuario_id == current_user).first()
        if ConsultarLote is None:
            return None
        else:
            LoteAnimal = ConsultarLote.nombre_bovino
            db.close()
            return LoteAnimal



    def Buscar_ID_Nombre_Padre(self, db: Session, id_bovino_padre, current_user):
        ConsultarNombrePadre = db.query(modelo_registro_pajillas).filter(
            modelo_registro_pajillas.columns.Codigo_toro_pajilla == id_bovino_padre,
            modelo_registro_pajillas.c.usuario_id == current_user).first()
        if ConsultarNombrePadre is None:
            return None
        else:
            ID_BovinoPadre = ConsultarNombrePadre.id_pajillas
            db.close()
            return ID_BovinoPadre
    def Buscar_Nombre_Pajilla(self,db: Session,Codigo_toro_pajilla, current_user):
        ConsultarNombre_pajilla = db.query(modelo_registro_pajillas).filter(
            modelo_registro_pajillas.columns.id_pajillas == Codigo_toro_pajilla,
            modelo_registro_pajillas.c.usuario_id == current_user).first()
        Nombre_Bovino_pajilla = f'Pajilla {ConsultarNombre_pajilla.Codigo_toro_pajilla} ({(ConsultarNombre_pajilla.nombre_toro)})'
        db.close()
        return Nombre_Bovino_pajilla
    def Buscar_Ruta_Fisica_Marca(self,db: Session,id_registro_marca, current_user):

        try:
            BuscarRutaFisica = db.query(modelo_registro_marca).filter(
                modelo_registro_marca.columns.id_registro_marca == id_registro_marca,
                modelo_registro_marca.c.usuario_id == current_user).first()

            # Manejar el caso en que BuscarRutaFisica sea None
            if BuscarRutaFisica is None:
                return None  # o cualquier valor predeterminado que desees

            Ruta_Marca = BuscarRutaFisica.ruta_marca
            db.close()

            return Ruta_Marca
        except AttributeError as e:
            # Manejar la excepción de AttributeError

            return None  # o cualquier valor predeterminado que desees


    def Buscar_Ruta_Foto_Perfil(self,db: Session,id_bovino, current_user):

        try:
            BuscarRutaFisicaFotoPerfil = db.query(modelo_bovinos_inventario).filter(
                modelo_bovinos_inventario.columns.id_bovino == id_bovino,
                modelo_bovinos_inventario.c.usuario_id == current_user).first()

            # Manejar el caso en que BuscarRutaFisica sea None
            if BuscarRutaFisicaFotoPerfil is None:
                return None  # o cualquier valor predeterminado que desees

            Ruta_Marca = BuscarRutaFisicaFotoPerfil.ruta_fisica_foto_perfil
            db.close()

            return Ruta_Marca
        except AttributeError as e:
            # Manejar la excepción de AttributeError

            return None  # o cualquier valor predeterminado que desees


    def Buscar_Ruta_Foto_Marca(self,db: Session,id_registro_marca, current_user):

        try:
            BuscarRutaFisicaFotoMarca = db.query(modelo_registro_marca).filter(
                modelo_registro_marca.columns.id_registro_marca == id_registro_marca,
                modelo_registro_marca.c.usuario_id == current_user).first()

            # Manejar el caso en que BuscarRutaFisica sea None
            if BuscarRutaFisicaFotoMarca is None:
                return None

            Ruta_Marcas = BuscarRutaFisicaFotoMarca.ruta_marca
            db.close()

            return Ruta_Marcas
        except AttributeError as e:
            # Manejar la excepción de AttributeError

            return None


    def Buscar_Usuario_Conectado(self,db: Session, current_user):

        try:
            Buscar_Datos_usuario = db.query(modelo_usuarios).filter(
                modelo_usuarios.c.usuario_id == current_user).all()

            # Manejar el caso en que Buscar_Datos_usuario sea None
            if Buscar_Datos_usuario is None:
                return None  # o cualquier valor predeterminado que desees


            db.close()

            return Buscar_Datos_usuario
        except AttributeError as e:
            # Manejar la excepción de AttributeError

            return None  # o cualquier valor predeterminado que desees


    def VerificarConsultaDatosFotoPerfilBovino(self,Buscar_Datos_Foto_Perfil,Rutabase):
        if not Buscar_Datos_Foto_Perfil:
            Consulta = "ConsultaVacia"
            return Consulta
        else:
            RutasUnidas = Rutabase + Buscar_Datos_Foto_Perfil

            return RutasUnidas

    def ActualizarCantidadAnimalesEnLote(self,db,current_user):

        """

        :param db:
        :param current_user:
        :return:
        """
        ConsultarNombreLote = db.query(modelo_lotes_bovinos).filter(
            modelo_lotes_bovinos.c.usuario_id == current_user).all()

        for Consulta in ConsultarNombreLote:
            ContarAnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == Consulta.nombre_lote,
                       modelo_bovinos_inventario.c.usuario_id == current_user).count()
            db.execute(modelo_lotes_bovinos.update().values(total_bovinos=ContarAnimalesLote).where(
                modelo_lotes_bovinos.c.id_lote_bovinos == Consulta.id_lote_bovinos,
                modelo_bovinos_inventario.c.usuario_id == current_user))
            db.commit()
            db.close()



bovinos_inventario = CRUDBovinos()