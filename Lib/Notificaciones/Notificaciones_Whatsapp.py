"""
@Autor:odvr
Se realiza  la siguiente Función para poder realizar el Envio de Notificaciones Vía whatsapp

"""
import urllib.request
import json
import re


def enviar_Notificaciones_Whatsapp(NumeroCliente, Mensaje):
    # Asegurar que NumeroCliente es una cadena
    if NumeroCliente is None:
        print("Error: NumeroCliente es None")
        return

    NumeroCliente = str(NumeroCliente)  # Convertir a string por seguridad
    NumeroCliente = re.sub(r'\D', '', NumeroCliente)  # Eliminar caracteres no numéricos

    if not NumeroCliente.startswith("57"):  # Agregar código de país si falta
        NumeroCliente = "57" + NumeroCliente

    url = "http://notificaciones-whatsapp-api-1:3000/send-message"
    data = json.dumps({"number": NumeroCliente, "message": Mensaje}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print("Mensaje enviado de forma exitosa")
            print("Respuesta:", response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error HTTP: {e.code}")
        print("Respuesta del servidor:", e.read().decode())
    except urllib.error.URLError as e:
        print(f"Error de conexión: {e.reason}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
# Uso
# enviar_Notificaciones_Whatsapp("123456789", "Hola desde FastAPI!")
