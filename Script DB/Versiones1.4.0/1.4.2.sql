
CREATE TABLE `fincas` (
	`id_finca` INT(255) NOT NULL AUTO_INCREMENT,
	`nombre_finca` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`departamento` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`municipio` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`extension` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tipo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_finca`) USING BTREE,
	INDEX `FK__usuarios` (`usuario_id`) USING BTREE,
	CONSTRAINT `FK__usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;

CREATE TABLE `potreros` (
    `id_potrero` INT(255) NOT NULL AUTO_INCREMENT,
    `nombre_potrero` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
    `extension` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
    `id_finca` INT(255) NULL DEFAULT NULL COLLATE 'latin1_bin',
    `nombre_finca` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
    `usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
    PRIMARY KEY (`id_potrero`) USING BTREE,
    INDEX `FK_finca` (`id_finca`) USING BTREE,
    INDEX `FK_usuarios` (`usuario_id`) USING BTREE,
    CONSTRAINT `FK_finca` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT `FK_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE CASCADE ON DELETE CASCADE
)
COLLATE='latin1_bin'
ENGINE=InnoDB;

ALTER TABLE `bovinos`
	ADD COLUMN `id_finca` INT(255) NULL AFTER `chip_asociado`,
	ADD COLUMN `nombre_finca` VARCHAR(300) NULL DEFAULT NULL AFTER `id_finca`,
	ADD CONSTRAINT `FK_bovinos_finca` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `capacidad_carga`
	ADD COLUMN `id_potrero` INT(255) NULL AFTER `periodo_ocupacion`,
	ADD COLUMN `id_finca` INT(255) NULL AFTER `dias_descanso`,
	ADD COLUMN `nombre_finca` VARCHAR(300) NULL DEFAULT NULL AFTER `id_finca`,
	ADD CONSTRAINT `FK_capacidad_carga_potreros` FOREIGN KEY (`id_potrero`) REFERENCES `potreros` (`id_potrero`) ON UPDATE CASCADE ON DELETE CASCADE,
	ADD CONSTRAINT `FK_capacidad_carga_fincas` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `empleados`
	ADD COLUMN `id_finca` INT(255) NULL AFTER `usuario_id`,
	ADD COLUMN `nombre_finca` VARCHAR(300) NULL DEFAULT NULL AFTER `id_finca`,
	ADD CONSTRAINT `FK_empleados_finca` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `facturas`
	ADD COLUMN `id_finca` INT(255) NULL AFTER `usuario_id`,
	ADD COLUMN `nombre_finca` VARCHAR(300) NULL DEFAULT NULL AFTER `id_finca`,
	ADD CONSTRAINT `FK_facturas_finca` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE `lotes_bovinos`
	ADD COLUMN `id_finca` INT(255) NULL AFTER `total_bovinos`,
	ADD COLUMN `nombre_finca` VARCHAR(300) NULL DEFAULT NULL AFTER `id_finca`,
	ADD CONSTRAINT `FK_lotes_bovinoss_finca` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE;


CREATE TABLE `indicadores_finca` (
	`id_indicadores_finca` INT(255) NOT NULL AUTO_INCREMENT,
	`perdida_de_terneros_finca` FLOAT NULL DEFAULT NULL,
	`tasa_supervivencia_finca` FLOAT NULL DEFAULT NULL,
	`total_animales_finca` INT(11) NULL DEFAULT NULL,
	`vacas_prenadas_porcentaje_finca` FLOAT NULL DEFAULT NULL,
	`animales_levante_finca` INT(11) NULL DEFAULT NULL,
	`animales_ceba_finca` INT(11) NULL DEFAULT NULL,
	`animales_leche_finca` INT(11) NULL DEFAULT NULL,
	`vacas_prenadas_finca` INT(11) NULL DEFAULT NULL,
	`vacas_vacias_finca` INT(11) NULL DEFAULT NULL,
	`animales_fallecidos_finca` INT(11) NULL DEFAULT NULL,
	`animales_vendidos_finca` INT(11) NULL DEFAULT NULL,
	`machos_finca` INT(11) NULL DEFAULT NULL,
	`hembras_finca` INT(11) NULL DEFAULT NULL,
	`vacas_en_ordeno_finca` INT(11) NULL DEFAULT NULL,
	`vacas_no_ordeno_finca` INT(11) NULL DEFAULT NULL,
	`porcentaje_ordeno_finca` FLOAT NULL DEFAULT NULL,
	`animales_rango_edades_0_9_finca` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_9_12_finca` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_12_24_finca` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_24_36_finca` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_mayor_36_finca` INT(11) NULL DEFAULT NULL,
	`animales_optimos_levante_finca` INT(11) NULL DEFAULT NULL,
	`animales_optimos_ceba_finca` INT(11) NULL DEFAULT NULL,
	`vientres_aptos_finca` INT(11) NULL DEFAULT NULL,
	`relacion_toros_vientres_aptos_finca` INT(11) NULL DEFAULT NULL,
	`interpretacion_relacion_toros_vientres_aptos_finca` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`total_unidades_animales_finca` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`IEP_hato_finca` FLOAT NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
   `id_finca` INT(255) NULL DEFAULT NULL COLLATE 'latin1_bin',
   `nombre_finca` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_indicadores_finca`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	INDEX `FK_finca` (`id_finca`) USING BTREE,
	CONSTRAINT `FK_finca_indicadores` FOREIGN KEY (`id_finca`) REFERENCES `fincas` (`id_finca`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `indicadores_FK` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.2', 'Nuevas tablas para fincas', '2025-01-10', 'jvega','N/A');