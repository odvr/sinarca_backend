ALTER TABLE `historial_partos`
	ADD COLUMN `cantidad` INT NULL DEFAULT NULL AFTER `nombre_hijo`,
	ADD COLUMN `tecnica_reproduccion` VARCHAR(300) NULL DEFAULT NULL AFTER `cantidad`,
	ADD COLUMN `observaciones` VARCHAR(300) NULL DEFAULT NULL AFTER `tecnica_reproduccion`;


CREATE TABLE `embriones_transferencias` (
	`id_embrion` INT(11) NOT NULL AUTO_INCREMENT,
	`inf_madre_biologica` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`inf_padre_biologico` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`estado` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_implante` DATE NULL DEFAULT NULL,
	`id_receptora` INT(11) NULL DEFAULT NULL,
	`nombre_receptora` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`resultado_trasnplante` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_parto` DATE NULL DEFAULT NULL,
	`id_bovino_hijo` INT(11) NULL DEFAULT NULL,
	`nombre_hijo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_embrion`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `embriones_transferencias_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=40
;


ALTER TABLE `historial_partos`
	ADD COLUMN `id_bovino_madre` INT NULL AFTER `usuario_id`,
	ADD COLUMN `id_bovino_padre` INT NULL AFTER `id_bovino_madre`,
	ADD COLUMN `nombre_padre` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_madre`;



CREATE TABLE `detalles_partos` (
	`id_detalle_parto` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino_madre` INT(11) NULL DEFAULT NULL,
	`id_bovino_padre` INT(11) NULL DEFAULT NULL,
	`nombre_madre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`nombre_padre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_parto` DATE NULL DEFAULT NULL,
	`id_bovino_hijo` INT(11) NULL DEFAULT NULL,
	`nombre_hijo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_detalle_parto`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `detalles_partos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=45
;

ALTER TABLE `embriones_transferencias`
	ADD COLUMN `raza` VARCHAR(300) NULL DEFAULT NULL AFTER `observaciones`;


ALTER TABLE `embriones_transferencias`
	CHANGE COLUMN `resultado	_trasnplante` `resultado_trasnplante` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin' AFTER `nombre_receptora`;


ALTER TABLE `embriones_transferencias`
	ADD COLUMN `codigo_nombre_embrion` VARCHAR(300) NULL DEFAULT NULL AFTER `id_embrion`;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.5.0', 'Se agrega nuevas tablas para dar avance a embriones y partos multiples', '2025-03-26', 'jvega','NA');