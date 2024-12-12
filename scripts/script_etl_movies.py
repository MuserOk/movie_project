import os # para gestionar las variables de ntorno y trabajar con rutas de archivos
import requests # para interactuar con la api (solicitudes get , post)
import pyodbc #relacionar pyrhon con base de datos (escalable a futuro/ actualizaciones constantes)
import json #por datos en formato json (conversion)

# Cargar variables de entorno desde un archivo .env
from dotenv import load_dotenv # dotenv cargar variables de entorno(seguridad:archivos con datos snsibles)
load_dotenv()

# Variables de configuración desde el archivo .env
API_KEY = os.getenv("TMDB_API_KEY")

# Verificar si la clave fue cargada correctamente
if not API_KEY:
    print("La clave de la API no se cargó correctamente.")

DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Ruta de los archivos SQL
CREATE_TABLE_SQL = "scripts/create_table_Movies.sql"
LOAD_TABLE_SQL = "scripts/load_table_Movies.sql"

# Configuración de conexión a la base de datos (pyodbc actúa aquí)
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD}"
)

# URL base de la API de TMDB
API_BASE_URL = "https://api.themoviedb.org/3/movie/popular"

# Constante para definir el límite de películas a extraer
LIMIT = 50  # Cambia este valor según lo necesites

# Función para ejecutar un script SQL desde un archivo
def execute_sql_file(file_path):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Leer y ejecutar el archivo SQL
        with open(file_path, "r", encoding="utf-8") as sql_file:
            sql_script = sql_file.read()
            cursor.execute(sql_script)
            conn.commit()

        print(f"Archivo {file_path} ejecutado exitosamente.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al ejecutar el archivo {file_path}: {e}")

# Función para extraer datos de la API de TMDB
def extract_movies_data(limit):
    movies = []
    page = 1

    while len(movies) < limit:
        try:
            url = f"{API_BASE_URL}?api_key={API_KEY}&page={page}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Agregar películas de la página actual al resultado
            for movie in data.get("results", []):
                if len(movies) < limit:
                    movies.append(movie)
                else:
                    break

            print(f"Página {page} procesada. Total de películas extraídas: {len(movies)}")
            page += 1

            # Detener si no hay más páginas
            if page > data.get("total_pages", 0):
                break
        except requests.exceptions.RequestException as e:
            print(f"Error al extraer datos de la API: {e}")
            break

    return movies

# Función para cargar datos en la tabla desde un archivo SQL
def insert_movies_data(file_path, data):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Leer la consulta de inserción desde el archivo cargar_tabla.sql
        with open(file_path, "r", encoding="utf-8") as sql_file:
            insert_query = sql_file.read()

        # Insertar datos en la tabla usando la consulta cargada
        for movie in data:
            cursor.execute(insert_query, (
                movie["id"],
                movie["title"],
                movie.get("release_date"),
                movie.get("original_language"),
                movie.get("vote_average"),
                movie.get("vote_count"),
                movie.get("popularity"),
                movie.get("overview"),
                json.dumps(movie.get("genre_ids", []))  # Convertir lista a JSON para almacenarla
            ))
        conn.commit()

        print("Datos insertados exitosamente en la tabla Movies.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al insertar datos usando {file_path}: {e}")

# Flujo principal del script
if __name__ == "__main__":
    # Paso 1: Crear la tabla
    execute_sql_file(CREATE_TABLE_SQL)

    # Paso 2: Extraer datos de la API
    peliculas_data = extract_movies_data(limit=50)  # Modifica el límite según lo que necesites

    # Paso 3: Insertar los datos en la tabla
    if peliculas_data:
        insert_movies_data(LOAD_TABLE_SQL, peliculas_data)
