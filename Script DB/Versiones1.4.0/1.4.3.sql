
CREATE TABLE `notificacion_proximidad_parto` (
	`id_notificacion` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_estimada_parto` DATE NULL DEFAULT NULL,
	`fecha_mensaje` DATE NULL DEFAULT NULL,
	`mensaje` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_notificacion`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `notificacion_proximidad_partofk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
AUTO_INCREMENT=8
;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.3', 'se crea tabla de notificacion de parto', '2025-01-29', 'jvega','N/A');