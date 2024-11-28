CREATE TABLE `proveedores` (
	`proveedor_id` INT(11) NOT NULL AUTO_INCREMENT,
	`nombre` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`direccion` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`telefono` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`correo` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tipoCliente` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tipoPersona` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	PRIMARY KEY (`proveedor_id`) USING BTREE,
	INDEX `usuario_id` (`usuario_id`) USING BTREE,
	CONSTRAINT `proveedores_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
ENGINE=InnoDB
AUTO_INCREMENT=5
;

-- Nuevo campo en la tabla de facturas

ALTER TABLE `facturas`
	ADD COLUMN `nombre_cliente_proveedor` VARCHAR(300) NULL DEFAULT NULL AFTER `cliente_id`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.4.0', 'Nueva tabla de Proveedores', '2024-11-27', 'odvr','Versiones superiores a FronTend 1.4.7');