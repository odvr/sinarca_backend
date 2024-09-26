/* Se agrega una Nueva tabla de parametrizaciones de ceba y levante */
use sinarca;


CREATE TABLE IF NOT EXISTS parametros_levante_ceba (
    id_parametros INT(11) PRIMARY KEY,
    peso_levante INT(11),
    edad_levante INT(11),
    peso_ceba INT(11),
    edad_ceba INT(11),
    usuario_id VARCHAR(300),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.4', 'Se agrega una nueva tabla de parametrizaciones', '2024-02-01', 'Jose Vega', 'Se requiere acutualización del FrondEnd versión Git 718e9c2 o superior
');

