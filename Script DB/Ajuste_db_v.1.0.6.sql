
use sinarca;
/* Ajustes para tabla de capacidad de carga*/

ALTER TABLE capacidad_carga
DROP COLUMN tipo_de_muestra;
DROP COLUMN carga_animal_recomendada;
DROP COLUMN capacidad_carga;
DROP COLUMN nombre_bovino;
ADD COLUMN periodo_ocupacion INT;
ADD COLUMN nombre_potrero VARCHAR(300);
ADD COLUMN interpretacion VARCHAR(300);

/* Ajustes para tabla de capacidad de carga (se cambia id de string a entero)*/
ALTER TABLE `capacidad_carga`
	CHANGE COLUMN `id_capacidad` `id_capacidad` INT(255) NOT NULL AUTO_INCREMENT FIRST;




INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.6', '', '2024-02-26', 'Jose Vega', 'N/A');