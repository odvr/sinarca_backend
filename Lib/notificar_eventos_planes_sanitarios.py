
from contextlib import contextmanager
from sqlalchemy.orm import Session
import crud
from Lib.enviar_correos import enviar_correo
from config.db import  get_session
import logging
from datetime import  datetime
from models.modelo_bovinos import  modelo_eventos_asociados_lotes

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


"""
Trae la configuración de conexión de la base de datos
"""
@contextmanager
def get_database_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def  Notificar_Eventos_Planes_Sanitarios(db: Session):

    "Consulta para ejecutada para validar los datos"
    ConsultarTablaEventosPlanesSanitariosLotes = db.query(modelo_eventos_asociados_lotes).all()


    """
    Debe recorrer la tabla completa para poder realizar la valitación de los Estad
    """
    for DatosPlanesSanitarios in ConsultarTablaEventosPlanesSanitariosLotes:

        Asunto = "Notificación Planes Sanitarios"
        "Busca la información del Usuario para realizar el Envio de la Notificación"
        DatosUsuario = crud.bovinos_inventario.Buscar_Usuario_Conectado(db=db,
                                                                        current_user=DatosPlanesSanitarios.usuario_id)

        if DatosPlanesSanitarios.estado_evento == "Ejecutado":
            pass
        if DatosPlanesSanitarios.estado_evento == "Planeado":
            CalcularDiasNotificacion = (datetime.now().date() - DatosPlanesSanitarios.FechaNotificacion).days
            if CalcularDiasNotificacion == 0:

                #Recorre la lista de las personas para enviar la notificación
                for BuscarCorreo in DatosUsuario:
                    NombreLoteNotificar = DatosPlanesSanitarios.nombre_lote
                    TipoEvento= DatosPlanesSanitarios.nombre_evento
                    #Invoca la funcioón de envio de correo electronico
                    enviar_correo(destinatario=BuscarCorreo.correo_electronico, asunto=Asunto, Notificacion = "¡Hola!\n\nTe recuerdo que hoy tienes programado el Plan Sanitario "+ TipoEvento + " correspondiente al Lote "+NombreLoteNotificar +".\n\nEs importante que actualices tus planes sanitarios y los mantengas al día, ya que son fundamentales para la salud de tu hato ganadero.")




            if CalcularDiasNotificacion == 2:
                # Recorre la lista de las personas para enviar la notificación
                for BuscarCorreo in DatosUsuario:
                    NombreLoteNotificar = DatosPlanesSanitarios.nombre_lote
                    FechaEvento = datetime.combine(DatosPlanesSanitarios.FechaNotificacion, datetime.min.time())
                    # Formato de la fecha como cadena
                    FechaEventoStr = FechaEvento.strftime("%d-%m-%Y")

                    TipoEvento = DatosPlanesSanitarios.nombre_evento
                    # Invoca la funcioón de envio de correo electronico
                    enviar_correo(destinatario=BuscarCorreo.correo_electronico, asunto=Asunto,
                                  Notificacion="¡Hola!\n\nTe recuerdo que el día "+ FechaEventoStr + " tienes programado el Plan Sanitario " + TipoEvento + " correspondiente al Lote " + NombreLoteNotificar + ".\n\nEs importante que actualices tus planes sanitarios y los mantengas al día, ya que son fundamentales para la salud de tu hato ganadero.")


# Usando el context manager para obtener y cerrar la sesión de base de datos correctamente
with get_database_session() as db:
    Notificar_Eventos_Planes_Sanitarios(db=db)

