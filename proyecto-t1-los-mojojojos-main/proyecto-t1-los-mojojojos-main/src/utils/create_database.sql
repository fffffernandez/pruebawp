
-- Borrar la tabla si ya existe
DROP TABLE IF EXISTS consumo_granada;

-- Crear la tabla consumo_granada con las columnas especificadas
CREATE TABLE consumo_granada (
    consumption_kwh DECIMAL(10,3),
    temperature DECIMAL(5,2),
    hour INT,
    month INT,
    day_of_week INT,
    day_of_month INT,
    year INT,
    hour_sin DECIMAL(10,5),
    hour_cos DECIMAL(10,5),
    month_sin DECIMAL(10,5),
    month_cos DECIMAL(10,5),
    is_weekend INT,
    is_holiday INT,
    is_non_working INT,
    temp_sq DECIMAL(10,5),
    zona_Albaicin_Alto INT,
    zona_Albaicin_Bajo INT,
    zona_Bola_De_Oro INT,
    zona_Camino_Ronda INT,
    zona_Cartuja INT,
    zona_Centro_Catedral INT,
    zona_Cervantes INT,
    zona_Chana_Barrio INT,
    zona_Chana_Bobadilla INT,
    zona_Fuentenueva INT,
    zona_Mercagranada INT,
    zona_Norte_Almanjayar INT,
    zona_Pedro_Antonio INT,
    zona_Periodistas INT,
    zona_Plaza_Toros INT,
    zona_Pts_Tecnologico INT,
    zona_Realejo INT,
    zona_Sacromonte INT,
    zona_Zaidin_Nuevo INT,
    zona_Zaidin_Vergeles INT
);

-- Confirmación de creación de la tabla
SELECT 'Tabla consumo_granada creada exitosamente.' AS mensaje;

-- Importar datos desde un archivo CSV (ajustar la ruta del archivo según sea necesario)
-- Nosotros lo hacemos desde el pgadmin directamente.