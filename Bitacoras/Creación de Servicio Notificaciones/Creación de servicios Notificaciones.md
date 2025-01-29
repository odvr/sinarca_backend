# Mejora: Módulo de Notificaciones


Versión: V.1.4.9
## Requerimiento:

Se requiere crear un módulo que permita realizar el envío de notificaciones de manera automatizada y eficiente, adaptándose a las necesidades del sistema actual.

## Alcance / Objetivo:

- Mejorar el sistema de notificaciones de la aplicación para optimizar la comunicación interna y externa.
- Implementar un mecanismo centralizado y modular para el envío de notificaciones, garantizando mayor flexibilidad y mantenibilidad del código.
- Establecer un soporte inicial en ambientes Unix con posibilidad de expandirse a otros entornos en el futuro.

## Rama:

- **Main**

## Ajustes Modelo de Base de Datos:

- No se requiere ajuste de base de datos, ya que la funcionalidad propuesta opera únicamente a nivel de aplicación.

## Requerimientos/Módulos Afectados:

1. **Nueva Librería: Script**
   - Se crea una nueva librería llamada `Script`, donde se alojará el archivo `notificaciones.py`.
   - Este archivo contendrá las funciones necesarias para la gestión de notificaciones.
   - La librería debe ser estructurada de manera modular para facilitar futuras ampliaciones.

2. **Método de Conexión**
   - Las funciones dentro de `notificaciones.py` deben hacer uso del método de conexión existente para unificar y simplificar el acceso a recursos compartidos.
   - Esto garantiza un manejo consistente de la conectividad en toda la aplicación.

3. **Tareas Programadas**
   - La ejecución de las notificaciones se gestionará a través de una tarea programada.
   - Este mecanismo permitirá el envío automatizado de notificaciones de acuerdo con un cronograma predefinido.
   - Por ahora, el desarrollo está optimizado para ambientes Unix.


## Librerias Utilies:

-Utiliza el recurso [crud_bovinos_inventario.py](..%2F..%2Fcrud%2Fcrud_bovinos_inventario.py)  El metodo Buscar_Correo_Usuario  Te permitirá retornar el correo del usuario para agilizar el envio de la información del correo electronico con la función  
[enviar_correos.py](..%2F..%2FLib%2Fenviar_correos.py) Se encuentra debidamente actualizada y documentada



## Modo de Operación:
### Instalación del servicio Crontab
`apt update && apt install cron -y`

. Crear el directorio de cron:
Si el directorio /etc/crontabs no existe, vamos a crearlo manualmente:
`mkdir -p /etc/crontabs`
1. Permisos del Archivo
`chmod +x /app/Lib/Script/Notificaciones.sh`
2. Crear el archivo root:
Ahora puedes crear el archivo root dentro de /etc/crontabs:
`echo "0 */12 * * * /bin/bash /app/Lib/Script/Notificaciones.sh >> /app/Lib/Script/Logs/Logs.log 2>&1" > /etc/crontabs/root`
3. Verificar que cron está corriendo:
Verifica si el servicio cron está activo. Puedes hacerlo ejecutando:
`ps aux | grep cron`
4. Iniciar cron si es necesario:
Si cron no está en ejecución, intenta arrancarlo:
`service cron start`
5. Verificar cron:
Asegúrate de que cron esté ejecutando correctamente las tareas. Puedes mirar los logs de cron con:


`tail -f /var/log/cron`

Si el archivo de log no existe, créalo manualmente:

`mkdir -p /var/log
touch /var/log/cron
 `



Verificar si la tarea cron está programada
Revisar el archivo crontab de root:

Primero, asegurémonos de que la tarea cron esté correctamente registrada. Ejecuta el siguiente comando para verificar el contenido del archivo crontab de root:

`cat /etc/crontabs/root`
Deberías ver la tarea que escribiste:
`0 */12 * * * /bin/bash /app/Lib/Script/Notificaciones.sh >> /app/Lib/Script/Logs/Logs.log 2>&1`

5. Prueba Manualmente el Script
`/bin/bash /app/Lib/Script/Notificaciones.sh >> /app/Lib/Script/Logs/Logs.log 2>&1`


Anexo del Servicio 


Se realiza ajuste 



Para programar la ejecución de Logs_Notificaciones.sh en Crontab, sigue estos pasos:

1️⃣ Asegúrate de que el script tenga permisos de ejecución:
Ejecuta en la terminal:


`chmod +x /app/Lib/Script/Notificaciones.sh`

2️⃣ Edita el crontab:
Abre el crontab con:

`crontab -e`

3️⃣ Agrega una línea para programar la tarea:
Por ejemplo, si deseas ejecutar el script cada día a las 8:00 AM:

`0 8 * * * /app/Lib/Script/Logs_Notificaciones.sh`

📌 Explicación del cronjob (0 8 * * *):

0 → Minuto 0
8 → Hora 8 AM
* → Cualquier día del mes
* → Cualquier mes
* → Cualquier día de la semana
Si quieres ejecutarlo cada hora:

`0 * * * * /app/Lib/Script/Logs_Notificaciones.sh`
Si quieres ejecutarlo cada 5 minutos:


`*/5 * * * * /app/Lib/Script/Logs_Notificaciones.sh`
4️⃣ Verifica que el cron esté corriendo:
Después de guardarlo en crontab -e, revisa si está programado con:



`crontab -l`
5️⃣ Revisa los logs de cron si no funciona:

`cat /var/log/syslog | grep CRON****`