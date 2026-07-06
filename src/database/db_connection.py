"""
Database Connection Module
Multi-Touch Marketing Attribution & ROI Dashboard
"""

import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

# Load environment variables from .env
load_dotenv()


def _get_db_url() -> str:
    """Build a PostgreSQL connection URL from environment variables."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "marketing_attribution")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def get_engine() -> Engine:
    """
    Return a SQLAlchemy Engine for use with pd.read_sql().

    Returns:
        sqlalchemy.Engine: Connected engine instance.
    """
    return create_engine(_get_db_url())


def get_connection():
    """
    Establish and return a PostgreSQL database connection.

    Returns:
        psycopg2.connection: Active database connection object.

    Raises:
        OperationalError: If connection to the database fails.
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "marketing_attribution"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
        )
        return connection
    except OperationalError as e:
        print(f"[ERROR] Could not connect to database: {e}")
        raise


def test_connection() -> bool:
    """
    Test if the database connection is healthy.

    Returns:
        bool: True if connection is successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        print("[INFO] Database connection successful.")
        return True
    except OperationalError:
        print("[ERROR] Database connection failed.")
        return False


if __name__ == "__main__":
    test_connection()
