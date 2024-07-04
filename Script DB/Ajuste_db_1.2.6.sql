/**
  Se realiza renombramiento de la tabla de eventos a Notificar
  */

ALTER TABLE `eventos_asociados_lotes`
	CHANGE COLUMN `FechaNotificacionRecienNacido` `FechaNotificacion` DATE NULL DEFAULT NULL AFTER `estado_evento`;


/*Creación de la tabla de descorne*/
CREATE TABLE IF NOT EXISTS `descorne_lotes` (
	`id_descorne_lote` INT(11) NOT NULL AUTO_INCREMENT,
	`estado_solicitud_descorne` VARCHAR(100) NOT NULL COLLATE 'latin1_bin',
	`metodo_descorne` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_descorne` DATE NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_lote_asociado` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`comentario_descorne` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_descorne_lote`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `descorne_lotes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarca`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;
ALTER TABLE `control_parasitos_lote`
	ADD COLUMN `estado_solicitud_parasitos` VARCHAR(300) NULL DEFAULT NULL AFTER `id_control_parasitos`;



/***Creación de la tabla de control de parasitos*/


ALTER TABLE `descorne_lotes`
	ADD COLUMN `estado_solicitud_descorne` VARCHAR(100) NOT NULL AFTER `id_descorne_lote`;

CREATE TABLE IF NOT EXISTS `control_parasitos_lote` (
	`id_control_parasitos` INT(11) NOT NULL AUTO_INCREMENT,
	`fecha_tratamiento_lote` DATE NULL DEFAULT NULL,
	`tipo_tratamiento` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`producto_usado` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`nombre_bovino` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_lote_asociado` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`comentario_parasitos` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_control_parasitos`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `control_parasitos_lote_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarca`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;


/*
Se realiza ajuste de la tabla de vacunaciones para asociar vacunas por Lostes
*/

ALTER TABLE `registro_vacunacion_bovinos`
	ADD COLUMN `nombre_lote_asociado` VARCHAR(300) NULL DEFAULT NULL AFTER `nombre_bovino`;



CREATE TABLE IF NOT EXISTS `control_podologia_lotes` (
	`id_control_podologia` INT(11) NOT NULL AUTO_INCREMENT,
	`fecha_registro_podologia` DATE NULL DEFAULT NULL,
	`espacialista_podologia` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`comentario_podologia` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`nombre_bovino` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_lote_asociado` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`estado_solicitud_podologia` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`FechaNotificacionPodologia` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_control_podologia`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `control_podologia_lotes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarca`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.6', '', '2024-06-30', 'Omar Vega ','Se requiere Versión FrodTend V.1.2.6 o superior');