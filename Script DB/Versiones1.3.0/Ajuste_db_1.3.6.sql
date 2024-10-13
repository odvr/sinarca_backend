ALTER TABLE `empleados`
	ADD COLUMN `email` VARCHAR(100) NULL DEFAULT NULL AFTER `numero_seguridad_social`,
	ADD COLUMN `telefono` VARCHAR(100) NULL DEFAULT NULL AFTER `email`,
	ADD COLUMN `direccion` VARCHAR(100) NULL DEFAULT NULL AFTER `telefono`,
	ADD COLUMN `departamento` VARCHAR(100) NULL DEFAULT NULL AFTER `direccion`;


ALTER TABLE `empleados`
	CHANGE COLUMN `fecha_contratación` `fecha_contratacion` DATE NULL DEFAULT NULL AFTER `salario_base`;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.6', 'Se agregan Nuevos Campos en Empleados', '2024-10-12', 'odvr','Versiones superiores a FronTend 1.4.3');