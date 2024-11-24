import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.db import remitente, password, servidor_smtp, puerto_smtp, Rutabase
import logging
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




def enviar_correo_publicidad(destinatario):
    """

    :param destinatario: Envia el destinatario para el
    :return:
    """

    try:

        # Cargar el contenido del archivo HTML desde la carpeta 'Plantillas'
        with open(Rutabase+'/Lib/Plantillas/Publicidad.html', 'r', encoding='utf-8') as file:
            MensajeEnvioPublicidad = file.read()
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = "Optimiza tu Ganadería con Ruta Ganadera - ¡Aumenta tu Productividad!"
        # Agregar el cuerpo del mensaje con encabezado html
        msg.attach(MIMEText(MensajeEnvioPublicidad, 'html'))
        # Establecer conexión con el servidor SMTP
        servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
        servidor.starttls()  # Habilitar la capa de seguridad
        # Iniciar sesión en el servidor SMTP
        servidor.login(remitente, password)
        # Enviar el correo electrónico
        servidor.sendmail(remitente, destinatario, msg.as_string())
        # Cerrar la conexión
        servidor.quit()


    except Exception as e:
        logger.error(f'Error al enviar Correo Publicitario: {e}')
        raise

def enviar_correo_bienvenida(destinatario):
    """

    :param destinatario: Envia el destinatario de Bienvenida
    :return:
    """

    try:

        # Cargar el contenido del archivo HTML desde la carpeta 'Plantillas'
        with open(Rutabase+'/Lib/Plantillas/Bienvenida.html', 'r', encoding='utf-8') as file:
            MensajeEnvioBienvenida = file.read()
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = "Bienvenida - Ruta Ganadera"
        # Agregar el cuerpo del mensaje con encabezado html
        msg.attach(MIMEText(MensajeEnvioBienvenida, 'html'))
        # Establecer conexión con el servidor SMTP
        servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
        servidor.starttls()  # Habilitar la capa de seguridad
        # Iniciar sesión en el servidor SMTP
        servidor.login(remitente, password)
        # Enviar el correo electrónico
        servidor.sendmail(remitente, destinatario, msg.as_string())
        # Cerrar la conexión
        servidor.quit()


    except Exception as e:
        logger.error(f'Error al enviar Correo Bienvenida: {e}')
        raise





def enviar_correo_publicidad_Asociaciones(destinatario):
    """
    La siguiente Función envia publicidad a las asociaciones

    :return:
    """

    try:

        # Cargar el contenido del archivo HTML desde la carpeta 'Plantillas'
        with open(Rutabase+'/Lib/Plantillas/PublicidadAsociaciones.html', 'r', encoding='utf-8') as file:
            MensajeEnvioPublicidad = file.read()
        # Configurar el mensaje
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = " Ruta Ganadera: Transformando tu ganadería 🐄💻"
        # Agregar el cuerpo del mensaje con encabezado html
        msg.attach(MIMEText(MensajeEnvioPublicidad, 'html'))
        # Establecer conexión con el servidor SMTP
        servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
        servidor.starttls()  # Habilitar la capa de seguridad
        # Iniciar sesión en el servidor SMTP
        servidor.login(remitente, password)
        # Enviar el correo electrónico
        servidor.sendmail(remitente, destinatario, msg.as_string())
        # Cerrar la conexión
        servidor.quit()


    except Exception as e:
        logger.error(f'Error al enviar Correo Publicitario Para Asociaciones: {e}')
        raise
