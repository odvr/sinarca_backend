ALTER TABLE `bovinos`
	ADD COLUMN `numero_siniiga` VARCHAR(300) NULL DEFAULT NULL AFTER `numero_chapeta`;

ALTER TABLE `bovinos`
	ADD COLUMN `numero_upp` VARCHAR(50) NULL DEFAULT NULL AFTER `numero_siniiga`;



INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.5.2', 'Se realiza ajuste en el Inventario de Acuerdo a requerimiento para cliente en Mexico', '2025-04-14', 'ovega','Se requiere actualizar a la versión V.1.5.8 del FrondEnd ');