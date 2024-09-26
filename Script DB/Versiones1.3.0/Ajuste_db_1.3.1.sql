/*
Se agrega nuevo campo para validar la cantidad de notificaciones enviadas
**/

ALTER TABLE `eventos_asociados_lotes`
	ADD COLUMN `notificaciones_generadas` INT NULL DEFAULT NULL AFTER `FechaNotificacion`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.1', 'Se agrega Nuevo campo que cuenta las notificaciones Enviadas', '2024-07-08', 'odvr','Se requiere Versión FrodTend V.1.3.3 o superior');