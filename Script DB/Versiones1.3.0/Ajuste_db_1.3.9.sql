ALTER TABLE `usuarios`
	ADD COLUMN `tipo_usuario` VARCHAR(300) NULL DEFAULT NULL AFTER `codigo_asociacion`;



-- Actualizar todos los usuarios con tipo_usuario = 'admin'
UPDATE `usuarios`
SET `tipo_usuario` = 'admin';

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.9', 'Nuevo campo de roles de usuarios', '2024-11-25', 'odvr','Versiones superiores a FronTend 1.4.6');