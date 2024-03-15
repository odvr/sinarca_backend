import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.db import remitente,password,servidor_smtp,puerto_smtp
def enviar_correo(destinatario, asunto, mensaje):


    # Configurar el mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain'))

    # Establecer conexión con el servidor SMTP
    servidor = smtplib.SMTP(host=servidor_smtp, port=puerto_smtp)
    servidor.starttls()  # Habilitar la capa de seguridad

    # Iniciar sesión en el servidor SMTP
    servidor.login(remitente, password)

    # Enviar el correo electrónico
    servidor.sendmail(remitente, destinatario, msg.as_string())

    # Cerrar la conexión
    servidor.quit()


