# app/services/postgres_service.py
import psycopg2
from app.core.settings import settings

class PostgresService:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
        )

    def fetch_schema(self):
        query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
