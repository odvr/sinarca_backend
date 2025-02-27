"""
@Autor:odvr
Se realiza  la siguiente Función para poder realizar el Envio de Notificaciones Vía whatsapp

"""
import urllib.request
import json

def enviar_Notificaciones_Whatsapp(NumeroCliente, Mensaje):
    """
    Envía una notificación de WhatsApp usando urllib.request.
    """

    "Cambiar URL de acuerdo a ajustes a realizar "
    url = "http://host.docker.internal:3000/send-message"
    data = json.dumps({"number": NumeroCliente, "message": Mensaje}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            print("Mensaje enviado de forma exitosa")
            print("Respuesta:", response.read().decode())
    except urllib.error.HTTPError as e:
        print("Error en la solicitud:", e.read().decode())

# Uso
# enviar_Notificaciones_Whatsapp("123456789", "Hola desde FastAPI!")
