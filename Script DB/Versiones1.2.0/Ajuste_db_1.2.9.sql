ALTER TABLE `registro_vacunacion_bovinos`
	ADD COLUMN `estado_evento_lotes` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_lote_asociado`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.9', '', '2024-07-08', 'odvr','Se requiere Versión FrodTend V.1.3.3 o superior');