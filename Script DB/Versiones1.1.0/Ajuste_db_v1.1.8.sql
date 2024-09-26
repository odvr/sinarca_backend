ALTER TABLE `palpaciones`
	ADD COLUMN `dias_gestacion` INT NULL DEFAULT NULL AFTER `nombre_bovino`,
	ADD COLUMN `fecha_estimada_prenez` DATE NULL DEFAULT NULL AFTER `dias_gestacion`,
	ADD COLUMN `fecha_estimada_parto` DATE NULL DEFAULT NULL AFTER `fecha_estimada_prenez`;

ALTER TABLE `periodos_secado`
	ADD COLUMN `fecha_recomendada_secado` DATE NULL DEFAULT NULL AFTER `nombre_bovino`,
	ADD COLUMN `secado_realizado` VARCHAR(300) NULL DEFAULT NULL AFTER `fecha_recomendada_secado`,
	ADD COLUMN `tratamiento` VARCHAR(300) NULL DEFAULT NULL AFTER `usuario_id`;

CREATE TABLE `evaluaciones_macho_reproductor` (
	`id_evaluacion` INT(11) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(11) NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_evaluacion` DATE NULL DEFAULT NULL,
	`edad_evaluacion` INT(11) NULL DEFAULT NULL,
	`circunferencia_escrotal` FLOAT NULL DEFAULT NULL,
	`simetria_testicular` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`forma_escrotal` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`consistencia_testiculos` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tamano_prepucio` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`linea_dorsal` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tipo_pezuna` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`muculatura` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`pezunas` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`mensaje` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_evaluacion`) USING BTREE,
	INDEX `FK__bovinos` (`id_bovino`) USING BTREE,
	INDEX `FK_evaluaciones_macho_reproductor_usuarios` (`usuario_id`) USING BTREE,
	CONSTRAINT `FK__bovinos` FOREIGN KEY (`id_bovino`) REFERENCES `sinarcas`.`bovinos` (`id_bovino`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `FK_evaluaciones_macho_reproductor_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `sinarcas`.`usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.8', 'Nuevos campos en tabla de palpaciones y secados', '2024-05-02', 'Jose Vega',' N/A');