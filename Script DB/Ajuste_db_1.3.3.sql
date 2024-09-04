CREATE TABLE `enviar_correos_publicidad` (
	`id_envio_correo_publicidad` INT(11) NOT NULL AUTO_INCREMENT,
	`correo_enviado` VARCHAR(100) NOT NULL DEFAULT '' COLLATE 'latin1_bin',
	`fecha_envio` DATETIME NULL DEFAULT NULL,
	`estado_envio` VARCHAR(100) NOT NULL DEFAULT '' COLLATE 'latin1_bin',
	PRIMARY KEY (`id_envio_correo_publicidad`) USING BTREE,
	UNIQUE INDEX `id_envio_correo_publicidad` (`id_envio_correo_publicidad`) USING BTREE
)
COLLATE='latin1_bin'
ENGINE=InnoDB
AUTO_INCREMENT=2
;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.3', 'Nueva tabla para el envio de correos de publicidad', '2024-09-03', 'odvega','Versiones superiores a FronTend V.1.3.8');