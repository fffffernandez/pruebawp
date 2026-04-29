"""
Configuración y gestión de la conexión a la base de datos PostgreSQL
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', 5432),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}


@contextmanager
def get_db_connection():
    """
    Context manager para manejar conexiones a la base de datos.
    Asegura que las conexiones se cierren correctamente.
    """
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except psycopg2.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        raise
    finally:
        if conn:
            conn.close()


def test_connection():
    """
    Prueba la conexión a la base de datos y devuelve True si es exitosa.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print(f"✓ Conexión exitosa a PostgreSQL")
                print(f"  Versión: {version[0]}")
                return True
    except Exception as e:
        print(f"✗ Error al conectar: {e}")
        return False


def execute_query(query, params=None, fetch_one=False):
    """
    Ejecuta una consulta SELECT y retorna los resultados como diccionarios.
    
    Args:
        query: Consulta SQL a ejecutar
        params: Parámetros para la consulta (opcional)
        fetch_one: Si es True, retorna solo un registro
        
    Returns:
        Lista de diccionarios con los resultados o un diccionario si fetch_one=True
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch_one:
                    return dict(cur.fetchone()) if cur.rowcount > 0 else None
                return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        raise


def get_table_names():
    """
    Obtiene la lista de tablas en la base de datos.
    """
    query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """
    try:
        result = execute_query(query)
        return [row['table_name'] for row in result]
    except Exception as e:
        print(f"Error obteniendo nombres de tablas: {e}")
        return []


def get_table_columns(table_name):
    """
    Obtiene las columnas de una tabla específica.
    """
    query = """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = %s
        ORDER BY ordinal_position;
    """
    try:
        return execute_query(query, (table_name,))
    except Exception as e:
        print(f"Error obteniendo columnas de la tabla {table_name}: {e}")
        return []
