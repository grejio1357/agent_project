from typing import Optional, List, Tuple
from app.core.llm import LLMService
from app.prompts.text2sql_prompt import SYSTEM_PROMPT, INSTRUCTION_PROMPT, EXAMPLES
from app.services.postgres_service import PostgresService, COLUMN_MAP


class SQLAgent:
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()
        self.pg = PostgresService()  # PostgresService 연결

    def run(
        self,
        question: str,
        schema: dict,
        error_hint: Optional[str] = None,
    ) -> List[Tuple]:
        """
        1️⃣ 질문 → LLM SQL (한글 컬럼)
        2️⃣ SQL 실행 (한글 → 영어 컬럼 변환)
        3️⃣ 실행 결과 반환
        """
        schema_text = self._format_schema(schema)
        error_section = f"\nNote: 이전 SQL 실패 - {error_hint}\n" if error_hint else ""

        prompt = f"""
{SYSTEM_PROMPT}

{INSTRUCTION_PROMPT}

Schema:
{schema_text}

{EXAMPLES}

{error_section}

Question: {question}
SQL:
"""
        # 1️⃣ LLM 호출
        sql_response = self.llm.invoke(prompt).content.strip()

        # 2️⃣ PostgresService 실행 (한글 → 영어 컬럼 변환)
        result = self.pg.run(sql_response)

        return result

    def _format_schema(self, schema: dict) -> str:
        """Schema dict → 문자열"""
        lines = []
        for table, meta in schema.items():
            lines.append(f"Table: {table}")
            for col, dtype in meta["columns"].items():
                lines.append(f"  - {col}: {dtype}")
        return "\n".join(lines)

