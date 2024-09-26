/**
  Ajuste en la tabla de total_bovino
  */

ALTER TABLE `lotes_bovinos`
	ADD COLUMN `total_bovinos` INT(100) NULL DEFAULT NULL AFTER `usuario_id`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.3', 'Se Agrega un campo para contar la cantidad de Lotes', '2024-06-20', 'Omar Vega ','');