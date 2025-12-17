# app/agents/schema_agent.py
from app.services.postgres_service import PostgresService

class SchemaAgent:
    def __init__(self):
        self.pg = PostgresService()

    def run(self):
        rows = self.pg.fetch_schema()

        schema = {}
        for table, column, dtype in rows:
            if table not in schema:
                schema[table] = {"columns": {}}
            schema[table]["columns"][column] = dtype

        return schema