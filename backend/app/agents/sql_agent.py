from typing import Optional
from app.core.llm import llm
from app.prompts.text2sql_prompt import (
    SYSTEM_PROMPT,
    INSTRUCTION_PROMPT,
    EXAMPLES
)


class SQLAgent:
    def run(
        self,
        question: str,
        schema: dict,
        error_hint: Optional[str] = None,
    ) -> str:
        """
        Generate SQL query from natural language question.
        If error_hint is provided, use it as a reference for retry.
        """

        schema_text = self._format_schema(schema)

        error_section = ""
        if error_hint:
            error_section = f"""
Note:
The previous SQL attempt was rejected for the following reason:
- {error_hint}

Please consider this information when generating the SQL again.
"""

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

        response = llm.invoke(prompt)
        return response.content.strip()

    def _format_schema(self, schema: dict) -> str:
        lines = []
        for table, meta in schema.items():
            lines.append(f"Table: {table}")
            for col, dtype in meta["columns"].items():
                lines.append(f"  - {col}: {dtype}")
        return "\n".join(lines)

