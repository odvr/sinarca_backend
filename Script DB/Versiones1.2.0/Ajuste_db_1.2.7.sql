/*
Se agrega la un nuevo campo que envia el ID del Evento Asociado
*/

ALTER TABLE `descorne_lotes`
	ADD COLUMN `id_evento_lote_asociado` INT NULL DEFAULT NULL AFTER `nombre_lote_asociado`;


ALTER TABLE `control_parasitos_lote`
	ADD COLUMN `id_evento_lote_asociado` INT NULL DEFAULT NULL AFTER `nombre_lote_asociado`;

ALTER TABLE `registro_vacunacion_bovinos`
	ADD COLUMN `id_evento_lote_asociado` INT NULL DEFAULT NULL AFTER `nombre_lote_asociado`;

ALTER TABLE `control_podologia_lotes`
	ADD COLUMN `id_evento_lote_asociado` INT NULL DEFAULT NULL AFTER `nombre_lote_asociado`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.7', '', '2024-07-03', 'odvr','Se requiere Versión FrodTend V.1.2.9 o superior');