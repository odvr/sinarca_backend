ALTER TABLE `empleados`
	ADD COLUMN `tipo_contrato` VARCHAR(100) NULL DEFAULT NULL AFTER `departamento`,
	ADD COLUMN `periodicidad_pago` VARCHAR(100) NULL DEFAULT NULL AFTER `tipo_contrato`,
	ADD COLUMN `detalles` VARCHAR(500) NULL DEFAULT NULL AFTER `periodicidad_pago`;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='sinarca';
ALTER TABLE `empleados`
	ADD COLUMN `estado` VARCHAR(100) NULL DEFAULT NULL AFTER `detalles`;
ALTER TABLE `empleados`
	ADD COLUMN `fecha_retiro` DATE NULL DEFAULT NULL AFTER `estado`;
INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)

ALTER TABLE `nomina`
	ADD COLUMN `recargos` FLOAT NULL DEFAULT NULL AFTER `deducciones`;

DROP TABLE `movimientos_stock`;

ALTER TABLE `facturas`
	ADD COLUMN `destino` VARCHAR(150) NULL DEFAULT NULL AFTER `tipo_venta`;


ALTER TABLE `facturas`
	ADD COLUMN `lote_asociado` VARCHAR(300) NULL DEFAULT NULL AFTER `destino`;

ALTER TABLE `facturas`
	ADD COLUMN `radicado_factura` VARCHAR(500) NULL DEFAULT NULL AFTER `cliente_id`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.7', 'Modulo de Empleados Nuevos Campos', '2024-10-17', 'odvr','Versiones superiores a FronTend 1.4.4');