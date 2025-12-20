from app.services.faiss_service import FaissService
from app.core.llm import llm
from app.prompts.rag_prompt import SYSTEM_PROMPT, RAG_TEMPLATE


class RAGAgent:
    def __init__(self):
        self.faiss = FaissService()

    def run(self, question: str) -> str:
        docs = self.faiss.search(question)

        context = "\n\n".join(docs)

        prompt = f"""
{SYSTEM_PROMPT}

{RAG_TEMPLATE.format(
    context=context,
    question=question
)}
"""

        response = llm.invoke(prompt)
        return response.content.strip()
