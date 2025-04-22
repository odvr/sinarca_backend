CREATE TABLE `hembras_donantes` (
	`id_donante` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`raza` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`edad` INT(11) NULL DEFAULT NULL,
	`edad_AA_MM_DD` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`embriones_producidos` INT(11) NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_donante`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `hembras_donantes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;


CREATE TABLE `extracciones_embriones` (
	`id_extraccion` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_extraccion` DATE NULL DEFAULT NULL,
	`observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`total_embriones` INT(11) NULL DEFAULT NULL,
	`embriones_viables` INT(11) NULL DEFAULT NULL,
	`responsable` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_extraccion`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `extracciones_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;

CREATE TABLE `embriones` (
	`id_embrion` INT(11) NOT NULL AUTO_INCREMENT,
	`codigo_identificador` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_extraccion` INT(11) NULL DEFAULT NULL,
	`extraccion` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`metodo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_donante` INT(11) NULL DEFAULT NULL,
	`nombre_donante` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`padre_o_pajilla` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_padre_pajilla` INT(11) NULL DEFAULT NULL,
	`nombre_padre_o_pajilla` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`calidad_embrion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`estado_embrion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`productor` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`raza_madre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`raza_padre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`pedigree_madre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`pedigree_padre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_produccion_embrion` DATE NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_embrion`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;



CREATE TABLE `transferencias_embriones` (
	`id_transferencia` INT(11) NOT NULL AUTO_INCREMENT,
	`id_embrion` INT(11) NULL DEFAULT NULL,
	`embrion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_receptora` INT(11) NULL DEFAULT NULL,
	`nombre_receptora` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_transferencia` DATE NULL DEFAULT NULL,
	`resultado` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_parto` INT(11) NULL DEFAULT NULL,
	`id_cria` INT(11) NULL DEFAULT NULL,
	`nombre_cria` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_transferencia`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `transferencias_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;




CREATE TABLE `termocriogenico_embriones` (
	`id_termo` INT(11) NOT NULL AUTO_INCREMENT,
	`nombre_termo_identificador` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`cantidad_canastillas` INT(11) NULL DEFAULT NULL,
	`ubicacion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_termo`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `termocriogenico_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;


CREATE TABLE `canastillas_embriones` (
	`id_canastilla_embrion` INT(11) NOT NULL AUTO_INCREMENT,
	`id_termo` INT(11) NOT NULL DEFAULT '0',
	`nombre_termo_identificador` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`nombre_codigo_canastilla` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`gondolas` INT(11) NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_canastilla_embrion`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `canastillas_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=12
;



CREATE TABLE `gondolas_embriones` (
	`id_gondola` INT(11) NOT NULL AUTO_INCREMENT,
	`id_termo` INT(11) NULL DEFAULT NULL,
	`nombre_termo_identificador` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_canastilla_embrion` INT(11) NULL DEFAULT NULL,
	`nombre_codigo_canastilla` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`nombre_posicion_gondola` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`estado` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_gondola`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `gondolas_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=11
;

CREATE TABLE `banco_embriones` (
	`id_banco` INT(11) NOT NULL AUTO_INCREMENT,
	`id_embrion` INT(11) NULL DEFAULT NULL,
	`nombre_codigo_embrion` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_ingreso` DATE NULL DEFAULT NULL,
	`fecha_salida` DATE NULL DEFAULT NULL,
	`id_termo` INT(11) NULL DEFAULT NULL,
	`termo` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_canastilla_embrion` INT(11) NULL DEFAULT NULL,
	`nombre_codigo_canastilla` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`id_gondola` INT(11) NULL DEFAULT NULL,
	`gondola_posicion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_banco`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `banco_embriones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=11
;


CREATE TABLE `hembras_receptoras` (
	`id_receptora` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`raza` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`edad` INT(11) NULL DEFAULT NULL,
	`edad_AA_MM_DD` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`transferencias_recibidas` INT NULL DEFAULT NULL COLLATE 'latin1_bin',
	`transferencias_exitosas` INT NULL DEFAULT NULL,
	`transferecnias_fallidas` INT NULL DEFAULT NULL,
	`tasa_exito` DOUBLE NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_receptora`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `hembras_receptoras_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC
AUTO_INCREMENT=8
;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.5.4', 'Se cambia agregan tablas para el sistemas de embriones', '2025-04-21', 'jvega','NA');