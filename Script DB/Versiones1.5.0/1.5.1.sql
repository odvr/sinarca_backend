ALTER TABLE embriones_transferencias
ADD COLUMN raza_madre_biologica VARCHAR(300),
ADD COLUMN genetica_madre_biologica VARCHAR(300),
ADD COLUMN edad_madre_biologica VARCHAR(300),
ADD COLUMN historial_madre_biologica VARCHAR(300),
ADD COLUMN tratamientos_hormonales_madre_biologica VARCHAR(300),
ADD COLUMN raza_padre_biologico VARCHAR(300),
ADD COLUMN genetica_padre_biologico VARCHAR(300),
ADD COLUMN edad_padre_biologico VARCHAR(300),
ADD COLUMN historial_reproductivo_padre_biologico VARCHAR(300),
ADD COLUMN fecha_extracion DATE,
ADD COLUMN calidad_embrion VARCHAR(300),
ADD COLUMN metodo_recoleccion VARCHAR(300),
ADD COLUMN codigo_unico VARCHAR(300),
ADD COLUMN lote_procedencia VARCHAR(300),
ADD COLUMN caracteristicas_geneticas VARCHAR(300),
ADD COLUMN tanque_nitrogeno VARCHAR(300),
ADD COLUMN pajilla VARCHAR(300),
ADD COLUMN numero_canister VARCHAR(300),
ADD COLUMN historial_completo VARCHAR(300),
ADD COLUMN programacion_transferencia VARCHAR(300),
ADD COLUMN tecnica_utilizada VARCHAR(300);





INSERT INTO configuracion (nombre_aplicacion, version, descripcion, fecha_actualizacion, responsable_actualizacion, observaciones)
VALUES ('Ruta Ganadera', '1.5.1', 'Se realiza ajuste de nuevos campos para la tabla de embriones', '2025-04-12', 'ovega','Se requiere actualizar a la versión V.1.5.8 del FrondEnd ');