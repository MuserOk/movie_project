"Este producto utiliza la API de TMDB pero no está respaldado ni certificado por TMDB"

-------Descripción General--------
Propósito:
_________1- Extraer datos de películas desde la API de TMDB.
_________2- Transformar los datos de popularidad en categorías: Alta, Media y Baja.
_________3- Cargar los datos en SQL Server para su análisis posterior.

Características Principales:
_________Extraer columnas relevantes.
_________Almacenar los datos crudos en una tabla llamada movies en SQL Server.
_________Clasificar la popularidad de las películas y guardar los resultados en una tabla llamada movies_popularity.

Requisitos Previos:
_________Python 3.8 o superior.
_________Conexión activa a Internet.
_________Credenciales de acceso a la API de TMDB (obtenidas al crear una cuenta en TMDB).
_________SQL Server instalado y configurado.
_________Biblioteca de Python para conectarse a SQL Server (pyodbc o pymssql).

----DATOS A EXTRAER----
____movie_id 
____title 
____release_date 
____original_language 
____vote_average 
____vote_count 
____popularity 
____overview 
____genre_ids

---------------------

TABLA DE POPULARIDAD:
__ REALIZAR CON PYTHON movie_id title popularity_category valores que deberia tener (BAJA, MEDIA, ALTA)

---------------------