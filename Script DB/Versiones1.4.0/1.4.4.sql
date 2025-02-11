
ALTER TABLE `periodos_secado`
	CHANGE COLUMN `tratamiento` `tratamiento` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin' AFTER `fecha_final_secado`,
	CHANGE COLUMN `interpretacion` `observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin' AFTER `duracion`,
	DROP COLUMN `fecha_recomendada_secado`,
	DROP COLUMN `secado_realizado`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.4', 'se ajusta la tabla de periodos secado', '2025-02-11', 'jvega','N/A');