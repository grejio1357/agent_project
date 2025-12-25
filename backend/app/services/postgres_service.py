# app/services/postgres_service.py
import psycopg2
from app.core.settings import settings
from typing import List, Tuple

# 한글 ↔ 영어 컬럼명 매핑
COLUMN_MAP = {
    "연도": "year",
    "지역": "region",
    "작물": "crop",
    "재배유형": "cultivation_type",
    "평당수확량": "yield_kg_10a",
    "총생산량": "production_ton"
}

class PostgresService:
    def __init__(self):
        self.conn = None

    def _connect(self):
        """
        PostgreSQL 연결을 생성 또는 재사용
        """
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                dbname=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
            )

    def fetch_schema(self) -> dict:
        """
        DB 스키마 조회 후 LLM에게 보여줄 때 한글 컬럼명으로 변환
        반환: {
            "테이블명": {
                "columns": {
                    "한글컬럼명": "데이터타입",
                    ...
                }
            }
        }
        """
        self._connect()
        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        schema = {}
        with self.conn.cursor() as cur:
            cur.execute(query)
            for table, column, dtype in cur.fetchall():
                if table not in schema:
                    schema[table] = {"columns": {}}
                # 영어 컬럼명을 한글로 매핑
                kor_column = next((k for k, v in COLUMN_MAP.items() if v == column), column)
                schema[table]["columns"][kor_column] = dtype
        return schema

    def run(self, sql: str) -> List[Tuple]:
        """
        SQL 실행 전 한글 컬럼명을 영어 컬럼명으로 변환 후 실행
        반환: [(row1_col1, row1_col2, ...), ...]
        """
        self._connect()

        # 1️⃣ SQL 내 한글 컬럼명 → 영어 컬럼명 치환
        for kor, eng in COLUMN_MAP.items():
            sql = sql.replace(kor, eng)

        with self.conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
