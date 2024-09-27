-- Verifica si la tabla `ventas` existe
IF NOT EXISTS (
    SELECT * FROM information_schema.tables
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
) THEN
    -- Crear la tabla `ventas` si no existe
    CREATE TABLE `ventas` (
        `id_venta` INT(11) NOT NULL AUTO_INCREMENT,
        `id_bovino` INT(11) NULL DEFAULT NULL,
        `numero_bono_venta` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `estado` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `fecha_venta` DATE NULL DEFAULT NULL,
        `precio_venta` INT(11) NULL DEFAULT NULL,
        `razon_venta` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `medio_pago` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `comprador` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `peso_venta` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `valor_kg_venta` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `id_factura_asociada` INT(11) NULL DEFAULT NULL,
        `usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        `nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin',
        PRIMARY KEY (`id_venta`) USING BTREE,
        INDEX `id_bovino` (`id_bovino`) USING BTREE,
        INDEX `usuario_id` (`usuario_id`) USING BTREE,
        CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_bovino`) REFERENCES `bovinos` (`id_bovino`) ON UPDATE RESTRICT ON DELETE RESTRICT,
        CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
    )
    COLLATE='latin1_bin'
    ENGINE=InnoDB
    AUTO_INCREMENT=23;
END IF;

-- Verifica si las columnas necesarias existen en la tabla `ventas`
-- Agrega cada columna si no está presente

-- id_bovino
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'id_bovino'
) THEN
    ALTER TABLE `ventas` ADD `id_bovino` INT(11) NULL DEFAULT NULL;
END IF;

-- numero_bono_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'numero_bono_venta'
) THEN
    ALTER TABLE `ventas` ADD `numero_bono_venta` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- estado
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'estado'
) THEN
    ALTER TABLE `ventas` ADD `estado` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- fecha_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'fecha_venta'
) THEN
    ALTER TABLE `ventas` ADD `fecha_venta` DATE NULL DEFAULT NULL;
END IF;

-- precio_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'precio_venta'
) THEN
    ALTER TABLE `ventas` ADD `precio_venta` INT(11) NULL DEFAULT NULL;
END IF;

-- razon_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'razon_venta'
) THEN
    ALTER TABLE `ventas` ADD `razon_venta` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- medio_pago
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'medio_pago'
) THEN
    ALTER TABLE `ventas` ADD `medio_pago` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- comprador
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'comprador'
) THEN
    ALTER TABLE `ventas` ADD `comprador` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- peso_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'peso_venta'
) THEN
    ALTER TABLE `ventas` ADD `peso_venta` VARCHAR(500) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- valor_kg_venta
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'valor_kg_venta'
) THEN
    ALTER TABLE `ventas` ADD `valor_kg_venta` VARCHAR(50) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- id_factura_asociada
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'id_factura_asociada'
) THEN
    ALTER TABLE `ventas` ADD `id_factura_asociada` INT(11) NULL DEFAULT NULL;
END IF;

-- usuario_id
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'usuario_id'
) THEN
    ALTER TABLE `ventas` ADD `usuario_id` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;

-- nombre_bovino
IF NOT EXISTS (
    SELECT * FROM information_schema.columns
    WHERE table_schema = 'nombre_de_tu_base_de_datos'
    AND table_name = 'ventas'
    AND column_name = 'nombre_bovino'
) THEN
    ALTER TABLE `ventas` ADD `nombre_bovino` VARCHAR(300) NULL DEFAULT NULL COLLATE 'latin1_bin';
END IF;


INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.3.4', 'Ajuste en la tabla de Ventas', '2024-09-26', 'odvega','Versiones superiores a FronTend 1.4.0');