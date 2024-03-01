/*Ajuste a tabla de partos (registro de mosntas)*/
ALTER TABLE `partos`
	DROP FOREIGN KEY `partos_ibfk_1`;

/*Ajuste a tabla de registro de celos*/
ALTER TABLE `registro_celos`
ADD COLUMN servicio VARCHAR(300);
 ADD COLUMN `id_servicio` INT(255) NULL AFTER `usuario_id`,
	ADD CONSTRAINT `FK_registro_celos_partos` FOREIGN KEY (`id_servicio`) REFERENCES `partos` (`id_parto`) ON UPDATE RESTRICT ON DELETE RESTRICT;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.8', 'Se ajusta tabla de registro de montas', '2024-03-01', 'Jose Vega'
');

