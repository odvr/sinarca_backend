ALTER TABLE `usuarios`
	ADD COLUMN `indicador_pais` INT NULL AFTER `ultimo_login`;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.5.3', 'Se agrega un nuevo campo Para indicador de País para Notificaciones Vía  whatsapp', '2025-04-16', 'ovega','Se requiere actualizar a la versión V.1.5.9 del FrondEnd ');