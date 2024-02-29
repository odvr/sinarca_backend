/*se crea tabla de registro de celos*/

CREATE TABLE IF NOT EXISTS registro_celos (
    id_celo INT PRIMARY KEY,
    id_bovino INT,
    nombre_bovino VARCHAR(300),
    fecha_celo DATE,
    observaciones VARCHAR(300),
    usuario_id VARCHAR(300),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
	 );

/*se crea tabla de registro de tasas de concepcion*/
CREATE TABLE IF NOT EXISTS tasas_concepcion (
    id_tasa INT PRIMARY KEY,
    id_bovino INT,
    nombre_bovino VARCHAR(300),
    servicios_concepcion INT,
    fecha_prenez DATE,
    tasa_concepcion FLOAT,
    usuario_id VARCHAR(300),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

/* Ajustes para la tabla de partos**/

ALTER TABLE partos
ADD COLUMN observaciones VARCHAR(300);

ALTER TABLE `registro_celos`
	CHANGE COLUMN `id_celo` `id_celo` INT(255) NOT NULL AUTO_INCREMENT FIRST;

INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.7', 'Se agrega nueva tabla de registro de celos, una tabla para tasas de concepcion y se agrega campo de observaciones al registro de montas', '2024-02-29', 'Jose Vega', 'Se requiere acutualización del FrondEnd versión V.1.0.3 o superior
');

