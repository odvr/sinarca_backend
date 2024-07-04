ALTER TABLE `eventos_asociados_lotes`
	ADD COLUMN `comentario_evento` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_evento`;



INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.8', '', '2024-07-04', 'odvr','Se requiere Versión FrodTend V.1.3.1 o superior');