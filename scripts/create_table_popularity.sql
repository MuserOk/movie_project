-- Crear tabla de popularidad si no existe
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'movies_popularity' AND xtype = 'U')
BEGIN
    CREATE TABLE movies_popularity (
        movie_id INT PRIMARY KEY,
        title NVARCHAR(255),
        popularity_category NVARCHAR(50)
    );
    PRINT 'Tabla movies_popularity creada exitosamente.'
END
ELSE
BEGIN
    PRINT 'La tabla movies_popularity ya existe.'
END
