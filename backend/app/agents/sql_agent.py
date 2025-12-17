from app.core.llm import llm
from app.prompts.text2sql_prompt import (
    SYSTEM_PROMPT,
    INSTRUCTION_PROMPT,
    EXAMPLES
)

class SQLAgent:
    def run(self, question: str, schema: dict) -> str:
        """
        Generate SQL query from natural language question.
        """

        schema_text = self._format_schema(schema)

        prompt = f"""
{SYSTEM_PROMPT}

{INSTRUCTION_PROMPT}

Schema:
{schema_text}

{EXAMPLES}

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
