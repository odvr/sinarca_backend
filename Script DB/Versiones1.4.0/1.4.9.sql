CREATE TABLE `reportes_semanales` (
	`id_reporte` INT(11) NOT NULL AUTO_INCREMENT,
	`fecha_generacion` DATETIME NULL DEFAULT NULL,
	`total_animales` INT(11) NULL DEFAULT NULL,
	`animales_produccion_leche` INT(11) NULL DEFAULT NULL,
	`animales_levante` INT(11) NULL DEFAULT NULL,
	`animales_ceba` INT(11) NULL DEFAULT NULL,
	`nacimientos_semanales` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`porcentaje_endogamia` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`animales_muertos_semanales` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`animales_vendidos_semanales` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`animales_comprados_semanales` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`registro_pesos_semanales` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`historial_perdida_terneros_anual` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`bovinos_descartes` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`historial_natalidad_paricion_real` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`periodo_iep_promedio` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`natalidad_paricion_real` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tasa_supervivencia_actual` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`intervalo_entre_partos` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`porcentaje_ordeno` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`vacas_vacias` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`vacas_prenadas` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`porcentaje_prenadas` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`proximos_periodos_secado` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`planes_sanitarios_lotes_agendados` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`proyecciones_partos` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`animales_optimos_levante` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`animales_optimos_ceba` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`ventas_totales` INT(11) NULL DEFAULT NULL,
	`total_compras` INT(11) NULL DEFAULT NULL,
	`total_nomina` INT(11) NULL DEFAULT NULL,
	`saldos_totales` INT(11) NULL DEFAULT NULL,
	`saldos_promedios` INT(11) NULL DEFAULT NULL,
	`facturacion_anual` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`perdida_de_terneros` FLOAT NULL DEFAULT NULL,
	`machos` INT(11) NULL DEFAULT NULL,
	`hembras` INT(11) NULL DEFAULT NULL,
	`vacas_en_ordeno` INT(11) NULL DEFAULT NULL,
	`vacas_no_ordeno` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_0_9` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_9_12` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_12_24` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_24_36` INT(11) NULL DEFAULT NULL,
	`animales_rango_edades_mayor_36` INT(11) NULL DEFAULT NULL,
	`vientres_aptos` INT(11) NULL DEFAULT NULL,
	`relacion_toros_vientres_aptos` INT(11) NULL DEFAULT NULL,
	`interpretacion_relacion_toros_vientres_aptos` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`total_unidades_animales` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`IEP_hato` FLOAT NULL DEFAULT NULL,
	PRIMARY KEY (`id_reporte`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `reportes_semanales_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
AUTO_INCREMENT=337
;



INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.9', 'Se agrega  nueva tabla que contendra la información sobre los reportes semanales de cada Usuario', '2025-03-10', 'ovega','Requiere actualización FrondEnd V1.5.7 ');