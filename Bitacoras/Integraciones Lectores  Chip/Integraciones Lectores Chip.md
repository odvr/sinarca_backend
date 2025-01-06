

# Bitácora de Funcionamiento del Sistema de Lectura RFID

## Requerimiento:

El sistema de lectura RFID se ha implementado con éxito para facilitar la identificación y gestión de animales a través de microchips estandarizados ISO 11784/11785 FDX-B. Este documento detalla el funcionamiento, las pruebas realizadas, los resultados obtenidos y las mejoras futuras previstas.

## Alcance / Objetivo:

Lector RFID P180:

- Frecuencia: 134.2/125 kHz

- Compatibilidad: ISO 11784/11785 FDX-B y EMID

- Conexiones: Bluetooth HID/SPP y USB 2.0

- Almacenamiento de hasta 128 registros

### Funciones principales:

- Búsqueda y conexión de dispositivos Bluetooth.

- Recepción y almacenamiento de datos de etiquetas RFID.

- Visualización en tiempo real de información recibida.

## Rama:

 - Main

## Ajustes Modelo de Base de datos

- [1.4.1.sql](..%2F..%2FScript%20DB%2FVersiones1.4.0%2F1.4.1.sql)

## Requerimientos/Módulos Afectados

- Modulo de Inventarios, Se realiza la creación de un Nuevo Item

## Resultado Esperado / Modo de Funcionamiento:

Encender el lector RFID y asegurarse de que esté en modo Bluetooth o USB según sea necesario.

Acceder a la aplicación web y buscar el dispositivo lector disponible.

Establecer la conexión.

Escanear etiquetas RFID:

Confirmar que el lector registre correctamente el código en pantalla.

Visualizar los datos en la interfaz de la aplicación web.

