ALTER TABLE usuarios
ADD COLUMN ultimo_login DATETIME;
INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.2', 'Se agrega Campo de Ultimo Login', '2024-03-16', 'Omar Vega',' Sin Observaciones');