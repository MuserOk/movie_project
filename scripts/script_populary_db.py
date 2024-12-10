from dotenv import load_dotenv
import os
import pyodbc

# Cargar variables de entorno
load_dotenv()

# Cargar las credenciales de la base de datos desde el archivo .env
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Función para conectarse a la base de datos
def connect_db():
    connection_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}'
    return pyodbc.connect(connection_str)

# Función para ejecutar un archivo SQL
def execute_sql_script(connection, script_path):
    with open(script_path, 'r') as file:
        sql_script = file.read()
    cursor = connection.cursor()
    cursor.execute(sql_script)
    cursor.commit()
    print(f"Archivo {script_path} ejecutado exitosamente.")

# Función principal
def main():
    try:
        # Conectar a la base de datos
        connection = connect_db()
        with connection.cursor() as cursor:
            # Verificar si hay datos en la tabla `movies`
            cursor.execute("SELECT COUNT(*) FROM movies")
            movie_count = cursor.fetchone()[0]

            if movie_count == 0:
                print("No hay datos en la tabla de películas. No se procederá a crear la tabla de popularidad.")
            else:
                print("Existen datos en la tabla `movies`, procediendo a crear la tabla `movies_popularity`...")
                execute_sql_script(connection, 'scripts/create_table_popularity.sql')

                # Clasificación de la popularidad y actualización de la tabla `movies_popularity`
                cursor.execute("SELECT movie_id, title, popularity FROM movies WHERE popularity IS NOT NULL")
                movie_data = cursor.fetchall()

                if not movie_data:
                    print("No se obtuvieron datos de películas para procesar.")
                else:
                    # Clasificación de popularidad y carga en la tabla `movies_popularity`
                    for row in movie_data:
                        movie_id = row[0]
                        title = row[1]
                        popularity = row[2]

                        # Clasificación de la popularidad
                        if popularity < 500:
                            popularity_category = 'BAJA'
                        elif 500 <= popularity <= 999:
                            popularity_category = 'MEDIA'
                        else:
                            popularity_category = 'ALTA'

                        # Verificar si el movie_id ya existe
                        cursor.execute("SELECT COUNT(*) FROM movies_popularity WHERE movie_id = ?", (movie_id,))
                        exists = cursor.fetchone()[0]

                        # Si no existe, insertar el nuevo registro
                        if exists == 0:
                            cursor.execute("""
                                INSERT INTO movies_popularity (movie_id, title, popularity_category)
                                VALUES (?, ?, ?)
                                """, (movie_id, title, popularity_category))

                    connection.commit()  # Confirmar cambios
                    print("Datos de popularidad cargados correctamente.")

    except Exception as e:
        print(f"Error al conectar o ejecutar consultas: {e}")

if __name__ == "__main__":
    main()
