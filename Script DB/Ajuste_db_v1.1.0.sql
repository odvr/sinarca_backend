
ALTER TABLE `produccion_levante`
	ADD COLUMN `ganancia_media_diaria` FLOAT NULL DEFAULT NULL AFTER `nombre_bovino`;

ALTER TABLE `produccion_ceba`
	ADD COLUMN `ganancia_media_diaria` FLOAT NULL DEFAULT NULL AFTER `nombre_bovino`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.0', 'Se agrega un nuevo campo En tablas de levante y ceba', '2024-03-08', 'Jose Vega','');