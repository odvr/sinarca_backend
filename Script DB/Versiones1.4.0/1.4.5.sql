
ALTER TABLE `bovinos`
	ADD COLUMN `edad_YY_MM_DD` VARCHAR(300) NULL AFTER `nombre_finca`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.5', 'se agrega campo edad YY-MM-DD en tabla de bovinos', '2025-02-19', 'jvega','N/A');