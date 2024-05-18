ALTER TABLE `evaluaciones_macho_reproductor`
	ADD COLUMN `estado_solicitud_reproductor` VARCHAR(300) NULL DEFAULT NULL AFTER `usuario_id`;

ALTER TABLE `evaluaciones_macho_reproductor`
	ADD COLUMN `comentarios_evaluacion_reproductor` VARCHAR(300) NULL DEFAULT NULL AFTER `estado_solicitud_reproductor`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.9', 'Se realiza la actualización del campo para estado de la solicitud', '2024-05-17', 'Omar Vega ',' Se debe ajustar a la versión V.1.1.4 FrondEnd o superior');