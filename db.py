import os
import psycopg2

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")  # Use environment variable for PostgreSQL connection

def get_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn
