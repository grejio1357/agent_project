from typing import Optional, List, Tuple
from app.core.llm import LLMService
from app.prompts.text2sql_prompt import SYSTEM_PROMPT, INSTRUCTION_PROMPT, EXAMPLES


class SQLAgent:
    def __init__(self, llm_service: LLMService | None = None):
        self.llm = llm_service or LLMService()

    def run(
        self,
        question: str,
        schema: dict,
        error_hint: Optional[str] = None,
    ) -> List[Tuple]:

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
        sql_response = self.llm.invoke(prompt).strip()

        return sql_response

    def _format_schema(self, schema: dict) -> str:
        """Schema dict → 문자열"""
        lines = []
        for table, meta in schema.items():
            lines.append(f"Table: {table}")
            for col, dtype in meta["columns"].items():
                lines.append(f"  - {col}: {dtype}")
        return "\n".join(lines)

