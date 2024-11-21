ALTER TABLE `usuarios`
	ADD COLUMN `codigo_asociacion` VARCHAR(300) NULL DEFAULT NULL AFTER `correo_electronico`;



CREATE TABLE `asociados` (
	`id_asociado` INT(11) NULL DEFAULT NULL,
	`correo` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`telefono` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`codigo` VARCHAR(100) NULL DEFAULT NULL COLLATE 'latin1_bin',
	`fecha_creacion` DATE NULL DEFAULT NULL
)
COLLATE='latin1_bin'
ENGINE=InnoDB
;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.8', 'Se agrega una nuevo campo para el registro de Asociados', '2024-11-20', 'odvr','Versiones superiores a FronTend 1.4.4');