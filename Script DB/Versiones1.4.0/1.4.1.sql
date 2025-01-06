
ALTER TABLE `bovinos`
	ADD COLUMN `chip_asociado` VARCHAR(50) NULL DEFAULT NULL AFTER `nombre_lote_bovino`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.1', 'Nuevo Campo de Integraciones', '2025-01-03', 'odvr','Versiones superiores a FronTend V.1.4.9');