import os
import psycopg2

# Configuracion de base de datos
DATABASE_URL = os.getenv("DATABASE_URL")  # # Usa variable de entorno para hacer conexion a postgresql

def get_db():
    """Conectar a la base de datos Postgre."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn
