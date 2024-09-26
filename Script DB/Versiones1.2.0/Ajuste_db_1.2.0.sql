ALTER TABLE `periodos_lactancia`
	DROP FOREIGN KEY `FK_periodos_lactancia_historial_partos`;
ALTER TABLE `periodos_lactancia`
	ADD CONSTRAINT `FK_periodos_lactancia_historial_partos` FOREIGN KEY (`id_parto`) REFERENCES `sinarca`.`historial_partos` (`id_parto`) ON UPDATE CASCADE ON DELETE CASCADE;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.0', 'Se realiza ajuste para el Bug de producción de leche', '2024-05-21', 'Omar Vega ',' Ajuste para eliminación en cascada de la tabla de producción');