CREATE TABLE `manejo_ternero_recien_nacido_lotes` (
	`id_manejo_recien_nacido_lote` INT NOT NULL AUTO_INCREMENT,
	`estado_solicitud_recien_nacido` VARCHAR(50) NULL DEFAULT NULL,
	`id_bovino` INT NULL DEFAULT NULL,
	`nombre_bovino` VARCHAR(50) NULL DEFAULT NULL,
	`estado_respiratorio_inicial_lote` VARCHAR(300) NULL DEFAULT NULL,
	`fecha_desinfeccion_lote` VARCHAR(300) NULL DEFAULT NULL,
	`producto_usado_lote` VARCHAR(300) NULL DEFAULT NULL,
	`metodo_aplicacion_lote` VARCHAR(300) NULL DEFAULT NULL,
	`notificar_evento_lote` VARCHAR(300) NULL DEFAULT NULL,
	PRIMARY KEY (`id_manejo_recien_nacido_lote`),
	UNIQUE INDEX `id_manejo_recien_nacido_lote` (`id_manejo_recien_nacido_lote`)
)
COLLATE='latin1_bin';


ALTER TABLE `manejo_ternero_recien_nacido_lotes`
	ADD COLUMN `usuario_id` VARCHAR(300) NULL DEFAULT NULL AFTER `notificar_evento_lote`,
	ADD CONSTRAINT `FK_manejo_ternero_recien_nacido_lotes_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE NO ACTION ON DELETE NO ACTION;



ALTER TABLE `manejo_ternero_recien_nacido_lotes`
	ADD COLUMN `nombre_lote_asociado` VARCHAR(300) NULL DEFAULT NULL AFTER `estado_solicitud_recien_nacido`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.4', 'Nueva Tabla para aplicada para las Notificaciones del plan Sanitario', '2024-06-26', 'Omar Vega ','Se requiere Versión FrodTend V.1.2.6 o superior');