
ALTER TABLE usuarios
ADD COLUMN fecha_de_registro DATETIME;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.9', 'Se agrega un nuevo campo En usuarios', '2024-03-02', 'Omar Vega','Versión del FrondEnd 1.0.6');