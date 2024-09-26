ALTER TABLE `bovinos`
	ADD COLUMN `edad_destete` INT(10) NULL AFTER `fecha_de_ingreso_sistema`;

CREATE TABLE `abortos` (
	`id_aborto` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_aborto` DATE NULL DEFAULT NULL,
	`causa` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_aborto`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `abortos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarcas`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;


CREATE TABLE `periodos_lactancia` (
	`id_lactancia` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_inicio_lactancia` DATE NULL DEFAULT NULL,
	`fecha_final_lactancia` DATE NULL DEFAULT NULL,
	`duracion` INT(11) NULL DEFAULT NULL,
	`total_litros_producidos` FLOAT NULL DEFAULT NULL,
	`tipo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`pico` FLOAT NULL DEFAULT NULL,
	`fecha_pico` DATE NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_lactancia`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `periodos_lactancia_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarcas`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;


CREATE TABLE `periodos_secado` (
	`id_secado` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_inicio_secado` DATE NULL DEFAULT NULL,
	`fecha_final_secado` DATE NULL DEFAULT NULL,
	`duracion` INT(11) NULL DEFAULT NULL,
	`interpretacion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_secado`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `periodos_secado_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `sinarcas`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;



INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.6', 'nuevas tablas (abortos, periodos lactancia y periodos secado)', '2024-04-26', 'Jose Vega','');