CREATE TABLE `ganancia_historica_peso` (
	`id_ganancia` INT(255) NOT NULL AUTO_INCREMENT,
	`id_bovino` INT(255) NOT NULL,
	`nombre_bovino` VARCHAR(300) NOT NULL,
	`peso_anterior` FLOAT NOT NULL,
	`peso_posterior` FLOAT NOT NULL,
	`fecha_anterior` DATE NOT NULL,
	`fecha_posterior` DATE NOT NULL,
	`dias` INT(255) NOT NULL,
	`ganancia_diaria_media` FLOAT NOT NULL,
	`usuario_id` VARCHAR(300) NOT NULL,
	PRIMARY KEY (`id_ganancia`),
	CONSTRAINT `FK__usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='latin1_bin'
;
INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.3', 'nueva tabla de gananacias historicas de peso', '2024-03-17', 'Jose Vega');