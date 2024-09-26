ALTER TABLE bovinos
ADD COLUMN fecha_de_ingreso_hato DATETIME,
ADD COLUMN fecha_de_ingreso_sistema DATETIME;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.1.1', 'Campos de Ingreso Del Sistema y Hato Ganadero', '2024-03-14', 'Omar Vega',' Requiere actualizacion frondEnd');