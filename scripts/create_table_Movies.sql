-- Verificar y crear la tabla 'Movies' si no existe
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Movies')
BEGIN
    CREATE TABLE Movies (
        movie_id INT PRIMARY KEY,
        title NVARCHAR(255),
        release_date DATE,
        original_language NVARCHAR(10),
        vote_average FLOAT,
        vote_count INT,
        popularity FLOAT,
        overview NVARCHAR(MAX),
        genre_ids NVARCHAR(MAX)
    );
END;
