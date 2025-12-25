# app/agents/schema_agent.py
from app.services.postgres_service import PostgresService

class SchemaAgent:
    def __init__(self):
        self.pg = PostgresService()

    def run(self) -> dict:
        """
        DB 스키마를 한글 컬럼명으로 LLM에 제공
        {테이블명: {"columns": {한글컬럼: 타입}}}
        """
        return self.pg.fetch_schema()
