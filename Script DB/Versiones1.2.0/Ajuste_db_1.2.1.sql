/*
Se realiza la creaciòn de  para asignar el numero de Lote seleccionado
*/
ALTER TABLE `bovinos`
	ADD COLUMN `nombre_lote_bovino` VARCHAR(300) NULL DEFAULT NULL AFTER `edad_destete`;

/*
Creaciòn de Tabla de Lotes Utilizada como tabla de referencia
*/

CREATE TABLE `lotes_bovinos` (
	`id_lote_bovinos` INT(11) NOT NULL AUTO_INCREMENT,
	`nombre_lote` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`estado` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`ubicacion` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tipo_uso` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`tamano_lote` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`observaciones` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
	UNIQUE INDEX `id_lote_bovinos` (`id_lote_bovinos`) USING BTREE,
	INDEX `FK_lotes_bovinos_usuarios` (`usuario_id`) USING BTREE,
	CONSTRAINT `FK_lotes_bovinos_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `sinarca`.`usuarios` (`usuario_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.1', 'Se agrega una Nueva Columna en Bovinos y Nueva Tabla de Lotes', '2024-06-06', 'Omar Vega ','Se requiere ajuste FrondEnd V.1.1.6 o superior');