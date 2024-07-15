/*
Se agrega nuevo campo para validar la cantidad de notificaciones enviadas
**/

CREATE TABLE `registro_ocupaciones_potreros` (
	`id_ocupacion` INT(11) NOT NULL AUTO_INCREMENT,
	`id_potrero` INT(11) NULL DEFAULT NULL,
	`nombre_potrero` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_lote` INT(11) NULL DEFAULT NULL,
	`nombre_lote` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_inicio_ocupacion` DATE NULL DEFAULT NULL,
	`fecha_final_recomendada` DATE NULL DEFAULT NULL,
	`fecha_final_real` DATE NULL DEFAULT NULL,
	`observacion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_ocupacion`),
	INDEX `usuario_id` (`usuario_id`),
	CONSTRAINT `registro_ocupaciones_potreros_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`)
);

ALTER TABLE `carga_animal`
	ADD COLUMN `id_lote` INT(11) NULL DEFAULT NULL AFTER `nombre_bovino`,
	ADD COLUMN `nombre_lote` VARCHAR(300) NULL DEFAULT NULL AFTER `id_lote`;

ALTER TABLE `carga_animal`
	ADD CONSTRAINT `FK_carga_animal_lotes_bovinos` FOREIGN KEY (`id_lote`) REFERENCES `lotes_bovinos` (`id_lote_bovinos`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `capacidad_carga`
	ADD COLUMN `id_lote` INT(11) NULL DEFAULT NULL AFTER `interpretacion`,
	ADD COLUMN `nombre_lote` VARCHAR(300) NULL DEFAULT NULL AFTER `id_lote`,
	ADD COLUMN `estado` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_lote`,
	ADD COLUMN `fecha_inicio_ocupacion` DATE NULL DEFAULT NULL AFTER `estado`,
	ADD COLUMN `fecha_final_recomendada` DATE NULL DEFAULT NULL AFTER `fecha_inicio_ocupacion`,
	ADD COLUMN `fecha_final_real` DATE NULL DEFAULT NULL AFTER `fecha_final_recomendada`,
	ADD COLUMN `fecha_inicio_descanso` DATE NULL DEFAULT NULL AFTER `fecha_final_real`,
	ADD COLUMN `fecha_final_descanso` DATE NULL DEFAULT NULL AFTER `fecha_inicio_descanso`,
	ADD COLUMN `dias_descanso` INT(11) NULL DEFAULT NULL AFTER `fecha_final_descanso`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.2', 'Se agregan nuevos campos y tablas para capacidad de carga con lotes', '2024-07-15', 'jfvega','N/A');