ALTER TABLE `facturas`
	ADD COLUMN `tipo_venta` VARCHAR(150) NULL DEFAULT NULL AFTER `cliente_id`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.4', 'Ajuste en la tabla de Facturación', '2024-09-25', 'odvega','Versiones superiores a FronTend 1.4.0');