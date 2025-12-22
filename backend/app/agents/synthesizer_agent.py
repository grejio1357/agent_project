# app/agents/synthesizer_agent.py
from typing import List, Any, Optional
from app.core.llm import llm


class SynthesizerAgent:
    def run(
        self,
        question: str,
        sql_result: Optional[List[Any]] = None,
        rag_docs: Optional[List[str]] = None,
    ) -> str:
        """
        Generate final natural language answer
        using SQL results and/or RAG documents.
        """

        context_parts = []

        # 1️⃣ SQL 결과 (사실)
        if sql_result:
            context_parts.append(
                "Structured Data (SQL Result):\n"
                f"{sql_result}"
            )

        # 2️⃣ RAG 문서 (설명 근거)
        if rag_docs:
            joined_docs = "\n\n".join(rag_docs)
            context_parts.append(
                "Reference Documents:\n"
                f"{joined_docs}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
You are an agricultural data assistant.

Answer the user's question using ONLY the information provided
in the context below.

Rules:
- If numerical results are provided, use them as factual evidence.
- Do NOT invent numbers or facts.
- If documents are provided, use them to explain or justify the answer.
- If both are provided, combine them naturally.
- If information is insufficient, say so clearly.

Question:
{question}

Context:
{context}

Answer in Korean, clearly and concisely.
"""

        response = llm.invoke(prompt)
        return response.content.strip()
