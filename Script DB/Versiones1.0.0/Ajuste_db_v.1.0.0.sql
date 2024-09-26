
/*
Se crea el ajustes de nueva tabla de db para el registro de la marca
*/
CREATE TABLE registro_marca (
    id_registro_marca INT PRIMARY KEY,
    ruta_marca VARCHAR(500),
    nombre_marca_propietario VARCHAR(50),
    usuario_id VARCHAR(300),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

/*
Se realiza ajusta en la tabla de bovinos para la ruta
**/

ALTER TABLE `bovinos`
	ADD COLUMN `ruta_imagen_marca` VARCHAR(300) NULL DEFAULT NULL AFTER `ruta_fisica_foto_perfil`;
SELECT `DEFAULT_COLLATION_NAME` FROM `information_schema`.`SCHEMATA` WHERE `SCHEMA_NAME`='sinarca';


/*Se crea la tabla de configuraciones*/

CREATE TABLE configuracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_aplicacion VARCHAR(255) NOT NULL,
    version VARCHAR(20) NOT NULL,
    descripcion VARCHAR(100),
    fecha_actualizacion DATE,
    responsable_actualizacion VARCHAR(100),
    observaciones VARCHAR(100)
);



/***/
INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.0', '', '2023-11-30', 'Omar Vega', 'N/A');