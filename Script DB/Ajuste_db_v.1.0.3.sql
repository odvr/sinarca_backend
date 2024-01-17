/**Ajuste de campo de inceminación*/


ALTER TABLE usuarios
ADD COLUMN nombre_predio VARCHAR(300),
ADD COLUMN correo_electronico VARCHAR(300),
ADD COLUMN telefono VARCHAR(300),
ADD COLUMN ubicacion_predio VARCHAR(300),
ADD COLUMN nombre_apellido VARCHAR(300);


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.3', 'Se agregan nuevos campos en tabla de usuarios', '2024-01-17', 'Omar Vega', 'Se requiere acutualización del FrondEnd versión Git 673ae21
');

