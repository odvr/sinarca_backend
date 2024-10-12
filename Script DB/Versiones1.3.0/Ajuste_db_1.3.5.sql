ALTER TABLE `facturas`
	ADD COLUMN `descripcion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin' AFTER `usuario_id`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.5', 'Ajuste en la tabla de Facturas', '2024-10-12', 'jvega','Versiones superiores a FronTend 1.4.0');