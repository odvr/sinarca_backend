from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.orm import Session

import logging

from models.modelo_bovinos import modelo_bovinos_inventario, modelo_registro_marca, modelo_registro_pajillas, \
    modelo_usuarios, modelo_lotes_bovinos, modelo_manejo_ternero_recien_nacido_lotes, modelo_eventos_asociados_lotes, \
    modelo_descorne_lotes, modelo_control_parasitos_lotes, modelo_registro_vacunas_bovinos, \
    modelo_control_podologia_lotes

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

    def CrearPlanSanidadRecienNacidosBovinos(self,nombre_lote_asociado,estado_respiratorio_inicial_lote,fecha_desinfeccion_lote,producto_usado_lote,metodo_aplicacion_lote,notificar_evento_lote,FechaNotificacion, db,current_user):
        """
        Realiza la creación de planes sanitario solamente para los parametros de Recien Nacidos
        :param nombre_lote_asociado:
        :param estado_respiratorio_inicial_lote:
        :param fecha_desinfeccion_lote:
        :param producto_usado_lote:
        :param metodo_aplicacion_lote:
        :param notificar_evento_lote:
        :param db:
        :param current_user:
        :return:
        """


        try:
            #La siguiente consulta trae la información de la tabla de inventario de los animales asociados al Lote
            AnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == nombre_lote_asociado,
                       modelo_bovinos_inventario.c.usuario_id == current_user).all()

            IngresarEventos = modelo_eventos_asociados_lotes.insert().values(

                nombre_lote=nombre_lote_asociado,
                nombre_evento="Manejo del Ternero Recién Nacido",
                estado_evento="Activo",
                FechaNotificacion=FechaNotificacion,

                usuario_id=current_user

            )

            db.execute(IngresarEventos)
            db.commit()

            for IDAnimales in AnimalesLote:
                ListadoIDBovino = IDAnimales.id_bovino
                NombreBovino = IDAnimales.nombre_bovino

                # La siguiente variable contiene el estado de la solicitud de la tabla
                Estado="Activo"
                #Consulta si El animal ya existe para actualizar o crear el campo dentro de la tabla
                ConsultaIDExiste = db.execute(
                    modelo_manejo_ternero_recien_nacido_lotes.select().where(
                        modelo_manejo_ternero_recien_nacido_lotes.columns.id_bovino == ListadoIDBovino)).first()
                if ConsultaIDExiste is None:
                    IngresarPlanSanidadLotes = modelo_manejo_ternero_recien_nacido_lotes.insert().values(
                        estado_solicitud_recien_nacido=Estado,
                        id_bovino=ListadoIDBovino,
                        nombre_bovino=NombreBovino,
                        estado_respiratorio_inicial_lote=estado_respiratorio_inicial_lote,
                        fecha_desinfeccion_lote=fecha_desinfeccion_lote, nombre_lote_asociado=nombre_lote_asociado,
                        producto_usado_lote=producto_usado_lote,
                        metodo_aplicacion_lote=metodo_aplicacion_lote, notificar_evento_lote=notificar_evento_lote,
                        usuario_id=current_user

                    )

                    db.execute(IngresarPlanSanidadLotes)
                    db.commit()
                else:
                    db.execute(modelo_manejo_ternero_recien_nacido_lotes.update().where(modelo_manejo_ternero_recien_nacido_lotes.c.id_bovino == ListadoIDBovino).values(
                        nombre_bovino=NombreBovino,
                        estado_solicitud_recien_nacido=Estado,
                        estado_respiratorio_inicial_lote=estado_respiratorio_inicial_lote,
                        fecha_desinfeccion_lote=fecha_desinfeccion_lote, nombre_lote_asociado=nombre_lote_asociado,
                        producto_usado_lote=producto_usado_lote,
                        metodo_aplicacion_lote=metodo_aplicacion_lote, notificar_evento_lote=notificar_evento_lote,))
                    db.commit()


        except Exception as e:
            logger.error(f'Error al Registrar Manejo de Terneros Recien Nacidos: {e}')
            raise


    def CrearPlanSanidadDescorne (self,nombre_lote_asociado,metodo_descorne,fecha_descorne,comentario_descorne, db,current_user):

        """
        Realiza la cración de planes de sanidad referentes al Descorne de los Animales


        :param nombre_lote_asociado:
        :param metodo_descorne:
        :param fecha_descorne:
        :param comentario_descorne:
        :param db:
        :param current_user:
        :return:
        """

        try:
            #La siguiente consulta trae la información de la tabla de inventario de los animales asociados al Lote
            AnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == nombre_lote_asociado,
                       modelo_bovinos_inventario.c.usuario_id == current_user).all()

            IngresarEventos = modelo_eventos_asociados_lotes.insert().values(

                nombre_lote=nombre_lote_asociado,
                nombre_evento="Descorne",
                estado_evento="Activo",
                usuario_id=current_user

            )

            db.execute(IngresarEventos)
            db.commit()

            for IDAnimales in AnimalesLote:
                ListadoIDBovino = IDAnimales.id_bovino
                NombreBovino = IDAnimales.nombre_bovino

                # La siguiente variable contiene el estado de la solicitud de la tabla
                Estado="Activo"
                #Consulta si El animal ya existe para actualizar o crear el campo dentro de la tabla
                ConsultaIDExiste = db.execute(
                    modelo_descorne_lotes.select().where(
                        modelo_descorne_lotes.columns.id_bovino == ListadoIDBovino)).first()
                if ConsultaIDExiste is None:
                    IngresarPlanSanidadLotesDescorne = modelo_descorne_lotes.insert().values(
                        estado_solicitud_descorne=Estado,
                        id_bovino=ListadoIDBovino,
                        nombre_bovino=NombreBovino,
                        nombre_lote_asociado=nombre_lote_asociado,
                        metodo_descorne=metodo_descorne,
                        fecha_descorne=fecha_descorne,
                        comentario_descorne=comentario_descorne,
                        usuario_id=current_user

                    )

                    db.execute(IngresarPlanSanidadLotesDescorne)
                    db.commit()
                else:
                    db.execute(modelo_manejo_ternero_recien_nacido_lotes.update().where(modelo_descorne_lotes.c.id_bovino == ListadoIDBovino).values(
                        nombre_bovino=NombreBovino,
                        estado_solicitud_recien_nacido=Estado,
                        metodo_descorne=metodo_descorne,
                        fecha_descorne=fecha_descorne,
                        comentario_descorne=comentario_descorne))
                    db.commit()


        except Exception as e:
            logger.error(f'Error al Registrar Descorne: {e}')
            raise

    def CrearPlanSanidadControlParasitos(self, nombre_lote_asociado, fecha_tratamiento_lote, tipo_tratamiento, producto_usado,comentario_parasitos, db,
                                 current_user):



        try:
            # La siguiente consulta trae la información de la tabla de inventario de los animales asociados al Lote
            AnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == nombre_lote_asociado,
                       modelo_bovinos_inventario.c.usuario_id == current_user).all()

            IngresarEventos = modelo_eventos_asociados_lotes.insert().values(

                nombre_lote=nombre_lote_asociado,
                nombre_evento="Programa de Control de Parásitos",
                estado_evento="Activo",
                usuario_id=current_user

            )

            db.execute(IngresarEventos)
            db.commit()

            for IDAnimales in AnimalesLote:
                ListadoIDBovino = IDAnimales.id_bovino
                NombreBovino = IDAnimales.nombre_bovino

                # La siguiente variable contiene el estado de la solicitud de la tabla
                Estado = "Activo"
                # Consulta si El animal ya existe para actualizar o crear el campo dentro de la tabla
                ConsultaIDExiste = db.execute(
                    modelo_control_parasitos_lotes.select().where(
                        modelo_control_parasitos_lotes.columns.id_bovino == ListadoIDBovino)).first()
                if ConsultaIDExiste is None:
                    IngresarPlanSanidadLotesDescorne = modelo_control_parasitos_lotes.insert().values(
                        estado_solicitud_parasitos=Estado,
                        id_bovino=ListadoIDBovino,
                        nombre_bovino=NombreBovino,
                        nombre_lote_asociado=nombre_lote_asociado,
                        fecha_tratamiento_lote=fecha_tratamiento_lote,
                        tipo_tratamiento=tipo_tratamiento,
                        producto_usado=producto_usado,
                        comentario_parasitos=comentario_parasitos,
                        usuario_id=current_user

                    )

                    db.execute(IngresarPlanSanidadLotesDescorne)
                    db.commit()
                else:
                    db.execute(modelo_control_parasitos_lotes.update().where(
                        modelo_descorne_lotes.c.id_bovino == ListadoIDBovino).values(
                        nombre_bovino=NombreBovino,
                        estado_solicitud_recien_nacido=Estado,
                        fecha_tratamiento_lote=fecha_tratamiento_lote,
                        tipo_tratamiento=tipo_tratamiento,
                        producto_usado=producto_usado,
                        comentario_parasitos=comentario_parasitos,))
                    db.commit()


        except Exception as e:
            logger.error(f'Error al Registrar Parasitos: {e}')
            raise

    def CrearPlanSanidadVacunacion(self, nombre_lote_asociado,  db,current_user,fecha_registrada_usuario,tipo_vacuna,FechaNotificacionVacuna,):



        try:
            # La siguiente consulta trae la información de la tabla de inventario de los animales asociados al Lote
            AnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == nombre_lote_asociado,
                       modelo_bovinos_inventario.c.usuario_id == current_user).all()
            # Ingresa los eventos Asociados A los Planes sanitarios
            IngresarEventos = modelo_eventos_asociados_lotes.insert().values(

                nombre_lote=nombre_lote_asociado,
                nombre_evento="Vacunaciones",
                estado_evento="Activo",
                FechaNotificacion=FechaNotificacionVacuna,
                usuario_id=current_user

            )

            db.execute(IngresarEventos)
            db.commit()

            for IDAnimales in AnimalesLote:
                ListadoIDBovino = IDAnimales.id_bovino
                NombreBovino = IDAnimales.nombre_bovino

                # La siguiente variable contiene el estado de la solicitud de la tabla
                Estado = "Activo"
                # Consulta si El animal ya existe para actualizar o crear el campo dentro de la tabla
                ConsultaIDExiste = db.execute(
                    modelo_registro_vacunas_bovinos.select().where(
                        modelo_registro_vacunas_bovinos.columns.id_bovino == ListadoIDBovino)).first()
                if ConsultaIDExiste is None:


                    IngresarPlanSanidadLotesDescorne = modelo_registro_vacunas_bovinos.insert().values(

                        id_bovino=ListadoIDBovino,
                        nombre_bovino=NombreBovino,
                        nombre_lote_asociado=nombre_lote_asociado,
                        fecha_registrada_usuario=fecha_registrada_usuario,
                        tipo_vacuna=tipo_vacuna,


                        usuario_id=current_user

                    )

                    db.execute(IngresarPlanSanidadLotesDescorne)
                    db.commit()
                else:
                    db.execute(modelo_registro_vacunas_bovinos.update().where(
                        modelo_descorne_lotes.c.id_bovino == ListadoIDBovino).values(
                        nombre_bovino=NombreBovino,
                        fecha_registrada_usuario=fecha_registrada_usuario,
                        tipo_vacuna=tipo_vacuna,))
                    db.commit()


        except Exception as e:
            logger.error(f'Error al Registrar Vacunación: {e}')
            raise

    def CrearPlanSanidadPodologia(self, nombre_lote_asociado, fecha_registro_podologia, espacialista_podologia, comentario_podologia,FechaNotificacionPodologia, db,
                                 current_user):



        try:
            # La siguiente consulta trae la información de la tabla de inventario de los animales asociados al Lote
            AnimalesLote = db.query(modelo_bovinos_inventario). \
                filter(modelo_bovinos_inventario.c.nombre_lote_bovino == nombre_lote_asociado,
                       modelo_bovinos_inventario.c.usuario_id == current_user).all()

            IngresarEventos = modelo_eventos_asociados_lotes.insert().values(

                nombre_lote=nombre_lote_asociado,
                nombre_evento="Podología",
                estado_evento="Activo",
                FechaNotificacion=FechaNotificacionPodologia,
                usuario_id=current_user

            )

            db.execute(IngresarEventos)
            db.commit()

            for IDAnimales in AnimalesLote:
                ListadoIDBovino = IDAnimales.id_bovino
                NombreBovino = IDAnimales.nombre_bovino

                # La siguiente variable contiene el estado de la solicitud de la tabla
                Estado = "Activo"
                # Consulta si El animal ya existe para actualizar o crear el campo dentro de la tabla
                ConsultaIDExiste = db.execute(
                    modelo_control_podologia_lotes.select().where(
                        modelo_control_podologia_lotes.columns.id_bovino == ListadoIDBovino)).first()
                if ConsultaIDExiste is None:
                    IngresarPlanSanidadLotesPodologia= modelo_control_podologia_lotes.insert().values(
                        estado_solicitud_podologia=Estado,
                        id_bovino=ListadoIDBovino,
                        nombre_bovino=NombreBovino,
                        nombre_lote_asociado=nombre_lote_asociado,
                        fecha_registro_podologia=fecha_registro_podologia,
                        espacialista_podologia=espacialista_podologia,
                        comentario_podologia=comentario_podologia,

                        usuario_id=current_user

                    )

                    db.execute(IngresarPlanSanidadLotesPodologia)
                    db.commit()
                else:
                    db.execute(modelo_manejo_ternero_recien_nacido_lotes.update().where(
                        modelo_descorne_lotes.c.id_bovino == ListadoIDBovino).values(
                        nombre_bovino=NombreBovino,
                        estado_solicitud_recien_nacido=Estado,

                        nombre_lote_asociado=nombre_lote_asociado,
                        fecha_registro_podologia=fecha_registro_podologia,
                        espacialista_podologia=espacialista_podologia,
                        comentario_podologia=comentario_podologia,))
                    db.commit()


        except Exception as e:
            logger.error(f'Error al Registrar Podologia: {e}')
            raise
bovinos_inventario = CRUDBovinos()