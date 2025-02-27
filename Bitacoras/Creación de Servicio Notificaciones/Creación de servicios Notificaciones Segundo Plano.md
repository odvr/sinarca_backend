# Ejecución de un Script Python en Segundo Plano con `nohup`

## Introducción
Cuando se ejecuta un script en un entorno de servidor o en sistemas donde la sesión puede cerrarse, es útil ejecutarlo en segundo plano para que continúe funcionando incluso después de cerrar la terminal. `nohup` (No Hang Up) permite que un proceso siga ejecutándose aunque la sesión se cierre.

## Comando Básico
Para ejecutar un script de Python en segundo plano y redirigir su salida a un archivo de log, usa:

```sh
nohup python Notificaciones.py > mi_log.log 2>&1 &
```

### Explicación del Comando:
- `nohup` → Permite que el proceso continúe corriendo incluso después de cerrar la terminal.
- `python Notificaciones.py` → Ejecuta el script de Python.
- `>` → Redirige la salida estándar (stdout) a un archivo.
- `mi_log.log` → Archivo donde se guardará la salida del script.
- `2>&1` → Redirige también los errores (stderr) al mismo archivo.
- `&` → Ejecuta el proceso en segundo plano.

## Verificación del Proceso
Para comprobar si el script está corriendo, usa:

```sh
ps aux | grep Notificaciones.py
```

Si el script está en ejecución, verás un resultado similar a:

```sh
root       1234  0.1  0.6 131364 48900 pts/0    Sl   15:07   0:00 python Notificaciones.py
```

Si necesitas detener el proceso, puedes hacerlo con:

```sh
kill -9 1234  # Donde 1234 es el PID del proceso
```

O puedes detener todas las instancias con:

```sh
pkill -f Notificaciones.py
```

## Monitoreo del Log
Para ver en tiempo real lo que está haciendo el script, usa:

```sh
tail -f mi_log.log
```

Esto mostrará en la terminal la salida del script a medida que se genera.

## Conclusión
Usar `nohup` con redirección de logs permite ejecutar scripts Python de forma confiable en segundo plano, asegurando que sigan corriendo incluso si la sesión se cierra. Además, el monitoreo mediante `tail -f` ayuda a revisar su funcionamiento sin necesidad de detenerlo.

