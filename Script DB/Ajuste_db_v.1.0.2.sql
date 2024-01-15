/**Ajuste de campo de inceminación*/
ALTER TABLE arbol_genealogico
ADD COLUMN inseminacion VARCHAR(300);

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.2', '', '2024-01-15', 'Omar Vega', 'Se agrega un nuevo campo en el arbol genialogico para arbol de decisiones');

