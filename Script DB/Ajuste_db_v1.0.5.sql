
CREATE TABLE IF NOT EXISTS canastillas (
    id_canastilla INT PRIMARY KEY,
    nombre_canastilla VARCHAR(300),
    unidades_disponibles INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);


ALTER TABLE registro_pajillas
ADD COLUMN unidades INT,
ADD COLUMN precio INT,
ADD COLUMN nombre_canastilla VARCHAR(300),
ADD COLUMN id_canastilla INT,
ADD
FOREIGN KEY (id_canastilla) REFERENCES canastillas(id_canastilla);



INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.5', 'Se agrega nueva tabla de canstillas y parametros a la tabla de pajillas y se crean funciones de conteo y eliminacion de canastillas', '2024-02-08', 'Jose Vega', 'Se requiere acutualización del FrondEnd versión V.1.0.3 o superior
');

