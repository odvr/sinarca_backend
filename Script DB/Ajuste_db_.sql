
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