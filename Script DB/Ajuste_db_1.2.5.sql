/*
Creación de la tabla de eventos
**/


CREATE TABLE `eventos_asociados_lotes` (
	`id_eventos_asociados` INT NOT NULL AUTO_INCREMENT,
	`id_lote_asociado` VARCHAR(300) NULL DEFAULT NULL,
	`nombre_lote` VARCHAR(300) NULL DEFAULT NULL,
	`nombre_evento` VARCHAR(300) NULL DEFAULT NULL,
	`estado_evento` VARCHAR(300) NULL DEFAULT NULL,
	`usuario_id` VARCHAR(300) NULL DEFAULT NULL,
	PRIMARY KEY (`id_eventos_asociados`)
)
COLLATE='latin1_bin';



ALTER TABLE `eventos_asociados_lotes`
	ADD CONSTRAINT `FK_eventos_asociados_lotes_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE NO ACTION ON DELETE NO ACTION;


ALTER TABLE `eventos_asociados_lotes`
	ADD COLUMN `FechaNotificacionRecienNacido` DATE NULL DEFAULT NULL AFTER `estado_evento`;
S