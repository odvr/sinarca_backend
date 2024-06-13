ALTER TABLE `lotes_bovinos`
	DROP COLUMN `tamano_lote`;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.2.2', 'Se elimina el Campo de Tamaño de Lote', '2024-06-13', 'Omar Vega ','Se requiere ajuste FrondEnd  V.1.2.1 o superior');