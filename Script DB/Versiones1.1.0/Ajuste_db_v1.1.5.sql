ALTER TABLE `reportespesaje`
	ADD COLUMN `tipo_pesaje` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_bovino`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.5', 'nuevo campo en tabla de pesaje(tipo_pesaje)', '2024-04-26', 'Jose Vega');