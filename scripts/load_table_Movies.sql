-- Inserción de datos en la tabla 'Movies' (valores a ser reemplazados desde Python)
INSERT INTO Movies (
    movie_id, 
    title, 
    release_date, 
    original_language, 
    vote_average, 
    vote_count, 
    popularity, 
    overview, 
    genre_ids
) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
