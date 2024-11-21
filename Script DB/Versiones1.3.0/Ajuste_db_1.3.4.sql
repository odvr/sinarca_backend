


ALTER TABLE `ventas`
ADD COLUMN `peso_venta` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
ADD COLUMN `valor_kg_venta` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
ADD COLUMN `id_factura_asociada` INT(11) NULL DEFAULT NULL;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.4', 'Ajuste en la tabla de Ventas', '2024-09-26', 'odvega','Versiones superiores a FronTend 1.4.0');