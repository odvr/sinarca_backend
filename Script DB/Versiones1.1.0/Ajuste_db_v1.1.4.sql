CREATE TABLE `natalidad_o_paricion_real` (
	`id_natalidad` INT(255) NOT NULL AUTO_INCREMENT,
	`periodo` INT(255) NOT NULL,
	`intervalo_entre_partos_periodo` FLOAT NOT NULL,
	`natalidad_paricion_real` FLOAT NOT NULL,
	`usuario_id` VARCHAR(300) NOT NULL,
	PRIMARY KEY (`id_natalidad`),
	CONSTRAINT `FK__usuarios_natalidad` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.4', 'nueva tabla de natalidades (paricion real)', '2024-03-17', 'Jose Vega');