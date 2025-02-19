CREATE TABLE `produccion_general_leche` (
	`id_produccion_leche` INT(11) NOT NULL AUTO_INCREMENT,
	`leche` INT(11) NULL DEFAULT NULL,
	`fecha_ordeno` DATETIME NULL DEFAULT NULL,
	`fecha_registro_sistema` DATE NULL DEFAULT NULL,
	`precio_venta` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`detalles` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`id_produccion_leche`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `produccion_general_leche_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.6', 'Nueva Tabla General Leche', '2025-02-10', 'ovega','Se debe tener actualizado el FrondTend  V.1.5.4 o superiores');