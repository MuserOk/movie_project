-- Cargar datos en la tabla `movies_popularity`
INSERT INTO movies_popularity (movie_id, title, popularity_category)
SELECT movie_id, title, popularity_category
FROM movies
WHERE popularity_category IS NOT NULL;

