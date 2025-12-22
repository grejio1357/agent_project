# app/agents/rag_agent.py
from typing import List
from app.services.faiss_service import FaissService


class RAGAgent:
    def __init__(self):
        self.faiss = FaissService()

    def run(self, question: str) -> List[str]:
        """
        Retrieve relevant documents for RAG.
        No LLM call here.
        """
        docs = self.faiss.search(question)

        if not docs:
            return []

        return docs
