ALTER TABLE `bovinos`
	ADD COLUMN `numero_chapeta` VARCHAR(300) NULL DEFAULT NULL AFTER `edad_YY_MM_DD`;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.7', 'Se agrega nuevo campo para chapetas', '2025-02-21', 'ovega','Se requiere actualización FrondTend a10998');