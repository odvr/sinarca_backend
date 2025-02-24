ALTER TABLE `produccion_leche`
	ADD COLUMN `cantidad_partos_manual` INT(50) NULL DEFAULT NULL AFTER `dias_abiertos`;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.8', 'Se agrega nuevo campo para partos manuales', '2025-02-23', 'jvega','N/A');