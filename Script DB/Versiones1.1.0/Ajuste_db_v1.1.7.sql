ALTER TABLE `periodos_lactancia`
	ADD COLUMN `id_parto` INT(11) NULL DEFAULT NULL AFTER `usuario_id`,
	ADD CONSTRAINT `FK_periodos_lactancia_historial_partos` FOREIGN KEY (`id_parto`) REFERENCES `historial_partos` (`id_parto`) ON UPDATE NO ACTION ON DELETE NO ACTION;

ALTER TABLE `periodos_lactancia`
	ADD COLUMN `mensaje` VARCHAR(300) NULL DEFAULT NULL AFTER `id_parto`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.7', 'Nuevo campo en tabla de lactancia(id_parto)', '2024-04-28', 'Jose Vega',' N/A');