
use sinarca;
/* Se agrega una nueva tabla de dias abiertos*/
ALTER TABLE produccion_leche
ADD COLUMN dias_abiertos Integer;


/* Ajustes para la tabla de partos**/

ALTER TABLE partos
ADD COLUMN notificacion VARCHAR(300),
ADD COLUMN tipo VARCHAR(300),
ADD COLUMN id_reproductor VARCHAR(300),
ADD COLUMN nombre_bovino_reproductor VARCHAR(300);


/*Ajuste para la tabla de palpaciones*/

ALTER TABLE palpaciones
ADD COLUMN notificacion VARCHAR(300),
ADD COLUMN tipo VARCHAR(300),
ADD COLUMN id_reproductor VARCHAR(300),
ADD COLUMN nombre_bovino_reproductor VARCHAR(300);


/*Creación de la nueva tabla de dias abiertos*/

CREATE TABLE dias_abiertos (
    id_dias_abiertos INT PRIMARY KEY,
    id_bovino INT,
    nombre_bovino VARCHAR(300),
    fecha_parto DATE,
    fecha_prenez DATE,
    dias_abiertos INT,
    usuario_id VARCHAR(300),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.0.1', '', '2023-11-30', 'Jose Vega', 'N/A');